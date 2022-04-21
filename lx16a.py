from typing import Union
from math import pi
import serial


class ServoError(Exception):
    def __init__(self, message: str, id_: int = None):
        super().__init__(message)
        self.id_ = id_


class ServoTimeoutError(ServoError):
    pass


class ServoChecksumError(ServoError):
    pass


class ServoArgumentError(ServoError):
    pass


class ServoLogicalError(ServoError):
    pass


class _BSpline:
    def __init__(
        self,
        knots: list[float],
        control_points: list[tuple[float, float]],
        degree: int,
        num_samples: int,
    ):
        self.knots = knots
        self.control_points = control_points
        self.degree = degree

        self.samples = []
        for i in range(num_samples + 1):
            self.samples.append(self.sample(i / num_samples))

    def weight(self, i: int, u: float):
        if self.degree == 0:
            if self.knots[i] <= u < self.knots[i + 1]:
                return 1
            else:
                return 0

        term1 = (
            0
            if self.knots[i] == self.knots[i + self.degree]
            else (u - self.knots[i])
            / (self.knots[i + self.degree] - self.knots[i])
            * self.weight(self.knots, i, self.degree - 1, u)
        )
        term2 = (
            0
            if self.knots[i + 1] == self.knots[i + self.degree + 1]
            else (self.knots[i + self.degree + 1] - u)
            / (self.knots[i + self.degree + 1] - self.knots[i + 1])
            * self.weight(self.knots, i + 1, self.degree - 1, u)
        )
        return term1 + term2

    def sample(self, u: float) -> tuple[float, float]:
        sx = 0
        sy = 0

        for i, control_point in enumerate(self.control_points):
            w = self.weight(i, u)
            sx += w * control_point[0]
            sy += w * control_point[1]

        return sx, sy

    def sample_x(self, x: float):
        for sample in self.samples[:-1]:
            if sample[0] >= x:
                return sample[1]


