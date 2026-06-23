# Operations

## View Recorder Logs

```bash
tail -f /home/user/avian-acoustic-monitoring/logs/recorder.log
```

## View Update Logs

```bash
tail -f /home/user/avian-acoustic-monitoring/logs/update.log
```

## Check Cron Status

```bash
crontab -l
systemctl status cron
```

## Run Recording Manually

```bash
docker compose --profile jobs run --rm recorder
```

## Run Database Migration Manually

```bash
docker compose --profile jobs run --rm migrate
```

## Pull Images

```bash
docker compose pull
```

## Restart Dashboard

```bash
docker compose restart dashboard
```

## Verify Database Connectivity

```bash
docker compose exec db psql -U acoustic_user -d acoustic_monitor
```

## Update Application

The update service performs the following actions:

1. Fetches the latest repository changes.
2. Updates the local deployment branch.
3. Rebuilds Docker images.
4. Executes database migrations.
5. Removes unused Docker images.
