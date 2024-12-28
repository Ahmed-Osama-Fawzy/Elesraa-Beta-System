import sqlite3

class SQLiteDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute(self, query, params=None):
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        return cursor

    def commit(self):
        if self.connection:
            self.connection.commit()

    def fetchall(self, query, params=None):
        cursor = self.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def fetchone(self, query, params=None):
        cursor = self.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def update(self, query, params=None):
        cursor = self.execute(query, params)
        self.commit()
        return cursor.rowcount > 0
    
    def insert(self, query, params=None):
        cursor = self.execute(query, params)
        self.commit()
        return cursor.rowcount > 0
