import tkinter as tk
import os
import datetime
from tkinter import messagebox, ttk
from emp_database import add_employee_db, create_employees_table, check_for_emp, fetch_employee_name

from tool_database import (
    add_tool_db,
    create_tool_table,
    tool_analytics_search,
    part_analytics_search,
    operation_analytics_search,
    machine_analytics_search,
    operator_analytics_search
)

from utils import fetch_machines, fetch_all_records, clear_database, create_searchable_dropdown

# Create Database tables

create_employees_table()
create_tool_table()


# Main Application / Display Main Screen / Sets Title / Controls What Frame a User Sees


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("DTMT")
        self.state("zoomed")

        container = tk.Frame(self)
        # Replace the pack method with grid
        container.grid(sticky='nsew')

        self.columnconfigure(0, weight=1)  # Allow column to expand
        self.rowconfigure(0, weight=1)  # Allow row to expand

        self.frames = {}
        self.current_user = []

        for F in (LoginScreen, RegisterScreen, AddToolScreen, AdminLoginScreen, DataAnalysisScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Login Screen / Frame

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Create function to submit login entry fields

        def submit_login_form():
            emp_num = emp_number_entry.get()
            machine = selected_machine.get()
            login_user(emp_num, machine)

        def login_user(emp_num, machine):

            if machine == "----":
                messagebox.showerror(
                    title="ERROR: Machine Selection",
                    message="Please select a machine from the drop down menu."
                )

                return

            if emp_num[:4] != "0000" or len(emp_num) != 8 or not emp_num.isdigit():
                messagebox.showerror(
                    title="ERROR: Employee Number",
                    message=
                    "Employee number should start with '0000' Followed by your four unique numbers.\n"
                    "Only enter numbers into this field."
                )

                return

            emp_in_database = check_for_emp(emp_num)

            if emp_in_database is True:

                emp_name = fetch_employee_name(emp_num)

                if emp_name:

                    # Update Current User
                    controller.current_user.append(emp_name)
                    controller.current_user.append(machine)

                    # Move to Add Tool Screen
                    controller.show_frame(AddToolScreen)

                    # Clear Login Screen
                    emp_number_entry.delete(0, tk.END)
                    selected_machine.set("----")

                    # Display Current User To Console
                    print(controller.current_user)

                else:
                    messagebox.showerror(
                        title="ERROR: SYSTEM ERROR",
                        message="Please Contact System Administrator."
                    )

            else:
                return

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
        selected_machine.set("----")  # Default option

        # List Machines Dropdown Menu
        machine_dropdown = tk.OptionMenu(self, selected_machine, *machines_list)
        machine_dropdown.grid(row=1, column=1, padx=(5, 10), pady=(5, 10))

        # Create login button
        login_button = tk.Button(self, text="Login", command=submit_login_form)
        login_button.grid(row=2, columnspan=2, pady=(5, 10))

        # Create Register button
        register_user_button = tk.Button(self, text="Register", command=lambda: controller.show_frame(RegisterScreen))
        register_user_button.grid(row=3, columnspan=3, pady=(5, 10))

        # Admin Button
        admin_button = tk.Button(self, text="Admin Login", command=lambda: controller.show_frame(AdminLoginScreen))
        admin_button.grid(row=4, columnspan=4, pady=(5,10))


# Register Screen / Frame

class RegisterScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Used to clear register entries after they have been entered and the user returns to LoginScreen

        def clear_register_entries():
            emp_number_entry.delete(0, tk.END)
            emp_name_first_entry.delete(0, tk.END)
            emp_name_last_entry.delete(0, tk.END)
            selected_machine.set("-----")

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
                    message="Name fields should not be longer than 10 letters.\n"
                            "Only user letters for these fields."
                )

                return

            if machine == "-----":
                messagebox.showerror(
                    title="ERROR: Machine Select",
                    message="Please select a valid machine from the drop down menu."
                )

                return

            else:
                created_user_info.append(machine)

            if not unfulfilled_number and not unfulfilled_name:

                user_response = messagebox.askyesno(
                    title="Validate Credentials",
                    message=
                    f"Employee Number: {emp_num}\nEmployee Name: {emp_name}\nEmployee Machine: {machine}\n"
                    f"Employee will be added to DTMT Database!\n"
                    "If this information is correct, press 'Yes'. If you want to make changes, press 'No'."
                )

                if user_response:
                    if add_employee_db(created_user_info) is True:
                        clear_register_entries()
                        controller.show_frame(LoginScreen)
                    else:

                        # Display CURRENT Database
                        all_emp_records = fetch_all_records("employee.db", "employees")

                        for record in all_emp_records:
                            print(record)

                        return

                    # Display UPDATED Database
                    all_emp_records = fetch_all_records("employee.db", "employees")
                    for record in all_emp_records:
                        print(record)

            else:

                messagebox.showerror(
                    title="SYSTEM ERROR",
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


class AddToolScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.current_user = controller.current_user

        # Logout Function

        def log_out():

            # Clear Entry Fields
            tool_num_entry.delete(0, tk.END)
            part_number_entry.delete(0, tk.END)
            op_number_entry.delete(0, tk.END)
            incident_desc_entry_field.delete('1.0', tk.END)

            # Move to Login Screen
            controller.show_frame(LoginScreen)

            # Clear Current User
            controller.current_user = []

        # Current Time Function

        def set_current_time(self):

            current_time = datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')
            return current_time

        # Damaged Tool Submission

        def submit_tool_data():
            tool_num = tool_num_entry.get()
            part_num = part_number_entry.get()
            op_num = op_number_entry.get()
            desc = incident_desc_entry_field.get('1.0', 'end')
            desc = desc.strip()

            validate_tool_data(tool_num, part_num, op_num, desc)

        # Submissions Validation

        def validate_tool_data(tool_num, part_num, op_num, desc):
            user_entered_details = []

            try:

                tool_num_int = int(tool_num)

                if tool_num_int in tool_numbers:

                    user_entered_details.append(tool_num_int)

                else:

                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    title="ERROR: Selected Tool Number",
                    message="Please enter a valid tool number or contact System Administrator."
                )

            if part_num in part_numbers:

                user_entered_details.append(part_num)

            else:

                messagebox.showerror(
                    title="ERROR: Selected Part Number",
                    message="Please enter a valid part number or contact System Administrator."
                )

            try:

                op_num_int = int(op_num)

                if op_num_int in op_numbers:

                    user_entered_details.append(op_num_int)

                else:

                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    title="ERROR: Selected Operation Number",
                    message="Please enter a valid operation number or contact System Administrator."
                )

            if len(desc) > 20 < 300:

                user_entered_details.append(desc)

            else:

                messagebox.showerror(
                    title="ERROR: Entered Description",
                    message=f"Minimum word count: 20\nMaximum word count: 300\nCurrent word count:{len(desc)}\n"
                            f"Please contact System Administrator if this issue persist."
                )

            if len(user_entered_details) == 4:

                continue_submission = messagebox.askyesno(
                    title="Validate Damaged Tool Submission",
                    message=
                    f"Tool Number: {tool_num}\nPart Number: {part_num}\nOperation Number: {op_num}\n"
                    f"Make sure description accurately illustrates the incident that occurred."
                )

                if continue_submission is True:

                    date_time = set_current_time(self)
                    add_tool_db(user_entered_details, controller.current_user, date_time)

                    messagebox.showinfo(
                        title="Success",
                        message="Tool Submitted.\nYou may submit another tool or logout now."
                    )

                    # Display UPDATED Database
                    all_tool_records = fetch_all_records("tool.db", "tools")
                    for record in all_tool_records:
                        print(record)

                else:
                    return

            else:
                messagebox.showerror(
                    title="ERROR: SYSTEM ERROR",
                    message="Please review your submitted fields.\nContact System Administrator."
                )

        # Create Tool Number Menu

        tool_numbers = list(range(1,901))
        tool_num_entry, tool_listbox, selected_tool =\
            create_searchable_dropdown(self, tool_numbers, "Enter Tool Number")

        # Create Part Number Menu

        part_numbers_test = 'C:/Users/towma/Desktop/damaged_tool_system/part_numbers_test'
        part_numbers = [part for part in os.listdir(part_numbers_test)]
        part_number_entry, part_listbox, selected_part =\
            create_searchable_dropdown(self,part_numbers, "Enter Part Number")

        # Create Operation Menu

        op_numbers = list(range(0,901,5))
        op_number_entry, op_listbox, selected_op =\
            create_searchable_dropdown(self,op_numbers, "Enter Operation Number")

        # Create Description Input Field (text)

        desc_label = tk.Label(self, text="Description of Incident and Section of Program: ")
        desc_label.pack()

        desc_sub_label = tk.Label(self, text="(include time of incident with description)")
        desc_sub_label.pack()

        incident_desc_entry_field = tk.Text(self, width=50, height=10)
        incident_desc_entry_field.pack()

        # Create Damaged Tool Submit Button
        dam_tool_submit_button = tk.Button(self, text="Submit", command=submit_tool_data)
        dam_tool_submit_button.pack()

        # Create Logout Button
        log_out_button = tk.Button(self, text="Logout", command=log_out)
        log_out_button.pack()


class DataAnalysisScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Create a frame for the statistics

        statistics_label = tk.Label(self, text="Statistics", font=("Helvetica", 12, "bold"))

        self.statistics_frame = ttk.LabelFrame(
            self, borderwidth=2,
            labelwidget=statistics_label
        )

        self.statistics_frame.grid(row=13, column=0, padx=5, pady=5, sticky='nw')

        # Initially hide the statistics frame

        self.statistics_frame.grid_remove()

        # Create all the GUI Statistic Labels

        self.tool_number_result = tk.Label(self.statistics_frame, text="")
        self.tool_number_result.grid(row=0, column=0, sticky='nw')

        self.part_number_result = tk.Label(self.statistics_frame, text="")
        self.part_number_result.grid(row=1, column=0, sticky='nw')

        self.operation_number_result = tk.Label(self.statistics_frame, text="")
        self.operation_number_result.grid(row=2, column=0, sticky='nw')

        self.machine_result = tk.Label(self.statistics_frame, text="")
        self.machine_result.grid(row=3, column=0, sticky='nw')

        self.description_result = tk.Label(self.statistics_frame, text="")
        self.description_result.grid(row=4, column=0, sticky='nw')

        self.operator_result = tk.Label(self.statistics_frame, text="")
        self.operator_result.grid(row=5, column=0, sticky='nw')

        self.total_incidents = tk.Label(self.statistics_frame, text="")
        self.total_incidents.grid(row=6, column=0, sticky='nw')

        self.date_result = tk.Label(self.statistics_frame, text="")
        self.date_result.grid(row=7, column=0, sticky='nw')

        # Store the results of the query based on data types

        self.data_search_results = []

        # Data Search Function

        def data_search():

            # Controller for next and prev buttons

            self.incident_indexer = 0

            def next_incident_button():

                if self.data_search_results and self.incident_indexer < len(self.data_search_results) - 1:

                    self.incident_indexer += 1

                    self.tool_number_result.config(
                        text=f"Tool Number: {self.data_search_results[self.incident_indexer][0]}"
                    )

                    self.part_number_result.config(
                        text=f"Part Number: {self.data_search_results[self.incident_indexer][1]}"
                    )

                    self.operation_number_result.config(
                        text=f"Operation Number: {self.data_search_results[self.incident_indexer][2]}"
                    )

                    self.machine_result.config(
                        text=f"Machine: {self.data_search_results[self.incident_indexer][4]}"
                    )

                    self.description_result.config(
                        text=f"Incident Description: {self.data_search_results[self.incident_indexer][3]}"
                    )

                    self.operator_result.config(
                        text=f"Operator: {self.data_search_results[self.incident_indexer][5]}"
                    )

                    self.date_result.config(
                        text=f"Date of Incident: {self.data_search_results[self.incident_indexer][6]}"
                    )

                    self.update_idletasks()

                else:
                    return

            def prev_incident_button():

                if self.data_search_results and self.incident_indexer > 0:

                    self.incident_indexer -= 1

                    self.tool_number_result.config(
                        text=f"Tool Number: {self.data_search_results[self.incident_indexer][0]}"
                    )

                    self.part_number_result.config(
                        text=f"Part Number: {self.data_search_results[self.incident_indexer][1]}"
                    )

                    self.operation_number_result.config(
                        text=f"Operation Number: {self.data_search_results[self.incident_indexer][2]}"
                    )

                    self.machine_result.config(
                        text=f"Machine: {self.data_search_results[self.incident_indexer][4]}"
                    )

                    self.description_result.config(
                        text=f"Incident Description: {self.data_search_results[self.incident_indexer][3]}"
                    )

                    self.operator_result.config(
                        text=f"Operator: {self.data_search_results[self.incident_indexer][5]}"
                    )

                    self.date_result.config(
                        text=f"Date of Incident: {self.data_search_results[self.incident_indexer][6]}"
                    )

                    self.update_idletasks()

                else:
                    return

            # Tool Data Search

            if self.data_name == "Tool Data":

                try:

                    part_num = part_number_combobox.get()
                    op_num = op_number_combobox.get()
                    machine = machine_combobox.get()
                    tool_num = tool_number_combobox.get()

                    op_num = int(op_num)
                    tool_num = int(tool_num)

                    self.data_search_results = tool_analytics_search(part_num, op_num, machine, tool_num)
                    self.data_search_results = self.data_search_results[::-1]

                    # Create Statistics GUI

                    self.statistics_frame.grid()

                    self.tool_number_result.config(
                        text=f"Tool Number: {self.data_search_results[self.incident_indexer][0]}"
                    )

                    self.part_number_result.config(
                        text=f"Part Number: {self.data_search_results[self.incident_indexer][1]}"
                    )

                    self.operation_number_result.config(
                        text=f"Operation Number: {self.data_search_results[self.incident_indexer][2]}"
                    )

                    self.machine_result.config(
                        text=f"Machine: {self.data_search_results[self.incident_indexer][4]}"
                    )

                    self.description_result.config(
                        text=f"Incident Description: {self.data_search_results[self.incident_indexer][3]}"
                    )

                    self.operator_result.config(
                        text=f"Operator: {self.data_search_results[self.incident_indexer][5]}"
                    )

                    self.total_incidents.config(text=f"Total Incidents: {len(self.data_search_results)}")

                    self.date_result.config(
                        text=f"Date of Incident: {self.data_search_results[self.incident_indexer][6]}"
                    )

                    # Next Incident Button

                    next_button = tk.Button(
                        self.statistics_frame,
                        text=">>",
                        command=lambda: next_incident_button()
                    )

                    next_button.grid(row=8, column=1, sticky='nw')

                    # Previous Incident Button

                    prev_button = tk.Button(
                        self.statistics_frame,
                        text="<<",
                        command= lambda: prev_incident_button()
                    )

                    prev_button.grid(row=8, column=0, sticky='nw')

                    self.update_idletasks()

                except IndexError:

                    messagebox.showerror(
                        title="ERROR: Database Search",
                        message="The current search inquery was not found in the database. If this inquery should exist"
                                " in the database, contact the System Administrator."
                    )
                    return

            # Part Data Search

            if self.data_name == "Part Data":

                try:

                    part_num = part_number_combobox_2.get()
                    self.data_search_results = part_analytics_search(part_num)
                    self.data_search_results = self.data_search_results[::-1]

                    # Create Statistics GUI

                    self.statistics_frame.grid()

                    self.tool_number_result.config(
                        text=f"Tool Number: {self.data_search_results[self.incident_indexer][0]}"
                    )

                    self.part_number_result.config(
                        text=f"Part Number: {self.data_search_results[self.incident_indexer][1]}"
                    )

                    self.operation_number_result.config(
                        text=f"Operation Number: {self.data_search_results[self.incident_indexer][2]}"
                    )

                    self.machine_result.config(
                        text=f"Machine: {self.data_search_results[self.incident_indexer][4]}"
                    )

                    self.description_result.config(
                        text=f"Incident Description: {self.data_search_results[self.incident_indexer][3]}"
                    )

                    self.operator_result.config(
                        text=f"Operator: {self.data_search_results[self.incident_indexer][5]}"
                    )

                    self.total_incidents.config(text=f"Total Incidents: {len(self.data_search_results)}")

                    self.date_result.config(
                        text=f"Date of Incident: {self.data_search_results[self.incident_indexer][6]}"
                    )

                    # Next Incident Button

                    next_button = tk.Button(
                        self.statistics_frame,
                        text=">>",
                        command=lambda: next_incident_button()
                    )

                    next_button.grid(row=8, column=1, sticky='nw')

                    # Previous Incident Button

                    prev_button = tk.Button(
                        self.statistics_frame,
                        text="<<",
                        command= lambda: prev_incident_button()
                    )

                    prev_button.grid(row=8, column=0, sticky='nw')

                    self.update_idletasks()

                except IndexError:

                    messagebox.showerror(
                        title="ERROR: Database Search",
                        message="The current search inquery was not found in the database. If this inquery should exist"
                                " in the database, contact the System Administrator."
                    )
                    return

            # Operation Data Search

            if self.data_name == "Operation Data":

                try:

                    part_num = part_number_combobox_3.get()
                    op_num = op_number_combobox_2.get()

                    self.data_search_results = operation_analytics_search(part_num, op_num)
                    self.data_search_results = self.data_search_results[::-1]

                    # Create Statistics GUI

                    self.statistics_frame.grid()

                    self.tool_number_result.config(
                        text=f"Tool Number: {self.data_search_results[self.incident_indexer][0]}"
                    )

                    self.part_number_result.config(
                        text=f"Part Number: {self.data_search_results[self.incident_indexer][1]}"
                    )

                    self.operation_number_result.config(
                        text=f"Operation Number: {self.data_search_results[self.incident_indexer][2]}"
                    )

                    self.machine_result.config(
                        text=f"Machine: {self.data_search_results[self.incident_indexer][4]}"
                    )

                    self.description_result.config(
                        text=f"Incident Description: {self.data_search_results[self.incident_indexer][3]}"
                    )

                    self.operator_result.config(
                        text=f"Operator: {self.data_search_results[self.incident_indexer][5]}"
                    )

                    self.total_incidents.config(text=f"Total Incidents: {len(self.data_search_results)}")

                    self.date_result.config(
                        text=f"Date of Incident: {self.data_search_results[self.incident_indexer][6]}"
                    )

                    # Next Incident Button

                    next_button = tk.Button(
                        self.statistics_frame,
                        text=">>",
                        command=lambda: next_incident_button()
                    )

                    next_button.grid(row=8, column=1, sticky='nw')

                    # Previous Incident Button

                    prev_button = tk.Button(
                        self.statistics_frame,
                        text="<<",
                        command=lambda: prev_incident_button()
                    )

                    prev_button.grid(row=8, column=0, sticky='nw')

                    self.update_idletasks()

                except IndexError:

                    messagebox.showerror(
                        title="ERROR: Database Search",
                        message="The current search inquery was not found in the database. If this inquery should exist"
                                " in the database, contact the System Administrator."
                    )
                    return

            # Machine Data Search

            if self.data_name == "Machine Data":

                try:

                    machine = machine_combobox_2.get()
                    self.data_search_results = machine_analytics_search(machine)
                    self.data_search_results = self.data_search_results[::-1]

                    # Create Statistics GUI

                    self.statistics_frame.grid()

                    self.tool_number_result.config(
                        text=f"Tool Number: {self.data_search_results[self.incident_indexer][0]}"
                    )

                    self.part_number_result.config(
                        text=f"Part Number: {self.data_search_results[self.incident_indexer][1]}"
                    )

                    self.operation_number_result.config(
                        text=f"Operation Number: {self.data_search_results[self.incident_indexer][2]}"
                    )

                    self.machine_result.config(
                        text=f"Machine: {self.data_search_results[self.incident_indexer][4]}"
                    )

                    self.description_result.config(
                        text=f"Incident Description: {self.data_search_results[self.incident_indexer][3]}"
                    )

                    self.operator_result.config(
                        text=f"Operator: {self.data_search_results[self.incident_indexer][5]}"
                    )

                    self.total_incidents.config(text=f"Total Incidents: {len(self.data_search_results)}")

                    self.date_result.config(
                        text=f"Date of Incident: {self.data_search_results[self.incident_indexer][6]}"
                    )

                    # Next Incident Button

                    next_button = tk.Button(
                        self.statistics_frame,
                        text=">>",
                        command=lambda: next_incident_button()
                    )

                    next_button.grid(row=8, column=1, sticky='nw')

                    # Previous Incident Button

                    prev_button = tk.Button(
                        self.statistics_frame,
                        text="<<",
                        command=lambda: prev_incident_button()
                    )

                    prev_button.grid(row=8, column=0, sticky='nw')

                    self.update_idletasks()

                except IndexError:

                    messagebox.showerror(
                        title="ERROR: Database Search",
                        message="The current search inquery was not found in the database. If this inquery should exist"
                                " in the database, contact the System Administrator."
                    )
                    return

            # Operator Data Search

            if self.data_name == "Operator Data":

                try:

                    operator = operator_name.get()
                    self.data_search_results = operator_analytics_search(operator)
                    self.data_search_results = self.data_search_results[::-1]

                    # Create Statistics GUI

                    self.statistics_frame.grid()

                    self.tool_number_result.config(
                        text=f"Tool Number: {self.data_search_results[self.incident_indexer][0]}"
                    )

                    self.part_number_result.config(
                        text=f"Part Number: {self.data_search_results[self.incident_indexer][1]}"
                    )

                    self.operation_number_result.config(
                        text=f"Operation Number: {self.data_search_results[self.incident_indexer][2]}"
                    )

                    self.machine_result.config(
                        text=f"Machine: {self.data_search_results[self.incident_indexer][4]}"
                    )

                    self.description_result.config(
                        text=f"Incident Description: {self.data_search_results[self.incident_indexer][3]}"
                    )

                    self.operator_result.config(
                        text=f"Operator: {self.data_search_results[self.incident_indexer][5]}"
                    )

                    self.total_incidents.config(text=f"Total Incidents: {len(self.data_search_results)}")

                    self.date_result.config(
                        text=f"Date of Incident: {self.data_search_results[self.incident_indexer][6]}"
                    )

                    # Next Incident Button

                    next_button = tk.Button(
                        self.statistics_frame,
                        text=">>",
                        command=lambda: next_incident_button()
                    )

                    next_button.grid(row=8, column=1, sticky='nw')

                    # Previous Incident Button

                    prev_button = tk.Button(
                        self.statistics_frame,
                        text="<<",
                        command=lambda: prev_incident_button()
                    )

                    prev_button.grid(row=8, column=0, sticky='nw')

                    self.update_idletasks()

                except IndexError:

                    messagebox.showerror(
                        title="ERROR: Database Search",
                        message="The current search inquery was not found in the database. If this inquery should exist"
                                " in the database, contact the System Administrator."
                    )
                    return

        # Create a function to hide and show required fields

        def show_field(show_frame, frames):
            for frame in frames:
                frame.grid_remove()

            show_frame.grid(row=8, column=0, padx=5, pady=5, sticky='nw')

        # Create a function to update the required fields

        self.data_name = "Selected Data Type (select a data type above)"

        def update_data_name(new_data_name):
            self.data_name = new_data_name
            data_fields_label.config(text=f"Enter Required Fields for {self.data_name}")

        # Create Data Frames

        tool_data_frame = tk.Frame(self)
        part_data_frame = tk.Frame(self)
        operation_data_frame = tk.Frame(self)
        machine_data_frame = tk.Frame(self)
        operator_data_frame = tk.Frame(self)

        self.frames = [
            tool_data_frame,
            part_data_frame,
            operation_data_frame,
            machine_data_frame,
            operator_data_frame
        ]

        # List Tool Numbers

        tool_numbers = list(range(1, 901))

        #List Part Numbers

        part_numbers_test = 'C:/Users/towma/Desktop/damaged_tool_system/part_numbers_test'
        part_numbers = [part for part in os.listdir(part_numbers_test)]

        # List Operation Numbers

        op_numbers = list(range(0, 901, 5))

        # List Machines

        machines_list = fetch_machines()
        selected_machine = tk.StringVar(self)
        selected_machine.set("----")  # Default option

        # Create Data Select Header

        data_select_label = tk.Label(self, text="Select Data to Display", font=("Helvetica", 12, "bold"))
        data_select_label.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Create Data Field Requirement Header

        data_fields_label = tk.Label(self, text=f"Enter Required Fields for {self.data_name}",
                                     font=("Helvetica", 12, "bold"))
        data_fields_label.grid(row=7, column=0, padx=5, pady=5, sticky='nw')

        # Tool Data Button

        tool_data_button = tk.Button(
            self,
            text="Tool Data",
            command=lambda: (show_field(self.frames[0], self.frames), update_data_name("Tool Data"))
        )

        tool_data_button.grid(row=1, column=0, padx=5, pady=5, sticky='nw')

        # Tool Data Fields
        tool_fields = tk.Frame(tool_data_frame)
        tk.Label(tool_fields, text="Part Number:").grid(row=0, column=0)
        part_number_combobox = ttk.Combobox(tool_fields, values=part_numbers)
        part_number_combobox.grid(row=0, column=1)
        part_number_combobox.configure(state="normal")

        tk.Label(tool_fields, text="Operation:").grid(row=1, column=0)
        op_number_combobox = ttk.Combobox(tool_fields, values=op_numbers)
        op_number_combobox.grid(row=1, column=1)
        op_number_combobox.configure(state="normal")

        tk.Label(tool_fields, text="Machine:").grid(row=2, column=0)
        machine_combobox = ttk.Combobox(tool_fields, values=machines_list)
        machine_combobox.grid(row=2, column=1)
        machine_combobox.configure(state="normal")

        tk.Label(tool_fields, text="Tool Number:").grid(row=3, column=0)
        tool_number_combobox = ttk.Combobox(tool_fields, values=tool_numbers)
        tool_number_combobox.grid(row=3, column=1)
        tool_number_combobox.configure(state="normal")

        tool_fields.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Part Data Button

        part_data_button = tk.Button(
            self,
            text="Part Data",
            command=lambda: (show_field(self.frames[1], self.frames), update_data_name("Part Data"))
        )

        part_data_button.grid(row=2, column=0, padx=5, pady=5, sticky='nw')

        # Part Data Fields
        part_fields = tk.Frame(part_data_frame)
        tk.Label(part_fields, text="Part Number:").grid(row=0, column=0)
        part_number_combobox_2 = ttk.Combobox(part_fields, values=part_numbers)
        part_number_combobox_2.grid(row=0, column=1)
        part_number_combobox_2.configure(state="normal")

        part_fields.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Operation Data Button

        operation_data_button = tk.Button(
            self,
            text="Operation Data",
            command=lambda: (show_field(self.frames[2], self.frames), update_data_name("Operation Data"))
        )

        operation_data_button.grid(row=3, column=0, padx=5, pady=5, sticky='nw')

        # Operation Data Fields
        operation_fields = tk.Frame(operation_data_frame)
        tk.Label(operation_fields, text="Part Number:").grid(row=0, column=0)
        part_number_combobox_3 = ttk.Combobox(operation_fields, values=part_numbers)
        part_number_combobox_3.grid(row=0, column=1)
        part_number_combobox_3.configure(state="normal")

        tk.Label(operation_fields, text="Operation Number:").grid(row=1, column=0)
        op_number_combobox_2 = ttk.Combobox(operation_fields, values=op_numbers)
        op_number_combobox_2.grid(row=1, column=1)
        op_number_combobox_2.configure(state="normal")

        operation_fields.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Machine Data Button

        machine_data_button = tk.Button(
            self,
            text="Machine Data",
            command=lambda: (show_field(self.frames[3], self.frames), update_data_name("Machine Data"))
        )

        machine_data_button.grid(row=4, column=0, padx=5, pady=5, sticky='nw')

        # Machine Data Fields
        machine_fields = tk.Frame(machine_data_frame)
        tk.Label(machine_fields, text="Select Machine:").grid(row=0, column=0)
        machine_combobox_2 = ttk.Combobox(machine_fields, values=machines_list)
        machine_combobox_2.grid(row=0, column=1)
        machine_combobox_2.configure(state="normal")

        machine_fields.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Operator Data Button

        operator_data_button = tk.Button(
            self,
            text="Operator Data",
            command=lambda: (show_field(self.frames[4], self.frames), update_data_name("Operator Data"))
        )
        operator_data_button.grid(row=5, column=0, padx=5, pady=5, sticky='nw')

        # Operator Data Fields

        operator_fields = tk.Frame(operator_data_frame)
        tk.Label(operator_fields, text="Operator Name:").grid(row=0, column=0)
        operator_name = tk.Entry(operator_fields)
        operator_name.grid(row=0, column=1)


        operator_fields.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Data Search Button

        search_button = tk.Button(self, text="Search", command=data_search)
        search_button.grid(row=10, column=0, padx=5, pady=5, sticky='nw')

        # Used to only show the currently selected data fields
        for frame in self.frames:
            frame.grid_remove()


class AdminLoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        def admin_login():

            admin_id = admin_id_entry.get()

            if admin_id == "admin0100":

                controller.show_frame(DataAnalysisScreen)

                # Clear Entry Fields
                admin_id_entry.delete(0, tk.END)

            else:
                messagebox.showerror(
                    title="ERROR: Not Admin",
                    message="The entered ID is not associated with any stored admin ID.\n"
                            "Contact System Administrator for further assistance."
                )

                return

        # Admin Login
        admin_id_label = tk.Label(self, text="Admin ID:")
        admin_id_label.pack()
        admin_id_entry = tk.Entry(self, show="*")
        admin_id_entry.pack()

        # Login Button
        login_button = tk.Button(self, text="Login", command=admin_login)
        login_button.pack()

        # Back To Login Screen
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(LoginScreen))
        back_button.pack()


# DATABASE CLEAR !!!
# clear_database("employee.db", "employees")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
