# Use this file for shared function amid other files

import sqlite3

# Used to grab machines from the machine database!
def fetch_machines():
    conn = sqlite3.connect("machines.db")
    c = conn.cursor()
    c.execute("SELECT * FROM machines")
    machines = c.fetchall()
    conn.close()
    return [machine[0] for machine in machines]