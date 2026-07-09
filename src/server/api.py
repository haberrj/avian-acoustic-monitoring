import os

from fastapi import FastAPI, Header, HTTPException

from src.server.schemas.schemas import (
    DetectionUploadPayload,
    DetectionUploadResponse,
    HeartbeatIn,
    HeartbeatResponse,)
from src.storage.crud import insert_detection_payload, insert_heartbeat

app = FastAPI(title="Avian Acoustic Monitoring API")


@app.post("/detections/", response_model=DetectionUploadResponse)
def create_detection_payload(
    payload: DetectionUploadPayload,
    authorization: str | None = Header(default=None),
) -> DetectionUploadResponse:
    expected_token = os.getenv("INGESTION_API_TOKEN")

    if not expected_token:
        raise HTTPException(status_code=500, detail="INGESTION_API_TOKEN is not configured")

    if authorization != f"Bearer {expected_token}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not payload.detections:
        return DetectionUploadResponse(status="ok", inserted=0)
    print("Received payload")
    print(payload.model_dump())
    print(f"Authorization header present: {authorization is not None}")

    insert_detection_payload(payload.model_dump())

    return DetectionUploadResponse(status="ok", inserted=len(payload.detections))

@app.post("/heartbeat/", response_model=HeartbeatResponse)
def create_heartbeat(
    payload: HeartbeatIn,
    authorization: str | None = Header(default=None),
) -> HeartbeatResponse:
    expected_token = os.getenv("INGESTION_API_TOKEN")

    if not expected_token:
        raise HTTPException(status_code=500, detail="INGESTION_API_TOKEN is not configured")

    if authorization != f"Bearer {expected_token}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    insert_heartbeat(payload.model_dump())

    return HeartbeatResponse(status="ok")
