import os
from typing import Any

from fastapi import FastAPI, Header, HTTPException

from src.storage.crud import insert_detection_payload

app = FastAPI()


@app.post("/detections/")
def create_detection_payload(
    payload: dict[str, Any],
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    expected_token = os.getenv("INGESTION_API_TOKEN")

    if not expected_token:
        raise HTTPException(status_code=500, detail="INGESTION_API_TOKEN is not configured")

    if authorization != f"Bearer {expected_token}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    detections = payload.get("detections", [])

    if not detections:
        return {"status": "ok", "inserted": 0}

    insert_detection_payload(payload)

    return {"status": "ok", "inserted": len(detections)}
