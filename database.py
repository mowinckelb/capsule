import os
import uuid
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def get_index():
    index_name = "capsule-data"
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    return pc.Index(index_name)

def add_memory(user_id: str, memory: str):
    index = get_index()
    vector = [0.0] * 384  # Placeholder vector
    index.upsert(vectors=[(f"id_{user_id}_{uuid.uuid4()}", vector, {"memory": memory})], namespace=user_id)

def query_memories(user_id: str, query_text: str):
    index = get_index()
    query_vector = [0.0] * 384  # Placeholder vector
    results = index.query(vector=query_vector, top_k=5, include_metadata=True, namespace=user_id)
    return [match.metadata["memory"] for match in results.matches]