import board
import busio

# Initialize the I2C bus
shared_i2c = busio.I2C(board.SCL, board.SDA)