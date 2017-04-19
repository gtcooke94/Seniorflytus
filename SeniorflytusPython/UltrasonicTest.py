import time, sys
import ps_drone # Import PS-Drone-API
import sys

# Ultrasonic Code Below
#########################################################################
##                           Include Modules                           ##
#########################################################################
from smbus import SMBus	                  # Allows Python on Linux devices to access I2C/dev interface
from time import sleep                    # Allows us to put delays in our code
#########################################################################


#########################################################################
##                     Global Variable Definitions                     ##
#########################################################################
# The Raspberry Pi uses 7 bit addresses and a read/write bit.
address_array = [0x70, 0x65]                    # The hex I2C addresses in the order they are to be read
											#  Enter addresses in hex separated by commas in the square brackets, []

# The following three variables only need to be adjusted if you are changing the address of your sensor.
# Addresses up to 127 are valid, however, 'sudo i2cdetect -y 1' only displays addresses through 119.
run_address_change = 0                    # Set to 1 to change an address or 0 when no addresses are  being changed
old_address = 0x70                        # The current address of a sensor (used in changing the address)
new_address = 0x70                        # The desired new address of a sensor (used in changing the address)
#########################################################################


#########################################################################
##                   Function: Take a Range Reading                    ##
#########################################################################
def take_range(address):				  
	SMBus(1).write_byte(address, 0x51)      # Write the sensors address and the range command, 0x51
	#sleep(0.1)                              # Allow the sensor to process the readings with a ~100mS delay
#########################################################################


#########################################################################
##                  Function: Report a Range Reading                   ##
#########################################################################
def report_range(address):
	latest_range = SMBus(1).read_word_data(address, 0xFF)
	# Commanding a read at the sensor address sends the latest range
	#  data as a word
	# A command (set to 0xFF here) is required by syntax not the part
	#print "Sensor", i, ":", ((latest_range & 0xFF) << 8) + (latest_range >> 8), 'cm'
	# The Raspberry Pi expects the high and low bytes in the opposite order
	#  The and operations and bit shifts essentially swap the high and low bytes
	#  Finally, we add the two range bytes together and print
	return ((latest_range & 0xFF) << 8) + (latest_range >> 8)
#########################################################################


#########################################################################
##                 Function: Change the sensor address                 ##
#########################################################################
def change_address(old_address, new_address):
	if (new_address != 0) and (new_address != 40) and (new_address != 82) and (new_address != 85):
	# Verify we are not using a restricted address
		try:
			SMBus(1).write_i2c_block_data(old_address, 0xAA, [0xA5, new_address << 1])
			# Write the current address, the address unlock 1 command, 0xAA,
			#  the address unlock 2 command, 0xA5, and the new address
			print "Address successfully changed to", new_address
		except IOError:
			print "Please verify the circuit. Also verify the current sensor address by running 'sudo i2cdetect -y 1'."
	else:
		print "The sensor address cannot be 0, 40, 82, or 85."  
#########################################################################
#
# Ultrasonic Main Loop Function
def UltrasonicTakeRange():
	i = 0
	if run_address_change:
		change_address(old_address, new_address)
	try:                                 
		# Used to cycle through address_array and read each sensor
		number_sensors = len(address_array)     # The array length is used to loop through the addresses
		while i < number_sensors:
			address = address_array[i]
			take_range(address)
			i = i + 1                             # Cycle through the array of addresses 
	except IOError:
		print "Please verify the circuit. Also verify the current sensor address by running 'sudo i2cdetect -y 1'."

def UltrasonicReportRange():
	i = 0
	values = [0,0]
	try:                                 
		# Used to cycle through address_array and read each sensor
		number_sensors = len(address_array)     # The array length is used to loop through the addresses
		while i < number_sensors:
			address = address_array[i]
			reading = report_range(address)
			values[i] = reading 
		i = i + 1
		                             # Cycle through the array of addresses 
	except IOError:
		print "Please verify the circuit. Also verify the current sensor address by running 'sudo i2cdetect -y 1'."
	return values


#fileName = raw_input("Log File Name: " )
#fileName = fileName + ".txt"
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
drone.setSpeed(.1)

drone.trim()
time.sleep(1)
#drone.trim() # Recalibrate sensors
#drone.getSelfRotation(5) # Get auto-alteration of gyroscope-sensor
#print "Auto-alt.:"+str(drone.selfRotation)+"dec/s" # Showing value for auto-alteration

drone.takeoff() # Fly, drone, fly !
while drone.NavData["demo"][0][2]: time.sleep(0.1) # Wait until drone is completely flying


drone.hover()
time.sleep(.1)
##### Mainprogram begin #####
print "Drone is flying now"
xpos = 0
ypos = 0
firstFlag = False
originalTime = 0
timeDrone = 0
lastSensorReadTime = 0
# Flag to read ultrasonic sensor
flagToRead = True
# Flag to get the data from the ultrasonic sensor (with .1 second delay from the previous flag)
flagToGet = False
ultrasonicValues = [0, 0]
ndc = drone.NavDataCount
#while ((timeDrone - originalTime) < 30):
while (True):

	# wait for the next NavData-package
	while ndc == drone.NavDataCount:
		time.sleep(0.00001)

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
	sensorTimeNow = lastSensorReadTime
	if (not firstFlag):
		firstFlag = True
		oldTime = timeDrone
		lastSensorReadTime = timeDrone
		originalTime = timeDrone
	#getPosition(vx, vy, vz, oldTime, timeDrone)
	oldTime = timeDrone

	#Get Ultrasonic Data
	if (flagToRead):
		# Read ultrasonic sensor
		UltrasonicTakeRange()
		flagToGet = True
		flagToRead = False
		lastSensorReadTime = timeDrone
		print "Sensor -> Bus"
	elif (flagToGet and ((timeDrone - lastSensorReadTime) > .1)):
		ultrasonicValues = UltrasonicReportRange()
		flagToRead = True
		flagToGet = False
		print "Read Sensor"
		print ultrasonicValues
	#print vx, vy, vz
	#print xpos, ypos, angle, timeDrone

	#xdata.append(xpos)
	#ydata.append(ypos)

	drone.hover()