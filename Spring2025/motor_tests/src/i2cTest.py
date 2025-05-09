"""
I2C Device Detection Test

This script tests the I2C connection to a PCA9685 PWM controller board.
It initializes the I2C bus and attempts to connect to the PCA9685 at its
default address (0x40). If successful, it prints a confirmation message.

Requirements:
    - adafruit_pca9685 library
    - board library
    - busio library
    - PCA9685 PWM controller connected via I2C

Usage:
    Run this script to verify I2C communication with the PCA9685.
    A success message will be printed if the connection is established.
"""
import board
import busio
from adafruit_pca9685 import PCA9685

# Initialize I2C (NO address argument here)
i2c = busio.I2C(board.SCL, board.SDA)  

# Initialize PCA9685 with the correct I2C address
#pca = PCA9685(i2c, address=0x70)  # Use 0x70 if that's what i2cdetect shows
pca = PCA9685(i2c)  # Use 0x70 if that's what i2cdetect shows

print("PCA9685 detected at 0x40!")