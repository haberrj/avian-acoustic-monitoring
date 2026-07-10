# Hardware

## Overview

The recording node is designed to use inexpensive, widely available hardware while providing sufficient performance for local BirdNET inference.

The hardware requirements are intentionally modest to make deployments affordable and easy to reproduce.

---

# Hardware Philosophy

The project prioritizes:

- Low cost
- Easy replacement of failed components
- Readily available hardware
- Low power consumption
- Sufficient performance for local inference

Rather than relying on specialized acoustic monitoring equipment, the system is designed to operate using commodity hardware and open-source software.

---

# Recommended Hardware

| Component | Recommendation |
|----------|----------------|
| Single-board computer | Raspberry Pi 4 (4 GB RAM or greater) |
| Storage | 32 GB or larger microSD card |
| Microphone | USB microphone |
| Power supply | Official Raspberry Pi USB-C power supply |
| Network | Wi-Fi or Ethernet |
| Enclosure | Weather-resistant enclosure for outdoor deployments |

---

# Raspberry Pi

The Raspberry Pi performs all local processing, including:

- Audio recording
- BirdNET inference
- Detection filtering
- Detection upload
- Heartbeat monitoring

BirdNET inference is performed entirely on the node.

The server never processes audio.

---

# Microphone

The project currently assumes a USB microphone.

Advantages include:

- Plug-and-play support
- Good Linux compatibility
- No additional hardware required
- Easy replacement

The microphone should be positioned to minimize:

- Wind noise
- Rain exposure
- Mechanical vibration

Outdoor deployments should include appropriate weather protection.

---

# Storage

The recording pipeline stores audio only temporarily.

Normal workflow:

```
Record Audio
      │
      ▼
BirdNET Analysis
      │
      ▼
Upload Detection Metadata
      │
      ▼
Delete Recording
```

Only detection metadata is retained during normal operation.

This greatly reduces storage requirements.

When debug mode is enabled, recordings may be preserved for troubleshooting.

---

# Recording Configuration

The default recording schedule is:

| Setting | Value |
|----------|-------|
| Recording duration | 60 seconds |
| Recording interval | 10 minutes |
| Sample rate | 44.1 kHz |

These values provide a balance between:

- Detection probability
- CPU utilization
- Storage usage
- Network usage

The recording interval can be adjusted using environment variables.

---

# Network Requirements

Recording nodes require network connectivity only when uploading:

- Detection metadata
- Heartbeat information

BirdNET inference does not require an Internet connection.

Temporary network outages do not prevent local detection processing.

---

# Power

Recording nodes are designed for continuous operation.

Recommendations:

- Stable power supply
- Surge protection where appropriate
- UPS for permanent installations (optional)

Outdoor deployments may alternatively use:

- Solar panels
- Battery systems

These deployment scenarios have not yet been extensively tested.

---

# Outdoor Deployment

For permanent outdoor installations, consider:

- Weather-resistant enclosure
- Condensation control
- Wind protection
- Rain protection
- Cable strain relief
- Insect protection
- Secure mounting

Microphone placement has a significant impact on recording quality.

Avoid locations close to:

- Roads
- Air-conditioning units
- Building ventilation
- Moving water (unless intentionally monitoring wetlands)

---

# Performance

Local BirdNET inference allows the system to operate without cloud-based audio processing.

Typical resource usage is low enough for continuous operation on a Raspberry Pi 4.

Heartbeat monitoring reports operational metrics including:

- Available memory
- Available disk space
- System uptime
- Software version

These metrics help identify hardware issues before they affect monitoring.

---

# Scaling

The hardware architecture is designed to support multiple independent recording stations.

Each node operates independently and communicates only with the central server.

Adding additional stations does not require changes to the server architecture.

---

# Future Improvements

Potential future hardware enhancements include:

- Higher-quality microphones
- GPS modules
- Battery-powered deployments
- Solar-powered deployments
- Environmental sensors (temperature, humidity, etc.)
- Improved enclosure designs
- Additional hardware health monitoring

The current architecture has been designed to accommodate these additions without requiring significant software changes.