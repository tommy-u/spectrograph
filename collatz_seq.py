seq = []

def collatz_sequence(x):
    global seq
    seq.append(x)
    if x == 1:
        return 
    if (x % 2) == 0:
        collatz_sequence(x / 2)
    else:
        collatz_sequence((x * 3) + 1)

collatz_sequence(63728127)
print (len(seq))