# Self-Sustaining Dual-Axis Solar Tracker
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
📁 Solar_Tracker_Project/
├── 📄 .micropico/               <-- Local VS Code workspace configuration
├── 📄 main.py                   <-- Root boot file (Required by the Pico firmware)
├── 📄 config.py                 <-- All custom modules and configurations
├── 📄 README.md                 <-- Markdown file with the information about the project.
├── 📄 system_controller.py      <-- Main layer to wire all classes and objects together
├── 📁 comms/                    <-- Communications / Transmitters
    ├── 📄 data_transmitter.py   
    └── 📄 serial_transmitter.py 
├── 📁 inputs/  
    └── 📄 inputs.py             <-- OOP Class handling data saving to CSV
├── 📁 logs/                     <-- Creates a store of the data required.
    └── 📄 datta_logger.py 
├── 📁 models/                   <-- Individual Reading Objects
    └── 📄 sensor_reading.py
├── 📁 outputs/                  <-- Output devices files
    ├── 📄 oled_display.py   
    └── 📄 outputs.py 
├── 📁 sensors/                  <-- Files for the individual input sensors.
    ├── 📄 clock_module.py   
    ├── 📄 environmental_sensor.py   
    └── 📄 sensor.py 
├── 📁 tracking/                 <-- Files responsible to handle the calculation of the sun position and the servo motors.
    ├── 📄 servo_motor.py   
    ├── 📄 single_axis_tracker.py   
    └── 📄 sun_position_calculator.py 

```


# File Organisation
## Directory - Input Sensors (/sensors/):
    Clock Module:
    Environmental Sensor: 
    Sensor: It is an abstract base class for all input/sensing hardware. 

## Directory: Communications / Transmitters (/comms/)
    Data Transmitter: It is an abstract base for communications
    Serial Transmitter: It sends SensorReadings out over usb formatted as CSV rows

## Directory: Outputs (/output/)
    OLED Display:
    Outputs: It is a marker superclass which does nothing :/

## Directory: Tracking (/tracking/)

[//]: # ( The class in Servo Motors assumes there is only one servo motor. This is fixed in the Single Axis Tracker file. )

    Servo Motors: Class for Servo Motors 
    Single Axis Tracker: It moves two servomotors to keep them angled towards sun
    Sun Position Calculator: When it recieves a timestamp and a fixed site location colculate suns position.

## Single File Directories:
    Inputs (/inputs/inputs.py): A marker superclass for all inputs.

    Logs (/logs/data_logger.py): An in-memory store of recent sensorreadings, used for the on-device history.

    Models (/models/sensor_reading.py): It is a Data Container

---

## Project Management Methodology
We use a **WAgile (Waterfall + Agile)** approach to balance scheduling predictability with hardware development flexibility.

* **Waterfall Phases:** Applied to sequential, highly predictable project milestones (e.g., scoping, part procurement, final documentation, and reflections). This prevents overspending before development begins.
* **Agile Phases:** Applied to the development and testing phases. Because hardware bugs and software errors can be unpredictable, overlapping these phases allows for iterative prototyping and continuous integration.
* **Buffer Period:** A two-week holiday buffer ensures adequate planning and design work are complete before parts arrive for assembly.