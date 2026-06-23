#!/usr/bin/env bash
set -euo pipefail

SERVICE_DIR="/etc/systemd/system"
REPO_DIR="/home/birdpi/avian-acoustic-monitoring"

cd "$REPO_DIR"

chmod +x scripts/record.sh
chmod +x scripts/update_and_rebuild.sh

sudo install -m 644 scripts/avian-recorder.service "$SERVICE_DIR/avian-recorder.service"
sudo install -m 644 scripts/avian-recorder.timer "$SERVICE_DIR/avian-recorder.timer"
sudo install -m 644 scripts/avian-update.service "$SERVICE_DIR/avian-update.service"
sudo install -m 644 scripts/avian-update.timer "$SERVICE_DIR/avian-update.timer"

sudo systemctl daemon-reload

sudo systemctl enable avian-recorder.timer
sudo systemctl start avian-recorder.timer

sudo systemctl enable avian-update.timer
sudo systemctl start avian-update.timer

systemctl list-timers --all | grep avian || true

echo "Avian systemd timers installed and started."