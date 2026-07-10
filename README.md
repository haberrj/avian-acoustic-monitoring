# Avian Acoustic Monitoring

Avian Acoustic Monitoring is a distributed passive acoustic monitoring platform designed to identify bird vocalizations using BirdNET while requiring only low-cost hardware at the recording location.

The project consists of two independent deployable components:

- **Server** – receives detections from recording nodes, stores them in PostgreSQL, and provides a web dashboard and REST API.
- **Node** – a Raspberry Pi-based recording station that performs local BirdNET inference and uploads only detection metadata to the server.

Separating inference from storage allows multiple recording nodes to contribute to a single centralized dataset while keeping bandwidth requirements low and avoiding the transfer of raw audio.

---

# Why?

Passive acoustic monitoring is becoming an increasingly important tool for understanding biodiversity and long-term changes in bird populations. While many existing monitoring systems rely on expensive commercial hardware or cloud-based processing, this project explores whether similar capabilities can be achieved using inexpensive commodity hardware and open-source software.

The project was designed to answer several practical engineering questions:

- Can BirdNET perform reliable on-device inference on low-cost Raspberry Pi hardware?
- Can a distributed network of autonomous recording stations be managed through a centralized server?
- Can environmental monitoring be performed while minimizing storage, bandwidth, and privacy concerns?
- Can the entire system be deployed and maintained using reproducible Docker-based infrastructure?

Rather than treating each recording station as an isolated device, the system is designed as a distributed platform where multiple nodes contribute detections to a single centralized database. This architecture simplifies deployment, enables long-term monitoring across multiple geographic locations, and provides a single interface for visualization and analysis.

The long-term goal is to build a scalable, privacy-conscious, and reproducible platform for passive acoustic biodiversity monitoring that can be deployed by researchers, conservation organizations, or hobbyists using affordable hardware.

---

# System Architecture

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

The server has no dependency on BirdNET and performs no audio processing. This separation keeps the server lightweight, allows recording nodes to operate independently, and significantly reduces network bandwidth by transmitting only detection metadata rather than raw audio.

All inference occurs on the recording nodes.

---

# Design Goals

The project was designed around several principles.

- Perform inference at the edge.
- Centralize storage and visualization.
- Minimize bandwidth usage.
- Avoid long-term storage of environmental audio.
- Support multiple recording stations.
- Keep deployments reproducible using Docker.

---

# Components

## Server

The server provides the central services required by all recording nodes.

Responsibilities include:

- FastAPI REST API
- PostgreSQL database
- Streamlit dashboard
- Database migrations
- Alembic database migrations
- Station management
- Heartbeat monitoring
- Detection storage

The server is intended to remain online continuously.

---

## Recording Node

Each recording node is designed to operate independently.

Responsibilities include:

- Scheduled audio recording
- BirdNET inference
- Detection filtering
- Uploading detections
- Uploading heartbeat information

Nodes require only network connectivity to communicate with the server.

Additional recording stations can be deployed without modifying the server architecture.

---

# Processing Pipeline

For every scheduled recording, the following pipeline is executed.

```
Record Audio
      │
      ▼
BirdNET Analysis
      │
      ▼
Filter by Confidence Threshold
      │
      ▼
Extract Detection Metadata
      │
      ▼
Upload to Server
      │
      ▼
Delete Recording
```

Only detection metadata is uploaded during normal operation.
The system stores timestamps internally in UTC while presenting data in each station's local timezone.

---

# Dashboard

The Streamlit dashboard provides access to the centralized dataset.

Current functionality includes:

- Detection overview
- Detection map
- Species summaries
- Monthly detection statistics
- Station health monitoring
- Node heartbeat monitoring
- Confidence filtering
- Station filtering
- Species filtering
- Station filtering
- Local timezone display

---

# Technology Stack

| Component | Technology |
|------------|------------|
| Programming Language | Python |
| Acoustic Classification | BirdNET |
| API | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Dashboard | Streamlit |
| Containers | Docker |
| Reverse Proxy | Cloudflare Tunnel |
| CI | GitHub Actions |
| Linting | Ruff |
| Testing | Pytest |

---

# Repository Structure

```
src/
├── node/
│   ├── recorder
│   ├── heartbeat
│   └── upload
│
├── server/
│   ├── api
│   ├── schemas
│   └── authentication
│
├── storage/
│   ├── models
│   ├── crud
│   └── database
│
dashboard/
│
docker/
│
migrations/
│
docs/
```

---

# Data Model

The server stores three primary entities:

- Stations
- Detections
- Node Heartbeats

Detections are linked to the recording station that produced them, allowing observations from multiple geographic locations to be analyzed through a single centralized database.

---

# Deployment

The repository contains Docker Compose configurations for both deployment targets.

## Server

The server deployment includes:

- FastAPI
- PostgreSQL
- Streamlit
- Cloudflare Tunnel

Database schema changes are managed using Alembic migrations.

## Node

Each recording node runs independently and periodically executes:

- Audio recording
- BirdNET inference
- Detection upload
- Heartbeat upload

The same Docker image can be deployed to any number of recording stations.

---

# Documentation

Additional documentation is available in the `docs` directory.

| Document | Description |
|----------|-------------|
| architecture.md | Overall system architecture |
| deployment.md | Server and node deployment |
| development.md | Development workflow |
| environment_variables.md | Configuration reference |
| hardware.md | Hardware recommendations |
| operations.md | Operational procedures |
| privacy.md | Privacy considerations |
| challenges.md | Design decisions |

---

# Current Status

Implemented

- Distributed client-server architecture
- Docker-based deployment
- FastAPI ingestion API
- PostgreSQL backend
- Streamlit dashboard
- Heartbeat monitoring
- Station management
- Local timezone support
- Monthly detection summaries
- Automatic database migrations

Planned

- Per-node authentication
- Additional ecological analytics
- Multi-region deployments
- Long-term seasonal analysis

---

# License

Licensed under the MIT License.