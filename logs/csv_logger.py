"""
persists sensorreadings to a csv file on the pico's flash storage so they
survive power loss and can be pulled off over usb (e.g. thonny's file panel,
or `mpremote cp`) for analysis on a pc
"""

import os
from models.sensor_reading import SensorReading


class CSVLogger:
    """
    appends sensorreadings to a csv file, creating it with a header row
    if it doesn't already exist
    """

    _HEADER = "timestamp,tilt_angle,temperature,humidity,pressure"

    def __init__(self, filename: str = "solar_tracker_log.csv"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """create the file with a header row if it isn't already there"""
        try:
            os.stat(self.filename)
            print("[DEBUG][csv_logger] {} already exists, appending".format(self.filename))
        except OSError:
            print("[DEBUG][csv_logger] {} not found, creating with header".format(self.filename))
            with open(self.filename, "w") as f:
                f.write(self._HEADER + "\n")

    def append(self, reading: SensorReading):
        """append one reading as a csv row"""
        row = reading.to_csv_row()
        with open(self.filename, "a") as f:
            f.write(row + "\n")
        print("[DEBUG][csv_logger] append() ->", row)

    def append_all(self, readings):
        """append many readings at once (e.g. flushing the in-memory DataLogger)"""
        with open(self.filename, "a") as f:
            for reading in readings:
                f.write(reading.to_csv_row() + "\n")
        print("[DEBUG][csv_logger] append_all() -> {} rows".format(len(readings)))

    def read_all(self) -> str:
        """
        return the full file contents as one string - useful for dumping the whole log over serial on demand)
        """
        with open(self.filename, "r") as f:
            contents = f.read()
        print("[DEBUG][csv_logger] read_all() -> {} bytes".format(len(contents)))
        return contents

    def file_size_bytes(self) -> int:
        size = os.stat(self.filename)[6]
        print("[DEBUG][csv_logger] file_size_bytes() ->", size)
        return size

    def clear(self):
        """wipe the log file back down to just the header row"""
        print("[DEBUG][csv_logger] clear()")
        with open(self.filename, "w") as f:
            f.write(self._HEADER + "\n")