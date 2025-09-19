import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def get_user_collection(user_id: str):
    index_name = f"capsule-{user_id}"
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    return pc.Index(index_name)

def add_memory(user_id: str, memory: str):
    index = get_user_collection(user_id)
    vector = [0.0] * 1536  # Placeholder; replace with actual embedding in production
    index.upsert(vectors=[(f"id_{user_id}_{index.stats()['total_vector_count']}", vector, {"user_id": user_id, "memory": memory})])

def query_memories(user_id: str, query_text: str):
    index = get_user_collection(user_id)
    query_vector = [0.0] * 1536  # Placeholder; replace with actual embedding
    results = index.query(vector=query_vector, top_k=5, filter={"user_id": user_id})
    return [match["metadata"]["memory"] for match in results["matches"]]