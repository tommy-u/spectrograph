"""
Creates sound by combining and modulating sin waves. Very basic.
"""
import numpy as np
import pyaudio
def play_sound(data):
    """
    Plays sound for visualization.
    """
    #Plays tone proportional to time varying signal.
    #play_tone(data['stream'], data['tone'] * 500 + 30)
    #Plays chord with components equal to the magnitude of the transform coefficients.
    chord = data['spec'][:, data['spec'].shape[1]-1][1:]
    play_chord(data['stream'], chord)

def create_stream():
    """
    How sound is played.
    """
    #Audio stream
    return pyaudio.PyAudio().open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)

import math
def sin(frequency, amp, length, rate):
    """
    Creats sin wave.
    """
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return .01 * amp * np.sin(np.arange(length) * factor)

def play_tone(stream, frequency, length=.1, rate=44100):
    """
    Plays single pure sin wave.
    """
    chunks = []
    chunks.append(sin(frequency, 1, length, rate))
    chunk = np.concatenate(chunks) * 0.25
    stream.write(chunk.astype(np.float32).tostring())

def play_chord(stream, amp, length=.1, rate=44100):
    """
    Creates a cord by adding the influence of multiple pure sin waves.
    Component sin waves are assumed to be distributed linearly from
    200 to 3000 hz.
    """
    #CEG in various octaves
    freq = [65.4, 82.25, 98.0, 130.8, 164.5, 196.0, 261.6, 329.0, 392.0, 523.2, 658.0, 784.0, 1046.4, 1316.0, 1568.0, 2092.8, 2632.0, 3136.0]
    freq = freq[3:3+len(amp)]
    chord = []

    while len(freq) != 0:
        tmp = []
        tmp.append(sin(freq[0], amp[0], length, rate))
        if chord == []:
            chord = np.concatenate(tmp)
        else:
            chord += np.concatenate(tmp)
        freq = freq[1:]
        amp = amp[1:]

    stream.write(chord.astype(np.float32).tostring())
