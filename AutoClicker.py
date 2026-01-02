import time
import threading
import tkinter as tk
from tkinter import ttk
from pynput.mouse import Button, Controller
import keyboard

mouse = Controller()

clicking = False
running = True


def click_loop():
    global clicking
    while running:
        if clicking:
            try:
                cps = float(cps_entry.get())
                delay = 1 / cps if cps > 0 else 1
            except ValueError:
                delay = 1

            button = Button.left if button_var.get() == "Left" else Button.right
            mouse.click(button)
            time.sleep(delay)
        else:
            time.sleep(0.1)


def toggle_clicking():
    global clicking
    clicking = not clicking
    status_label.config(
        text="Status: RUNNING" if clicking else "Status: PAUSED"
    )


def on_close():
    global running
    running = False
    root.destroy()


# Hotkey
keyboard.add_hotkey("F6", toggle_clicking)

# GUI
root = tk.Tk()
root.title("Python Auto Clicker")
root.geometry("300x220")
root.resizable(False, False)

ttk.Label(root, text="Clicks Per Second:").pack(pady=5)
cps_entry = ttk.Entry(root)
cps_entry.insert(0, "10")
cps_entry.pack()

ttk.Label(root, text="Mouse Button:").pack(pady=5)
button_var = tk.StringVar(value="Left")
button_menu = ttk.Combobox(
    root, textvariable=button_var, values=["Left", "Right"], state="readonly"
)
button_menu.pack()

status_label = ttk.Label(root, text="Status: PAUSED", font=("Arial", 10, "bold"))
status_label.pack(pady=10)

ttk.Label(root, text="Press F6 to Start / Pause").pack(pady=5)

# Thread
thread = threading.Thread(target=click_loop, daemon=True)
thread.start()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
