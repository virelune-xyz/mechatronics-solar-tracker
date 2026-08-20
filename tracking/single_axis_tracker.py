from tracking.sun_position_calculator import SunPositionCalculator
from tracking.servo_motor import ServoMotor
import config


class SingleAxisTracker:

    def __init__(
        self,
        servo1: ServoMotor,
        servo2: ServoMotor,
        calculator: SunPositionCalculator,
    ):
        self.servo1 = servo1
        self.servo2 = servo2
        self.calculator = calculator

    def track(self, dt: tuple):
        """
        calc the suns current position for timestamp dt, then move to it.
        parks if the sun is below the horizon.
        """
        elevation_deg, azimuth_deg = self.calculator.calculate_position(dt)
        print("[DEBUG][single_axis_tracker] track(dt={}) -> elevation={:.2f} azimuth={:.2f}".format(
            dt, elevation_deg, azimuth_deg
        ))

        if elevation_deg <= 0:
            print("[DEBUG][single_axis_tracker] sun below horizon, parking")
            self.park()
            return

        self.move_to(azimuth_deg)

    def move_to(self, azimuth_deg: float):
        """
        map the sun's azimuth linearly onto the servo range.
        """
        unwrapped = azimuth_deg - 360.0 if azimuth_deg > 180.0 else azimuth_deg

        unwrapped_clamped = max(
            config.AZIMUTH_SUNSET_DEG, min(config.AZIMUTH_SUNRISE_DEG, unwrapped)
        )
        span = config.AZIMUTH_SUNRISE_DEG - config.AZIMUTH_SUNSET_DEG
        fraction = (config.AZIMUTH_SUNRISE_DEG - unwrapped_clamped) / span

        servo_range = self.servo1.max_angle - self.servo1.min_angle
        target_angle = self.servo1.min_angle + fraction * servo_range
        print("[DEBUG][single_axis_tracker] azimuth {:.2f} -> unwrapped {:.2f} -> fraction {:.3f} -> servo angle {:.2f}".format(
            azimuth_deg, unwrapped, fraction, target_angle
        ))

        self.servo1.set_angle(target_angle)

        mirrored = self.servo1.min_angle + self.servo1.max_angle - target_angle
        print("[DEBUG][single_axis_tracker] mirrored angle for servo2 -> {}".format(mirrored))
        self.servo2.set_angle(mirrored)

    def park(self):
        print("[DEBUG][single_axis_tracker] park()")
        self.servo1.center()
        self.servo2.center()