import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # NOQA: E402 pylint: disable=[C0413]
from src.capture.recorder import AudioRecorder
from src.detection.birdnet import BirdNetAudio
from src.storage.crud import insert_detections


def run_pipeline():
    print("Starting pipeline...")

    # Record audio
    audio_recorder = AudioRecorder('temp', 44100)  # Will change this eventually to 32 kHz for energy saving
    file_path= audio_recorder.record_audio(30)

    gps_coords = {
        "lat": 48.746,
        "lon": 11.463
    }

    try:
        # Run BirdNET
        analyzer = BirdNetAudio(gps_coords, file_path)

        # Filter detections
        detections = analyzer.filter_detections(threshold=0.7)

        if not detections:
            print("No valid detections. Deleting recording.")
            return

        # Write to database
        insert_detections(detections)

        print(f"Inserted {len(detections)} detections.")

    finally:
        # Always delete recording post processing
        if os.path.exists(file_path):
            os.remove(file_path)
            print("Deleted recording.")

    print("Pipeline run complete.")


if __name__ == "__main__":
    run_pipeline()
