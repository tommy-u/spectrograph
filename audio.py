"""
Creates sound by combining and modulating sin waves. Very basic.
"""

import numpy as np

import math
def sin(frequency, amp, length, rate):
    """
    Creats sin wave.
    """
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return amp * np.sin(np.arange(length) * factor)

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
    min_freq = 200
    max_freq = 3000
    freq = np.linspace(min_freq, max_freq, len(amp))

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
