import tkinter as tk
from utils import fetch_machines


def register_screen():

    def register_user(emp_num, emp_name_first, emp_name_last, machine):

        # # Take in the entry fields from Tkinter
        # emp_num = emp_number_entry.get()
        # emp_name_first = emp_name_first_entry.get()
        # emp_name_last = emp_name_last_entry.get()
        # machine = tk.StringVar(registerScreen)

        # Boolean to check register fields
        unfulfilled_number = True
        unfulfilled_name = True

        # Store the created user to add to the database and return to user
        created_user_info = []

        while unfulfilled_number:

            if emp_num[:4] == "0000" and len(emp_num) == 8 and emp_num.isdigit():
                unfulfilled_number = False
                created_user_info.append(emp_num)

            else:
                error_label.config(
                    text="Error: Employee number should start with '0000' followed by your four unique numbers.\nOnly enter numbers into this field!")

        # Field constraints for emp_name
        while unfulfilled_name:

            if emp_name_first.isalpha() and len(emp_name_first) <= 10:
                if emp_name_last.isalpha and len(emp_name_last) <= 10:
                    emp_name = emp_name_first.capitalize() + " " + emp_name_last.capitalize()
                    created_user_info.append(emp_name)
                    unfulfilled_name = False

            else:
                error_label.config(
                    text="Name fields should not be longer than 10 letters.\nOnly use letters for these fields!")

        if unfulfilled_number == False and unfulfilled_name == False:

            success_label.config(text = f"{emp_num}, {emp_name}, {machine} added to DTMT Database!")
        else:
            success_label.config("SYSTEM ERROR")

    def submit_register_form():
        emp_num = emp_number_entry.get()
        emp_name_first = emp_name_first_entry.get()
        emp_name_last = emp_name_last_entry.get()
        machine = selected_machine.get()

        register_user(emp_num, emp_name_first, emp_name_last, machine)


    # Main window for the register screen
    registerScreen = tk.Tk()

    # Window Name
    registerScreen.title("DTMT Register")

    # Set the size of the screen to full-screen
    registerScreen.state('zoomed')

    # Entry Fields

    # Employee Number
    emp_number_label = tk.Label(registerScreen, text="Enter Employee Number:")
    emp_number_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="e")
    emp_number_entry = tk.Entry(registerScreen)
    emp_number_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

    # Employee First Name
    emp_name_first_label = tk.Label(registerScreen, text="Enter First Name:")
    emp_name_first_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="e")
    emp_name_first_entry = tk.Entry(registerScreen)
    emp_name_first_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

    # Employee Last Name
    emp_name_last_label = tk.Label(registerScreen, text="Enter Last Name:")
    emp_name_last_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="e")
    emp_name_last_entry = tk.Entry(registerScreen)
    emp_name_last_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

    # Success Message
    success_label = tk.Label(registerScreen, text="")
    emp_name_last_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="e")
    emp_name_last_entry = tk.Entry(registerScreen)
    emp_name_last_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

    # Employee Machine
    machine_label = tk.Label(registerScreen, text="Select Machine:")
    machine_label.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="e")

    # List Machines
    machines_list = fetch_machines()
    selected_machine = tk.StringVar(registerScreen)
    selected_machine.set("-----")  # Default option

    # List Machines Dropdown Menu'
    machine_dropdown = tk.OptionMenu(registerScreen, selected_machine, *machines_list)
    machine_dropdown.grid(row=1, column=1, padx=(5, 10), pady=(5, 10))

    # Create register button
    register_button = tk.Button(registerScreen, text="Register", command=submit_register_form)
    register_button.grid(row=2, columnspan=2, pady=(5, 10))
