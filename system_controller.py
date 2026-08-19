import time

from sensors.clock_module import ClockModule
from sensors.environmental_sensor import EnvironmentalSensor
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
        tracker: SingleAxisTracker,
        display: OLEDDisplay,
        logger: DataLogger,
        transmitter: DataTransmitter,
        update_interval_sec: int = 60,
    ):
        self.clock = clock
        self.env_sensor = env_sensor
        self.tracker = tracker
        self.display = display
        self.logger = logger
        self.transmitter = transmitter
        self.update_interval_sec = update_interval_sec

    def initialize(self):
        """
        make sure every sensor reports is_ready() before entering run(), and show a startup message on the display, if fails then display a message on the oled
        """
        for name, sensor in (("clock", self.clock), ("env_sensor", self.env_sensor)):
            if not sensor.is_ready():
                self.display.show_message("{} not ready".format(name))
                raise OSError("{} failed readiness check".format(name))

        self.display.show_message("System ready")

    def collect_data(self) -> SensorReading:
        """
        pull current timestamp and readings into one sensorreading
        """
        timestamp = self.clock.get_datetime()
        env_data = self.env_sensor.read()
        tilt_angle = self.tracker.servo1.get_angle()

        return SensorReading(
            timestamp=timestamp,
            tilt_angle=tilt_angle,
            temperature=env_data["temperature"],
            humidity=env_data["humidity"],
            pressure=env_data["pressure"],
        )

    def update_display(self, reading: SensorReading):
        self.display.show_readings(reading.to_dict())

    def track_sun(self):
        """delegate to self.tracker.track() using the current rtc time"""
        timestamp = self.clock.get_datetime()
        self.tracker.track(timestamp)

    def transmit_data(self, reading: SensorReading):
        self.transmitter.send(reading)

    def run(self):
        """
        main loop: track_sun() -> collect_data() -> log -> display -> transmit -> sleep(update_interval_sec) -> repeat - runs forever once called from main
        """
        while True:
            self.track_sun()
            reading = self.collect_data()
            self.logger.add_reading(reading)
            self.update_display(reading)
            self.transmit_data(reading)
            time.sleep(self.update_interval_sec)