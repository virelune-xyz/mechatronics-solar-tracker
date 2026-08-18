from sensors.sensor import Sensor

try:
	import bme280_float as bme280
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
				"bme280 driver not found"
			)

		present = self.i2c.scan()
		for address in _CANDIDATE_ADDRESSES:
			if address in present:
				self._address = address
				break
		else:
			raise OSError(
				"bme280 not found on the i2c bus at 0x76 or 0x77 -- "
			)

		self.bme = bme280.BME280(i2c=self.i2c, address=self._address)

	def read(self) -> dict:
		"""returns {"temperature": float, "humidity": float, "pressure": float}"""
		# Returns (temp, pressure_in_Pa, humidity)
		temp, press, hum = self.bme.read_compensated_data()
		return {
			"temperature": temp,              # °C
			"humidity": hum,                  # % RH
			"pressure": press / 100.0,        # Convert Pa to hPa
		}

	def is_ready(self) -> bool:
		return self.bme is not None


	def read_temperature(self) -> float:
		"""deg celsius"""
		return self.bme.read_compensated_data()[0]

	def read_humidity(self) -> float:
		"""relative humidity in %"""
		return self.bme.read_compensated_data()[2]

	def read_pressure(self) -> float:
		"""barometric pressure in hPa"""
		return self.bme.read_compensated_data()[1] / 100.0