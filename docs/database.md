# Database

## Overview

The server uses PostgreSQL as its primary data store.

The database is designed to support multiple recording stations contributing detections to a single centralized dataset while maintaining a simple relational schema.

Database schema changes are managed using Alembic migrations.

---

# Design Philosophy

The database intentionally separates relatively static station information from rapidly growing detection and heartbeat records.

This normalization reduces duplicated data, simplifies updates to station metadata, and supports efficient querying as the dataset grows.

The schema favors clarity and maintainability over excessive normalization, while remaining flexible enough to support future monitoring stations and additional operational metrics.

---

# Entity Relationship Diagram

```
                 Stations
                     │
          1          │         N
     ┌───────────────┼────────────────┐
     │               │                │
     ▼               ▼                ▼
Detections                     Node Heartbeats
```

Each recording station can produce many detections and many heartbeat records.

---

# Stations

The `stations` table represents individual recording locations.

Each station stores relatively static information describing a deployment.

Typical information includes:

- Station identifier
- Display name
- Description
- Geographic location
- Country
- Region
- Timezone

The station identifier is used by recording nodes when uploading detections and heartbeat information.

The identifier is intended to remain stable even if descriptive information changes.

---

# Detections

The `detections` table stores BirdNET detections produced by recording nodes.

Each detection belongs to exactly one recording station.

Typical information includes:

- Species name
- Scientific name
- Confidence
- Detection timestamp
- Geographic coordinates
- Call duration

Detection timestamps are stored internally in UTC.

The dashboard converts timestamps to the station's configured local timezone for display.

---

# Node Heartbeats

The `node_heartbeats` table stores operational information reported by recording nodes.

Heartbeat information is independent of BirdNET detections.

This separation allows hardware failures to be distinguished from periods of low bird activity.

Typical heartbeat information includes:

- Timestamp
- System uptime
- Available memory
- Available disk space
- CPU temperature (when available)
- Wi-Fi signal strength (when available)
- Node software version

The dashboard uses recent heartbeat information to determine whether a station is online.

---

# Relationships

The database uses a simple one-to-many relationship model.

```
Station
   │
   ├──────────────► Detections
   │
   └──────────────► Node Heartbeats
```

Each detection and heartbeat record references its originating station.

This design supports:

- Multiple recording stations
- Independent station metadata
- Efficient filtering
- Simple aggregation

---

# Time Handling

All timestamps are stored internally in UTC.

Displaying local time is the responsibility of the dashboard.

Advantages include:

- Correct daylight saving time handling
- Consistent storage
- Simplified querying
- Support for globally distributed deployments

Each station stores its IANA timezone, allowing timestamps to be converted correctly for presentation.

---

# Station Metadata

Station information is intentionally separated from detections.

This avoids duplication and allows station metadata to evolve without modifying historical detections.

Examples include:

- Renaming a station
- Updating coordinates
- Changing descriptions
- Updating timezone information

Historical detections remain unchanged.

---

# Migrations

Database schema changes are managed using Alembic.

Typical workflow:

```
Modify SQLAlchemy Models
          │
          ▼
Generate Alembic Migration
          │
          ▼
Review Migration
          │
          ▼
Apply Migration
```

Migrations provide:

- Version-controlled schema changes
- Repeatable deployments
- Safe production upgrades

Production databases should never be modified manually.

---

# Scaling

The schema is designed to support additional recording stations without structural changes.

Adding a new station requires:

1. Creating a station entry.
2. Configuring the recording node.
3. Uploading detections.

No schema changes are required.

---

# Future Schema Evolution

The schema has been designed to evolve through Alembic migrations.

Potential future additions include:

- Per-node authentication
- Detection verification workflow
- Environmental sensor data
- Recorder configuration history
- Additional operational metrics

Schema changes should remain backwards compatible whenever practical.