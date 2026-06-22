docker compose up -d --build db dashboard cloudflared
docker compose --profile jobs run --rm migrate
./scripts/setup_system.sh