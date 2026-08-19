from outputs.outputs import Outputs

try:
	import drivers.ssd1306
except ImportError:
	ssd1306 = None  # surfaced as a clear error in _connect(), not at import time

_LINE_HEIGHT_PX = 10  # 8px font + 2px spacing, fits 6 lines on a 64px-tall display


class OLEDDisplay(Outputs):
	"""
	i2c connected 128x64 SSD1306 OLED
	"""

	def __init__(self, i2c, width: int = 128, height: int = 64):
		self.i2c = i2c
		self.width = width
		self.height = height
		self.driver = None  # populated in _connect(); ssd1306.SSD1306_I2C instance
		self._connect()

	def _connect(self):
		if ssd1306 is None:
			raise ImportError(
				"ssd1306 driver not found"
			)
		self.driver = ssd1306.SSD1306_I2C(self.width, self.height, self.i2c)
		self.clear()

	def clear(self):
		self.driver.fill(0)
		self.driver.show()

	def show_readings(self, reading):
		"""
		render a sensorreading to the screen
		"""
		self.driver.fill(0)
		y = 0

		timestamp = reading.get("timestamp")
		if timestamp is not None:
			year, month, day, hour, minute, second = timestamp[:6]
			self.driver.text(
				"{:04d}-{:02d}-{:02d}".format(year, month, day), 0, y
			)
			y += _LINE_HEIGHT_PX
			self.driver.text(
				"{:02d}:{:02d}:{:02d}".format(hour, minute, second), 0, y
			)
			y += _LINE_HEIGHT_PX

		temperature = reading.get("temperature")
		if temperature is not None:
			self.driver.text("Temp: {:.1f} C".format(temperature), 0, y)
			y += _LINE_HEIGHT_PX

		humidity = reading.get("humidity")
		if humidity is not None:
			self.driver.text("Hum:  {:.1f} %".format(humidity), 0, y)
			y += _LINE_HEIGHT_PX

		pressure = reading.get("pressure")
		if pressure is not None:
			self.driver.text("Pres: {:.1f} hPa".format(pressure), 0, y)
			y += _LINE_HEIGHT_PX

		self.driver.show()

	def show_message(self, text: str):
		"""render a message (maybe error or failure or whatever)"""
		self.driver.fill(0)
		chars_per_line = self.width // 8
		y = 0
		for start in range(0, len(text), chars_per_line):
			self.driver.text(text[start:start + chars_per_line], 0, y)
			y += _LINE_HEIGHT_PX
			if y >= self.height:
				break
		self.driver.show()
