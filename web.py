from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from database import add_memory, query_memories
from llm import process_input
import sqlite3

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, hashed_password TEXT)")
conn.commit()

def get_current_user(token: str = Depends(oauth2_scheme)):
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (token,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"user_id": user[0]}

@app.post("/register")
async def register(user_id: str = Form(), password: str = Form()):
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID exists")
    hashed_password = pwd_context.hash(password)
    cursor.execute("INSERT INTO users (user_id, hashed_password) VALUES (?, ?)", (user_id, hashed_password))
    conn.commit()
    return {"status": "registered"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    cursor.execute("SELECT hashed_password FROM users WHERE user_id = ?", (form_data.username,))
    user = cursor.fetchone()
    if not user or not pwd_context.verify(form_data.password, user[0]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
    return {"access_token": form_data.username, "token_type": "bearer"}

@app.post("/add")
async def add(memory: str, user: dict = Depends(get_current_user)):
    user_id = user["user_id"]
    refined_memory = process_input(user_id, memory, is_query=False)
    add_memory(user_id, refined_memory)
    return {"status": "added"}

@app.get("/query")
async def query(q: str, user: dict = Depends(get_current_user)):
    user_id = user["user_id"]
    refined_query = process_input(user_id, q, is_query=True)
    results = query_memories(user_id, refined_query)
    return {"results": results}

@app.post("/upload")
async def upload(mcp_data: dict, user: dict = Depends(get_current_user)):
    user_id = user["user_id"]
    data_str = str(mcp_data)
    refined_data = process_input(user_id, data_str, is_query=False)
    add_memory(user_id, refined_data)
    return {"status": "uploaded"}

if __name__ == "__main__":
    import uvicorn
    import os
    uvicorn.run("app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=False)