# Uncomment the next two lines if you want to save the animation
#import matplotlib
#matplotlib.use("Agg")

import numpy
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation



# Sent for figure
font = {'size'   : 9}
matplotlib.rc('font', **font)

# Setup figure and subplots
f0 = figure(num = 0, figsize = (12, 8))#, dpi = 100)
f0.suptitle("Oscillation decay", fontsize=12)
ax01 = subplot2grid((2, 1), (0, 0))
ax03 = subplot2grid((2, 1), (1, 0))

#tight_layout()

# Set titles of subplots
ax01.set_title('Position vs Time')
ax03.set_title('Position and Velocity vs Time')

# set y-limits
ax01.set_ylim(0,2)
ax03.set_ylim(-0,5)


# sex x-limits
ax01.set_xlim(0,5.0)
ax03.set_xlim(0,5.0)


# Turn on grids
ax01.grid(True)
ax03.grid(True)

# set label names
ax01.set_xlabel("x")
ax01.set_ylabel("py")
ax03.set_xlabel("t")
ax03.set_ylabel("py")


# Data Placeholders
yp1=zeros(0)
yv1=zeros(0)
yp2=zeros(0)
yv2=zeros(0)
t=zeros(0)

# set plots
p011, = ax01.plot(t,yp1,'b-', label="yp1")
p012, = ax01.plot(t,yp2,'g-', label="yp2")



p031, = ax03.plot(t,yp1,'b-', label="yp1")


# set lagends
ax01.legend([p011,p012], [p011.get_label(),p012.get_label()])


# Data Update
xmin = 0.0
xmax = 5.0
x = 0.0

def updateData(self):
	global x
	global yp1
	global yv1
	global yp2
	global yv2
	global t

	tmpp1 = 1 + exp(-x) *sin(2 * pi * x)
	tmpv1 = - exp(-x) * sin(2 * pi * x) + exp(-x) * cos(2 * pi * x) * 2 * pi
	yp1=append(yp1,tmpp1)
	yv1=append(yv1,tmpv1)
	yp2=append(yp2,0.5*tmpp1)
	yv2=append(yv2,0.5*tmpv1)
	t=append(t,x)

	x += 0.05

	p011.set_data(t,yp1)
	p012.set_data(t,yp2)


	p031.set_data(t,yp1)


	if x >= xmax-1.00:
		p011.axes.set_xlim(x-xmax+1.0,x+1.0)

		p031.axes.set_xlim(x-xmax+1.0,x+1.0)


	return p011, p031

# interval: draw new frame every 'interval' ms
# frames: number of frames to draw
simulation = animation.FuncAnimation(f0, updateData, blit=False, frames=200, interval=20, repeat=False)

# Uncomment the next line if you want to save the animation
#simulation.save(filename='sim.mp4',fps=30,dpi=300)

plt.show()
