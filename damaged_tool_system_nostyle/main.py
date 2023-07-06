import tkinter as tk
import os
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import seaborn as sns

from emp_database import (
    add_employee_db,
    create_employees_table,
    check_for_emp,
    fetch_employee_name
)

from tool_database import (
    add_tool_db,
    create_tool_table,
    tool_analytics_search,
    part_analytics_search,
    operation_analytics_search,
    machine_analytics_search,
    operator_analytics_search,
    part_frequency_search,
    all_tools_search,
    top_five_tools_search,
    machine_frequency_search,
    selected_month_search
)

from utils import (
    fetch_machines,
    fetch_all_records,
    clear_database,
    create_searchable_dropdown
)

# Create database tables

create_employees_table()
create_tool_table()

# Create application icon

icon = 'drilling.ico'


# Main Application / Display Main Screen / Sets Title / Controls What Frame a User Sees ===============================#


class MainApp(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set title and icon / set screen state

        self.title("DTMT")
        self.state('zoomed')
        self.iconbitmap(icon)

        # Determine the screen width and height

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # Set the window size to the screen size

        self.geometry(f"{self.screen_width}x{self.screen_height}")

        # Create container that will house all other frames and nested frames

        container = tk.Frame(self)
        container.grid(sticky='nsew')

        # Set applications global style

        self.style = ttk.Style(self)
        self.style.theme_use('radiance')

        # Set .grid() configurations

        self.columnconfigure(0, weight=0)
        self.rowconfigure(0, weight=0)

        # Create frame dictionary

        self.frames = {}
        self.current_user = []

        for F in (LoginScreen, RegisterScreen, AddToolScreen, AdminLoginScreen, DataAnalysisScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Display LoginScreen on start up

        self.show_frame(LoginScreen)

        # Store the current user logged into the application

        self.current_user = []

    # Create function to show a selected frame

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Login Screen / Frame ================================================================================================#


class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Create function to submit a users login data

        def submit_login_form():
            emp_num = emp_number_entry.get()
            machine = selected_machine.get()
            login_user(emp_num, machine)

        # Create function to execute login if all conditions are met

        def login_user(emp_num, machine):

            # Check that a user machine is selected

            if machine == "----":
                messagebox.showerror(
                    title="ERROR: Machine Selection",
                    message="Please select a machine from the drop down menu."
                )

                return

            # Check that a users employee number is correct

            if emp_num[:4] != "0000" or len(emp_num) != 8 or not emp_num.isdigit():
                messagebox.showerror(
                    title="ERROR: Employee Number",
                    message=
                    "Employee number should start with '0000' Followed by your four unique numbers.\n"
                    "Only enter numbers into this field."
                )

                return

            # Use check_for_emp from emp_database.py to make sure employee is in database

            emp_in_database = check_for_emp(emp_num)

            if emp_in_database is True:

                # Grab employee name using fetch_employee_name from emp_database.py

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

        # GUI Components ==============================================================================================#

        # Employee Number

        emp_number_label = ttk.Label(self, text="Employee Number:")
        emp_number_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="e")
        emp_number_entry = ttk.Entry(self)
        emp_number_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

        # Employee Machine

        machine_label = ttk.Label(self, text="Machine:")
        machine_label.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="e")

        # List Machines

        machines_list = fetch_machines()
        machines_list.insert(0, "----")
        selected_machine = tk.StringVar(self)
        selected_machine.set(machines_list[0])  # Default option

        # List Machines Dropdown Menu

        machine_dropdown = ttk.OptionMenu(self, selected_machine, *machines_list)
        machine_dropdown.grid(row=1, column=1, padx=(5, 10), pady=(5, 10))

        # Create login button

        login_button = ttk.Button(self, text="Login", command=submit_login_form)
        login_button.grid(row=2, columnspan=2, pady=(5, 10))

        # Create Register button

        register_user_button = ttk.Button(self, text="Register", command=lambda: controller.show_frame(RegisterScreen))
        register_user_button.grid(row=3, columnspan=3, pady=(5, 10))

        # Admin Button

        admin_button = ttk.Button(self, text="Admin Login", command=lambda: controller.show_frame(AdminLoginScreen))
        admin_button.grid(row=4, columnspan=4, pady=(5, 10))

        # END GUI COMPONENTS ==========================================================================================#


# Register Screen / Frame =============================================================================================#

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

        # GUI Components (Entry Fields) ===============================================================================#

        # Employee Number

        emp_number_label = ttk.Label(self, text="Enter Employee Number:")
        emp_number_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="e")
        emp_number_entry = ttk.Entry(self)
        emp_number_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

        # Employee First Name

        emp_name_first_label = ttk.Label(self, text="Enter First Name:")
        emp_name_first_label.grid(row=1, column=0, padx=(10, 5), pady=(10, 5), sticky="e")
        emp_name_first_entry = ttk.Entry(self)
        emp_name_first_entry.grid(row=1, column=1, padx=(5, 10), pady=(10, 5))

        # Employee Last Name

        emp_name_last_label = ttk.Label(self, text="Enter Last Name:")
        emp_name_last_label.grid(row=2, column=0, padx=(10, 5), pady=(10, 5), sticky="e")
        emp_name_last_entry = ttk.Entry(self)
        emp_name_last_entry.grid(row=2, column=1, padx=(5, 10), pady=(10, 5))

        # Employee Machine

        machine_label = ttk.Label(self, text="Select Machine:")
        machine_label.grid(row=3, column=0, padx=(10, 5), pady=(5, 10), sticky="e")

        # List Machines

        machines_list = fetch_machines()
        machines_list.insert(0, "----")
        selected_machine = tk.StringVar(self)
        selected_machine.set(machines_list[0])  # Default option

        # List Machines Dropdown Menu

        machine_dropdown = ttk.OptionMenu(self, selected_machine, *machines_list)
        machine_dropdown.grid(row=3, column=1, padx=(5, 10), pady=(5, 10))

        # Create register button

        register_button = ttk.Button(self, text="Register", command=submit_register_form)
        register_button.grid(row=4, column=0, columnspan=2, pady=(5, 10))

        # Back Button --> LoginScreen

        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(LoginScreen))
        back_button.grid(row=5, column=0, columnspan=2, pady=(5, 10))

        # END GUI COMPONENTS ==========================================================================================#

