import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("Prosthetic Guitar Simulator")

# Load the background image
bg_image_path = "/home/teambig/capstone/Prosthetic_Guitar_Simulator_Spring2025/Spring2025/finger_sim/finger-simulation/assets/robotGuitarist.jpeg"
bg_image = Image.open(bg_image_path)
bg_photo = ImageTk.PhotoImage(bg_image)

# Set the window size to the size of the background image
root.geometry(f"{bg_photo.width()}x{bg_photo.height()}")

# Create a canvas to place the background image
canvas = tk.Canvas(root, width=bg_photo.width(), height=bg_photo.height())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Create a frame for the controls
frame = tk.Frame(root, bg='#34ACCF')
frame.place(x=100, y=150, width=400, height=150)

# String dropdown
string_label = tk.Label(frame, text="String:")
string_label.pack(anchor="w")
string_var = tk.StringVar()
string_dropdown = ttk.Combobox(frame, textvariable=string_var)
string_dropdown['values'] = ("0 - open", "1 - E", "2 - B", "3 - G", "4 - D", "5 - A", "6 - E")
string_dropdown.pack(anchor="w")

# Duration entry
duration_label = tk.Label(frame, text="Duration (s):")
duration_label.pack(anchor="w")
duration_entry = tk.Entry(frame)
duration_entry.pack(anchor="w")

# Buttons
start_button = tk.Button(frame, text="Start")
start_button.pack(side="left", padx=5, pady=5)

stop_button = tk.Button(frame, text="Stop")
stop_button.pack(side="left", padx=5, pady=5)

demo_button = tk.Button(frame, text="Demo Mode")
demo_button.pack(side="left", padx=5, pady=5)

# Run the application
root.mainloop()
