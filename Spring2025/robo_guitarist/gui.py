import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow for image handling
import os
import subprocess

BASE_DIR = os.path.dirname(__file__)

def gui_launch():
    root = tk.Tk()
    root.title("Robo Guitarist")
    root.geometry("1024x576")  # Set the window size

    def on_exit_click():
        root.destroy()  # Close the GUI
        nonlocal state
        state = "exit"

    def on_window_close():
        root.destroy()  # Close the GUI
        nonlocal state
        state = "exit"

    state = "running"
    root.protocol("WM_DELETE_WINDOW", on_window_close)  # Handle window close event

    # IMAGE HANDLING
    # Load the background image
    bg_image_path = os.path.join(BASE_DIR, "assets", "images", "GUI3.png")
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((1024, 576), Image.LANCZOS)  # Use LANCZOS directly from Image
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a Label to display the background image
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Stretch to cover the entire window

    # Ensure the image reference is not garbage collected
    bg_label.image = bg_photo

    # Create a parent frame for all controls on the left
    controls_frame = tk.Frame(root, padx=10, pady=10)
    controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20, anchor="n")  # Align to the left

    # BUTTONS IN A LABELED BOX
    button_frame = tk.LabelFrame(controls_frame, text="Select a string", padx=10, pady=10)
    button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)  # Stack at the top

    def on_button_click(button_id):
        messagebox.showinfo("Button Clicked", f"Button {button_id} clicked!")

    # Add the "Open" button in the first row
    open_button = tk.Button(button_frame, text="Open", command=lambda: on_button_click("Open"))
    open_button.grid(row=0, column=0, columnspan=7, pady=5, sticky="w")  # Span across all columns

    # Add buttons 1 to 6 in the second row
    for i in range(1, 7):  # Create buttons 1 to 6
        button = tk.Button(button_frame, text=str(i), command=lambda i=i: on_button_click(i))
        button.grid(row=1, column=i-1, padx=5, pady=5, sticky="w")  # Align buttons to the left

    # DURATION FIELD
    duration_frame = tk.Frame(controls_frame)
    duration_frame.pack(side=tk.TOP, fill=tk.X, pady=10)  # Stack below the button frame

    tk.Label(duration_frame, text="Duration (seconds):").pack(side=tk.LEFT, padx=5)

    duration_var = tk.StringVar()
    duration_entry = tk.Entry(duration_frame, textvariable=duration_var)
    duration_entry.pack(side=tk.LEFT, padx=5)

    def on_duration_submit():
        try:
            duration = float(duration_var.get())
            messagebox.showinfo("Duration Submitted", f"Duration set to {duration} seconds!")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid float value for duration.")

    submit_button = tk.Button(duration_frame, text="Submit", command=on_duration_submit)
    submit_button.pack(side=tk.LEFT, padx=5)

    # RANDOM MODE BUTTON
    def on_random_mode_click():
        messagebox.showinfo("Random Mode", "Random Mode activated!")

    random_mode_button = tk.Button(controls_frame, text="Random Mode", command=on_random_mode_click)
    random_mode_button.pack(side=tk.TOP, pady=10, anchor="w")  # Align to the left below the duration field

    # EXIT BUTTON
    button_exit = tk.Button(root, text="Exit", command=on_exit_click)
    button_exit.place(relx=0.02, rely=0.95, anchor="sw")  # Position at bottom left

    root.mainloop()
    
    return state


if __name__ == "__main__":
    # Launch the GUI and capture its state
    gui_state = gui_launch()

    # If the GUI exits with "exit", run roboGuitar.py
    if gui_state == "exit":
        current_dir = os.path.dirname(__file__)
        main_path = os.path.join(current_dir, "roboGuitar.py")
        subprocess.run(["python", main_path])