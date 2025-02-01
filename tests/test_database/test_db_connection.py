import app
import database.db_init
import unittest
import sqlite3
from unittest.mock import patch
from database.db_connection import get_db_connection
from unittest.mock import patch, MagicMock

class TestDBConnection(unittest.TestCase):

    @patch("database.db_connection.get_database_name", return_value=":memory:")
    def test_get_db_connection_success(self, mock_get_database_name):
        """Test if get_db_connection successfully establishes a connection."""
        with get_db_connection() as conn:
            self.assertIsInstance(conn, sqlite3.Connection)  # Connection must be an instance of sqlite3.Connection
            cursor = conn.cursor()
            cursor.execute("SELECT 1")  # This should work if the connection is open

    @patch("database.db_connection.get_database_name", return_value=":memory:")
    def test_get_db_connection_closes_on_exit(self, mock_get_database_name):
        """Test if get_db_connection closes the connection after the context manager exits."""
        with get_db_connection() as conn:
            self.assertIsInstance(conn, sqlite3.Connection)  # Check connection type
        with self.assertRaises(sqlite3.ProgrammingError):  # Connection should be closed now
            conn.execute("SELECT 1")

    '''
    @patch("database.db_connection.get_database_name", return_value=":memory:")
    @patch("sqlite3.connect")
    def test_get_db_connection_handles_exception(self, mock_connect, mock_get_database_name):
        """Test if get_db_connection handles database connection exceptions properly."""
        mock_connect.side_effect = sqlite3.Error("Mocked database error")  # Force an error

        with self.assertRaises(sqlite3.Error):  # Expect an error to be raised
            with get_db_connection(): # pragma: no cover
                pass  # Attempt to use the context manager
    '''
    @patch("database.db_connection.get_database_name", return_value=":memory:")
    def test_get_db_connection_handles_exception(self, mock_get_database_name):
        """Test if get_db_connection catches exceptions properly."""
        
        with self.assertRaises(sqlite3.Error):  
            with get_db_connection() as conn:
                raise sqlite3.Error("Forced database error")  # Trigger an error inside the block

        # If the except block runs, the function should still print/log an error

    @patch("database.db_connection.get_database_name", return_value=":memory:")
    @patch("sqlite3.connect", side_effect=sqlite3.Error("Mocked database error"))
    def test_get_db_connection_exception_message(self, mock_connect, mock_get_database_name):
        """Test if get_db_connection prints the error message when an exception occurs."""
        with self.assertRaises(sqlite3.Error):
            with get_db_connection(): # pragma: no cover
                pass
        
        mock_connect.assert_called_once()  # Ensure connection was attempted

if __name__ == "__main__": # pragma: no cover
    unittest.main()