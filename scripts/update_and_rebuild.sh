#!/usr/bin/env bash
set -euo pipefail

cd /home/birdpi/avian-acoustic-monitoring

git fetch origin

LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse origin/main)"

if [ "$LOCAL" != "$REMOTE" ]; then
    git reset --hard origin/main

    docker compose build
    docker compose up -d db dashboard cloudflared
    docker compose --profile jobs run --rm migrate

    docker image prune -f
fi