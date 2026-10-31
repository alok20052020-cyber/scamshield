import sqlite3
from datetime import datetime

DATABASE = "scamshield.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            reference TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_complaint(category, description, reference=""):
    conn = get_connection()
    conn.execute("""
        INSERT INTO complaints
        (category, description, reference, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        category,
        description,
        reference,
        datetime.now().strftime("%d-%m-%Y %H:%M")
    ))
    conn.commit()
    conn.close()

def get_complaints():
    conn = get_connection()
    complaints = conn.execute("""
        SELECT * FROM complaints
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return complaints

def update_complaint_status(complaint_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE complaints SET status = ? WHERE id = ?",
        (status, complaint_id)
    )

    conn.commit()
    conn.close()
