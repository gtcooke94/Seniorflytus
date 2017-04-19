####### Definitions #############################
def turnToHeading(current_heading, new_heading):
	#theres probably a better way to do this, but I'm tired so heres the basic way to do it
	#90 degress to fix jump from 6 to 0 and 0 to 6
	if (current_heading == new_heading):
		return
	elif (abs(current_heading - new_heading) == 6):
		if (current_heading > new_heading):
			turn90Left()
		else:
			turn90Right()
	#180 degrees
	elif (abs(current_heading - new_heading) == 4):
		turn90Left()
		drone.hover()
		time.sleep(3)
		turn90Left()
	#90 degrees
	elif (abs(current_heading - new_heading) == 2):
		if (current_heading > new_heading):
			turn90Right()
		else:
			turn90Left()
	drone.hover()
	time.sleep(3)

def turn90Left():
	print("Turning Left...")
	drone.turnAngle(-90, 0.8)

def turn90Right():
	print("Turning Right...")
	drone.turnAngle(90, 0.8)

def moveForward(cells=1):
	print("Moving Forward...")
	drone.moveForward(0.1)
	time.sleep(1.75)



# drone.moveForward(0.3)
# time.sleep(2)

# drone.hover()
# time.sleep(3)

# drone.moveForward(0.3)
# time.sleep(2)

# drone.hover()
# time.sleep(3)

###### Execution ############################

import ps_drone #3 as ps_drone
import time
from planning import *

#start = (49,24)
#goal = (51,24)

start = (1,1)
goal = (51,47)

headings = setup(start, goal) #sets up grid

#starting heading
current_heading = 6;
drone = ps_drone.Drone()
drone.startup()

drone.takeoff()
time.sleep(8)

for heading in headings:
	print("Heading: " + str(heading))
	#drone.takeoff()
	#time.sleep(3)

	print("About to Turn...")
	turnToHeading(current_heading, heading)
	print("About to Move...")
	moveForward()
	# drone.moveForward(0.3)
	# time.sleep(2)

	print("About to Hover...")
	drone.hover()
	time.sleep(2)
	print("About to Land...")
	#drone.land()
	#time.sleep(8)

drone.land()