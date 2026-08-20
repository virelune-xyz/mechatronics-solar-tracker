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

    print("[DEBUG][main] config: I2C_ID={} SDA={} SCL={} FREQ={}".format(
        config.I2C_ID, config.I2C_SDA_PIN, config.I2C_SCL_PIN, config.I2C_FREQ_HZ
    ))
    print("[DEBUG][main] config: SERVO_1_PIN={} SERVO_2_PIN={} range=({},{})".format(
        config.SERVO_1_PIN, config.SERVO_2_PIN, config.SERVO_MIN_ANGLE, config.SERVO_MAX_ANGLE
    ))
    print("[DEBUG][main] config: SITE_LATITUDE={} SITE_LONGITUDE={} SITE_UTC_OFFSET={}".format(
        config.SITE_LATITUDE, config.SITE_LONGITUDE, config.SITE_UTC_OFFSET
    ))

    print("[DEBUG][main] setting up I2C bus")
    i2c = I2C(
        config.I2C_ID,
        sda=Pin(config.I2C_SDA_PIN),
        scl=Pin(config.I2C_SCL_PIN),
        freq=config.I2C_FREQ_HZ,
    )
    print("[DEBUG][main] i2c.scan() ->", [hex(a) for a in i2c.scan()])

    print("[DEBUG][main] constructing ClockModule")
    clock = ClockModule(i2c)
    print("[DEBUG][main] constructing EnvironmentalSensor")
    env_sensor = EnvironmentalSensor(i2c)

    print("[DEBUG][main] constructing servo1 on pin {}".format(config.SERVO_1_PIN))
    servo1 = ServoMotor(config.SERVO_1_PIN, config.SERVO_MIN_ANGLE, config.SERVO_MAX_ANGLE)
    print("[DEBUG][main] constructing servo2 on pin {}".format(config.SERVO_2_PIN))
    servo2 = ServoMotor(config.SERVO_2_PIN, config.SERVO_MIN_ANGLE, config.SERVO_MAX_ANGLE)
    print("[DEBUG][main] constructing SunPositionCalculator")
    calculator = SunPositionCalculator(
        config.SITE_LATITUDE, config.SITE_LONGITUDE, config.SITE_UTC_OFFSET
    )
    print("[DEBUG][main] constructing SingleAxisTracker")
    tracker = SingleAxisTracker(servo1, servo2, calculator)

    print("[DEBUG][main] constructing OLEDDisplay")
    display = OLEDDisplay(i2c)
    print("[DEBUG][main] constructing DataLogger")
    logger = DataLogger(config.DATA_LOGGER_MAX_ENTRIES)
    print("[DEBUG][main] constructing SerialTransmitter")
    transmitter = SerialTransmitter(config.SERIAL_BAUDRATE)

    print("[DEBUG][main] constructing SystemController")
    controller = SystemController(
        clock=clock,
        env_sensor=env_sensor,
        tracker=tracker,
        display=display,
        logger=logger,
        transmitter=transmitter,
        update_interval_sec=config.UPDATE_INTERVAL_SEC,
    )

    print("[DEBUG][main] calling controller.initialize()")
    controller.initialize()
    print("[DEBUG][main] calling controller.run(); entering main loop")
    controller.run()


if __name__ == "__main__":
    main()