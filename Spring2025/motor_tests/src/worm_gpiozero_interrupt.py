"""
Worm Gear Motor Control with Interrupt-Based Encoder Feedback

This script provides control for a DC motor with worm gear and implements
interrupt-based encoder feedback. It monitors encoder signals using GPIO interrupts,
logs encoder data to a CSV file, and controls motor direction and speed using PWM.

Hardware Configuration:
    Raspberry Pi to Motor Driver:
    - GPIO 17 (BCM) / Pin 11: IN1 - Direction control
    - GPIO 27 (BCM) / Pin 13: IN2 - Direction control
    - GPIO 18 (BCM) / Pin 12: ENA - PWM speed control

    Motor Encoder to Raspberry Pi:
    - GPIO 23 (BCM) / Pin 16: Encoder channel A
    - GPIO 24 (BCM) / Pin 18: Encoder channel B

Features:
    - PWM motor speed control at 1 kHz frequency
    - Interrupt-based encoder position tracking
    - Forward/backward direction control with increasing speed
    - Multi-threaded operation for simultaneous control and monitoring
    - CSV logging of encoder data with timestamps
    - Encoder transition validation

Usage:
    Run this script to start motor control that alternates between forward and
    backward rotation at varying speeds while monitoring and logging encoder data.
    Press Ctrl+C to stop the motor and clean up.

Data Logging:
    Encoder data is logged to a CSV file with the following columns:
    - Timestamp: ISO format timestamp when the encoder state changed
    - Encoder State: The current state of both encoder channels [A, B]
    - Count: Cumulative count of valid encoder transitions
"""
# filepath: /home/teambig/capstone/Prosthetic_Guitar_Simulator_Spring2025/Spring2025/motor_tests/src/worm_gpiozero_interrupt.py
from gpiozero import PWMOutputDevice, DigitalOutputDevice, DigitalInputDevice
import time
import threading
import csv
from datetime import datetime

# Define GPIO Pins (BCM mode)
IN1 = 17  # Motor direction. Physical pin 11
IN2 = 27  # Motor direction. Physical pin 13
ENA = 18  # Motor speed (PWM) Physical pin 12

ENC_A = 23  # Encoder A signal. Physical pin 16
ENC_B = 24  # Encoder B signal. Physical pin 18

FREQ = 1000  # PWM frequency

# Initialize GPIO devices
in1 = DigitalOutputDevice(IN1)
in2 = DigitalOutputDevice(IN2)
ena = PWMOutputDevice(ENA, frequency=FREQ)

enc_a_state = DigitalInputDevice(ENC_A)
enc_b_state = DigitalInputDevice(ENC_B)

# Initialize variables
enc_prev = [0, 0]
enc_count = 0
state = "forward"
speed_loc = 0

# Define valid state transitions for the encoder
VALID_TRANSITIONS = {
    (0, 0): [(0, 1), (1, 0)],
    (0, 1): [(1, 1), (0, 0)],
    (1, 0): [(1, 1), (0, 0)],
    (1, 1): [(0, 1), (1, 0)],
}

# Define CSV file path
CSV_FILE = "/home/teambig/capstone/Prosthetic_Guitar_Simulator_Spring2025/encoder_data.csv"

# Initialize CSV file
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Encoder State", "Count"])  # Write header

# Encoder interrupt handler
def handle_encoder_change():
    global enc_prev, enc_count
    enc = [enc_a_state.value, enc_b_state.value]
    if enc != enc_prev:
        if tuple(enc) in VALID_TRANSITIONS.get(tuple(enc_prev), []):
            enc_count += 1
        enc_prev = enc
        print(f"Encoder State: {enc}, Count: {enc_count}")

        # Write to CSV file
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().isoformat(), enc, enc_count])

# Attach interrupts to encoder pins
enc_a_state.when_activated = handle_encoder_change
enc_a_state.when_deactivated = handle_encoder_change
enc_b_state.when_activated = handle_encoder_change
enc_b_state.when_deactivated = handle_encoder_change

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

# Motor control thread
def motor_control():
    global state, speed_loc, enc_count
    while True:
        if state == "forward":
            enc_count = 0
            while speed_loc <= 1:
                motor_forward(speed_loc)
                time.sleep(0.5)
                speed_loc += 0.25
            speed_loc = 0
            state = "backward"

        elif state == "backward":
            enc_count = 0
            while speed_loc <= 1:
                motor_backward(speed_loc)
                time.sleep(0.5)
                speed_loc += 0.25
            speed_loc = 0
            state = "forward"

# Main program
try:
    print("Motor control and encoder feedback running. Press Ctrl+C to stop.")

    # Create and start motor control thread
    motor_thread = threading.Thread(target=motor_control, daemon=True)
    motor_thread.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping motor and cleaning up.")
    stop_motor()