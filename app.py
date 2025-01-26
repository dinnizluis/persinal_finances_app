import sqlite3
from datetime import datetime
from logic.expenses import add_expense  # Adjust the import based on your project structure
from database.db_init import initialize_database

def main():
    """
    Main function to run the application, allowing the user to add expenses.
    """
    initialize_database()

    while True:
        print("\nPersonal Finance App")
        print("1. Add Expense")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Enter the expense amount: "))
            category = input("Enter the expense category: ")
            description = input("Enter a description for the expense: ")
            date = input("Enter the date of the expense (YYYY-MM-DD): ")

            # Call the add_expense function
            add_expense(amount, category, description, date)
            print(f"Expense of {amount} in category '{category}' added successfully.")
        elif choice == '2':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()