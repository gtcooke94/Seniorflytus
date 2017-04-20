import Queue
import thread
import time

# from UltrasonicScript import *

# def getUltrasonic():
# 	if run_address_change:
# 	  change_address(old_address, new_address)
# 	try:
# 	  i = 0                                   # Used to cycle through address_array and read each sensor
# 	  number_sensors = len(address_array)     # The array length is used to loop through the addresses
# 	  while i < number_sensors:
# 	    address = address_array[i]
# 	    take_range(address)
# 	    report_range(address)
# 	    i = i + 1                             # Cycle through the array of addresses
# 	    i = i % number_sensors                # The modulo, %, operator lets i loop back to zero for an infinite loop
# 	except IOError:
# 	  print "Please verify the circuit. Also verify the current sensor address by running 'sudo i2cdetect -y 1'."

num1 = 0
num2 = 0

def test1():
	global num1
	while True:
		#print "test1"
		num1 = num1 + 1
		time.sleep(1)

def test2():
	global num2
	while True:
		#print "test2"
		num2 = num2 + 2
		time.sleep(2)

def test3():
	while True:
		#print "test2"
		print num1, num2
		time.sleep(1)

#Test Threading
try:
	thread.start_new_thread(test1, ())
	thread.start_new_thread(test2, ())
	thread.start_new_thread(test3, ())
except:
   print "Thread Error"

while 1:
   pass