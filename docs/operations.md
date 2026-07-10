# Operations

## Overview

This document describes the operational procedures required to maintain an Avian Acoustic Monitoring deployment.

The procedures assume the server and recording nodes have already been deployed.

---

# Server Operations

## Check Running Services

View the status of all server containers.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    ps
```

---

## View Logs

View logs for the FastAPI service.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    logs api
```

Follow the logs continuously.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    logs -f api
```

Dashboard logs.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    logs dashboard
```

Database logs.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    logs db
```

---

## Restart Services

Restart all server services.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    restart
```

Restart only the API.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    restart api
```

---

# Updating the Server

Pull the newest container images.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    pull
```

Run database migrations.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    --profile jobs \
    run --rm migrate
```

Restart services.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    up -d
```

Verify:

- API responds
- Dashboard loads
- Stations appear online
- Detections continue arriving

---

# Database

## Create Backup

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    exec -T db \
    pg_dump \
    -U acoustic_user \
    acoustic_monitor \
    > backup.sql
```

---

## Access PostgreSQL

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    exec db \
    psql \
    -U acoustic_user \
    -d acoustic_monitor
```

---

## Check Alembic Version

```sql
SELECT version_num
FROM alembic_version;
```

---

## Verify Station Configuration

```sql
SELECT
    id,
    station_id,
    name,
    timezone
FROM stations;
```

---

## View Recent Heartbeats

```sql
SELECT *
FROM node_heartbeats
ORDER BY timestamp DESC
LIMIT 10;
```

---

## Count Detections

```sql
SELECT COUNT(*)
FROM detections;
```

---

# Recording Node Operations

## Run Recorder Manually

```bash
docker compose \
    -f docker/docker-compose.node.yaml \
    --profile jobs \
    run --rm recorder
```

---

## Run Heartbeat Manually

```bash
docker compose \
    -f docker/docker-compose.node.yaml \
    --profile jobs \
    run --rm heartbeat
```

---

## Pull Latest Image

```bash
docker compose \
    -f docker/docker-compose.node.yaml \
    pull
```

Remove unused images.

```bash
docker image prune -f
```

---

## View Recorder Logs

```bash
docker compose \
    -f docker/docker-compose.node.yaml \
    logs
```

---

# Health Checks

A healthy deployment should satisfy the following conditions.

## Server

- API container running
- Dashboard container running
- PostgreSQL container running
- Cloudflare Tunnel connected

---

## Recording Node

- Heartbeats arriving regularly
- Detections uploaded successfully
- Sufficient disk space
- Sufficient available memory

---

# Verifying Heartbeats

The dashboard should show:

- Online indicator
- Last heartbeat
- Available disk space
- Available memory
- Node version

Heartbeat uploads can also be verified directly in PostgreSQL.

---

# Verifying Detection Uploads

A successful recorder execution should produce:

- Detection payload uploaded
- HTTP 200 response
- Detection count increases in PostgreSQL
- Dashboard updates automatically

---

# Common Maintenance Tasks

## Update Server

1. Pull latest images.
2. Run migrations.
3. Restart services.
4. Verify dashboard.
5. Verify heartbeat uploads.

---

## Update Recording Node

1. Pull latest image.
2. Remove unused images.
3. Wait for next scheduled execution.
4. Verify heartbeat.
5. Verify detections.

---

## Add a New Recording Station

1. Deploy Raspberry Pi.
2. Configure environment variables.
3. Set station metadata.
4. Start heartbeat.
5. Verify station appears in dashboard.
6. Verify first detection upload.

---

# Monitoring

Recommended metrics to monitor include:

- Heartbeat frequency
- Detection frequency
- Database size
- Disk utilization
- Memory utilization
- API availability

Monitoring these metrics helps identify hardware failures and deployment issues before they result in data loss.