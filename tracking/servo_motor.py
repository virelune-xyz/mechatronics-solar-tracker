"""
this class only thinks theres one servo and does all the setup assuming only one, only in single_axis_tracker do we specify that theres two
"""

from outputs.outputs import Outputs


class ServoMotor(Outputs):
    """
    single pwm-driven servo with clamped range of motion
    """

    def __init__(self, pin: int, min_angle: int = 0, max_angle: int = 180):
        self.pwm = None  # machine.PWM instance, set up in _configure_pwm()
        self.current_angle = None
        self.min_angle = min_angle
        self.max_angle = max_angle
        self._pin = pin
        self._configure_pwm()

    def _configure_pwm(self) -> None:
        """
        set up machine.PWM on self._pin at the correct frequency and assign it to self.pwm
        """
        raise NotImplementedError

    def set_angle(self, angle: int) -> None:
        """
        move the servo to angle degrees, clamped to self.min_angle and self.max_angle, updates self.current_angle
        """
        raise NotImplementedError

    def get_angle(self) -> int:
        """last commanded angle"""
        raise NotImplementedError

    def center(self) -> None:
        """move to  midpoint of min_angle and max_angle"""
        raise NotImplementedError
