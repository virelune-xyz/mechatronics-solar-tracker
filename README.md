# Self-Sustaining Single-Axis Solar Tracker
A smart mechatronic prototype designed to maximize solar harvesting efficiency through real-time environmental monitoring and automated solar tracking.

## Overview
Traditional stationary solar panels lose up to 40% of their potential daily energy because they cannot adjust to the movement of the sun. 

Our solution is a **Self-Sustaining Solar Tracker**. This mechatronic prototype actively tilts every 20 minutes to maintain an optimal angle with the sun. Instead of discarding the tracking metrics, the system logs information into spreadsheets, charts, and graphs for deeper analysis.

## System Architecture & Inputs
The design focuses on simplicity, leveraging only two core input sensors to orchestrate tracking and data storage:

1. **Precision Real-Time Clock (RTC):** Establishes a time baseline to calculate where the sun should be positioned. It also provides highly accurate timestamps for data logging.
2. **BME280 Sensor:** Captures Ambient Temperature, Humidity, and Barometric Pressure. Because solar panels lose efficiency as temperatures rise, tracking thermal metrics helps monitor health and performance.

### User Interface & Data Export
* **Real-Time Monitoring:** A Blue OLED I2C Display provides live onsite stats.
* **Deep Data Analysis:** A built-in USB interface allows users to easily download log files directly to a PC or personal device.

---

# Project Structure

```text
📁 mechatronics-solar-tracker/
├── 📄 .gitignore                		<-- Git ignore rules
├── 📄 .micropico                		<-- Local VS Code workspace configuration
├── 📄 main.py                   		<-- Root boot file (Required by the Pico firmware)
├── 📄 config.py                 		<-- Pin assignments and system configuration
├── 📄 README.md                 		<-- Markdown file with project information
├── 📄 system_controller.py      		<-- Main orchestrator that wires all components together
├── 📄 test.py                   		<-- Manual servo motor testing utility
├── 📁 comms/                    		<-- Communications / Transmitters
│   ├── 📄 data_transmitter.py   		<-- Abstract base for communications
│   └── 📄 serial_transmitter.py 		<-- USB serial transmitter (dict/CSV output)
├── 📁 drivers/                  		<-- Hardware driver libraries
│   ├── 📄 bme280_float.py       		<-- BME280 environmental sensor driver
│   └── 📄 ssd1306.py            		<-- SSD1306 OLED display driver
├── 📁 inputs/                   		<-- Input device abstractions
│   └── 📄 inputs.py             		<-- Marker superclass for input devices
├── 📁 logs/                     		<-- Data logging and storage
│   └── 📄 data_logger.py        		<-- In-memory log of sensor readings
├── 📁 models/                   		<-- Data models and containers
│   └── 📄 sensor_reading.py     		<-- Timestamped sensor data container
├── 📁 outputs/                  		<-- Output device drivers
│   ├── 📄 oled_display.py       		<-- OLED display interface
│   └── 📄 outputs.py            		<-- Marker superclass for output devices
├── 📁 sensors/                  		<-- Input sensor drivers
│   ├── 📄 clock_module.py       		<-- DS3231 RTC driver
│   ├── 📄 environmental_sensor.py 		<-- BME280 sensor wrapper
│   └── 📄 sensor.py             		<-- Abstract base class for sensors
└── 📁 tracking/                 		<-- Sun tracking and motor control
    ├── 📄 servo_motor.py        		<-- PWM servo motor driver
    ├── 📄 single_axis_tracker.py 		<-- Dual servo tracker controller
    └── 📄 sun_position_calculator.py 	<-- Solar position calculations
```


# File Organisation

## Core Files
- **main.py**: Entry point that initializes all hardware components and starts the system controller
- **config.py**: Centralized configuration for pin assignments, I2C bus settings, and system parameters
- **system_controller.py**: Main orchestrator that coordinates sensor reading, sun tracking, display updates, logging, and data transmission in a continuous loop
- **test.py**: Utility for manual testing of servo motor movement and pin validation

## Directory: Communications (/comms/)
- **data_transmitter.py**: Abstract base class for transmission protocols
- **serial_transmitter.py**: USB serial transmitter that sends sensor readings as a dictionary/CSV rows

## Directory: Drivers (/drivers/)
- **bme280_float.py**: BME280 environmental sensor driver (third-party MicroPython library)
- **ssd1306.py**: SSD1306 OLED display driver (third-party MicroPython library)

## Directory: Inputs (/inputs/)
- **inputs.py**: Marker superclass for all input devices

## Directory: Logs (/logs/)
- **data_logger.py**: In-memory circular buffer for recent sensor readings (FIFO with configurable max entries)

## Directory: Models (/models/)
- **sensor_reading.py**: Timestamped container for sensor data with methods to export as dict or CSV

## Directory: Outputs (/outputs/)
- **outputs.py**: Marker superclass for all output devices
- **oled_display.py**: I2C OLED display interface that renders readings and messages

## Directory: Sensors (/sensors/)
- **sensor.py**: Abstract base class defining the interface for all sensor subclasses
- **clock_module.py**: DS3231 real-time clock driver providing timestamps for tracking and logging
- **environmental_sensor.py**: Wrapper around the BME280 driver that reads temperature, humidity, and pressure

## Directory: Tracking (/tracking/)
- **sun_position_calculator.py**: Calculates solar elevation and azimuth using Cooper's equation
- **servo_motor.py**: PWM-based servo motor driver with angle clamping; assumes single servo logic
- **single_axis_tracker.py**: Coordinates two servo motors to track the sun, with mirroring for opposite-side mounting

---

## Project Management Methodology
We use a **WAgile (Waterfall + Agile)** approach to balance scheduling predictability with hardware development flexibility.

* **Waterfall Phases:** Applied to sequential, highly predictable project milestones (e.g., scoping, part procurement, final documentation, and reflections). This prevents overspending before development begins.
* **Agile Phases:** Applied to the development and testing phases. Because hardware bugs and software errors can be unpredictable, overlapping these phases allows for iterative prototyping and continuous integration.
* **Buffer Period:** A two-week holiday buffer ensures adequate planning and design work are complete before parts arrive for assembly.
