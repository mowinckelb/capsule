import os
import uuid
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from defaults import DB_PROVIDERS, DEFAULT_DB_PROVIDER

load_dotenv()

class DBHandler:
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
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.index_name = provider_config['index_name']
            self.dimension = provider_config['dimension']
            self.metric = provider_config['metric']
            self.spec = ServerlessSpec(cloud=provider_config['cloud'], region=provider_config['region'])
        else:
            # TODO: Add new provider setup here, e.g., elif provider == 'chroma': self.client = chromadb.Client(provider_config['path'])
            raise NotImplementedError(f"Provider '{provider}' not implemented yet—add in __init__ using provider_config")

    def get_index(self):
        if self.provider == 'pinecone':
            index_name = self.index_name
            if index_name not in self.pc.list_indexes().names():
                self.pc.create_index(name=index_name, dimension=self.dimension, metric=self.metric, spec=self.spec)
            return self.pc.Index(index_name)
        else:
            raise NotImplementedError(f"get_index not implemented for '{self.provider}'")

    def add_memory(self, user_id: str, memory: str | dict):
        if self.provider == 'pinecone':
            index = self.get_index()
            if isinstance(memory, dict):
                content = memory.get('content', memory)
                content = str(content) if not isinstance(content, str) else content
                if not content:
                    content = ''
                vector = self.model.encode(content).tolist()
                metadata = {'summary': memory.get('summary', ''), 'tags': memory.get('tags', [])}
            else:
                content = memory
                content = str(content) if not isinstance(content, str) else content
                if not content:
                    content = ''
                vector = self.model.encode(memory).tolist()
                metadata = {"memory": memory}
            index.upsert(vectors=[(f"id_{user_id}_{uuid.uuid4()}", vector, metadata)], namespace=user_id)
        else:
            raise NotImplementedError(f"add_memory not implemented for '{self.provider}'")

    def query_memories(self, user_id: str, query_text: str):
        if self.provider == 'pinecone':
            index = self.get_index()
            query_vector = self.model.encode(query_text).tolist()
            results = index.query(vector=query_vector, top_k=5, include_metadata=True, namespace=user_id)
            return [match.metadata.get("memory", match.metadata.get("summary", "")) for match in results.matches]
        else:
            raise NotImplementedError(f"query_memories not implemented for '{self.provider}'")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    db = DBHandler()
    db.add_memory('test', 'Test memory')
    print(db.query_memories('test', 'memory'))