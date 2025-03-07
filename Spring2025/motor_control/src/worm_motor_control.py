import gpiod
import time

# Define GPIO Pins (BCM mode)
IN1 = 17  # Motor direction
IN2 = 27  # Motor direction
ENA = 18  # Motor speed (PWM)

ENC_A = 23  # Encoder A signal
ENC_B = 24  # Encoder B signal

# Open GPIO chip
chip = gpiod.Chip('gpiochip0')

# Request motor control pins as output
in1_line = chip.get_line(IN1)
in2_line = chip.get_line(IN2)
ena_line = chip.get_line(ENA)

in1_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)
in2_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)
ena_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)

# Request encoder lines as input
enc_a_line = chip.get_line(ENC_A)
enc_b_line = chip.get_line(ENC_B)

enc_a_line.request(consumer="encoder", type=gpiod.LINE_REQ_EV_BOTH_EDGES)
enc_b_line.request(consumer="encoder", type=gpiod.LINE_REQ_DIR_IN)

# Motor Control Functions
def motor_forward(speed=1):
    """Move motor forward at a given speed (0-1)."""
    in1_line.set_value(1)
    in2_line.set_value(0)
    ena_line.set_value(int(speed * 1))  # Enable motor (1 = Full power)

def motor_backward(speed=1):
    """Move motor backward at a given speed (0-1)."""
    in1_line.set_value(0)
    in2_line.set_value(1)
    ena_line.set_value(int(speed * 1))  # Enable motor (1 = Full power)

def stop_motor():
    """Stop motor."""
    ena_line.set_value(0)  # Disable motor

# Encoder Reading
encoder_count = 0
last_time = time.time()

def read_encoder():
    """Read encoder and display raw values for debugging."""
    global encoder_count, last_time

    event = enc_a_line.event_wait(sec=1)  # Wait for an event on ENC_A
    if event:
        enc_a_state = enc_a_line.get_value()
        enc_b_state = enc_b_line.get_value()

        # Quadrature decoding
        if enc_a_state == enc_b_state:
            encoder_count += 1  # Forward rotation
        else:
            encoder_count -= 1  # Reverse rotation

        current_time = time.time()
        time_diff = current_time - last_time
        last_time = current_time

        # Calculate RPM (assuming 20 pulses per revolution)
        if time_diff > 0:  # Avoid division by zero
            rpm = (encoder_count / 20) * (60 / time_diff)
        else:
            rpm = 0

        # Print raw encoder values and counts for debugging
        print(f"ENC_A: {enc_a_state}, ENC_B: {enc_b_state} | Count: {encoder_count}, RPM: {rpm:.2f}")

# Main Loop
try:
    print("Motor control and encoder feedback running. Press Ctrl+C to stop.")
    
    # Start motor
    motor_forward(speed=1)  # Full speed
    time.sleep(2)

    while True:
        read_encoder()

except KeyboardInterrupt:
    print("\nStopping motor and cleaning up.")
    stop_motor()
    chip.close()
