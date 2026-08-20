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
        dropped = False
        if len(self.readings) > self.max_entries:
            self.readings.pop(0)
            dropped = True
        print("[DEBUG][data_logger] add_reading() -> count={} dropped_oldest={}".format(
            len(self.readings), dropped
        ))

    def get_latest(self) -> SensorReading | None:
        result = self.readings[-1] if self.readings else None
        print("[DEBUG][data_logger] get_latest() ->", result)
        return result

    def get_all(self) -> list:
        result = list(self.readings)
        print("[DEBUG][data_logger] get_all() -> {} readings".format(len(result)))
        return result

    def clear(self):
        print("[DEBUG][data_logger] clear(); was {} readings".format(len(self.readings)))
        self.readings = []