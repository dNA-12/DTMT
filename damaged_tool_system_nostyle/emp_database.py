import sqlite3
from db_context_manager import DatabaseConnection, DatabaseCursor
from utils import fetch_record
from tkinter import messagebox

# Use this in main.py to add users to the employee database


def add_employee_db(created_user_info):
    with DatabaseConnection("employee.db") as conn:
        with DatabaseCursor(conn) as c:

            # Check if the employee already exists in the database
            c.execute("SELECT * FROM employees WHERE emp_num = :emp_num", {'emp_num': created_user_info[0]})
            result = c.fetchone()

            # If the employee is not in the database, insert the employee
            if result is None:
                c.execute(
                    "INSERT INTO employees VALUES (:emp_num, :emp_name, :emp_mc)",
                    {'emp_num': created_user_info[0], 'emp_name': created_user_info[1], 'emp_mc': created_user_info[2]}
                )
                messagebox.showinfo(
                    title="Success",
                    message="User successfully created!\nYou will be returned to the Login Screen now."
                )

                print("Employee Added")
                conn.commit()
                return True

            else:

                messagebox.showerror(
                    title="ERROR: Database",
                    message="User already present in database.\nIf issue persist, see System Administrator."
                )
                return False
    return


# Use this to create the table for the user database


def create_employees_table():
    with DatabaseConnection("employee.db") as conn:
        with DatabaseCursor(conn) as c:
            c.execute("""CREATE TABLE IF NOT EXISTS employees (
                            emp_num INTEGER PRIMARY KEY,
                            emp_name TEXT,
                            emp_mc TEXT
                        )""")
        conn.commit()

# Used to check for specific records of the employee data


def emp_db_check(employee_num):

    employee_num = created_user_info[0]
    database_name = "employee.db"
    table_name = "employees"
    primary_key_column = "emp_num"

    added_emp = fetch_record(database_name, table_name, primary_key_column, employee_num)

    if added_emp:
        print(f"Employee {added_emp[1]} with employee number{added_emp[0]} was added to the database.")
    else:
        print(f"Employee number {employee_num} not in database.")


def check_for_emp(emp_num):
    with DatabaseConnection("employee.db") as conn:
        with DatabaseCursor(conn) as c:

            # Check if the employee already exists in the database
            c.execute("SELECT * FROM employees WHERE emp_num = :emp_num", {'emp_num': emp_num})
            result = c.fetchone()

            if result is None:
                messagebox.showerror(
                    title="ERROR: Employee not found",
                    message="The employee number you entered was not found in the DTMT Database.\n"
                            "Please try again. If the issue persist,"
                            " attempt to register this employee number or see System Administrator"
                )
                print("Login Failure")
                return False

            else:
                print("Login Successful!")
                return True


def fetch_employee_name(emp_num):
    with DatabaseConnection("employee.db") as conn:
        with DatabaseCursor(conn) as c:

            c.execute("SELECT emp_name FROM employees WHERE emp_num=?", (emp_num,))
            emp_name = c.fetchone()

            if emp_name:
                return emp_name[0]
            else:
                print("ERROR: Could not find employee name with passed emp_num!")
