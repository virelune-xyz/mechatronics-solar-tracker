from sensors.sensor import Sensor


class BatterySensor(Sensor):
    """
    adc connected battery
    """

    def __init__(self, adc_pin):
        super().__init__(bus_or_pin=adc_pin)
        self.adc_pin = adc_pin
        # ratio to undo the resistor divider (eg 2.0 for equal R1/R2).
        self.voltage_divider_ratio = 2.0

    def read(self) -> dict:
        """returns {"voltage": float, "percentage": float}"""
        raise NotImplementedError

    def is_ready(self) -> bool:
        raise NotImplementedError

    def get_voltage(self) -> float:
        """battery terminal voltage in volts after undoing the divider"""
        raise NotImplementedError

    def get_percentage(self) -> float:
        """
        estimated state of charge 0-100 from get_voltage() against the discharge curve of the battery (TODO: SEARCH THIS UP LATER) 
        """
        raise NotImplementedError
