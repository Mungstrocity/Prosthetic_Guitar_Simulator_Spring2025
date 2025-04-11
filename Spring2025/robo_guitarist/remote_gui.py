import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from tkinter.ttk import Combobox
import requests

BASE_DIR = os.path.dirname(__file__)

# Global state variables
state_vars = {
    "state": "not_started",
    "selected_button": None,
    "duration": None,
    "string_num": None,
    "active_button": None,
}

# Add a function to handle blocked input notification
def notify_blocked_input():
    if state_vars["state"] == "random":
        messagebox.showinfo("Random Mode Active", "Inputs are blocked while in Random Mode. Exit Random Mode to continue.")

# Add a function to update the status label
def update_status(fret, string, duration):
    status_text.set(f"Playing fret {fret} on string {string} for {duration:.1f} seconds")

# Add a function to send data to the server
def send_data_to_server(state, string_num, duration):
    server_ip = "10.228.12.158"  # IP address of the server
    server_url = f"http://{server_ip}:5000/handle_gui_data"

    data = {
        "state": state,
        "string_num": string_num,
        "duration": duration
    }

    try:
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            print("Data sent successfully to the server.")
        else:
            print(f"Failed to send data to the server. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the server: {e}")

# Add a function to test server connection
def test_server_connection():
    server_ip = "10.228.12.158"  # IP address of the server
    server_url = f"http://{server_ip}:5000/handle_gui_data"

    try:
        response = requests.get(server_url)
        if response.status_code == 200:
            print("Successfully connected to the server.")
        else:
            print(f"Server connection failed. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the server: {e}")

# Button control functions
def on_button_click(button_id, button_widgets):
    global state_vars
    if state_vars["state"] == "random":
        notify_blocked_input()  # Notify if inputs are blocked
        return

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
            update_status("fret 1", state_vars["string_num"], state_vars["duration"])
            if state_vars["active_button"]:
                state_vars["active_button"].config(relief=tk.RAISED)
                state_vars["active_button"] = None
            state_vars["selected_button"] = None
            duration_var.set("")
            state_vars["state"] = "get_angles"
            print(f"Submitted: {state_vars}")
        else:
            messagebox.showerror("Invalid Submission", "Please select a string nubmer and enter a duration greater than 0.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid float value for duration.")

# GUI-building function
def gui_launch(random_flag, on_data_submit):
    global state_vars
    state_vars["state"] = "ready" if not random_flag else "random"

    # Test server connection
    test_server_connection()

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
        button.grid(row=0, column=i, padx=5, pady=5, sticky="w")
        button_widgets[i] = button

    # Bind buttons to notify_blocked_input
    for button in button_widgets.values():
        button.bind("<Button-1>", lambda event: notify_blocked_input())

    # Duration input
    tk.Label(button_frame, text="Duration (seconds):").grid(row=1, column=0, columnspan=2, pady=5, sticky="w")
    duration_var = tk.StringVar()
    duration_entry = tk.Entry(button_frame, textvariable=duration_var)
    duration_entry.grid(row=1, column=2, columnspan=3, pady=5, padx=5, sticky="w")

    # Bind duration entry to notify_blocked_input
    duration_entry.bind("<FocusIn>", lambda event: notify_blocked_input())

    def submit_data():
        if state_vars["state"] == "random":
            messagebox.showinfo("Random Mode Active", "Inputs not accepted while in Random Mode. Exit Random Mode to continue.")
            return
        on_duration_submit(duration_var)
        if state_vars["state"] == "get_angles":
            # Send data to the server
            send_data_to_server(state_vars["state"], state_vars["string_num"], state_vars["duration"])
            # Invoke the callback with the current state, string number, and duration
            on_data_submit(state_vars["state"], state_vars["string_num"], state_vars["duration"])

    tk.Button(button_frame, text="Submit", command=submit_data).grid(row=1, column=5, columnspan=2, pady=5, padx=5, sticky="w")

    # Random mode toggle using a Button
    def toggle_random_mode():
        if state_vars["state"] == "ready":
            state_vars["state"] = "random"
            random_mode_button.config(
                relief=tk.SUNKEN, 
                text="Random Mode (ON)", 
                bg="#990000", 
                fg="white", 
                font=("Helvetica", 10, "bold"),
                activebackground="#990000",  # Disable hover logic
                activeforeground="white"     # Disable hover logic
            )
        elif state_vars["state"] == "random":
            state_vars["state"] = "ready"
            random_mode_button.config(
                relief=tk.RAISED, 
                text="Random Mode (OFF)", 
                bg="#f0f0f0",  # Platform-independent neutral color
                fg="black", 
                font=("Helvetica", 10, "normal"),
                activebackground="#f0f0f0",  # Disable hover logic
                activeforeground="black"     # Disable hover logic
            )

    random_mode_button = tk.Button(
        controls_frame,
        text="Random Mode (OFF)",
        relief=tk.RAISED,
        command=toggle_random_mode
    )
    random_mode_button.pack(side=tk.TOP, pady=10, anchor="w")

    # Status section
    status_frame = tk.Frame(controls_frame, padx=10, pady=10)
    status_frame.pack(side=tk.TOP, fill=tk.X, pady=10, anchor="w")

    global status_text
    status_text = tk.StringVar()
    status_text.set("Status: Idle")
    status_label = tk.Label(status_frame, textvariable=status_text, font=("Helvetica", 12))
    status_label.pack(anchor="w")

    # Bind the Enter key and the 10-key Enter key to the submit_data function
    root.bind("<Return>", lambda event: submit_data())
    root.bind("<KP_Enter>", lambda event: submit_data())

    # Exit button
    tk.Button(root, text="Exit", command=on_exit_click).place(relx=0.02, rely=0.95, anchor="sw")

    root.mainloop()