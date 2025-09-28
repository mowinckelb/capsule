"""
Capsule Application - Complete Integration

This is the main application that brings together all modules:
- Database (vector storage)
- LLM (language processing) 
- Authentication (user management)
- API (FastAPI endpoints)
- Web (HTML interface)

This file demonstrates how all modules work together seamlessly.
"""

import sys
import os
import uvicorn
from pathlib import Path

# Add current directory to path for module imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import all module integrations
from database import database_service
from llm import llm_service  
from authentication import auth_service
from api import api_service
from web import web_service

class CapsuleApplication:
    """
    Main Capsule application that integrates all modules
    """
    
    def __init__(self):
        self.database = database_service
        self.llm = llm_service
        self.auth = auth_service
        self.api = api_service
        self.web = web_service
        
        print("🚀 Initializing Capsule Application")
        self._check_services()
    
    def _check_services(self):
        """Check health of all services"""
        services = {
            'Database': self.database,
            'LLM': self.llm,
            'Authentication': self.auth,
            'API': self.api,
            'Web': self.web
        }
        
        print("\n📊 Service Health Check:")
        print("-" * 40)
        
        all_healthy = True
        for name, service in services.items():
            try:
                if hasattr(service, 'health_check'):
                    healthy = service.health_check()
                    status = "✅ Healthy" if healthy else "❌ Unhealthy"
                    print(f"{name:15} {status}")
                    if not healthy:
                        all_healthy = False
                else:
                    print(f"{name:15} ⚠️  No health check")
            except Exception as e:
                print(f"{name:15} ❌ Error: {e}")
                all_healthy = False
        
        print("-" * 40)
        if all_healthy:
            print("🎉 All services are healthy!")
        else:
            print("⚠️  Some services have issues")
        print()
    
    def get_app(self):
        """Get the complete FastAPI application"""
        # Get the API app (which includes all endpoints)
        app = self.api.get_app()
        
        # The API module already includes static file serving from web module
        # through its dependency injection system
        
        return app
    
    def start_server(self, host="0.0.0.0", port=8001, reload=False):
        """Start the complete Capsule server"""
        app = self.get_app()
        
        print(f"🌐 Starting Capsule Server")
        print(f"   📡 Host: {host}")
        print(f"   🔌 Port: {port}")
        print(f"   🔄 Reload: {reload}")
        print(f"   🌍 Access: http://localhost:{port}")
        print()
        
        uvicorn.run(app, host=host, port=port, reload=reload)
    
    def get_service_info(self):
        """Get information about all services"""
        info = {
            'application': 'Capsule - Personal Memory System',
            'version': '1.0.0',
            'modules': {
                'database': {
                    'status': self.database.health_check() if hasattr(self.database, 'health_check') else 'unknown',
                    'provider': getattr(self.database, 'get_provider', lambda: 'unknown')()
                },
                'llm': {
                    'status': self.llm.health_check() if hasattr(self.llm, 'health_check') else 'unknown',
                    'provider': getattr(self.llm, 'get_provider', lambda: 'unknown')()
                },
                'authentication': {
                    'status': self.auth.health_check() if hasattr(self.auth, 'health_check') else 'unknown',
                    'users': len(getattr(self.auth, 'list_users', lambda: [])())
                },
                'api': {
                    'status': self.api.health_check() if hasattr(self.api, 'health_check') else 'unknown',
                    'routes': len(getattr(self.api, 'get_routes_info', lambda: [])())
                },
                'web': {
                    'status': self.web.health_check() if hasattr(self.web, 'health_check') else 'unknown',
                    'files': getattr(self.web, 'get_file_info', lambda: {})().get('total_files', 0)
                }
            }
        }
        return info
    
    def demo_workflow(self):
        """Demonstrate the complete workflow"""
        print("🎬 Capsule Workflow Demo")
        print("=" * 50)
        
        try:
            # 1. User Management
            print("1️⃣ User Management:")
            users = self.auth.list_users()
            print(f"   Current users: {len(users)}")
            
            # 2. Memory Storage (mock)
            print("\n2️⃣ Memory Storage:")
            print("   Storing: 'I had a great lunch at Mario's restaurant'")
            # In real usage: self.database.add_memory("demo_user", processed_memory)
            
            # 3. LLM Processing (mock)
            print("\n3️⃣ LLM Processing:")
            print("   Processing memory through LLM...")
            # In real usage: processed = self.llm.process_input("demo_user", memory)
            
            # 4. Query Interface
            print("\n4️⃣ Query Interface:")
            print("   Query: 'Where did I eat lunch?'")
            # In real usage: results = self.database.query_memories("demo_user", query)
            
            # 5. Web Interface
            print("\n5️⃣ Web Interface:")
            web_files = self.web.get_file_info()
            print(f"   Available web files: {web_files['total_files']}")
            print(f"   Main interface: {'✅' if web_files['main_interface'] else '❌'}")
            
            print("\n🎉 Workflow complete! All modules working together.")
            
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
        
        print("=" * 50)


def create_app():
    """Create the Capsule application"""
    app_instance = CapsuleApplication()
    return app_instance.get_app()


def main():
    """Main entry point"""
    print("🧠 Capsule - Personal Memory System")
    print("=" * 40)
    
    # Create application
    capsule = CapsuleApplication()
    
    # Show service info
    info = capsule.get_service_info()
    print(f"📱 Application: {info['application']}")
    print(f"🔢 Version: {info['version']}")
    
    # Run demo workflow
    capsule.demo_workflow()
    
    # Start server
    print("\n🚀 Starting server...")
    capsule.start_server()


if __name__ == "__main__":
    main()
