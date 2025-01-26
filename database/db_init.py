import sqlite3

def initialize_database():
    # Connect to SQLite (creates the file if it doesn't exist)
    connection = sqlite3.connect("personal_finance_app.db")
    cursor = connection.cursor()

    # Create 'expenses' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        value REAL NOT NULL,
        category TEXT NOT NULL,
        status BOOLEAN NOT NULL DEFAULT 0,
        due_date DATE NOT NULL
    );
    """)

    # Create 'income' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        net_income REAL NOT NULL,
        received_date DATE NOT NULL,
        status BOOLEAN NOT NULL DEFAULT 0,
        monthly_buffer REAL DEFAULT 0
    );
    """)

    # Create 'subscriptions' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE DEFAULT NULL
    );
    """)

    # Create 'goals' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        current_amount REAL DEFAULT 0,
        target_amount REAL NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        status BOOLEAN NOT NULL DEFAULT 1
    );
    """)

    # Optional: Create 'transactions' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_name TEXT NOT NULL,
        action TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        details TEXT
    );
    """)

    # Commit changes and close connection
    connection.commit()
    connection.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()