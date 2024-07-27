import pyaudio
import numpy as np
import librosa
import soundfile as sf
import noisereduce as nr

# Parameters for audio processing
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100

def process_audio(audio_data, modulation_type, param=None):
    y, sr = sf.read(audio_data, dtype='float32')
    # Apply noise reduction
    y = nr.reduce_noise(y=y, sr=sr)

    if modulation_type == 'male_to_female':
        y_mod = librosa.effects.pitch_shift(y, sr, n_steps=4)
    elif modulation_type == 'female_to_male':
        y_mod = librosa.effects.pitch_shift(y, sr, n_steps=-4)
    elif modulation_type == 'change_pitch' and param is not None:
        y_mod = librosa.effects.pitch_shift(y, sr, n_steps=param)
    elif modulation_type == 'change_speed' and param is not None:
        y_mod = librosa.effects.time_stretch(y, param)
    elif modulation_type == 'change_loudness' and param is not None:
        y_mod = librosa.effects.preemphasis(y, coef=param)
    else:
        y_mod = y
    return y_mod, sr

def save_audio(audio_data, file_path):
    sf.write(file_path, audio_data, RATE)
