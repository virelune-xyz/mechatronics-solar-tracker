from sensors.clock_module import ClockModule
from sensors.environmental_sensor import EnvironmentalSensor
from sensors.battery_sensor import BatterySensor
from tracking.single_axis_tracker import SingleAxisTracker
from outputs.oled_display import OLEDDisplay
from logs.data_logger import DataLogger
from comms.data_transmitter import DataTransmitter
from models.sensor_reading import SensorReading


class SystemController:
    """
    wires everything together
    """

    def __init__(
        self,
        clock: ClockModule,
        env_sensor: EnvironmentalSensor,
        battery_sensor: BatterySensor,
        tracker: SingleAxisTracker,
        display: OLEDDisplay,
        logger: DataLogger,
        transmitter: DataTransmitter,
        update_interval_sec: int = 60,
    ):
        self.clock = clock
        self.env_sensor = env_sensor
        self.battery_sensor = battery_sensor
        self.tracker = tracker
        self.display = display
        self.logger = logger
        self.transmitter = transmitter
        self.update_interval_sec = update_interval_sec

    def initialize(self):
        """
        make sure every sensor reports is_ready() before entering run(), and show a startup message on the display, if fails then display a message on the oled
        """
        raise NotImplementedError

    def collect_data(self) -> SensorReading:
        """
        pull current timestamp and readings into one sensorreading
        """
        raise NotImplementedError

    def update_display(self, reading: SensorReading):
        raise NotImplementedError

    def track_sun(self):
        """delegate to self.tracker.track() using the current rtc time"""
        raise NotImplementedError

    def transmit_data(self, reading: SensorReading):
        raise NotImplementedError

    def run(self):
        """
        main loop: track_sun() -> collect_data() -> log -> display -> transmit -> sleep(update_interval_sec) -> repeat - runs forever once called from main
        """
        raise NotImplementedError
