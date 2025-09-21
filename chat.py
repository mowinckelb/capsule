import sqlite3
from llm import process_input
from database import add_memory, query_memories
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, hashed_password TEXT)")
conn.commit()

def authenticate_user(user_id: str, password: str):
    cursor.execute("SELECT hashed_password FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user or not pwd_context.verify(password, user[0]):
        return False
    return True

def register_user(user_id: str, password: str):
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        return False
    hashed_password = pwd_context.hash(password)
    cursor.execute("INSERT INTO users (user_id, hashed_password) VALUES (?, ?)", (user_id, hashed_password))
    conn.commit()
    return True

def chat_with_llm():
    print("Welcome to Capsule! Are you an existing user? (yes/no)")
    is_existing = input("> ").strip().lower()
    
    if is_existing == "no":
        print("Enter new user ID and password.")
        new_user_id = input("New User ID: ").strip()
        new_password = input("New Password: ").strip()
        if register_user(new_user_id, new_password):
            print(f"User {new_user_id} registered successfully!")
            user_id = new_user_id
        else:
            print("User ID already exists. Try again.")
            return
    elif is_existing == "yes":
        print("Enter your user ID and password.")
        user_id = input("User ID: ").strip()
        password = input("Password: ").strip()
        if not authenticate_user(user_id, password):
            print("Wrong password or user ID.")
            return
    else:
        print("Please enter 'yes' or 'no'.")
        return
    
    print(f"Authenticated as {user_id}. Type 'input: <memory>' to save, 'output: <question>' to retrieve, or 'exit' to quit.")
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            break
        if user_input.lower().startswith("input:"):
            memory = user_input[6:].strip()
            refined = process_input(user_id, memory, is_query=False)
            add_memory(user_id, refined)
            print("Memory saved successfully!")
        elif user_input.lower().startswith("output:"):
            query = user_input[7:].strip()
            refined = process_input(user_id, query, is_query=True)
            results = query_memories(user_id, refined)
            if results:
                summary_prompt = f"For user {user_id}, respond to '{query}' in concise, natural language using only the information in these memories: {results}. Do not add or assume details not present."
                response = process_input(user_id, summary_prompt, is_query=False)
                print(response)
            else:
                print("No matching memories found.")
        else:
            print("Use 'input: <memory>' or 'output: <question>'.")
    conn.close()

if __name__ == "__main__":
    chat_with_llm()