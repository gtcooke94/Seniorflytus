import time, sys
import ps_drone # Import PS-Drone-API
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#fileName = raw_input("Log File Name: " )
#fileName = fileName + ".txt"
drone = ps_drone.Drone() # Start using drone    
drone.startup() # Connects to drone and starts subprocesses

drone.reset() # Sets drone's status to good
while (drone.getBattery()[0]==-1): time.sleep(0.1) # Wait until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"% "+str(drone.getBattery()[1]) # Battery-status
if drone.getBattery()[1]=="empty": sys.exit() # Give it up if battery is empty

drone.useDemoMode(False) # Set 15 basic dataset/sec (default anyway)
drone.addNDpackage(["demo"]) # Packets, which shall be decoded
drone.addNDpackage(["magneto"])
drone.addNDpackage(["time"])
drone.getNDpackage(["all"])
time.sleep(0.5) # Give it some time to awake fully

#drone.trim() # Recalibrate sensors
#drone.getSelfRotation(5) # Get auto-alteration of gyroscope-sensor
#print "Auto-alt.:"+str(drone.selfRotation)+"dec/s" # Showing value for auto-alteration

drone.takeoff() # Fly, drone, fly !
while drone.NavData["demo"][0][2]: time.sleep(0.1) # Wait until drone is completely flying

##### Mainprogram begin #####
print "Drone is flying now"

stop = False


while (not stop):
    if (drone.getKey() == 'c'): stop = True
    drone.hover()
    ndc = drone.NavDataCount                      # wait for the next NavData-package
    while ndc == drone.NavDataCount:
        time.sleep(0.00001)

    kalib = (time.time()-reftime)*drone.selfRotation # trys to recalibrate, causing moving sensor-values around 0.0185 deg/sec
    navData = drone.NavData
    cpos = navData["demo"][2][2]             # get the current angle
    vx = navData["demo"][4][0]
    vy = navData["demo"][4][1]
    vz = navData["demo"][4][2]
    mx = navData["magneto"][0][0]
    my = navData["magneto"][0][1]
    mz = navData["magneto"][0][2]
    timeDrone = navData["time"]
    plt.plot(vx, vy)

"""
=====
Decay
=====

This example showcases a sinusoidal decay animation.
"""





def data_gen(t=0):
    #Get data from drone


def init():
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlim(0, 10)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = [], []


def run(data):
    # update the data
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,
