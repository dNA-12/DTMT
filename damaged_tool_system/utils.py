# Use this file for shared function amid other files

import sqlite3
from db_context_manager import DatabaseConnection, DatabaseCursor

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

#======================================================================================================================#
# END OF DATABASE UTILITY FUNCTIONS
