from lx16a import *
from math import sin, cos
import time

# This is the port that the controller board is connected to
# This will be different for different computers
# On Windows, try the ports COM1, COM2, COM3, etc...
# On Raspbian, try each port in /dev/
LX16A.initialize("/dev/ttyUSB0")

# There should two servos connected, with IDs 1 and 2
# If one isn't connected, an exception is thrown
try:
	servo1 = LX16A(1)
	servo2 = LX16A(2)
except ServoTimeout as e:
	print(f"Servo {e.ID} is not responding. Exiting...")
	exit()

t = 0

while True:
	# Two sine waves out of phase
	# The servos can rotate between 0 and 240 degrees,
	# So we adjust the waves to be in that range
	servo1.moveTimeWrite(sin(t) * 120 + 120)
	servo2.moveTimeWrite(cos(t) * 120 + 120)
	time.sleep(0.05)

	t += 0.05
