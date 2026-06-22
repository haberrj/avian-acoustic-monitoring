from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    country = Column(String, nullable=True)
    region = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    detections = relationship("Detection", back_populates="station")


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

    station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    station = relationship("Station", back_populates="detections")

    def __repr__(self):
        return f"<Detection(species={self.species}, confidence={self.confidence})>"
