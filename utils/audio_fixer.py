import os
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from pydub.utils import which
import pyloudnorm as pyln
import warnings

# ✅ Step 1: Ensure ffmpeg is available for pydub
ffmpeg_path = which("ffmpeg")
if ffmpeg_path:
    AudioSegment.converter = ffmpeg_path
else:
    warnings.warn("⚠️ ffmpeg not found. Audio fixing may not work.", RuntimeWarning)

def fix_audio_issues(file_path, output_path="fixed_audio.wav", target_lufs=-14.0, fade_out_duration=3000):
    try:
        # ✅ Step 2: Load audio using pydub
        audio = AudioSegment.from_file(file_path, format="wav")

        # ✅ Step 3: Convert to numpy array for loudness & clipping analysis
        samples = np.array(audio.get_array_of_samples())
        sample_width = audio.sample_width * 8
        dtype = np.int16 if sample_width == 16 else np.int32
        max_val = np.iinfo(dtype).max

        # ✅ Step 4: Detect & fix clipping
        clipped = np.clip(samples, -max_val, max_val)
        audio = audio._spawn(clipped.astype(dtype).tobytes())

        # ✅ Step 5: Normalize LUFS using pyloudnorm
        samples_float32 = clipped.astype(np.float32) / max_val
        meter = pyln.Meter(audio.frame_rate)  # LUFS meter
        loudness = meter.integrated_loudness(samples_float32)
        gain_needed = target_lufs - loudness
        audio = audio.apply_gain(gain_needed)

        # ✅ Step 6: Fade out
        if len(audio) > fade_out_duration:
            audio = audio.fade_out(fade_out_duration)

        # ✅ Step 7: Export to fixed WAV
        audio.export(output_path, format="wav")

        return output_path, f"✅ Audio fixed successfully. LUFS adjusted from {loudness:.2f} to {target_lufs}."

    except Exception as e:
        return None, f"❌ Error fixing audio: {e}"