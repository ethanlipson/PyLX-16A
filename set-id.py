from lx16a import *
from time import sleep

# Simple app to change the ID of a servo.  

# This is the port that the controller board is connected to
# This will be different for different computers
# On Windows, try the ports COM1, COM2, COM3, etc...
# On Raspbian, try each port in /dev/
LX16A.initialize("/dev/ttyUSB0")

curr_id = 1
new_id  = 101

servo1 = LX16A(curr_id)

servo1.IDWrite(new_id)

sleep(.2)
servo2 = LX16A(new_id)
servo2.moveTimeWrite(120)
