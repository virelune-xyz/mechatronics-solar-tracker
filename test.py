import machine
import time

# Set up Pin 26 (ADC0) to listen to the battery spy wire
battery_adc = machine.ADC(0) 

# Conversion factor for standard 3.3V Pico pin reading 16-bit values
conversion_factor = 3.3 / 65535

while True:
    # Read the raw sensor value
    raw_value = battery_adc.read_u16()
    
    # Calculate the true battery voltage
    battery_voltage = raw_value * conversion_factor
    
    print(f"True Battery Voltage: {battery_voltage:.2f} V")
    
    # Simple alert if the battery is running low
    if battery_voltage < 3.4:
        print("⚠️ Warning: Battery is low!")
        
    time.sleep(2)