from contextlib import contextmanager
from const import get_database_name
import sqlite3

@contextmanager
def get_db_connection():
    """
    Context manager for SQLite database connection.

    :yield: sqlite3.Connection object
    """
    conn = sqlite3.connect(get_database_name())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise
    finally:
        conn.close()