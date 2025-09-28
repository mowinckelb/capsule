"""
Grok LLM Implementation

This implements the LLM interface using Grok API.
This file can be modified/improved without affecting other modules.
"""

import os
import requests
import json
from typing import Dict, Any, Union
from dotenv import load_dotenv

from .interface import LLMInterface

load_dotenv()


class GrokLLMImplementation(LLMInterface):
    """Grok-specific implementation of LLM interface"""
    
    def __init__(self):
        self.api_key = os.getenv('GROK_API_KEY')
        self.base_url = 'https://api.x.ai/v1/chat/completions'
        self.model = 'grok-4'
        
        # Different system prompts for different use cases
        self.storage_prompt = (
            "You are an intermediary for a personal vector database. "
            "For storage, refine input into JSON only: "
            "{summary: concise str summary, tags: list of 5-10 key phrases for semantic search}. "
            "No extras or Markdown."
        )
        
        self.query_prompt = (
            "You are an intermediary for a personal vector database. "
            "For queries, refine for relevance and semantic search. "
            "Return JSON: {summary: search-optimized summary, tags: relevant search terms}."
        )
        
        self.response_prompt = (
            "You are a helpful assistant. Answer questions naturally and directly "
            "based on the provided information. Do not return JSON or structured data."
        )
        
        if not self.api_key:
            raise ValueError("GROK_API_KEY not found in environment variables")
    
    def process_input(self, user_id: str, input_text: Union[str, Dict[str, Any]], 
                     is_query: bool = False, context: str = None) -> Union[str, Dict[str, Any]]:
        """Process input through Grok API"""
        
        # Parse input content
        if isinstance(input_text, str):
            content = input_text
        elif isinstance(input_text, dict):
            content = input_text.get('messages', [{}])[-1].get('content', str(input_text))
        else:
            content = str(input_text)
        
        # Determine system prompt and user prompt based on use case
        if "Answer this question:" in content:
            # Natural language response
            system_prompt = self.response_prompt
            user_prompt = content
        elif is_query:
            # Query optimization
            system_prompt = self.query_prompt
            user_prompt = f"Optimize this query for semantic search in user {user_id}'s database: {content}"
        else:
            # Storage preparation
            system_prompt = self.storage_prompt
            user_prompt = f"Refine this input for storage in user {user_id}'s database: {content}"
        
        # Add context if provided
        if context:
            user_prompt += f" Context: {context}"
        
        # Make API call
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                self.base_url, 
                headers={
                    "Authorization": f"Bearer {self.api_key}", 
                    "Content-Type": "application/json"
                }, 
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            response_data = response.json()
            content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not content:
                return {'content': 'No response from LLM', 'tags': [], 'summary': 'No response'}
            
            # If this was a natural language request, return string directly
            if "Answer this question:" in user_prompt:
                return content.strip()
            
            # Otherwise, try to parse as JSON for structured data
            try:
                parsed = json.loads(content)
                return parsed
            except json.JSONDecodeError:
                return {'content': content, 'tags': [], 'summary': content}
                
        except requests.RequestException as e:
            raise RuntimeError(f"LLM API request failed: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"LLM processing failed: {str(e)}")
    
    def health_check(self) -> bool:
        """Check if Grok API is accessible"""
        try:
            test_payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "health check"}],
                "max_tokens": 10
            }
            
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=test_payload,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception:
            return False
    
    def get_provider_info(self) -> Dict[str, str]:
        """Get Grok provider information"""
        return {
            "provider": "grok",
            "model": self.model,
            "base_url": self.base_url,
            "api_key_status": "configured" if self.api_key else "missing"
        }
