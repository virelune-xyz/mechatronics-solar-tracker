"""
test.py

quick manual test for the two tilt servos. sweeps each servo through
its full range independently (so you can confirm each one is wired to
the right pin and moves the direction you expect), then moves both
together in sync (which is how they'll actually be driven once
single_axis_tracker is filled in).

run this directly on the pico -- e.g. `mpremote run test.py`, or copy
it to the device and run at the REPL.
"""

import time

import config
from tracking.servo_motor import ServoMotor

STEP_DEG = 10
STEP_DELAY_SEC = 0.3


def sweep(servo: ServoMotor, label: str):
    print("sweeping {} ({} -> {} deg)".format(label, servo.min_angle, servo.max_angle))

    for angle in range(servo.min_angle, servo.max_angle + 1, STEP_DEG):
        servo.set_angle(angle)
        print("  {} -> {} deg".format(label, servo.get_angle()))
        time.sleep(STEP_DELAY_SEC)

    for angle in range(servo.max_angle, servo.min_angle - 1, -STEP_DEG):
        servo.set_angle(angle)
        print("  {} -> {} deg".format(label, servo.get_angle()))
        time.sleep(STEP_DELAY_SEC)

    servo.center()
    print("  {} centered at {} deg".format(label, servo.get_angle()))


def main():
    servo1 = ServoMotor(config.SERVO_1_PIN, config.SERVO_MIN_ANGLE, config.SERVO_MAX_ANGLE)
    servo2 = ServoMotor(config.SERVO_2_PIN, config.SERVO_MIN_ANGLE, config.SERVO_MAX_ANGLE)

    sweep(servo1, "servo1 (pin {})".format(config.SERVO_1_PIN))
    time.sleep(1)
    sweep(servo2, "servo2 (pin {})".format(config.SERVO_2_PIN))
    time.sleep(1)

    print("moving both together")
    midpoint = (config.SERVO_MIN_ANGLE + config.SERVO_MAX_ANGLE) // 2
    for angle in (config.SERVO_MIN_ANGLE, midpoint, config.SERVO_MAX_ANGLE, midpoint):
        servo1.set_angle(angle)
        servo2.set_angle(angle)
        print("  both -> {} deg".format(angle))
        time.sleep(1)

    print("done -- both servos centered at {} deg".format(midpoint))


if __name__ == "__main__":
    main()