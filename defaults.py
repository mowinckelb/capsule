import os
from dotenv import load_dotenv

load_dotenv()

# List of available providers (add new here for easy extension)
PROVIDERS = {
    'grok': {
        'api_key_env': 'GROK_API_KEY',
        'base_url': 'https://api.x.ai/v1/chat/completions',
        'model': 'grok-4',
        'system_prompt': "You are an intermediary for a personal vector database. Refine inputs for storage or optimize queries for retrieval, ensuring clarity and relevance."
    },
    # TODO: Add new providers here, e.g., 'anthropic': {'api_key_env': 'ANTHROPIC_API_KEY', 'model': 'claude-3-5-sonnet-20241022', ...}
}

# Default from env, validated against PROVIDERS
DEFAULT_PROVIDER = os.getenv('DEFAULT_PROVIDER', 'grok')
if DEFAULT_PROVIDER not in PROVIDERS:
    raise ValueError(f"Invalid DEFAULT_PROVIDER '{DEFAULT_PROVIDER}': Must be in {list(PROVIDERS.keys())}")

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