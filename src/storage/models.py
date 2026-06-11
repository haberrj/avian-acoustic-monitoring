from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

Base = declarative_base()

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    species = Column(String, nullable=True)
    confidence = Column(Float)

    def __repr__(self):
        return f"<Detection(species={self.species}, confidence={self.confidence})>"
