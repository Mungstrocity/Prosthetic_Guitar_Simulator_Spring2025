"""
Worm Gear Motor Control Test

This script provides control for a DC motor with worm gear using PWM for speed control
and digital output pins for direction control. The motor runs at full speed in the forward
direction when executed.

Pin Configuration:
    - PWM Pin: GPIO 26 (physical pin 37) - Controls motor speed
    - Direction Pin A: GPIO 5 (physical pin 29) - Forward direction when high
    - Direction Pin B: GPIO 6 (physical pin 31) - Reverse direction when high

Requirements:
    - gpiozero library
    - DC motor with H-bridge or motor driver connected to specified GPIO pins

Usage:
    Run this script to start the motor at full speed in forward direction.
    Press Ctrl+C to stop the motor and clean up GPIO pins.
"""
from gpiozero import PWMOutputDevice, DigitalOutputDevice
import time

# Pin configuration
MOTOR_PWM_PIN = 26  # physical pin 37

# Direction control
MOTOR_DIRECTION_PIN_A = 5  # physical pin 29
MOTOR_DIRECTION_PIN_B = 6  # physical pin 31

# GPIO setup
pwm = PWMOutputDevice(MOTOR_PWM_PIN, frequency=1000)  # Set frequency to 1 kHz
direction_a = DigitalOutputDevice(MOTOR_DIRECTION_PIN_A)
direction_b = DigitalOutputDevice(MOTOR_DIRECTION_PIN_B)

def set_motor_speed(duty_cycle):
    """Set the motor speed by adjusting the PWM duty cycle."""
    pwm.value = duty_cycle / 100.0

def set_motor_direction(forward):
    """Set the motor direction.
    Args:
        forward (bool): True for forward, False for backward.
    """
    if forward:
        direction_a.on()
        direction_b.off()
    else:
        direction_a.off()
        direction_b.on()

if __name__ == "__main__":
    try:
        print("Starting motor control...")
        set_motor_direction(True)  # Set direction to forward
        set_motor_speed(100)  # Run motor at 100% duty cycle
        while True:
            time.sleep(1)  # Keep the motor running
    except KeyboardInterrupt:
        print("Motor control stopped by user.")
    finally:
        pwm.close()
        direction_a.close()
        direction_b.close()