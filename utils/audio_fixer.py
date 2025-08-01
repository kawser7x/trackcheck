import numpy as np
import soundfile as sf

def fix_audio_issues(file_path, output_path="fixed_audio.wav", target_dbfs=-14.0, fade_out_duration_ms=3000):
    try:
        # 1. Load WAV file
        data, samplerate = sf.read(file_path)
        
        # Convert stereo to mono if needed
        if data.ndim > 1:
            data = np.mean(data, axis=1)

        # 2. Normalize loudness
        rms = np.sqrt(np.mean(data**2))
        current_dbfs = 20 * np.log10(rms) if rms > 0 else -np.inf
        gain = 10 ** ((target_dbfs - current_dbfs) / 20)
        data *= gain

        # 3. Remove clipping (limit within [-1.0, 1.0])
        data = np.clip(data, -1.0, 1.0)

        # 4. Apply fade-out
        fade_samples = int((fade_out_duration_ms / 1000) * samplerate)
        if len(data) > fade_samples:
            fade_curve = np.linspace(1.0, 0.0, fade_samples)
            data[-fade_samples:] *= fade_curve

        # 5. Save fixed WAV
        sf.write(output_path, data, samplerate)

        return output_path, "✅ Audio fixed successfully (WAV-only, no ffmpeg used)."

    except Exception as e:
        return None, f"❌ Error fixing audio: {e}"