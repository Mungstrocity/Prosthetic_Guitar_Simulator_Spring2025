import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

BASE_DIR = os.path.dirname(__file__)

# Global state variables
state_vars = {
    "state": "not_started",
    "selected_button": None,
    "duration": None,
    "string_num": None,
    "active_button": None,
}

# Button control functions
def on_button_click(button_id, button_widgets):
    global state_vars
    selected_button, active_button = state_vars["selected_button"], state_vars["active_button"]
    state_vars["selected_button"] = button_id

    if active_button:
        active_button.config(relief=tk.RAISED)

    state_vars["active_button"] = button_widgets[button_id]
    state_vars["active_button"].config(relief=tk.SUNKEN)

def on_duration_submit(duration_var):
    global state_vars
    try:
        duration_value = float(duration_var.get())
        if duration_value > 0 and state_vars["selected_button"] is not None:
            state_vars["string_num"], state_vars["duration"] = state_vars["selected_button"], duration_value
            if state_vars["active_button"]:
                state_vars["active_button"].config(relief=tk.RAISED)
                state_vars["active_button"] = None
            state_vars["selected_button"] = None
            duration_var.set("")
            state_vars["state"] = "get_angles"
            print(f"Submitted: {state_vars}")
        else:
            messagebox.showerror("Invalid Submission", "Please select a button and enter a duration greater than 0.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid float value for duration.")

# GUI-building function
def gui_launch(random_flag, on_data_submit):
    global state_vars
    state_vars["state"] = "ready" if not random_flag else "random"

    root = tk.Tk()
    root.title("Robo Guitarist")
    root.geometry("1024x576")

    def on_exit_click():
        state_vars["state"] = "exit"
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_exit_click)

    # Load background image
    bg_image_path = os.path.join(BASE_DIR, "assets", "images", "GUI3.png")
    bg_image = Image.open(bg_image_path).resize((1024, 576), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_photo

    # Controls frame
    controls_frame = tk.Frame(root, padx=10, pady=10)
    controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20, anchor="n")

    # String selection buttons
    button_frame = tk.LabelFrame(controls_frame, text="Select a string", padx=10, pady=10)
    button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

    button_widgets = {}
    for i in range(7):  # 0 for "Open", 1-6 for strings
        text = "Open" if i == 0 else str(i)
        button = tk.Button(button_frame, text=text, command=lambda i=i: on_button_click(i, button_widgets))
        button.grid(row=i // 7, column=i % 7, padx=5, pady=5, sticky="w")
        button_widgets[i] = button

    # Duration input
    duration_frame = tk.Frame(controls_frame)
    duration_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
    tk.Label(duration_frame, text="Duration (seconds):").pack(side=tk.LEFT, padx=5)
    duration_var = tk.StringVar()
    tk.Entry(duration_frame, textvariable=duration_var).pack(side=tk.LEFT, padx=5)

    def submit_data():
        on_duration_submit(duration_var)
        if state_vars["state"] == "get_angles":
            # Invoke the callback with the current state, string number, and duration
            on_data_submit(state_vars["state"], state_vars["string_num"], state_vars["duration"])

    tk.Button(duration_frame, text="Submit", command=submit_data).pack(side=tk.LEFT, padx=5)

    # Random mode button
    tk.Button(controls_frame, text="Random Mode", command=lambda: state_vars.update({"state": "random"})).pack(side=tk.TOP, pady=10, anchor="w")

    # Exit button
    tk.Button(root, text="Exit", command=on_exit_click).place(relx=0.02, rely=0.95, anchor="sw")

    root.mainloop()