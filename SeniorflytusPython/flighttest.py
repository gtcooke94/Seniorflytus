import ps_drone #3 as ps_drone
import time
from planning import *

drone = ps_drone.Drone()
drone.startup()

drone.takeoff()
time.sleep(8)

print("Turning Left...")
drone.turnAngle(-90, 0.4, 1)

time.sleep(2)

print("Landing...")
drone.land()