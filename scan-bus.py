from lx16a import *

# This code scans every bus address and returns the addresses where servos respond.
# Also, if it gets a checksum error when scanning an address, it prints a message warning that
# you might have two servos with the same address.

# This is the port that the controller board is connected to
# This will be different for different computers
# On Windows, try the ports COM1, COM2, COM3, etc...
# On Raspbian, try each port in /dev/
LX16A.initialize("/dev/ttyUSB0")


print("Testing servo: ")
for a in range(0,254):
	print(a, end='')
	try:
		servo = LX16A(a)
	except ServoError as err:
		print("Checksum error at address:: ", a)
		print(" Possibly two servos at this address")
	except ServoTimeout:
		print(",", end="", flush=True)
	else:
		print("")
		print("Servo found at address: ", a)
		del servo
print("")