class LX16A:
    _controller = None

    @staticmethod
    def initialize(port: str, timeout: float = 0.02) -> None:
        if LX16A._controller is not None:
            LX16A._controller.reset_input_buffer()
            LX16A._controller.reset_output_buffer()
            LX16A._controller.close()

        LX16A._controller = serial.Serial(
            port=port, baudrate=115200, timeout=timeout, write_timeout=timeout
        )

    @staticmethod
    def set_timeout(seconds: float) -> None:
        LX16A._controller.timeout = seconds
        LX16A._controller.write_timeout = seconds

    @staticmethod
    def get_timeout() -> float:
        return LX16A._controller.timeout

    def __init__(self, id_: int, disable_torque: bool = False) -> None:
        if id_ < 0 or id_ > 253:
            raise ServoArgumentError(
                "Servo ID must be between 0 and 253 inclusive", id_
            )

        self._id = id_
        self._commanded_angle = LX16A._to_servo_range(self.get_physical_angle())
        self._waiting_angle = self._commanded_angle
        self._waiting_for_move = False
        self._angle_offset = LX16A._to_servo_range(
            self.get_angle_offset(poll_hardware=True)
        )
        self._angle_limits = tuple(
            map(LX16A._to_servo_range, self.get_angle_limits(poll_hardware=True))
        )
        self._vin_limits = self.get_vin_limits(poll_hardware=True)
        self._temp_limit = self.get_temp_limit(poll_hardware=True)
        self._motor_mode = self.is_motor_mode(poll_hardware=True)
        self._motor_speed = (
            self.get_motor_speed(poll_hardware=True) if self._motor_mode else None
        )
        self._torque_enabled = self.is_torque_enabled(poll_hardware=True)
        self._led_powered = self.is_led_power_on(poll_hardware=True)
        self._led_error_triggers = self.get_led_error_triggers(poll_hardware=True)
        self._bspline = None

        if disable_torque:
            self.disable_torque()
        else:
            self.enable_torque()

    ############### Utility Functions ###############

    @staticmethod
    def _checksum(packet: list[int]) -> int:
        s = ~sum(packet[2:])
        return s % 256

    @staticmethod
    def _to_bytes(n: int) -> tuple[int, int]:
        return n % 256, n // 256

    @staticmethod
    def _check_packet(packet: list[int], servo_id: int) -> None:
        if sum(packet) == 0:
            raise ServoTimeoutError(f"Servo {servo_id}: not responding", servo_id)
        if LX16A._checksum(packet[:-1]) != packet[-1]:
            LX16A._controller.flushInput()
            raise ServoChecksumError(f"Servo {servo_id}: bad checksum", servo_id)

    @staticmethod
    def _send_packet(packet: list[int]) -> None:
        packet = [0x55, 0x55, *packet]
        packet.append(LX16A._checksum(packet))
        LX16A._controller.write(bytes(packet))

    @staticmethod
    def _read_packet(num_bytes: int, servo_id: int) -> list[int]:
        received = LX16A._controller.read(num_bytes + 6)

        if len(received) != num_bytes + 6:
            raise ServoTimeoutError(
                f"Servo {servo_id}: {len(received)} bytes (expected {num_bytes})",
                servo_id,
            )

        if LX16A._checksum(received[:-1]) != received[-1]:
            raise ServoChecksumError(f"Servo {servo_id}: bad checksum", servo_id)

        return list(received[5:-1])

    @staticmethod
    def _to_servo_range(angle: float) -> int:
        return round(angle * 25 / 6)

    @staticmethod
    def _from_servo_range(angle: int) -> float:
        return angle * 6 / 25

    @staticmethod
    def _check_within_limits(
        value: Union[float, int],
        lower_limit: Union[float, int],
        upper_limit: Union[float, int],
        variable_name: str,
        servo_id: int,
    ) -> None:
        if value < lower_limit or value > upper_limit:
            raise ServoArgumentError(
                f"Servo {servo_id}: {variable_name} must be between {lower_limit} and {upper_limit} (received {value})",
                servo_id,
            )

    ################ Write Commands ################

    def move(
        self, angle: float, time: int = 0, relative: bool = False, wait: bool = False
    ) -> None:
        if not self._torque_enabled:
            raise ServoLogicalError(
                f"Servo {self._id}: torque must be enabled to move", self._id
            )
        if self._motor_mode:
            raise ServoLogicalError(
                f"Servo {self._id}: motor mode must be disabled to control movement",
                self._id,
            )

        LX16A._check_within_limits(angle, 0, 240, "angle", self._id)
        LX16A._check_within_limits(
            angle,
            LX16A._from_servo_range(self._angle_limits[0]),
            LX16A._from_servo_range(self._angle_limits[1]),
            "angle",
            self._id,
        )

        angle = LX16A._to_servo_range(angle)

        if relative:
            angle += self._commanded_angle

        if wait:
            packet = [self._id, 7, 7, *LX16A._to_bytes(angle), *LX16A._to_bytes(time)]
        else:
            packet = [self._id, 7, 1, *LX16A._to_bytes(angle), *LX16A._to_bytes(time)]

        LX16A._send_packet(packet)

        if wait:
            self._waiting_angle = angle
            self._waiting_for_move = True
        else:
            self._commanded_angle = angle

    def move_bspline(self, x: float, time: int = 0, wait: bool = False) -> None:
        if self._bspline is None:
            raise ServoLogicalError(f"Servo {self._id}: no B-Spline defined", self._id)

        self.move(self._bspline.sample_x(x), time, False, wait)

    def move_start(self) -> None:
        if not self._waiting_for_move:
            raise ServoLogicalError(f"Servo {self._id}: not waiting for move", self._id)
        if not self._torque_enabled:
            raise ServoLogicalError(
                f"Servo {self._id}: torque must be enabled to move", self._id
            )
        if self._motor_mode:
            raise ServoLogicalError(
                f"Servo {self._id}: motor mode must be disabled to control movement",
                self._id,
            )

        packet = [self._id, 3, 11]
        LX16A._send_packet(packet)

        self._commanded_angle = self._waiting_angle
        self._waiting_for_move = False

    def move_stop(self) -> None:
        if self._motor_mode:
            raise ServoLogicalError(
                f"Servo {self._id}: motor mode must be disabled to control movement",
                self._id,
            )

        packet = [self._id, 3, 12]
        LX16A._send_packet(packet)

        self._commanded_angle = LX16A._to_servo_range(self.get_physical_angle())

    def set_id(self, id_: int) -> None:
        LX16A._check_within_limits(id_, 0, 253, "servo ID", self._id)

        packet = [self._id, 4, 13, id_]
        LX16A._send_packet(packet)
        self._id = id_

    def set_angle_offset(self, offset: int, permanent: bool = False) -> None:
        LX16A._check_within_limits(offset, -30, 30, "angle offset", self._id)

        offset = LX16A._to_servo_range(offset)
        if offset < 0:
            offset = 256 + offset

        packet = [self._id, 4, 17, offset]
        LX16A._send_packet(packet)
        self._angle_offset = offset

        if permanent:
            packet = [self._id, 3, 18]
            LX16A._send_packet(packet)

    def set_angle_limits(self, lower_limit: float, upper_limit: float) -> None:
        LX16A._check_within_limits(lower_limit, 0, 240, "lower limit", self._id)
        LX16A._check_within_limits(upper_limit, 0, 240, "upper limit", self._id)
        if upper_limit < lower_limit:
            raise ServoArgumentError(
                f"Servo {self._id}: lower limit (received {lower_limit}) must be less than upper limit (received {upper_limit})",
                self._id,
            )

        lower_limit = LX16A._to_servo_range(lower_limit)
        upper_limit = LX16A._to_servo_range(upper_limit)

        packet = [
            self._id,
            7,
            20,
            *LX16A._to_bytes(lower_limit),
            *LX16A._to_bytes(upper_limit),
        ]
        LX16A._send_packet(packet)
        self._angle_limits = lower_limit, upper_limit

    def set_vin_limits(self, lower_limit: int, upper_limit: int) -> None:
        LX16A._check_within_limits(lower_limit, 4500, 12000, "lower limit", self._id)
        LX16A._check_within_limits(upper_limit, 4500, 12000, "upper limit", self._id)
        if upper_limit < lower_limit:
            raise ServoArgumentError(
                f"Servo {self._id}: lower limit (received {lower_limit}) must be less than upper limit (received {upper_limit})",
                self._id,
            )

        packet = [
            self._id,
            7,
            22,
            *LX16A._to_bytes(lower_limit),
            *LX16A._to_bytes(upper_limit),
        ]
        LX16A._send_packet(packet)
        self._vin_limits = lower_limit, upper_limit

    def set_temp_limit(self, upper_limit: int) -> None:
        LX16A._check_within_limits(upper_limit, 50, 100, "temperature limit", self._id)

        packet = [self._id, 4, 24, upper_limit]
        LX16A._send_packet(packet)
        self._temp_limit = upper_limit

    def motor_mode(self, speed: int) -> None:
        if not self._torque_enabled:
            raise ServoLogicalError(
                f"Servo {self._id}: torque must be enabled to control movement",
                self._id,
            )
        # if self._motor_mode:
        #   raise ServoLogicalError(f'Servo {self._id}: servo is already in motor mode')

        LX16A._check_within_limits(speed, -1000, 1000, "motor speed", self._id)
        if speed < 0:
            speed += 65536

        packet = [self._id, 7, 29, 1, 0, *LX16A._to_bytes(speed)]
        LX16A._send_packet(packet)
        self._motor_mode = True

    def servo_mode(self) -> None:
        # if not self._motor_mode:
        #   raise ServoLogicalError(f'Servo {self._id}: servo is already in servo mode')

        packet = [self._id, 7, 29, 0, 0, 0, 0]
        LX16A._send_packet(packet)
        self._motor_mode = False

    def enable_torque(self) -> None:
        packet = [self._id, 4, 31, 0]
        LX16A._send_packet(packet)
        self._torque_enabled = True

    def disable_torque(self) -> None:
        packet = [self._id, 4, 31, 1]
        LX16A._send_packet(packet)
        self._torque_enabled = False

    def led_power_off(self) -> None:
        packet = [self._id, 4, 33, 1]
        LX16A._send_packet(packet)
        self._led_powered = False

    def led_power_on(self) -> None:
        packet = [self._id, 4, 33, 0]
        LX16A._send_packet(packet)
        self._led_powered = True

    def set_led_error_triggers(
        self, over_temperature: bool, over_voltage: bool, rotor_locked: bool
    ) -> None:
        combined = 4 * rotor_locked + 2 * over_voltage + over_temperature
        packet = [self._id, 4, 35, combined]
        LX16A._send_packet(packet)
        self._led_error_triggers = over_temperature, over_voltage, rotor_locked

    def set_bspline(
        self,
        knots: list[float],
        control_points: list[tuple[float, float]],
        degree: int,
        num_samples: int = 100,
    ) -> None:
        if len(knots) != len(control_points) - degree + 1:
            raise ServoArgumentError(
                f"Servo {self._id}: len(knots) != len(control_points) - degree + 1",
                self._id,
            )

        self._bspline = _BSpline(knots, control_points, degree, num_samples)

    ################ Read Commands ################

    def get_last_instant_move_hw(self) -> tuple[float, int]:
        packet = [self._id, 3, 2]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(4, self._id)
        angle = LX16A._from_servo_range(received[0] + received[1] * 256)
        time = received[2] + received[3] * 256
        return angle, time

    def get_last_delayed_move_hw(self) -> tuple[float, int]:
        packet = [self._id, 3, 8]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(4, self._id)
        angle = LX16A._from_servo_range(received[0] + received[1] * 256)
        time = received[2] + received[3] * 256
        return angle, time

    def get_id(self, poll_hardware: bool = False) -> int:
        if not poll_hardware:
            return self._id

        packet = [self._id, 3, 14]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(1, self._id)
        return received[0]

    def get_angle_offset(self, poll_hardware: bool = False) -> int:
        if not poll_hardware:
            return LX16A._from_servo_range(self._angle_offset)

        packet = [self._id, 3, 19]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(1, self._id)
        if received[0] > 125:
            return LX16A._from_servo_range(received[0] - 256)

        return LX16A._from_servo_range(received[0])

    def get_angle_limits(self, poll_hardware: bool = False) -> tuple[float, float]:
        if not poll_hardware:
            return LX16A._from_servo_range(
                self._angle_limits[0]
            ), LX16A._from_servo_range(self._angle_limits[1])

        packet = [self._id, 3, 21]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(4, self._id)
        lower_limit = LX16A._from_servo_range(received[0] + received[1] * 256)
        upper_limit = LX16A._from_servo_range(received[2] + received[3] * 256)
        return lower_limit, upper_limit

    def get_vin_limits(self, poll_hardware: bool = False) -> tuple[int, int]:
        if not poll_hardware:
            return self._vin_limits

        packet = [self._id, 3, 23]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(4, self._id)
        lower_limit = received[0] + received[1] * 256
        upper_limit = received[2] + received[3] * 256
        return lower_limit, upper_limit

    def get_temp_limit(self, poll_hardware: bool = False) -> int:
        if not poll_hardware:
            return self._temp_limit

        packet = [self._id, 3, 25]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(1, self._id)
        return received[0]

    def is_motor_mode(self, poll_hardware: bool = False) -> bool:
        if not poll_hardware:
            return self._motor_mode

        packet = [self._id, 3, 30]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(4, self._id)
        return received[0] == 1

    def get_motor_speed(self, poll_hardware: bool = False) -> int:
        if not self._motor_mode:
            raise ServoLogicalError(f"Servo {self._id}: not in motor mode", self._id)

        if not poll_hardware:
            return self._motor_speed

        packet = [self._id, 3, 30]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(4, self._id)
        if received[0] == 1:
            speed = received[2] + received[3] * 256
            return speed - 65536 if speed > 32767 else speed

        return None

    def is_torque_enabled(self, poll_hardware: bool = False) -> bool:
        if not poll_hardware:
            return self._torque_enabled

        packet = [self._id, 3, 32]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(1, self._id)
        return received[0] == 1

    def is_led_power_on(self, poll_hardware: bool = False) -> bool:
        if not poll_hardware:
            return self._led_powered

        packet = [self._id, 3, 34]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(1, self._id)
        return received[0] == 0

    def get_led_error_triggers(
        self, poll_hardware: bool = False
    ) -> tuple[bool, bool, bool]:
        if not poll_hardware:
            return self._led_error_triggers

        packet = [self._id, 3, 36]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(1, self._id)
        over_temperature = received[0] & 1 != 0
        over_voltage = received[0] & 2 != 0
        rotor_locked = received[0] & 4 != 0
        return over_temperature, over_voltage, rotor_locked

    def get_temp(self) -> int:
        packet = [self._id, 3, 26]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(1, self._id)
        return received[0]

    def get_vin(self) -> int:
        packet = [self._id, 3, 27]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(2, self._id)
        return received[0] + received[1] * 256

    def get_physical_angle(self) -> float:
        packet = [self._id, 3, 28]
        LX16A._send_packet(packet)

        received = LX16A._read_packet(2, self._id)
        angle = received[0] + received[1] * 256
        return LX16A._from_servo_range(angle - 65536 if angle > 32767 else angle)

    def get_commanded_angle(self) -> float:
        return LX16A._from_servo_range(self._commanded_angle)

    def get_waiting_angle(self) -> float:
        if not self._waiting_for_move:
            raise ServoLogicalError(f"Servo {self._id}: not waiting for move", self._id)

        return LX16A._from_servo_range(self._waiting_angle)
