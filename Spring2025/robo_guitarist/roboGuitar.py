import tkinter as tk
from tkinter import messagebox
from gui import gui_launch
from finger_control import fret_note
from angles import get_angles
import random
import sys

def main():
    random_flag = False  # Define random_flag as a local variable

    def handle_gui_data(state, string_num, duration):
        nonlocal random_flag  # Access the local random_flag variable
        print(f"roboGuitar, {state}, {string_num}, {duration}")  # Debugging output

        if state == "exit":
            print("Exiting application.")
            sys.exit(0)
        elif state == "get_angles":
            print(f"roboGuitar, {state}, {string_num}")  # Debugging output
            state, angles = get_angles(string_num, 1)
            print(f"roboGuitar, {state}, {angles}")  # Debugging output
            state = fret_note(angles, duration)
        elif state == "random":
            random_flag = True
            while random_flag:
                string_num = random.randint(0, 6)
                print(f"roboGuitar-random, {state}, {string_num}, {duration}")  # Debugging output
                angles = get_angles(string_num, fret_number=1)
                fret_note("angles acquired", angles, duration, finger=1)
                print(f"roboGuitar-random, angles acquired, {angles}")
                if random_flag == False:
                    break

    # Launch the GUI and pass the callback
    gui_launch(random_flag=False, on_data_submit=handle_gui_data)

if __name__ == "__main__":
    main()