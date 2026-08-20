"""
abstract base class for all input/sensing hardware; concrete subclasses live alongside this file in sensors/.
"""

from inputs.inputs import Inputs


class Sensor(Inputs):
    def __init__(self, bus_or_pin):
        # bus_or_pin: machine.I2C instance, machine.ADC instance, or raw pin/channel identifier depending on subclass
        self.bus_or_pin = bus_or_pin

    def read(self) -> dict:
        """
        return the sensors current readings as a dict
        """
        raise NotImplementedError("subclasses of sensor must implement read()")

    def is_ready(self) -> bool:
        """
        return whether the underlying hardware is present and responding
        """
        raise NotImplementedError("subclasses of sensor must implement is_ready()")
