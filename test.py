"""
examples/bme_rtc_display_demo.py

Standalone demo: reads temperature/humidity/pressure from the BME280
and the current time from the DS3231, and shows both on the SSD1306
OLED, refreshing every few seconds.

This intentionally bypasses SystemController -- that class still
orchestrates the full sensing/tracking/logging/transmit pipeline (and
is still a stub), whereas this script exists to exercise just the
three pieces requested: EnvironmentalSensor, ClockModule, and
OLEDDisplay, wired directly. Once SystemController is filled in, this
script becomes redundant and can be deleted or folded into a test.

Copy this file's contents into main.py (or run it directly at the
REPL) to try it on-device. Pin numbers and I2C bus ID come from
config.py.
"""

import time
from machine import I2C, Pin

import config
from sensors.clock_module import ClockModule
from sensors.environmental_sensor import EnvironmentalSensor
from outputs.oled_display import OLEDDisplay

REFRESH_INTERVAL_SEC = 5


def main() -> None:
    i2c = I2C(
        config.I2C_ID,
        sda=Pin(config.I2C_SDA_PIN),
        scl=Pin(config.I2C_SCL_PIN),
        freq=config.I2C_FREQ_HZ,
    )

    display = OLEDDisplay(i2c)
    display.show_message("Starting up...")

    clock = ClockModule(i2c)
    env_sensor = EnvironmentalSensor(i2c)

    for name, sensor in (("RTC", clock), ("BME280", env_sensor)):
        sensor._connect()
        if not sensor.is_ready():
            display.show_message("{} not found -- check wiring".format(name))
            raise OSError("{} failed to initialize".format(name))

    while True:
        year, month, day, hour, minute, second, _weekday = clock.get_datetime()
        env_data = env_sensor.read()

        display.show_readings({
            "timestamp": (year, month, day, hour, minute, second),
            "temperature": env_data["temperature"],
            "humidity": env_data["humidity"],
            "pressure": env_data["pressure"],
        })

        time.sleep(REFRESH_INTERVAL_SEC)


if __name__ == "__main__":
    main()
