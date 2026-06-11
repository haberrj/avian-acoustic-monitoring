from datetime import datetime
from src.storage.database import SessionLocal
from src.storage.models import Detection

def create_detection(species, confidence, lat=None, lon=None):
    db = SessionLocal()

    detection = Detection(
        timestamp=datetime.utcnow(),
        species=species,
        confidence=confidence,
        latitude=lat,
        longitude=lon
    )

    db.add(detection)
    db.commit()
    db.close()


def get_all_detections():
    db = SessionLocal()
    results = db.query(Detection).all()
    db.close()
    return results
