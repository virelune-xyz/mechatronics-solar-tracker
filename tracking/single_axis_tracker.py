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
        elevation_deg, _azimuth_deg = self.calculator.calculate_position(dt)
        self.move_to(elevation_deg)

    def move_to(self, elevation: float):
        """
        move both servos to elevation; need to mirror one (change the angle to be the opposite) since theyre on opposite sides
        """
        self.servo1.set_angle(round(elevation))

        # mirror around the midpoint of the servo's own range, since servo2 is mounted on the opposite side of the panel
        mirrored = self.servo1.min_angle + self.servo1.max_angle - elevation
        self.servo2.set_angle(round(mirrored))

    def park(self):
        """
        move both servos to a center position - probably not needed (except for graceful shutdown to park if necessary)
        """
        self.servo1.center()
        self.servo2.center()