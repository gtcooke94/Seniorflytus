##### Suggested clean drone startup sequence #####
import time, sys
import ps_drone # Import PS-Drone-API

drone = ps_drone.Drone() # Start using drone	
drone.startup() # Connects to drone and starts subprocesses

drone.reset() # Sets drone's status to good
while (drone.getBattery()[0]==-1): time.sleep(0.1) # Wait until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"% "+str(drone.getBattery()[1]) # Battery-status
drone.useDemoMode(True) # Set 15 basic dataset/sec

##### Mainprogram begin #####
drone.setConfigAllID() # Go to multiconfiguration-mode
drone.sdVideo() # Choose lower resolution (try hdVideo())
drone.frontCam() # Choose front view
CDC = drone.ConfigDataCount
while CDC==drone.ConfigDataCount: 
	time.sleep(0.001) # Wait until it is done (after resync)
drone.startVideo() # Start video-function
drone.showVideo() # Display the video



##### And action !
print "Use to toggle front- and groundcamera, any other key to stop"
IMC = drone.VideoImageCount	# Number of encoded videoframes
stop = False
ground = False
while not stop:
	while drone.VideoImageCount==IMC: 
		time.sleep(0.01)	# Wait until the next video-frame
	IMC = drone.VideoImageCount
	key = drone.getKey()
	if key==" ": 
		if ground: ground = False
		else: ground = True
		drone.groundVideo(ground) # Toggle between front- and groundcamera.
	elif key and key != " ": stop =	True