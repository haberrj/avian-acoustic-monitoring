import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # NOQA: E402 pylint: disable=[C0413]
from src.storage.database import SessionLocal
from src.storage.models import Detection


def insert_detections(detections: list[dict]):
    """Insert multiple detections into DB"""

    db = SessionLocal()

    try:
        for d in detections:
            detection_obj = Detection(
                timestamp=d.get("recording_timestamp"),
                event_time=d.get("event_time"),
                latitude=d.get("latitude"),
                longitude=d.get("longitude"),
                species=d.get("scientific_name"),
                common_name=d.get("common_name"),
                confidence=d.get("confidence"),
                call_duration=d.get("call_duration")
            )

            db.add(detection_obj)

        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()
