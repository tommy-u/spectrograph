"""
Controls initialization and looping of animation.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import my_sig
import numpy as np
import pyaudio

import audio

def printout(data):
    """
    For debugging backend values.
    """

    for key, value in data.items():
        print(key, value)

def init_backend(params):
    """
    Prepairs all data arrays for the animation loop.
    Returns them in a dictionary.
    """
    #Collect Signal
    the_sig = my_sig.get_the_collatz() #Long Collatz seq
    the_sig = np.log(the_sig) #Reduce to smaller range
    max_sig_val = np.amax(the_sig)

    #Spectrogram 2d array
    spec = np.zeros(((params['LEN_TRACE_WIN'] / 2) + 1, params['SPEC_MAX_TIME']))

    #The window
    trace_win = np.zeros(params['LEN_TRACE_WIN'])

    #
    trace_vis = np.zeros(params['LEN_TRACE_WIN'])
    trace_vis = np.append(
        trace_vis,
        the_sig[: params['LEN_TRACE_VIS'] - params['LEN_TRACE_WIN']])

    #zero len(trace_win) elements of trace_win_fft
    trace_win_fft = np.zeros(params['LEN_TRACE_WIN'])
    tone = 0

    #prep audio component
    pya = pyaudio.PyAudio()
    stream = pya.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)

    return {
        'the_sig'       : the_sig,
        'spec'          : spec,
        'trace_win'     : trace_win,
        'trace_vis'     : trace_vis,
        'trace_win_fft' : trace_win_fft,
        'tone'          : tone,
        'max_sig_val'   : max_sig_val,
        'stream'        : stream
        }

def init_frontend(params, data):
    """
    Prepairs the two visuals, a trace, and a spectrogram.
    """
    #Plots
    fig = plt.figure(figsize=(12, 10), facecolor='white')
    #Trace subplot
    trsp = plt.subplot2grid((2, 1), (0, 0))
    #Spectrogram sub plot
    ssp = plt.subplot2grid((2, 1), (1, 0))

    line_t, = trsp.plot(np.zeros(params['LEN_TRACE_VIS']), color="blue")

    params['LWR_BND'] = -1

    trsp.set_ylim(params['LWR_BND'], data['max_sig_val']+1)

    #green line specifying where transform window occurs
    trsp.plot(
        (params['LEN_TRACE_WIN'], params['LEN_TRACE_WIN']),
        (params['LWR_BND'], data['max_sig_val']+1), 'g-')

    domain = np.linspace(0, 1, params['SPEC_MAX_TIME'])

    lines = []
    for i in range(len(data['spec'])):
        #perspective trick
        xscale = 1 - i / 200
        lnw = 1.5 - i / 100
        if i == 0:
            line, = ssp.plot(xscale*domain, 2*i + data['spec'][i], color="green", lw=lnw)
        else:
            line, = ssp.plot(xscale*domain, 2*i + data['spec'][i], color="cyan", lw=lnw)

        lines.append(line)

    ssp.grid(True)
    ssp.set_ylim(params['LWR_BND'], 350)
    trsp.set_axis_bgcolor('grey')
    ssp.set_axis_bgcolor('grey')

    #Add frontend data.
    data['line_t'] = line_t
    data['lines'] = lines
    data['fig'] = fig
    return data

def run():
    """
    Starts the animation.
    """
    plt.show()

def initialize(params):
    """
    Prepairs the back and front ends to create animation.
    """
    data = init_backend(params)
    data = init_frontend(params, data)

    animation.FuncAnimation(data['fig'], engine, fargs=([data, params]), interval=1)

    return data

def engine(i, data, params):
    """
    The loop that updates the data and redraws the plots.
    """

    #Redraw trace animation.
    data['line_t'].set_ydata(data['trace_vis'])

    #Redraw spectrogram animation.
    for i in range(len(data['lines'])):
        data['lines'][i].set_ydata(data['spec'][i] + params['SPREAD'] * i)

    #Remove oldest data from backend.
    data['trace_win'] = np.delete(data['trace_win'], 0)
    data['trace_vis'] = np.delete(data['trace_vis'], 0)
    #Deletes col 1 of spectogram matrix.
    data['spec'] = np.delete(data['spec'], 0, 1)

    #What to append into the transform window, more signal or 0's at end.
    fill = data['the_sig'][0] if (np.size(data['the_sig']) > 0) else 0
    data['trace_win'] = np.append(data['trace_win'], fill)

    #Play audio component.
    data['tone'] = fill / data['max_sig_val']

    #Plays tone proportional to time varying signal.
    #audio.play_tone(data['stream'], data['tone'] * 500 + 30)
    #Plays chord with components equal to the magnitude of the transform coefficients.
    chord = data['spec'][:, data['spec'].shape[1]-1][1:]
    audio.play_chord(data['stream'], chord)

    #Pull next element out of signal that's not yet visible, add it to the trace.
    len_non_win = params['LEN_TRACE_VIS'] - params['LEN_TRACE_WIN']
    fill = data['the_sig'][len_non_win] if (np.size(data['the_sig']) > len_non_win) else 0
    data['trace_vis'] = np.append(data['trace_vis'], fill)

    #Removes oldest element of the signal.
    if np.size(data['the_sig']) > 0:
        data['the_sig'] = np.delete(data['the_sig'], 0)

    #Calc rfft of the window.
    data['trace_win_fft'] = np.abs(np.fft.rfft(data['trace_win']))

    #Append the vector of fourier components to the spectrogram.
    data['spec'] = np.c_[data['spec'], data['trace_win_fft']]
