"""
Controls visual plots, animated graphs.
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import control

def kickoff():
    """
    Start the animation.
    """
    plt.show()

def draw_animations(params, data):
    """
    Updates animated graphs.
    """
    #Redraw trace animation.
    data['line_t'].set_ydata(data['trace_vis'])

    #Redraw spectrogram animation.
    for i in range(len(data['lines'])):
        data['lines'][i].set_ydata(data['spec'][i] + params['SPREAD'] * i)

def init_plots(params, data):
    """
    Preps animations.
    """
    #Plots
    fig = plt.figure(figsize=(12, 10), facecolor='white')
    #Trace subplot
    trsp = plt.subplot2grid((2, 1), (0, 0))
    #Spectrogram sub plot
    ssp = plt.subplot2grid((2, 1), (1, 0))

    line_t, = trsp.plot(np.zeros(params['LEN_TRACE_VIS']), color="blue")

    lwr_bound = -1

    trsp.set_ylim(lwr_bound, data['max_sig_val']+1)

    #green line specifying where transform window occurs
    trsp.plot(
        (params['LEN_TRACE_WIN'], params['LEN_TRACE_WIN']),
        (lwr_bound, data['max_sig_val']+1), 'g-')

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
    ssp.set_ylim(lwr_bound, 350)
    trsp.set_axis_bgcolor('grey')
    ssp.set_axis_bgcolor('grey')

    #Add frontend data.
    data['fig'] = fig
    data['line_t'] = line_t
    data['lines'] = lines

    animation.FuncAnimation(data['fig'], control.engine, fargs=([params, data]), interval=1)

    return data
