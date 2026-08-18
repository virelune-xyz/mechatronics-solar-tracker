from sensors.sensor import Sensor

_DS3231_ADDRESS = 0x68
_REG_SECONDS = 0x00  # first of 7 contiguous time registers

def _bcd_to_dec(bcd: int) -> int:
	return (bcd >> 4) * 10 + (bcd & 0x0F)


def _dec_to_bcd(dec: int) -> int:
	return ((dec // 10) << 4) | (dec % 10)

class ClockModule(Sensor):
	"""
	i2c connected DS3231 rtc
	"""

	def __init__(self, i2c):
		super().__init__(bus_or_pin=i2c)
		self.i2c = i2c
		self.rtc = None  # populated in _connect(); ds3231 driver instance
		self._connect()

	def _connect(self) -> None:
		if self.is_ready():
			self.rtc = _DS3231_ADDRESS
		else:
			raise OSError(
				"ds3231 not responding at 0x{:02X}; check wiring maybe and that the rtc has power".format(_DS3231_ADDRESS)
			)

	def read(self) -> dict:
		"""returns {"timestamp": tuple}"""
		return {"timestamp": self.get_datetime()}

	def is_ready(self) -> bool:
		try:
			self.i2c.readfrom_mem(_DS3231_ADDRESS, _REG_SECONDS, 1)
			return True
		except OSError:
			return False

	def get_datetime(self) -> tuple:
		"""return the current (year, month, day, hour, minute, second) tuple"""
		raw = self.i2c.readfrom_mem(_DS3231_ADDRESS, _REG_SECONDS, 7)
		
		second = _bcd_to_dec(raw[0] & 0x7F)
		minute = _bcd_to_dec(raw[1] & 0x7F)
		hour = _bcd_to_dec(raw[2] & 0x3F)  # assumes 24-hour mode (bit6 low)
		weekday = raw[3] & 0x07
		day = _bcd_to_dec(raw[4] & 0x3F)
		month = _bcd_to_dec(raw[5] & 0x1F)  # bit7 (century) ignored
		year = 2000 + _bcd_to_dec(raw[6])

		return (year, month, day, hour, minute, second, weekday)

	def set_datetime(self, dt: tuple) -> None:
		"""
		write a new datetime to the rtc

		format: (year, month, day, hour, minute, second, weekday)
		"""
		year, month, day, hour, minute, second, weekday = dt

		payload = bytes([
			_dec_to_bcd(second),
			_dec_to_bcd(minute),
			_dec_to_bcd(hour),      # 24-hour mode (bit6 left low)
			weekday & 0x07,
			_dec_to_bcd(day),
			_dec_to_bcd(month),
			_dec_to_bcd(year % 100),
		])
		self.i2c.writeto_mem(_DS3231_ADDRESS, _REG_SECONDS, payload)

