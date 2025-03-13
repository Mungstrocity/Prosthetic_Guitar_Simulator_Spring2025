from gpiozero import PWMOutputDevice, DigitalOutputDevice
import time
import math

# Define GPIO Pins (BCM mode)
IN1 = 17  # Motor direction
IN2 = 27  # Motor direction


ENC_A = 23  # Encoder A signal
ENC_B = 24  # Encoder B signal
ENA = 18

freq = 100  # PWM frequency

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
            motor_backward(0.25)
            time.sleep(0.25)

    
        


except KeyboardInterrupt:
    print("\nStopping motor and cleaning up.")
    stop_motor()