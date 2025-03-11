import board
import busio
from adafruit_pca9685 import PCA9685

# Initialize I2C (NO address argument here)
i2c = busio.I2C(board.SCL, board.SDA)  

# Initialize PCA9685 with the correct I2C address
#pca = PCA9685(i2c, address=0x70)  # Use 0x70 if that's what i2cdetect shows
pca = PCA9685(i2c)  # Use 0x70 if that's what i2cdetect shows

print("PCA9685 detected at 0x40!")