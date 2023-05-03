# Use this file for shared function amid other files

import sqlite3
import tkinter as tk
from tkinter import ttk

from db_context_manager import DatabaseConnection, DatabaseCursor

#======================================================================================================================#
# DATABASE UTILITY FUNCTIONS
#======================================================================================================================#
# Used to grab machines from the machine database!


def fetch_machines():
    conn = sqlite3.connect("machines.db")
    c = conn.cursor()
    c.execute("SELECT * FROM machines")
    machines = c.fetchall()
    conn.close()
    return [machine[0] for machine in machines]

# Used to grab specific records from any database


def fetch_record(database_name, table_name, primary_key_column, primary_key_value):
    with DatabaseConnection(database_name) as conn:
        with conn.cursor() as c:

            c.execute(f"SELECT * FROM {table_name} WHERE {primary_key_column} = :primary_key_value",
                      {'primary_key_value': primary_key_value})
            record = c.fetchone()

    return record


# Used to fetch ALL records of a database


def fetch_all_records(database_name, table_name):
    with DatabaseConnection(database_name) as conn:
        with DatabaseCursor(conn) as c:
            c.execute(f"SELECT * FROM {table_name}")
            records = c.fetchall()
    return records

# Used to clear data_base


def clear_database(database, table):
    with DatabaseConnection(database) as conn:
        with DatabaseCursor(conn) as c:

            c.execute(f"select * FROM {table};")
            previous_data = c.fetchall()

            if previous_data:

                print(f"Current data in {table}")

                for data in previous_data:
                    print(data)
            else:
                print("Table is already empty.")

            try:
                c.execute(f"DELETE FROM {table};")
                conn.commit()

            except sqlite3.Error as e:
                print(f"An error occurred while deleting rows from {table}: {e}")

            finally:
                if previous_data:

                    print(f"Current data in {table}")

                    for data in previous_data:
                        print(data)
                else:
                    print("CLEARED!")


# def fetch_data_from_db():
#     conn = sqlite3.connect('your_database.db')  # Replace with the name of your database file
#     cursor = conn.cursor()
#
#     cursor.execute('SELECT column_name FROM your_table_name')  # Replace with your table and column names
#     items = [row[0] for row in cursor.fetchall()]
#
#     conn.close()
#     return items

#======================================================================================================================#
# GUI Functions
#======================================================================================================================#

# Used to create searchable menus

def create_searchable_dropdown(master, options, title, **kwargs):
    title_label = tk.Label(master, text=title)
    title_label.pack()

    def on_entry_changed(*args):
        search = entry_var.get().lower()
        filtered_options = [opt for opt in options if search in str(opt).lower()]

        listbox.delete(0, tk.END)
        for item in filtered_options:
            listbox.insert(tk.END, item)

    def on_listbox_select(event):
        selected_indices = listbox.curselection()
        if selected_indices:
            selected_value = listbox.get(selected_indices)
            selected_option.set(selected_value)
            entry_var.set(selected_value)

    entry_var = tk.StringVar()
    entry = tk.Entry(master, textvariable=entry_var, **kwargs)
    entry.pack()

    selected_option = tk.StringVar()

    # Create a frame to hold Listbox and Scrollbar
    listbox_frame = tk.Frame(master)
    listbox_frame.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=listbox.yview)
    listbox.bind("<<ListboxSelect>>", on_listbox_select)

    entry_var.trace_add("write", on_entry_changed)
    on_entry_changed()

    return entry, listbox, selected_option
