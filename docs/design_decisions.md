# Engineering Decisions

## Overview

Every software project involves trade-offs.

This document explains the major architectural decisions made during the development of Avian Acoustic Monitoring, why they were made, and the alternatives that were considered.

The goal is to document the reasoning behind the architecture rather than simply describe its implementation.

---

# Why a Distributed Architecture?

The project separates the recording nodes from the server.

```
  Recording Node
        │
        ▼
    REST API
        │
        ▼
     Server
```

This provides several advantages:

- Multiple recording stations can contribute to a single dataset.
- Recording nodes remain lightweight and independent.
- The server can be upgraded without modifying recording nodes.
- Nodes can be deployed in different geographic regions.

Alternative considered:

- Running BirdNET directly on the server.

This would require transferring every audio recording across the network, increasing bandwidth requirements and introducing unnecessary latency.

---

# Why Edge Inference?

BirdNET runs locally on each Raspberry Pi rather than on the server.

Advantages:

- Lower bandwidth usage
- Reduced server load
- Offline recording capability
- Improved privacy
- Better scalability

Only processed detection metadata is uploaded.

---

# Why FastAPI?

The server exposes a REST API used by all recording nodes.

FastAPI was selected because it provides:

- Automatic request validation
- Type hints
- High performance
- Automatic OpenAPI documentation
- Straightforward integration with Pydantic

Alternative considered:

- Flask

FastAPI provides stronger typing and automatic API documentation with minimal additional complexity.

---

# Why PostgreSQL?

Detections are stored in PostgreSQL.

Reasons:

- Mature relational database
- Excellent support for SQLAlchemy
- Reliable transactions
- Easy backups
- Good scalability

Alternative considered:

- SQLite

SQLite would simplify deployment but is less suitable for concurrent access and future multi-node deployments.

---

# Why SQLAlchemy?

The project uses SQLAlchemy as its ORM.

Reasons:

- Clear data model
- Database abstraction
- Good Alembic integration
- Strong Python ecosystem

---

# Why Alembic?

Database schemas evolve over time.

Alembic allows schema changes to be version controlled and applied consistently across deployments.

Using migrations avoids manual changes to production databases.

---

# Why Docker?

Both the server and recording nodes are deployed using Docker.

Benefits include:

- Consistent environments
- Reproducible deployments
- Simple updates
- Platform independence
- Easier dependency management

Using the same Docker images in development and production reduces deployment differences.

---

# Why Delete Audio?

Audio recordings are temporary processing artifacts.

Normal workflow:

```
Record
   │
   ▼
Analyze
   │
   ▼
Extract Metadata
   │
   ▼
Delete Recording
```

Advantages:

- Reduced storage requirements
- Lower privacy concerns
- Reduced backup sizes
- Lower bandwidth usage

Debug mode can optionally preserve recordings.

---

# Why UTC?

All timestamps are stored internally in UTC.

The dashboard converts timestamps to each station's configured timezone.

Advantages:

- Correct daylight saving handling
- Simpler querying
- Multi-region support
- Consistent storage

---

# Why Heartbeats?

Bird detections alone cannot distinguish between:

- No birds present
- Recording node offline

Heartbeat monitoring allows the dashboard to identify hardware failures independently of detection activity.

This makes the operational status of each recording node visible even during periods of low bird activity.

---

# Why Station IDs?

Every recording node has a unique station identifier.

The station ID is independent of:

- Station name
- Geographic location

This allows:

- Station renaming
- Metadata updates
- Multi-node deployments
- Stable foreign key relationships

---

# Why Local Time in the Dashboard?

Detection timestamps are stored in UTC but displayed in the station's local timezone.

This improves usability while maintaining consistent storage.

Users can interpret detections using local sunrise, sunset, and seasonal patterns without sacrificing database consistency.

---

# Why Docker-Based Scheduled Jobs?

Recording and heartbeat uploads are executed as short-lived Docker containers.

Advantages:

- Stateless execution
- Easy updates
- Consistent runtime environment
- Simple recovery from failures

A long-running service may be evaluated in the future, but scheduled jobs currently provide sufficient reliability while keeping operational complexity low.

---

# Lessons Learned

Several practical lessons emerged during development.

- Keeping inference on the node significantly simplifies the server.
- Storing only metadata greatly reduces storage requirements.
- UTC simplifies distributed deployments.
- Heartbeats are essential for distinguishing hardware failures from periods of low bird activity.
- Docker makes both deployment and maintenance substantially easier.
- Separating server and recording node responsibilities improves scalability and maintainability.

These principles continue to guide the project's evolution.