import os

from fastapi import FastAPI, Header, HTTPException

from src.server.schemas.schemas import DetectionUploadPayload, DetectionUploadResponse
from src.storage.crud import insert_detection_payload

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

    insert_detection_payload(payload.model_dump())

    return DetectionUploadResponse(status="ok", inserted=len(payload.detections))
