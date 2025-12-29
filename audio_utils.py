import librosa
import numpy as np

def extract_audio_peaks(audio_path, sr=22050):
    y, sr = librosa.load(audio_path, sr=sr)

    rms = librosa.feature.rms(y=y)[0]
    rms = (rms - rms.min()) / (rms.max() - rms.min())

    times = librosa.frames_to_time(range(len(rms)), sr=sr)

    peaks = []
    for t, e in zip(times, rms):
        if e > 0.75:
            peaks.append((t, float(e)))

    return peaks
