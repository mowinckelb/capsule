"""
LLM Module Usage Example

This shows how other modules should interact with the LLM module.
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import llm_service


def example_usage():
    """Demonstrate how to use the LLM module"""
    
    print("LLM Module Usage Example")
    print("=" * 30)
    
    # Check if service is healthy
    if not llm_service.health_check():
        print("✗ LLM service is not healthy")
        return
    
    print("✓ LLM service is healthy")
    
    # Get provider info
    info = llm_service.get_info()
    print(f"Provider: {info.get('provider', 'unknown')}")
    
    try:
        # Example 1: Process input for storage
        print("\n1. Processing input for storage:")
        storage_result = llm_service.process_input(
            user_id="example_user",
            input_text="I really enjoy eating sushi and reading science fiction books",
            is_query=False
        )
        print(f"Storage result: {storage_result}")
        
        # Example 2: Process query
        print("\n2. Processing query:")
        query_result = llm_service.process_input(
            user_id="example_user",
            input_text="what are my interests?",
            is_query=True
        )
        print(f"Query result: {query_result}")
        
        # Example 3: Generate natural language response
        print("\n3. Generating natural language response:")
        response_result = llm_service.process_input(
            user_id="example_user",
            input_text="Answer this question: What do I like to eat? Using: User enjoys sushi",
            is_query=False
        )
        print(f"Response: {response_result}")
        
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    example_usage()
