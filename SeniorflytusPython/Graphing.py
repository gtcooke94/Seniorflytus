##### Suggested clean drone startup sequence #####
import time, sys
import ps_drone # Import PS-Drone-API
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

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
xpos = 0
ypos = 0
oldTime = 0
firstFlag = False
#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800)
def getPosition(vx, vy, vz, ts, te):
    global xpos
    global ypos
    xpos = xpos + (vx * (te - ts))/1000
    ypos  = ypos + (vy * (te - ts))/1000

def run(data):
    # update the data
    global xpos
    global ypos
    global oldTime
    global firstFlag   
    #drone.hover()
    ndc = drone.NavDataCount                      # wait for the next NavData-package
    while ndc == drone.NavDataCount:
        time.sleep(0.00001)

    #kalib = (time.time()-reftime)*drone.selfRotation # trys to recalibrate, causing moving sensor-values around 0.0185 deg/sec
    navData = drone.NavData
    angle = navData["demo"][2][2]             # get the current angle
    vx = navData["demo"][4][0]
    vy = navData["demo"][4][1]
    vz = navData["demo"][4][2]
    mx = navData["magneto"][0][0]
    my = navData["magneto"][0][1]
    mz = navData["magneto"][0][2]
    timeDrone = navData["time"][0]
    if (not firstFlag):
        firstFlag = True
        oldTime = timeDrone
    getPosition(vx, vy, vz, oldTime, timeDrone)
    print xpos, ypos, timeDrone
    xdata.append(xpos)
    ydata.append(ypos)
    xmin, xmax = ax.get_xlim()

    ax.set_ylim(-5, 5)
    ax.set_xlim(-5, 5)
    '''
    if timeDrone >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    '''
    line.set_data(xdata, ydata)
    if ((timeDrone - oldTime) > 5):
        drone.forward(1)
    else:
        drone.hover()

    oldTime = timeDrone

    return line,


ani = animation.FuncAnimation(fig, run, blit=False, interval=10,
                              repeat=False, init_func=init)
plt.show()
# Make this work
#ani.save('hoverExample.mp4', writer=writer)


drone.stop()
time.sleep(2)
drone.land()
