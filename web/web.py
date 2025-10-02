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
from contextlib import contextmanager

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("⚠️  psycopg2 not available, using SQLite fallback")

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

# Database connection helper
@contextmanager
def get_db_connection():
    """Get database connection (PostgreSQL if available, SQLite fallback)"""
    database_url = os.getenv('DATABASE_URL')
    
    if database_url and database_url.startswith('postgresql') and POSTGRES_AVAILABLE:
        # Use PostgreSQL
        conn = psycopg2.connect(database_url)
        try:
            yield conn
        finally:
            conn.close()
    else:
        # Fallback to SQLite for local development
        conn = sqlite3.connect("users.db")
        try:
            yield conn
        finally:
            conn.close()

def is_postgres():
    """Check if using PostgreSQL"""
    database_url = os.getenv('DATABASE_URL')
    return database_url and database_url.startswith('postgresql') and POSTGRES_AVAILABLE

# Initialize database for users
def init_user_db():
    database_url = os.getenv('DATABASE_URL')
    
    if database_url and database_url.startswith('postgresql') and POSTGRES_AVAILABLE:
        # PostgreSQL initialization
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            user_id TEXT PRIMARY KEY,
                            hashed_password TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    conn.commit()
            print("✓ PostgreSQL users table initialized")
        except Exception as e:
            print(f"✗ PostgreSQL initialization failed: {e}")
    else:
        # SQLite initialization
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, hashed_password TEXT)")
        conn.commit()
        conn.close()
        print("✓ SQLite users database initialized (local fallback)")

# Initialize database on startup
init_user_db()

# Debug environment variables on startup
print("=== Environment Variables Debug ===")
print(f"GROK_API_KEY: {'Set' if os.getenv('GROK_API_KEY') else 'Not set'}")
print(f"PINECONE_API_KEY: {'Set' if os.getenv('PINECONE_API_KEY') else 'Not set'}")
print(f"DEFAULT_PROVIDER: {os.getenv('DEFAULT_PROVIDER', 'grok')}")
print(f"DEFAULT_DB_PROVIDER: {os.getenv('DEFAULT_DB_PROVIDER', 'pinecone')}")
print(f"DATABASE_URL: {'Set (PostgreSQL)' if os.getenv('DATABASE_URL') else 'Not set (SQLite)'}")
print(f"Using database: {'PostgreSQL' if is_postgres() else 'SQLite'}")
print("=====================================")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        placeholder = "%s" if is_postgres() else "?"
        cursor.execute(f"SELECT user_id FROM users WHERE user_id = {placeholder}", (token,))
        user = cursor.fetchone()
        
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return {"user_id": user[0]}

@app.post("/register")
async def register(user_id: str = Form(), password: str = Form()):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        placeholder = "%s" if is_postgres() else "?"
        
        # Check if user exists
        cursor.execute(f"SELECT user_id FROM users WHERE user_id = {placeholder}", (user_id,))
        if cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists")
        
        # Hash password and insert
        hashed_password = pwd_context.hash(password)
        cursor.execute(f"INSERT INTO users (user_id, hashed_password) VALUES ({placeholder}, {placeholder})", (user_id, hashed_password))
        conn.commit()
        
    return {"status": "registered"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        placeholder = "%s" if is_postgres() else "?"
        cursor.execute(f"SELECT hashed_password FROM users WHERE user_id = {placeholder}", (form_data.username,))
        user = cursor.fetchone()
        
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
    
    hashed_password = user[0]
    
    if not pwd_context.verify(form_data.password, hashed_password):
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

# Admin endpoints for user management
@app.get("/admin/users")
async def list_all_users(user: dict = Depends(get_current_user)):
    """List all users (requires authentication)"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, created_at FROM users ORDER BY created_at DESC")
            users = cursor.fetchall()
        
        return {
            "users": [
                {
                    "user_id": u[0],
                    "created_at": str(u[1]) if len(u) > 1 and u[1] else "unknown"
                } for u in users
            ],
            "count": len(users)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/admin/users/{user_id}")
async def delete_user(user_id: str, user: dict = Depends(get_current_user)):
    """Delete a specific user (requires authentication)"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            placeholder = "%s" if is_postgres() else "?"
            
            # Check if user exists
            cursor.execute(f"SELECT user_id FROM users WHERE user_id = {placeholder}", (user_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="user not found")
            
            # Delete user
            cursor.execute(f"DELETE FROM users WHERE user_id = {placeholder}", (user_id,))
            conn.commit()
        
        return {"status": "deleted", "user_id": user_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/admin/users")
async def delete_all_users(user: dict = Depends(get_current_user)):
    """Delete all users - USE WITH CAUTION (requires authentication)"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            
            cursor.execute("DELETE FROM users")
            conn.commit()
        
        return {"status": "all users deleted", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)), reload=False)
