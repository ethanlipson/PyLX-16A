# Version 1.1.2

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
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIntValidator
import serial.tools.list_ports
import serial.serialutil
from pylx16a.lx16a import *
import platform
import sys


def catch_disconnection(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            if isinstance(e, serial.serialutil.SerialException):
                self.disable_widgets()
                self.clear_servo()
                self.port_refresh_button_clicked(None)
                QMessageBox.critical(None, "Error", "Disconnected from device")
            else:
                QMessageBox.information(None, "Error", str(e))

    return wrapper


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 410)
        self.setWindowTitle(f"LX-16A Testing Software v1.1.2 ({platform.system()})")

        self.port_selection_box = QComboBox(self)
        self.port_selection_box.setFixedSize(200, 27)
        self.port_selection_box.move(30, 65)
        port_selection_box_label = QLabel("Select Port:", self)
        port_selection_box_label.move(30, 35)

        self.port_selection_box_refresh_button = QPushButton("Refresh", self)
        self.port_selection_box_refresh_button.setFixedSize(60, 23)
        self.port_selection_box_refresh_button.move(170, 38)

        self.id_selection_box = QListWidget(self)
        self.id_selection_box.setFixedSize(200, 200)
        self.id_selection_box.move(30, 135)
        id_selection_box_label = QLabel("Connected Servos:", self)
        id_selection_box_label.setFixedWidth(200)
        id_selection_box_label.move(30, 105)

        self.id_selection_box_refresh_button = QPushButton("Refresh", self)
        self.id_selection_box_refresh_button.setFixedSize(60, 23)
        self.id_selection_box_refresh_button.move(170, 108)

        self.set_id_line_edit = QLineEdit(self)
        self.set_id_line_edit.setFixedSize(50, 27)
        self.set_id_line_edit.move(80, 355)
        set_id_line_edit_label = QLabel("Set ID:", self)
        set_id_line_edit_label.move(30, 355)
        set_id_line_edit_label.setFixedSize(50, 27)

        self.set_id_button = QPushButton("Change ID!", self)
        self.set_id_button.setFixedSize(85, 27)
        self.set_id_button.move(145, 355)

        self.position_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.position_slider.setMinimum(0)
        self.position_slider.setMaximum(240)
        self.position_slider.setFixedWidth(200)
        self.position_slider.move(300, 55)
        self.position_slider_readout = QLabel("0.00°", self)
        self.position_slider_readout.setFixedWidth(50)
        self.position_slider_readout.move(450, 30)
        self.position_slider_readout.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        position_slider_label = QLabel("Angle (degrees):", self)
        position_slider_label.move(300, 30)

        self.position_offset_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.position_offset_slider.setMinimum(-30)
        self.position_offset_slider.setMaximum(30)
        self.position_offset_slider.setFixedWidth(200)
        self.position_offset_slider.move(300, 125)
        self.position_offset_slider_readout = QLabel("0.00°", self)
        self.position_offset_slider_readout.setFixedWidth(50)
        self.position_offset_slider_readout.move(450, 100)
        self.position_offset_slider_readout.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
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
        self.id_selection_box_refresh_button.setEnabled(False)
        self.disable_widgets()

        self.port_selection_box.currentTextChanged.connect(
            self.port_selection_box_changed
        )
        self.port_selection_box_refresh_button.clicked.connect(
            self.port_refresh_button_clicked
        )
        self.id_selection_box.currentTextChanged.connect(self.id_selection_box_changed)
        self.id_selection_box_refresh_button.clicked.connect(
            self.id_refresh_button_clicked
        )
        self.set_id_button.pressed.connect(self.id_updated)
        self.position_slider.sliderMoved.connect(self.position_slider_updated)
        self.position_offset_slider.sliderMoved.connect(
            self.position_offset_slider_updated
        )
        self.angle_lower_limit_textentry.textChanged.connect(
            self.angle_lower_limit_updated
        )
        self.angle_upper_limit_textentry.textChanged.connect(
            self.angle_upper_limit_updated
        )
        self.vin_lower_limit_textentry.textChanged.connect(self.vin_lower_limit_updated)
        self.vin_upper_limit_textentry.textChanged.connect(self.vin_upper_limit_updated)
        self.temp_limit_textentry.textChanged.connect(self.temp_limit_updated)
        self.servo_mode_radio_button.toggled.connect(
            self.servo_mode_radio_button_toggled
        )
        self.motor_mode_radio_button.toggled.connect(
            self.motor_mode_radio_button_toggled
        )
        self.motor_speed_slider.valueChanged.connect(self.motor_speed_slider_updated)
        self.torque_enabled_checkbox.stateChanged.connect(
            self.torque_enabled_checkbox_toggled
        )
        self.led_enabled_checkbox.stateChanged.connect(
            self.led_enabled_checkbox_toggled
        )
        self.led_over_temp_checkbox.stateChanged.connect(
            self.led_error_triggers_checkbox_toggled
        )
        self.led_over_voltage_checkbox.stateChanged.connect(
            self.led_error_triggers_checkbox_toggled
        )
        self.led_rotor_locked_checkbox.stateChanged.connect(
            self.led_error_triggers_checkbox_toggled
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

    @catch_disconnection
    def set_servo_id(self, id_):
        if not id_.isdigit():
            return

        self.active_servo = LX16A(int(id_))
        self.active_servo.enable_torque()

        self.position_slider.setValue(int(self.active_servo.get_physical_angle()))
        self.position_slider_readout.setText(
            f"{int(self.active_servo.get_physical_angle() * 25 / 6) * 6 / 25:0.2f}°"
        )
        self.position_offset_slider.setValue(int(self.active_servo.get_angle_offset()))
        self.position_offset_slider_readout.setText(
            f"{int(self.active_servo.get_angle_offset() * 25 / 6) * 6 / 25:0.2f}°"
        )
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
        self.led_over_temp_checkbox.setChecked(
            self.active_servo.get_led_error_triggers()[0]
        )
        self.led_over_voltage_checkbox.setChecked(
            self.active_servo.get_led_error_triggers()[1]
        )
        self.led_rotor_locked_checkbox.setChecked(
            self.active_servo.get_led_error_triggers()[2]
        )

    @catch_disconnection
    def scan_for_servos(self, port):
        self.setCursor(Qt.CursorShape.WaitCursor)

        LX16A.initialize(port)

        self.id_selection_box.clear()

        for i in range(0, 254):
            try:
                servo = LX16A(i)
                self.id_selection_box.addItem(str(i))
            except:
                pass

        self.setCursor(Qt.CursorShape.ArrowCursor)

    @catch_disconnection
    def scan_for_ports(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_selection_box.addItem(port.device)

    @catch_disconnection
    def update_readouts(self):
        if self.active_servo is None:
            return

        try:
            self.physical_position_readout.setText(
                f"{self.active_servo.get_physical_angle():0.2f}°"
            )
            self.temperature_readout.setText(f"{self.active_servo.get_temp()} °C")
            self.voltage_readout.setText(f"{self.active_servo.get_vin() / 1000} V")
        except (ServoTimeoutError, ServoChecksumError):
            pass

    @catch_disconnection
    def id_updated(self):
        new_id = self.set_id_line_edit.text()

        try:
            servo = LX16A(int(new_id))
        except ServoTimeoutError:
            # Meaning this ID is not taken
            self.active_servo.set_id(int(new_id))
            self.id_selection_box.item(self.id_selection_box.currentRow()).setText(
                new_id
            )

            return

        QMessageBox.warning(None, "Error", "ID already taken")

    @catch_disconnection
    def position_slider_updated(self, pos):
        if float(self.voltage_readout.text()[:-2]) < 5:
            QMessageBox.warning(
                None,
                "Error",
                "The voltage going through the servo is too low. Is your battery powered on?",
            )

            return
        self.active_servo.move(pos)
        self.position_slider_readout.setText(f"{int(pos * 25 / 6) * 6 / 25:0.2f}°")

    @catch_disconnection
    def position_offset_slider_updated(self, pos):
        self.active_servo.set_angle_offset(pos)
        self.position_offset_slider_readout.setText(
            f"{int(pos * 25 / 6) * 6 / 25:0.2f}°"
        )

    @catch_disconnection
    def angle_lower_limit_updated(self, text):
        if (
            QIntValidator(0, 240, self).validate(text, 0)
            != QIntValidator.State.Acceptable
        ):
            return

        if int(text) > int(self.angle_upper_limit_textentry.text()):
            return

        self.active_servo.set_angle_limits(
            int(text), int(self.angle_upper_limit_textentry.text())
        )

    @catch_disconnection
    def angle_upper_limit_updated(self, text):
        if (
            QIntValidator(0, 240, self).validate(text, 0)
            != QIntValidator.State.Acceptable
        ):
            return

        if int(text) < int(self.angle_lower_limit_textentry.text()):
            return

        self.active_servo.set_angle_limits(
            int(self.angle_lower_limit_textentry.text()), int(text)
        )

    @catch_disconnection
    def vin_lower_limit_updated(self, text):
        if (
            QIntValidator(4500, 12000, self).validate(text, 0)
            != QIntValidator.State.Acceptable
        ):
            return

        if int(text) > int(self.vin_upper_limit_textentry.text()):
            return

        self.active_servo.set_vin_limits(
            int(text), int(self.vin_upper_limit_textentry.text())
        )

    @catch_disconnection
    def vin_upper_limit_updated(self, text):
        if (
            QIntValidator(4500, 12000, self).validate(text, 0)
            != QIntValidator.State.Acceptable
        ):
            return

        if int(text) < int(self.vin_lower_limit_textentry.text()):
            return

        self.active_servo.set_vin_limits(
            int(self.vin_lower_limit_textentry.text()), int(text)
        )

    @catch_disconnection
    def temp_limit_updated(self, text):
        if (
            QIntValidator(50, 100, self).validate(text, 0)
            != QIntValidator.State.Acceptable
        ):
            return

        self.active_servo.set_temp_limit(int(text))

    @catch_disconnection
    def servo_mode_radio_button_toggled(self, checked):
        if checked:
            self.active_servo.servo_mode()
            self.motor_speed_slider.setEnabled(False)
            self.position_slider.setEnabled(True)
            self.position_offset_slider.setEnabled(True)
        else:
            self.active_servo.motor_mode(int(self.motor_speed_slider.value()))
            self.motor_speed_slider.setEnabled(True)
            self.position_slider.setEnabled(False)
            self.position_offset_slider.setEnabled(False)

    @catch_disconnection
    def motor_mode_radio_button_toggled(self, checked):
        if checked:
            self.active_servo.motor_mode(int(self.motor_speed_slider.value()))
            self.motor_speed_slider.setEnabled(True)
            self.position_slider.setEnabled(False)
            self.position_offset_slider.setEnabled(False)
        else:
            self.active_servo.servo_mode()
            self.motor_speed_slider.setEnabled(False)
            self.position_slider.setEnabled(True)
            self.position_offset_slider.setEnabled(True)

    @catch_disconnection
    def motor_speed_slider_updated(self, pos):
        self.active_servo.motor_mode(pos)

    @catch_disconnection
    def torque_enabled_checkbox_toggled(self, checked):
        if checked:
            self.active_servo.enable_torque()
        else:
            self.active_servo.disable_torque()

        self.position_slider.setEnabled(checked)
        self.position_offset_slider.setEnabled(checked)
        self.servo_mode_radio_button.setEnabled(checked)
        self.motor_mode_radio_button.setEnabled(checked)
        self.motor_speed_slider.setEnabled(checked)

    @catch_disconnection
    def led_enabled_checkbox_toggled(self, checked):
        if checked:
            self.active_servo.led_power_on()
        else:
            self.active_servo.led_power_off()

    @catch_disconnection
    def led_error_triggers_checkbox_toggled(self):
        self.active_servo.set_led_error_triggers(
            self.led_over_voltage_checkbox.isChecked(),
            self.led_over_temp_checkbox.isChecked(),
            self.led_rotor_locked_checkbox.isChecked(),
        )

    @catch_disconnection
    def port_refresh_button_clicked(self, value):
        self.id_selection_box_refresh_button.setEnabled(False)
        self.disable_widgets()
        self.port_selection_box.clear()
        self.id_selection_box.clear()
        self.scan_for_ports()

    @catch_disconnection
    def id_refresh_button_clicked(self, value):
        self.disable_widgets()
        self.id_selection_box.clear()
        self.scan_for_servos(self.port_selection_box.currentText())

    @catch_disconnection
    def port_selection_box_changed(self, text):
        if text == "":
            return

        self.id_selection_box_refresh_button.setEnabled(True)
        self.disable_widgets()
        self.id_selection_box.clear()
        self.clear_servo()
        self.scan_for_servos(text)

    @catch_disconnection
    def id_selection_box_changed(self, text):
        if text == "":
            return

        self.enable_widgets()
        self.set_servo_id(text)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
