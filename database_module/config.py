# Database configuration for the database module
# This is self-contained within the database feature branch

import os
from dotenv import load_dotenv

load_dotenv()

# DB Providers (add new for easy extension)
DB_PROVIDERS = {
    'pinecone': {
        'api_key_env': 'PINECONE_API_KEY',
        'index_name': 'capsule-data',
        'dimension': 384,
        'metric': 'cosine',
        'cloud': 'aws',
        'region': 'us-east-1'
    },
    # TODO: Add new, e.g., 'chroma': {'path': 'local_db', 'embedding_model': 'all-MiniLM-L6-v2'}
}

DEFAULT_DB_PROVIDER = os.getenv('DEFAULT_DB_PROVIDER', 'pinecone')
if DEFAULT_DB_PROVIDER not in DB_PROVIDERS:
    raise ValueError(f"Invalid DEFAULT_DB_PROVIDER '{DEFAULT_DB_PROVIDER}': Must be in {list(DB_PROVIDERS.keys())}")
