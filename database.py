import sqlite3
from datetime import datetime

def get_db_connection():
    """Get database connection and create table if it doesn't exist"""
    conn = sqlite3.connect("memories.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

def add_memory(user_id: str, memory: str):
    """Add a memory for a specific user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO memories (user_id, content, timestamp) VALUES (?, ?, ?)",
        (user_id, memory, timestamp)
    )
    conn.commit()
    conn.close()
    return True

def query_memories(user_id: str, query_text: str):
    """Query memories for a specific user with simple text search"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Simple text search - find memories containing the query text
    cursor.execute(
        "SELECT content FROM memories WHERE user_id = ? AND content LIKE ? ORDER BY timestamp DESC LIMIT 5",
        (user_id, f"%{query_text}%")
    )

    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results