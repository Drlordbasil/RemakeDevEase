import sqlite3

def connect_to_database():
    # Create a new database or connect to an existing one
    conn = sqlite3.connect('tasks.db')
    return conn

def create_cursor(conn):
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    return cursor

def create_tasks_table(cursor):
    # Create a table to store tasks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    ''')

def add_task(conn, content):
    # Function to add a new task to the database
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (content) VALUES (?)', (content,))
    conn.commit()

def get_tasks(cursor):
    # Function to retrieve all tasks from the database
    cursor.execute('SELECT * FROM tasks')
    return cursor.fetchall()

def mark_tasks_as_done(conn, cursor, task_id):
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    return True