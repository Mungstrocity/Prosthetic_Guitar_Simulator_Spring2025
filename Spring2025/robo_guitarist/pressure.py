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