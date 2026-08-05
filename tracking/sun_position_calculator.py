"""
given a timestamp and a fixed site location colculate suns position 
"""


class SunPositionCalculator:
    """
    calculates solar elevation
    """

    def __init__(self, latitude: float, longitude: float, utc_offset: int):
        self.latitude = latitude
        self.longitude = longitude
        self.utc_offset = utc_offset

    def calculate_position(self, dt: tuple) -> tuple:
        """
        given an rtc timestamp tuple, return the suns position
        """
        raise NotImplementedError

    def day_of_year(self, dt: tuple) -> int:
        raise NotImplementedError

    def solar_declination(self, day_of_year: int) -> float:
        raise NotImplementedError

    def hour_angle(self, dt: tuple) -> float:
        raise NotImplementedError
