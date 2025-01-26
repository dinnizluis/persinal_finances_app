from contextlib import contextmanager
import sqlite3

@contextmanager
def get_db_connection():
    """
    Context manager for SQLite database connection.

    :yield: sqlite3.Connection object
    """
    conn = sqlite3.connect('finance.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise
    finally:
        conn.close()