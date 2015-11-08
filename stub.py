"Why does the recursive one return None"

def append_5(seq):
	seq.append(5)
	return seq

print('result of append_5: ',append_5([]))
#prints [5]

# def collatz_sequence(seq, x):
#     seq = seq + [x]
#     print(seq)
#     input('p2')
#     if x == 1:
#         return [seq]
#     if (x % 2) == 0:
#         collatz_sequence(seq, x / 2)
#     else:
#         collatz_sequence(seq, (x * 3) + 1)



print ('result of collats(4): ', collatz_sequence([],4))
#prints None
