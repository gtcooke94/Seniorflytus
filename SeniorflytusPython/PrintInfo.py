##### Suggested clean drone startup sequence #####
import time, sys
import ps_drone # Import PS-Drone-API

drone = ps_drone.Drone() # Start using drone	
drone.startup() # Connects to drone and starts subprocesses

drone.reset() # Sets drone's status to good
while (drone.getBattery()[0]==-1): time.sleep(0.1) # Wait until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"% "+str(drone.getBattery()[1]) # Battery-status
if drone.getBattery()[1]=="empty": sys.exit() # Give it up if battery is empty

drone.useDemoMode(True) # Set 15 basic dataset/sec (default anyway)
drone.getNDpackage(["demo"]) # Packets, which shall be decoded
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
		while not stop and counter<=5:
		ndc = self.__NavDataCount						# wait for the next NavData-package
		while ndc == self.__NavDataCount:		time.sleep(0.001)
		kalib = (time.time()-reftime)*self.selfRotation	# trys to recalibrate, causing moving sensor-values around 0.0185 deg/sec
		cpos = self.__NavData["demo"][2][2]				# get the current angle
		if minaxis > cpos:			minaxis = cpos		# set the minimal seen angle
		if maxaxis < cpos:			maxaxis = cpos		# set the maximal seen angle
		if cpos-minaxis >= 180:		cpos = cpos-360		# correct the angle-value if necessary...
		elif maxaxis-cpos >= 180:	cpos = cpos+360		# ...for an easier calculation
		speed = abs(cpos-npos+kalib) / 10.0				# the closer to the destination the slower the drone turns

    

drone.stop()
time.sleep(2)
drone.land()
