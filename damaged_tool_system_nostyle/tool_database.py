from db_context_manager import DatabaseConnection, DatabaseCursor
from utils import fetch_record
from tkinter import messagebox
from collections import defaultdict
from datetime import datetime
import heapq


def create_tool_table():
    with DatabaseConnection("tool.db") as conn:
        with DatabaseCursor(conn) as c:
            c.execute("""CREATE TABLE IF NOT EXISTS tools (
                            tool_num INTEGER,
                            part_num TEXT,
                            op_num INTEGER,
                            desc TEXT,
                            emp_mc TEXT,
                            emp_name TEXT,
                            date_time TEXT
                        )""")
        conn.commit()


def add_tool_db(user_entered_details, current_user, date_time):
    with DatabaseConnection("tool.db") as conn:
        with DatabaseCursor(conn) as c:

            c.execute(
                "INSERT INTO tools VALUES (:tool_num, :part_num, :op_num, :desc, :emp_name, :emp_mc, :date_time)",
                {'tool_num': user_entered_details[0],
                 'part_num': user_entered_details[1],
                 'op_num': user_entered_details[2],
                 'desc': user_entered_details[3],
                 'emp_name': current_user[1],
                 'emp_mc': current_user[0],
                 'date_time': date_time}
            )

            print("Tool Added")
            conn.commit()
            return True

# Used to Find Tool Data in DataAnalyticsScreen


def tool_analytics_search(part_num, op_num, machine, tool_num):
    with DatabaseConnection("tool.db") as conn:
        with DatabaseCursor(conn) as c:

            result = []

            # Print the entire tools table

            c.execute("SELECT * FROM tools")
            all_rows = c.fetchall()
            print("All rows in the tools table:")
            for row in all_rows:
                print(row)

            print(f"Searching for: Part Number - {part_num}, Operation Number - {op_num},"
                  f" Machine - {machine}, Tool Number - {tool_num}")

            # Ensure that tool_num and op_num are integers

            tool_num = int(tool_num)
            op_num = int(op_num)

            query = c.execute(
                '''
                SELECT * FROM tools where (
                tool_num = ? AND
                part_num = ? AND
                op_num = ? AND
                emp_mc = ? 
                )
                ''', (tool_num, part_num, op_num, machine)
            )

            for item in query.fetchall():
                result.append(item)

            print(result)
            return result

# Used to Find Tool Data in DataAnalyticsScreen


def part_analytics_search(part_num):
    with DatabaseConnection("tool.db") as conn:
        with DatabaseCursor(conn) as c:

            result = []

            # Print the entire tools table

            c.execute("SELECT * FROM tools")
            all_rows = c.fetchall()
            print("All rows in the tools table:")
            for row in all_rows:
                print(row)

            print(f"Searching for: Part Number - {part_num}")

            query = c.execute(

                '''
                SELECT * FROM tools WHERE (
                part_num = ?
                )
                ''', (part_num,)

            )

            for item in query.fetchall():
                result.append(item)

            print(result)
            return result


def part_frequency_search(part_numbers):
    with DatabaseConnection("tool.db") as conn:
        with DatabaseCursor(conn) as c:

            # Use defaultdict to establish the freq of each part

            part_freq = defaultdict(int)

            # Add all parts regardless if they have not appeared in the database yet

            for part in part_numbers:
                part_freq[part]

            query = c.execute(
                '''
                SELECT part_num FROM tools
                '''
            )

            parts = [row[0] for row in query.fetchall()]

            for part in parts:
                part_freq[part] += 1

            print(part_freq)
            return part_freq


def machine_frequency_search(machine_nums):
    with DatabaseConnection("tool.db") as conn:
        with DatabaseCursor(conn) as c:

            machine_freq = defaultdict(int)

            query = c.execute(
                '''
                SELECT emp_mc FROM tools
                '''
            )

            machines = [row[0] for row in query.fetchall()]

            for machine in machines:
                machine_freq[machine] += 1

            print(machine_freq)
            return machine_freq


