#!/usr/bin/env bash
set -euo pipefail

cd /home/birdpi/avian-acoustic-monitoring

git fetch origin
# Checkout the deploy branch to avoid breaking changes
git reset --hard origin/deploy

docker compose build recorder
docker image prune -f