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
        raise NotImplementedError

    def move_to(self, elevation: float):
        """
        move both servos to elevation; need to mirror one (change the angle to be the opposite) since theyre on opposite sides
        """
        raise NotImplementedError

    def park(self):
        """
		move both servos to a center position - probably not needed
        """
        raise NotImplementedError
