# LLM configuration for the LLM module
# This is self-contained within the LLM feature branch

import os
from dotenv import load_dotenv

load_dotenv()

# List of available providers (add new here for easy extension)
PROVIDERS = {
    'grok': {
        'api_key_env': 'GROK_API_KEY',
        'base_url': 'https://api.x.ai/v1/chat/completions',
        'model': 'grok-4',
        'system_prompt': "You are an intermediary for a personal vector database. For storage, refine input into JSON only: {summary: concise str summary, tags: list of 5-10 key phrases for semantic search}. For queries, refine for relevance. User: {user_id}. Handle MCP multi-modal input (text/image via tools). No extras or Markdown."
    },
    # TODO: Add new providers here, e.g., 'anthropic': {'api_key_env': 'ANTHROPIC_API_KEY', 'model': 'claude-3-5-sonnet-20241022', ...}
}

# Default from env, validated against PROVIDERS
DEFAULT_PROVIDER = os.getenv('DEFAULT_PROVIDER', 'grok')
if DEFAULT_PROVIDER not in PROVIDERS:
    raise ValueError(f"Invalid DEFAULT_PROVIDER '{DEFAULT_PROVIDER}': Must be in {list(PROVIDERS.keys())}")
