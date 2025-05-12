import sqlite3

class TargetStore:
    def __init__(self, db_name="targets.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._initialize_db()

    def _initialize_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                priority TEXT CHECK(priority IN ('High', 'Medium', 'Low')) NOT NULL
            )
        """)
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_priority ON targets(priority)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_url ON targets(url)")
        self.conn.commit()

    def add_target(self, url, priority="Medium"):
        self.cursor.execute("INSERT INTO targets (url, priority) VALUES (?, ?)", (url, priority))
        self.conn.commit()

    def get_targets(self, priority=None):
        if priority:
            self.cursor.execute("SELECT * FROM targets WHERE priority=?", (priority,))
        else:
            self.cursor.execute("SELECT * FROM targets")
        return self.cursor.fetchall()

    def remove_target(self, target_id):
        self.cursor.execute("DELETE FROM targets WHERE id=?", (target_id,))
        self.conn.commit()

    def search_targets(self, query):
        like_query = f"%{query}%"
        self.cursor.execute("SELECT * FROM targets WHERE url LIKE ?", (like_query,))
        return self.cursor.fetchall()

    def update_target(self, target_id, new_url, new_priority):
        self.cursor.execute("""
            UPDATE targets
            SET url = ?, priority = ?
            WHERE id = ?
        """, (new_url, new_priority, target_id))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()
