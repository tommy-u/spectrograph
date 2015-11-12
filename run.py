"""
This is a small audio/visualization tool. It creates two
animated graphs and an audio the_sig.
"""

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

import my_sig	#The input signal under inspection
import audio	#Tool for making sounds
import control	#For Coorinating Animation & Sound

PARAMS = {
	'LEN_TRACE_VIS' : 256,	#How much of trace to show
	'LEN_TRACE_WIN' :  30,	#Size of the FFT window
	'SPEC_MAX_TIME' :  50,  #Time to show on spectrogram
	'SPREAD'        :  20,	#Distance between spec lines
	'LWR_BND'		:  -1	#Bottom of trace graph
	}

assert PARAMS['LEN_TRACE_VIS'] > 0 
assert PARAMS['LEN_TRACE_WIN'] > 0 
assert PARAMS['SPEC_MAX_TIME'] > 0 
assert PARAMS['LEN_TRACE_WIN'] <= PARAMS['LEN_TRACE_VIS']

#For backend
control.initialize(PARAMS)
control.run()
