import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # NOQA: E402 pylint: disable=[C0413]
from src.storage.database import SessionLocal
from src.storage.models import Detection, Station


def insert_detections(detections: list[dict]):
    """Insert multiple detections into DB"""

    db = SessionLocal()

    try:
        station = get_or_create_station(db)

        for d in detections:
            detection_obj = Detection(
                timestamp=d.get("recording_timestamp"),
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

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


def get_or_create_station(db) -> Station:
    station_name = os.getenv("STATION_NAME", "Default Station")

    station = db.query(Station).filter(Station.name == station_name).first()
    if station is not None:
        return station

    station = Station(
        name=station_name,
        description=os.getenv("STATION_DESCRIPTION"),
        country=os.getenv("STATION_COUNTRY"),
        region=os.getenv("STATION_REGION"),
        latitude=float(os.getenv("STATION_LATITUDE", "0.0")),
        longitude=float(os.getenv("STATION_LONGITUDE", "0.0")),
        is_active=True,
    )

    db.add(station)
    db.commit()
    db.refresh(station)

    return station
