"""
data container
"""


class SensorReading:
    """
    timestamped snapshot of environmental + battery state
    """

    def __init__(
        self,
        timestamp: tuple,
        tilt_angle: int,
        temperature: float,
        humidity: float,
        pressure: float,
        battery_voltage: float,
        battery_percentage: float,
    ):
        self.timestamp = timestamp
        self.tilt_angle = tilt_angle
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.battery_voltage = battery_voltage
        self.battery_percentage = battery_percentage

    def to_dict(self) -> dict:
        raise NotImplementedError

    def to_csv_row(self) -> str:
        raise NotImplementedError
