import sqlite3
from app.config import DB_PATH

def init_sqlite_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunk_metadata (
                id TEXT PRIMARY KEY,
                source TEXT,
                chunk_index INTEGER,
                word_count INTEGER,
                char_count INTEGER,
                line_count INTEGER
            )
        ''')
        conn.commit()

def store_metadata_in_sqlite(point_id: str, source: str, index: int, word_count: int, char_count: int, line_count: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chunk_metadata (id, source, chunk_index, word_count, char_count, line_count)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (point_id, source, index, word_count, char_count, line_count))
        conn.commit()
