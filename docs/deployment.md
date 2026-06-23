# Deployment

## Requirements

* Raspberry Pi 4 or newer
* Raspberry Pi OS Lite (64-bit)
* Docker
* Docker Compose
* USB microphone
* Internet connectivity

## Initial Setup

Clone the repository:

```bash
git clone <repository-url>
cd avian-acoustic-monitoring
```

Create the environment file:

```bash
cp .env.example .env
```

Update configuration values as required.

## Start Core Services

Pull the Docker Image from dockerhub:
```bash
docker pull
```

Start long-running services:

```bash
docker compose up -d db dashboard cloudflared
```

Run database migrations:

```bash
docker compose --profile jobs run --rm migrate
```

## Install System Services

```bash
crontab -e
*/3 * * * * cd /home/user/avian-acoustic-monitoring && /usr/bin/docker compose --profile jobs run --rm recorder >> /home/user/avian-acoustic-monitoring/logs/recorder.log 2>&1
0 3 * * * cd /home/user/avian-acoustic-monitoring && git pull && docker compose pull >> /home/user/avian-acoustic-monitoring/logs/update.log 2>&1
```

This installs the systemd services and timers required for scheduled recording and update operations.

## Verify Installation

Check running containers:

```bash
docker ps
```

Check cron jobs:

```bash
crontab -l
systemctl status cron
```
