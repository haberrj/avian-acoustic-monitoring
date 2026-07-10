# Architecture

## Overview

Avian Acoustic Monitoring is designed as a distributed client-server system for passive acoustic bird monitoring.

The system separates **acoustic inference** from **data storage and visualization**. Raspberry Pi recording nodes perform local BirdNET inference and transmit only processed detection metadata to a centralized server.

This architecture minimizes bandwidth usage, simplifies deployment, and allows multiple geographically distributed recording stations to contribute to a single centralized dataset.

---

# High-Level Architecture

```
                            +--------------------------------+
                            |            Server              |
                            |--------------------------------|
                            | FastAPI REST API              |
                            | PostgreSQL                    |
                            | Streamlit Dashboard           |
                            | Alembic Migrations            |
                            | Cloudflare Tunnel             |
                            +---------------+---------------+
                                            ^
                                            |
                                      HTTPS REST API
                                            |
          +---------------------------------+---------------------------------+
          |                                 |                                 |
          |                                 |                                 |
+---------+---------+             +---------+---------+             +---------+---------+
| Raspberry Pi Node |             | Raspberry Pi Node |             | Raspberry Pi Node |
+-------------------+             +-------------------+             +-------------------+
| Audio Recording   |             | Audio Recording   |             | Audio Recording   |
| BirdNET Inference |             | BirdNET Inference |             | BirdNET Inference |
| Detection Upload  |             | Detection Upload  |             | Detection Upload  |
| Heartbeat Upload  |             | Heartbeat Upload  |             | Heartbeat Upload  |
+-------------------+             +-------------------+             +-------------------+
```

The server does **not** perform BirdNET inference or process audio recordings.

Instead, each node performs inference locally and sends only processed metadata to the server.

---

# Design Principles

Several architectural principles guided the design of the system.

## Edge Processing

BirdNET inference is performed entirely on the Raspberry Pi.

Advantages include:

- Reduced network traffic
- Lower server resource requirements
- Offline recording capability
- Improved privacy
- Scalable multi-node deployments

Only detections that pass the configured confidence threshold are transmitted.

---

## Centralized Storage

All detections are stored in a single PostgreSQL database.

Centralized storage provides:

- Unified visualization
- Simplified querying
- Long-term archival
- Support for multiple recording stations
- Consistent data model

The server remains stateless apart from the database.

---

## Privacy by Design

Environmental recordings may unintentionally contain human speech.

To reduce privacy concerns, the normal processing workflow is:

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

Only processed detection metadata is retained.

Raw recordings may optionally be preserved when debug mode is enabled.

---

# Server Responsibilities

The server provides all centralized services required by the monitoring network.

Responsibilities include:

- REST API for ingestion
- Detection validation
- Database persistence
- Database migrations
- Dashboard hosting
- Station management
- Heartbeat monitoring

The server is designed to remain online continuously while recording nodes may be added or removed without affecting overall operation.

---

# Recording Node Responsibilities

Each Raspberry Pi node operates independently.

Responsibilities include:

- Scheduled audio recording
- BirdNET inference
- Detection filtering
- Uploading detections
- Uploading heartbeat information
- Automatic software updates

Nodes require only network connectivity to communicate with the server.

No direct communication occurs between recording nodes.

---

# Processing Flow

Each scheduled recording follows the same processing pipeline.

```
Record Audio
      │
      ▼
BirdNET Analysis
      │
      ▼
Confidence Filtering
      │
      ▼
Extract Detection Metadata
      │
      ▼
Upload Detection
      │
      ▼
Delete Recording
```

Detection metadata includes:

- Species name
- Scientific name
- Confidence score
- Detection timestamp
- Geographic coordinates
- Call duration
- Station identifier

---

# Time Handling

All timestamps are stored internally in **UTC**.

Displaying timestamps in local time is handled by the dashboard using each station's configured timezone.

This approach:

- avoids daylight saving issues
- simplifies querying
- supports globally distributed recording stations
- maintains consistent storage regardless of deployment location

---

# Heartbeat Monitoring

Recording nodes periodically upload heartbeat information to the server.

Heartbeat messages include operational information such as:

- Last heartbeat timestamp
- Available disk space
- Available memory
- System uptime
- Software version

The dashboard uses heartbeat information to determine whether a recording station is online, stale, or offline.

Heartbeat monitoring is independent of bird detections, allowing hardware failures to be identified even when no birds are detected.

---

# Database

The system stores three primary entities.

## Stations

Represents each recording location.

Stores:

- Station identifier
- Geographic location
- Timezone
- Descriptive metadata

---

## Detections

Represents individual BirdNET detections.

Each detection belongs to exactly one station.

---

## Node Heartbeats

Represents the operational status of a recording node.

Heartbeats provide near real-time health information independently of bird detections.

---

# Deployment Model

The architecture supports multiple deployment scenarios.

Single node

```
Pi
 │
 ▼
Server
```

Multiple nodes

```
    Pi Munich
        │
    Pi Canada
        │
  Pi South Africa
        │
        ▼
      Server
```

Adding additional recording stations does not require architectural changes.

Each node simply uploads detections to the same centralized server via the API.

---

# Future Architecture

The current architecture is designed to support future enhancements without significant structural changes.

Planned improvements include:

- Per-node authentication
- Additional recording stations
- Long-running node service
- Enhanced ecological analytics
- Outdoor production deployments