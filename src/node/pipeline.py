import os

from src.node.capture.recorder import AudioRecorder
from src.node.detection.birdnet import BirdNetAudio
from src.node.payload import build_detection_payload
from src.node.uploader import upload_detection_payload


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

    threshold = float(os.getenv("BIRD_CONFIDENCE_THRESHOLD", "0.2"))
    try:
        # Run BirdNET
        analyzer = BirdNetAudio(gps_coords, file_path)

        # Filter detections
        detections = analyzer.filter_detections(threshold=threshold)

        if not detections:
            print("No valid detections. Deleting recording.")
            return

        # Write to database
        print("Building upload payload...")
        payload = build_detection_payload(detections, file_path)
        print("Payload built successfully")
        upload_detection_payload(payload)
        print(f"Uploaded {len(detections)} detections.")

    finally:
        # Always delete recording post processing unless debugging
        if os.path.exists(file_path):
            if not int(os.getenv("DEBUG", "0")):
                os.remove(file_path)
                print("Deleted recording,", file_path)

    print("Pipeline run complete.")


if __name__ == "__main__":
    run_pipeline()