# Add Tool Screen / Incident submission form ==========================================================================#


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

            current_time = datetime.now().strftime('%Y-%m-%d %I:%M %p')
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
                    message=f"Minimum character count: 20\nMaximum character count: 300\n"
                            f"Current character count: {len(desc)}\n"
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

        # GUI Components / Submission Fields ==========================================================================#

        # Create Tool Number Menu

        tool_numbers = list(range(1, 901))
        tool_num_entry, tool_listbox, selected_tool = \
            create_searchable_dropdown(self, tool_numbers, "Enter Tool Number")

        # Create Part Number Menu

        part_numbers_test = 'C:/Users/towma/Desktop/damaged_tool_system/part_numbers_test'
        part_numbers = [part for part in os.listdir(part_numbers_test)]
        part_number_entry, part_listbox, selected_part = \
            create_searchable_dropdown(self, part_numbers, "Enter Part Number")

        # Create Operation Menu

        op_numbers = list(range(0, 901, 5))
        op_number_entry, op_listbox, selected_op = \
            create_searchable_dropdown(self, op_numbers, "Enter Operation Number")

        # Create Description Input Field (text)

        desc_label = ttk.Label(self, text="Description of Incident and Section of Program: ")
        desc_label.pack()

        desc_sub_label = ttk.Label(self, text="(include time of incident with description)")
        desc_sub_label.pack()

        incident_desc_entry_field = tk.Text(self, width=50, height=10)
        incident_desc_entry_field.pack()

        # Create Damaged Tool Submit Button

        dam_tool_submit_button = ttk.Button(self, text="Submit", command=submit_tool_data)
        dam_tool_submit_button.pack()

        # Create Logout Button

        log_out_button = ttk.Button(self, text="Logout", command=log_out)
        log_out_button.pack()

        # END GUI COMPONENTS / SUBMISSION FIELDS ======================================================================#

# END ADD TOOL SCREEN / INCIDENT SUBMISSION FORM ======================================================================#

# Admin Access Data Analysis ==========================================================================================#


class DataAnalysisScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Create all selectable options ===============================================================================#

        # Create Toolbar Options
        # REF. Line 2177

        self.toolbar_options = ['All Tools', 'Machine Frequency Chart', 'Part Frequency Chart', 'Top 5 Tools']

        # List Tool Numbers

        tool_numbers = list(range(1, 901))

        # List Part Numbers

        part_numbers_test = 'C:/Users/towma/Desktop/damaged_tool_system/part_numbers_test'
        part_numbers = [part for part in os.listdir(part_numbers_test)]

        # List Operation Numbers

        op_numbers = list(range(0, 901, 5))

        # Machine List

        machine_nums = [
            'MORI', 'OKK', 'MAZAK 101', 'MAZAK 102',
            'MAZAK 103', 'MAZAK 104', 'TOY 115', 'TOY 116',
            'MITSUI', 'NIIGATA 138', 'NIIGATA 139', 'OKUMA 187',
            'OKUMA 188', 'PRATT', 'MEGA', 'TACHII',
            'VDF', 'TOSH 195', 'TOSH 196', 'KARACHI 191'
        ]

        # END SELECTABLE OPTIONS ======================================================================================#

        # Major Analytic Frames =======================================================================================#

        # Create bottom buttons frame:

        button_frame = ttk.Frame(self)

        button_frame.grid(row=10, column=0, padx=5, pady=5, sticky='nw')

        # Create statistics frame

        statistics_label = ttk.Label(self, text="Statistics", font=("Helvetica", 12, "bold"))

        self.statistics_frame = ttk.LabelFrame(
            self, borderwidth=2,
            labelwidget=statistics_label,
            width=600,
            height=350
        )

        # Lock the frame from changing sizes

        self.statistics_frame.grid_propagate(False)

        self.statistics_frame.grid(row=0, column=1, padx=5, pady=5, sticky='n')

        # Create next and prev button frame

        self.buttons_frame = ttk.Frame(self.statistics_frame)
        self.buttons_frame.grid(row=10, column=0, columnspan=2, sticky='sw')

        # Create graph frame

        graph_label = ttk.Label(self, text="Logged Incidents", font=("Helvetica", 12, "bold"))

        self.graph_frame = ttk.LabelFrame(
            self,
            borderwidth=2,
            labelwidget=graph_label
        )

        self.graph_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n')

        # Create Part Frequency Frame

        self.part_frequency_frame = ttk.Frame(self)

        self.part_frequency_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n')

        # Create Machine Frequency Frame

        self.machine_frequency_frame = ttk.Frame(self)

        self.machine_frequency_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n')

        # Create All Tool Chart Frame

        self.all_tool_chart_frame = ttk.Frame(self)

        self.all_tool_chart_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n')

        # Create Top 5 Tools Frame

        self.top_five_tools_frame = ttk.Frame(self)

        self.top_five_tools_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n')

        # Initially hide the statistics frame

        self.statistics_frame.grid_remove()

        # Create all the GUI Statistic Labels

        self.tool_number_result = ttk.Label(self.statistics_frame, text="")
        self.tool_number_result.grid(row=0, column=0, sticky='nw')

        self.part_number_result = ttk.Label(self.statistics_frame, text="")
        self.part_number_result.grid(row=1, column=0, sticky='nw')

        self.operation_number_result = ttk.Label(self.statistics_frame, text="")
        self.operation_number_result.grid(row=2, column=0, sticky='nw')

        self.machine_result = ttk.Label(self.statistics_frame, text="")
        self.machine_result.grid(row=3, column=0, sticky='nw')

        self.description_result = ttk.Label(
            self.statistics_frame,
            text="",
            wraplength=600,
            anchor='w',
            justify='left'
        )

        self.description_result.grid(row=4, column=0, sticky='nw')

        self.operator_result = ttk.Label(self.statistics_frame, text="")
        self.operator_result.grid(row=5, column=0, sticky='nw')

        self.total_incidents = ttk.Label(self.statistics_frame, text="")
        self.total_incidents.grid(row=6, column=0, sticky='nw')

        self.date_result = ttk.Label(self.statistics_frame, text="")
        self.date_result.grid(row=7, column=0, sticky='nw')

        # Create Data Select Frame

        data_options_frame = tk.Frame(self)
        data_options_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nw')

        # END MAJOR ANALYTIC FRAMES ===================================================================================#

        # Store the results of the query based on data types for query functions

        self.data_search_results = []

        # Data Search Function

        def data_search():

            # Controller for next and prev buttons

            self.incident_indexer = 0

            # Function(s) to display queried data =====================================================================#

            def visualize_data():

                def visualize_tool_data(data_search_results):

                    # Create graph figure

                    tool_fig, ax = plt.subplots()

                    # Collect the data the graph will use

                    data = data_search_results

                    # Generate the X dates

                    dates = [datetime.strptime(item[-1], "%Y-%m-%d %I:%M %p") for item in data]

                    # Find the starting and end dates, include the first day zero'd to prevent errors

                    start_date = min(dates).replace(hour=0, minute=0, second=0, microsecond=0)
                    end_date = max(dates)

                    # Create the range of x values, or, dates

                    date_range = pd.date_range(start_date, end_date).to_pydatetime().tolist()

                    # Track the number of incidents and keep count

                    total_incidents = {date.date(): 0 for date in date_range}

                    # Create counter for incidents and remove time from date

                    for date in dates:
                        date_no_time = date.date()
                        total_incidents[date_no_time] += 1

                    # Assign the tracked incidents to y

                    y = pd.Series(total_incidents).cumsum().values

                    # Plot our data

                    ax.plot(date_range, y)

                    # Format x values to be readable

                    tool_fig.autofmt_xdate()

                    # Create out canvas

                    tool_canvas = FigureCanvasTkAgg(tool_fig, master=self.graph_frame)

                    # Create our widget

                    tool_canvas_widget = tool_canvas.get_tk_widget()

                    # Place the widget

                    tool_canvas_widget.grid(row=0, column=0, columnspan=10)

                def visualize_part_data(data_search_results):

                    # Create graph figure

                    part_fig, ax = plt.subplots()

                    # Collect the data the graph will use

                    data = data_search_results

                    # Generate the X dates

                    dates = [datetime.strptime(item[-1], "%Y-%m-%d %I:%M %p") for item in data]

                    # Find the starting and end dates, include the first day zero'd to prevent errors

                    start_date = min(dates).replace(hour=0, minute=0, second=0, microsecond=0)
                    end_date = max(dates)

                    # Create the range of x values, or, dates

                    date_range = pd.date_range(start_date, end_date).to_pydatetime().tolist()

                    # Track the number of incidents and keep count

                    total_incidents = {date.date(): 0 for date in date_range}

                    # Create counter for incidents and remove time from date

                    for date in dates:
                        date_no_time = date.date()
                        total_incidents[date_no_time] += 1

                    # Assign the tracked incidents to y

                    y = pd.Series(total_incidents).cumsum().values

                    # Plot our data

                    ax.plot(date_range, y)

                    # Format x values to be readable

                    part_fig.autofmt_xdate()

                    # Create out canvas

                    op_canvas = FigureCanvasTkAgg(part_fig, master=self.graph_frame)

                    # Create our widget

                    part_canvas_widget = op_canvas.get_tk_widget()

                    # Place the widget

                    part_canvas_widget.grid(row=0, column=0, columnspan=10)

                def visualize_operation_data(data_search_results):

                    # Create graph figure

                    op_fig, ax = plt.subplots()

                    # Collect the data the graph will use

                    data = data_search_results

                    # Generate the X dates

                    dates = [datetime.strptime(item[-1], "%Y-%m-%d %I:%M %p") for item in data]

                    # Find the starting and end dates, include the first day zero'd to prevent errors

                    start_date = min(dates).replace(hour=0, minute=0, second=0, microsecond=0)
                    end_date = max(dates)

                    # Create the range of x values, or, dates

                    date_range = pd.date_range(start_date, end_date).to_pydatetime().tolist()

                    # Track the number of incidents and keep count

                    total_incidents = {date.date(): 0 for date in date_range}

                    # Create counter for incidents and remove time from date

                    for date in dates:
                        date_no_time = date.date()
                        total_incidents[date_no_time] += 1

                    # Assign the tracked incidents to y

                    y = pd.Series(total_incidents).cumsum().values

                    # Plot our data

                    ax.plot(date_range, y)

                    # Format x values to be readable

                    op_fig.autofmt_xdate()

                    # Create out canvas

                    op_canvas = FigureCanvasTkAgg(op_fig, master=self.graph_frame)

                    # Create our widget

                    op_canvas_widget = op_canvas.get_tk_widget()

                    # Place the widget

                    op_canvas_widget.grid(row=0, column=0, columnspan=10)

                def visualize_machine_data(data_search_results):

                    # Create graph figure

                    machine_fig, ax = plt.subplots()

                    # Collect the data the graph will use

                    data = data_search_results

                    # Generate the X dates

                    dates = [datetime.strptime(item[-1], "%Y-%m-%d %I:%M %p") for item in data]

                    # Find the starting and end dates, include the first day zero'd to prevent errors

                    start_date = min(dates).replace(hour=0, minute=0, second=0, microsecond=0)
                    end_date = max(dates)

                    # Create the range of x values, or, dates

                    date_range = pd.date_range(start_date, end_date).to_pydatetime().tolist()

                    # Track the number of incidents and keep count

                    total_incidents = {date.date(): 0 for date in date_range}

                    # Create counter for incidents and remove time from date

                    for date in dates:
                        date_no_time = date.date()
                        total_incidents[date_no_time] += 1

                    # Assign the tracked incidents to y

                    y = pd.Series(total_incidents).cumsum().values

                    # Plot our data

                    ax.plot(date_range, y)

                    # Format x values to be readable

                    machine_fig.autofmt_xdate()

                    # Create out canvas

                    machine_canvas = FigureCanvasTkAgg(machine_fig, master=self.graph_frame)

                    # Create our widget

                    machine_canvas_widget = machine_canvas.get_tk_widget()

                    # Place the widget

                    machine_canvas_widget.grid(row=0, column=0, columnspan=10)

                def visualize_operator_data(data_search_results):

                    # Create graph figure

                    operator_fig, ax = plt.subplots()

                    # Collect the data the graph will use

                    data = data_search_results

                    # Generate the X dates

                    dates = [datetime.strptime(item[-1], "%Y-%m-%d %I:%M %p") for item in data]

                    # Find the starting and end dates, include the first day zero'd to prevent errors

                    start_date = min(dates).replace(hour=0, minute=0, second=0, microsecond=0)
                    end_date = max(dates)

                    # Create the range of x values, or, dates

                    date_range = pd.date_range(start_date, end_date).to_pydatetime().tolist()

                    # Track the number of incidents and keep count

                    total_incidents = {date.date(): 0 for date in date_range}

                    # Create counter for incidents and remove time from date

                    for date in dates:
                        date_no_time = date.date()
                        total_incidents[date_no_time] += 1

                    # Assign the tracked incidents to y

                    y = pd.Series(total_incidents).cumsum().values

                    # Plot our data

                    ax.plot(date_range, y)

                    # Format x values to be readable

                    operator_fig.autofmt_xdate()

                    # Create out canvas

                    operator_canvas = FigureCanvasTkAgg(operator_fig, master=self.graph_frame)

                    # Create our widget

                    operator_canvas_widget = operator_canvas.get_tk_widget()

                    # Place the widget

                    operator_canvas_widget.grid(row=0, column=0, columnspan=10)

                if self.data_name == "Tool Data":
                    visualize_tool_data(self.data_search_results)

                if self.data_name == "Part Data":
                    visualize_part_data(self.data_search_results)

                if self.data_name == "Operation Data":
                    visualize_operation_data(self.data_search_results)

                if self.data_name == "Machine Data":
                    visualize_machine_data(self.data_search_results)

                if self.data_name == "Operator Data":
                    visualize_operator_data(self.data_search_results)

            # Arrow Buttons Functions To Move Through Query Results ===================================================#

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
            # END OF ARROW BUTTON FUNCTIONS ===========================================================================#

            # Conditional Displays of Queried Data ====================================================================#

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
                    self.graph_frame.grid()
                    self.part_frequency_frame.grid_remove()
                    self.all_tool_chart_frame.grid_remove()
                    self.top_five_tools_frame.grid_remove()
                    self.machine_frequency_frame.grid_remove()

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

                    next_button = ttk.Button(
                        self.buttons_frame,
                        text=">>",
                        command=lambda: next_incident_button()
                    )

                    next_button.grid(row=8, column=1, sticky='nw')

                    # Previous Incident Button

                    prev_button = ttk.Button(
                        self.buttons_frame,
                        text="<<",
                        command=lambda: prev_incident_button()
                    )

                    prev_button.grid(row=8, column=0, sticky='nw')

                    visualize_data()
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
                    self.graph_frame.grid()
                    self.part_frequency_frame.grid_remove()
                    self.all_tool_chart_frame.grid_remove()
                    self.top_five_tools_frame.grid_remove()
                    self.machine_frequency_frame.grid_remove()

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

                    next_button = ttk.Button(
                        self.buttons_frame,
                        text=">>",
                        command=lambda: next_incident_button()
                    )

                    next_button.grid(row=8, column=1, sticky='nw')

                    # Previous Incident Button

                    prev_button = ttk.Button(
                        self.buttons_frame,
                        text="<<",
                        command=lambda: prev_incident_button()
                    )

                    prev_button.grid(row=8, column=0, sticky='nw')

                    visualize_data()
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
                    self.graph_frame.grid()
                    self.part_frequency_frame.grid_remove()
                    self.all_tool_chart_frame.grid_remove()
                    self.top_five_tools_frame.grid_remove()
                    self.machine_frequency_frame.grid_remove()

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

                    next_button = ttk.Button(
                        self.buttons_frame,
                        text=">>",
                        command=lambda: next_incident_button()
                    )

                    next_button.grid(row=8, column=1, sticky='nw')

                    # Previous Incident Button

                    prev_button = ttk.Button(
                        self.buttons_frame,
                        text="<<",
                        command=lambda: prev_incident_button()
                    )

                    prev_button.grid(row=8, column=0, sticky='nw')

                    visualize_data()
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
                    self.graph_frame.grid()
                    self.part_frequency_frame.grid_remove()
                    self.all_tool_chart_frame.grid_remove()
                    self.top_five_tools_frame.grid_remove()
                    self.machine_frequency_frame.grid_remove()

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

                    next_button = ttk.Button(
                        self.buttons_frame,
                        text=">>",
                        command=lambda: next_incident_button()
                    )

                    next_button.grid(row=8, column=1, sticky='nw')

                    # Previous Incident Button

                    prev_button = ttk.Button(
                        self.buttons_frame,
                        text="<<",
                        command=lambda: prev_incident_button()
                    )

                    prev_button.grid(row=8, column=0, sticky='nw')

                    visualize_data()
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
                    self.graph_frame.grid()
                    self.part_frequency_frame.grid_remove()
                    self.all_tool_chart_frame.grid_remove()
                    self.top_five_tools_frame.grid_remove()
                    self.machine_frequency_frame.grid_remove()

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

                    next_button = ttk.Button(
                        self.buttons_frame,
                        text=">>",
                        command=lambda: next_incident_button()
                    )

                    next_button.grid(row=8, column=1, sticky='nw')

                    # Previous Incident Button

                    prev_button = ttk.Button(
                        self.buttons_frame,
                        text="<<",
                        command=lambda: prev_incident_button()
                    )

                    prev_button.grid(row=8, column=0, sticky='nw')

                    visualize_data()
                    self.update_idletasks()

                except IndexError:

                    messagebox.showerror(
                        title="ERROR: Database Search",
                        message="The current search inquery was not found in the database. If this inquery should exist"
                                " in the database, contact the System Administrator."
                    )
                    return

            # END OF CONDITIONAL QUERY DISPLAYS =======================================================================#

        # Other Statistics Menu Functions =============================================================================#

        # Function to control what is displayed from the Other Statistics Dropdown Menu

        def toolbar_options_select(selected_option):

            if selected_option == 'Part Frequency Chart':
                part_frequency_chart()

            if selected_option == 'All Tools':
                all_tools_chart()

            if selected_option == 'Top 5 Tools':
                top_five_tools()

            if selected_option == 'Machine Frequency Chart':
                machine_frequency_chart()

        # Function for Part Frequency Displays

        def part_frequency_chart():

            self.selected_month = tk.StringVar()

            def close_graph():
                self.part_frequency_frame.grid_forget()
                selected_option.set('Other Statistics')

            def display_part_all_time():

                # Clear Other the Statistics Frame and Graph Frame

                self.statistics_frame.grid_remove()
                self.graph_frame.grid_remove()
                self.all_tool_chart_frame.grid_remove()
                self.top_five_tools_frame.grid_remove()
                self.machine_frequency_frame.grid_remove()

                # Clear the previous contents of the frame

                for widget in self.part_frequency_frame.winfo_children():
                    widget.destroy()

                # Create the plot

                part_frequency_figure = plt.Figure(figsize=(7, 4), dpi=100)
                part_frequency_ax = part_frequency_figure.add_subplot(111)

                part_frequency_widget = FigureCanvasTkAgg(part_frequency_figure, self.part_frequency_frame)
                part_frequency_widget.get_tk_widget().grid(row=0, column=0, sticky='nsew')

                parts_search = part_frequency_search(part_numbers)

                # Gather data

                parts = list(parts_search.keys())
                parts_freq = list(parts_search.values())

                # Create bar chart

                part_frequency_ax.barh(parts, parts_freq, color='red', edgecolor='black')

                part_frequency_ax.set_xlabel('Total Damaged Tooling')
                part_frequency_ax.set_ylabel('Part Numbers')
                part_frequency_ax.set_title('Total Damaged Tools Per Part')

                # Part Frequency Button Frame

                pfb_frame = ttk.Frame(self.part_frequency_frame)
                pfb_frame.grid(row=1, column=0)

                close_button = ttk.Button(
                    pfb_frame,
                    text="Close",
                    command=close_graph
                )

                all_time_button = ttk.Button(
                    pfb_frame,
                    text='All Time',
                    command=display_part_all_time
                )

                # Month Select Menu Drop Down

                select_month_button = ttk.Menubutton(
                    pfb_frame,
                    text='Select Month'
                )

                # Create Month Selection
                month_dropdown = tk.Menu(select_month_button, tearoff=False)
                select_month_button.configure(menu=month_dropdown)

                months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                          'August', 'September', 'October', 'November', 'December']

                for month in months:
                    month_dropdown.add_command(label=month, command=lambda month=month: self.selected_month.set(month))

                close_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')
                all_time_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')
                select_month_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

                if not parts or not parts_freq:
                    messagebox.showerror(
                        "ERROR: No Data", "No data available for the requested month."
                                          " Please contact the System Administrator if the issue persists.")

                part_frequency_figure.tight_layout()

                self.part_frequency_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n')
                self.part_frequency_frame.update_idletasks()

            # Show data based on selected month

            def display_part_select_month(selected_month):

                # Clear Other the Statistics Frame and Graph Frame

                self.statistics_frame.grid_remove()
                self.graph_frame.grid_remove()
                self.all_tool_chart_frame.grid_remove()
                self.top_five_tools_frame.grid_remove()
                self.part_frequency_frame.grid_remove()

                # Clear the previous contents of the frame

                for widget in self.part_frequency_frame.winfo_children():
                    widget.destroy()

                months_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
                               'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

                query_num = months_dict[self.selected_month.get()]

                selected_month_data = selected_month_search(query_num, 'part')

                # Create the plot

                part_frequency_figure = plt.Figure(figsize=(7, 4), dpi=100)
                part_frequency_ax = part_frequency_figure.add_subplot(111)

                part_frequency_widget = FigureCanvasTkAgg(part_frequency_figure, self.part_frequency_frame)
                part_frequency_widget.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky='n')
                parts_search = selected_month_data

                # Gather data

                parts = list(parts_search.keys())
                parts_freq = list(parts_search.values())

                # Create bar chart

                part_frequency_ax.barh(parts, parts_freq, color='red', edgecolor='black')

                part_frequency_ax.set_xlabel(f'Total Damaged Tooling ({self.selected_month.get()})')
                part_frequency_ax.set_ylabel('Part Numbers')
                part_frequency_ax.set_title(f'Total Damaged Tools Per part ({self.selected_month.get()})')

                part_frequency_figure.tight_layout()

                self.part_frequency_frame.grid(row=0, column=0, padx=5, pady=5)
                self.part_frequency_frame.update_idletasks()

                # Part Frequency Button Frame

                pfb_frame = ttk.Frame(self.part_frequency_frame)

                pfb_frame.grid(row=1, column=0)

                close_button = ttk.Button(
                    pfb_frame,
                    text="Close",
                    command=close_graph
                )

                all_time_button = ttk.Button(

                    pfb_frame,
                    text='All Time',
                    command=display_part_all_time
                )

                # Month Select Menu Drop Down

                select_month_button = ttk.Menubutton(

                    pfb_frame,
                    text='Select Month'
                )

                # Create Month Selection

                month_dropdown = tk.Menu(select_month_button, tearoff=False)
                select_month_button.configure(menu=month_dropdown)

                months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                          'August', 'September', 'October', 'November', 'December']

                for month in months:
                    month_dropdown.add_command(label=month, command=lambda month=month: self.selected_month.set(month))

                close_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')

                all_time_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

                select_month_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

                if not parts or not parts_freq:
                    messagebox.showerror(
                        "ERROR: No Data", "No data available for requested month."
                                          " Please contact System Administrator if issue persist")

                    return

            display_part_all_time()

            # Trace the Selected Month

            self.selected_month.trace_add("write", lambda *args: display_part_select_month(self.selected_month.get()))

        # Function for Machine Frequency Displays

        def machine_frequency_chart():

            # Create Variable for Month Selection

            self.selected_month = tk.StringVar()

            def close_graph():
                self.machine_frequency_frame.grid_forget()
                selected_option.set('Other Statistics')

            def display_all_time():

                # Clear Other the Statistics Frame and Graph Frame

                self.statistics_frame.grid_remove()
                self.graph_frame.grid_remove()
                self.all_tool_chart_frame.grid_remove()
                self.top_five_tools_frame.grid_remove()
                self.part_frequency_frame.grid_remove()

                # Clear the previous contents of the frame

                for widget in self.machine_frequency_frame.winfo_children():
                    widget.destroy()

                # Create the plot

                machine_frequency_figure = plt.Figure(figsize=(7, 4), dpi=100)
                machine_frequency_ax = machine_frequency_figure.add_subplot(111)

                machine_frequency_widget = FigureCanvasTkAgg(machine_frequency_figure, self.machine_frequency_frame)
                machine_frequency_widget.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky='n')
                machines_search = machine_frequency_search(machine_nums)

                # Gather data

                machines = list(machines_search.keys())
                machines_freq = list(machines_search.values())

                # Create bar chart
                machine_frequency_ax.barh(machines, machines_freq, color='red', edgecolor='black')

                machine_frequency_ax.set_xlabel('Total Damaged Tooling (All Time)')
                machine_frequency_ax.set_ylabel('Machine')
                machine_frequency_ax.set_title('Total Damaged Tools Per Machine (All Time)')

                machine_frequency_figure.tight_layout()

                self.machine_frequency_frame.grid(row=0, column=0, padx=5, pady=5)
                self.machine_frequency_frame.update_idletasks()

                # Machine Frequency Button Frame

                mfb_frame = ttk.Frame(self.machine_frequency_frame)

                mfb_frame.grid(row=1, column=0)

                close_button = ttk.Button(
                    mfb_frame,
                    text="Close",
                    command=close_graph
                )

                all_time_button = ttk.Button(

                    mfb_frame,
                    text='All Time',
                    command=display_all_time
                )

                # Month Select Menu Drop Down

                select_month_button = ttk.Menubutton(

                    mfb_frame,
                    text='Select Month'
                )

                # Create Month Selection

                month_dropdown = tk.Menu(select_month_button, tearoff=False)
                select_month_button.configure(menu=month_dropdown)

                months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                          'August', 'September', 'October', 'November', 'December']

                for month in months:
                    month_dropdown.add_command(label=month, command=lambda month=month: self.selected_month.set(month))

                close_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')

                all_time_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

                select_month_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

            # Display data based on selected month

            def display_select_month(selected_month):

                # Clear Other the Statistics Frame and Graph Frame

                self.statistics_frame.grid_remove()
                self.graph_frame.grid_remove()
                self.all_tool_chart_frame.grid_remove()
                self.top_five_tools_frame.grid_remove()
                self.part_frequency_frame.grid_remove()

                # Clear the previous contents of the frame

                for widget in self.machine_frequency_frame.winfo_children():
                    widget.destroy()

                months_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
                               'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

                query_num = months_dict[selected_month]

                selected_month_data = selected_month_search(query_num, 'mc')

                # Create the plot

                machine_frequency_figure = plt.Figure(figsize=(7, 4), dpi=100)
                machine_frequency_ax = machine_frequency_figure.add_subplot(111)

                machine_frequency_widget = FigureCanvasTkAgg(machine_frequency_figure, self.machine_frequency_frame)
                machine_frequency_widget.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky='n')
                machines_search = selected_month_data

                # Gather data

                machines = list(machines_search.keys())
                machines_freq = list(machines_search.values())

                # Create bar chart
                machine_frequency_ax.barh(machines, machines_freq, color='red', edgecolor='black')

                machine_frequency_ax.set_xlabel(f'Total Damaged Tooling ({self.selected_month.get()})')
                machine_frequency_ax.set_ylabel('Machine')
                machine_frequency_ax.set_title(f'Total Damaged Tools Per Machine ({self.selected_month.get()})')

                machine_frequency_figure.tight_layout()

                self.machine_frequency_frame.grid(row=0, column=0, padx=5, pady=5)
                self.machine_frequency_frame.update_idletasks()

                # Machine Frequency Button Frame

                mfb_frame = ttk.Frame(self.machine_frequency_frame)

                mfb_frame.grid(row=1, column=0)

                close_button = ttk.Button(
                    mfb_frame,
                    text="Close",
                    command=close_graph
                )

                all_time_button = ttk.Button(

                    mfb_frame,
                    text='All Time',
                    command=display_all_time
                )

                # Month Select Menu Drop Down

                select_month_button = ttk.Menubutton(

                    mfb_frame,
                    text='Select Month'
                )

                # Create Month Selection

                month_dropdown = tk.Menu(select_month_button, tearoff=False)
                select_month_button.configure(menu=month_dropdown)

                months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                          'August', 'September', 'October', 'November', 'December']

                for month in months:
                    month_dropdown.add_command(label=month, command=lambda month=month: self.selected_month.set(month))

                close_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')

                all_time_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

                select_month_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

                if not machines or not machines_freq:
                    messagebox.showerror(
                        "ERROR: No Data", "No data available for requested month."
                                          " Please contact System Administrator if issue persist")

                    return

            display_all_time()

            # Trace the Selected Month

            self.selected_month.trace_add("write", lambda *args: display_select_month(self.selected_month.get()))

        # All Tools Chart Functions

        def all_tools_chart():

            # Clear Other the Statistics Frame and Graph Frame

            self.statistics_frame.grid_remove()
            self.graph_frame.grid_remove()
            self.top_five_tools_frame.grid_remove()
            self.part_frequency_frame.grid_remove()
            self.machine_frequency_frame.grid_remove()

            # Clear the previous contents of the frame

            for widget in self.all_tool_chart_frame.winfo_children():
                widget.destroy()

            data = all_tools_search()
            data = data[::-1]

            tools_columns = ['Tool No.', 'Part No.', 'Op No.', 'Desc.', 'Machine', 'Operator', 'Date']

            tools_tree = ttk.Treeview(self.all_tool_chart_frame, columns=tools_columns, show='headings')

            # Add the scrollbar

            scrollbar = ttk.Scrollbar(self.all_tool_chart_frame, orient='vertical', command=tools_tree.yview)

            # Configure tree view

            tools_tree.configure(yscrollcommand=scrollbar.set)

            # Create column headings and width

            for col in tools_columns:
                tools_tree.heading(col, text=col)
                tools_tree.column(col, width=155)

            for tool in data:
                tools_tree.insert('', 'end', values=tool)

            # Grid tool tree

            tools_tree.grid(row=0, column=0, sticky='nsew')

            self.all_tool_chart_frame.grid_rowconfigure(0, weight=1)
            self.all_tool_chart_frame.grid_columnconfigure(0, weight=1)

            scrollbar.grid(row=0, column=1, sticky='ns')

            # Create close button

            def close_graph():
                self.all_tool_chart_frame.grid_forget()
                selected_option.set('Other Statistics')

            close_button = ttk.Button(
                self.all_tool_chart_frame,
                text="Close",
                command=close_graph
            )

            close_button.grid(row=1, column=0, columnspan=2)

            self.all_tool_chart_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n')
            self.all_tool_chart_frame.update_idletasks()

        def top_five_tools():

            # Clear Other the Statistics Frame and Graph Frame

            self.statistics_frame.grid_remove()
            self.graph_frame.grid_remove()
            self.all_tool_chart_frame.grid_remove()
            self.part_frequency_frame.grid_remove()
            self.machine_frequency_frame.grid_remove()

            # Clear the previous contents of the frame

            for widget in self.top_five_tools_frame.winfo_children():
                widget.destroy()

            data = top_five_tools_search()

            top_five_inner_frame = ttk.LabelFrame(self.top_five_tools_frame, text="Top 5 Tools")

            top_five_inner_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

            ranks = ttk.Label(
                top_five_inner_frame,
                text=f"1: Tool Number: {data[0][0][0]}, Part: {data[0][0][1]}, Op: {data[0][0][2]},"
                     f" Total Incidents: {data[0][1]}\n"
                     f"2: Tool Number: {data[1][0][0]}, Part: {data[1][0][1]}, Op: {data[1][0][2]},"
                     f" Total Incidents: {data[1][1]}\n"
                     f"3: Tool Number: {data[2][0][0]}, Part: {data[2][0][1]}, Op: {data[2][0][2]},"
                     f" Total Incidents: {data[2][1]}\n"
                     f"4: Tool Number: {data[3][0][0]}, Part: {data[3][0][1]}, Op: {data[3][0][2]},"
                     f" Total Incidents: {data[3][1]}\n"
                     f"5: Tool Number: {data[4][0][0]}, Part: {data[4][0][1]}, Op: {data[4][0][2]},"
                     f" Total Incidents: {data[4][1]}",
                font=("Helvetica", 12, "bold")
            )

            ranks.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

            def close_graph():
                self.top_five_tools_frame.grid_forget()
                selected_option.set('Other Statistics')

            close_button = ttk.Button(
                self.top_five_tools_frame,
                text="Close",
                command=close_graph
            )

            close_button.grid(row=1, column=0, columnspan=2)

            self.top_five_tools_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n')
            self.top_five_tools_frame.update_idletasks()

        # END OTHER STATISTICS MENU FUNCTIONS =========================================================================#

        # GUI Components ==============================================================================================#

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

        # List Machines

        # Use fetch_machines from machine database.py

        machines_list = fetch_machines()
        selected_machine = tk.StringVar(self)
        selected_machine.set("----")  # Default option

        # Create Data Select Header

        data_select_label = ttk.Label(data_options_frame, text="Select Data to Display", font=("Helvetica", 12, "bold"))
        data_select_label.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Create Data Field Requirement Header

        data_fields_label = ttk.Label(data_options_frame, text=f"Enter Required Fields for {self.data_name}",
                                      font=("Helvetica", 12, "bold"))
        data_fields_label.grid(row=7, column=0, padx=5, pady=5, sticky='nw')

        # Data Buttons ================================================================================================#

        # Tool Data Button

        tool_data_button = ttk.Button(
            data_options_frame,
            text="Tool Data",
            command=lambda: (show_field(self.frames[0], self.frames), update_data_name("Tool Data"))
        )
        tool_data_button.grid(row=1, column=0, padx=5, pady=5, sticky='nw')

        # Tool Data Fields

        tool_fields = ttk.Frame(tool_data_frame)
        ttk.Label(tool_fields, text="Part Number:").grid(row=0, column=0)
        part_number_combobox = ttk.Combobox(tool_fields, values=part_numbers)
        part_number_combobox.grid(row=0, column=1)
        part_number_combobox.configure(state="normal")

        ttk.Label(tool_fields, text="Operation:").grid(row=1, column=0)
        op_number_combobox = ttk.Combobox(tool_fields, values=op_numbers)
        op_number_combobox.grid(row=1, column=1)
        op_number_combobox.configure(state="normal")

        ttk.Label(tool_fields, text="Machine:").grid(row=2, column=0)
        machine_combobox = ttk.Combobox(tool_fields, values=machines_list)
        machine_combobox.grid(row=2, column=1)
        machine_combobox.configure(state="normal")

        ttk.Label(tool_fields, text="Tool Number:").grid(row=3, column=0)
        tool_number_combobox = ttk.Combobox(tool_fields, values=tool_numbers)
        tool_number_combobox.grid(row=3, column=1)
        tool_number_combobox.configure(state="normal")

        tool_fields.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Part Data Button

        part_data_button = ttk.Button(
            data_options_frame,
            text="Part Data",
            command=lambda: (show_field(self.frames[1], self.frames), update_data_name("Part Data"))
        )
        part_data_button.grid(row=2, column=0, padx=5, pady=5, sticky='nw')

        # Part Data Fields

        part_fields = tk.Frame(part_data_frame)
        ttk.Label(part_fields, text="Part Number:").grid(row=0, column=0)
        part_number_combobox_2 = ttk.Combobox(part_fields, values=part_numbers)
        part_number_combobox_2.grid(row=0, column=1)
        part_number_combobox_2.configure(state="normal")

        part_fields.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Operation Data Button

        operation_data_button = ttk.Button(
            data_options_frame,
            text="Operation Data",
            command=lambda: (show_field(self.frames[2], self.frames), update_data_name("Operation Data"))
        )
        operation_data_button.grid(row=3, column=0, padx=5, pady=5, sticky='nw')

        # Operation Data Fields

        operation_fields = tk.Frame(operation_data_frame)
        ttk.Label(operation_fields, text="Part Number:").grid(row=0, column=0)
        part_number_combobox_3 = ttk.Combobox(operation_fields, values=part_numbers)
        part_number_combobox_3.grid(row=0, column=1)
        part_number_combobox_3.configure(state="normal")

        ttk.Label(operation_fields, text="Operation Number:").grid(row=1, column=0)
        op_number_combobox_2 = ttk.Combobox(operation_fields, values=op_numbers)
        op_number_combobox_2.grid(row=1, column=1)
        op_number_combobox_2.configure(state="normal")

        operation_fields.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Machine Data Button

        machine_data_button = ttk.Button(
            data_options_frame,
            text="Machine Data",
            command=lambda: (show_field(self.frames[3], self.frames), update_data_name("Machine Data"))
        )
        machine_data_button.grid(row=4, column=0, padx=5, pady=5, sticky='nw')

        # Machine Data Fields

        machine_fields = tk.Frame(machine_data_frame)
        ttk.Label(machine_fields, text="Select Machine:").grid(row=0, column=0)
        machine_combobox_2 = ttk.Combobox(machine_fields, values=machines_list)
        machine_combobox_2.grid(row=0, column=1)
        machine_combobox_2.configure(state="normal")

        machine_fields.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Operator Data Button

        operator_data_button = ttk.Button(
            data_options_frame,
            text="Operator Data",
            command=lambda: (show_field(self.frames[4], self.frames), update_data_name("Operator Data"))
        )
        operator_data_button.grid(row=5, column=0, padx=5, pady=5, sticky='nw')

        # Operator Data Fields

        operator_fields = ttk.Frame(operator_data_frame)
        tk.Label(operator_fields, text="Operator Name:").grid(row=0, column=0)
        operator_name = ttk.Entry(operator_fields)
        operator_name.grid(row=0, column=1)

        operator_fields.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Toolbar Menu

        selected_option = tk.StringVar(self)
        self.toolbar_options.insert(0, "Other Statistics")
        selected_option.set(self.toolbar_options[0])
        toolbar_menu = ttk.OptionMenu(
            data_options_frame,
            selected_option,
            *self.toolbar_options,
            command=toolbar_options_select
        )

        toolbar_menu.grid(row=6, column=0, padx=5, pady=5, sticky='nw')

        # Back To Login Screen

        back_button = ttk.Button(button_frame, text="Back", command=lambda: controller.show_frame(LoginScreen))
        back_button.pack(side='left', padx=5)

        # Data Search Button

        search_button = ttk.Button(button_frame, text="Search", command=data_search)
        search_button.pack(side='left', padx=5)

        # END GUI COMPONENTS / DATA BUTTONS ===========================================================================#

# END ADMIN ACCESS DATA ANALYSIS ======================================================================================#

# Admin Login Screen ==================================================================================================#


class AdminLoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        def admin_login():

            admin_id = admin_id_entry.get()

            # *** BAD PRACTICE FIX ***
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

        # GUI COMPONENTS ==============================================================================================#

        # Admin Login

        admin_id_label = ttk.Label(self, text="Admin ID:")
        admin_id_label.grid(row=0, padx=10, column=0)
        admin_id_entry = ttk.Entry(self, show="*")
        admin_id_entry.grid(row=1, column=0, padx=10, sticky='nw')

        # Login Button

        login_button = ttk.Button(self, text="Login", command=admin_login)
        login_button.grid(row=2, column=0, padx=10, sticky='nw')

        # Back To Login Screen

        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(LoginScreen))
        back_button.grid(row=3, column=0, padx=10, sticky='nw')

        # END GUI COMPONENTS ==========================================================================================#

# END ADMIN LOGIN SCREEN ==============================================================================================#

# Test Functions ======================================================================================================#

# clear_database("employee.db", "employees")

# top_five_tools_search()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
