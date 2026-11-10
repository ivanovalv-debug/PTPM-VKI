from bs4 import BeautifulSoup
from src.models import Comment
from src.database import DatabaseRepository


class ForumParser:
    @staticmethod
    def parse_page(html_content: str) -> list[Comment]:
        soup = BeautifulSoup(html_content, 'lxml')
        comments = []
        
        
        for post_container in soup.find_all("div", class_="postContainer"):
            full_id = post_container.get("id", "")
            cid = int(full_id.replace("pc", "")) if full_id.startswith("pc") else 0
            
            name_tag = post_container.find("span", class_="name")
            author = name_tag.get_text(strip=True) if name_tag else "Anonymous"
           
            msg_tag = post_container.find("blockquote", class_="postMessage")
            text = msg_tag.decode_contents() if msg_tag else ""
            
            if cid > 0 and text:
                comments.append(Comment(cid, author, text))
                
        return comments

    @staticmethod
    def save_to_db(comments: list[Comment], repository: DatabaseRepository):
        for c in comments:
            repository.add(c.comment_id, c.name, c.message)