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
        """Проверяем, что парсер нашел все 25 постов из треда"""
        comments = ForumParser.parse_page(self.html)
        self.assertEqual(len(comments), 25)
       
        self.assertEqual(comments[0].comment_id, 43695612)
        self.assertEqual(comments[0].name, "Anonymous")
        self.assertIn("Smissmas", comments[0].message)

    def test_save_to_db_works(self):
        """Проверяем сохранение реальных данных из 4chan"""
        comments = ForumParser.parse_page(self.html)
        ForumParser.save_to_db(comments, self.repo)
        
        op_post = self.repo.get_by_id(43695612)
        self.assertIsNotNone(op_post)
        self.assertEqual(op_post.name, "Anonymous")
        
        all_comments = self.repo.get_by_name("Anonymous")
        self.assertEqual(len(all_comments), 25)

if __name__ == "__main__":
    unittest.main()