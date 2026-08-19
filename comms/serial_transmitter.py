"""
sends SensorReadings out over usb as CSV rows
"""

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
        raise NotImplementedError

    def send(self, reading) -> bool:
        """
        dont format specially and send
        """
        raise NotImplementedError

    def send_csv_row(self, reading) -> bool:
        """
        format to csv and send
        """
        raise NotImplementedError
