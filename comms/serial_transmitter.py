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
        send a reading as one CSV row over the connected USB serial stream
        """
        try:
            row = reading.to_csv_row()
            self.uart_or_usb.write(row + "\n")
            print("[DEBUG][serial_transmitter] send() OK ->", row)
            return True
        except Exception as e:
            print("[DEBUG][serial_transmitter] send() FAILED:", e)
            return False

    def send_logs(self, readings) -> bool:
        """send each logged reading as a CSV row over the USB connection"""
        try:
            sent_count = 0
            for reading in readings:
                if not self.send(reading):
                    return False
                sent_count += 1
            print("[DEBUG][serial_transmitter] send_logs() OK -> {} readings".format(sent_count))
            return True
        except Exception as e:
            print("[DEBUG][serial_transmitter] send_logs() FAILED:", e)
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