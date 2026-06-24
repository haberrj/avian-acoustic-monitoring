import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer


class BirdNetAudio:
    """A class for analysing the audio via BirdNet"""
    def __init__(self, gps_coords: Dict[str, float], recording: str) -> None:
        if not os.path.exists(recording):
            raise FileNotFoundError(f"Could not find the recording, {recording}.")
        self.latitude: float = gps_coords['lat']
        self.longitude: float = gps_coords['lon']
        self.filename: str = recording
        self.timestamp: datetime = self._extract_timestamp_from_filename()

    def _extract_timestamp_from_filename(self) -> datetime:
        filename = os.path.basename(self.filename)
        timestamp_str = filename.replace('recording_', "").replace(".wav", "")
        dt = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
        dt = dt.replace(tzinfo=timezone.utc)
        return dt

    def _analyze_audio(self) -> List[Any]:
        """Run BirdNET analysis on an audio file"""
        analyzer = Analyzer()
        recording = Recording(
            analyzer,
            self.filename,
            lat=self.latitude,
            lon=self.longitude,
            date=self.timestamp.date()
        )
        recording.analyze()

        return recording.detections
    
    def filter_detections(self, threshold: float = 0.7) -> List[Any]:
        """Filters the detections based on a confidence threshold to prevent
        false positives."""
        analysis = self._analyze_audio()
        detections = []
        for detection in analysis:
            print(detection)
            if detection['confidence'] >= threshold:
                duration = detection.get("end_time", 0.0) - detection.get("start_time", 0.0)
                if duration < 0.0:
                    print(f"Skipping detection @ {detection.get('start_time')} invalid call duration.")
                    continue  # Ignore the detection altogether
                detection['call_duration'] = duration
                start_offset = detection.get("start_time", 0)
                event_time = self.timestamp + timedelta(seconds=start_offset)
                detection['timestamp'] = self.timestamp
                detection['event_time'] = event_time
                detection['longitude'] = self.longitude
                detection['latitude'] = self.latitude
                detections.append(detection)
        return detections
