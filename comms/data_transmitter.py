"""
just abstract base for communications
"""

from outputs.outputs import Outputs


class DataTransmitter(Outputs):
    """
    do NOT instantiate directly, subclasses must implement send()
    """

    def send(self, reading) -> bool:
        """
        transmit reading off-device, returns true on success, false on a handled failure
        """
        raise NotImplementedError("subclasses of datatransmitter must implement send()")

    def send_logs(self, readings) -> bool:
        """
        transmit a collection of readings, returning false if any send fails
        """
        for reading in readings:
            if not self.send(reading):
                return False
        return True
