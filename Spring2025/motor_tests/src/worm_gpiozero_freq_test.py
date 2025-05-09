"""
PWM Frequency Test for DC Motor with Worm Gear

Testing optimal PWM frequency for the DC motor with worm gear.
We determined optimal frequencies are 1 kHz and 2kHz.
1 kHz is the considered the standard frequency for operation.
All other frequencies create inconsistent motion especially at lower
speeds.

This script allows for interactive testing of different PWM frequencies
to observe motor behavior and find the optimal settings.

Pin Configuration:
    - GPIO 17 (BCM): IN1 - Motor direction control
    - GPIO 27 (BCM): IN2 - Motor direction control
    - GPIO 18 (BCM): ENA - Motor speed control (PWM)
    - GPIO 23 (BCM): ENC_A - Encoder A signal (not used in this test)
    - GPIO 24 (BCM): ENC_B - Encoder B signal (not used in this test)

Usage:
    Run this script and input frequency values when prompted.
    Valid frequency range: 100 Hz to 10,000 Hz
    Press Ctrl+C to stop the test and clean up.
"""
from gpiozero import PWMOutputDevice, DigitalOutputDevice
import time
import math

# Define GPIO Pins (BCM mode)
IN1 = 17  # Motor direction
IN2 = 27  # Motor direction


ENC_A = 23  # Encoder A signal
ENC_B = 24  # Encoder B signal
ENA = 18

freq = 1000  # PWM frequency

# Initialize GPIO devices
in1 = DigitalOutputDevice(IN1)
in2 = DigitalOutputDevice(IN2)
ena = PWMOutputDevice(ENA, frequency=freq)

# Motor Control Functions
def motor_forward(speed):
    """Move motor forward at a given speed (0-1)."""
    in1.on()
    in2.off()
    ena.value = speed  # Set PWM duty cycle
    print(f'Forward {speed}')

def motor_backward(speed):
    """Move motor backward at a given speed (0-1)."""
    in1.off()
    in2.on()
    ena.value = speed  # Set PWM duty cycle
    print(f'Backward {speed}')

def stop_motor():
    """Stop motor."""
    ena.value = 0  # Disable motor



# Main Loop
try:
    print("Motor control and encoder feedback running. Press Ctrl+C to stop.")
    
    # Start motor
    while True:
        direction = int(input("enter frequency: "))
        if direction >= 100 and direction <= 10000:
            freq = direction
            ena.close()
            ena = PWMOutputDevice(ENA, frequency = freq)
            print(f'freq: {freq}')
            motor_backward(0.15)
            time.sleep(0.15)

    
        


except KeyboardInterrupt:
    print("\nStopping motor and cleaning up.")
    stop_motor()