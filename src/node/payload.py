import os
from datetime import datetime, timezone
from typing import Any


def _iso(value: Any) -> Any:
    """Convert datetimes to ISO strings; leave other values unchanged."""
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat()
    return value


def build_detection_payload(
    detections: list[dict[str, Any]],
    recording_path: str,
) -> dict[str, Any]:
    """Build the upload payload sent from an RPi node to the server API."""
    return {
        "station": {
            "station_id": os.getenv("STATION_ID", "Default-Station"),
            "name": os.getenv("STATION_NAME", "Default Station"),
            "description": os.getenv("STATION_DESCRIPTION"),
            "country": os.getenv("STATION_COUNTRY"),
            "region": os.getenv("STATION_REGION"),
            "latitude": float(os.getenv("STATION_LATITUDE", "0.0")),
            "longitude": float(os.getenv("STATION_LONGITUDE", "0.0")),
        },
        "recording": {
            "path": recording_path,
            "sample_rate": int(os.getenv("AUDIO_SAMPLE_RATE", "44100")),
            "duration_seconds": int(os.getenv("RECORD_DURATION_SECONDS", "30")),
        },
        "detections": [
            {key: _iso(value) for key, value in detection.items()}
            for detection in detections
        ],
    }