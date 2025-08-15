from homeassistant.components.camera import Camera
import time
import logging
import requests
from fake_useragent import UserAgent
import logging
from .const import (
    FLORIDA_TRAFFIC_CAM_QUERY_URL, 
    IMAGES_DATA_KEY, 
    IMAGES_ID_INDEX, 
    IMAGES_ID_KEY,
    VIDEO_URL_KEY,
    FLORIDA_CAMERA_TOKEN_URL,
    CAMERA_TOKEN_KEY,
    CAMERA_SOURCE_ID_KEY,
    CAMERA_SYSTEM_SOURCE_ID_KEY,
    CAMERA_SOURCE_ID_URL,
    APPLICATION_JSON_HEADERS,
    FLORIDA_VIDEO_FEED_URL
)

_LOGGER = logging.getLogger(__name__)

class FloridaTrafficCameraCoordinator(Camera):
    def __init__(self, hass, camera_name):
        super().__init__()
        
        self.hass = hass
        self._attr_name = camera_name
        self.video_url = None
        self.camera_token = None
        self.video_session_token = None
        self.system_source_id = None
        self.source_id = None
        self.image_id = None
        self.fake_user_data = {
                "User-Agent": UserAgent().chrome,  # Random Chrome user agent
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
            }
                
    async def stream_source(self):
        try:
            await self.hass.async_add_executor_job(self._get_camera_id)
            await self.hass.async_add_executor_job(self._get_camera_token)
            await self.hass.async_add_executor_job(self._get_video_session_token)
            
            stream_url = FLORIDA_VIDEO_FEED_URL.format(self.video_url, self.video_session_token)
            
            _LOGGER.info(f"Using stream url for {self._attr_name}: {stream_url}")
            
            return FLORIDA_VIDEO_FEED_URL.format(self.video_url, self.video_session_token)
        
        except Exception as err:
            _LOGGER.error(f"Failed to fetch camera data: {err}")
            return None
        
    def _get_camera_id(self):
        try:
            response = requests.get(FLORIDA_TRAFFIC_CAM_QUERY_URL.format(self.name), headers=self.fake_user_data.copy())
            response.raise_for_status()
            
            images_data = response.json().get(IMAGES_DATA_KEY)
            self.image_id = images_data[IMAGES_ID_INDEX].get(IMAGES_ID_KEY)
            self.video_url = images_data[IMAGES_ID_INDEX].get(VIDEO_URL_KEY)
            
            _LOGGER.info(f"Camera: {self.name}, Image ID: {self.image_id}, Video URL: {self.video_url}")
            
        except Exception as e:
            _LOGGER.error(f"Unable to fetch camera id information. {e}")
            
    def _get_camera_token(self):
        try:
            response = requests.get(FLORIDA_CAMERA_TOKEN_URL.format(self.image_id, int(time.time() * 1000)), headers=self.fake_user_data.copy())
            response.raise_for_status()
            
            response_data = response.json()
            self.camera_token = response_data.get(CAMERA_TOKEN_KEY)
            self.source_id = response_data.get(CAMERA_SOURCE_ID_KEY)
            self.system_source_id = response_data.get(CAMERA_SYSTEM_SOURCE_ID_KEY)
            
            _LOGGER.info(f"Camera Token: {self.camera_token}, Source ID: {self.source_id}, System Source ID: {self.system_source_id}")
            
        except Exception as e:
            _LOGGER.error(f"Unable to get camera session information. {e}")
            
    def _get_video_session_token(self):
        try:
            payload = {
                CAMERA_SOURCE_ID_KEY : self.source_id,
                CAMERA_SYSTEM_SOURCE_ID_KEY : self.system_source_id,
                CAMERA_TOKEN_KEY : self.camera_token
            }
            
            headers = APPLICATION_JSON_HEADERS.copy()
            headers.update(self.fake_user_data.copy())
            
            response = requests.post(CAMERA_SOURCE_ID_URL, json=payload, headers=headers)
            response.raise_for_status()
            
            self.video_session_token = response.json()
            
            _LOGGER.info(f"Video Session Token: {self.video_session_token}")
            
        except Exception as e:
            _LOGGER.error(f"Unable to get video session token. {e}")