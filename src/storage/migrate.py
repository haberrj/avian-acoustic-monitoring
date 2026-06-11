from src.storage.database import engine
from src.storage.models import Base

Base.metadata.create_all(bind=engine)
