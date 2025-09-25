from llm import LLMManager
print("Creating LLMManager...")
manager = LLMManager()
print("Available providers:", manager.get_available())
print("Default provider:", manager.default)
if manager.default:
    try:
        result = manager.process_input('test', 'Dune book', is_query=False)
        print("Result:", result)
    except Exception as e:
        print("Error:", e)
