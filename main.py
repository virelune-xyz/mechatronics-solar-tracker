# from machine import I2C, ADC, Pin

# from lib.clock_module import ClockModule
# from lib.environmental_sensor import EnvironmentalSensor
# from lib.battery_sensor import BatterySensor
# from lib.servo_motor import ServoMotor
# from lib.sun_position_calculator import SunPositionCalculator
# from lib.single_axis_tracker import SingleAxisTracker
# from lib.oled_display import OLEDDisplay
# from lib.data_logger import DataLogger
# from lib.serial_transmitter import SerialTransmitter
# from lib.system_controller import SystemController

"""
only job is hardware construction (machine.I2C/ADC/pin setup) and wiring the objects into a SystemController
"""

def main() -> None:
    raise NotImplementedError(
        "construct hardware handles, build a SystemController, call initialize() and run()."
    )


if __name__ == "__main__":
    main()
