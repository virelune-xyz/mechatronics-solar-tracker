"""
this class only thinks theres one servo and does all the setup assuming only one, only in single_axis_tracker do we specify that theres two
"""

import time
from machine import Pin, PWM
import config

from outputs.outputs import Outputs

_PWM_FREQ_HZ = 50
_PULSE_MIN_US = 500
_PULSE_MAX_US = 2500
_PERIOD_US = 1_000_000 // _PWM_FREQ_HZ


class ServoMotor(Outputs):

    def __init__(self, pin: int, min_angle: int = 0, max_angle: int = 180):
        self.pwm = None
        self.current_angle = (min_angle + max_angle) // 2
        self.min_angle = min_angle
        self.max_angle = max_angle
        self._pin = pin
        self._configure_pwm()

    def _configure_pwm(self):
        print("[DEBUG][servo_motor] configuring PWM on pin {} at {}Hz".format(self._pin, _PWM_FREQ_HZ))
        self.pwm = PWM(Pin(self._pin))
        self.pwm.freq(_PWM_FREQ_HZ)
        self._write_angle(self.current_angle)  # snap to known-safe start, no sweep needed yet

    def _write_angle(self, angle: float):
        """actually push a single angle out to the pwm pin, no interpolation"""
        pulse_us = _PULSE_MIN_US + (angle / 180) * (_PULSE_MAX_US - _PULSE_MIN_US)
        duty_u16 = int((pulse_us / _PERIOD_US) * 65535)
        self.pwm.duty_u16(duty_u16)

    def set_angle(self, angle: float, smooth: bool = True):
        """
        move the servo to angle degrees, clamped to min/max.
        by default sweeps there in small steps instead of jumping instantly.
        """
        clamped = max(self.min_angle, min(self.max_angle, angle))
        print("[DEBUG][servo_motor] pin {}: set_angle({}) -> clamped={}".format(
            self._pin, angle, clamped
        ))

        if smooth:
            self._sweep_to(clamped)
        else:
            self._write_angle(clamped)

        self.current_angle = clamped

    def _sweep_to(self, target: float):
        start = self.current_angle
        if start == target:
            return
        step = config.SERVO_STEP_DEGREES if target > start else -config.SERVO_STEP_DEGREES

        angle = start
        while (step > 0 and angle < target) or (step < 0 and angle > target):
            angle += step
            if (step > 0 and angle > target) or (step < 0 and angle < target):
                angle = target  # don't overshoot on the last step
            self._write_angle(angle)
            time.sleep_ms(config.SERVO_STEP_DELAY_MS)

    def get_angle(self) -> float:
        print("[DEBUG][servo_motor] pin {}: get_angle() -> {}".format(self._pin, self.current_angle))
        return self.current_angle

    def center(self):
        print("[DEBUG][servo_motor] pin {}: center()".format(self._pin))
        self.set_angle((self.min_angle + self.max_angle) // 2)