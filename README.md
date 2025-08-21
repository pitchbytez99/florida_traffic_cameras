<div align="center">
  <img src="https://github.com/pitchbytez99/florida_traffic_cameras/blob/main/custom_components/florida_traffic_cams/icons/logo.jpg" alt="Florida Traffic Cameras Icon" width="100"><h1>Florida Traffic Cameras</h1>
</div>

![GitHub release (latest by date)](https://img.shields.io/github/v/release/pitchbytez99/florida_traffic_cameras?style=flat-square)
![HACS Compatible](https://img.shields.io/badge/HACS-Compatible-brightgreen?style=flat-square)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Integration-blue?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/pitchbytez99/florida_traffic_cameras?style=flat-square)
![GitHub stars](https://img.shields.io/github/stars/pitchbytez99/florida_traffic_cameras?style=flat-square)

---

## About
Custom integration to expose any Florida traffic camera as a camera entity in Home Assistant.
Traffic cameras that can be used can be found on **https://fl511.com/map**

### Configuration
1. Open **https://fl511.com/map**
2. Find the traffic camera you would like to stream
3. Copy the exact camera name shown in the window into the interations configuration

![Configuring my integration](docs/ezgif-633592c0e2fb3a.gif)

### Installation (HACS)
1. Open **HACS** in Home Assistant.
2. Search for *"Florida Traffic Cameras"* in the Integrations section (check "Available for download" or "New").
3. Click **Download**.
4. Navigate to **Settings > Devices & Services** in Home Assistant.
5. Click the blue **+ Add Integration** button.
6. Search for "Florida Traffic Cameras" then select **Florida Traffic Cameras**.
7. Type in the traffic camera name

### Reporting Issues
- Please include your Home Assistant logs

### My Other Projects
- [Florida Fire Danger Index](../florida_fire_danger_index)