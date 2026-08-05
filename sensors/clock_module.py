from sensors.sensor import Sensor


class ClockModule(Sensor):
    """
    i2c connected DS3231 rtc
    """

    def __init__(self, i2c):
        super().__init__(bus_or_pin=i2c)
        self.i2c = i2c
        self.rtc = None  # populated in _connect(); ds3231 driver instance

    def _connect(self) -> None:
        raise NotImplementedError

    def read(self) -> dict:
        """returns {"timestamp": tuple}"""
        raise NotImplementedError

    def is_ready(self) -> bool:
        raise NotImplementedError

    def get_datetime(self) -> tuple:
        """return the current (year, month, day, hour, minute, second) tuple"""
        raise NotImplementedError

    def set_datetime(self, dt: tuple) -> None:
        """write a new datetime to the rtc"""
        raise NotImplementedError
