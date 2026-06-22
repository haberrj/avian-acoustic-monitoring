# Avian Acoustic Monitoring

Avian Acoustic Monitoring is a Raspberry Pi-based passive acoustic monitoring system designed to identify bird species using BirdNET and store detections for visualization and analysis.

The project was developed as an exploration of low-cost wildlife monitoring using open-source software and commodity hardware.

## Features

* Automated audio recording
* BirdNET-based species identification
* PostgreSQL-backed detection storage
* Streamlit dashboard
* Docker-based deployment
* Automated scheduling via systemd timers
* Cloudflare Tunnel support for remote dashboard access

## Architecture

```text
Recorder
    ↓
BirdNET
    ↓
Detection Filtering
    ↓
PostgreSQL
    ↓
Dashboard
```

Audio recordings are analyzed locally on a Raspberry Pi. Detection metadata is stored in PostgreSQL and exposed through a Streamlit dashboard.

By default, raw audio recordings are deleted after processing.

## Quick Start

Clone the repository:

```bash
git clone https://github.com/haberrj/avian-acoustic-monitoring.git
cd avian-acoustic-monitoring
```

Create the environment file:

```bash
cp .env.example .env
```

Start services:

```bash
docker compose up -d --build db dashboard cloudflared
docker compose --profile jobs run --rm migrate
```

Install system services:

```bash
chmod +x scripts/*.sh
./scripts/setup_system.sh
```

## Documentation

Additional documentation is available in the `docs` directory:

* architecture.md
* deployment.md
* development.md
* operations.md
* privacy.md
* challenges.md
* hardware.md

## Project Status

This project is under active development and should currently be considered experimental.

## License

MIT License
