from pathlib import Path
from unittest.mock import patch

from src.pipeline import run_pipeline


def test_pipeline_deletes_recording_after_processing(tmp_path: Path) -> None:
    audio_file = tmp_path / "recording_20260622_101530.wav"
    audio_file.write_bytes(b"fake wav")

    with patch("src.pipeline.AudioRecorder") as recorder_cls, \
         patch("src.pipeline.BirdNetAudio") as birdnet_cls, \
         patch("src.pipeline.insert_detections") as insert_detections:

        recorder_cls.return_value.record_audio.return_value = str(audio_file)
        birdnet_cls.return_value.filter_detections.return_value = [
            {"common_name": "Great Tit", "confidence": 0.9}
        ]

        run_pipeline()

    assert not audio_file.exists()
    insert_detections.assert_called_once()