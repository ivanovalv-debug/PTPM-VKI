import sqlite3
from config import DB_PATH
from src.models import Comment


class DatabaseRepository:
    MAX_NAME_LEN = 256
    MAX_MSG_LEN = 8096

    def __init__(self, db_path=None):
        # Если путь не передан явно, берем из конфига (файловая БД)
        self.db_path = db_path or DB_PATH
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def _validate_lengths(self, username: str, message: str):
        if not isinstance(username, str) or len(username) > self.MAX_NAME_LEN:
            raise ValueError(f"Имя должно быть строкой до {self.MAX_NAME_LEN} символов")
        if not isinstance(message, str) or len(message) > self.MAX_MSG_LEN:
            raise ValueError(f"Сообщение должно быть строкой до {self.MAX_MSG_LEN} символов")

    def get_by_id(self, comment_id: int):
        cursor = self.conn.execute("SELECT * FROM comments WHERE id=?", (comment_id,))
        row = cursor.fetchone()
        return Comment(row[0], row[1], row[2]) if row else None

    def get_by_name(self, username: str):
        cursor = self.conn.execute("SELECT * FROM comments WHERE name=?", (username,))
        return [Comment(r[0], r[1], r[2]) for r in cursor.fetchall()]

    def add(self, comment_id: int, username: str, message: str) -> bool:
        self._validate_lengths(username, message)
        try:
            self.conn.execute("INSERT INTO comments VALUES (?, ?, ?)", 
                              (comment_id, username, message))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update(self, comment_id: int, new_message: str) -> bool:
        self._validate_lengths("", new_message)
        cursor = self.conn.execute("UPDATE comments SET message=? WHERE id=?", 
                                   (new_message, comment_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete(self, comment_id: int) -> bool:
        cursor = self.conn.execute("DELETE FROM comments WHERE id=?", (comment_id,))
        self.conn.commit()
        return cursor.rowcount > 0