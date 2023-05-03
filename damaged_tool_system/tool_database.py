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
                            emp_name,
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
                 'emp_name': current_user[0],
                 'emp_mc': current_user[1],
                 'date_time': date_time}
            )

            print("Tool Added")
            conn.commit()
            return True
