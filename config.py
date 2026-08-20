"""
just used for pin assignments and stuff like that so theres a nicer way to change things on the fly
"""

# i2c bus (clock, envsensor, oled)
I2C_ID = 1          # eg 0
I2C_SDA_PIN = 2     # eg 0  (GPIO0)
I2C_SCL_PIN = 3
I2C_FREQ_HZ = 400_000

# servo signal pins
SERVO_1_PIN = 8     # eg 2  (GPIO2)
SERVO_2_PIN = 9 
SERVO_MIN_ANGLE = 45
SERVO_MAX_ANGLE = 135

# serial transmitter
SERIAL_BAUDRATE = 115200

# site location for the calculator
SITE_LATITUDE = -33.81789
SITE_LONGITUDE = 150.99607
SITE_UTC_OFFSET = 10

# system
UPDATE_INTERVAL_SEC = 10
DATA_LOGGER_MAX_ENTRIES = 500

# tracking / smoothing
AZIMUTH_SUNRISE_DEG = 90.0
AZIMUTH_SUNSET_DEG = -90.0
SERVO_STEP_DEGREES = 2      # smaller = smoother but slower
SERVO_STEP_DELAY_MS = 15    # delay between each step

# csv logging
CSV_LOG_FILENAME = "solar_tracker_log.csv"