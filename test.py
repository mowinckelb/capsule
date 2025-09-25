from llm import LLMHandler
print("Creating LLMHandler...")
handler = LLMHandler()
print("Provider:", handler.provider)
try:
    result = handler.process_input('test', 'Dune book', is_query=False)
    print("Result:", result)
except Exception as e:
    print("Error:", e)