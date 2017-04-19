import time, sys
import ps_drone # Import PS-Drone-API
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
drone.setSpeed(.1)

#drone.trim()

#drone.trim() # Recalibrate sensors
#drone.getSelfRotation(5) # Get auto-alteration of gyroscope-sensor
#print "Auto-alt.:"+str(drone.selfRotation)+"dec/s" # Showing value for auto-alteration

drone.takeoff() # Fly, drone, fly !
while drone.NavData["demo"][0][2]: time.sleep(0.1) # Wait until drone is completely flying


drone.hover()
time.sleep(.1)
##### Mainprogram begin #####
print "Drone is flying now"
xpos = 0
ypos = 0
firstFlag = False
originalTime = 0
timeDrone = 0


def getPosition(vx, vy, vz, ts, te):
    global xpos
    global ypos
    xpos = xpos + (vx * (te - ts))/1000
    ypos  = ypos + (vy * (te - ts))/1000


def moveForwardX(dist):
	global xpos
	global ypos
	global oldTime
	global timeDrone
	global firstFlag
	ndc = drone.NavDataCount 
	while xpos < dist:
                     # wait for the next NavData-package
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
		    originalTime = timeDrone
		getPosition(vx, vy, vz, oldTime, timeDrone)
		oldTime = timeDrone
		print vx, vy, vz
		print xpos, ypos, angle, timeDrone
		#xdata.append(xpos)
		#ydata.append(ypos)

		drone.moveForward(.1)

	drone.stop()
	time.sleep(1)
	drone.hover()

moveForwardX(1)

drone.stop()
drone.hover()
time.sleep(.1)


xpos = 0
ypos = 0
firstFlag = False
timeDrone = 0
oldTime = 0

moveForwardX(1)
drone.stop()
drone.hover()
time.sleep(.1)
drone.land()
#drone.hover()
