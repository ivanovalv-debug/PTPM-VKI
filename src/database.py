import sqlite3
import logging


class Database:

    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self.logger = logging.getLogger(self.__class__.__name__)
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS triangle_results (
                side_a REAL,
                side_b REAL,
                side_c REAL,
                type TEXT,
                message TEXT,
                PRIMARY KEY (side_a, side_b, side_c)
            )
        """)
        self.conn.commit()

    def get_record(self, a: float, b: float, c: float) -> dict | None:
        cursor = self.conn.execute(
            "SELECT type, message FROM triangle_results WHERE side_a=? AND side_b=? AND side_c=?",
            (a, b, c)
        )
        row = cursor.fetchone()
        if row:
            return {"type": row[0], "message": row[1]}
        return None

    def add_record(self, a: float, b: float, c: float, t_type: str, message: str) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO triangle_results VALUES (?, ?, ?, ?, ?)",
            (a, b, c, t_type, message)
        )
        self.conn.commit()

    def delete_record(self, a: float, b: float, c: float) -> None:
        self.conn.execute(
            "DELETE FROM triangle_results WHERE side_a=? AND side_b=? AND side_c=?",
            (a, b, c)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()