import sqlite3

def get_user_connection(user_id: str):
    conn = sqlite3.connect(f"memories_{user_id}.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, memory TEXT)")
    conn.commit()
    return conn, cursor

def add_memory(user_id: str, memory: str):
    conn, cursor = get_user_connection(user_id)
    cursor.execute("INSERT INTO memories (memory) VALUES (?)", (memory,))
    conn.commit()
    conn.close()

def query_memories(user_id: str, query_text: str):
    conn, cursor = get_user_connection(user_id)
    cursor.execute("SELECT memory FROM memories WHERE memory LIKE ?", ('%' + query_text + '%',))
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results