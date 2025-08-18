import time
import logging
import requests
from fake_useragent import UserAgent
import logging
import json
import re
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
    FLORIDA_VIDEO_FEED_URL,
    CAMERA_SNAPSHOT_URL,
    DATA_KEY,
    DATA_INDEX,
    HTTP_OK_RANGE,
    INDEX_URL_HEADER,
    XFLOW_KEY,
    INDEX_KEY
)

_LOGGER = logging.getLogger(__name__)

class FloridaTrafficCameraCoordinator():
    def __init__(self, hass, camera_name):
        
        self.hass = hass
        self._attr_name = camera_name
        self.video_url = None
        self.camera_token = None
        self.video_session_token = None
        self.system_source_id = None
        self.source_id = None
        self.image_id = None
        self.fake_user_data = None
        self.snapshot_url = None
        self.stream_url = None
        self.index_url = None
                
    async def stream_source(self):
        try:
            if self.fake_user_data is None:
                await self.hass.async_add_executor_job(self._create_fake_user_data)
                    
            if self.stream_url is not None:
                test_result = await self.hass.async_add_executor_job(self._test_stream_url)
                
                _LOGGER.debug(f"Result of the stream url {test_result}")
                
                if not test_result:
                    self.stream_url = None
                
            if self.stream_url is None:
                await self.hass.async_add_executor_job(self._get_camera_id)
                await self.hass.async_add_executor_job(self._get_camera_token)
                await self.hass.async_add_executor_job(self._get_video_session_token)
                
                self.index_url = FLORIDA_VIDEO_FEED_URL.format(self.video_url, self.video_session_token)
                
                xflow_path = await self.hass.async_add_executor_job(self._get_xflow_url)
                self.stream_url = f"{self.video_url.split(INDEX_KEY)[0]}{xflow_path}"
            
            _LOGGER.debug(f"Using stream url for {self._attr_name}: {self.stream_url}")
            
            return self.stream_url
        
        except Exception as err:
            _LOGGER.error(f"Failed to fetch camera data: {err}")
            return None
        
    async def perform_get_snapshot(self):
        try:
            if self.fake_user_data is None:
                await self.hass.async_add_executor_job(self._create_fake_user_data)
            
            if self.snapshot_url is None:
                await self.hass.async_add_executor_job(self._get_camera_id)
                
            return await self.hass.async_add_executor_job(self._get_snapshot)
        
        except Exception as error:
            _LOGGER.error(f"Unable to perform get snapshot for {self._attr_name}. {error}")
            return None
        
    def _get_xflow_url(self):
        try:
            header = INDEX_URL_HEADER.copy()
            header["User-Agent"] = self.fake_user_data["User-Agent"]
            header["Host"] = re.search(r"(dim-se\d+\.divas\.cloud:8200)", self.video_url).group(0)
            
            response = requests.get(self.index_url, headers=header, verify=False)
            response.raise_for_status()
            
            _LOGGER.debug(f"Reponse for index url: {response.text}")
            
            xflow_url = XFLOW_KEY
            for line in response.text.splitlines():
                if XFLOW_KEY in line:
                    xflow_url = f"{xflow_url}{line.split(XFLOW_KEY)[1]}"
                                        
            _LOGGER.debug(f"Got the xflow url: {xflow_url}")
            
            return xflow_url.strip()           
            
        except Exception as error:
            _LOGGER.error(f"Unable to post index url: {self.index_url}. {error}")
        
    def _create_fake_user_data(self):
        _LOGGER.debug("Fake user data")
        
        self.fake_user_data = {
                "User-Agent": str(UserAgent().chrome),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
            }
    
    def _test_stream_url(self):
        try:
            response = requests.head(self.stream_url, timeout=10, headers=self.fake_user_data, verify=False)
            
            _LOGGER.debug(f"Testing stream url status code. {response.status_code}")
            
            return HTTP_OK_RANGE["MIN"] <= response.status_code <= HTTP_OK_RANGE["MAX"]
        
        except Exception as e:
            _LOGGER.error(f"Failed to check stream url: {self.stream_url}. {e}")
            
            return False
        
    def _get_snapshot(self):
        try:
            reponse = requests.get(self.snapshot_url, verify=False)
            reponse.raise_for_status()
            
            _LOGGER.debug(f"Getting traffic camera snapshot {self._attr_name} using {self.snapshot_url}")
            
            return reponse.content
            
        except Exception as error:
            _LOGGER.error(f"Failed to get camera snapshot of {self._attr_name}. {error}")
            return None
        
    def _get_camera_id(self):
        try:
            response = requests.get(FLORIDA_TRAFFIC_CAM_QUERY_URL.format(self._attr_name), headers=self.fake_user_data.copy(), verify=False)
            response.raise_for_status()
            
            _LOGGER.debug(response.json())
            
            images_data = response.json().get(DATA_KEY)[DATA_INDEX][IMAGES_DATA_KEY]
            self.image_id = images_data[IMAGES_ID_INDEX].get(IMAGES_ID_KEY)
            self.video_url = images_data[IMAGES_ID_INDEX].get(VIDEO_URL_KEY)
            self.snapshot_url = CAMERA_SNAPSHOT_URL.format(self.image_id, int(time.time() * 1000))
            
            _LOGGER.debug(f"Camera: {self._attr_name}, \
                Image ID: {self.image_id}, \
                Video URL: {self.video_url}, \
                Snapshot URL: {self.snapshot_url}")
       
        except Exception as e:
            _LOGGER.error(f"Unable to fetch camera id information. {e}")
            return None
            
    def _get_camera_token(self):
        try:
            response = requests.get(FLORIDA_CAMERA_TOKEN_URL.format(self.image_id, int(time.time() * 1000)), headers=self.fake_user_data.copy(), verify=False)
            response.raise_for_status()
            
            response_data = response.json()
            self.camera_token = response_data.get(CAMERA_TOKEN_KEY)
            self.source_id = response_data.get(CAMERA_SOURCE_ID_KEY)
            self.system_source_id = response_data.get(CAMERA_SYSTEM_SOURCE_ID_KEY)
            
            _LOGGER.debug(f"Camera Token: {self.camera_token}, Source ID: {self.source_id}, System Source ID: {self.system_source_id}")
            
        except Exception as e:
            _LOGGER.error(f"Unable to get camera session information. {e}")
            return None
            
    def _get_video_session_token(self):
        try:
            payload = {
                CAMERA_SOURCE_ID_KEY : self.source_id,
                CAMERA_SYSTEM_SOURCE_ID_KEY : self.system_source_id,
                CAMERA_TOKEN_KEY : self.camera_token
            }
            
            headers = APPLICATION_JSON_HEADERS.copy()
            headers.update(self.fake_user_data.copy())
            
            response = requests.post(CAMERA_SOURCE_ID_URL, json=payload, headers=headers, verify=False)
            response.raise_for_status()
            
            self.video_session_token = response.json()
            
            _LOGGER.debug(f"Video Session Token: {self.video_session_token}")
            
        except Exception as e:
            _LOGGER.error(f"Unable to get video session token. {e}")
            return None