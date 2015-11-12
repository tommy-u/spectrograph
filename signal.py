import numpy as np

def get_the_saw():
    """
    Collects the signal.
    """
    return np.fromiter( (x%100 for x in range(1,5000)) , int )

def get_the_collatz(x=63728127):
    seq = []
    seq = collatz_sequence(seq, x)
    return np.asarray(seq)

def collatz_sequence(seq, x):
    seq.append(x)
    if x == 1:
        return seq
    x = x/2 if (x % 2 == 0)  else x*3+1
    return collatz_sequence(seq, x)
