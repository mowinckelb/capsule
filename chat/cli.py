"""
Capsule CLI Interface

This provides a command-line interface to the Capsule system using all modules.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for module imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent))

# Import integrated services
from database.interface import database_service
from llm.interface import llm_service
from authentication.interface import auth_service

class CapsuleCLI:
    """Command-line interface for Capsule"""
    
    def __init__(self):
        self.current_user = None
        self.running = False
    
    def authenticate_user(self):
        """Handle user authentication"""
        print("🧠 Welcome to Capsule CLI!")
        print("Are you an existing user? (yes/no)")
        is_existing = input("> ").strip().lower()
        
        if is_existing == "no":
            return self._register_new_user()
        elif is_existing == "yes":
            return self._login_existing_user()
        else:
            print("Please enter 'yes' or 'no'.")
            return False
    
    def _register_new_user(self):
        """Register a new user"""
        print("Enter new user ID and password.")
        new_user_id = input("New User ID: ").strip()
        new_password = input("New Password: ").strip()
        
        try:
            auth_service.register(new_user_id, new_password)
            print(f"✅ User {new_user_id} registered successfully!")
            self.current_user = new_user_id
            return True
        except Exception as e:
            print(f"❌ Registration failed: {e}")
            return False
    
    def _login_existing_user(self):
        """Login an existing user"""
        print("Enter your user ID and password.")
        user_id = input("User ID: ").strip()
        password = input("Password: ").strip()
        
        try:
            if auth_service.authenticate(user_id, password):
                self.current_user = user_id
                return True
            else:
                print("❌ Wrong password or user ID.")
                return False
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def show_help(self):
        """Display available commands"""
        print(f"✅ Authenticated as {self.current_user}")
        print("Commands:")
        print("  input: <memory>    - Save a memory")
        print("  output: <question> - Ask a question") 
        print("  help              - Show this help")
        print("  exit              - Quit")
        print()
    
    def process_input_command(self, memory):
        """Process an input (save memory) command"""
        try:
            # Process through LLM
            refined = llm_service.process_input(
                self.current_user, 
                memory, 
                is_query=False, 
                db_provider=database_service.get_provider()
            )
            # Store in database
            database_service.add_memory(self.current_user, refined)
            print("💾 Memory saved successfully!")
        except Exception as e:
            print(f"❌ Error saving memory: {e}")
    
    def process_output_command(self, query):
        """Process an output (query) command"""
        try:
            # Process query through LLM
            refined = llm_service.process_input(
                self.current_user, 
                query, 
                is_query=True, 
                db_provider=database_service.get_provider()
            )
            # Query database
            results = database_service.query_memories(self.current_user, refined)
            
            if results:
                # Generate natural language response
                summary_prompt = f"Answer this question: '{query}' using only this information: {results}. Give a direct, natural answer."
                response = llm_service.process_input(self.current_user, summary_prompt, is_query=False)
                
                if isinstance(response, str):
                    print(f"💡 {response}")
                elif isinstance(response, dict):
                    print(f"💡 {response.get('content', 'Based on your memories: ' + ', '.join(results))}")
                else:
                    print(f"💡 Based on your memories: {', '.join(results)}")
            else:
                print("🤔 No matching memories found.")
        except Exception as e:
            print(f"❌ Error processing query: {e}")
    
    def process_command(self, user_input):
        """Process a user command"""
        if user_input.lower() == "exit":
            return False
        elif user_input.lower() == "help":
            self.show_help()
        elif user_input.lower().startswith("input:"):
            memory = user_input[6:].strip()
            if memory:
                self.process_input_command(memory)
            else:
                print("Please provide a memory after 'input:'")
        elif user_input.lower().startswith("output:"):
            query = user_input[7:].strip()
            if query:
                self.process_output_command(query)
            else:
                print("Please provide a question after 'output:'")
        else:
            print("Unknown command. Use 'help' to see available commands.")
        
        return True
    
    def run(self):
        """Main CLI loop"""
        if not self.authenticate_user():
            return
        
        self.show_help()
        self.running = True
        
        while self.running:
            try:
                user_input = input(f"{self.current_user}> ").strip()
                if not self.process_command(user_input):
                    break
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
        
        print("👋 Session ended!")

def main():
    """Entry point for CLI"""
    cli = CapsuleCLI()
    cli.run()

if __name__ == "__main__":
    main()
