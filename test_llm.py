if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    from llm import LLMHandler
    handler = LLMHandler()
    print("Handler created successfully!")