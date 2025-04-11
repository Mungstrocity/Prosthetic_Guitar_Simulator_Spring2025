from gpiozero import PWMOutputDevice, DigitalOutputDevice, DigitalInputDevice
import time
import math
import threading
from queue import Queue

# Define GPIO Pins (BCM mode)
IN1 = 17  # Motor direction
IN2 = 27  # Motor direction
ENA = 18  # Motor speed (PWM)

ENC_A = 23  # Encoder A signal
ENC_B = 24  # Encoder B signal

FREQ = 1000  # PWM frequency

# Initialize GPIO devices
in1 = DigitalOutputDevice(IN1)
in2 = DigitalOutputDevice(IN2)
ena = PWMOutputDevice(ENA, frequency = FREQ)

direction = "forward"

# Initialize a queue for encoder updates
encoder_queue = Queue()

# Initialize encoder input devices
enc_a_state = DigitalInputDevice(ENC_A)
enc_b_state = DigitalInputDevice(ENC_B)

# Define callback functions for encoder pin changes
def enc_a_changed():
    process_encoder_change()

def enc_b_changed():
    process_encoder_change()

def process_encoder_change():
    global enc_prev, enc_count
    enc = [enc_a_state.value, enc_b_state.value]
    if enc != enc_prev:
        is_valid = 1 if tuple(enc) in VALID_TRANSITIONS.get(tuple(enc_prev), []) else 0
        enc_prev = enc
        enc_count += 1  # Increment count on state change
        encoder_queue.put(enc)  # Add the new state to the queue
        print(f"Direction: {state}, Encoder: {enc}, Count: {enc_count}, Valid: {is_valid}")

# Attach callbacks to encoder pins
enc_a_state.when_activated = enc_a_changed
enc_a_state.when_deactivated = enc_a_changed
enc_b_state.when_activated = enc_b_changed
enc_b_state.when_deactivated = enc_b_changed

# In another part of the program, process the queue
def process_encoder_updates():
    while True:
        if not encoder_queue.empty():
            enc = encoder_queue.get()
            #print(f"Processed Encoder State: {enc}")

# Motor control thread
def motor_control():
    global state, speed_loc, enc_count
    while True:
        if state == "forward":
            enc_count = 0  # Reset count when direction changes
            while speed_loc <= 1:
                motor_forward(speed_loc)  # Set speed
                #print(f"Direction: {state}, Encoder: {read_encoder()}, Count: {enc_count}")
                time.sleep(0.5)  # Motor control delay
                speed_loc += 0.25
            speed_loc = 0
            state = "backward"

        elif state == "backward":
            enc_count = 0  # Reset count when direction changes
            while speed_loc <= 1:
                motor_backward(speed_loc)  # Set speed
                #print(f"Direction: {state}, Encoder: {read_encoder()}, Count: {enc_count}")
                time.sleep(0.5)  # Motor control delay
                speed_loc += 0.25
            speed_loc = 0
            state = "forward"

# Motor Control Functions
def motor_forward(speed):
    in1.on()
    in2.off()
    ena.value = speed  # Set PWM duty cycle
    #print(f'Forward {speed}')

def motor_backward(speed):
    """Move motor backward at a given speed (0-1)."""
    in1.off()
    in2.on()
    ena.value = speed  # Set PWM duty cycle
    #print(f'Backward {speed}')

def stop_motor():
    """Stop motor."""
    ena.value = 0  # Disable motor

# Encoder Reading
encoder_count = 0
last_time = time.time()

def read_encoder():
    """Read encoder and display raw values for debugging."""
    global encoder_count, last_time


    enc = [enc_a_state.value, enc_b_state.value]
    
    return enc

    # Quadrature decoding
    # if enc_a_state == enc_b_state:
    #     encoder_count += 1  # Forward rotation
    # else:
    #     encoder_count -= 1  # Reverse rotation
    


    current_time = time.time()
    time_diff = current_time - last_time
    last_time = current_time

    # Calculate RPM (assuming 20 pulses per revolution)
    if time_diff > 0:  # Avoid division by zero
        rpm = (encoder_count / 20) * (60 / time_diff)
    else:
        rpm = 0

    # Print raw encoder values and counts for debugging
    #print(f"ENC_A: {enc_a_state}, ENC_B: {enc_b_state} | Count: {encoder_count}, RPM: {rpm:.2f}")

# Encoder Reading Thread
def read_encoder_continuously():
    """Continuously read encoder values and print them."""
    while True:
        enc = [enc_a_state.value, enc_b_state.value]
        #print(f"Encoder Values: {enc}")
        time.sleep(0.001)  # Small delay to avoid excessive CPU usage

# Function to monitor missed encoder changes
def monitor_missed_changes():
    """Compare actual encoder count with expected count to detect missed changes."""
    global enc_count
    pulses_per_revolution = 20  # Adjust based on encoder specification
    while True:
        # Calculate expected count based on motor speed and time
        motor_rpm = ena.value * 100  # Example: scale PWM value to RPM
        expected_count = round((motor_rpm / 60) * pulses_per_revolution * 0.5)  # Round to nearest integer
        missed_changes = abs(expected_count - enc_count)
        print(f"Expected Count: {expected_count}, Actual Count: {enc_count}, Missed Changes: {missed_changes}")
        time.sleep(0.5)  # Check every 0.5 seconds

# Define valid state transitions for the encoder
VALID_TRANSITIONS = {
    (0, 0): [(0, 1), (1, 0)],
    (0, 1): [(1, 1), (0, 0)],
    (1, 0): [(1, 1), (0, 0)],
    (1, 1): [(0, 1), (1, 0)],
}

# Function to monitor skipped transitions
def monitor_skipped_transitions():
    """Detect skipped transitions in encoder states."""
    global enc_prev
    while True:
        enc = [enc_a_state.value, enc_b_state.value]
        if enc != enc_prev:
           # if tuple(enc) not in VALID_TRANSITIONS.get(tuple(enc_prev), []):
                #print(f"Skipped Transition Detected: {enc_prev} -> {enc}")
            enc_prev = enc
        time.sleep(0.001)  # Small delay to avoid excessive CPU usage

# Main program
try:
    print("Motor control and encoder feedback running. Press Ctrl+C to stop.")
    
    # Initialize variables
    enc_prev = [0, 0]
    enc_count = 0
    state = "forward"
    speed_loc = 0

    # Create and start threads
    motor_thread = threading.Thread(target=motor_control, daemon=True)
    process_thread = threading.Thread(target=process_encoder_updates, daemon=True)
    encoder_thread = threading.Thread(target=read_encoder_continuously, daemon=True)
    skip_monitor_thread = threading.Thread(target=monitor_skipped_transitions, daemon=True)

    motor_thread.start()
    process_thread.start()
    encoder_thread.start()
    skip_monitor_thread.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping motor and cleaning up.")
    stop_motor()