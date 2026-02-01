import os
from mem0 import Memory
from dotenv import load_dotenv

load_dotenv()

# Use environment variables
groq_key = os.getenv("GROQ_API_KEY")
if groq_key == "your_groq_key": groq_key = None

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "path": r"C:\Users\rattu\Downloads\agentic-bi-natural-language-querying\agentic-bi-saas\memories\qdrant_storage",
            "collection_name": "agentic_bi_memories"
        }
    },
    "llm": {
        "provider": "groq",
        "config": {
            "model": "llama-3.3-70b-versatile",
            "api_key": groq_key
        }
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "sentence-transformers/all-MiniLM-L6-v2"
        }
    }
}

memory = None
try:
    if groq_key:
        print(f"[MEMORY] Initializing with key: {groq_key[:5]}...")
        memory = Memory.from_config(config)
        print("[MEMORY] Mem0 initialized successfully with real provider.")
    else:
        print("[MEMORY] GROQ_API_KEY missing or invalid - Using Mock Memory.")
except Exception as e:
    print(f"[MEMORY] CRITICAL: Initialization failed: {e}")
    import traceback
    traceback.print_exc()

# Provide a mock memory object if init fails to prevent crashes
if memory is None:
    class MockMemory:
        def add(self, *args, **kwargs): 
            print("[MEMORY-MOCK] Add ignored (Initialization failed)")
            pass
        def search(self, *args, **kwargs): 
            print("[MEMORY-MOCK] Search returned [] (Initialization failed)")
            return []
    memory = MockMemory()
