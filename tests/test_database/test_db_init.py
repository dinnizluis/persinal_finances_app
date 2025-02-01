
import sys
import os
import sqlite3
import unittest
from unittest.mock import patch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from database.db_init import initialize_database


class TestDatabaseInitialization(unittest.TestCase):

    @patch("database.db_init.get_database_name", return_value=":memory:")
    def test_initialize_database(self, mock_get_database_name):
        """Test if initialize_database creates all necessary tables."""
        # Create an in-memory database
        connection = sqlite3.connect(":memory:")

        # Call the function (it will use the in-memory database)
        initialize_database(connection=connection)

        # Fetch existing tables
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row[0] for row in cursor.fetchall()}

        # Expected tables
        expected_tables = {"expenses", "income", "subscriptions", "goals", "transactions"}
        print('Created tables ::: ', tables)
        # Validate that all required tables exist
        self.assertTrue(expected_tables.issubset(tables))

        # Clean up
        connection.close()

if __name__ == "__main__": # pragma: no cover
    unittest.main()