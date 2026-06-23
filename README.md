# Avian Acoustic Monitoring

Avian Acoustic Monitoring is a Raspberry Pi-based passive acoustic monitoring system designed to identify bird species using BirdNET and store detections for visualization and analysis.

The project was developed as an exploration of low-cost wildlife monitoring using open-source software and commodity hardware.

## Features

* Automated audio recording
* BirdNET-based species identification
* PostgreSQL-backed detection storage
* Streamlit dashboard
* Docker-based deployment
* Automated scheduling via cron
* Cloudflare Tunnel support for remote dashboard access
* Multi-station architecture support

## Architecture

```text
Audio Recorder
      ↓
   BirdNET
      ↓
Detection Filtering
      ↓
 PostgreSQL
      ↓
 Streamlit Dashboard
```

Audio recordings are analyzed locally on a Raspberry Pi. Detection metadata is stored in PostgreSQL and exposed through a Streamlit dashboard.

By default, raw audio recordings are deleted after processing. Debug mode can optionally preserve recordings for troubleshooting and validation.

## Hardware

The prototype hardware currently consists of:

* Raspberry Pi 4 (4 GB)
* USB microphone
* MicroSD card
* Network connection (Wi-Fi or Ethernet)

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

Review and update the station configuration:

```env
STATION_NAME=Name of Station
STATION_DESCRIPTION=Description
STATION_COUNTRY=Country Name
STATION_REGION=Region Name
STATION_LATITUDE=1.12345678
STATION_LONGITUDE=1.12345678
```

Start the database:

```bash
docker compose up -d db
```

Run database migrations:

```bash
docker compose --profile jobs run --rm migrate
```

Start the dashboard and Cloudflare tunnel:

```bash
docker compose up -d dashboard cloudflared
```

## Scheduling

The recorder is designed to run periodically using cron.

Example:

```bash
*/3 * * * * cd /home/user/avian-acoustic-monitoring && /usr/bin/docker compose --profile jobs run --rm recorder >> /home/user/avian-acoustic-monitoring/logs/recorder.log 2>&1
0 3 * * * cd /home/user/avian-acoustic-monitoring && git pull && docker compose pull >> /home/user/avian-acoustic-monitoring/logs/update.log 2>&1
```

Verify cron jobs:

```bash
crontab -l
```

Verify cron service:

```bash
systemctl status cron
```

If the service is not able to run properly, please ensure the user has write access to the repo directory.

```bash
sudo chown -R user:hostname /path/to/repo 
```

## Database Migrations

Schema changes are managed with Alembic.

Generate a migration:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
docker compose --profile jobs run --rm migrate
```

## Cloudflare Access

The dashboard can be exposed securely through Cloudflare Tunnel and protected using Cloudflare Access authentication.

Typical deployment:

```text
Internet
    ↓
Cloudflare Access
    ↓
Cloudflare Tunnel
    ↓
Streamlit Dashboard
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

Current capabilities:

* Automated recording
* BirdNET inference
* PostgreSQL storage
* Dashboard visualization
* Remote access through Cloudflare

Planned improvements:

* Additional station deployments
* Centralized multi-node collection
* Health monitoring and station heartbeats
* Solar-powered field deployment

## License

MIT License
