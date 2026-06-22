from datetime import timezone
from pathlib import Path
from unittest.mock import patch

from src.detection.birdnet import BirdNetAudio


def test_extracts_timestamp_from_filename(tmp_path: Path) -> None:
    audio_file = tmp_path / "recording_20260622_101530.wav"
    audio_file.write_bytes(b"fake wav")

    analyzer = BirdNetAudio({"lat": 0.00000, "lon": 0.00000}, str(audio_file))

    assert analyzer.timestamp.year == 2026
    assert analyzer.timestamp.month == 6
    assert analyzer.timestamp.day == 22
    assert analyzer.timestamp.hour == 10
    assert analyzer.timestamp.minute == 15
    assert analyzer.timestamp.second == 30
    assert analyzer.timestamp.tzinfo == timezone.utc


def test_filter_detections_adds_metadata(tmp_path: Path) -> None:
    audio_file = tmp_path / "recording_20260622_101530.wav"
    audio_file.write_bytes(b"fake wav")

    fake_detections = [
        {
            "common_name": "Great Tit",
            "scientific_name": "Parus major",
            "confidence": 0.9,
            "start_time": 2.0,
            "end_time": 5.0,
        },
        {
            "common_name": "Low Confidence Bird",
            "confidence": 0.1,
            "start_time": 0.0,
            "end_time": 1.0,
        },
    ]

    birdnet = BirdNetAudio({"lat": 0.00000, "lon": 0.00000}, str(audio_file))

    with patch.object(BirdNetAudio, "_analyze_audio", return_value=fake_detections):
        detections = birdnet.filter_detections(threshold=0.2)

    assert len(detections) == 1
    assert detections[0]["common_name"] == "Great Tit"
    assert detections[0]["call_duration"] == 3.0
    assert detections[0]["latitude"] == 0.00000
    assert detections[0]["longitude"] == 0.00000