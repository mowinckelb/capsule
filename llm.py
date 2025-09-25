import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from defaults import PROVIDERS, DEFAULT_PROVIDER

load_dotenv()

class LLMHandler:
    def __init__(self, provider: str = DEFAULT_PROVIDER):
        self.provider = provider
        if provider not in PROVIDERS:
            raise ValueError(f"Provider '{provider}' not in PROVIDERS")
        provider_config = PROVIDERS[provider]
        if provider == 'grok':
            api_key = os.getenv(provider_config['api_key_env'])
            if not api_key:
                raise ValueError(f"No {provider_config['api_key_env']}")
            self.api_key = api_key
            self.base_url = provider_config['base_url']
            self.model = provider_config['model']
            self.system_prompt = provider_config.get('system_prompt', '') + " Handle MCP multi-modal input (text/image via tools)."
        else:
            # TODO: Add new provider setup here, e.g., elif provider == 'anthropic': self.client = Anthropic(os.getenv(provider_config['api_key_env']))
            raise NotImplementedError(f"Provider '{provider}' not implemented yet—add in __init__ using provider_config")

    def process_input(self, user_id: str, input_text: str | Dict[str, Any], is_query: bool = False, db_provider: str = None) -> str:
        # Parse input: str or MCP dict (future-ready)
        content = input_text if isinstance(input_text, str) else input_text.get('messages', [{}])[-1].get('content', str(input_text))
        
        if self.provider == 'grok':
            prompt = f"{'Optimize this query' if is_query else 'Refine this input'} for {db_provider or 'abstracted'} storage in user {user_id}'s sovereign DB: {content}"
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            response = requests.post(self.base_url, headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        else:
            # TODO: Add new provider logic here, e.g., elif self.provider == 'anthropic': client.messages.create with tools
            raise NotImplementedError(f"Provider '{self.provider}' not implemented yet—add in process_input using provider_config")

if __name__ == "__main__":
    handler = LLMHandler()
    print(handler.process_input('test', 'Dune book', is_query=False))