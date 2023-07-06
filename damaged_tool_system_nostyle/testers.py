import tkinter as tk
from tkinter import ttk

# Define your data - database query result
data = [
    (1, '200-5580-Piston', 0, 'testtest testtest testtest testtest', 'MORI', 'Noah Ashley', '2023-05-10 08:49 PM'),
    (10, '91803450-New Rev', 45, 'testtest testtest testtest testtest', 'TOY 115', 'Noah Ashley', '2023-05-10 08:59 PM'),
    (710, '91803450-New Rev', 470, 'testtest testtest testtest testtest', 'TOY 115', 'Noah Ashley', '2023-05-10 08:59 PM'),
]

# Define the column names
columns = ['ID', 'Part Number', 'Cycle Time', 'Notes', 'Machine', 'Name', 'Timestamp']

# Create a root window
root = tk.Tk()
root.geometry('1000x600')

# Create a Treeview widget
tree = ttk.Treeview(root, columns=columns, show='headings')

# Add a vertical scrollbar
vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')

# Configure the Treeview to use the vertical scrollbar
tree.configure(yscrollcommand=vsb.set)

# Define the column headings and widths
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Insert the data into the Treeview
for datum in data:
    tree.insert('', 'end', values=datum)

# Pack the Treeview
tree.pack(side='left', fill='both', expand=True)

root.mainloop()