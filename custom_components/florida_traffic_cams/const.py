from homeassistant.const import Platform

DOMAIN = "florida_traffic_cameras"
PLATFORMS = [Platform.CAMERA]
FLORIDA_TRAFFIC_CAM_QUERY_URL = "https://fl511.com/List/GetData/Cameras?query={'columns':[{'data':null,'name':''},{'name':'sortOrder','s':true},{'name':'region','s':true},{'name':'county','s':true},{'name':'roadway','s':true},{'name':'location'},{'name':'direction','s':true},{'data':7,'name':''}],'order':[{'column':1,'dir':'asc'},{'column':2,'dir':'asc'}],'start':0,'length':10,'search':{'value':{0}}}}&lang=en-US"
VIDEO_URL_KEY = "videoUrl"
IMAGES_DATA_KEY = "images"
IMAGES_ID_INDEX = 0
IMAGES_ID_KEY = "id"
FLORIDA_CAMERA_TOKEN_URL = "https://fl511.com/Camera/GetVideoUrl?imageId={0}&_={1}"
CAMERA_TOKEN_KEY = "token"
CAMERA_SOURCE_ID_KEY = "sourceId"
CAMERA_SYSTEM_SOURCE_ID_KEY = "systemSourceId"
CAMERA_SOURCE_ID_URL = "https://divas.cloud/VDS-API/SecureTokenUri/GetSecureTokenUriBySourceId"
FLORIDA_VIDEO_FEED_URL = "{0}{1}"
APPLICATION_JSON_HEADERS={"Content-Type": "application/json"}
CAMERA_SNAPSHOT_URL = "	https://fl511.com/map/Cctv/{0}?t={1}"