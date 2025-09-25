from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from database import DBHandler
from llm import LLMHandler
from sqlalchemy import create_engine, Column, String # type: ignore
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase # type: ignore
from typing import Dict, Generator
import uvicorn
import os

handler = LLMHandler()

db = DBHandler()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///users.db")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)

def create_tables() -> None:
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.add_event_handler("startup", create_tables)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/", StaticFiles(directory=".", html=True), name="static")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = db.query(User).filter(User.user_id == token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"user_id": user.user_id}

@app.post("/register")
async def register(db: Session = Depends(get_db), user_id: str = Form(), password: str = Form()):
    existing = db.query(User).filter(User.user_id == user_id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID exists")
    new_user = User(user_id=user_id, hashed_password=pwd_context.hash(password))
    db.add(new_user)
    db.commit()
    return {"status": "registered"}

@app.post("/login")
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.user_id == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
    return {"access_token": form_data.username, "token_type": "bearer"}

@app.post("/add")
async def add(memory: str = Form(), user: Dict[str, str] = Depends(get_current_user)):
    try:
        user_id = user["user_id"]
        refined_memory = handler.process_input(user_id, memory, is_query=False, db_provider=db.provider)
        db.add_memory(user_id, refined_memory)
        return {"status": "added"}
    except Exception as e:
        print(f"Error in /add: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/query")
async def query(q: str, user: Dict[str, str] = Depends(get_current_user)):
    user_id = user["user_id"]
    refined_query = handler.process_input(user_id, q, is_query=True, db_provider=db.provider)
    results = db.query_memories(user_id, refined_query)
    if results:
        summary_prompt = f"Respond to '{q}' in natural language, using only: {results}. Avoid metadata or formatting."
        response = handler.process_input(user_id, summary_prompt, is_query=False, db_provider=db.provider)
        return {"results": response}
    return {"results": "No matching memories found."}

@app.post("/upload")
async def upload(mcp_data: dict, user: Dict[str, str] = Depends(get_current_user)):
    user_id = user["user_id"]
    refined_data = handler.process_input(user_id, mcp_data, is_query=False, db_provider=db.provider)
    db.add_memory(user_id, refined_data)
    return {"status": "uploaded"}

@app.get("/{full_path:path}", include_in_schema=False)
async def read_root(full_path: str):
    return FileResponse("index.html")

if __name__ == "__main__":
    uvicorn.run("app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=False)