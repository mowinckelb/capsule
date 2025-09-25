from llm import LLMHandler
from database import DBHandler
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

handler = LLMHandler()

db = DBHandler()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///users.db")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(user_id: str, password: str):
    db = next(get_db())
    user = db.query(User).filter(User.user_id == user_id).first()
    db.close()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return True

def register_user(user_id: str, password: str):
    db = next(get_db())
    existing = db.query(User).filter(User.user_id == user_id).first()
    if existing:
        db.close()
        return False
    new_user = User(user_id=user_id, hashed_password=pwd_context.hash(password))
    db.add(new_user)
    db.commit()
    db.close()
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
            refined = handler.process_input(user_id, memory, is_query=False, db_provider=db.provider)
            db.add_memory(user_id, refined)
            print("Memory saved successfully!")
        elif user_input.lower().startswith("output:"):
            query = user_input[7:].strip()
            refined = handler.process_input(user_id, query, is_query=True, db_provider=db.provider)
            results = db.query_memories(user_id, refined)
            if results:
                summary_prompt = f"For user {user_id}, respond to '{query}' in concise, natural language using only the information in these memories: {results}. Do not add or assume details not present."
                response = handler.process_input(user_id, summary_prompt, is_query=False, db_provider=db.provider)
                print(response)
            else:
                print("No matching memories found.")
        else:
            print("Use 'input: <memory>' or 'output: <question>'.")

if __name__ == "__main__":
    chat_with_llm()