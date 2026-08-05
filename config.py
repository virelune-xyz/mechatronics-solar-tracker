"""
just used for pin assignments and stuff like that so theres a nicer way to change things on the fly
"""

# i2c bus (clock, envsensor, oled)
I2C_ID = None          # eg 0
I2C_SDA_PIN = None     # eg 0  (GPIO0)
I2C_SCL_PIN = None
I2C_FREQ_HZ = 400_000

# servo signal pins
SERVO_1_PIN = None     # eg 2  (GPIO2)
SERVO_2_PIN = None 
SERVO_MIN_ANGLE = 0
SERVO_MAX_ANGLE = 180

# battery voltage sense (through the resistor divider)
BATTERY_ADC_PIN = None         # eg 26 (GPIO26)
BATTERY_DIVIDER_RATIO = 2.0    # undoes the divider

# serial transmitter
SERIAL_BAUDRATE = 115200

# site location for the calculator
SITE_LATITUDE = None
SITE_LONGITUDE = None
SITE_UTC_OFFSET = None

# system
UPDATE_INTERVAL_SEC = 60
DATA_LOGGER_MAX_ENTRIES = 500
