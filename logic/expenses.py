from datetime import datetime
from database.db_connection import get_db_connection

def add_expense(amount, category, description=None, date=None):
    """
    Adds a new expense to the database.

    :param amount: The amount of the expense.
    :param category: The category of the expense (e.g., 'Food', 'Transport').
    :param description: A brief description of the expense (optional).
    :param date: The date of the expense in 'YYYY-MM-DD' format (optional).
    :return: None
    """
    # Use the current date if no date is provided
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

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
            cursor.execute(
                "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                (amount, category, description, date)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e