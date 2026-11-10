import sqlite3
from src.models import Comment

class DatabaseRepository:
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL CHECK(length(name) <= 256),
                message TEXT NOT NULL CHECK(length(message) <= 8096)
            )
        """)
        self.conn.commit()

    def get_by_id(self, comment_id: int):
        cursor = self.conn.execute("SELECT * FROM comments WHERE id=?", (comment_id,))
        row = cursor.fetchone()
        return Comment(row[0], row[1], row[2]) if row else None

    def get_by_name(self, username: str):
        cursor = self.conn.execute("SELECT * FROM comments WHERE name=?", (username,))
        return [Comment(r[0], r[1], r[2]) for r in cursor.fetchall()]

    def add(self, comment_id: int, username: str, message: str) -> bool:
        try:
            self.conn.execute("INSERT INTO comments VALUES (?, ?, ?)", (comment_id, username, message))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update(self, comment_id: int, new_message: str) -> bool:
        cursor = self.conn.execute("UPDATE comments SET message=? WHERE id=?", (new_message, comment_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete(self, comment_id: int) -> bool:
        cursor = self.conn.execute("DELETE FROM comments WHERE id=?", (comment_id,))
        self.conn.commit()
        return cursor.rowcount > 0