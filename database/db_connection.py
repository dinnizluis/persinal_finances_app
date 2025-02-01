from contextlib import contextmanager
import logging
from const import get_database_name
import sqlite3

@contextmanager
def get_db_connection():
    """
    Context manager for SQLite database connection.

    :yield: sqlite3.Connection object
    """
    database_name = get_database_name()
    conn = sqlite3.connect(database_name)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")  
        print(f"Error connecting to database: {e}")
        raise e
    finally:
        conn.close()