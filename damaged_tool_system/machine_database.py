import sqlite3

# Create database for machines
conn = sqlite3.connect("machines.db")

# Cursor to execute db cmds
c = conn.cursor()

c.execute("""CREATE TABLE machines (
            mc_name TEXT
)""")

# Machine List
machine_nums = ['MORI', 'OKK', 'MAZAK 101', 'MAZAK 102',
                'MAZAK 103', 'MAZAK 104', 'TOY 115', 'TOY 116',
                'MITSUI', 'NIIGATA 138', 'NIIGATA 139', 'OKUMA 187',
                'OKUMA 188', 'PRATT', 'MEGA', 'TACHII',
                'VDF', 'TOSH 195', 'TOSH 196', 'KARACHI 191']

# Add Machines to Database

for machine in machine_nums:
    with conn:

        c.execute("INSERT INTO machines VALUES (:mc_name)",{'mc_name': machine})

# Fetch the added machines and display them
c.execute("SELECT * FROM machines")
result = c.fetchall()

for row in result:
    print(row)

conn.commit()
conn.close()