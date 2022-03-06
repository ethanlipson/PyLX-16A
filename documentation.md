# PyLX-16A Documentation

This document details the features of the library. For a quickstart guide, refer to `readme.md`.

### General notes

- Getter methods ending in `hw` physically query the servo.
- This library throws exceptions instead of silently failing, as it's important to remember that servos can be dangerous if not handled responsibly. Meaning:
  - Out-of-bounds arguments raise an exception. They are not clamped.
  - Attempting to rotate the servo with torque disabled will raise an exception.
- If you are working in a high-stakes environment, you may want to initialize servo objects with torque disabled just to be safe.

## Table of Contents

### Exceptions

- `ServoError` - Base exception for the library
  - `ServoTimeoutError` - Exception for timeout issues
  - `ServoChecksumError` - Exception for bad checksums
  - `ServoArgumentError` - Exception for bad arguments
  - `ServoLogicalError` - Exception for out-of-order commands
    - e.g. `get_motor_speed()` while not in motor mode, `move()` while torque is disabled

Since the last four exceptions inherit from `ServoError`, they can all be caught using `except ServoError`.

All servo exceptions have an `id_` member variable containing the errant servo's ID.

### Initialization

- [`LX16A.initialize`](#lx16ainitialize) - Initialize the class with the bus controller's port
- [`LX16A.__init__`](#lx16a__init__) - LX16A object constructor

### Miscellaneous

- [`LX16A.set_timeout`](#lx16aset_timeout) - Set the serial port's read and write timeouts
- [`LX16A.get_timeout`](#lx16aget_timeout) - Get the serial port's read and write timeouts

### Setter member functions

- [`LX16A.move`](#lx16amove) - Rotate the servo
- [`LX16A.move_bspline`](#lx16amove_bspline) - Sample a point on a B-spline curve to move to, set by [`LX16A.set_bspline`](#lx16aset_bspline)
- [`LX16A.move_start`](#lx16amove_start) - Begin a delayed servo move if set by [`LX16A.move(..., wait=True)`](#lx16amove)
- [`LX16A.move_stop`](#lx16amove_stop) - Halt servo movement
- [`LX16A.set_id`](#lx16aset_id) - Give the servo a new ID (changes the virtual servo's ID to match)
- [`LX16A.set_angle_offset`](#lx16aset_angle_offset) - Set an angle offset applied to all move commands
- [`LX16A.set_angle_limits`](#lx16aset_angle_limits) - Set angle limits to servo rotation
- [`LX16A.set_vin_limits`](#lx16aset_vin_limits) - Set input voltage limits
- [`LX16A.set_temp_limit`](#lx16aset_temp_limit) - Set temperature limits in degrees Celsius
- [`LX16A.motor_mode`](#lx16amotor_mode) - Switch the servo to motor mode and set its rotation speed
- [`LX16A.servo_mode`](#lx16aservo_mode) - Switch the servo to servo mode
- [`LX16A.enable_torque`](#lx16aenable_torque) - Allow the servo to produce torque and prevent it from easily giving to external forces
- [`LX16A.disable_torque`](#lx16adisable_torque) - Prevent the servo from producing torque and allow it to easily give to external forces
- [`LX16A.led_power_on`](#lx16aled_power_on) - Light up the servo's LED
- [`LX16A.led_power_off`](#lx16aled_power_off) - Shut off the servo's LED
- [`LX16A.set_led_error_triggers`](#lx16aset_led_error_triggers) - Set what conditions cause the servo's LED to flash
- [`LX16A.set_bspline`](#lx16aset_bspline) - Set the servo's B-spline to be used by [`LX16A.move_bspline`](#lx16amove_bspline)

### Getter member functions

- [`LX16A.get_last_instant_move_hw`](#lx16aget_last_instant_move_hw) - Get the angle and time of the last call to [`LX16A.move(..., wait=False)`](#lx16amove)
- [`LX16A.get_last_delayed_move_hw`](#lx16aget_last_delayed_move_hw) - Get the angle and time of the last call to [`LX16A.move(..., wait=True)`](#lx16amove)
- [`LX16A.get_id`](#lx16aget_id) - Get the ID of the servo (to avoid making a physical query, servo.id\_ can be used instead)
- [`LX16A.get_angle_offset`](#lx16aget_angle_offset) - Get the servo's angle offset
- [`LX16A.get_angle_limits`](#lx16aget_angle_limits) - Get the servo's angle limits
- [`LX16A.get_vin_limits`](#lx16aget_vin_limits) - Get the servo's input voltage limits
- [`LX16A.get_temp_limit`](#lx16aget_temp_limit) - Get the servo's temperature limit in degrees Celsius
- [`LX16A.is_motor_mode`](#lx16ais_motor_mode) - Check if the servo is in motor mode
- [`LX16A.get_motor_speed`](#lx16aget_motor_speed) - If the servo is in motor mode, get its speed
- [`LX16A.is_torque_enabled`](#lx16ais_torque_enabled) - Check if the servo is allowed to produce torque
- [`LX16A.is_led_power_on`](#lx16ais_led_power_on) - Check if the servo's LED is currently enabled
- [`LX16A.get_led_error_triggers`](#lx16aget_led_error_triggers) - Check what conditions will cause the servo's LED to flash
- [`LX16A.get_temp`](#lx16aget_temp) - Get the servo's current temperature
- [`LX16A.get_vin`](#lx16aget_vin) - Get the servo's current input voltage
- [`LX16A.get_physical_angle`](#lx16aget_physical_angle) - Get the servo's physical angle
- [`LX16A.get_commanded_angle`](#lx16aget_commanded_angle) - Get the servo's commanded angle
- [`LX16A.get_waiting_angle`](#lx16aget_waiting_angle) - Get the servo's waiting angle, if set by [`LX16A.move(..., wait=True)`](#lx16amove)

# Function Documentation

## LX16A.initialize

`@staticmethod LX16A.initialize(port: str, timeout: float = 0.02) -> None`

Initializes the LX16A class with the servo bus controller's port.

#### Parameters

| Parameter | Type  | Default Value | Range | Description                        |
| --------- | ----- | ------------- | ----- | ---------------------------------- |
| port      | str   | Required      | N/A   | Servo controller port              |
| timeout   | float | 0.02          | > 0   | Serial port read and write timeout |

#### Return value

None

#### Exceptions

None

## LX16A.\_\_init\_\_

`LX16A.__init__(self, id_: int, disable_torque: bool = False) -> None`

Servo object constructor.

#### Parameters

| Parameter      | Type | Default Value | Range       | Description                                         |
| -------------- | ---- | ------------- | ----------- | --------------------------------------------------- |
| id\_           | int  | Required      | 0 - 253     | Servo ID                                            |
| disable_torque | bool | False         | True, False | If True, the servo initializes with torque disabled |

#### Return value

None

#### Exceptions

- `ServoArgumentError`
  - If the servo ID is outside the range 0 - 253

## LX16A.set_timeout

`@staticmethod set_timeout(seconds: float) -> None`

Set the serial port's read and write timeouts.

#### Parameters

| Parameter | Type  | Default Value | Range | Description |
| --------- | ----- | ------------- | ----- | ----------- |
| timeout   | float | Required      | > 0   | New timeout |

#### Return value

None

#### Exceptions

None

## LX16A.get_timeout

`@staticmethod get_timeout() -> float`

Get the serial port's read and write timeout.

#### Parameters

None

#### Return value

| Type  | Range | Description     |
| ----- | ----- | --------------- |
| float | > 0   | Current timeout |

#### Exceptions

None

## LX16A.move

`LX16A.move(angle: float, time: float = 0, relative: bool = False, wait: bool = False) -> None`

Move the servo to the specified angle, with options to control rotation duration, relativity, and delay.

#### Parameters

| Parameter | Type  | Default Value | Range             | Description                                                            |
| --------- | ----- | ------------- | ----------------- | ---------------------------------------------------------------------- |
| angle     | float | Required      | 0&deg; - 240&deg; | Target angle in degrees                                                |
| time      | int   | 0             | 0 - 30000         | Rotation duration in milliseconds                                      |
| relative  | bool  | False         | True, False       | Determines if the `angle` parameter is relative                        |
| wait      | bool  | False         | True, False       | Delays movement until [`LX16A.move_start`](#lx16amove_start) is called |

#### Return value

None

#### Exceptions

- `ServoArgumentError`
  - If the angle is outside the range 0&deg; - 240&deg;
  - If the angle is outside the range set by [`LX16A.set_angle_limits`](#lx16aset_angle_limits)
- `ServoLogicalError`
  - If the command is issued while in motor mode
  - If the command is issued while torque is disabled

## LX16A.move_bspline

`LX16A.move_bspline(x: float, time: int = 0, wait: bool = False) -> None`

Samples a point on the B-spline curve set by [`LX16A.set_bspline`](#lx16aset_bspline) and moves to it. Note that this does not sample using the parameter, but effectively finds the parameter corresponding to the input x-value and moves to its matching y-value.

#### Parameters

| Parameter | Type  | Default Value | Range                                                  | Description                                                            |
| --------- | ----- | ------------- | ------------------------------------------------------ | ---------------------------------------------------------------------- |
| x         | float | Required      | Determined by [`LX16A.set_bspline`](#lx16aset_bspline) | B-spline sample x-value                                                |
| time      | int   | 0             | 0 - 30000                                              | Rotation duration in milliseconds                                      |
| wait      | bool  | False         | True, False                                            | Delays movement until [`LX16A.move_start`](#lx16amove_start) is called |

#### Return value

None

#### Exceptions

- `ServoLogicalError`
  - If no B-spline has been set by [`LX16A.set_bspline`](#lx16aset_bspline)

## LX16A.move_start

`LX16A.move_start() -> None`

If a movement command has been set by [`LX16A.move(..., wait=True)`](#lx16amove), running this command will execute it.

#### Parameters

None

#### Return value

None

#### Exceptions

- `ServoLogicalError`
  - If no move command has been set by [`LX16A.move(..., wait=True)`](#lx16amove)
  - If the command is issued while in motor mode
  - If the command is issued while torque is disabled

## LX16A.move_stop

`LX16A.move_stop() -> None`

Halts the servo's movement.

#### Parameters

None

#### Return value

None

#### Exceptions

- `ServoLogicalError`
  - If the command is issued while in motor mode

## LX16A.set_id

`LX16A.set_id(id_: int) -> None`

Gives the servo a new ID. The class instance's internal ID is updated as well, so there shouldn't be any hiccups.

Use this command with care. Many difficulties can arise from two servos having the same ID.

#### Parameters

| Parameter | Type | Default Value | Range | Description  |
| --------- | ---- | ------------- | ----- | ------------ |
| id\_      | int  | Required      | 0-253 | New servo ID |

#### Return value

None

#### Exceptions

- `ServoArgumentError`
  - If the ID is outside the range 0 - 253

## LX16A.set_angle_offset

`LX16A.set_angle_offset(offset: int, permanent: bool = False) -> None`

Creates an offset for move commands. All angle readings will automatically correct for the offset, so you can essentially forget that it's there.

#### Parameters

| Parameter | Type | Default Value | Range              | Description                                |
| --------- | ---- | ------------- | ------------------ | ------------------------------------------ |
| offset    | int  | Required      | -30&deg; - 30&deg; | New rotation angle offset in degrees       |
| permanent | bool | False         | True, False        | If True, saves the offset across shutdowns |

#### Return value

None

#### Exceptions

- `ServoArgumentError`
  - If the offset is outside the range -30&deg; - 30&deg;

## LX16A.set_angle_limits

`LX16A.set_angle_limits(lower_limit: float, upper_limit: float) -> None`

Creates lower and upper angle limits for move commands. If these limits are violated, an exception is thrown.

#### Parameters

| Parameter   | Type  | Default Value | Range             | Description                  |
| ----------- | ----- | ------------- | ----------------- | ---------------------------- |
| lower_limit | float | Required      | 0&deg; - 240&deg; | Lower angle limit in degrees |
| upper_limit | float | Required      | 0&deg; - 240&deg; | Upper angle limit in degrees |

#### Return value

None

#### Exceptions

- `ServoArgumentError`
  - If either limit is outside the range 0&deg; - 240&deg;
  - If the upper limit is less than the lower limit

## LX16A.set_vin_limits

`LX16A.set_vin_limits(lower_limit: int, upper_limit: int) -> None`

Creates lower and upper voltage limits for the servo. If these limits are violated AND the voltage condition has been enabled using [`set_led_error_triggers`](#lx16aset_led_error_triggers), the servo's LED will flash.

#### Parameters

| Parameter   | Type  | Default Value | Range        | Description                             |
| ----------- | ----- | ------------- | ------------ | --------------------------------------- |
| lower_limit | float | Required      | 4500 - 12000 | Lower input voltage limit in millivolts |
| upper_limit | float | Required      | 4500 - 12000 | Upper input voltage limit in millivolts |

#### Return value

None

#### Exceptions

- `ServoArgumentError`
  - If either limit is outside the range 4500 - 12000 millivolts
  - If the upper limit is less than the lower limit

## LX16A.set_temp_limit

`LX16A.set_temp_limit(upper_limit: int) -> None`

Creates an upper temperature limit for the servo. If this limit violated AND the temperature condition has been enabled using [`set_led_error_triggers`](#lx16aset_led_error_triggers), the servo's LED will flash.

#### Parameters

| Parameter   | Type | Default Value | Range    | Description                          |
| ----------- | ---- | ------------- | -------- | ------------------------------------ |
| upper_limit | int  | Required      | 50 - 100 | Temperature limit in degrees Celsius |

#### Return value

None

#### Exceptions

- `ServoArgumentError`
  - If the limit is outside the range 50 &deg;C - 100 &deg;C

## LX16A.motor_mode

`LX16A.motor_mode(speed: int) -> None`

Switches the servo to motor mode, where the rotation speed is controlled instead of the angle.

#### Parameters

| Parameter | Type | Default Value | Range        | Description          |
| --------- | ---- | ------------- | ------------ | -------------------- |
| speed     | int  | Required      | -1000 - 1000 | Motor rotation speed |

#### Return value

None

#### Exceptions

- `ServoArgumentError`
  - If the motor speed is outside the range -1000 - 1000
- `ServoLogicalError`
  - If torque is disabled

## LX16A.servo_mode

`LX16A.servo_mode() -> None`

Switches the servo to servo mode (from motor mode).

#### Parameters

None

#### Return value

None

#### Exceptions

None

## LX16A.enable_torque

`LX16A.enable_torque() -> None`

Allows the servo to produce torque and stops it from being rotated manually.

#### Parameters

None

#### Return value

None

#### Exceptions

- `ServoLogicalError`
  - If torque is already enabled

## LX16A.disable_torque

`LX16A.disable_torque() -> None`

Prevents the servo from producing torque and lets it be rotated manually, essentially reversing [`LX16A.enable_torque`](#lx16aenable_torque).

#### Parameters

None

#### Return value

None

#### Exceptions

- `ServoLogicalError`
  - If torque is already disabled

## LX16A.led_power_on

`LX16A.led_power_on() -> None`

Powers on the servo's LED. Note that even if this function is not called, the LED will still flash if any of the error conditions set by [`LX16A.set_led_error_triggers`](#lx16aset_led_error_triggers) are met.

#### Parameters

None

#### Return value

None

#### Exceptions

None

## LX16A.led_power_off

`LX16A.led_power_off() -> None`

Powers off the servo's LED. Note that even if this function is called, the LED will still flash if any of the error conditions set by [`LX16A.set_led_error_triggers`](#lx16aset_led_error_triggers) are met.

#### Parameters

None

#### Return value

None

#### Exceptions

None

## LX16A.set_led_error_triggers

`LX16A.set_led_error_triggers(over_temperature: bool, over_voltage: bool, rotor_locked: bool) -> None`

Sets what error conditions will cause the servo's LED to flash.

#### Parameters

| Parameter        | Type | Default Value | Range       | Description                                                                |
| ---------------- | ---- | ------------- | ----------- | -------------------------------------------------------------------------- |
| over_temperature | bool | Required      | True, False | If True, the servo's LED will flash if the temperature limit is exceeded   |
| over_voltage     | bool | Required      | True, False | If True, the servo's LED will flash if the input voltage limit is exceeded |
| rotor_locked     | bool | Required      | True, False | If True, the servo's LED will flash if the rotor is locked                 |

#### Return value

None

#### Exceptions

None

## LX16A.set_bspline

`set_bspline(knots: list[float], control_points: list[tuple[float, float]], degree: int, num_samples: int = 100) -> None`

Set the servo's B-spline to be used by [`LX16A.move_bspline`](#lx16amove_bspline).

#### Parameters

| Parameter      | Type                      | Default Value | Range | Description                                                                  |
| -------------- | ------------------------- | ------------- | ----- | ---------------------------------------------------------------------------- |
| knots          | list[float]               | Required      | N/A   | B-spline knots                                                               |
| control_points | list[tuple[float, float]] | Required      | N/A   | B-spline control points                                                      |
| degree         | int                       | Required      | N/A   | B-spline degree                                                              |
| num_samples    | int                       | 100           | > 0   | Number of samples used to compute [`LX16A.move_bspline`](#lx16amove_bspline) |

#### Return value

None

#### Exceptions

- `ServoArgumentError`
  - `len(knots) != len(control_points) - degree + 1`

## LX16A.get_last_instant_move_hw

`LX16A.get_last_instant_move_hw() -> tuple[float, int]`

Gets the `angle` and `time` parameters from the most recent call to [`LX16A.move(..., wait=False)`](#lx16amove).

#### Parameters

None

#### Return value

| Index | Type  | Range             | Description                       |
| ----- | ----- | ----------------- | --------------------------------- |
| 0     | float | 0&deg; - 240&deg; | Target angle in degrees           |
| 1     | int   | 0 - 30000         | Rotation duration in milliseconds |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.get_last_delayed_move_hw

`LX16A.get_last_delayed_move_hw() -> tuple[float, int]`

Gets the `angle` and `time` parameters from the most recent call to [`LX16A.move(..., wait=True)`](#lx16amove).

#### Parameters

None

#### Return value

| Index | Type  | Range             | Description                       |
| ----- | ----- | ----------------- | --------------------------------- |
| 0     | float | 0&deg; - 240&deg; | Target angle in degrees           |
| 1     | int   | 0 - 30000         | Rotation duration in milliseconds |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.get_id

`LX16A.get_id(poll_hardware: bool = False) -> int`

Gets the servo's ID. Set by [`LX16A.set_id`](#lx16aset_id).

#### Parameters

| Parameter     | Type | Default Value | Range       | Description                                                    |
| ------------- | ---- | ------------- | ----------- | -------------------------------------------------------------- |
| poll_hardware | bool | False         | True, False | If true, queries the servo instead of returning internal value |

#### Return value

| Type | Range | Description  |
| ---- | ----- | ------------ |
| int  | 0-253 | New servo ID |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.get_angle_offset

`LX16A.get_angle_offset(poll_hardware: bool = False) -> int`

Gets the servo's angle offset. Set by [`LX16A.set_angle_offset`](#lx16aset_angle_offset)

#### Parameters

| Parameter     | Type | Default Value | Range       | Description                                                    |
| ------------- | ---- | ------------- | ----------- | -------------------------------------------------------------- |
| poll_hardware | bool | False         | True, False | If true, queries the servo instead of returning internal value |

#### Return value

| Type | Range              | Description                          |
| ---- | ------------------ | ------------------------------------ |
| int  | -30&deg; - 30&deg; | New rotation angle offset in degrees |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.get_angle_limits

`LX16A.get_angle_limits(poll_hardware: bool = False) -> tuple[float, float]`

Gets the servo's angle limits. Set by [`LX16A.set_angle_limits`](#lx16aset_angle_limits).

#### Parameters

| Parameter     | Type | Default Value | Range       | Description                                                    |
| ------------- | ---- | ------------- | ----------- | -------------------------------------------------------------- |
| poll_hardware | bool | False         | True, False | If true, queries the servo instead of returning internal value |

#### Return value

| Index | Type  | Range             | Description                  |
| ----- | ----- | ----------------- | ---------------------------- |
| 0     | float | 0&deg; - 240&deg; | Lower angle limit in degrees |
| 1     | float | 0&deg; - 240&deg; | Upper angle limit in degrees |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.get_vin_limits

`LX16A.get_vin_limits(poll_hardware: bool = False) -> tuple[int, int]`

Gets the servo's input voltage limits. Set by [`LX16A.set_vin_limits`](#lx16aset_vin_limits).

#### Parameters

| Parameter     | Type | Default Value | Range       | Description                                                    |
| ------------- | ---- | ------------- | ----------- | -------------------------------------------------------------- |
| poll_hardware | bool | False         | True, False | If true, queries the servo instead of returning internal value |

#### Return value

| Index | Type  | Range        | Description                             |
| ----- | ----- | ------------ | --------------------------------------- |
| 0     | float | 4500 - 12000 | Lower input voltage limit in millivolts |
| 1     | float | 4500 - 12000 | Upper input voltage limit in millivolts |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.get_temp_limit

`LX16A.get_temp_limit(poll_hardware: bool = False) -> int`

Gets the servo's temperature limit. Set by [`LX16A.set_temp_limit`](#lx16aset_temp_limit).

#### Parameters

| Parameter     | Type | Default Value | Range       | Description                                                    |
| ------------- | ---- | ------------- | ----------- | -------------------------------------------------------------- |
| poll_hardware | bool | False         | True, False | If true, queries the servo instead of returning internal value |

#### Return value

| Type | Range    | Description                          |
| ---- | -------- | ------------------------------------ |
| int  | 50 - 100 | Temperature limit in degrees Celsius |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.is_motor_mode

`LX16A.is_motor_mode(poll_hardware: bool = False) -> bool`

Checks if the servo is in motor mode. Set by [`LX16A.motor_mode`](#lx16amotor_mode) and [`LX16A.servo_mode`](#lx16aservo_mode).

#### Parameters

| Parameter     | Type | Default Value | Range       | Description                                                    |
| ------------- | ---- | ------------- | ----------- | -------------------------------------------------------------- |
| poll_hardware | bool | False         | True, False | If true, queries the servo instead of returning internal value |

#### Return value

| Type | Range       | Description                               |
| ---- | ----------- | ----------------------------------------- |
| bool | True, False | Whether or not the servo is in motor mode |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.get_motor_speed

`LX16A.get_motor_speed(poll_hardware: bool = False) -> int`

If the servo is in motor mode, gets its speed. Set by [`LX16A.motor_mode`](#lx16amotor_mode).

#### Parameters

| Parameter     | Type | Default Value | Range       | Description                                                    |
| ------------- | ---- | ------------- | ----------- | -------------------------------------------------------------- |
| poll_hardware | bool | False         | True, False | If true, queries the servo instead of returning internal value |

#### Return value

| Type | Range        | Description          |
| ---- | ------------ | -------------------- |
| int  | -1000 - 1000 | Motor rotation speed |

#### Exceptions

- `ServoLogicalError`
  - If the servo is not in motor mode
- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.is_torque_enabled

`LX16A.is_torque_enabled(poll_hardware: bool = False) -> bool`

Check if the servo can produce torque. Set by [`LX16A.enable_torque`](#lx16aenable_torque) and [`LX16A.disable_torque`](#lx16adisable_torque).

#### Parameters

| Parameter     | Type | Default Value | Range       | Description                                                    |
| ------------- | ---- | ------------- | ----------- | -------------------------------------------------------------- |
| poll_hardware | bool | False         | True, False | If true, queries the servo instead of returning internal value |

#### Return value

| Type | Range       | Description                        |
| ---- | ----------- | ---------------------------------- |
| bool | True, False | Whether or not the servo is loaded |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.is_led_power_on

`LX16A.is_led_power_on(poll_hardware: bool = False) -> bool`

Checks if the servo's LED is powered on. Set by [`LX16A.led_power_off`](#lx16aled_power_on) and [`LX16A.led_power_off`](#lx16aled_power_off).

Note that the servo's LED will flash regardless of the LED's power state if any of the error conditions set by [`LX16A.set_led_error_triggers`](#lx16aset_led_error_triggers) are met.

#### Parameters

| Parameter     | Type | Default Value | Range       | Description                                                    |
| ------------- | ---- | ------------- | ----------- | -------------------------------------------------------------- |
| poll_hardware | bool | False         | True, False | If true, queries the servo instead of returning internal value |

#### Return value

| Type | Range       | Description                               |
| ---- | ----------- | ----------------------------------------- |
| bool | True, False | Whether or not the servo's LED is enabled |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.get_led_error_triggers

`LX16A.get_led_error_triggers(poll_hardware: bool = False) -> tuple[bool, bool, bool]`

Checks what error conditions will cause the servo's LED to flash. Set by [`LX16A.set_led_error_triggers`](#lx16aset_led_error_triggers).

#### Parameters

| Parameter     | Type | Default Value | Range       | Description                                                    |
| ------------- | ---- | ------------- | ----------- | -------------------------------------------------------------- |
| poll_hardware | bool | False         | True, False | If true, queries the servo instead of returning internal value |

#### Return value

| Index | Type | Range       | Description                                                                |
| ----- | ---- | ----------- | -------------------------------------------------------------------------- |
| 0     | bool | True, False | If True, the servo's LED will flash if the temperature limit is exceeded   |
| 1     | bool | True, False | If True, the servo's LED will flash if the input voltage limit is exceeded |
| 2     | bool | True, False | If True, the servo's LED will flash if the rotor is locked                 |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.get_temp

`LX16A.get_temp() -> int`

Gets the temperature of the servo in degrees Celsius.

#### Parameters

None

#### Return value

| Type | Range | Description                                        |
| ---- | ----- | -------------------------------------------------- |
| int  | ℤ     | The servo's current temperature in degrees Celsius |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.get_vin

`LX16A.get_vin() -> int`

Gets the input voltage of the servo in millivolts.

#### Parameters

None

#### Return value

| Type | Range | Description                                     |
| ---- | ----- | ----------------------------------------------- |
| int  | ℕ     | The servo's current input voltage in millivolts |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.get_physical_angle

`LX16A.get_physical_angle() -> float`

Gets the physical angle of the servo. Note that this angle may not be equal to the commanded angle ([`LX16A.get_commanded_angle`](#lx16aget_commanded_angle)), such as in the case of excessive load.

#### Parameters

None

#### Return value

| Type  | Range             | Description                           |
| ----- | ----------------- | ------------------------------------- |
| float | 0&deg; - 240&deg; | The servo's physical angle in degrees |

#### Exceptions

- `ServoTimeoutError`
  - If the program receives less bytes than expected
- `ServoChecksumError`
  - If the program receives a bad checksum

## LX16A.get_commanded_angle

`LX16A.get_commanded_angle() -> float`

Gets the commanded angle of the servo.

#### Parameters

None

#### Return value

| Type  | Range             | Description                            |
| ----- | ----------------- | -------------------------------------- |
| float | 0&deg; - 240&deg; | The servo's commanded angle in degrees |

#### Exceptions

None

## LX16A.get_waiting_angle

`LX16A.get_waiting_angle() -> float`

Gets the servo's waiting angle, if set by [`LX16A.move(..., wait=True)`](#lx16amove).

#### Parameters

None

#### Return value

| Type  | Range             | Description                          |
| ----- | ----------------- | ------------------------------------ |
| float | 0&deg; - 240&deg; | The servo's waiting angle in degrees |

#### Exceptions

- `ServoLogicalError`
  - If no move has been set by [`LX16A.move(..., wait=True)`](#lx16amove)
