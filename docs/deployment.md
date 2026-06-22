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

Build and start long-running services:

```bash
docker compose up -d --build db dashboard cloudflared
```

Run database migrations:

```bash
docker compose --profile jobs run --rm migrate
```

## Install System Services

```bash
chmod +x scripts/*.sh
./scripts/setup_system.sh
```

This installs the systemd services and timers required for scheduled recording and update operations.

## Verify Installation

Check running containers:

```bash
docker ps
```

Check timers:

```bash
systemctl list-timers
```

Check recorder logs:

```bash
journalctl -u avian-recorder
```
