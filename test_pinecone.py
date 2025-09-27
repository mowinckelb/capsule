from dotenv import load_dotenv
import os
from pinecone import Pinecone

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY", "")
print("Loaded key prefix:", api_key[:20])

pc = Pinecone()  # uses a PINECONE_API_KEY env variable by default
try:
    print("Accessible indexes:", pc.list_indexes().names())
except Exception as e:
    print("Error listing indexes:", e)