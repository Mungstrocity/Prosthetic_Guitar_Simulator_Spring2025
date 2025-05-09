"""
Pressure sensing module for the robotic guitarist.

This module interfaces with pressure sensors via an ADS1115 analog-to-digital
converter to measure the pressure applied by the robot's fingers on the guitar strings.
It provides functions to read and interpret pressure values to help optimize
finger positioning and force application.
"""

from i2c_shared import shared_i2c
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# Use the shared I2C bus
ads = ADS1115(shared_i2c)

# Create an analog input channel (e.g., channel 0)
#pressure_channel = AnalogIn(ads, ADS1115.P0)

#CHANGE THIS TO THE CORRECT VALUE

def read_pressure():
    """
    Read the pressure value from the ADS1115.

    Returns:
        float: The voltage corresponding to the pressure sensor.
    """
    #voltage = pressure_channel.voltage,
    voltage = 0.1
    return voltage