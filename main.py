from machine import I2C, Pin

import config
from sensors.clock_module import ClockModule
from sensors.environmental_sensor import EnvironmentalSensor
from tracking.servo_motor import ServoMotor
from tracking.sun_position_calculator import SunPositionCalculator
from tracking.single_axis_tracker import SingleAxisTracker
from outputs.oled_display import OLEDDisplay
from logs.data_logger import DataLogger
from comms.serial_transmitter import SerialTransmitter
from system_controller import SystemController

"""
only job is hardware construction (machine.I2C/ADC/pin setup) and wiring the objects into a SystemController. only runs once
"""

def main():
    if config.SITE_LATITUDE == None or config.SITE_LONGITUDE == None or config.SITE_UTC_OFFSET == None:
        raise ValueError(
            "fix the time configs buddy"
        )

    i2c = I2C(
        config.I2C_ID,
        sda=Pin(config.I2C_SDA_PIN),
        scl=Pin(config.I2C_SCL_PIN),
        freq=config.I2C_FREQ_HZ,
    )

    clock = ClockModule(i2c)
    env_sensor = EnvironmentalSensor(i2c)

    servo1 = ServoMotor(config.SERVO_1_PIN, config.SERVO_MIN_ANGLE, config.SERVO_MAX_ANGLE)
    servo2 = ServoMotor(config.SERVO_2_PIN, config.SERVO_MIN_ANGLE, config.SERVO_MAX_ANGLE)
    calculator = SunPositionCalculator(
        config.SITE_LATITUDE, config.SITE_LONGITUDE, config.SITE_UTC_OFFSET
    )
    tracker = SingleAxisTracker(servo1, servo2, calculator)

    display = OLEDDisplay(i2c)
    logger = DataLogger(config.DATA_LOGGER_MAX_ENTRIES)
    transmitter = SerialTransmitter(config.SERIAL_BAUDRATE)

    controller = SystemController(
        clock=clock,
        env_sensor=env_sensor,
        tracker=tracker,
        display=display,
        logger=logger,
        transmitter=transmitter,
        update_interval_sec=config.UPDATE_INTERVAL_SEC,
    )

    controller.initialize()
    controller.run()


if __name__ == "__main__":
    main()