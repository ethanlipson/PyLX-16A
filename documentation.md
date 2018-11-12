# PyLX-16A Documentation

This is the documentation for the Python library PyLX16A, a library for controlling LewanSoul's LX-16A servos. To get started with using them, read `userGuide.md`. This document specifies all of the functionality of the library, so I would recommend reading the User Guide first.

NOTE: In this document, I make a distinction between the physical servo and the virtual servo object. In any program using PyLX16A, there should be a one-to-one correspondence between virtual servo objects and physical servos.

## Reference Guide

### Initialization Functions
* [LX16A.initialize(port)](#lx16ainitializeport) - Initializes the connection between the computer and the servo controller board
* [LX16A.\_\_init\_\_(ID)](#lx16a__init__id) - Creates a servo object

### Write Commands
* [LX16A.moveTimeWrite(angle, time=0)](#lx16amovetimewriteangle-time0) - Rotates the servo to the specified angle over the specified time
* [LX16A.moveTimeWaitWrite(angle, time=0)](#lx16amovetimewaitwriteangle-time0) - Sets an angle and time to be rotated to later
* [LX16A.moveTimeWriteRel(relAngle, time=0)](#lx16amovetimewriterelrelangle-time0) - Rotates the servo to the specified relative angle over the specified time
* [LX16A.moveTimeWaitWriteRel(relAngle, time=0)](#lx16amovetimewaitwriterelrelangle-time0) - Sets a relative angle and time to be rotated to later
* [LX16A.moveStart()](#lx16amovestart) - Begins servo rotation (to be with [`LX16A.moveTimeWaitWrite`](#lx16amovetimewaitwriteangle-time0) or [`LX16A.moveTimeWaitWriteRel`](#lx16amovetimewaitwriterelrelangle-time0))
* [LX16A.moveStop()](#lx16amovestop) - Halts the servo's rotation
* [LX16A.IDWrite(ID)](#lx16aidwriteid) - Modifies the servo's ID
* [LX16A.angleOffsetAdjust(offset)](#lx16aangleoffsetadjustoffset) - Adjusts the servo's position offset
* [LX16A.angleOffsetWrite()](#lx16aangleoffsetwrite) - Permanently writes the servo's position offset to memory
* [LX16A.angleLimitWrite(lower, upper)](#lx16aanglelimitwritelower-upper) - Adjusts the servo's angle boundaries
* [LX16A.vInLimitWrite(lower, upper)](#lx16avinlimitwritelower-upper) - Adjusts the servo's input voltage limits
* LX16A.tempMaxLimitWrite(temp) - Adjusts the servo's maximum temperature limit
* [LX16A.motorMode(speed)](#lx16amotormodespeed) - Switches the servo to motor mode, and makes it rotate at the specified speed
* [LX16A.servoMode()](#lx16aservomode) - Switches the servo to servo mode
* LX16A.loadOrUnloadWrite(power) - Turns the servo on or off
* LX16A.LEDCtrlWrite(power) - Turns the servo's LED on or off
* LX16A.LEDErrorWrite(temp, volt, lock) - Adjusts whether the servo's LED will flash if an error occurs

### Read Commands
* LX16A.moveTimeRead() - Returns the parameters to the last call to `LX16A.moveTimeWrite`
* LX16A.moveTimeWaitRead() - Returns the parameters to the last call to `LX16A.moveTimeWaitWrite`
* LX16A.IDRead() - Returns the servo's ID
* LX16A.angleOffsetRead() - Returns the servo's angle offset
* LX16A.angleLimitRead() - Returns the servo's angle limits
* LX16A.vInLimitRead() - Returns the maximum legal input voltage to the servo
* LX16A.tempMaxLimitRead() - Returns the maximum legal temperature of the servo
* LX16A.tempRead() - Returns the current temperature of the servo
* LX16A.vInRead() - Returns the current input voltage to the servo
* [LX16A.getPhysicalPos()](#lx16agetphysicalpos) - Returns the current physical position of the servo
* [LX16A.getVirtualPos()](#lx16agetvirtualpos) - Returns the current virtual position of the servo
* LX16A.servoMotorModeRead() - Returns whether the servo is in servo or motor mode
* LX16A.loadOrUnloadRead() - Returns whether the servo is loaded or unloaded
* LX16A.LEDCtrlRead() - Returns whether the LED is on or off
* LX16A.LEDErrorRead() - Returns which error conditions will cause the LED to flash

### Global Commands
* LX16A.moveStartAll() - Rotates all servos at once (if they have parameters set by `LX16A.moveTimeWaitWrite` or `LX16A.moveTimeWaitWriteRel`.
* LX16A.moveStopAll() - Halts all servo movement
* LX16A.moveTimeWriteList(servos, data) - Moves multiple servos simultaneously, each with distinct parameters
* LX16A.moveTimeWriteListRel(servos, data) - Moves multiple servos simultaneously, each with distinct parameters, and with relative angles
* LX16A.getServos() - Returns a list of all `LX16A` objects in existence

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
Rotates the servo to the specified angle (in degrees) over the given time (in milliseconds). If the time argument is 0, the servo will rotate as fast as it can, but it will not be instant. If no time argument is given, it will be assumed to be 0. The angle must be inside the bounds set by `LX16A.angleLimitWrite`.

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| angle     | `int` | 0*          | 240*        |
| time      | `int` | 0           | 30000       |

\* These values can be modified by `LX16A.angleLimitWrite`

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
If `angle` is outside of the bounds set by `LX16A.angleLimitWrite`, or if `time` is out of range, a `ServoError` will be raised.

### LX16A.moveTimeWaitWrite(angle, time=0)
Similar to LX16A.moveTimeWrite, except that the servo does not rotate immediately. Instead, it rotates by the angle and time when `LX16A.moveStart` or `LX16A.moveStartAll` is called. The angle must be inside the bounds set by `LX16A.angleLimitWrite`.

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| angle     | `int` | 0*          | 240*        |
| time      | `int` | 0           | 30000       |

\* These values can be modified by `LX16A.angleLimitWrite`

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
If `angle` is outside of the bounds set by `LX16A.angleLimitWrite`, or if `time` is out of range, a `ServoError` will be raised.

### LX16A.moveTimeWriteRel(relAngle, time=0)
Rotates the servo relative to its current angle (in degrees) over the specified time (in seconds). If the time argument is 0, the servo will rotate as fast as it can, but it will not be instant. If no time argument is given, it will be assumed to be 0. The absolute angle must be inside the bounds set by `LX16A.angleLimitWrite`.

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| relAngle  | `int` | 0*          | 240*        |
| time      | `int` | 0           | 30000       |

\* These values can be modified by `LX16A.angleLimitWrite`

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
If the servo's current angle plus `relAngle` is outside of the bounds set by `LX16A.angleLimitWrite`, or if `time` is out range, a `ServoError` will be raised.

### LX16A.moveTimeWaitWriteRel(relAngle, time=0)
Similar to LX16A.moveTimeWriteRel, except that the servo does not rotate immediately. Instead, it rotates by the angle (relative to its current angle) and time when `LX16A.moveStart` or `LX16A.moveStartAll` is called. The absolute angle must be inside the bounds set by `LX16A.angleLimitWrite`.

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| relAngle  | `int` | 0*          | 240*        |
| time      | `int` | 0           | 30000       |

\* These values can be modified by `LX16A.angleLimitWrite`

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
If the servo's current angle plus `relAngle` is outside of the bounds set by `LX16A.angleLimitWrite`, or if `time` is out range, a `ServoError` will be raised.

### LX16A.moveStart()
Rotates the servo by the angle specified by LX16A.moveTimeWaitWrite, or by the the angle specified by moveTimeWaitWriteRel (relative to the servo's current angle), over the specified time.

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

#### Example Program
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

### LX16A.angleOffsetWrite()
Permanently writes the angle offset (set by `LX16A.angleOffsetAdjust`) to the servo's memory. Normally, after the servo is powered off, it loses its angle offset, but after using this command, it will remember.

#### Parameters
None

#### Example Program
```python
from lx16a import *

LX16A.initialize("COM3")

servo1 = LX16A(1)

# Set the angle offset to 22 degrees
servo1.angleOffsetAdjust(22)
servo1.angleOffsetWrite()

# Power the servo off and on again
# ...

# Write 90 degrees to the servo, but since it still remembers the offset,
# the servo is really at 112 degrees (90 + 22 degrees)
servo1.angleOffsetWrite(90)
```

#### Return Value
None

#### Possible Errors
None

### LX16A.angleLimitWrite(lower, upper)
Sets the upper and lower limits for the servo's position. By default, these values are at their limits, 0 and 240 degrees. Note that the lower bound must be strictly less than the upper bound. If you attempt to rotate the servo to a position out of bounds, it will rotate but stop at its limits. If the servo's position is out of bounds set by this command, the servo will be able to rotate back into the legal range, but not back out.

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| lower     | `int` | 0           | 240         |
| upper     | `int` | 0           | 240         |

#### Example Program
```python
from lx16a import *
import time

LX16A.initialize("COM3")

servo1 = LX16A(1)

servo1.moveTimeWrite(120)

time.sleep(1)

servo1.angleLimitWrite(60, 180)

# This command works
servo1.moveTimeWrite(90)

# This one does not
# servo1.moveTimeWrite(210)
```

#### Return Value
None

#### Possible Errors
If either `lower` or `upper` is out of range, or if `lower` >= `upper`, a `ServoError` will be raised.

### LX16A.vInLimitWrite(lower, upper)
Sets the lower and upper limits (in millivolts) for the voltage going into the servo. If the voltage goes outside of these bounds, then the servo will stop working, and the LED will flash. Note that the lower bound must be strictly less than the upper bound.

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| lower     | `int` | 4500        | 12000       |
| upper     | `int` | 4500        | 12000       |

#### Example Program
```python
from lx16a import *

LX16A.initialize("COM3")

servo1 = LX16A(1)

# Normal range
servo1.vInLimitWrite(6000, 10000)
```

#### Return Value
None

#### Possible Errors
If either `lower` or `upper` is out of range, or if `lower` >= `upper`, a `ServoError` will be raised.

### LX16A.motorMode(speed)
Commands the servo to start continously rotating (like a motor), at a speed between -1000 and 1000 (0 is still, 1000 is full speed, and -1000 is full speed in the opposite direction).

#### Parameters
| Parameter | Type  | Lower Bound | Upper Bound |
| --------- | ----- | ----------- | ----------- |
| speed     | `int` | -1000       | 1000        |

#### Example Program
```python
from lx16a import *
import time

LX16A.initialize("COM3")

servo1 = LX16A(1)

# Have the servo rotate back and forth, changing direction every seccond
while True:
  # Set the servo rotating at full speed
  servo1.motorMode(1000)
  time.sleep(1)
  
  # Set the servo rotating at full speed, but backwards
  servo1.motorMode(-1000)
  time.sleep(1)
```

#### Return Value
None

#### Possible Errors
If `speed` is out of bounds, a `ServoError` will be raised.

### LX16A.servoMode()
Reverts the servo back to servo mode (from motor mode, discussed in [`LX16A.motorMode()`](#lx16amotormodespeed).

#### Parameters
None

#### Example Program
```python
from lx16a import *
import time

LX16A.initialize("COM3")

servo1 = LX16A(1)

# Switch the servo to servo mode. rotating at half speed
servo1.motorMode(500)
time.sleep(1)

# Switch the servo back to servo mode
servo1.servoMode()
servo1.moveTimeWrite(60)
```

#### Return Value
None

#### Possible Errors
None

### LX16A.getPhysicalPos()
Returns the physical position of the servo. This will sometimes differ from the commanded position of the servo if, for example, the servo's load is too big, or something is blocking it from rotating.

#### Parameters
None

#### Example Program
```python
from lx16a import *

LX16A.initialize("COM3")

servo1 = LX16A(1)

pos = servo1.getPhysicalPos()
print("The servo's phyiscal position is {} degrees".format(pos))
```

#### Return Value
The physical position of the servo, between 0 and 240 degrees.

#### Possible Errors
None

### LX16A.getVirtualPos()
Returns the position that the servo is ***supposed*** to be at. The servo will usually physically be at this position, but if it is preventing from fully rotating because of a large load (for example), then its physical position will be different.

#### Parameters
None

#### Example Program
```python
from lx16a import *

LX16A.initialize("COM3")

servo1 = LX16A(1)

print("The servo is supposed to be at position", servo1.getVirtualPos())
print("The servo is physically at position", servo1.getPhysicalPos())
```

#### Return Value
The virtual position of the servo, between 0 and 240 degrees.

#### Possible Errors
None
