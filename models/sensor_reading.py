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
        temperature: float,
        humidity: float,
        pressure: float,
        battery_voltage: float,
        battery_percentage: float,
    ):
        self.timestamp = timestamp
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.battery_voltage = battery_voltage
        self.battery_percentage = battery_percentage

    def to_dict(self) -> dict:
        raise NotImplementedError

    def to_csv_row(self) -> str:
        raise NotImplementedError
