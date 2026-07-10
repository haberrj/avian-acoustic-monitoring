# Testing

## Overview

This document describes how to verify that an Avian Acoustic Monitoring deployment is functioning correctly.

The procedures are intended to validate the complete system after deployment, updates, or infrastructure changes.

Testing is divided into four areas:

- Server
- Recording Node
- Dashboard
- End-to-End System

---

# Server Verification

## Containers

Verify all required containers are running.

```bash
docker compose \
    -f docker/docker-compose.server.yaml \
    ps
```

Expected services:

- PostgreSQL
- FastAPI
- Streamlit
- Cloudflare Tunnel

---

## API

Verify the API is reachable.

Swagger documentation:

```
http://<server>:8000/docs
```

OpenAPI specification:

```
http://<server>:8000/openapi.json
```

---

## Database

Verify the current Alembic migration.

```sql
SELECT version_num
FROM alembic_version;
```

Verify stations exist.

```sql
SELECT
    station_id,
    name,
    timezone
FROM stations;
```

Verify detections.

```sql
SELECT COUNT(*)
FROM detections;
```

Verify heartbeat table.

```sql
SELECT COUNT(*)
FROM node_heartbeats;
```

---

# Recording Node Verification

## Recorder

Run the recorder manually.

```bash
docker compose \
    -f docker/docker-compose.node.yaml \
    --profile jobs \
    run --rm recorder
```

Expected:

- Recording completes
- BirdNET runs
- Detection upload succeeds

---

## Heartbeat

Run heartbeat manually.

```bash
docker compose \
    -f docker/docker-compose.node.yaml \
    --profile jobs \
    run --rm heartbeat
```

Expected:

- HTTP 200 response
- Heartbeat inserted into database

---

## Docker Image

Verify the latest image is present.

```bash
docker images
```

---

# Dashboard Verification

Open the dashboard.

Verify:

- Dashboard loads successfully
- No Streamlit errors
- Detection map loads
- Species page loads
- Stations page loads
- System page loads

---

# Station Verification

Verify the recording station:

- Appears in the Stations page
- Shows Online status
- Displays recent heartbeat
- Displays correct timezone
- Displays latest detection

---

# Detection Verification

After a successful recorder execution:

Verify:

- Detection count increases
- Dashboard updates
- Species statistics update
- Monthly detections update

---

# Heartbeat Verification

Confirm:

- Heartbeat timestamp updates
- Available memory updates
- Available disk space updates
- Node version displayed
- Station remains Online

---

# Timezone Verification

Confirm:

- Database stores timestamps in UTC.
- Dashboard displays local station time.
- Daylight saving time is handled correctly.

---

# Database Migration Verification

After every migration:

Verify:

- Migration completed successfully.
- Existing detections remain.
- Existing stations remain.
- Heartbeat table accessible.
- Dashboard functions normally.

---

# End-to-End Verification

The following sequence validates the complete system.

```
Recorder
     │
     ▼
BirdNET
     │
     ▼
Detection Upload
     │
     ▼
FastAPI
     │
     ▼
PostgreSQL
     │
     ▼
Dashboard
```

A successful end-to-end test confirms:

- BirdNET inference
- REST API
- Database
- Dashboard

are all functioning correctly.

---

# Release Checklist

Before considering a deployment complete:

- [ ] Server containers running
- [ ] Database migrations applied
- [ ] API reachable
- [ ] Dashboard accessible
- [ ] Heartbeat upload verified
- [ ] Detection upload verified
- [ ] Station shown as Online
- [ ] Local timezone displayed correctly
- [ ] Detection count increasing
- [ ] No container errors
- [ ] Database backup completed (production)

Completing this checklist provides confidence that the deployment is operating as expected.