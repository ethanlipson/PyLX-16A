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

| Parameter | Type |
| --------- | ---- |
| port      | str  |

#### Example Program
```python
import lx16a

# Initializes the controller board on the port `COM3`
# On Linux, you could use `/dev/ttyUSB0` instead
LX16A.initialize("COM3")
