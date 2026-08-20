# from machine import I2C, Pin

import config
# from sensors.clock_module import ClockModule
from comms.serial_transmitter import SerialTransmitter
from models.sensor_reading import SensorReading


def main() -> None:
	# i2c = I2C(
	# 	config.I2C_ID,
	# 	sda=Pin(config.I2C_SDA_PIN),
	# 	scl=Pin(config.I2C_SCL_PIN),
	# 	freq=config.I2C_FREQ_HZ,
	# )
	# clock = ClockModule(i2c)
	# clock.set_datetime((2026, 8, 20, 12, 0, 0, 0))
	# print(clock.get_datetime())

	transmitter = SerialTransmitter(config.SERIAL_BAUDRATE)
	readings = [
		SensorReading((2026, 8, 20, 12, 0, 0, 0), 90, 25.5, 40.0, 1013.2),
		SensorReading((2026, 8, 20, 12, 1, 0, 0), 91, 25.7, 40.5, 1013.1),
	]

	success = transmitter.send_logs(readings)
	print("log transmission successful:", success)


if __name__ == "__main__":
	main()