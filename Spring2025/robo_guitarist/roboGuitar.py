import tkinter as tk
from tkinter import messagebox


state = "initial"

while True:
    if state == "initial":
        root = tk.Tk()
        root.title("Robo Guitarist")
        root.geometry("500x200")

        def on_button_click():
            global state
            state = "playing"
            messagebox.showinfo("Info", "Playing the guitar!")

        button = tk.Button(root, text="Play Guitar", command=on_button_click)
        button.pack(pady=20)

        root.mainloop()

    elif state == "playing":
        # Simulate playing the guitar
        print("Playing the guitar...")
        break  # Exit the loop after playing