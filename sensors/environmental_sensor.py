from sensors.sensor import Sensor

try:
	import drivers.bme280_float as bme280
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

	def _connect(self):
		"""
		instantiate the underlying bme280 driver against self.i2c and assign it to self.bme. separate from init() so software and hardware failures are split
		"""
		print("[DEBUG][environmental_sensor] connecting to BME280")
		if bme280 == None:
			print("[DEBUG][environmental_sensor] bme280 driver import FAILED")
			raise ImportError(
				"bme280 driver not found"
			)

		present = self.i2c.scan()
		print("[DEBUG][environmental_sensor] i2c.scan() ->", [hex(a) for a in present])
		for address in _CANDIDATE_ADDRESSES:
			if address in present:
				self._address = address
				break
		else:
			print("[DEBUG][environmental_sensor] connect FAILED; neither 0x76 nor 0x77 present")
			raise OSError(
				"bme280 not found on the i2c bus at 0x76 or 0x77; "
			)

		print("[DEBUG][environmental_sensor] using address {}".format(hex(self._address)))
		self.bme = bme280.BME280(i2c=self.i2c, address=self._address)
		print("[DEBUG][environmental_sensor] connected OK")

	def read(self) -> dict:
		"""returns {"temperature": float, "humidity": float, "pressure": float}"""
		# Returns (temp, pressure_in_Pa, humidity)
		temp, press, hum = self.bme.read_compensated_data()
		result = {
			"temperature": temp,              # °C
			"humidity": hum,                  # % RH
			"pressure": press / 100.0,        # Convert Pa to hPa
		}
		print("[DEBUG][environmental_sensor] read() ->", result)
		return result

	def is_ready(self) -> bool:
		result = self.bme != None
		print("[DEBUG][environmental_sensor] is_ready() ->", result)
		return result


	def read_temperature(self) -> float:
		"""deg celsius"""
		value = self.bme.read_compensated_data()[0]
		print("[DEBUG][environmental_sensor] read_temperature() ->", value)
		return value

	def read_humidity(self) -> float:
		"""relative humidity in %"""
		value = self.bme.read_compensated_data()[2]
		print("[DEBUG][environmental_sensor] read_humidity() ->", value)
		return value

	def read_pressure(self) -> float:
		"""barometric pressure in hPa"""
		value = self.bme.read_compensated_data()[1] / 100.0
		print("[DEBUG][environmental_sensor] read_pressure() ->", value)
		return value