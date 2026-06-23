import os

from src.capture.recorder import AudioRecorder
from src.detection.birdnet import BirdNetAudio
from src.storage.crud import insert_detections


def run_pipeline():
    print("Starting pipeline...")

    # Record audio
    recordings_dir = os.getenv("RECORDINGS_DIR", "/app/recordings")
    audio_recorder = AudioRecorder(recordings_dir, 44100)  # Will change this eventually to 32 kHz for energy saving
    file_path = audio_recorder.record_audio(30)

    gps_coords = {
        "lat": float(os.getenv("STATION_LATITUDE", "0.0")),
        "lon": float(os.getenv("STATION_LONGITUDE", "0.0"))
    }

    try:
        # Run BirdNET
        analyzer = BirdNetAudio(gps_coords, file_path)

        # Filter detections
        detections = analyzer.filter_detections(threshold=0.2)

        if not detections:
            print("No valid detections. Deleting recording.")
            return

        # Write to database
        insert_detections(detections)

        print(f"Inserted {len(detections)} detections.")

    finally:
        # Always delete recording post processing unless debugging
        if os.path.exists(file_path):
            if not int(os.getenv("DEBUG", "0")):
                os.remove(file_path)
                print("Deleted recording,", file_path)

    print("Pipeline run complete.")


if __name__ == "__main__":
    run_pipeline()
