import serial

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

def send_command(command):
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
        print(f"[PI] Sending: {command}")
        ser.write((command + "\n").encode())

        while True:
            line = ser.readline().decode().strip()
            if not line:
                break
            print(f"[PICO] {line}")
            if line == "DONE":
                break

def main():
    print("Motor Command Server Ready.")
    while True:
        try:
            cmd = input("> ")
            if cmd.lower() == "exit":
                break
            send_command(cmd)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
