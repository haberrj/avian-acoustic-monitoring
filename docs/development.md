# Development

## Overview

This document describes the development workflow for Avian Acoustic Monitoring.

The project follows a distributed architecture consisting of independent server and recording node components that share a common codebase.

Development should prioritize maintainability, reproducibility, and backwards-compatible database changes whenever practical.

---

# Design Philosophy

When introducing new features, prefer:

- Simplicity over abstraction
- Explicit configuration over implicit behavior
- Composition over inheritance
- Stateless services where practical
- Reproducible Docker deployments
- Backwards-compatible database migrations

---

# Repository Structure

```
.
├── dashboard/              Streamlit dashboard
├── docker/                 Docker Compose files
├── docs/                   Project documentation
├── migrations/             Alembic migrations
├── scripts/                Helper scripts
├── src/
│   ├── node/               Raspberry Pi recording node
│   ├── server/             FastAPI application
│   └── storage/            Database layer
├── tests/                  Unit tests
└── README.md
```

---

# Architecture

The project consists of three logical layers.

```
  Node
    │
    ▼
  Server
    │
    ▼
 Database
```

The dashboard reads from the database and is not involved in ingestion.

Whenever possible:

- Keep node logic independent of server logic.
- Keep API logic independent of dashboard code.
- Keep database access inside the storage layer.

---

# Branch Strategy

Development follows a simple Git workflow.

## main

Production-ready code.

Only stable releases should be merged into `main`.

---

## develop

Primary development branch.

New features should be merged into `develop` before being promoted to `main`.

---

## feature/*

Used for new functionality.

Examples:

```
feature/heartbeat
feature/dashboard
feature/stations
```

---

## hotfix/*

Used for small fixes that do not introduce new functionality.

Examples:

```
hotfix/docker-compose
hotfix/dashboard-filter
```

---

# Coding Guidelines

## General

- Use type hints where practical.
- Prefer explicit code over clever code.
- Keep functions focused on a single responsibility.
- Avoid duplicated logic.
- Document non-obvious design decisions.

---

## Python

Follow PEP 8.

Formatting and linting are performed using Ruff.

Run before opening a pull request.

```bash
ruff check .
ruff format .
```

---

## SQLAlchemy

- Database access belongs in `src/storage`.
- Avoid database logic inside API routes.
- Keep models focused on persistence.
- Use Alembic for schema changes.

---

## FastAPI

Routes should remain lightweight.

Business logic should live outside API endpoints whenever possible.

Prefer:

```
  Route
    ↓
  CRUD
    ↓
 Database
```

rather than placing database logic directly inside routes.

---

## Dashboard

The dashboard should only visualize data.

Avoid placing business logic inside Streamlit pages.

Whenever possible:

```
Database
    ↓
DataFrame
    ↓
Visualization
```

---

# Database Changes

All schema changes must be implemented through Alembic migrations.

Typical workflow:

```
Modify SQLAlchemy model
        │
        ▼
 Generate migration
        │
        ▼
  Review migration
        │
        ▼
  Apply migration
```

Never modify production databases manually.

---

# Testing

Run the test suite before opening a pull request.

```bash
pytest
```

Lint the repository.

```bash
ruff check .
```

---

# Docker

The project uses Docker for both development and deployment.

Server services:

- PostgreSQL
- FastAPI
- Streamlit
- Cloudflare Tunnel

Node services:

- Recorder
- Heartbeat

Docker images should remain platform independent whenever practical.

---

# Pull Requests

Pull requests should include:

- Clear description
- Updated documentation
- Database migration (if required)
- Passing tests
- Passing Ruff checks

---

# Documentation

Documentation is considered part of the project.

New features should include documentation updates when appropriate.

Relevant documents include:

- README
- architecture.md
- deployment.md
- operations.md
- environment_variables.md

---

# Future Development

Current priorities include:

- Per-node authentication
- Additional ecological analytics
- Long-running recording service
- Additional monitoring stations

Development priorities may evolve as real-world monitoring data becomes available.