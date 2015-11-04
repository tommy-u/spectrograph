"""
This is a small audio/visualization tool. It creates two
animated graphs and an audio signal.
"""

import numpy as np
#for animation
import matplotlib.pyplot as plt
import matplotlib.animation as animation

LEN_TRACE_VIS = 256	#How much of trace to show
LEN_TRACE_WIN = 64 	#Size of the FFT window
SPEC_MAX_TIME = 10  #Time to show on spectrogram

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
	spec = np.zeros( (LEN_TRACE_WIN, SPEC_MAX_TIME) )
		
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
	#standin for animation
	line.set_ydata( data['trace_vis'] )
	#printout(data)

	#input('enter to continue')

	#Remove oldest data 
	data['trace_win'] = np.delete( data['trace_win'], 0 )
	data['trace_vis'] = np.delete( data['trace_vis'], 0 )

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
	data['trace_win_fft'] = np.abs( np.fft.fft ( data['trace_win'] ) )
	
	#probably throw out first elem (vertical offset)
	
	#Append as col. 
	data['spec'] = np.c_[data['spec'], data['trace_win_fft']]

def printout(data):
	for key, value in data.items():
		print(key, value)

def animation():
	#For animation
	fig, ax = plt.subplots()
	x = np.arange(0, LEN_TRACE_VIS)
	line, = ax.plot(x, np.sin(x))
	LWR_BND = -1
	ax.set_ylim(LWR_BND, data['max_sig_val']+1)
	ax.plot((LEN_TRACE_WIN, LEN_TRACE_WIN ), (LWR_BND, data['max_sig_val']+1 ), 'g-')
	#For backend
	data = initialize()
	
	#data is sent in as a list because it's going to be unpacked.
	animation.FuncAnimation(fig, engine, fargs= [data], interval=10)
	
	plt.show()

data = initialize()
animation()











