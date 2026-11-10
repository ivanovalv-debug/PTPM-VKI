from bs4 import BeautifulSoup
from src.models import Comment
from src.database import DatabaseRepository

class ForumParser:
    @staticmethod
    def parse_page(html_content: str) -> list[Comment]:
        soup = BeautifulSoup(html_content, 'lxml')
        comments = []
        
        for post in soup.find_all("div", class_="post"):
            cid = int(post.get("data-id", 0))
            author_tag = post.find("span", class_="author")
            content_tag = post.find("div", class_="content")
            
            if author_tag and content_tag:
                author = author_tag.get_text(strip=True)
                text = content_tag.decode_contents() 
                comments.append(Comment(cid, author, text))
            
        return comments

    @staticmethod
    def save_to_db(comments: list[Comment], repository: DatabaseRepository):
        for c in comments:
            repository.add(c.comment_id, c.name, c.message)