import sqlite3

DB_NAME = "tasks.db"


def connect_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            deadline TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def add_task(name, deadline, category, priority):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (name, deadline, category, priority, completed)
        VALUES (?, ?, ?, ?, 0)
    """, (name, deadline, category, priority))

    conn.commit()
    conn.close()


def get_tasks():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, deadline, category, priority, completed
        FROM tasks
        ORDER BY deadline ASC, id DESC
    """)

    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task_status(task_id, completed):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = ?
        WHERE id = ?
    """, (completed, task_id))

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()