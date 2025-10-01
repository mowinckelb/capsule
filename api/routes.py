from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import os
from pathlib import Path

from .config import API_CONFIG
from .dependencies import get_database_service, get_llm_service, get_auth_service

class APIRoutes:
    """
    API Routes handler - contains all FastAPI endpoints
    """
    
    def __init__(self):
        self.app = FastAPI(
            title=API_CONFIG['title'],
            description=API_CONFIG['description'],
            version=API_CONFIG['version']
        )
        self._setup_middleware()
        self._setup_routes()
    
    def _setup_middleware(self):
        """Setup CORS and other middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
    
    def _setup_routes(self):
        """Setup all API routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def root():
            """Root endpoint - Serve the web interface"""
            try:
                # Get the frontend HTML file
                frontend_path = Path(__file__).parent.parent / "frontend" / "components" / "interface.html"
                if frontend_path.exists():
                    return frontend_path.read_text(encoding='utf-8')
                else:
                    # Fallback to API info if frontend not found
                    return """
                    <html><body>
                    <h1>🧠 Capsule - Personal Memory System</h1>
                    <p>Frontend interface not found. API is running at <a href="/docs">/docs</a></p>
                    </body></html>
                    """
            except Exception as e:
                return f"""
                <html><body>
                <h1>🧠 Capsule - Personal Memory System</h1>
                <p>Error loading interface: {e}</p>
                <p>API is running at <a href="/docs">/docs</a></p>
                </body></html>
                """
        
        @self.app.get("/api")
        async def api_info():
            """API info endpoint"""
            return {
                "message": "🧠 Capsule - Personal Memory System",
                "status": "running",
                "version": "1.0.0",
                "endpoints": {
                    "register": "POST /register - Register a new user",
                    "login": "POST /login - Login user",
                    "add": "POST /add - Add a memory",
                    "query": "GET /query?q=your_question - Query memories",
                    "upload": "POST /upload - Upload MCP data",
                    "health": "GET /health - Health check",
                    "users": "GET /users - List users (admin)",
                    "docs": "GET /docs - API documentation"
                }
            }
        
        @self.app.post("/register")
        async def register(user_id: str = Form(), password: str = Form()):
            """Register a new user"""
            try:
                auth_service = get_auth_service()
                result = auth_service.register(user_id, password)
                return {"status": "registered"}
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/login")
        async def login(form_data: OAuth2PasswordRequestForm = Depends()):
            """Login a user"""
            try:
                auth_service = get_auth_service()
                return auth_service.login(form_data.username, form_data.password)
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/add")
        async def add_memory(memory: str = Form(), user: dict = Depends(self._get_current_user)):
            """Add a memory for the authenticated user"""
            try:
                llm_service = get_llm_service()
                database_service = get_database_service()
                
                user_id = user["user_id"]
                
                # Process the memory through LLM
                refined_memory = llm_service.process_input(
                    user_id, 
                    memory, 
                    is_query=False, 
                    db_provider=database_service.get_provider()
                )
                
                # Store in database
                database_service.add_memory(user_id, refined_memory)
                
                return {"status": "added"}
                
            except Exception as e:
                print(f"Error in /add: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/query")
        async def query_memories(q: str, user: dict = Depends(self._get_current_user)):
            """Query memories for the authenticated user"""
            try:
                llm_service = get_llm_service()
                database_service = get_database_service()
                
                user_id = user["user_id"]
                print(f"Processing query for user {user_id}: {q}")
                
                # Process the query through LLM
                refined_query = llm_service.process_input(
                    user_id, 
                    q, 
                    is_query=True, 
                    db_provider=database_service.get_provider()
                )
                print(f"Refined query: {refined_query}")
                
                # Query the database
                results = database_service.query_memories(user_id, refined_query)
                print(f"Query results: {results}")
                
                if results and len(results) > 0:
                    # Filter out empty results
                    filtered_results = [r for r in results if r and str(r).strip()]
                    if filtered_results:
                        # Generate natural language response
                        summary_prompt = f"Answer this question: '{q}' using only this information: {filtered_results}. Give a direct, natural answer without any metadata."
                        response = llm_service.process_input(user_id, summary_prompt, is_query=False)
                        print(f"LLM response: {response}")
                        
                        # Handle response based on type
                        if isinstance(response, str):
                            response_text = response
                        elif isinstance(response, dict):
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
        
        @self.app.post("/upload")
        async def upload_data(mcp_data: dict, user: dict = Depends(self._get_current_user)):
            """Upload MCP data for the authenticated user"""
            try:
                llm_service = get_llm_service()
                database_service = get_database_service()
                
                user_id = user["user_id"]
                
                # Process the data through LLM
                refined_data = llm_service.process_input(
                    user_id, 
                    mcp_data, 
                    is_query=False, 
                    db_provider=database_service.get_provider()
                )
                
                # Store in database
                database_service.add_memory(user_id, refined_data)
                
                return {"status": "uploaded"}
                
            except Exception as e:
                print(f"Error in /upload: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            try:
                llm_service = get_llm_service()
                database_service = get_database_service()
                auth_service = get_auth_service()
                
                health_status = {
                    "api": "healthy",
                    "llm": llm_service.health_check(),
                    "database": database_service.health_check(),
                    "authentication": auth_service.health_check()
                }
                
                all_healthy = all(health_status.values())
                
                return {
                    "status": "healthy" if all_healthy else "degraded",
                    "services": health_status
                }
                
            except Exception as e:
                return {
                    "status": "unhealthy",
                    "error": str(e)
                }
        
        @self.app.get("/users")
        async def list_users(user: dict = Depends(self._get_current_user)):
            """List all users (admin function)"""
            try:
                auth_service = get_auth_service()
                users = auth_service.list_users()
                return {"users": users}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/providers")
        async def get_providers():
            """Get LLM and storage provider info"""
            try:
                from llm.config import DEFAULT_PROVIDER, PROVIDERS
                from database.config import DEFAULT_DB_PROVIDER
                llm_model = PROVIDERS.get(DEFAULT_PROVIDER, {}).get('model', 'unknown')
                return {"llm": llm_model, "storage": DEFAULT_DB_PROVIDER}
            except:
                return {"llm": "unknown", "storage": "unknown"}

        # Mount static files (for web interface)
        if API_CONFIG['serve_static']:
            try:
                # Mount frontend static files
                frontend_static_path = Path(__file__).parent.parent / "frontend" / "static"
                if frontend_static_path.exists():
                    self.app.mount("/static", StaticFiles(directory=str(frontend_static_path)), name="frontend_static")
                    print(f"✅ Mounted frontend static files from {frontend_static_path}")
            except Exception as e:
                print(f"⚠️ Could not mount static files: {e}")
    
    def _get_current_user(self, token: str = Depends(get_auth_service().get_oauth2_scheme())):
        """Get current user dependency"""
        auth_service = get_auth_service()
        return auth_service.get_user_from_token(token)
    
    def get_app(self) -> FastAPI:
        """Get the FastAPI application"""
        return self.app


# Create the main API instance
api_routes = APIRoutes()
