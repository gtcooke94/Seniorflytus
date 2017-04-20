import Queue
import thread, threading
import time

#from UltrasonicScript import getUltrasonic
import UltrasonicScript

import ps_drone # Import PS-Drone-API

# left_sensor = -1
# right_sensor = -1
# front_sensor = -1

# num1 = 0
# num2 = 0

# def test1():
# 	global num1
# 	while True:
# 		#print "test1"
# 		num1 = num1 + 1
# 		time.sleep(1)

# def test2():
# 	global num2
# 	while True:
# 		#print "test2"
# 		num2 = num2 + 2
# 		time.sleep(2)

def printVals():
	while True:
		#global left_sensor
		#print "test2"UltrasonicScript.left_sensor
		print "Test access: ", UltrasonicScript.left_sensor
		time.sleep(2)

drone = ps_drone.Drone() # Start using drone	
print("Starting Up...")
drone.startup() # Connects to drone and starts subprocesses
print("Started Up.")
drone.reset()
drone.trim() #on level ground

drone.takeoff()
time.sleep(7)
# drone.mtrim() #rotational calibration
drone.moveUp(0.5)
time.sleep(2)
drone.hover()
time.sleep(1)

# drone.move(0.3, 0, 0, 0)
# time.sleep(2)
# drone.hover()
#		leftright, backwardforward, downup, turnleftright
#      pos = left

#Test Threading
try:
	thread.start_new_thread(UltrasonicScript.getUltrasonic, ())
	thread.start_new_thread(printVals, ())
	#thread.start_new_thread(test2, ())
except:
   print "Thread Error"

key = drone.getKey()
counter = 0
while key != "w":
	forwardbackward = -0.10 #pos is forward
	leftright = 0 #pos is left
	# keep in center of hall
	if (UltrasonicScript.front_sensor < 200 and UltrasonicScript.front_sensor > 20):
		counter = counter + 1
		print counter
		forwardbackward = 0
		#drone.land()
		#break
		#drone.move(0, 0.1, 0, 0) #go forward
	elif counter > 0:
		print counter
		counter = counter - 1

	if (UltrasonicScript.left_sensor - UltrasonicScript.right_sensor) > 30:
		#drone.move(0.1, 0, 0, 0) #go left
		leftright = 0.1
		print "going left..."
	elif (UltrasonicScript.right_sensor - UltrasonicScript.left_sensor) > 30:
		#drone.move(-0.1, 0, 0, 0) #go right
		leftright = -0.1
		print "going right..."
	else:
		#drone.hover()
		print "holding..."

	drone.move(leftright, forwardbackward, 0, 0)

	if (counter > 25):
		drone.land()
		break

	# 150 cm from left wall
	# if UltrasonicScript.left_sensor > 150:
	# 	drone.move(0.1, 0, 0, 0) #go left
	# 	print "going left..."
	# elif UltrasonicScript.left_sensor < 110 and UltrasonicScript.left_sensor > 20:
	# 	drone.move(-0.1, 0, 0, 0) #go right
	# 	print "going right..."
	# else:
	# 	drone.hover()
	# 	print "holding..."
	# time.sleep(0.1)

	key = drone.getKey()
	#pass

print "Key w Pressed, Landing..."

drone.land()