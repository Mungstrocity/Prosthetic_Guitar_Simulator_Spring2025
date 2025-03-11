from gpiozero import PWMOutputDevice, DigitalOutputDevice
import time
import math

# Define GPIO Pins (BCM mode)
IN1 = 17  # Motor direction
IN2 = 27  # Motor direction
ENA = 18  # Motor speed (PWM)

ENC_A = 23  # Encoder A signal
ENC_B = 24  # Encoder B signal

FREQ = 5000  # PWM frequency

# Initialize GPIO devices
in1 = DigitalOutputDevice(IN1)
in2 = DigitalOutputDevice(IN2)
ena = PWMOutputDevice(ENA, frequency = FREQ)

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

# Encoder Reading
encoder_count = 0
last_time = time.time()

def read_encoder():
    """Read encoder and display raw values for debugging."""
    global encoder_count, last_time

    enc_a_state = GPIO.input(ENC_A)
    enc_b_state = GPIO.input(ENC_B)

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

speed_loc = 0

# Main Loop
try:
    print("Motor control and encoder feedback running. Press Ctrl+C to stop.")
    
    # Start motor
    while True:
        state = "forward"
        
        while state == "forward":
            while speed_loc <= 1:
                print(f'Speed: {speed_loc}')
                motor_forward(speed_loc)  # Set speed
                time.sleep(2)
                speed_loc += 0.25
                
        # if speed_loc == 1:
            speed_loc = 0
            state = "backward"
        
        while state == "backward":
            while speed_loc < 1:
                print(f'Speed: {speed_loc}')
                motor_backward(speed_loc)  # Set speed
                time.sleep(2)
                speed_loc += 0.25
                
        # if speed_loc == 1:
            speed_loc = 0
            state = "forward"
            
        


except KeyboardInterrupt:
    print("\nStopping motor and cleaning up.")
    stop_motor()