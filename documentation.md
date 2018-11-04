# PyLX-16A Documentation

## Reference Guide

### Initialization Functions
* LX16A.initialize(port)
* LX16A.\_\_init\_\_(ID)

### Utility Functions
* LX16A.checksum(nums)
* LX16A.toBytes(n)
* LX16A.sendPacket(packet)
* LX16A.checkPacket(packet)
* LX16A.getServos()

### Write Commands
* LX16A.moveTimeWrite(angle, time=0)
* LX16A.moveTimeWaitWrite(angle, time=0)
* LX16A.moveTimeWriteRel(relAngle, time=0)
* LX16A.moveTimeWaitWriteRel(relAngle, time=0)
* LX16A.moveStart()
* LX16A.moveStop()
* LX16A.IDWrite(ID)
* LX16A.angleOffsetAdjust(offset)
* LX16A.angleOffsetWrite()
* LX16A.angleLimitWrite(lower, upper)
* LX16A.vInLimitWrite(lower, upper)
* LX16A.tempMaxLimitWrite(temp)
* LX16A.servoMode()
* LX16A.motorMode(speed)
* LX16A.loadOrUnloadWrite(power)
* LX16A.LEDCtrlWrite(power)
* LX16A.LEDErrorWrite(temp, volt, lock)

### Read Commands
* LX16A.moveTimeRead()
* LX16A.moveTimeWaitRead()
* LX16A.IDRead()
* LX16A.angleOffsetRead()
* LX16A.angleLimitRead()
* LX16A.vInLimitRead()
* LX16A.tempMaxLimitRead()
* LX16A.tempRead()
* LX16A.vInRead()
* LX16A.posRead()
* LX16A.servoMotorModeRead()
* LX16A.loadOrUnloadRead()
* LX16A.LEDCtrlRead()
* LX16A.LEDErrorRead()


### Global Commands
* LX16A.moveStartAll()
* LX16A.moveStopAll()
* LX16A.moveTimeWriteList(servos, data)
* LX16A.moveTimeWriteListRel(servos, data)

## Documentation

### LX16A.initialize(port)
Initiates the connection between the computer and the servo controller board. No other commands will work if this function is not called.

| Parameter | Type   |
| --------- | ------ |
| port      | `str`  |

#### Example Programs
Windows
```python
from lx16a import *

# To find the port on Windows, try COM1, COM2, COM3, COM4, etc.

# This program initializes the controller board on the port COM3
LX16A.initialize("COM3")
```

Linux
```python
from lx16a import *

# To find the port on Windows, go to the directory /dev/ in the terminal,
# and type `ls`. This will list all available ports, so try all of them

# This program initializes the controller board on the port /dev/ttyUSB0
LX16A.initialize("/dev/ttyUSB0")
```

#### Return Value
None

#### Possible Errors
If the port does not exist, a `SerialException` will be raised.

### LX16A.\_\_init\_\_(ID)
Each physical servo has an ID number associated with it, between 0 and 253. Virtual servos also have an ID associated with them, and when a command is called in the code, this command affects the physical servo with the same ID. A servo's physical ID can be set programmatically or through LewanSoul's Bus Servo Terminal software.

| Parameter | Type   | Lower Bound | Upper Bound |
| --------- | ------ | ----------- | ----------- |
| ID        | `int`  | 0           | 253         |

#### Example Program
```python
from lx16a import *

LX16A.initialize("COM3")

# Creates two virtual servo objects, with IDs 1 and 5
servo1 = LX16A(1)
servo2 = LX16A(5)
```

#### Return Value
`LX16A` object

#### Possible Errors
If the `ID` parameter is out of range, a `ServoError` will be raised.

### LX16A.checksum(nums)
A checksum is included at the end of each command packet to ensure that the data is not corrupt. The formula is as follows: Sum up every number in the list, flip the bits, and take the least significant byte.

| Parameter | Type           |
| --------- | -------------- |
| nums      | list of `int`s |

#### Example Program
```python
from lx16a import *

data = [8, 26, 0xB4, 1337, 54345]
checksum = LX16A.checksum(data)

print(checksum)
```

#### Return Value
An `int` between 0 and 255 (inclusive)

#### Possible Errors
If any of the elements of `nums` is not an `int`, a `TypeError` will be raised.

### LX16A.toBytes(n)
Converts an `int` between 0 and 65535 (inclusive) to a list of two numbers between 0 and 255 (inclusive), each representing a byte. The first element of the list is the MSB, and the second element is the LSB.

| Parameter | Type | Upper Bound | Lower Bound |
