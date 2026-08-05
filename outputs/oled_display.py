"""
outputs/oled_display.py

Wraps the SSD1306 OLED for on-device readout, independent of whatever
gets sent off-device via a DataTransmitter.
"""

from outputs.outputs import Outputs


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

    def _connect(self) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def show_readings(self, reading) -> None:
        """
        render a sensorreading to the screen
        """
        raise NotImplementedError

    def show_message(self, text: str) -> None:
        """render a message (maybe error or failure or whatever)"""
        raise NotImplementedError
