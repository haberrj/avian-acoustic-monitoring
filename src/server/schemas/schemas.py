from pydantic import BaseModel, Field, ConfigDict


class StationPayload(BaseModel):
    station_id: str = Field(..., examples=["munich-garden-01"])
    name: str = Field(..., examples=["Munich Garden"])
    description: str | None = Field(default=None)
    country: str | None = Field(default=None, examples=["Germany"])
    region: str | None = Field(default=None, examples=["Bavaria"])
    latitude: float | None = Field(default=None, examples=[48.1351])
    longitude: float | None = Field(default=None, examples=[11.5820])


class RecordingPayload(BaseModel):
    path: str | None = Field(default=None, examples=["recordings/2026-06-24.wav"])
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