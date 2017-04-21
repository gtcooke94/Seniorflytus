import time
import Ultrasonic
import ps_drone

state = "Off"

def run(stop_event):#drone):
	global state
	drone = ps_drone.Drone() # Start using drone	
	#print("Starting Up...")
	try:
		drone.startup() # Connects to drone and starts subprocesses
		print("Started Up.")

		drone.reset()
		drone.trim()

		drone.takeoff()
		time.sleep(7)

		key = drone.getKey()
		counter = 0
		veering = 0 #-1 is left, 1 is right
		returnedToCenter = False
	
		while not stop_event.is_set():
			forwardbackward = -0.10 #pos is forward
			leftright = 0 #pos is left
			rotateadj = 0
			# keep in center of hall
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
					rotateadj = 0.05
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
					rotateadj = -0.05
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

			drone.move(leftright, forwardbackward, 0, 0) #rotateadj)

			if (counter > 25):
				state = "Turning"
				drone.turnAngle(-90, 0.8, 1)
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

