"""
Count-Based Pulse Motor Control with Encoder Feedback

This script provides precise control for a DC motor with worm gear by using encoder 
count-based pulses. It enables the motor to move an exact number of encoder counts,
making it suitable for precise positioning applications. The script also logs encoder
data and motor parameters to a timestamped CSV file for analysis.

Hardware Configuration:
    Motor to Driver Board:
    - M1 and M2: Connected to Out1 and Out2 on driver board
    - GND: Connected to driver board GND (NOT Raspberry Pi GND)
    - VCC: Connected to driver board VCC (NOT Raspberry Pi VCC)

    Raspberry Pi to Driver Board:
    - GPIO 17 (BCM) / Pin 11: IN1 on driver board - Direction control 
    - GPIO 27 (BCM) / Pin 13: IN2 on driver board - Direction control
    - GPIO 18 (BCM) / Pin 12: ENA on driver board - PWM speed control

    Motor Encoder to Raspberry Pi:
    - A signal: GPIO 23 (BCM) / Pin 16 - Encoder channel A
    - B signal: GPIO 24 (BCM) / Pin 18 - Encoder channel B

Features:
    - Interactive control of motor speed and pulse length
    - Precise positioning based on encoder count
    - PWM motor speed control with 1 kHz frequency
    - Real-time encoder feedback monitoring
    - Automatic CSV data logging with timestamps in filename
    - Simple interrupt-based encoder counting

Usage:
    1. Run the script
    2. Enter motor speed (0.0-1.0) when prompted
    3. Enter pulse length (number of encoder counts) when prompted
    4. The motor will run until it reaches the specified encoder count
    5. Press Ctrl+C to stop the program

Data Logging:
    Data is logged to a CSV file with the following columns:
    - A: Encoder A signal value (0 or 1)
    - B: Encoder B signal value (0 or 1)
    - Count: Current encoder count
    - Speed: Motor speed setting (0.0-1.0)
    - Direction: Motor direction ("forward" or "backward")
"""
# filepath: /home/teambig/capstone/Prosthetic_Guitar_Simulator_Spring2025/Spring2025/motor_tests/src/worm_gpiozero_interrupt.py
from gpiozero import PWMOutputDevice, DigitalOutputDevice, DigitalInputDevice
import time
import threading
import csv
from datetime import datetime
import os



# Define GPIO Pins (BCM mode)
IN1 = 17  # Motor direction. Physical pin 11
IN2 = 27  # Motor direction. Physical pin 13
ENA = 18  # Motor speed (PWM) Physical pin 12

ENC_A = 23  # Encoder A signal. Physical pin 16
ENC_B = 24  # Encoder B signal. Physical pin 18

FREQ = 1000  # PWM frequency

# Optimal frequency is 1 kHz or 2 kHz for this motor

# MOTOR TO DRIVER BOARD CONNECTIONS
# M1 and M1 : Out1 and Out2 on Driver board
# GND : GND on Driver board NOT ON RASPBERRY PI
# VCC : VCC on Driver board NOT ON RASPBERRY PI

# PI TO DRIVER BOARD CONNECTIONS
# IN1 and IN2 : IN1 and IN2 on Driver board
# ENA : ENA on Driver board

# MOTOR TO PI CONNECTIONS
# A and B : ENC_A and ENC_B on Rasbperry Pi
# When connected, a green LED will light solid on the motor on the side opposite
# the wire connections. This indicates that the motor is receiving power.

# Initialize GPIO devices
in1 = DigitalOutputDevice(IN1)
in2 = DigitalOutputDevice(IN2)
ena = PWMOutputDevice(ENA, frequency=FREQ)

enc_a_state = DigitalInputDevice(ENC_A)
enc_b_state = DigitalInputDevice(ENC_B)

# Initialize variables
enc_prev = [0, 0]
enc_count = 0

# Ensure the encoder count only increments when the value changes to 1
prev_enc_a_state = 0  # Track the previous state of ENC_A

# Define CSV file path
BASE_DIR = os.path.dirname(__file__)

CSV_FILE = os.path.join(BASE_DIR, f'encoder_data_count_based_pulse_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

# Update CSV file header to remove Pulse Count and keep only Change Count
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["A", "B", "Count", "Speed", "Direction"])  # Updated header

# Optimized encoder interrupt handler for high-speed signal processing
# Removed unnecessary logic to ensure real-time performance

def handle_encoder_change():
    global enc_count
    enc_count += 1  # Increment count on every signal change without additional checks
    print(enc_count)

# Attach interrupts to encoder pins
enc_a_state.when_activated = handle_encoder_change()
enc_a_state.when_deactivated = handle_encoder_change()

# Motor control functions
def motor_forward(speed):
    in1.on()
    in2.off()
    ena.value = speed

def motor_backward(speed):
    in1.off()
    in2.on()
    ena.value = speed

def stop_motor():
    ena.value = 0

debounce_time = 0.0000001  # Debounce time in seconds

# Simplify the logic to count encoder signals directly without additional math
# Remove gear ratio and output CPR calculations
GEAR_RATIO = 1  # No gear ratio adjustment needed for direct counts
HALL_FEEDBACK_RESOLUTION = 1  # Directly count encoder signals

# Main program
def motor_control():
    global enc_count
    # Initialize pulse_count at the start of the motor_control function
    pulse_count = 0  # Start pulse count at 1

    while True:
        # Prompt for initial speed and pulse length
        speed = float(input("Enter motor speed (0.0 to 1.0): "))
        pulse_length = int(input("Enter pulse length (number of counts): "))
        
        while True:
            # Ensure the encoder count resets to 0 for each pulse
            enc_count = 0  # Reset encoder count at the start of each pulse

            while enc_count < pulse_length:
                motor_forward(speed)  # Run motor forward at the specified speed
                time.sleep(debounce_time)  # Short sleep to allow real-time updates
                stop_motor()
                time.sleep(debounce_time)  # Short gap between checks

                # Log data to CSV
                with open(CSV_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        enc_a_state.value,  # Encoder A
                        enc_b_state.value,  # Encoder B
                        enc_count,          # Count
                        speed,              # Speed
                        "forward"           # Direction
                    ])

            # Pause for 0.5 seconds before starting the next pulse
            time.sleep(0.5)

try:
    print("Motor control and encoder feedback running. Press Ctrl+C to stop.")

    # Start motor control
    motor_control()

except KeyboardInterrupt:
    print("\nStopping motor and cleaning up.")
    stop_motor()