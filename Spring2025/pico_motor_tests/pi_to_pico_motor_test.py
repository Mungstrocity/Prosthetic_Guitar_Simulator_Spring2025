"""
Simple motor test script for controlling a Raspberry Pico via serial connection.

This script establishes a serial connection with a Raspberry Pico microcontroller,
sends a command to run a motor at 70% speed forward for 5 seconds, and then sends
a stop command. It demonstrates basic serial communication and motor control.

Note: This script assumes the Pico is connected at /dev/ttyACM0 on Linux.
For Windows, the port should be changed to a COM port (e.g., 'COM3').
"""
import serial
import time

# Open the serial connection to the Pico
# Check that /dev/ttyACM0 is correct (run `ls /dev/ttyACM*` to confirm)
with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as pico:
    #time.sleep(2)  # Wait for Pico to finish rebooting

    # Send run command (70% speed forward)
    pico.write(b'run 0.7\n')
    print("Sent: run 0.7")

    # Let it run for 5 seconds
    time.sleep(5)

    # Send stop command
    pico.write(b'stop\n')
    print("Sent: stop")
