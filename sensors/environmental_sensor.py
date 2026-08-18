from sensors.sensor import Sensor

try:
	import bme280
except ImportError:
	bme280 = None  # surfaced as a clear error in _connect(), not at import time

_CANDIDATE_ADDRESSES = (0x76, 0x77)


class EnvironmentalSensor(Sensor):
	"""
	i2c connected BME280 env sensor
	"""

	def __init__(self, i2c):
		super().__init__(bus_or_pin=i2c)
		self.i2c = i2c
		self.bme = None  # populated in _connect(); bme280 driver instance
		self._connect()

	def _connect(self) -> None:
		"""
		instantiate the underlying bme280 driver against self.i2c and assign it to self.bme. separate from init() so software and hardware failures are split
		"""
		if bme280 is None:
			raise ImportError(
				"bme280 driver not found -- install with `mip install bme280` "
				"before running this on-device."
			)

		present = self.i2c.scan()
		for address in _CANDIDATE_ADDRESSES:
			if address in present:
				self._address = address
				break
		else:
			raise OSError(
				"BME280 not found on the I2C bus at 0x76 or 0x77 -- "
				"check wiring and power."
			)

		self.bme = bme280.BME280(i2c=self.i2c, address=self._address)

	def read(self) -> dict:
		"""returns {"temperature": float, "humidity": float, "pressure": float}"""
		return {
				"temperature": self.read_temperature(),
				"humidity": self.read_humidity(),
				"pressure": self.read_pressure(),
			}

	def is_ready(self) -> bool:
		return self.bme is not None

	def read_temperature(self) -> float:
		"""deg celsius"""
		temperature, _pressure, _humidity = self.bme.raw_values
		return temperature

	def read_humidity(self) -> float:
		"""relative humidity in %"""
		_temperature, _pressure, humidity = self.bme.raw_values
		return humidity

	def read_pressure(self) -> float:
		"""barometric pressure in hPa"""
		_temperature, pressure, _humidity = self.bme.raw_values
		return pressure
