# persinal_finances_app
App for managing personal finances. The goal is to move the process for a Google Sheet to a Python application


# Suggested project strucuture
finance_app/
│
├── app.py                  # Entry point for the application
├── database/
│   ├── db_init.py          # Database setup and schema initialization
│   ├── models.py           # ORM models or raw SQL queries
│   └── db_connection.py    # Connection logic
│
├── logic/
│   ├── expenses.py         # Business logic for expenses
│   ├── income.py           # Business logic for income
│   ├── goals.py            # Business logic for goals
│   └── recurring.py        # Business logic for recurring subscriptions
│
├── ui/
│   ├── cli.py              # Command-line interface functions
│   └── (future GUI files)  # Placeholder for future GUI files
│
├── reports/
│   ├── summary.py          # Generates summaries for monthly spending
│   ├── graphs.py           # Visualizations for data
│   └── report_templates/   # Placeholder for saving report templates
│
└── tests/
    ├── test_expenses.py    # Unit tests for expenses
    ├── test_income.py      # Unit tests for income
    └── test_goals.py       # Unit tests for goals