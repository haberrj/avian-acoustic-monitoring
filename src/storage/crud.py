import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # NOQA: E402 pylint: disable=[C0413]
from src.storage.database import SessionLocal
from src.storage.models import Detection, Station

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
    station_name = station_payload.get("name", "Default Station")

    station = db.query(Station).filter(Station.name == station_name).first()
    if station is not None:
        return station

    station = Station(
        name=station_name,
        description=station_payload.get("description"),
        country=station_payload.get("country"),
        region=station_payload.get("region"),
        latitude=float(station_payload.get("latitude", 0.0)),
        longitude=float(station_payload.get("longitude", 0.0)),
        is_active=True,
    )

    db.add(station)
    db.commit()
    db.refresh(station)

    return station
