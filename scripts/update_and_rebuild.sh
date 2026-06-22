#!/usr/bin/env bash
set -euo pipefail

cd /home/birdpi/avian-acoustic-monitoring

git fetch origin

LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse origin/deploy)"

if [ "$LOCAL" != "$REMOTE" ]; then
    git reset --hard origin/deploy

    docker compose build
    docker compose up -d db dashboard cloudflared
    docker compose --profile jobs run --rm migrate

    docker image prune -f
fi