import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update(*args):
    #Right shift, duplicate 0th element
    data[:, 1:] = data[:, :-1]
    # Overwrite element 0 with new data
    data[:, 0] = np.random.uniform(0, 1, len(data))

    # Update lines
    for i in range(len(data)):
       lines[i].set_ydata(i + G * data[i])
#        lines[i].set_ydata(i + data[i])
    return lines

# Create new Fig
fig = plt.figure(figsize=(8, 8), facecolor='brown')
ax = plt.subplot(frameon=False)

num_lines = 50
num_data = 75
data = np.zeros((num_lines, num_data)) 

# Domain
X = np.linspace(0, 1, num_data)

# Controls amplitude of envelope. 
G = 1.5 * np.exp(-4 * X * X)

lines = []
for i in range(len(data)):
    # Small reduction of the X extents to get a cheap perspective effect
    xscale = 1 - i / 200.
    # Same for linewidth (thicker strokes on bottom)
    lw = 1.5 - i / 100.0

    line, = ax.plot(xscale * X, i + data[i], color="white", lw=lw)
    lines.append(line)

# Set y limit (or first line is cropped because of thickness)
ax.set_ylim(-1, 53)

#ax.set_xticks([])
#ax.set_yticks([])

# Construct the animation, using the update function as the animation director
anim = animation.FuncAnimation(fig, update, interval=1)
plt.show()