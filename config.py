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
UPDATE_INTERVAL_SEC = 60
DATA_LOGGER_MAX_ENTRIES = 500
