import os
import uuid
import logging
from datetime import datetime
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from config.providers import DATABASE_PROVIDERS as DB_PROVIDERS, DEFAULT_DATABASE_PROVIDER as DEFAULT_DB_PROVIDER

# Only import if not using Pinecone inference
USE_LOCAL_EMBEDDINGS = os.getenv('USE_LOCAL_EMBEDDINGS', 'false').lower() == 'true'
if USE_LOCAL_EMBEDDINGS:
    from sentence_transformers import SentenceTransformer

load_dotenv()
logger = logging.getLogger(__name__)

class DBHandler:
    _model = None
    
    def __init__(self, provider: str = DEFAULT_DB_PROVIDER):
        self.provider = provider
        if provider not in DB_PROVIDERS:
            raise ValueError(f"Provider '{provider}' not in DB_PROVIDERS")
        provider_config = DB_PROVIDERS[provider]
        if provider == 'pinecone':
            api_key = os.getenv(provider_config['api_key_env'])
            if not api_key:
                raise ValueError(f"No {provider_config['api_key_env']}")
            self.pc = Pinecone(api_key=api_key)
            self.index_name = provider_config['index_name']
            self.dimension = provider_config['dimension']
            self.metric = provider_config['metric']
            self.spec = ServerlessSpec(cloud=provider_config['cloud'], region=provider_config['region'])
            self._index = None
            self.use_inference = not USE_LOCAL_EMBEDDINGS
        else:
            # TODO: Add new provider setup here, e.g., elif provider == 'chroma': self.client = chromadb.Client(provider_config['path'])
            raise NotImplementedError(f"Provider '{provider}' not implemented yet—add in __init__ using provider_config")

    @property
    def model(self):
        if not USE_LOCAL_EMBEDDINGS:
            return None
        if DBHandler._model is None:
            DBHandler._model = SentenceTransformer('all-MiniLM-L6-v2')
        return DBHandler._model
    
    def _embed_text(self, text: str):
        """Generate embeddings using Pinecone inference or local model"""
        if self.use_inference:
            # Use Pinecone's inference API - no local model needed
            embeddings = self.pc.inference.embed(
                model="multilingual-e5-large",
                inputs=[text],
                parameters={"input_type": "passage"}
            )
            return embeddings[0]['values']
        else:
            # Use local SentenceTransformer
            return self.model.encode(text).tolist()

    def get_index(self):
        if self.provider == 'pinecone':
            if self._index is None:
                index_name = self.index_name
                if index_name not in self.pc.list_indexes().names():
                    self.pc.create_index(name=index_name, dimension=self.dimension, metric=self.metric, spec=self.spec)
                self._index = self.pc.Index(index_name)
            return self._index
        else:
            raise NotImplementedError(f"get_index not implemented for '{self.provider}'")

    def add_memory(self, user_id: str, memory: str | dict):
        if self.provider == 'pinecone':
            index = self.get_index()
            timestamp = datetime.now().isoformat()
            
            if isinstance(memory, dict):
                content = str(memory.get('content', memory.get('summary', '')))
                if not content:
                    content = ' '
                vector = self._embed_text(content)
                metadata = {
                    'memory': content,
                    'summary': memory.get('summary', ''),
                    'tags': memory.get('tags', []),
                    'timestamp': timestamp
                }
            else:
                content = str(memory) if memory else ' '
                vector = self._embed_text(content)
                metadata = {
                    "memory": content,
                    "timestamp": timestamp
                }
            index.upsert(vectors=[(f"id_{user_id}_{uuid.uuid4()}", vector, metadata)], namespace=user_id)
        else:
            raise NotImplementedError(f"add_memory not implemented for '{self.provider}'")

    def query_memories(self, user_id: str, query_text: str | dict, top_k: int = 5):
        if self.provider == 'pinecone':
            index = self.get_index()
            
            if isinstance(query_text, dict):
                text_content = str(query_text.get('summary', query_text.get('content', str(query_text))))
            else:
                text_content = str(query_text)
            
            if not text_content:
                text_content = ' '
            
            query_vector = self._embed_text(text_content)
            results = index.query(vector=query_vector, top_k=top_k, include_metadata=True, namespace=user_id)
            if not results or not hasattr(results, 'matches') or not results.matches:
                return []
            return [match.metadata.get("memory", match.metadata.get("summary", "")) for match in results.matches if match.metadata]
        else:
            raise NotImplementedError(f"query_memories not implemented for '{self.provider}'")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    db = DBHandler()
    db.add_memory('test', 'Test memory')
    print(db.query_memories('test', 'memory'))
