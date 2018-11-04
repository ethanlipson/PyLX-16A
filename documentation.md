# PyLX-16A Documentation

This is the documentation for the Python library PyLX16A, a library for controlling LewanSoul's LX-16A servos. To get started with using them, read `userGuide.md`. This document specifies all of the functionality of the library, so I would recommend reading the User Guide first.

NOTE: In this document, I make a distinction between the physical servo and the virtual servo object. In any program using PyLX16A, there should be a one-to-one correspondence between virtual servo objects and physical servos.

## Reference Guide

### Initialization Functions
* [LX16A.initialize(port)](#lx16ainitializeport)
* [LX16A.\_\_init\_\_(ID)](#lx16a__init__id)

### Utility Functions
* LX16A.checksum(nums)
* LX16A.toBytes(n)
* LX16A.sendPacket(packet)
* LX16A.checkPacket(packet)

### Write Commands
* [LX16A.moveTimeWrite(angle, time=0)](#lx16amovetimewriteangle-time0)
* [LX16A.moveTimeWaitWrite(angle, time=0)](#lx16amovetimewaitwriteangle-time0)
* [LX16A.moveTimeWriteRel(relAngle, time=0)](#lx16amovetimewriterelrelangle-time0)
* [LX16A.moveTimeWaitWriteRel(relAngle, time=0)](#lx16amovetimewaitwriterelrelangle-time0)
* [LX16A.moveStart()](#lx16amovestart)
* [LX16A.moveStop()](#lx16amovestop)
* [LX16A.IDWrite(ID)](#lx16aidwriteid)
* [LX16A.angleOffsetAdjust(offset)](#lx16aangleoffsetadjustoffset)
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
* LX16A.getServos()

## Documentation

### LX16A.initialize(port)
Initiates the connection between the computer and the servo controller board. No other commands will work if this function is not called.

#### Parameters
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

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| ID        | `int` | 0           | 253         |

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

### LX16A.moveTimeWrite(angle, time=0)
Rotates the servo to the specified angle (in degrees) over the given time (in milliseconds). If the time argument is 0, the servo will rotate as fast as it can, but it will not be instant. If no time argument is given, it will be assumed to be 0.

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| angle     | `int` | 0           | 240         |
| time      | `int` | 0           | 30000       |

#### Example Program
```python
from lx16a import *

LX16A.initialize("COM3")

servo1 = LX16A(1)
servo2 = LX16A(2)

# Rotates servo1 to its halfway position
servo1.moveTimeWrite(120)

# Rotates servo2 to 200 degrees over 3 seconds
servo2.moveTimeWrite(200, 3000)
```

#### Return Value
None

#### Possible Errors
If `angle` or `time` are out of range, a `ServoError` will be raised.

### LX16A.moveTimeWaitWrite(angle, time=0)
Similar to LX16A.moveTimeWrite, except that the servo does not rotate immediately. Instead, it rotates by the angle and time when `LX16A.moveStart` or `LX16A.moveStartAll` is called.

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| angle     | `int` | 0           | 240         |
| time      | `int` | 0           | 30000       |

#### Example Program
```python
from lx16a import *
import time

LX16A.initialize("COM3")

servo1 = LX16A(1)

# Stores angle=180 and time=2000 in servo1
servo1.moveTimeWaitWrite(180, 2000)

# Sleep for one second
time.sleep(1)

# Starts rotation of the servo
servo1.moveStart()
```

#### Return Value
None

#### Possible Errors
If `angle` or `time` are out of range, a `ServoError` will be raised.

### LX16A.moveTimeWriteRel(relAngle, time=0)
Rotates the servo relative to its current angle (in degrees) over the specified time (in seconds). If the time argument is 0, the servo will rotate as fast as it can, but it will not be instant. If no time argument is given, it will be assumed to be 0.

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| relAngle  | `int` | 0           | 240         |
| time      | `int` | 0           | 30000       |

#### Example Program
```python
from lx16a import *
import time

LX16A.initialize("COM3")

servo1 = LX16A(1)

# Rotate the servo to 120 degrees
servo1.moveTimeWrite(120)

# Wait for the servo to finish rotating
time.sleep(1)

# Rotate by 30 degrees to an absolute angle of 150 degrees
servo1.moveTimeWriteRel(30)
```

#### Return Value
None

#### Possible Errors
If the servo's current angle plus `relAngle` is out of range, or if `time` is out range, a `ServoError` will be raised.

### LX16A.moveTimeWaitWriteRel(relAngle, time=0)
Similar to LX16A.moveTimeWriteRel, except that the servo does not rotate immediately. Instead, it rotates by the angle (relative to its current angle) and time when `LX16A.moveStart` or `LX16A.moveStartAll` is called.

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| relAngle  | `int` | 0           | 240         |
| time      | `int` | 0           | 30000       |

#### Example Program
```python
from lx16a import *
import time

LX16A.initialize("COM3")

servo1 = LX16A(1)

# Rotate the servo to 120 degrees
servo1.moveTimeWrite(120)

# Stores relAngle=30 and time=2000 in servo1
servo1.moveTimeWaitWriteRel(30, 2000)

# Wait for the servo to finish rotating
time.sleep(1)

# Rotate by the stored angle and time
servo1.moveStart()
```

#### Return Value
None

#### Possible Errors
If the servo's current angle plus `relAngle` is out of range, or if `time` is out range, a `ServoError` will be raised.

### LX16A.moveStart()
Rotates the servo by the angle specified by LX16A.moveTimeWaitWrite, or by the the angle specified by moveTimeWaitWriteRel (relative to the servo's currenet angle), over the specified time.

#### Parameters
None

#### Example Program
```python
from lx16a import *
import time

LX16A.initialize("COM3")

servo1 = LX16A(1)

# Stores angle=180 and time=2000 in servo1
servo1.moveTimeWaitWrite(180, 2000)

# Sleep for one second
time.sleep(1)

# Starts rotation of the servo
servo1.moveStart()
```

#### Return Value
None

#### Possible Errors
None

### LX16A.moveStop()
Halts the servo's movement. LX16A.posRead() reflects its real angle, so it will still be accurate even after this function is called.

#### Parameters
None

#### Example Program
```python
from lx16a import *
import time

LX16A.initialize("COM3")

servo1 = LX16A(1)

servo1.moveTimeWrite(180, 5000)

time.sleep(2)

# Halts the servos movement, wherever it is
servo1.moveStop()
```

#### Return Value
None

#### Possible Errors
None

### LX16A.IDWrite(ID)
Changes the ID of the physical servo as well as the servo object. After calling this function, the servo object will still work, but future servo objects referencing this physical servo will have to be aware of the ID change.

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| ID        | `int` | 0           | 253         |

#### Example Program
```python
from lx16a import *

LX16A.initialize("COM3")

servo1 = LX16A(1)

# Changes servo1's ID to 4
servo1.IDWrite(4)
```

#### Return Value
None

#### Possible Errors
If `ID` is out of range, a `ServoError` will be raised.

### LX16A.angleOffsetAdjust(offset)
Adds a constant offset (in degrees) to the servo's position. In a situation where the physical servo was placed a few degrees in a certain direction, this command could be used to adjust for that error. The offset does not adjust the virtual servo's angle. When the servo is powered off, this offset is erased from its memory. It is possible to achieve a negative angle using this command, by having the offset plus the virtual angle be negative. To permanently set an offset, follow this command with `LX16A.angleOffsetWrite`.

NOTE: This command may affect the return value of LX16A.posRead()

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| offset    | `int` | -125        | 125         |

#### Example Code
```python
from lx16a import *

LX16A.initialize("COM3")

servo1 = LX16A(1)

# Sets the servo's offset to -4 degrees
servo1.angleOffsetAdjust(-4)

# Rotates to 120 degrees, but if the offset is taken into account,
# the servo is really at 116 degrees
servo1.moveTimeWrite(120)
```

#### Return Value
None

#### Possible Errors
If `offset` is out of range, a `ServoError` will be raised.
