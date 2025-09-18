import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROK_API_KEY")
BASE_URL = "https://api.x.ai/v1/chat/completions"

def process_input(user_id: str, input_text: str, is_query: bool = False):
    prompt = f"{'Optimize this query' if is_query else 'Refine this input'} for a personal vector database for user {user_id}: {input_text}"
    payload = {
        "model": "grok-4",
        "messages": [
            {"role": "system", "content": "You are an intermediary for a personal vector database. Refine inputs for storage or optimize queries for retrieval, ensuring clarity and relevance."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post(BASE_URL, headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]