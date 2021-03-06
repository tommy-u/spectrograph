"""
Controls initialization and looping of animation. An attempt is made to separate
out all audio and visual specific code to other modules and only perfrom the backend
number crunching here.
"""
import my_sig
import numpy as np

import audio, video

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
#    the_sig = my_sig.get_the_sea_level_pressure()
#    the_sig = my_sig.get_the_soi()
    the_sig = my_sig.get_the_collatz() #Long Collatz seq
    the_sig = np.log(the_sig) #Reduce to smaller range
    max_sig_val = np.amax(the_sig)

    #Spectrogram 2d array amplitudes of various frequencies fn time.
    spec = np.zeros(((params['LEN_TRACE_WIN'] / 2) + 1, params['SPEC_MAX_TIME']))

    #The transformation window.
    trace_win = np.zeros(params['LEN_TRACE_WIN'])

    #The visible trace.
    trace_vis = np.zeros(params['LEN_TRACE_WIN'])
    trace_vis = np.append(
        trace_vis,
        the_sig[: params['LEN_TRACE_VIS'] - params['LEN_TRACE_WIN']])

    #zero len(trace_win) elements of trace_win_fft
    trace_win_fft = np.zeros(params['LEN_TRACE_WIN'])
    tone = 0

    return {
        'the_sig'       : the_sig,
        'spec'          : spec,
        'trace_win'     : trace_win,
        'trace_vis'     : trace_vis,
        'trace_win_fft' : trace_win_fft,
        'tone'          : tone,
        'max_sig_val'   : max_sig_val,
        }

def init_frontend(params, data):
    """
    Prepairs the two visuals, a trace, and a spectrogram.
    """
    #prep audio component
    data['stream'] = audio.create_stream()
    data = video.init_plots(params, data)
    return data

def run():
    """
    Starts the show.
    """
    video.kickoff()

def initialize(params):
    """
    Prepairs the back and front ends to create animation.
    """
    data = init_backend(params)
    data = init_frontend(params, data)

    return data



def engine(i, params, data):
    """
    The loop that updates the data and redraws the plots. Called from bottom of
    video.init_plots.
    """
    video.draw_animations(params, data)

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

    audio.play_sound(data)


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
