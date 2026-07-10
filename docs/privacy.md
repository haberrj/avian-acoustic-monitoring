# Privacy

## Overview

Avian Acoustic Monitoring is designed with privacy as a core architectural consideration.

The system performs BirdNET inference locally on each recording node and uploads only detection metadata to the server during normal operation.

Environmental audio recordings are treated as temporary processing artifacts rather than long-term data.

---

# Local Processing

All BirdNET inference is performed on the recording node.

The server never receives or processes raw audio.

Normal processing workflow:

```
Record Audio
      │
      ▼
BirdNET Analysis
      │
      ▼
Extract Detection Metadata
      │
      ▼
Upload Metadata
      │
      ▼
Delete Recording
```

Only the extracted detection metadata is transmitted to the server.

---

# Metadata Collected

The server stores information required for visualization and analysis.

Typical detection metadata includes:

- Common species name
- Scientific species name
- Detection confidence
- Detection timestamp (UTC)
- Station identifier
- Geographic coordinates
- Call duration

Heartbeat messages additionally contain operational information such as:

- Available memory
- Available disk space
- System uptime
- Software version

No personal information is intentionally collected.

---

# Audio Retention

Audio recordings are deleted immediately after BirdNET inference under normal operation.

This approach:

- Reduces storage requirements
- Minimizes bandwidth usage
- Reduces privacy concerns
- Simplifies long-term deployments

When debug mode is enabled, recordings may be retained temporarily for troubleshooting or development purposes.

---

# Time Handling

All timestamps are stored internally in Coordinated Universal Time (UTC).

The dashboard converts timestamps to each station's configured local timezone for display.

Using UTC internally provides:

- Consistent storage
- Correct daylight saving time handling
- Support for globally distributed recording stations

---

# Station Information

Each recording node is associated with a station.

Station metadata includes:

- Station identifier
- Station name
- Geographic location
- Timezone

This information is required to organize detections and support multi-station deployments.

---

# Network Communication

Recording nodes communicate with the server using HTTPS.

Detection metadata and heartbeat information are transmitted over encrypted connections.

The server is designed to authenticate recording nodes before accepting uploaded data.

---

# Limitations

Although the system minimizes the collection of unnecessary information, environmental recordings may still contain:

- Human speech
- Domestic animals
- Vehicle noise
- Other environmental sounds

Users deploying recording nodes should ensure that deployments comply with applicable local privacy and data protection regulations.

---

# Design Philosophy

The project follows the principle of collecting only the information required for biodiversity monitoring.

Where practical, processing occurs locally on the recording node and only derived detection metadata is retained.

This approach reduces storage requirements, minimizes network traffic, and helps protect privacy while maintaining the functionality required for long-term ecological monitoring.

## Public Access

The public dashboard only exposes processed detection data.

Audio recordings are not published through the dashboard.

Database access is restricted to authorized system components.

## Disclaimer

Users are responsible for ensuring compliance with local laws, regulations, and privacy requirements applicable to their deployment location.

This document describes technical design considerations and should not be interpreted as legal advice.
