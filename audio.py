import numpy as np

import math
def sin(frequency, amp, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return amp * np.sin(np.arange(length) * factor)

def play_tone(stream, frequency, length=.1, rate=44100):
    chunks = []
    chunks.append(sin(frequency, 1, length, rate))
    chunk = np.concatenate(chunks) * 0.25
    stream.write(chunk.astype(np.float32).tostring())

def play_chord(stream, amp, length=.1, rate=44100):
    freq = np.linspace(200,3000,len(amp))
    
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
