import time
import Ultrasonic
import ps_drone

state = "Off"

def run(stop_event):#drone):
	global state
	global xpos
	global ypos
	global oldTime
	global timeDrone
	global firstFlag
	global angleWanted
	global changeAngleFlag
	drone = ps_drone.Drone() # Start using drone	
	s 
	#print("Starting Up...")
	try:
		drone.startup() # Connects to drone and starts subprocesses
		print("Started Up.")

		drone.reset()
		drone.trim()

		drone.useDemoMode(False) # Set 15 basic dataset/sec (default anyway)
		drone.addNDpackage(["demo"]) # Packets, which shall be decoded
		drone.addNDpackage(["magneto"])
		drone.addNDpackage(["time"])
		drone.getNDpackage(["all"])
		time.sleep(0.5) # Give it some time to awake fully
		drone.setSpeed(.1)

		drone.takeoff()
		while drone.NavData["demo"][0][2]: time.sleep(0.1)
		#time.sleep(7)
		drone.hover()
		time.sleep(.5)

		key = drone.getKey()
		counter = 0
		veering = 0 #-1 is left, 1 is right
		returnedToCenter = False
	
		while not stop_event.is_set():
			forwardbackward = -0.10 #pos is forward
			leftright = 0 #pos is left
			rotateadj = 0
			# keep in center of hall


			######## Getting NavData. This may need to be moved to a function. Currently we also do not care about missing packets
			if ndc > drone.NavDataCount:
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
				    angleWanted = angle
				getPosition(vx, vy, vz, oldTime, timeDrone)
				oldTime = timeDrone
				if changeAngleFlag:
					angleWanted = angle
					changeAngleFlag = False




			state = "Normal"
			print "Front sensor is: " + str(Ultrasonic.front_sensor)
			if (Ultrasonic.front_sensor < 200 and Ultrasonic.front_sensor > 20):
				counter = counter + 1
				# print counter
				forwardbackward = 0
				state = "Paused - Collision Detected"
				#drone.land()
				#break
				#drone.move(0, 0.1, 0, 0) #go forward
			elif counter > 0:
				print counter
				counter = counter - 1

			if (Ultrasonic.left_sensor - Ultrasonic.right_sensor) > 50:
				#drone.move(0.1, 0, 0, 0) #go left
				leftright = 0.1
				if returnedToCenter and veering == 1:
					#rotateadj = 0.05
					returnedToCenter = False
					#print "rotational adjust - left"
				else:
					veering = 1
				state = "Shifting to the Left"
				#print "going left..."
			elif (Ultrasonic.right_sensor - Ultrasonic.left_sensor) > 50:
				#drone.move(-0.1, 0, 0, 0) #go right
				leftright = -0.1
				if returnedToCenter and veering == -1:
					#rotateadj = -0.05
					returnedToCenter = False
					#print "rotational adjust - right"
				else:
					veering = -1
				state = "Shifting to the Right"
				#print "going right..."
			else:
				#drone.hover()
				returnedToCenter = True
				state = "Holding"
				#print "holding..."


			## Using the Yaw to change the rotation
			if ((angle - angleWanted) > 5):
				# Turn one way
				rotateadj = -.05
			elif ((angle - angleWanted) < -5):
				# Turn the other way
				rotateadj = 0.05
			else:
				rotateadj = 0
			drone.move(leftright, forwardbackward, 0, rotateadj) #rotateadj)

			if (counter > 25):
				state = "Turning"
				drone.turnAngle(-90, 0.8, 1)
				changeAngleFlag = True
				counter = 0

				i = 0
				while (i < 3):
					if Ultrasonic.right_sensor < 50:
						leftright = 0.1
						state = "Forward after Turn - Shift Left"
						#print "turning - shift left"
					else:
						leftright = 0
						state = "Forward after Turn"
					drone.move(leftright, -0.1, 0, 0)
					time.sleep(0.1)
					i = i + 0.1
				#break

			print state
			# 150 cm from left wall
			# if Ultrasonic.left_sensor > 150:
			# 	drone.move(0.1, 0, 0, 0) #go left
			# 	print "going left..."
			# elif Ultrasonic.left_sensor < 110 and Ultrasonic.left_sensor > 20:
			# 	drone.move(-0.1, 0, 0, 0) #go right
			# 	print "going right..."
			# else:
			# 	drone.hover()
			# 	print "holding..."
			# time.sleep(0.1)

			#pass
	except KeyboardInterrupt:
		print "Attempting to Land Drone2..."
		drone.land()

	if (stop_event.is_set()):
		print "Attempting to Land Drone3..."
		drone.land()


def getPosition(vx, vy, vz, ts, te):
    global xpos
    global ypos
    xpos = xpos + (vx * (te - ts))/1000
    ypos  = ypos + (vy * (te - ts))/1000
