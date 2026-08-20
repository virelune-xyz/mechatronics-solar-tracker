from tracking.sun_position_calculator import SunPositionCalculator
from tracking.servo_motor import ServoMotor


class SingleAxisTracker:
    """
    moves two servomotors to keep them angled towards sun
    """

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
        calc the suns current elevation for timestamp dt via self.calculator then call self.move_to() with the resulting angle. calls once per systemcontroller loop iteration
        """
        elevation_deg, azimuth_deg = self.calculator.calculate_position(dt)
        print("[DEBUG][single_axis_tracker] track(dt={}) -> elevation={:.2f} azimuth={:.2f}".format(
            dt, elevation_deg, azimuth_deg
        ))
        self.move_to(elevation_deg)

    def move_to(self, elevation: float):
        """
        move both servos to elevation; need to mirror one (change the angle to be the opposite) since theyre on opposite sides
        """
        print("[DEBUG][single_axis_tracker] move_to(elevation={})".format(elevation))

        elevation_clamped = max(0.0, min(90.0, elevation))
        servo_range = self.servo1.max_angle - self.servo1.min_angle
        target_angle = self.servo1.min_angle + (elevation_clamped / 90.0) * servo_range
        print("[DEBUG][single_axis_tracker] scaled elevation {:.2f} -> servo angle {:.2f} (range {}-{})".format(
            elevation, target_angle, self.servo1.min_angle, self.servo1.max_angle
        ))

        self.servo1.set_angle(target_angle)

        # mirror around the midpoint of the servo's own range, since servo2 is mounted on the opposite side of the panel
        mirrored = self.servo1.min_angle + self.servo1.max_angle - target_angle
        print("[DEBUG][single_axis_tracker] mirrored angle for servo2 -> {}".format(mirrored))
        self.servo2.set_angle(mirrored)

    def park(self):
        """
        move both servos to a center position - probably not needed (except for graceful shutdown to park if necessary)
        """
        print("[DEBUG][single_axis_tracker] park()")
        self.servo1.center()
        self.servo2.center()