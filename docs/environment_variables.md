## Environment Variables

The application is configured through a `.env` file.

| Variable | Description | Example |
|-----------|-------------|---------|
| `POSTGRES_DB` | PostgreSQL database name | `acoustic_monitor` |
| `POSTGRES_USER` | PostgreSQL username | `acoustic_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `your_secure_password_here` |
| `POSTGRES_HOST` | PostgreSQL hostname | `db` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `AUDIO_SAMPLE_RATE` | Recording sample rate in Hz | `44100` |
| `AUDIO_DEVICE` | Audio input device index inside the container | `1` |
| `RECORD_DURATION_SECONDS` | Length of each audio recording in seconds | `30` |
| `RECORDINGS_DIR` | Directory used for temporary recordings | `/app/recordings` |
| `DEBUG_RECORDINGS_DIR` | Directory used to store recordings when debug mode is enabled | `/app/debug_recordings` |
| `DEBUG` | Preserve recordings after processing (`0` = disabled, `1` = enabled) | `0` |
| `BIRD_CONFIDENCE_THRESHOLD` | Minimum BirdNET confidence required to retain a detection | `0.7` |
| `CLOUDFLARE_TUNNEL_TOKEN` | Cloudflare Tunnel authentication token | `xyz` |
| `STATION_NAME` | Human-readable station name | `Station Name` |
| `STATION_DESCRIPTION` | Description of the monitoring location | `Prototype deployment` |
| `STATION_COUNTRY` | Country where the station is located | `Some Country` |
| `STATION_REGION` | Region, state, or province | `Some Region` |
| `STATION_LATITUDE` | Station latitude in decimal degrees | `1.12345678` |
| `STATION_LONGITUDE` | Station longitude in decimal degrees | `1.12345678` |

### Example Configuration

```env
POSTGRES_DB=acoustic_monitor
POSTGRES_USER=acoustic_user
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_HOST=db
POSTGRES_PORT=5432

AUDIO_SAMPLE_RATE=44100
AUDIO_DEVICE=1
RECORD_DURATION_SECONDS=30
RECORDINGS_DIR=/app/recordings
DEBUG_RECORDINGS_DIR=/app/debug_recordings
DEBUG=0

BIRD_CONFIDENCE_THRESHOLD=0.7

CLOUDFLARE_TUNNEL_TOKEN=xyz

STATION_NAME=Name of Station
STATION_DESCRIPTION=Description
STATION_COUNTRY=Country Name
STATION_REGION=Region Name
STATION_LATITUDE=1.12345678
STATION_LONGITUDE=1.12345678
```

### Finding the Audio Device

To list available audio devices inside the recorder container:

```bash
docker compose run --rm recorder python -c "import sounddevice as sd; print(sd.query_devices())"
```

Use the device index shown for `AUDIO_DEVICE`.
