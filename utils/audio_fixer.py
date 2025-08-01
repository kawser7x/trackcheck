import os
import subprocess
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import warnings

# ✅ Real ffmpeg detection using subprocess
def find_ffmpeg():
    try:
        path = subprocess.check_output(["which", "ffmpeg"]).decode().strip()
        if os.path.isfile(path):
            return path
    except Exception:
        return None

ffmpeg_path = find_ffmpeg()
if ffmpeg_path:
    AudioSegment.converter = ffmpeg_path
else:
    warnings.warn("⚠️ ffmpeg binary not found. Audio fixing may not work.", RuntimeWarning)

# ✅ Core fixer function
def fix_audio_issues(file_path, output_path="fixed_audio.wav", target_dbfs=-14.0, fade_out_duration=3000):
    try:
        # Load and check
        audio = AudioSegment.from_file(file_path, format="wav")

        # ✅ Clipping fix
        samples = np.array(audio.get_array_of_samples())
        max_val = np.iinfo(samples.dtype).max
        clipped_samples = np.clip(samples, -max_val, max_val)
        audio = audio._spawn(clipped_samples.astype(samples.dtype).tobytes())

        # ✅ Loudness normalization
        change_in_dBFS = target_dbfs - audio.dBFS
        audio = audio.apply_gain(change_in_dBFS)

        # ✅ Fade-out
        if len(audio) > fade_out_duration:
            audio = audio.fade_out(fade_out_duration)

        # ✅ Export
        audio.export(output_path, format="wav")
        return output_path, "✅ Audio fixed successfully."

    except Exception as e:
        return None, f"❌ Error fixing audio: {e}"