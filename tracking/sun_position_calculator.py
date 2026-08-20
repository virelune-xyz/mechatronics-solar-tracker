"""
given a timestamp and a fixed site location colculate suns position 

uses coopers equation for declination + the equation-of-time approximation for hour angle
this is accurate to within about half a degree
"""

import math


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

        returns (elevation_deg, azimuth_deg)
        """
        day_of_year = self.day_of_year(dt)
        declination_deg = self.solar_declination(day_of_year)
        hour_angle_deg = self.hour_angle(dt)
        print(
            "[DEBUG][sun_position_calculator] day_of_year={} declination_deg={:.2f} hour_angle_deg={:.2f}".format(
                day_of_year, declination_deg, hour_angle_deg
            )
        )

        lat_rad = math.radians(self.latitude)
        decl_rad = math.radians(declination_deg)
        ha_rad = math.radians(hour_angle_deg)

        sin_elevation = (
            math.sin(lat_rad) * math.sin(decl_rad)
            + math.cos(lat_rad) * math.cos(decl_rad) * math.cos(ha_rad)
        )
        sin_elevation = max(-1.0, min(1.0, sin_elevation))  # clamp for float drift
        elevation_deg = math.degrees(math.asin(sin_elevation))

        elevation_rad = math.radians(elevation_deg)
        cos_elevation = math.cos(elevation_rad)
        if abs(cos_elevation) < 1e-6:
            # sun directly overhead so its undefined; pick a stable fallback rather than dividing by ~0
            azimuth_deg = 180.0 if hour_angle_deg > 0 else 0.0
            print("[DEBUG][sun_position_calculator] cos_elevation near zero, using azimuth fallback")
        else:
            cos_azimuth = (
                math.sin(decl_rad) - math.sin(elevation_rad) * math.sin(lat_rad)
            ) / (cos_elevation * math.cos(lat_rad))
            cos_azimuth = max(-1.0, min(1.0, cos_azimuth))
            azimuth_deg = math.degrees(math.acos(cos_azimuth))
            if hour_angle_deg > 0:
                azimuth_deg = 360.0 - azimuth_deg

        print(
            "[DEBUG][sun_position_calculator] calculate_position({}) -> elevation={:.2f} azimuth={:.2f}".format(
                dt, elevation_deg, azimuth_deg
            )
        )
        return (elevation_deg, azimuth_deg)

    def day_of_year(self, dt: tuple) -> int:
        year, month, day = dt[0], dt[1], dt[2]
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        if is_leap:
            days_in_month[1] = 29
        result = sum(days_in_month[: month - 1]) + day
        print("[DEBUG][sun_position_calculator] day_of_year({}) -> {}".format(dt, result))
        return result

    def solar_declination(self, day_of_year: int) -> float:
        # coopers equation, degrees
        result = 23.45 * math.sin(math.radians(360.0 / 365.0 * (284 + day_of_year)))
        print("[DEBUG][sun_position_calculator] solar_declination({}) -> {:.2f}".format(day_of_year, result))
        return result

    def hour_angle(self, dt: tuple) -> float:
        hour, minute, second = dt[3], dt[4], dt[5]
        day_of_year = self.day_of_year(dt)

        # equation of time (minutes) corrects for earth's elliptical orbit and axial tilt so "clock noon" and "solar noon" line up
        b_deg = 360.0 / 365.0 * (day_of_year - 81)
        b_rad = math.radians(b_deg)
        equation_of_time_min = (
            9.87 * math.sin(2 * b_rad) - 7.53 * math.cos(b_rad) - 1.5 * math.sin(b_rad)
        )

        local_standard_meridian_deg = 15.0 * self.utc_offset
        time_correction_min = (
            4.0 * (self.longitude - local_standard_meridian_deg) + equation_of_time_min
        )

        local_time_hr = hour + minute / 60.0 + second / 3600.0
        solar_time_hr = local_time_hr + time_correction_min / 60.0

        result = 15.0 * (solar_time_hr - 12.0)
        print(
            "[DEBUG][sun_position_calculator] hour_angle: eot_min={:.2f} time_correction_min={:.2f} "
            "local_time_hr={:.2f} solar_time_hr={:.2f} -> {:.2f}".format(
                equation_of_time_min, time_correction_min, local_time_hr, solar_time_hr, result
            )
        )
        return result