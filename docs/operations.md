# Operations

## View Recorder Logs

```bash
journalctl -u avian-recorder -f
```

## View Update Logs

```bash
journalctl -u avian-update -f
```

## Check Timer Status

```bash
systemctl status avian-recorder.timer
systemctl status avian-update.timer
```

## Run Recording Manually

```bash
docker compose --profile jobs run --rm recorder
```

## Run Database Migration Manually

```bash
docker compose --profile jobs run --rm migrate
```

## Rebuild Containers

```bash
docker compose build
```

## Restart Dashboard

```bash
docker compose restart dashboard
```

## Verify Database Connectivity

```bash
docker compose exec db psql -U postgres
```

## Update Application

The update service performs the following actions:

1. Fetches the latest repository changes.
2. Updates the local deployment branch.
3. Rebuilds Docker images.
4. Executes database migrations.
5. Removes unused Docker images.
