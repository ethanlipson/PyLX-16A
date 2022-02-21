from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QComboBox,
    QListWidget,
    QLabel,
    QSlider,
    QLineEdit,
    QRadioButton,
    QCheckBox,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIntValidator
import serial.tools.list_ports
from pylx16a.lx16a import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 410)
        self.setWindowTitle("PyLX16A Servo Testing Software")

        self.port_selection_box = QComboBox(self)
        self.port_selection_box.setFixedSize(200, 27)
        self.port_selection_box.move(30, 55)
        port_selection_box_label = QLabel("Select Port:", self)
        port_selection_box_label.move(30, 30)

        self.id_selection_box = QListWidget(self)
        self.id_selection_box.setFixedSize(200, 200)
        self.id_selection_box.move(30, 130)
        id_selection_box_label = QLabel("Available IDs:", self)
        id_selection_box_label.move(30, 105)

        self.set_id_line_edit = QLineEdit(self)
        self.set_id_line_edit.setFixedSize(50, 27)
        self.set_id_line_edit.move(80, 355)
        set_id_line_edit_label = QLabel("Set ID:", self)
        set_id_line_edit_label.move(30, 355)
        set_id_line_edit_label.setFixedSize(50, 27)

        self.position_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.position_slider.setMinimum(0)
        self.position_slider.setMaximum(240)
        self.position_slider.setFixedWidth(200)
        self.position_slider.move(300, 55)
        position_slider_label = QLabel("Angle (degrees):", self)
        position_slider_label.move(300, 30)

        self.position_offset_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.position_offset_slider.setMinimum(-30)
        self.position_offset_slider.setMaximum(30)
        self.position_offset_slider.setFixedWidth(200)
        self.position_offset_slider.move(300, 125)
        position_offset_slider_label = QLabel("Angle offset (degrees):", self)
        position_offset_slider_label.setFixedWidth(200)
        position_offset_slider_label.move(300, 100)

        self.angle_lower_limit_textentry = QLineEdit(self)
        self.angle_lower_limit_textentry.setFixedWidth(50)
        self.angle_lower_limit_textentry.move(450, 175)
        self.angle_lower_limit_textentry.setValidator(QIntValidator(0, 240, self))
        self.angle_upper_limit_textentry = QLineEdit(self)
        self.angle_upper_limit_textentry.setFixedWidth(50)
        self.angle_upper_limit_textentry.move(450, 210)
        self.angle_upper_limit_textentry.setValidator(QIntValidator(0, 240, self))
        self.angle_lower_limit_textentry_label = QLabel("Lower Limit (degrees):", self)
        self.angle_lower_limit_textentry_label.move(300, 175)
        self.angle_lower_limit_textentry_label.setFixedWidth(150)
        self.angle_upper_limit_textentry_label = QLabel("Upper Limit (degrees):", self)
        self.angle_upper_limit_textentry_label.move(300, 210)
        self.angle_upper_limit_textentry_label.setFixedWidth(150)

        self.vin_lower_limit_textentry = QLineEdit(self)
        self.vin_lower_limit_textentry.setFixedWidth(50)
        self.vin_lower_limit_textentry.move(450, 265)
        self.vin_lower_limit_textentry.setValidator(QIntValidator(4500, 12000, self))
        self.vin_upper_limit_textentry = QLineEdit(self)
        self.vin_upper_limit_textentry.setFixedWidth(50)
        self.vin_upper_limit_textentry.move(450, 300)
        self.vin_upper_limit_textentry.setValidator(QIntValidator(4500, 12000, self))
        self.vin_lower_limit_textentry_label = QLabel("Voltage Lower Limit (mV):", self)
        self.vin_lower_limit_textentry_label.move(300, 265)
        self.vin_lower_limit_textentry_label.setFixedWidth(150)
        self.vin_upper_limit_textentry_label = QLabel("Voltage Upper Limit (mV):", self)
        self.vin_upper_limit_textentry_label.move(300, 300)
        self.vin_upper_limit_textentry_label.setFixedWidth(150)

        self.temp_limit_textentry = QLineEdit(self)
        self.temp_limit_textentry.setFixedWidth(50)
        self.temp_limit_textentry.move(450, 355)
        self.temp_limit_textentry.setValidator(QIntValidator(50, 100, self))
        self.temp_limit_textentry_label = QLabel("Temp Limit (°C):", self)
        self.temp_limit_textentry_label.move(300, 355)
        self.temp_limit_textentry_label.setFixedWidth(150)

        self.servo_mode_radio_button = QRadioButton("Servo Mode", self)
        self.servo_mode_radio_button.move(565, 50)
        self.motor_mode_radio_button = QRadioButton("Motor Mode", self)
        self.motor_mode_radio_button.move(565, 75)

        self.motor_speed_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.motor_speed_slider.setMinimum(-1000)
        self.motor_speed_slider.setMaximum(1000)
        self.motor_speed_slider.setFixedWidth(200)
        self.motor_speed_slider.move(565, 125)
        motor_speed_slider_label = QLabel("Motor Speed:", self)
        motor_speed_slider_label.move(565, 100)

        self.torque_enabled_checkbox = QCheckBox("Torque Enabled", self)
        self.torque_enabled_checkbox.move(565, 175)
        self.torque_enabled_checkbox.setFixedWidth(200)

        self.led_enabled_checkbox = QCheckBox("LED Enabled", self)
        self.led_enabled_checkbox.move(565, 210)
        self.led_enabled_checkbox.setFixedWidth(200)

        self.led_over_temp_checkbox = QCheckBox("LED Over Temperature", self)
        self.led_over_temp_checkbox.move(565, 258)
        self.led_over_temp_checkbox.setFixedWidth(200)
        self.led_over_voltage_checkbox = QCheckBox("LED Over Voltage", self)
        self.led_over_voltage_checkbox.move(565, 283)
        self.led_over_voltage_checkbox.setFixedWidth(200)
        self.led_rotor_locked_checkbox = QCheckBox("LED Rotor Locked", self)
        self.led_rotor_locked_checkbox.move(565, 308)
        self.led_rotor_locked_checkbox.setFixedWidth(200)

        self.physical_position_readout = QLabel("--°", self)
        self.physical_position_readout.move(565, 367)
        self.physical_position_readout.setFixedWidth(200)
        self.physical_position_readout_label = QLabel("Position", self)
        self.physical_position_readout_label.move(565, 347)

        self.temperature_readout = QLabel("-- °C", self)
        self.temperature_readout.move(635, 367)
        self.temperature_readout.setFixedWidth(200)
        self.temperature_readout_label = QLabel("Temperature", self)
        self.temperature_readout_label.move(635, 347)

        self.voltage_readout = QLabel("-- V", self)
        self.voltage_readout.move(730, 367)
        self.voltage_readout.setFixedWidth(200)
        self.voltage_readout_label = QLabel("Voltage", self)
        self.voltage_readout_label.move(730, 347)

        self.readout_update_timer = QTimer(self)
        self.readout_update_timer.timeout.connect(self.update_readouts)
        self.readout_update_timer.start(250)

        self.active_servo: LX16A = None

        self.position_slider.setValue(0)
        self.position_offset_slider.setValue(0)
        self.motor_speed_slider.setValue(0)
        self.disable_widgets()

        self.port_selection_box.currentTextChanged.connect(self.scan_for_servos)
        self.port_selection_box.currentTextChanged.connect(self.disable_widgets)
        self.port_selection_box.currentTextChanged.connect(self.clear_servo)
        self.id_selection_box.currentTextChanged.connect(self.enable_widgets)
        self.id_selection_box.currentTextChanged.connect(self.set_servo_id)
        self.set_id_line_edit.returnPressed.connect(self.id_updated)
        self.position_slider.sliderMoved.connect(
            lambda pos: self.active_servo.move(pos)
        )
        self.position_offset_slider.sliderMoved.connect(
            lambda offset: self.active_servo.set_angle_offset(offset, permanent=True)
        )
        self.angle_lower_limit_textentry.textChanged.connect(
            lambda text: self.active_servo.set_angle_limits(
                int(text), self.active_servo.get_angle_limits()[1]
            )
            if text != ""
            and int(text) >= 0
            and int(text) <= 240
            and int(text) < self.active_servo.get_angle_limits()[1]
            else None
        )
        self.angle_upper_limit_textentry.textChanged.connect(
            lambda text: self.active_servo.set_angle_limits(
                self.active_servo.get_angle_limits()[0], int(text)
            )
            if text != ""
            and int(text) >= 0
            and int(text) <= 240
            and int(text) > self.active_servo.get_angle_limits()[0]
            else None
        )
        self.vin_lower_limit_textentry.textChanged.connect(
            lambda text: self.active_servo.set_vin_limits(
                int(text), self.active_servo.get_vin_limits()[1]
            )
            if text != ""
            and int(text) >= 4500
            and int(text) <= 12000
            and int(text) < self.active_servo.get_vin_limits()[1]
            else None
        )
        self.vin_upper_limit_textentry.textChanged.connect(
            lambda text: self.active_servo.set_vin_limits(
                self.active_servo.get_vin_limits()[0], int(text)
            )
            if text != ""
            and int(text) >= 4500
            and int(text) <= 12000
            and int(text) > self.active_servo.get_vin_limits()[0]
            else None
        )
        self.temp_limit_textentry.textChanged.connect(
            lambda text: self.active_servo.set_temp_limit(int(text))
            if text != "" and int(text) >= 50 and int(text) <= 100
            else None
        )
        self.servo_mode_radio_button.toggled.connect(
            lambda checked: (self.active_servo.servo_mode() if checked else None)
        )
        self.motor_mode_radio_button.toggled.connect(
            lambda checked: (
                self.active_servo.motor_mode(self.motor_speed_slider.value())
                if checked
                else None
            )
        )
        self.servo_mode_radio_button.toggled.connect(
            lambda checked: (
                checked
                and (
                    self.motor_speed_slider.setEnabled(False)
                    or self.position_slider.setEnabled(True)
                    or self.position_offset_slider.setEnabled(True)
                )
            )
        )
        self.motor_mode_radio_button.toggled.connect(
            lambda checked: (
                checked
                and (
                    self.motor_speed_slider.setEnabled(True)
                    or self.position_slider.setEnabled(False)
                    or self.position_offset_slider.setEnabled(False)
                )
            )
        )
        self.motor_speed_slider.valueChanged.connect(
            lambda speed: (
                self.active_servo.motor_mode(speed)
                if self.motor_mode_radio_button.isChecked()
                else None
            )
        )
        self.torque_enabled_checkbox.stateChanged.connect(
            lambda checked: (
                self.active_servo.enable_torque()
                if checked
                else self.active_servo.disable_torque()
            )
        )
        self.torque_enabled_checkbox.stateChanged.connect(
            lambda checked: (
                (
                    self.position_slider.setEnabled(False)
                    or self.position_offset_slider.setEnabled(False)
                    or self.motor_speed_slider.setEnabled(False)
                    or self.servo_mode_radio_button.setEnabled(False)
                    or self.motor_mode_radio_button.setEnabled(False)
                )
                if not checked
                else (
                    self.servo_mode_radio_button.setEnabled(True)
                    or self.motor_mode_radio_button.setEnabled(True)
                    or (
                        (
                            self.motor_speed_slider.setEnabled(False)
                            or self.position_slider.setEnabled(True)
                            or self.position_offset_slider.setEnabled(True)
                        )
                        if self.servo_mode_radio_button.isChecked()
                        else (
                            self.motor_speed_slider.setEnabled(True)
                            or self.position_slider.setEnabled(False)
                            or self.position_offset_slider.setEnabled(False)
                        )
                    )
                )
            )
        )
        self.led_enabled_checkbox.stateChanged.connect(
            lambda checked: (
                self.active_servo.led_power_on()
                if checked
                else self.active_servo.led_power_off()
            )
        )
        self.led_enabled_checkbox.stateChanged.connect(
            self.set_led_error_triggers_enabled
        )
        self.led_over_temp_checkbox.stateChanged.connect(
            self.set_servo_led_error_triggers
        )
        self.led_over_voltage_checkbox.stateChanged.connect(
            self.set_servo_led_error_triggers
        )
        self.led_rotor_locked_checkbox.stateChanged.connect(
            self.set_servo_led_error_triggers
        )

        self.scan_for_ports()

    def disable_widgets(self):
        self.set_id_line_edit.setEnabled(False)
        self.position_slider.setEnabled(False)
        self.position_offset_slider.setEnabled(False)
        self.angle_lower_limit_textentry.setEnabled(False)
        self.angle_upper_limit_textentry.setEnabled(False)
        self.vin_lower_limit_textentry.setEnabled(False)
        self.vin_upper_limit_textentry.setEnabled(False)
        self.temp_limit_textentry.setEnabled(False)
        self.servo_mode_radio_button.setEnabled(False)
        self.motor_mode_radio_button.setEnabled(False)
        self.motor_speed_slider.setEnabled(False)
        self.torque_enabled_checkbox.setEnabled(False)
        self.led_enabled_checkbox.setEnabled(False)
        self.led_over_temp_checkbox.setEnabled(False)
        self.led_over_voltage_checkbox.setEnabled(False)
        self.led_rotor_locked_checkbox.setEnabled(False)

    def enable_widgets(self):
        self.set_id_line_edit.setEnabled(True)
        self.position_slider.setEnabled(True)
        self.position_offset_slider.setEnabled(True)
        self.angle_lower_limit_textentry.setEnabled(True)
        self.angle_upper_limit_textentry.setEnabled(True)
        self.vin_lower_limit_textentry.setEnabled(True)
        self.vin_upper_limit_textentry.setEnabled(True)
        self.temp_limit_textentry.setEnabled(True)
        self.servo_mode_radio_button.setEnabled(True)
        self.motor_mode_radio_button.setEnabled(True)
        self.motor_speed_slider.setEnabled(True)
        self.torque_enabled_checkbox.setEnabled(True)
        self.led_enabled_checkbox.setEnabled(True)
        self.led_over_temp_checkbox.setEnabled(True)
        self.led_over_voltage_checkbox.setEnabled(True)
        self.led_rotor_locked_checkbox.setEnabled(True)

    def clear_servo(self):
        self.active_servo = None

    def set_servo_id(self, id_):
        if not id_.isdigit():
            return

        self.active_servo = LX16A(int(id_))
        self.active_servo.enable_torque()

        self.position_slider.setValue(int(self.active_servo.get_physical_angle()))
        self.position_offset_slider.setValue(int(self.active_servo.get_angle_offset()))
        self.angle_lower_limit_textentry.setText(
            str(int(self.active_servo.get_angle_limits()[0]))
        )
        self.angle_upper_limit_textentry.setText(
            str(int(self.active_servo.get_angle_limits()[1]))
        )
        self.vin_lower_limit_textentry.setText(
            str(self.active_servo.get_vin_limits()[0])
        )
        self.vin_upper_limit_textentry.setText(
            str(self.active_servo.get_vin_limits()[1])
        )
        self.temp_limit_textentry.setText(str(self.active_servo.get_temp_limit()))
        self.motor_speed_slider.setValue(
            self.active_servo.get_motor_speed()
            if self.active_servo.is_motor_mode()
            else 0
        )
        if self.active_servo.is_motor_mode():
            self.motor_mode_radio_button.setChecked(True)
        else:
            self.servo_mode_radio_button.setChecked(True)
        self.motor_speed_slider.setEnabled(self.active_servo.is_motor_mode())
        self.torque_enabled_checkbox.setChecked(self.active_servo.is_torque_enabled())
        self.led_enabled_checkbox.setChecked(self.active_servo.is_led_power_on())
        self.set_led_error_triggers_enabled(self.active_servo.is_led_power_on())
        self.led_over_temp_checkbox.setChecked(
            self.active_servo.get_led_error_triggers()[0]
        )
        self.led_over_voltage_checkbox.setChecked(
            self.active_servo.get_led_error_triggers()[1]
        )
        self.led_rotor_locked_checkbox.setChecked(
            self.active_servo.get_led_error_triggers()[2]
        )

    def set_servo_led_error_triggers(self):
        self.active_servo.set_led_error_triggers(
            self.led_over_temp_checkbox.isChecked(),
            self.led_over_voltage_checkbox.isChecked(),
            self.led_rotor_locked_checkbox.isChecked(),
        )

    def set_led_error_triggers_enabled(self, enabled):
        self.led_over_temp_checkbox.setEnabled(enabled)
        self.led_over_voltage_checkbox.setEnabled(enabled)
        self.led_rotor_locked_checkbox.setEnabled(enabled)

    def scan_for_servos(self, port):
        LX16A.initialize(port)

        self.id_selection_box.clear()

        for i in range(0, 254):
            try:
                servo = LX16A(i)
                self.id_selection_box.addItem(str(i))
            except:
                pass

    def scan_for_ports(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_selection_box.addItem(port.device)

    def update_readouts(self):
        if self.active_servo is None:
            return

        try:
            self.physical_position_readout.setText(
                f"{int(self.active_servo.get_physical_angle())}°"
            )
            self.temperature_readout.setText(f"{self.active_servo.get_temp()} °C")
            self.voltage_readout.setText(f"{self.active_servo.get_vin() / 1000} V")
        except (ServoTimeoutError, ServoChecksumError):
            pass

    def id_updated(self):
        new_id = self.set_id_line_edit.text()
        self.active_servo.set_id(int(new_id))
        self.id_selection_box.item(self.id_selection_box.currentRow()).setText(new_id)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
