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

def init_backend( PARAMS ):
	"""
	Prepairs all data arrays for the animation loop.
	Returns them in a dictionary.
	"""
	#Collect Signal
	the_sig = my_sig.get_the_collatz() #Long Collatz seq
	the_sig = np.log(the_sig) #Reduce to smaller range

	max_sig_val = np.amax( the_sig )

	#Spectrogram 2d array
	spec = np.zeros( ( (PARAMS['LEN_TRACE_WIN'] / 2 ) + 1 , PARAMS['SPEC_MAX_TIME']) )
		
	#The window
	trace_win = np.zeros( PARAMS['LEN_TRACE_WIN'] )
	
	#The 
	trace_vis = np.zeros( PARAMS['LEN_TRACE_WIN'] )
	trace_vis = np.append ( trace_vis, the_sig[ : PARAMS['LEN_TRACE_VIS'] - PARAMS['LEN_TRACE_WIN'] ] )
	
	#zero len(trace_win) elements of trace_win_fft
	trace_win_fft = np.zeros( PARAMS['LEN_TRACE_WIN'] )
	tone = 0

	#prep audio component
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paFloat32,channels=1, rate=44100, output=1)

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

def init_frontend( PARAMS, data ):
	"""
	Prepairs the two visuals, a trace, and a spectrogram.
	"""
	#Plots
	fig  = plt.figure(figsize=(12, 10), facecolor='white')
	#1d signal trace
	ax_t = plt.subplot2grid( (2,1), (0,0) )
	#Spectrogram
	ax   = plt.subplot2grid( (2,1), (1,0) )
	
	line_t, = ax_t.plot(np.zeros(PARAMS['LEN_TRACE_VIS']), color="blue")
	
	PARAMS['LWR_BND'] = -1
	
	ax_t.set_ylim(PARAMS['LWR_BND'], data['max_sig_val']+1)
	
	#green line specifying where transform window occurs
	ax_t.plot((PARAMS['LEN_TRACE_WIN'], PARAMS['LEN_TRACE_WIN'] ), (PARAMS['LWR_BND'], data['max_sig_val']+1 ), 'g-')
	
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
	ax.set_ylim(PARAMS['LWR_BND'], 350)
	ax_t.set_axis_bgcolor('grey')
	ax.set_axis_bgcolor('grey')
	
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

def initialize( PARAMS ):
	"""
	Prepairs the back and front ends to create animation.
	"""
	data = init_backend( PARAMS )
	data = init_frontend( PARAMS, data )

	animation.FuncAnimation( data['fig'], engine, fargs=([data, PARAMS]), interval=1)
	
	return data
	
def engine(i,data, PARAMS):	
	"""
	The loop that updates the data and redraws the plots.
	"""

	#Trace animation.
	data['line_t'].set_ydata( data['trace_vis'] )

	#Spectrogram animation.
	for i in range(len(data['lines'])):
		data['lines'][i].set_ydata( data['spec'][i] + PARAMS['SPREAD'] * i )

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
	#audio.play_tone(data['stream'], data['tone'] * 500 + 30)
	chord = data['spec'][:, data['spec'].shape[1]-1 ][1:]
	audio.play_chord( data['stream'], chord )

	#vis
	fill = data['the_sig'][PARAMS['LEN_TRACE_VIS'] - PARAMS['LEN_TRACE_WIN']] if ( np.size( data['the_sig'] ) > PARAMS['LEN_TRACE_VIS'] - PARAMS['LEN_TRACE_WIN'] ) else 0
	data['trace_vis'] = np.append( data['trace_vis'], fill)

	#data['the_sig']
	if ( np.size(data['the_sig']) > 0 ): data['the_sig'] = np.delete( data['the_sig'], 0 )
	
	#calc fft window sig
	data['trace_win_fft'] = np.abs( np.fft.rfft ( data['trace_win'] ) )

	#Fill every element of the spec with one element from the fft.
	data['spec'] = np.c_[data['spec'], data['trace_win_fft']]	