import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # NOQA: E402 pylint: disable=[C0413]
from src.storage.database import SessionLocal
from src.storage.models import Detection, Station, NodeHeartbeat

def insert_detection_payload(payload: dict) -> None:
    """Insert uploaded node detection payload into Postgres."""
    db = SessionLocal()

    try:
        station_payload = payload.get("station", {})
        detections = payload.get("detections", [])

        station = get_or_create_station_from_payload(db, station_payload)

        for d in detections:
            detection_obj = Detection(
                timestamp=d.get("timestamp"),
                event_time=d.get("event_time"),
                latitude=d.get("latitude"),
                longitude=d.get("longitude"),
                species=d.get("scientific_name"),
                common_name=d.get("common_name"),
                confidence=d.get("confidence"),
                call_duration=d.get("call_duration"),
                station_id=station.id,
            )
            db.add(detection_obj)

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_or_create_station_from_payload(db, station_payload: dict) -> Station:
    external_station_id = station_payload.get("station_id", "default-station")

    station = db.query(Station).filter(Station.station_id == external_station_id).first()
    if station is not None:
        return station

    station = Station(
        station_id=external_station_id,
        name=station_payload.get("name", "Default Station"),
        description=station_payload.get("description"),
        country=station_payload.get("country"),
        region=station_payload.get("region"),
        latitude=float(station_payload.get("latitude", 0.0)),
        longitude=float(station_payload.get("longitude", 0.0)),
        timezone=station_payload.get("timezone"),
        is_active=True,
    )

    db.add(station)
    db.commit()
    db.refresh(station)

    return station

def get_station_by_identifier(db, station_identifier: str) -> Station | None:
    return db.query(Station).filter(Station.station_id == station_identifier).first()


def insert_heartbeat(payload: dict) -> None:
    """Insert node heartbeat into Postgres."""
    db = SessionLocal()

    try:
        station = get_station_by_identifier(db, payload["station_id"])

        if station is None:
            raise ValueError(f"Unknown station_id/name for heartbeat: {payload['station_id']}")

        heartbeat = NodeHeartbeat(
            station_id=station.id,
            timestamp=payload["timestamp_utc"],
            uptime_seconds=payload.get("uptime_seconds"),
            cpu_temp_c=payload.get("cpu_temp_c"),
            memory_available_mb=payload.get("memory_available_mb"),
            disk_free_gb=payload.get("disk_free_gb"),
            wifi_signal_dbm=payload.get("wifi_signal_dbm"),
            node_version=payload.get("node_version"),
        )

        db.add(heartbeat)
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
