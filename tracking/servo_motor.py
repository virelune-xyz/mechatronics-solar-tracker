"""
this class only thinks theres one servo and does all the setup assuming only one, only in single_axis_tracker do we specify that theres two
"""

from machine import Pin, PWM

from outputs.outputs import Outputs

_PWM_FREQ_HZ = 50 # standard pwm rate
_PULSE_MIN_US = 500 # pulse width at angle 0
_PULSE_MAX_US = 2500  # pulse width at angle 180
_PERIOD_US = 1_000_000 // _PWM_FREQ_HZ # 20,000 microseconds at 50hz


class ServoMotor(Outputs):
    """
    single pwm-driven servo with clamped range of motion
    """

    def __init__(self, pin: int, min_angle: int = 0, max_angle: int = 180):
        self.pwm = None  # machine.PWM instance, set up in _configure_pwm()
        self.current_angle = (min_angle + max_angle) // 2
        self.min_angle = min_angle
        self.max_angle = max_angle
        self._pin = pin
        self._configure_pwm()

    def _configure_pwm(self) -> None:
        """
        set up machine.PWM on self._pin at the correct frequency and assign it to self.pwm
        """
        self.pwm = PWM(Pin(self._pin))
        self.pwm.freq(_PWM_FREQ_HZ)
        # start at a known safe position rather than leaving duty_u16
        # undefined until the first set_angle() call
        self.center()

    def set_angle(self, angle: int) -> None:
        """
        move the servo to angle degrees, clamped to self.min_angle and self.max_angle, updates self.current_angle
        """
        clamped = max(self.min_angle, min(self.max_angle, angle))
        pulse_us = _PULSE_MIN_US + (clamped / 180) * (_PULSE_MAX_US - _PULSE_MIN_US)
        duty_u16 = int((pulse_us / _PERIOD_US) * 65535)
        self.pwm.duty_u16(duty_u16)
        self.current_angle = clamped

    def get_angle(self) -> int:
        """last commanded angle"""
        return self.current_angle

    def center(self) -> None:
        """move to  midpoint of min_angle and max_angle"""
        self.set_angle((self.min_angle + self.max_angle) // 2)