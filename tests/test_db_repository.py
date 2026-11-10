import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.database import DatabaseRepository

class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self.repo = DatabaseRepository(":memory:")

    def test_add_success(self):
        self.assertTrue(self.repo.add(1, "Mila", "Hello"))
        self.assertIsNotNone(self.repo.get_by_id(1))

    def test_add_duplicate_id(self):
        self.repo.add(1, "Mila", "Hello")
        self.assertFalse(self.repo.add(1, "Admin", "World"))

    def test_get_by_id_found(self):
        self.repo.add(1, "Mila", "Hello")
        res = self.repo.get_by_id(1)
        self.assertEqual(res.name, "Mila")

    def test_get_by_id_not_found(self):
        self.assertIsNone(self.repo.get_by_id(999))

    def test_get_by_name(self):
        self.repo.add(1, "Mila", "Hi")
        self.repo.add(2, "Mila", "Bye")
        self.assertEqual(len(self.repo.get_by_name("Mila")), 2)

    def test_update_success(self):
        self.repo.add(1, "Mila", "Old")
        self.assertTrue(self.repo.update(1, "New"))
        self.assertEqual(self.repo.get_by_id(1).message, "New")

    def test_update_non_existent(self):
        self.assertFalse(self.repo.update(999, "Fail"))

    def test_delete_success(self):
        self.repo.add(1, "Mila", "Hi")
        self.assertTrue(self.repo.delete(1))
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_non_existent(self):
        self.assertFalse(self.repo.delete(999))

if __name__ == "__main__":
    unittest.main()