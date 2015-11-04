"""
This is a small audio/visualization tool. It creates two
animated graphs and an audio signal.
"""

import numpy as np
#for animation
import matplotlib.pyplot as plt
import matplotlib.animation as animation

LEN_TRACE_VIS = 256	#How much of trace to show
LEN_TRACE_WIN = 20 	#Size of the FFT window
SPEC_MAX_TIME = 50  #Time to show on spectrogram

LEN_NON_WIN = LEN_TRACE_VIS - LEN_TRACE_WIN	

assert LEN_TRACE_VIS > 0 
assert LEN_TRACE_WIN > 0 
assert SPEC_MAX_TIME > 0 
assert LEN_TRACE_WIN <= LEN_TRACE_VIS 

def initialize( ):
	"""
	Prepairs all data arrays for the animation loop.
	Returns them in a dictionary.
	"""

	#Signal
	the_sig = get_the_sig()
	max_sig_val = np.amax( the_sig )

	#Spectrogram 2d array
	spec = np.zeros( ( (LEN_TRACE_WIN/2) + 1 , SPEC_MAX_TIME) )
		
	#The window
	trace_win = np.zeros( LEN_TRACE_WIN )
	
	#The 
	trace_vis = np.zeros( LEN_TRACE_WIN )
	trace_vis = np.append ( trace_vis, the_sig[ : LEN_NON_WIN ] )
	
	#zero len(trace_win) elements of trace_win_fft
	trace_win_fft = np.zeros( LEN_TRACE_WIN )
	tone = 0

	return {
	'the_sig'       : the_sig, 
	'spec'          : spec,
	'trace_win'     : trace_win,
	'trace_vis'     : trace_vis,
	'trace_win_fft' : trace_win_fft,
	'tone'          : tone,
	'max_sig_val'   : max_sig_val
	}

def get_the_sig():
	"""
	Collects the signal.
	"""
	return np.fromiter( (x%100 for x in range(1,5000)) , int )

def engine(i,data):
	
	#Trace animation
	
	#line_t.set_ydata( data['trace_vis'] )

	for i in range(len(lines)):
		lines[i].set_ydata( data['spec'][i] + 4*i )

	#standin for animation
#	printout(data)

	#for pausing between frames
#	input('enter to continue')

	#Remove oldest data 
	data['trace_win'] = np.delete( data['trace_win'], 0 )
	data['trace_vis'] = np.delete( data['trace_vis'], 0 )

	#Deletes from every line	
	data['spec'] = np.delete( data['spec'], 0, 1 )

	#win
	fill = data['the_sig'][0] if ( np.size(data['the_sig']) > 0 ) else 0
	data['trace_win'] = np.append( data['trace_win'], fill )

	#tone
	data['tone'] = fill / data['max_sig_val'] 

	#vis
	fill = data['the_sig'][LEN_NON_WIN] if ( np.size( data['the_sig'] ) > LEN_NON_WIN ) else 0
	data['trace_vis'] = np.append( data['trace_vis'], fill)

	#data['the_sig']
	if ( np.size(data['the_sig']) > 0 ): data['the_sig'] = np.delete( data['the_sig'], 0 )
	
	#calc fft window sig
	data['trace_win_fft'] = np.abs( np.fft.rfft ( data['trace_win'] ) )
	
	#probably throw out first elem (vertical offset)
	
#	data['trace_win_fft'] = data['trace_win_fft'] / np.ptp(data['trace_win_fft'])
	data['trace_win_fft'] = np.log( data['trace_win_fft'] )
	#Append as col. 
	#Total kludge to remove dominating first term
#	data['trace_win_fft'][0] = 0
	data['spec'] = np.c_[data['spec'], data['trace_win_fft']]
	#data['spec'][0] = np.zeros(len(data['spec'][0]))
	
	

def printout(data):
	for key, value in data.items():
		print(key, value)

#For backend
data = initialize()

"""
#For trace animation 
fig_t, ax_t = plt.subplots()

x = np.arange(0, LEN_TRACE_VIS)
line_t, = ax_t.plot(x, np.sin(x))
LWR_BND = -1
ax_t.set_ylim(LWR_BND, data['max_sig_val']+1)
ax_t.plot((LEN_TRACE_WIN, LEN_TRACE_WIN ), (LWR_BND, data['max_sig_val']+1 ), 'g-')

#data is sent in as a list because it's going to be unpacked.
animation.FuncAnimation(fig_t, engine, fargs= [data], interval=10)
"""


fig = plt.figure(figsize=(8, 8), facecolor='brown')
ax = plt.subplot(frameon=False)
#data = np.zeros((LEN_TRACE_WIN, SPEC_MAX_TIME))
X = np.linspace(0, 1, SPEC_MAX_TIME)

lines = []
for i in range(len(data['spec'])):
	#perspective trick
	xscale = 1 - i / 200
	lw = 1.5 - i / 100
	line, = ax.plot(xscale*X, 2*i + data['spec'][i], color="white", lw=lw)
	lines.append(line)

LWR_BND = -1
#ax.set_ylim(LWR_BND, data['max_sig_val']+1)
ax.set_ylim(LWR_BND, 50)



anim = animation.FuncAnimation(fig, engine, fargs=([data]), interval=10)

plt.show()

# while(True):
# 	engine(1,data)





