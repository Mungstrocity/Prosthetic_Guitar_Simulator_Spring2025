import serial

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

def send_command(speed, duration):
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
        cmd = f"{speed} {duration}\n"
        print(f"[PI] Sending: {cmd.strip()}")
        ser.write(cmd.encode())

        while True:
            try:
                line = ser.readline()
                if not line:
                    continue  # just wait for more input

                decoded = line.decode().strip()
                if decoded:
                    print(f"[PICO] {decoded}")

                if decoded.startswith("[PICO] DONE") or "ERROR" in decoded:
                    break
            except UnicodeDecodeError:
                print(f"[PICO] [RAW] {repr(line)}")

def main():
    print("Motor Command Server Ready.")
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == "exit":
                break

            parts = user_input.split()
            if len(parts) != 2:
                print("ERR: Enter two numbers: <speed> <duration>")
                continue

            speed = float(parts[0])
            duration = float(parts[1])
            send_command(speed, duration)

        except KeyboardInterrupt:
            break
        except ValueError:
            print("ERR: Invalid numeric input")

if __name__ == "__main__":
    main()