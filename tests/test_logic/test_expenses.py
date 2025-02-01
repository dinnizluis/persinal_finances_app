import unittest
from unittest import mock
from unittest.mock import patch
import sqlite3

import pytest
from logic.expenses import add_expense

class TestAddExpense(unittest.TestCase):
    def setUp(self):
        # Set up an in-memory SQLite database
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                paid_status BOOLEAN NOT NULL DEFAULT 0,
                due_date DATE NOT NULL
            )
        ''')
        self.conn.commit()

    def tearDown(self):
        # Close the database connection after each test
        self.conn.close()

    @patch('logic.expenses.get_db_connection')
    def test_add_valid_expense(self, mock_get_db_connection):
        # Mock the database connection to use the in-memory database
        mock_get_db_connection.return_value = self.conn

        # Test adding a valid expense
        add_expense('Groceries', 150.00, 'Food', '2025-02-01')

        # Verify the expense was added to the database
        self.cursor.execute("SELECT * FROM expenses")
        expenses = self.cursor.fetchall()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0][1], 'Groceries')
        self.assertEqual(expenses[0][2], 150.00)
        self.assertEqual(expenses[0][3], 'Food')
        self.assertEqual(expenses[0][4], 0)  # Default paid_status
        self.assertEqual(expenses[0][5], '2025-02-01')

    @patch('logic.expenses.get_db_connection')
    def test_add_expense_negative_amount(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.conn
        with self.assertRaises(ValueError):
            add_expense('Refund', -50.00, 'Misc', '2025-02-01')

    @patch('logic.expenses.get_db_connection')
    def test_add_expense_invalid_date(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.conn
        with self.assertRaises(ValueError):
            add_expense('Subscription', 20.00, 'Entertainment', '01-02-2025')

    @patch('logic.expenses.get_db_connection')
    def test_add_expense_missing_name(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.conn
        with self.assertRaises(ValueError):
            add_expense('', 100.00, 'Utilities', '2025-02-01')

    @patch('logic.expenses.get_db_connection')
    def test_add_expense_missing_category(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.conn
        with self.assertRaises(ValueError):
            add_expense('Electricity Bill', 100.00, '', '2025-02-01')

    @patch('logic.expenses.get_db_connection')
    def test_add_expense_missing_due_date(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.conn
        with self.assertRaises(ValueError):
            add_expense('Water Bill', 50.00, 'Utilities', '')
   
    def test_add_expense_database_failure(self):
        # Create a mock database connection and cursor
        mock_conn = mock.MagicMock()
        mock_cursor = mock.MagicMock()
        
        # Ensure that `__enter__()` is used correctly in a `with` statement
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Simulate a database failure on execute
        mock_cursor.execute.side_effect = Exception("Database Error")

        # Define expected parameters
        name, amount, category, due_date = "Test Expense", 100.0, "Food", "2025-02-01"

        # Call add_expense and expect an exception
        with pytest.raises(Exception, match="Database Error"):
            add_expense(name, amount, category, due_date, db_connection=mock_conn)

        # Assert that execute was called with the correct query and parameters
        expected_query = '''
                INSERT INTO expenses (name, amount, category, paid_status, due_date)
                VALUES (?, ?, ?, ?, ?)
            '''
        expected_params = (name, amount, category, False, due_date)

        mock_cursor.execute.assert_called_once_with(expected_query, expected_params)

        # Ensure rollback was called due to the exception
        mock_conn.rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()