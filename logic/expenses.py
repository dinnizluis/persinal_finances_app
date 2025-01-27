from datetime import datetime
from database.db_connection import get_db_connection

def add_expense(name, amount, category, due_date, status=False):
    """
    Adds a new expense to the database.

    :param name: A brief description of the expense (name).
    :param amount: The amount of the expense.
    :param category: The category of the expense (e.g., 'Food', 'Transport').
    :param due_date: The due date of the expense in 'YYYY-MM-DD' format (optional).
    :return: None
    """
    # Use the current date if no date is provided
    if due_date is None:
        due_date = datetime.now().strftime('%Y-%m-%d')

    # Validate the amount
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    # Validate the category
    if not category:
        raise ValueError("Category cannot be empty.")

    # Establish a database connection
    with get_db_connection() as conn:
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