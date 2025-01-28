import unittest
from unittest.mock import patch
import sqlite3
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

if __name__ == '__main__':
    unittest.main()