import chromadb

def get_user_collection(user_id: str):
    client = chromadb.PersistentClient(path=f"./data_{user_id}")
    return client.get_or_create_collection("memories")

def add_memory(user_id: str, memory: str):
    get_user_collection(user_id).add(
        documents=[memory],
        metadatas=[{"user_id": user_id}],
        ids=[f"id_{len(get_user_collection(user_id).get()['ids'])}"]
    )

def query_memories(user_id: str, query_text: str):
    return get_user_collection(user_id).query(
        query_texts=[query_text],
        n_results=5
    )["documents"]