import sqlite3
from datetime import datetime

DATABASE_NAME = "library.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year TEXT,
            isbn TEXT UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            member_id TEXT UNIQUE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowed_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            borrow_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (member_id) REFERENCES members (id)
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', 'admin'))
    conn.commit()
    conn.close()

def check_credentials(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def get_members():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, member_id FROM members")
    members = cursor.fetchall()
    conn.close()
    return members

def add_member_db(name, member_id):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO members (name, member_id) VALUES (?, ?)", (name, member_id))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Member with this ID already exists.")
    finally:
        conn.close()

def update_member_db(member_db_id, name, member_id):
    conn = get_db_connection()
    try:
        conn.execute("UPDATE members SET name = ?, member_id = ? WHERE id = ?", (name, member_id, member_db_id))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Member with this ID already exists.")
    finally:
        conn.close()

def delete_member_db(member_db_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM members WHERE id = ?", (member_db_id,))
    conn.commit()
    conn.close()

def get_borrowed_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            bb.id, b.title, m.name, bb.borrow_date, bb.return_date
        FROM 
            borrowed_books bb
        JOIN 
            books b ON bb.book_id = b.id
        JOIN 
            members m ON bb.member_id = m.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def borrow_book_db(book_id, member_id, return_date):
    conn = get_db_connection()
    borrow_date = datetime.now().strftime("%Y-%m-%d")
    conn.execute("INSERT INTO borrowed_books (book_id, member_id, borrow_date, return_date) VALUES (?, ?, ?, ?)", (book_id, member_id, borrow_date, return_date))
    conn.commit()
    conn.close()

def return_book_db(borrow_record_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM borrowed_books WHERE id = ?", (borrow_record_id,))
    conn.commit()
    conn.close()

def is_book_borrowed_db(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM borrowed_books WHERE book_id = ?", (book_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

create_tables()