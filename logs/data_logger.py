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

    def add_reading(self, reading: SensorReading) -> None:
        """
        append reading; once len(self.readings) exceeds max_entries, the oldest entry should be dropped
        """
        raise NotImplementedError

    def get_latest(self) -> SensorReading:
        raise NotImplementedError

    def get_all(self) -> list:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError
