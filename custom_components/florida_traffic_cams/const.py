from homeassistant.const import Platform

DOMAIN = "florida_traffic_cameras"
PLATFORMS = [Platform.CAMERA]
VIDEO_URL_KEY = "videoUrl"
FLORIDA_TRAFFIC_CAM_QUERY_URL = (
    "https://fl511.com/List/GetData/Cameras?query={{\"columns\":[{{\"data\":null,\"name\":\"\"}},"
    "{{\"name\":\"sortOrder\",\"s\":true}},{{\"name\":\"region\",\"s\":true}},{{\"name\":\"county\",\"s\":true}},"
    "{{\"name\":\"roadway\",\"s\":true}},{{\"name\":\"location\"}},{{\"name\":\"direction\",\"s\":true}},"
    "{{\"data\":7,\"name\":\"\"}}],\"order\":[{{\"column\":1,\"dir\":\"asc\"}},{{\"column\":2,\"dir\":\"asc\"}}],"
    "\"start\":0,\"length\":10,\"search\":{{\"value\":\"{0}\"}}}}&lang=en"
)
DATA_KEY = "data"
DATA_INDEX = 0
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
CAMERA_SNAPSHOT_URL = "https://fl511.com/map/Cctv/{0}?t={1}"
HTTP_OK_RANGE = {"MIN": 200, "MAX": 399}
STREAM_URL_HEADERS = {
    "Accept" : "*/*",
    "Accept-Encoding" : "gzip, deflate, br, zstd",
    "Accept-Language" : "en-US,en;q=0.5",
    "Connection" : "keep-alive",
    "DNT" : 1,
    "Host" : "dim-se15.divas.cloud:8200",
    "Origin" : "https://fl511.com",
    "Referer" : "https://fl511.com/",
    "Sec-Fetch-Dest" : "empty",
    "Sec-Fetch-Mode" : "cors",
    "Sec-Fetch-Site" : "cross-site",
    "Sec-GPC" : 1
}