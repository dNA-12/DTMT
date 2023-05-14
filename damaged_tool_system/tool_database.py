from db_context_manager import DatabaseConnection, DatabaseCursor
from utils import fetch_record
from tkinter import messagebox


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
                SELECT * FROM tools where (
                part_num = ?
                )
                ''', (part_num,)

            )

            for item in query.fetchall():
                result.append(item)

            print(result)
            return result


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