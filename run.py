"""
This is a small audio/visualization tool. It creates two
animated graphs and an audio the_sig.
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np

import audio  
import my_sig
import control

PARAMS = {
	'LEN_TRACE_VIS' : 256,	#How much of trace to show
	'LEN_TRACE_WIN' : 30,	#Size of the FFT window
	'SPEC_MAX_TIME' : 50,  #Time to show on spectrogram
	'SPREAD'        : 20,	#Distance between spec lines
	}

assert PARAMS['LEN_TRACE_VIS'] > 0 
assert PARAMS['LEN_TRACE_WIN'] > 0 
assert PARAMS['SPEC_MAX_TIME'] > 0 
assert PARAMS['LEN_TRACE_WIN'] <= PARAMS['LEN_TRACE_VIS']

#For backend
data = control.initialize(PARAMS)

#init
fig  = plt.figure(figsize=(12, 10), facecolor='white')
ax_t = plt.subplot2grid( (2,1), (0,0) )
ax   = plt.subplot2grid( (2,1), (1,0) )

line_t, = ax_t.plot(np.zeros(PARAMS['LEN_TRACE_VIS']), color="blue")

LWR_BND = -1

ax_t.set_ylim(LWR_BND, data['max_sig_val']+1)

#green line specifying where transform window occurs
ax_t.plot((PARAMS['LEN_TRACE_WIN'], PARAMS['LEN_TRACE_WIN'] ), (LWR_BND, data['max_sig_val']+1 ), 'g-')

X = np.linspace(0, 1, PARAMS['SPEC_MAX_TIME'])

lines = []
for i in range(len(data['spec'])):
	#perspective trick
	xscale = 1 - i / 200
	lw = 1.5 - i / 100
	if i == 0:
		line, = ax.plot(xscale*X, 2*i + data['spec'][i], color="green", lw=lw)
	else:
		line, = ax.plot(xscale*X, 2*i + data['spec'][i], color="cyan", lw=lw)

	lines.append(line)

ax.grid(True)
ax.set_ylim(LWR_BND, 350)
ax_t.set_axis_bgcolor('grey')
ax.set_axis_bgcolor('grey')

data['line_t'] = line_t
data['lines'] = lines
anim = animation.FuncAnimation(fig, control.engine, fargs=([data, PARAMS]), interval=1)
plt.show()

