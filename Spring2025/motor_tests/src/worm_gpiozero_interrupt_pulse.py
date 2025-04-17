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
# VALID_TRANSITIONS = {
#     (0, 0): [(0, 1), (1, 0)],
#     (0, 1): [(1, 1), (0, 0)],
#     (1, 0): [(1, 1), (0, 0)],
#     (1, 1): [(0, 1), (1, 0)],
# }

# Define CSV file path
CSV_FILE = "/home/teambig/capstone/Prosthetic_Guitar_Simulator_Spring2025/encoder_data.csv"

# Update CSV file header
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["A", "B", "Pulse Count", "Change Count", "Speed", "Direction"])  # Updated header

# Encoder interrupt handler
def handle_encoder_change():
    global enc_count
    # Only count rising edges of ENC_A
    if enc_a_state.value == 1:
        enc_count += 1

# Attach interrupts to encoder pins
enc_a_state.when_activated = handle_encoder_change

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
        pulse_count = 1
        while speed_loc <= 1:
            enc_count = 0  # Reset encoder count for each pulse
            for _ in range(5):  # Run 5 pulses
                if state == "forward":
                    motor_forward(speed_loc)
                elif state == "backward":
                    motor_backward(speed_loc)

                time.sleep(1)  # 1 second per pulse
                stop_motor()
                time.sleep(0.5)  # 0.5-second gap between pulses

                # Write pulse data to CSV
                with open(CSV_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        enc_a_state.value,  # Encoder A
                        enc_b_state.value,  # Encoder B
                        pulse_count,        # Pulse Count
                        enc_count,          # Change Count
                        speed_loc,          # Speed
                        state               # Direction
                    ])
                pulse_count += 1  # Increment pulse count
                enc_count = 0  # Reset encoder count for the next pulse

            speed_loc += 0.1  # Increment speed after 5 pulses
            pulse_count = 1  # Reset pulse count for the next speed level

        speed_loc = 0.1  # Reset speed for the next direction
        state = "backward" if state == "forward" else "forward"  # Reverse direction

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