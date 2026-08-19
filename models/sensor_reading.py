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
        return {
            "timestamp": self.timestamp,
            "tilt_angle": self.tilt_angle,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "pressure": self.pressure,
        }

    def to_csv_row(self) -> str:
        year, month, day, hour, minute, second = self.timestamp[:6]
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d},{},{:.2f},{:.2f},{:.2f}".format(
            year, month, day, hour, minute, second,
            self.tilt_angle, self.temperature, self.humidity, self.pressure,
        )