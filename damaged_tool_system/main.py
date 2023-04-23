import tkinter as tk
from tkinter import messagebox, simpledialog
from utils import fetch_machines


# Main Application / Display Main Screen / Sets Title / Controls What Frame a User Sees


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("DTMT")
        self.state("zoomed")

        container = tk.Frame(self)
        container.pack(side = "top", fill="both", expand = True)

        self.frames = {}

        for F in (LoginScreen, RegisterScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(LoginScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Login Screen / Frame

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        def submit_form():
            emp_num = emp_number_entry.get()
            machine = selected_machine.get()
            print(f"Employee Number: {emp_num}\nMachine: {machine}")

        # Employee Number
        emp_number_label = tk.Label(self, text="Employee Number:")
        emp_number_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="e")
        emp_number_entry = tk.Entry(self)
        emp_number_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

        # Employee Machine
        machine_label = tk.Label(self, text="Machine:")
        machine_label.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="e")

        # List Machines
        machines_list = fetch_machines()
        selected_machine = tk.StringVar(self)
        selected_machine.set("Select Machine")  # Default option

        # List Machines Dropdown Menu
        machine_dropdown = tk.OptionMenu(self, selected_machine, *machines_list)
        machine_dropdown.grid(row=1, column=1, padx=(5, 10), pady=(5, 10))

        # Create login button
        login_button = tk.Button(self, text="Login", command=submit_form)
        login_button.grid(row=2, columnspan=2, pady=(5, 10))

        # Create Register button
        register_user_button = tk.Button(self, text="Register", command=lambda: controller.show_frame(RegisterScreen))
        register_user_button.grid(row=3, columnspan=3, pady=(5, 10))


# Register Screen / Frame

class RegisterScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Used to register user and add them to the employee database

        def register_user(emp_num, emp_name_first, emp_name_last, machine):
            unfulfilled_number = True
            unfulfilled_name = True
            created_user_info = []

            if emp_num[:4] == "0000" and len(emp_num) == 8 and emp_num.isdigit():
                unfulfilled_number = False
                created_user_info.append(emp_num)
            else:

                messagebox.showerror(
                    title="ERROR: Employee Number",
                    message=
                    "Employee number should start with '0000' Followed by your four unique numbers.\n"
                    "Only enter numbers into this field."
                )

                return

            if emp_name_first.isalpha() and len(emp_name_first) <= 10:
                if emp_name_last.isalpha() and len(emp_name_last) <= 10:
                    emp_name = emp_name_first.capitalize() + " " + emp_name_last.capitalize()
                    created_user_info.append(emp_name)
                    unfulfilled_name = False
            else:

                messagebox.showerror(
                    title="ERROR: Employee Name",
                    message= "Name fields should not be longer than 10 letters.\n"
                             "Only user letters for these fields."
                )

                return

            if machine == "-----":
                messagebox.showerror(
                    title="Machine Select",
                    message="Please select a valid machine from the drop down menu."
                )

                return

            else:
                created_user_info.append(machine)

            if not unfulfilled_number and not unfulfilled_name:

                messagebox.showinfo(
                    title = "Success",
                    message =
                    f"Employee Number: {emp_num}\nEmployee Name: {emp_name}\nEmployee Machine: {machine}\n"
                    f"Employee added to DTMT Database!"
                )

                ####

            else:

                messagebox.showerror(
                    title = "SYSTEM ERROR",
                    message=
                    "Please make sure there are no numbers in your name"
                    " and your Employee Number is formatted correctly.\n"
                    "See System Administrator for further information."
                )

        # Used to gather input fields for register function

        def submit_register_form():
            emp_num = emp_number_entry.get()
            emp_name_first = emp_name_first_entry.get()
            emp_name_last = emp_name_last_entry.get()
            machine = selected_machine.get()

            register_user(emp_num, emp_name_first, emp_name_last, machine)

        # Entry Fields

        # Employee Number
        emp_number_label = tk.Label(self, text="Enter Employee Number:")
        emp_number_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="e")
        emp_number_entry = tk.Entry(self)
        emp_number_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

        # Employee First Name
        emp_name_first_label = tk.Label(self, text="Enter First Name:")
        emp_name_first_label.grid(row=1, column=0, padx=(10, 5), pady=(10, 5), sticky="e")
        emp_name_first_entry = tk.Entry(self)
        emp_name_first_entry.grid(row=1, column=1, padx=(5, 10), pady=(10, 5))

        # Employee Last Name
        emp_name_last_label = tk.Label(self, text="Enter Last Name:")
        emp_name_last_label.grid(row=2, column=0, padx=(10, 5), pady=(10, 5), sticky="e")
        emp_name_last_entry = tk.Entry(self)
        emp_name_last_entry.grid(row=2, column=1, padx=(5, 10), pady=(10, 5))

        # Employee Machine
        machine_label = tk.Label(self, text="Select Machine:")
        machine_label.grid(row=3, column=0, padx=(10, 5), pady=(5, 10), sticky="e")

        # List Machines
        machines_list = fetch_machines()
        selected_machine = tk.StringVar(self)
        selected_machine.set("-----")  # Default option

        # List Machines Dropdown Menu'
        machine_dropdown = tk.OptionMenu(self, selected_machine, *machines_list)
        machine_dropdown.grid(row=3, column=1, padx=(5, 10), pady=(5, 10))

        # Create register button
        register_button = tk.Button(self, text="Register", command=submit_register_form)
        register_button.grid(row=4, column=0, columnspan=2, pady=(5, 10))

        # Back Button --> LoginScreen
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(LoginScreen))
        back_button.grid(row=5, column=0, columnspan=2, pady=(5, 10))


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()