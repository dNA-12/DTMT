# Create the database file for employees
conn_empdb = sqlite3.connect("employee.db")

# Create the cursor that interacts with the database and execute sql cmds
c = conn.cursor()

# c.execute("""CREATE TABLE employees (
#             emp_num integer,
#             emp_name text,
#             emp_mc text
#             )""")

# # These can be plugged in as emp for testing
# emp_1 = Employee(110217, 'Tester1', 'Okuma')
# emp_2 = Employee(110216, 'Tester2', 'Mazak')


def create_emp(emp):
    with conn_empdb:
        c.execute("INSERT INTO employees VALUES (:emp_num, :emp_name, :emp_mc)",
                  {'emp_num':emp.emp_num, 'emp_name': emp.emp_name, 'emp_mc': emp.emp_mc})


# c.execute("SELECT * FROM employees WHERE emp_mc=:emp_mc", {'emp_mc': 'Okuma'})

# Commit the changes to the database
conn_empdb.commit()

# Close connection to the database
conn_empdb.close()