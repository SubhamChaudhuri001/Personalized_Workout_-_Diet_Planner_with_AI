import sqlite3

def connect_db():
    return sqlite3.connect("fitness.db", check_same_thread=False)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        gender TEXT,
        height REAL,
        weight REAL,
        goal TEXT,
        calories INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()



#Fetch Progress Data
def get_progress():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT date, weight FROM progress")
    data = cursor.fetchall()

    conn.close()
    return data
