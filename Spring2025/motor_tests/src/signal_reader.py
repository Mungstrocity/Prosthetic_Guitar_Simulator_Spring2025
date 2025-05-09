from gpiozero import DigitalInputDevice
import time
"""Attempt to read motor signals on raspberry pi GPIO pins."""

# Pin configuration
MOTOR_SIGNAL_PIN_1 = 23  # GPIO pin for motor signal 1
MOTOR_SIGNAL_PIN_2 = 24  # GPIO pin for motor signal 2

# GPIO setup
signal_1 = DigitalInputDevice(MOTOR_SIGNAL_PIN_1)
signal_2 = DigitalInputDevice(MOTOR_SIGNAL_PIN_2)

def read_motor_signals():
    """Read the motor signals and print their values."""
    try:
        while True:
            signal_1_state = signal_1.value
            signal_2_state = signal_2.value
            print(f"Signal 1: {signal_1_state}, Signal 2: {signal_2_state}")
    except KeyboardInterrupt:
        print("Signal reading stopped by user.")

if __name__ == "__main__":
    read_motor_signals()