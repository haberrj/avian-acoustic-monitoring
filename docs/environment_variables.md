# Environment Variables

## Overview

Avian Acoustic Monitoring uses environment variables to configure both the server and recording nodes.

Each deployment target has its own configuration file.

| Component | Example File |
|-----------|--------------|
| Server | `.env.server.example` |
| Recording Node | `.env.node.example` |

The server and recording nodes are configured independently.

---

# Server Configuration

The server requires database, authentication, and deployment configuration.

## PostgreSQL

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_DB` | PostgreSQL database name. | `acoustic_monitor` |
| `POSTGRES_USER` | PostgreSQL username. | `acoustic_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password. | `your_secure_password_here` |
| `POSTGRES_HOST` | Database host. | `localhost` |
| `POSTGRES_PORT` | Database port. | `5432` |

---

## Cloudflare

| Variable | Description |
|----------|-------------|
| `CLOUDFLARE_TUNNEL_TOKEN` | Token used by Cloudflare Tunnel to securely expose the API and dashboard. |

---

## API Authentication

| Variable | Description |
|----------|-------------|
| `INGESTION_API_TOKEN` | Shared bearer token used by recording nodes when uploading detections and heartbeat information. |

> **Note**
>
> Per-node authentication is planned for a future release. The current implementation uses a shared ingestion token.

---

## Environment

| Variable | Description | Example |
|----------|-------------|---------|
| `ENVIRONMENT` | Deployment environment. Primarily used to distinguish development and production deployments. | `development` |

---

# Recording Node Configuration

Recording nodes require configuration for server communication, recording settings, BirdNET inference, and station metadata.

---

## API

| Variable | Description | Example |
|----------|-------------|---------|
| `API_URL` | URL of the server REST API. | `https://api.domain.com` |
| `API_TOKEN` | Bearer token used when uploading detections and heartbeats. | `super-secret-token` |
| `NODE_VERSION` | Software version reported through heartbeat monitoring. | `1.0.0` |

---

## Audio Processing

| Variable | Description | Example |
|----------|-------------|---------|
| `AUDIO_SAMPLE_RATE` | Recording sample rate in Hertz. | `44100` |
| `AUDIO_DEVICE` | Input device index used by the recorder. | `1` |
| `RECORD_DURATION_SECONDS` | Length of each recording. | `60` |
| `RECORD_INTERVAL_SECONDS` | Time between recordings. | `600` |
| `RECORDINGS_DIR` | Temporary recording directory. | `/app/recordings` |
| `DEBUG_RECORDINGS_DIR` | Directory for preserved recordings when debug mode is enabled. | `/app/debug_recordings` |
| `DEBUG` | Preserve recordings instead of deleting them. `0` = disabled, `1` = enabled. | `0` |

---

## BirdNET

| Variable | Description | Example |
|----------|-------------|---------|
| `BIRD_CONFIDENCE_THRESHOLD` | Minimum confidence required before a detection is uploaded. | `0.7` |

---

## Station Metadata

| Variable | Description | Example |
|----------|-------------|---------|
| `STATION_ID` | Unique identifier for the recording station. | `munich-1` |
| `STATION_NAME` | Human-readable station name. | `Munich` |
| `STATION_DESCRIPTION` | Optional description of the deployment site. | `Prototype installation` |
| `STATION_COUNTRY` | Country where the station is located. | `Germany` |
| `STATION_REGION` | Region or state. | `Bavaria` |
| `STATION_LATITUDE` | Latitude in decimal degrees. | `48.137154` |
| `STATION_LONGITUDE` | Longitude in decimal degrees. | `11.576124` |
| `STATION_TIMEZONE` | IANA timezone used for dashboard display. | `Europe/Berlin` |

---

# Timezone Handling

Recording nodes upload timestamps in UTC.

The dashboard converts timestamps into the station's configured timezone using the value provided by `STATION_TIMEZONE`.

Examples include:

- `Europe/Berlin`
- `America/Toronto`
- `Africa/Johannesburg`

Using IANA timezone names ensures daylight saving time is handled automatically.

---

# Typical Configuration

## Server

```text
POSTGRES_DB=acoustic_monitor
POSTGRES_USER=acoustic_user
POSTGRES_PASSWORD=********
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

INGESTION_API_TOKEN=********

ENVIRONMENT=production
```

## Recording Node

```text
API_URL=https://api.example.com
API_TOKEN=********

NODE_VERSION=1.0.0

RECORD_DURATION_SECONDS=60
RECORD_INTERVAL_SECONDS=600

STATION_ID=munich-1
STATION_NAME=Munich
STATION_TIMEZONE=Europe/Berlin
```

---

# Security

Environment files contain sensitive configuration values and should **never** be committed to version control.

Recommendations:

- Keep production credentials outside the repository.
- Rotate API tokens periodically.
- Use unique credentials for each deployment.
- Commit only `.env.example` files.