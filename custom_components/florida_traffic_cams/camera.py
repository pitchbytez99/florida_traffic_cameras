from homeassistant.components.camera import Camera
from .coordinator import FloridaTrafficCameraCoordinator

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Florida Fire Traffic Camera from config flow."""
    camera_name = config_entry.data["camera_name"]
    
    coordinator = FloridaTrafficCameraCoordinator(hass, camera_name)
    
    async_add_entities([FloridaTrafficCamera(coordinator)])

class FloridaTrafficCamera(Camera):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = coordinator._attr_name

    async def stream_source(self):
        return await self.coordinator.async_request_refresh()