def operation_analytics_search(part_num, op_num):
    with DatabaseConnection("tool.db") as conn:
        with DatabaseCursor(conn) as c:

            result = []

            # Print the entire tools table

            c.execute("SELECT * FROM tools")
            all_rows = c.fetchall()
            print("All rows in the tools table:")
            for row in all_rows:
                print(row)

            print(f"Searching for: Part Number - {part_num}, Operation: {op_num}")

            # Ensure op_num is an integer
            op_num = int(op_num)

            query = c.execute(
                '''
                SELECT * FROM tools WHERE(
                part_num = ? AND
                op_num = ?
                )
                ''', (part_num, op_num)
            )

            for item in query.fetchall():
                result.append(item)

            print(result)
            return result


def machine_analytics_search(machine):
    with DatabaseConnection("tool.db") as conn:
        with DatabaseCursor(conn) as c:

            result = []

            # Print the entire tools table

            c.execute("SELECT * FROM tools")
            all_rows = c.fetchall()
            print("All rows in the tools table:")
            for row in all_rows:
                print(row)

            print(f"Searching for: Machine - {machine}")

            query = c.execute(
                '''
                SELECT * FROM tools WHERE(
                emp_mc = ? 
                )
                ''', (machine,)
            )

            for item in query.fetchall():
                result.append(item)

            print(result)
            return result


def operator_analytics_search(operator):
    with DatabaseConnection("tool.db") as conn:
        with DatabaseCursor(conn) as c:

            result = []

            # Print the entire tools table

            c.execute("SELECT * FROM tools")
            all_rows = c.fetchall()
            print("All rows in the tools table:")
            for row in all_rows:
                print(row)

            print(f"Searching for: Operator - {operator}")

            query = c.execute(
                '''
                SELECT * FROM tools WHERE(
                emp_name = ? 
                )
                ''', (operator,)
            )

            for item in query.fetchall():
                result.append(item)

            print(result)
            return result


def all_tools_search():
    with DatabaseConnection("tool.db") as conn:
        with DatabaseCursor(conn) as c:

            result = []

            c.execute("SELECT * FROM tools")
            all_tools = c.fetchall()

            print("All rows in the tools table:")

            for tool in all_tools:
                result.append(tool)

            print(result)
            return result


def top_five_tools_search():
    with DatabaseConnection("tool.db") as conn:
        with DatabaseCursor(conn) as c:

            tool_freq = defaultdict(int)

            c.execute("SELECT * FROM tools")
            all_tools = c.fetchall()

            for tool in all_tools:

                key = (tool[0], tool[1], tool[2])

                tool_freq[key] += 1

            top_five = heapq.nlargest(5, tool_freq.items(), key= lambda i: i[1])

            print(top_five)
            return top_five


def selected_month_search(query_num, part_or_mc):
    with DatabaseConnection("tool.db") as conn:
        with DatabaseCursor(conn) as c:

            if part_or_mc == 'mc':

                machine_freq = defaultdict(int)

                selected_month_incidents = c.execute(
                    '''
                    SELECT * FROM tools WHERE strftime('%m', substr(date_time, 1, 10)) = ?
                    ''', (str(query_num).zfill(2),)
                )

                machines = [row[4] for row in selected_month_incidents.fetchall()]

                for machine in machines:
                    machine_freq[machine] += 1

                print(machine_freq)
                return machine_freq

            if part_or_mc == 'part':

                part_freq = defaultdict(int)

                selected_month_incidents = c.execute(
                    '''
                    SELECT * FROM tools WHERE strftime('%m', substr(date_time, 1, 10)) = ?
                    ''', (str(query_num).zfill(2),)
                )

                parts = [row[1] for row in selected_month_incidents.fetchall()]

                for part in parts:
                    part_freq[part] += 1

                print(part_freq)
                return part_freq
