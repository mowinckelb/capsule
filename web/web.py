from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.database import DBHandler
from llm.llm import LLMHandler
import sqlite3
import uvicorn

try:
    handler = LLMHandler()
    print("✓ LLM Handler initialized successfully")
except Exception as e:
    print(f"✗ LLM Handler initialization failed: {e}")
    handler = None

try:
    db = DBHandler()
    print("✓ Database Handler initialized successfully")
except Exception as e:
    print(f"✗ Database Handler initialization failed: {e}")
    db = None

app = FastAPI()

# Initialize SQLite database for users
def init_user_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, hashed_password TEXT)")
    conn.commit()
    conn.close()

# Initialize database on startup
init_user_db()

# Debug environment variables on startup
print("=== Environment Variables Debug ===")
print(f"GROK_API_KEY: {'Set' if os.getenv('GROK_API_KEY') else 'Not set'}")
print(f"PINECONE_API_KEY: {'Set' if os.getenv('PINECONE_API_KEY') else 'Not set'}")
print(f"DEFAULT_PROVIDER: {os.getenv('DEFAULT_PROVIDER', 'grok')}")
print(f"DEFAULT_DB_PROVIDER: {os.getenv('DEFAULT_DB_PROVIDER', 'pinecone')}")
print("=====================================")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (token,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"user_id": user[0]}

@app.post("/register")
async def register(user_id: str = Form(), password: str = Form()):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, hashed_password TEXT)")
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists")
    hashed_password = pwd_context.hash(password)
    cursor.execute("INSERT INTO users (user_id, hashed_password) VALUES (?, ?)", (user_id, hashed_password))
    conn.commit()
    conn.close()
    return {"status": "registered"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE user_id = ?", (form_data.username,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
    if not pwd_context.verify(form_data.password, user[0]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong password")
    return {"access_token": form_data.username, "token_type": "bearer"}

@app.post("/add")
async def add(memory: str = Form(), user: dict = Depends(get_current_user)):
    try:
        if not handler:
            raise HTTPException(status_code=500, detail="LLM Handler not initialized")
        if not db:
            raise HTTPException(status_code=500, detail="Database Handler not initialized")
            
        user_id = user["user_id"]
        refined_memory = handler.process_input(user_id, memory, is_query=False, db_provider=db.provider)
        db.add_memory(user_id, refined_memory)
        return {"status": "added"}
    except Exception as e:
        print(f"Error in /add: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/query")
async def query(q: str, user: dict = Depends(get_current_user)):
    try:
        if not handler:
            raise HTTPException(status_code=500, detail="LLM Handler not initialized")
        if not db:
            raise HTTPException(status_code=500, detail="Database Handler not initialized")
            
        user_id = user["user_id"]
        print(f"Processing query for user {user_id}: {q}")
        
        # Process the query
        refined_query = handler.process_input(user_id, q, is_query=True, db_provider=db.provider)
        print(f"Refined query: {refined_query}")
        
        # Query memories
        results = db.query_memories(user_id, refined_query)
        print(f"Query results: {results}")
        
        if results and len(results) > 0:
            # Filter out empty results
            filtered_results = [r for r in results if r and str(r).strip()]
            if filtered_results:
                summary_prompt = f"Answer this question: '{q}' using only this information: {filtered_results}. Give a direct, natural answer without any metadata."
                response = handler.process_input(user_id, summary_prompt, is_query=False, db_provider=db.provider)
                print(f"LLM response: {response}")
                
                # The LLM should now return a natural language string directly
                if isinstance(response, str):
                    response_text = response
                elif isinstance(response, dict):
                    # Fallback if still returning dict
                    response_text = response.get('content', f"Based on your memories: {', '.join(filtered_results)}")
                else:
                    response_text = str(response) if response else "No response generated"
                return {"results": response_text}
        
        return {"results": "No matching memories found."}
    except Exception as e:
        print(f"Error in /query: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"results": f"Error processing query: {str(e)}"}

@app.post("/upload")
async def upload(mcp_data: dict, user: dict = Depends(get_current_user)):
    user_id = user["user_id"]
    refined_data = handler.process_input(user_id, mcp_data, is_query=False, db_provider=db.provider)
    db.add_memory(user_id, refined_data)
    return {"status": "uploaded"}

# Mount frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=os.path.join(frontend_dir, "static")), name="static")

# Serve the main interface at root
@app.get("/")
async def root():
    interface_path = os.path.join(frontend_dir, "components", "interface.html")
    return FileResponse(interface_path)

# Get provider info (public endpoint, no auth required)
@app.get("/providers")
async def get_providers():
    try:
        from llm.config import DEFAULT_PROVIDER, PROVIDERS
        from database.config import DEFAULT_DB_PROVIDER
        
        llm_model = PROVIDERS.get(DEFAULT_PROVIDER, {}).get('model', 'unknown')
        return {
            "llm": llm_model,
            "storage": DEFAULT_DB_PROVIDER
        }
    except Exception as e:
        return {
            "llm": "unknown",
            "storage": "unknown"
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)), reload=False)
