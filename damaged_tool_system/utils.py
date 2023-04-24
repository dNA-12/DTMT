# Use this file for shared function amid other files

import sqlite3
from db_context_manager import DatabaseConnection, DatabaseCursor

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
