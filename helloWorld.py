from lx16a import *
from math import sin, cos

# This is the port that the controller board is connected to
# This will be different for different computers
LX16A.initialize('/dev/ttyUSB0')

# There should two servos connected, with IDs 1 and 2
servo1 = LX16A(1)
servo2 = LX16A(2)

t = 0

while True:
	# Two sine waves out of phase
	servo1.moveTimeWrite(sin(t))
	servo2.moveTimeWrite(cos(t))
	
	t += 0.01
