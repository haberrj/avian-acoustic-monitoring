from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    event_time = Column(DateTime, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    species = Column(String, nullable=True)
    common_name = Column(String, nullable=True)
    call_duration = Column(Float, nullable=True)
    confidence = Column(Float)

    def __repr__(self):
        return f"<Detection(species={self.species}, confidence={self.confidence})>"
