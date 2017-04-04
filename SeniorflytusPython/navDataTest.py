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

drone.trim() # Recalibrate sensors
drone.getSelfRotation(5) # Get auto-alteration of gyroscope-sensor
print "Auto-alt.:"+str(drone.selfRotation)+"dec/s" # Showing value for auto-alteration

drone.takeoff() # Fly, drone, fly !
while drone.NavData["demo"][0][2]: time.sleep(0.1) # Wait until drone is completely flying

##### Mainprogram begin #####
print "Drone is flying now"


stop = False
while (not stop):
    if (drone.getKey() == 'c'): stop = True
    #drone.turnAngle(0)
    #print drone.getNDpackage(["demo"])
    #opos = 	drone.NavData()
    #opos = opos["demo"][2][2]
    #print opos    
    drone.turnAngle(90, 1)  
    drone.hover()  
    time.sleep(1)
    

drone.stop()
time.sleep(2)
drone.land()
