##                   Raspberry Pi I2C for a MaxSonar                   ##
#########################################################################
##  Original Author: Cody Carlson, 11-08-2016, Revision: 1.0           ##
##  Modifications by:                                                  ##
##                                                                     ##
##  Revision History: 1.0 -- 11-08-2016 -- Created initial code build  ##
##                                                                     ##
##                                                                     ##
##  Special Thanks to MaxBotix Inc. for sponsoring this project!       ##
##    http://www.maxbotix.com -- High Performance Ultrasonic Sensors   ##
##                                                                     ##
##  For more information on using I2C devices on a Raspberry Pi visit  ##
##    https://www.raspberrypi.org/forums/                              ##
#########################################################################

#########################################################################
##                          Notes on this Code                         ##
#########################################################################
# MaxBotix sensors require clock stretching at speeds above 50kHz. Raspberry Pi drivers do not do proper clock stretching, so
#  a maximum clock speed of 50kHz is recommended at this time.
# You will need to enable I2C communication to run code successfully.
# The Raspberry Pi uses a seven bit address followed by a read/write bit. Do not confuse this with 8 bit addresses.
# Please review the full tutorial at www.maxbotix.com/moreURL for a step by step guide.
#########################################################################


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
address_array = [0x70]                    # The hex I2C addresses in the order they are to be read
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
  sleep(0.1)                              # Allow the sensor to process the readings with a ~100mS delay
#########################################################################


#########################################################################
##                  Function: Report a Range Reading                   ##
#########################################################################
def report_range(address):
  latest_range = SMBus(1).read_word_data(address, 0xFF)
                                          # Commanding a read at the sensor address sends the latest range
                                          #  data as a word
                                          # A command (set to 0xFF here) is required by syntax not the part
  print "Sensor", i, ":", ((latest_range & 0xFF) << 8) + (latest_range >> 8), 'cm'
                                          # The Raspberry Pi expects the high and low bytes in the opposite order
                                          #  The and operations and bit shifts essentially swap the high and low bytes
                                          #  Finally, we add the two range bytes together and print
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




#########################################################################
##                              MAIN LOOP                              ##
#########################################################################
# This is a working sample code for changing sensor addresses and reading range data.
# Feel free to add any additional code needed for your application here.
if run_address_change:
  change_address(old_address, new_address)
try:
  i = 0                                   # Used to cycle through address_array and read each sensor
  number_sensors = len(address_array)     # The array length is used to loop through the addresses
  while i < number_sensors:
    address = address_array[i]
    take_range(address)
    report_range(address)
    i = i + 1                             # Cycle through the array of addresses
    i = i % number_sensors                # The modulo, %, operator lets i loop back to zero for an infinite loop
except IOError:
  print "Please verify the circuit. Also verify the current sensor address by running 'sudo i2cdetect -y 1'."