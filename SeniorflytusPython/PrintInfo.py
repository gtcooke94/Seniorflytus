##### Suggested clean drone startup sequence #####
import time, sys
import ps_drone # Import PS-Drone-API

fileName = raw_input("Log File Name: " )
fileName = fileName + ".txt"
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


# From turnAngle()
navData = drone.NavData
#opos = navData["demo"][2][2]            # get the source/current (original) angle                                 # ...be correctly handled
speed = drone.speed
ospeed = speed                                   # stores the given speed-value
reftime = time.time()
accurateness = 0

#f1 = open(fileName, 'w')  

# End from turnAngle   
#drone.getSelfRotation()
while (not stop):
    if (drone.getKey() == 'c'): stop = True
    drone.hover()
    ndc = drone.NavDataCount                      # wait for the next NavData-package
    while ndc == drone.NavDataCount:
        time.sleep(0.0001)

    kalib = (time.time()-reftime)*drone.selfRotation # trys to recalibrate, causing moving sensor-values around 0.0185 deg/sec
    navData = drone.NavData
    cpos = navData["demo"][2][2]             # get the current angle
    vx = navData["demo"][4][0]
    vy = navData["demo"][4][1]
    vz = navData["demo"][4][2]
    mx = navData["magneto"][0][0]
    my = navData["magneto"][0][1]
    mz = navData["magneto"][0][2]
    times = navData["time"][0]
    #print "cpos = " + str(cpos)
    #print >> f1, "vx, vy, vz = " + str(vx) + ", " + str(vy) + ", " + str(vz)
    #print >> f1, "mx, my, mz = " + str(mx) + ", " + str(my) + ", " + str(mz) + "\n"
    #print "mx, my, mz = " + str(mx) + ", " + str(my) + ", " + str(mz) + "\n"
    #print "kalib = " + str(kalib)
    #print >> f1, str(mx) + ", " + str(my) + ", " + str(mz) + ", " + str(times)
    print str(cpos)

drone.stop()
time.sleep(2)
drone.land()
