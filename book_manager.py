import sqlite3
from db_manager import get_db_connection

def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return books

def add_book(book_data):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)",
                     (book_data['title'], book_data['author'], book_data['year'], book_data['isbn']))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: A book with this ISBN already exists.")
    finally:
        conn.close()

def update_book(book_id, book_data):
    conn = get_db_connection()
    try:
        conn.execute("UPDATE books SET title = ?, author = ?, year = ?, isbn = ? WHERE id = ?",
                     (book_data['title'], book_data['author'], book_data['year'], book_data['isbn'], book_id))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: A book with this ISBN already exists.")
    finally:
        conn.close()

def delete_book(book_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()