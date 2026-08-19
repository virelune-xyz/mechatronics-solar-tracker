"""
sends SensorReadings out over usb as CSV rows
"""

import sys

from comms.data_transmitter import DataTransmitter


class SerialTransmitter(DataTransmitter):
    """
    usb transmitter
    """

    def __init__(self, baudrate: int = 115200):
        self.uart_or_usb = None
        self._baudrate = baudrate
        self._connect()

    def _connect(self):
        # writes go out over the same usb connection the repl uses
        self.uart_or_usb = sys.stdout

    def send(self, reading) -> bool:
        """
        dont format specially and send
        """
        try:
            self.uart_or_usb.write(str(reading.to_dict()) + "\n")
            return True
        except Exception:
            return False

    def send_csv_row(self, reading) -> bool:
        """
        format to csv and send
        """
        try:
            self.uart_or_usb.write(reading.to_csv_row() + "\n")
            return True
        except Exception:
            return False