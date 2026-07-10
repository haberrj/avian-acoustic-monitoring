from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class StationPayload(BaseModel):
    station_id: str = Field(..., examples=["station-name-1"])
    name: str = Field(..., examples=["Station Name"])
    description: str | None = Field(default=None)
    country: str | None = Field(default=None, examples=["Country"])
    region: str | None = Field(default=None, examples=["Region"])
    latitude: float | None = Field(default=None, examples=[0.000])
    longitude: float | None = Field(default=None, examples=[0.000])
    timezone: str | None = Field(default=None, examples=["Europe/Berlin"])


class RecordingPayload(BaseModel):
    path: str | None = Field(default=None, examples=["recordings/2026-06-24_121212.wav"])
    sample_rate: int | None = Field(default=None, examples=[44100])
    duration_seconds: int | None = Field(default=None, examples=[30])


class DetectionPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    scientific_name: str | None = Field(default=None, examples=["Turdus merula"])
    common_name: str | None = Field(default=None, examples=["Common Blackbird"])
    confidence: float = Field(..., examples=[0.91])
    start_time: float | None = Field(default=None, examples=[3.0])
    end_time: float | None = Field(default=None, examples=[6.0])


class DetectionUploadPayload(BaseModel):
    station: StationPayload
    recording: RecordingPayload
    detections: list[DetectionPayload]


class DetectionUploadResponse(BaseModel):
    status: str
    inserted: int

class HeartbeatIn(BaseModel):
    station_id: str
    timestamp_utc: datetime
    uptime_seconds: float | None = None
    cpu_temp_c: float | None = None
    memory_available_mb: float | None = None
    disk_free_gb: float | None = None
    wifi_signal_dbm: float | None = None
    node_version: str | None = None


class HeartbeatResponse(BaseModel):
    status: str
