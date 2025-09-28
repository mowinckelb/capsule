"""
Capsule CLI Interface

This provides a command-line interface to the Capsule system using all modules.
"""

import sys
import os
from pathlib import Path

# Add current directory to path for module imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import integrated services
from database import database_service
from llm import llm_service
from authentication import auth_service

def chat_with_llm():
    """Command-line interface for Capsule"""
    print("🧠 Welcome to Capsule CLI!")
    print("Are you an existing user? (yes/no)")
    is_existing = input("> ").strip().lower()
    
    if is_existing == "no":
        print("Enter new user ID and password.")
        new_user_id = input("New User ID: ").strip()
        new_password = input("New Password: ").strip()
        
        try:
            auth_service.register(new_user_id, new_password)
            print(f"✅ User {new_user_id} registered successfully!")
            user_id = new_user_id
        except Exception as e:
            print(f"❌ Registration failed: {e}")
            return
            
    elif is_existing == "yes":
        print("Enter your user ID and password.")
        user_id = input("User ID: ").strip()
        password = input("Password: ").strip()
        
        if not auth_service.authenticate(user_id, password):
            print("❌ Wrong password or user ID.")
            return
    else:
        print("Please enter 'yes' or 'no'.")
        return
    
    print(f"✅ Authenticated as {user_id}")
    print("Commands:")
    print("  input: <memory>    - Save a memory")
    print("  output: <question> - Ask a question")
    print("  exit              - Quit")
    print()
    
    while True:
        user_input = input(f"{user_id}> ").strip()
        
        if user_input.lower() == "exit":
            break
            
        if user_input.lower().startswith("input:"):
            memory = user_input[6:].strip()
            try:
                # Process through LLM
                refined = llm_service.process_input(
                    user_id, 
                    memory, 
                    is_query=False, 
                    db_provider=database_service.get_provider()
                )
                # Store in database
                database_service.add_memory(user_id, refined)
                print("💾 Memory saved successfully!")
            except Exception as e:
                print(f"❌ Error saving memory: {e}")
                
        elif user_input.lower().startswith("output:"):
            query = user_input[7:].strip()
            try:
                # Process query through LLM
                refined = llm_service.process_input(
                    user_id, 
                    query, 
                    is_query=True, 
                    db_provider=database_service.get_provider()
                )
                # Query database
                results = database_service.query_memories(user_id, refined)
                
                if results:
                    # Generate natural language response
                    summary_prompt = f"Answer this question: '{query}' using only this information: {results}. Give a direct, natural answer."
                    response = llm_service.process_input(user_id, summary_prompt, is_query=False)
                    
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
        else:
            print("Use 'input: <memory>' or 'output: <question>'.")
    
    print("👋 Goodbye!")

if __name__ == "__main__":
    chat_with_llm()
