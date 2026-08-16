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
