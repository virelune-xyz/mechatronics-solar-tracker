"""
data container
"""


class SensorReading:
    """
    timestamped snapshot of environmental state
    """

    def __init__(
        self,
        timestamp: tuple,
        tilt_angle: int,
        temperature: float,
        humidity: float,
        pressure: float,
    ):
        self.timestamp = timestamp
        self.tilt_angle = tilt_angle
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

    def to_dict(self) -> dict:
        raise NotImplementedError

    def to_csv_row(self) -> str:
        raise NotImplementedError
