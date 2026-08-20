import time

from sensors.clock_module import ClockModule
from sensors.environmental_sensor import EnvironmentalSensor
from tracking.single_axis_tracker import SingleAxisTracker
from outputs.oled_display import OLEDDisplay
from logs.data_logger import DataLogger
from comms.data_transmitter import DataTransmitter
from models.sensor_reading import SensorReading
import config


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
        update_interval_sec: int = config.UPDATE_INTERVAL_SEC,
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
        print("[DEBUG][system_controller] initialize() starting")
        for name, sensor in (("clock", self.clock), ("env_sensor", self.env_sensor)):
            ready = sensor.is_ready()
            print("[DEBUG][system_controller] {} is_ready() -> {}".format(name, ready))
            if not ready:
                self.display.show_message("{} not ready".format(name))
                raise OSError("{} failed readiness check".format(name))

        self.display.show_message("System ready")
        print("[DEBUG][system_controller] initialize() complete")

    def collect_data(self) -> SensorReading:
        """
        pull current timestamp and readings into one sensorreading
        """
        timestamp = self.clock.get_datetime()
        env_data = self.env_sensor.read()
        tilt_angle = self.tracker.servo1.get_angle()
        print(
            "[DEBUG][system_controller] collect_data(): timestamp={} env_data={} tilt_angle={}".format(
                timestamp, env_data, tilt_angle
            )
        )

        return SensorReading(
            timestamp=timestamp,
            tilt_angle=tilt_angle,
            temperature=env_data["temperature"],
            humidity=env_data["humidity"],
            pressure=env_data["pressure"],
        )

    def update_display(self, reading: SensorReading):
        print("[DEBUG][system_controller] update_display()")
        self.display.show_readings(reading.to_dict())

    def track_sun(self):
        """delegate to self.tracker.track() using the current rtc time"""
        timestamp = self.clock.get_datetime()
        print("[DEBUG][system_controller] track_sun() at", timestamp)
        self.tracker.track(timestamp)

    def transmit_logs(self, readings):
        success = self.transmitter.send_logs(readings)
        print("[DEBUG][system_controller] transmit_logs() -> count={} success={}".format(
            len(readings), success
        ))

    def run(self):
        """
        main loop: track_sun() -> collect_data() -> log -> display -> transmit -> sleep(update_interval_sec) -> repeat - runs forever once called from main
        """
        loop_count = 0
        print("[DEBUG][system_controller] run() entering main loop, interval={}s".format(self.update_interval_sec))
        while True:
            loop_count += 1
            print("[DEBUG][system_controller] ---- loop iteration {} ----".format(loop_count))
            self.track_sun()
            reading = self.collect_data()
            self.logger.add_reading(reading)
            self.update_display(reading)
            self.transmit_logs([reading])
            print("[DEBUG][system_controller] loop iteration {} done, sleeping {}s".format(
                loop_count, self.update_interval_sec
            ))
            time.sleep(self.update_interval_sec)