#!/usr/bin/env bash
set -euo pipefail

cd /home/birdpi/avian-acoustic-monitoring

docker compose --profile jobs run --rm recorder