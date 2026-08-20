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
	clock.set_datetime((2026, 8, 20, 16, 0, 0, 0))
	print(clock.get_datetime())


if __name__ == "__main__":
	main()