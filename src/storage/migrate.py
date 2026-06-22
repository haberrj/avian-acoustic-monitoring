import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # NOQA: E402 pylint: disable=[C0413]
from src.storage.database import engine
from src.storage.models import Base

Base.metadata.create_all(bind=engine)
