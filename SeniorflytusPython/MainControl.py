import Queue
import thread, threading
import time

#from Ultrasonic import getUltrasonic
import Ultrasonic
import DroneGUI
import FlightControl
import BluetoothControl
import VideoProcessing

import ps_drone # Import PS-Drone-API


SENSOR_MAX = 756

abort = False

# drone.move(leftright, backwardforward, downup, turnleftright)
#      pos = left

#Thread Generation
# try:
# 	thread.start_new_thread(DroneGUI.runGUI, ())
# 	thread.start_new_thread(Ultrasonic.getUltrasonic, ())
# 	thread.start_new_thread(FlightControl.run, ())
# 	#thread.start_new_thread(printVals, ())
# except:
#    print "Thread Error Occurred"

stop_event = threading.Event()

t1 = threading.Thread(target=DroneGUI.runGUI)
t1.daemon = True
t1.start()

t2 = threading.Thread(target=Ultrasonic.getUltrasonic)
t2.daemon = True
t2.start()

t3 = threading.Thread(target=FlightControl.run, args=(stop_event,))
t3.daemon = False #keep flight control alive so that it can force drone to land
t3.start()

#t4 = threading.Thread(target=BluetoothControl.readDistance)
#t4.daemon = True
#t4.start()

#t5 = threading.Thread(target=VideoProcessing.processImage)
#t5.daemon = True
#t5.start()

#Keep Main Thread Alive
try:
	while 1:
		pass
except KeyboardInterrupt:
	stop_event.set()