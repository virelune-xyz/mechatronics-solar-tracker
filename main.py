from machine import I2C, ADC, Pin

import config
from sensors.clock_module import ClockModule
from sensors.environmental_sensor import EnvironmentalSensor
from sensors.battery_sensor import BatterySensor
from tracking.servo_motor import ServoMotor
from tracking.sun_position_calculator import SunPositionCalculator
from tracking.single_axis_tracker import SingleAxisTracker
from outputs.oled_display import OLEDDisplay
from logs.data_logger import DataLogger
from comms.serial_transmitter import SerialTransmitter
from system_controller import SystemController

"""
only job is hardware construction (machine.I2C/ADC/pin setup) and wiring the objects into a SystemController
Only runs once.
"""

def main() -> None:
    raise NotImplementedError(
        "construct hardware handles, build a SystemController, call initialize() and run()."
    )


if __name__ == "__main__":
    main()
