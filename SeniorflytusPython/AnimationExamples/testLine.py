import matplotlib.pyplot as plt
from random import randint
import time

xdata = []
ydata = []
line, = plt.plot(xdata, ydata)
while (True):
	xdata.append(randint(0, 9))
	ydata.append(randint(0, 9))
	line.set_data(xdata, ydata)
	print xdata
	print ydata
	plt.draw()
	plt.show()
	time.sleep(.1)

print "Done"
