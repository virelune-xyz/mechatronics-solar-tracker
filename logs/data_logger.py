"""
in-memory store of recent sensorreadings, used for the on-device history
"""

from models.sensor_reading import SensorReading


class DataLogger:
    """
    append only (until full, then oldest-drops-first) log of sensorreading objects
    """

    def __init__(self, max_entries: int = 500):
        self.readings = []
        self.max_entries = max_entries

    def add_reading(self, reading: SensorReading):
        """
        append reading; once len(self.readings) exceeds max_entries, the oldest entry should be dropped
        """
        self.readings.append(reading)
        if len(self.readings) > self.max_entries:
            self.readings.pop(0)

    def get_latest(self) -> SensorReading | None:
        if not self.readings:
            return None
        return self.readings[-1]

    def get_all(self) -> list:
        return list(self.readings)

    def clear(self):
        self.readings = []