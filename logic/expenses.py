from datetime import datetime
from database.db_connection import get_db_connection

def add_expense(name, amount, category, due_date, status=False, db_connection=None):
    """
    Adds a new expense to the database.

    :param name: A brief description of the expense (name).
    :param amount: The amount of the expense.
    :param category: The category of the expense (e.g., 'Food', 'Transport').
    :param due_date: The due date of the expense in 'YYYY-MM-DD' format (optional).
    :return: None
    """
    if not name:
        raise ValueError("Expense name is required.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if not category:
        raise ValueError("Category is required.")
    if not due_date:
        raise ValueError("Due date is required.")
    # Validate due_date format (YYYY-MM-DD)
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.")

    # Use injected db_connection or create a new one if not provided
    if db_connection is None:
        db_connection = get_db_connection()

    # Establish a database connection
    with db_connection as conn:
        cursor = conn.cursor()
        try:
            # Insert the expense into the table
            cursor.execute('''
                INSERT INTO expenses (name, amount, category, paid_status, due_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, amount, category, status, due_date))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e