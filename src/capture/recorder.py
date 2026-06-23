
import os
from datetime import datetime, timezone

import sounddevice as sd
from scipy.io.wavfile import write


class AudioRecorder:
    """A class for the audio recording."""

    def __init__(self, output_dir: str, sample_rate: int) -> None:
        self.output_dir: str = output_dir
        self.sample_rate = sample_rate

    def record_audio(self, duration_seconds: int=30) -> str:
        """Record audio and save to file"""

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"recording_{timestamp}.wav")

        audio_data = sd.rec(
            int(duration_seconds * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,  # mono is enough
            dtype="int16"
        )

        sd.wait()  # wait until recording is finished

        write(filename, self.sample_rate, audio_data)
        return filename


# if __name__ == "__main__":
#     recordings_dir = os.getenv("RECORDINGS_DIR", "/app/recordings")
#     audio_rec = AudioRecorder(recordings_dir, 44100)
#     recording = audio_rec.record_audio(30)
#     print("Recording,", recording, ", captured!")
