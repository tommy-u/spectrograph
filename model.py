"""
This is a small audio/visualization tool. It creates two
animated graphs and an audio signal.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyaudio 
import math

LEN_TRACE_VIS = 256	#How much of trace to show
LEN_TRACE_WIN = 30	#Size of the FFT window
SPEC_MAX_TIME = 50  #Time to show on spectrogram
SPREAD        = 20	#Distance between spec lines
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
	# the_sig = get_the_sig()
	the_sig = get_the_collatz(63728127) #Long Collatz seq
	the_sig = np.log(the_sig) #Reduce to smaller range

	#double length
#	the_sig = np.concatenate( [the_sig, the_sig] )

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

def get_the_sig():
	"""
	Collects the signal.
	"""
	return np.fromiter( (x%100 for x in range(1,5000)) , int )

def get_the_collatz(x):
	seq = []
	seq = collatz_sequence(seq, x)
	return np.asarray(seq)

def collatz_sequence(seq, x):
	seq.append(x)
	if x == 1:
		return seq
	x = x/2 if (x % 2 == 0)  else x*3+1
	return collatz_sequence(seq, x)

def engine(i,data):	
	#Trace animation.
	line_t.set_ydata( data['trace_vis'] )

	#Spectrogram animation.
	for i in range(len(lines)):
		lines[i].set_ydata( data['spec'][i] + SPREAD * i )
	# if (len(data['the_sig']) > 0):
	# 	print(data['the_sig'][0])

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
	play_tone(data['stream'], data['tone'] * 500 + 30)

	#vis
	fill = data['the_sig'][LEN_NON_WIN] if ( np.size( data['the_sig'] ) > LEN_NON_WIN ) else 0
	data['trace_vis'] = np.append( data['trace_vis'], fill)

	#data['the_sig']
	if ( np.size(data['the_sig']) > 0 ): data['the_sig'] = np.delete( data['the_sig'], 0 )
	
	#calc fft window sig
	data['trace_win_fft'] = np.abs( np.fft.rfft ( data['trace_win'] ) )

	#This is only to make visualization easier.
	#log of magnitudes
#	data['trace_win_fft'] = np.log( data['trace_win_fft'] )
	#data['trace_win_fft'] = data['trace_win_fft'] 

	#Fill every element of the spec with one element from the fft.
	data['spec'] = np.c_[data['spec'], data['trace_win_fft']]	

def printout(data):
	for key, value in data.items():
		print(key, value)

def sine(frequency, length, rate):
	length = int(length * rate)
	factor = float(frequency) * (math.pi * 2) / rate
	return np.sin(np.arange(length) * factor)

def play_tone(stream, frequency, length=.1, rate=44100):
	chunks = []
	chunks.append(sine(frequency, length, rate))
	chunk = np.concatenate(chunks) * 0.25
	stream.write(chunk.astype(np.float32).tostring())

#For backend
data = initialize()

fig  = plt.figure(figsize=(12, 10), facecolor='white')

ax_t = plt.subplot2grid( (2,1), (0,0) )
ax   = plt.subplot2grid( (2,1), (1,0) )

#For trace animation 
#x = np.arange(0, LEN_TRACE_VIS)
line_t, = ax_t.plot(np.zeros(LEN_TRACE_VIS), color="blue")

LWR_BND = -1
ax_t.set_ylim(LWR_BND, data['max_sig_val']+1)
#green line specifying where transform window occurs
ax_t.plot((LEN_TRACE_WIN, LEN_TRACE_WIN ), (LWR_BND, data['max_sig_val']+1 ), 'g-')


X = np.linspace(0, 1, SPEC_MAX_TIME)

lines = []
for i in range(len(data['spec'])):
	#perspective trick
	xscale = 1 - i / 200
	lw = 1.5 - i / 100
	if i == 0:
		line, = ax.plot(xscale*X, 2*i + data['spec'][i], color="green", lw=lw)
	else:
		line, = ax.plot(xscale*X, 2*i + data['spec'][i], color="brown", lw=lw)

	lines.append(line)
ax.grid(True)
ax.set_ylim(LWR_BND, 350)
ax_t.set_axis_bgcolor('grey')
ax.set_axis_bgcolor('grey')

anim = animation.FuncAnimation(fig, engine, fargs=([data]), interval=1)

plt.show()

