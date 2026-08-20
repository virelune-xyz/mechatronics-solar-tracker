from machine import I2C, Pin
import config
from sensors.clock_module import ClockModule

"""
irrelevant file used for testing only and is not a part of the main project in any way
"""

def main() -> None:
    i2c = I2C(
        config.I2C_ID,
        sda=Pin(config.I2C_SDA_PIN),
        scl=Pin(config.I2C_SCL_PIN),
        freq=config.I2C_FREQ_HZ,
    )
    clock = ClockModule(i2c)

    now = (2026, 20, 8, 5, 38, 0, 3)

    clock.set_datetime(now)
    print("RTC set to:", clock.get_datetime())


if __name__ == "__main__":
    main()