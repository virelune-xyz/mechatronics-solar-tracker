from sensors.sensor import Sensor


class EnvironmentalSensor(Sensor):
    """
    i2c connected BME280 env sensor
    """

    def __init__(self, i2c):
        super().__init__(bus_or_pin=i2c)
        self.i2c = i2c
        self.bme = None  # populated in _connect(); bme280 driver instance
        self._connect()

    def _connect(self) -> None:
        """
        instantiate the underlying bme280 driver against self.i2c and assign it to self.bme. separate from init() so software and hardware failures are split
        """
        raise NotImplementedError

    def read(self) -> dict:
        """returns {"temperature": float, "humidity": float, "pressure": float}"""
        raise NotImplementedError

    def is_ready(self) -> bool:
        raise NotImplementedError

    def read_temperature(self) -> float:
        """deg celsius"""
        raise NotImplementedError

    def read_humidity(self) -> float:
        """relative humidity in %"""
        raise NotImplementedError

    def read_pressure(self) -> float:
        """barometric pressure in hPa"""
        raise NotImplementedError
