import json
from sentence_transformers import SentenceTransformer
import chromadb

# ------------------ Load Knowledge Base ------------------
with open("knowledge.json", "r", encoding="utf-8") as f:
    knowledge = json.load(f)

# ------------------ Initialize Embedding Model ------------------
model = SentenceTransformer('all-MiniLM-L6-v2')

# ------------------ Initialize ChromaDB ------------------
client = chromadb.Client()
collection = client.create_collection("health_kb")

# ------------------ Add Knowledge Base to Chroma ------------------
for item in knowledge:
    embedding = model.encode(item["text"]).tolist()
    collection.add(
        documents=[item["text"]],
        embeddings=[embedding],
        ids=[item["id"]]
    )

# ------------------ Query Function ------------------
def query_health(question: str):
    q_embedding = model.encode(question).tolist()
    results = collection.query(query_embeddings=[q_embedding], n_results=1)
    answer = results['documents'][0][0]
    return answer

# ------------------ Test ------------------
if __name__ == "__main__":
    print(query_health("Mujhe bukhar hai aur temperature high hai"))
