import tkinter as tk
import sqlite3
# from gui_register_screen import register_screen
from utils import fetch_machines


def login_screen():

    def submit_form():
        emp_num = int(emp_num_entry.get())
        machine = machine_entry.get()
        print(f"Employee Number: {emp_num}\nMachine: {machine}")


    # Main window for the login screen
    loginScreen = tk.Tk()

    # Window Name
    loginScreen.title("DTMT Login")

    # Set the size of the screen to full-screen
    loginScreen.state('zoomed')

    # Entry Fields

    # Employee Number
    emp_number_label = tk.Label(loginScreen, text="Employee Number:")
    emp_number_label.grid(row=0, column=0, padx=(10,5), pady=(10,5), sticky="e")
    emp_number_entry = tk.Entry(loginScreen)
    emp_number_entry.grid(row=0, column=1, padx=(5,10), pady=(10,5))

    # Employee Machine
    machine_label = tk.Label(loginScreen, text="Machine:")
    machine_label.grid(row=1, column=0, padx=(10,5), pady=(5,10), sticky="e")

    # List Machines
    machines_list = fetch_machines()
    selected_machine = tk.StringVar(loginScreen)
    selected_machine.set("Select Machine") # Default option

    # List Machines Dropdown Menu'
    machine_dropdown = tk.OptionMenu(loginScreen, selected_machine, *machines_list)
    machine_dropdown.grid(row=1, column=1, padx=(5,10), pady=(5,10))

    # Create login button
    login_button = tk.Button(loginScreen, text="Login", command=submit_form)
    login_button.grid(row=2, columnspan=2, pady=(5,10))

    # Create Register button
    register_user_button = tk.Button(loginScreen, text="Register", command=register_screen)
    register_user_button.grid(row=3, columnspan=3, pady=(5,10))

    # Run the main loop
    loginScreen.mainloop()