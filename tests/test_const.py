import unittest
from const import get_database_name, DATABASE_NAME  # Replace 'your_module' with the actual module name

class TestDatabaseName(unittest.TestCase):
    def test_get_database_name(self):
        """Test if get_database_name returns the correct database name."""
        self.assertEqual(get_database_name(), DATABASE_NAME)

if __name__ == '__main__': # pragma: no cover
    unittest.main()