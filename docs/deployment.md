# Deployment

## Overview

Avian Acoustic Monitoring is deployed as two independent components:

- **Server** – hosts the REST API, PostgreSQL database, Streamlit dashboard, and supporting infrastructure.
- **Recording Node** – Raspberry Pi-based recording station responsible for audio recording, BirdNET inference, and uploading detections.

The server and recording nodes are deployed independently. A single server can support one or many recording nodes.

---

# Server Deployment

## Components

The server deployment consists of the following services:

| Service | Purpose |
|----------|---------|
| PostgreSQL | Stores stations, detections, and heartbeat information |
| FastAPI | REST API for detections and heartbeat uploads |
| Streamlit | Dashboard for visualization and monitoring |
| Cloudflare Tunnel | Secure remote access |
| Alembic | Database schema migrations |

---

## Prerequisites

- Docker
- Docker Compose
- Server with persistent storage
- Cloudflare Tunnel (optional, recommended)

---

## Configuration

Copy the example configuration file.

```bash
cp .env.server.example .env
```

Configure the required environment variables before starting the server.

See `environment_variables.md` for details.

---

## Starting the Server

Start all server services.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    up -d
```

Verify the services are running.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    ps
```

---

# Database Migrations

Database schema changes are managed using Alembic.

Run migrations after deploying a new version.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    --profile jobs \
    run --rm migrate
```

Before applying schema changes to production, creating a PostgreSQL backup is recommended.

---

# Updating the Server

Pull the newest images.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    pull
```

Apply database migrations.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    --profile jobs \
    run --rm migrate
```

Restart the services.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    up -d
```

---

# Recording Node Deployment

## Components

Each recording node runs independently and consists of:

- Scheduled recorder
- BirdNET inference
- Detection uploader
- Heartbeat uploader

No database is required on the node.

---

## Hardware Requirements

Minimum recommended hardware:

- Raspberry Pi 4
- 4 GB RAM
- USB microphone
- Stable network connection
- MicroSD card

Additional hardware recommendations are described in `hardware.md`.

---

## Configuration

Copy the example configuration file.

```bash
cp .env.node.example .env
```

Configure:

- Server URL
- API token
- Station identifier
- Geographic coordinates
- Timezone
- Recording parameters

---

## Pulling the Latest Image

```bash
docker compose \
    -f docker/docker-compose.node.yaml \
    pull
```

Unused images may be removed to conserve disk space.

```bash
docker image prune -f
```

---

## Running the Recorder

Execute the recording pipeline manually.

```bash
docker compose \
    -f docker/docker-compose.node.yaml \
    --profile jobs \
    run --rm recorder
```

---

## Running Heartbeat

Heartbeat uploads can be tested independently.

```bash
docker compose \
    -f docker/docker-compose.node.yaml \
    --profile jobs \
    run --rm heartbeat
```

---

# Updating a Recording Node

Pull the newest Docker image.

```bash
docker compose \
    -f docker/docker-compose.node.yaml \
    pull
```

Remove unused images.

```bash
docker image prune -f
```

The next scheduled execution will automatically use the updated image.

---

# Verifying a Deployment

After deployment, verify that:

- API is reachable
- Dashboard loads successfully
- Database migrations completed
- Recording node uploads detections
- Recording node uploads heartbeats
- Station appears online in the dashboard

---

# Deployment Workflow

Typical deployment workflow:

```
  Developer
      │
      ▼
    GitHub
      │
      ▼
GitHub Actions
      │
      ▼
  Docker Hub
      │
      ├──────────────┐
      ▼              ▼
 Server          Recording Nodes
```

This allows all recording nodes to deploy the same container image while remaining independently configurable through environment variables.

---

# Backup Recommendations

Before applying production updates:

- Backup the PostgreSQL database.
- Verify the backup can be restored.
- Apply database migrations.
- Restart the server.
- Verify heartbeat uploads.
- Verify detection uploads.

Database backups should be performed regularly to prevent data loss.