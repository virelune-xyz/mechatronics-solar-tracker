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
        print("[DEBUG][serial_transmitter] connecting (baudrate={}, though this is over USB-CDC not a real UART)".format(self._baudrate))
        self.uart_or_usb = sys.stdout

    def send(self, reading) -> bool:
        """
        dont format specially and send
        """
        try:
            self.uart_or_usb.write(str(reading.to_dict()) + "\n")
            print("[DEBUG][serial_transmitter] send() OK")
            return True
        except Exception as e:
            print("[DEBUG][serial_transmitter] send() FAILED:", e)
            return False

    def send_csv_row(self, reading) -> bool:
        """
        format to csv and send
        """
        try:
            row = reading.to_csv_row()
            self.uart_or_usb.write(row + "\n")
            print("[DEBUG][serial_transmitter] send_csv_row() OK ->", row)
            return True
        except Exception as e:
            print("[DEBUG][serial_transmitter] send_csv_row() FAILED:", e)
            return False