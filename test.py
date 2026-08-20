from machine import I2C, Pin
import config
from sensors.clock_module import ClockModule


def main() -> None:
    i2c = I2C(
        config.I2C_ID,
        sda=Pin(config.I2C_SDA_PIN),
        scl=Pin(config.I2C_SCL_PIN),
        freq=config.I2C_FREQ_HZ,
    )
    clock = ClockModule(i2c)

    # DS3231 tuple format: (year, month, day, hour, minute, second, weekday)
    # weekday: 0=Monday ... 6=Sunday
    # EDIT THIS LINE to match your actual current time before running:
    now = (2026, 20, 8, 5, 38, 0, 3)   # e.g. Thu 20 Aug 2026, 9:05pm

    clock.set_datetime(now)
    print("RTC set to:", clock.get_datetime())


if __name__ == "__main__":
    main()