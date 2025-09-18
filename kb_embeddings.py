import json
import time
from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path

KB_FILE = "kb_data.json"
CHECK_INTERVAL = 10  # seconds

# Initialize model & Chroma
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection_name = "health_kb"

# Create or get collection
if collection_name in [c.name for c in client.list_collections()]:
    collection = client.get_collection(collection_name)
else:
    collection = client.create_collection(collection_name)

def load_kb():
    with open(KB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def update_embeddings(kb_data):
    existing_ids = collection.get()['ids']
    for item in kb_data:
        if item["id"] not in existing_ids:
            emb = model.encode(item["text"]).tolist()
            collection.add(documents=[item["text"]], embeddings=[emb], ids=[item["id"]])
            print(f"Added new KB entry: {item['topic']}")

if __name__ == "__main__":
    last_mod = 0
    while True:
        kb_path = Path(KB_FILE)
        if kb_path.exists():
            mod_time = kb_path.stat().st_mtime
            if mod_time != last_mod:
                kb_data = load_kb()
                update_embeddings(kb_data)
                last_mod = mod_time
        time.sleep(CHECK_INTERVAL)
