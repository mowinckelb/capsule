"""
Provider Configurations

Configuration for LLM and database providers.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# LLM Providers configuration
LLM_PROVIDERS = {
    'grok': {
        'api_key_env': 'GROK_API_KEY',
        'base_url': 'https://api.x.ai/v1/chat/completions',
        'model': 'grok-4',
        'system_prompt': "You are an intermediary for a personal vector database. For storage, refine input into JSON only: {summary: concise str summary, tags: list of 5-10 key phrases for semantic search}. For queries, refine for relevance. User: {user_id}. Handle MCP multi-modal input (text/image via tools). No extras or Markdown.",
        'max_tokens': int(os.getenv('GROK_MAX_TOKENS', '4000')),
        'temperature': float(os.getenv('GROK_TEMPERATURE', '0.7')),
        'timeout': int(os.getenv('GROK_TIMEOUT', '30')),
    },
    'anthropic': {
        'api_key_env': 'ANTHROPIC_API_KEY',
        'base_url': 'https://api.anthropic.com/v1/messages',
        'model': 'claude-3-5-sonnet-20241022',
        'system_prompt': "You are an intermediary for a personal vector database. For storage, refine input into JSON only: {summary: concise str summary, tags: list of 5-10 key phrases for semantic search}. For queries, refine for relevance. User: {user_id}. Handle MCP multi-modal input (text/image via tools). No extras or Markdown.",
        'max_tokens': int(os.getenv('ANTHROPIC_MAX_TOKENS', '4000')),
        'temperature': float(os.getenv('ANTHROPIC_TEMPERATURE', '0.7')),
        'timeout': int(os.getenv('ANTHROPIC_TIMEOUT', '30')),
    },
    'openai': {
        'api_key_env': 'OPENAI_API_KEY',
        'base_url': 'https://api.openai.com/v1/chat/completions',
        'model': 'gpt-4',
        'system_prompt': "You are an intermediary for a personal vector database. For storage, refine input into JSON only: {summary: concise str summary, tags: list of 5-10 key phrases for semantic search}. For queries, refine for relevance. User: {user_id}. Handle MCP multi-modal input (text/image via tools). No extras or Markdown.",
        'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '4000')),
        'temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.7')),
        'timeout': int(os.getenv('OPENAI_TIMEOUT', '30')),
    }
}

# Database Providers configuration
DATABASE_PROVIDERS = {
    'pinecone': {
        'api_key_env': 'PINECONE_API_KEY',
        'index_name': os.getenv('PINECONE_INDEX_NAME', 'capsule-main'),
        'dimension': int(os.getenv('PINECONE_DIMENSION', '1024')),
        'metric': os.getenv('PINECONE_METRIC', 'cosine'),
        'cloud': os.getenv('PINECONE_CLOUD', 'aws'),
        'region': os.getenv('PINECONE_REGION', 'us-east-1'),
        'timeout': int(os.getenv('PINECONE_TIMEOUT', '30')),
    },
    'chroma': {
        'persist_directory': os.getenv('CHROMA_PERSIST_DIR', './chroma_db'),
        'collection_name': os.getenv('CHROMA_COLLECTION', 'capsule-memories'),
        'embedding_model': os.getenv('CHROMA_EMBEDDING_MODEL', 'all-MiniLM-L6-v2'),
        'distance_metric': os.getenv('CHROMA_DISTANCE_METRIC', 'cosine'),
    },
    'qdrant': {
        'url': os.getenv('QDRANT_URL', 'http://localhost:6333'),
        'api_key_env': 'QDRANT_API_KEY',
        'collection_name': os.getenv('QDRANT_COLLECTION', 'capsule-memories'),
        'vector_size': int(os.getenv('QDRANT_VECTOR_SIZE', '384')),
        'distance': os.getenv('QDRANT_DISTANCE', 'Cosine'),
    }
}

# Default providers
DEFAULT_LLM_PROVIDER = os.getenv('DEFAULT_LLM_PROVIDER', 'grok')
DEFAULT_DATABASE_PROVIDER = os.getenv('DEFAULT_DATABASE_PROVIDER', 'pinecone')

# Validation
if DEFAULT_LLM_PROVIDER not in LLM_PROVIDERS:
    raise ValueError(f"Invalid DEFAULT_LLM_PROVIDER '{DEFAULT_LLM_PROVIDER}': Must be in {list(LLM_PROVIDERS.keys())}")

if DEFAULT_DATABASE_PROVIDER not in DATABASE_PROVIDERS:
    raise ValueError(f"Invalid DEFAULT_DATABASE_PROVIDER '{DEFAULT_DATABASE_PROVIDER}': Must be in {list(DATABASE_PROVIDERS.keys())}")

# Embedding settings
EMBEDDING_CONFIG = {
    'model_name': os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2'),
    'cache_dir': os.getenv('EMBEDDING_CACHE_DIR', './embedding_cache'),
    'batch_size': int(os.getenv('EMBEDDING_BATCH_SIZE', '32')),
    'normalize_embeddings': os.getenv('NORMALIZE_EMBEDDINGS', 'true').lower() == 'true',
}
