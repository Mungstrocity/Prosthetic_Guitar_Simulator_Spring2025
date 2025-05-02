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
