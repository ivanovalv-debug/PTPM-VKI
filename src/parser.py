import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.parser import ForumParser
from src.database import DatabaseRepository

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "page.html")

class TestForumParser(unittest.TestCase):
    def setUp(self):
        with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
            self.html = f.read()
        self.repo = DatabaseRepository(":memory:")

    def test_parse_extracts_comments(self):
        comments = ForumParser.parse_page(self.html)
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0].name, "Mila")
        self.assertEqual(comments[0].comment_id, 1)

    def test_save_to_db_works(self):
        comments = ForumParser.parse_page(self.html)
        ForumParser.save_to_db(comments, self.repo)
        self.assertIsNotNone(self.repo.get_by_id(1))
        self.assertEqual(len(self.repo.get_by_name("Admin")), 1)

if __name__ == "__main__":
    unittest.main()