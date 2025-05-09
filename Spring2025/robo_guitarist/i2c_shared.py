"""
Shared I2C bus module for the robotic guitarist.

This module provides a single shared I2C bus that can be imported and used
by multiple modules in the robotic guitarist system. This ensures that all
I2C communications use the same bus instance, preventing conflicts between
different components requiring I2C access.
"""

import board
import busio

# Initialize the I2C bus
shared_i2c = busio.I2C(board.SCL, board.SDA)