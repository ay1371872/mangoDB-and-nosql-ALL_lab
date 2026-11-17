"""
Activity 17.1 - Vector Search & RAG Pipeline on MongoDB

Demonstrates:
1. Document ingestion and fixed-size chunking with metadata
2. Dense vector embeddings (simulated 384-dimensional vectors)
3. Cosine similarity context retrieval
4. Assembling prompt context for Generative AI (RAG)
"""

import json
import math
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "vector_knowledge_base"

KNOWLEDGE_CHUNKS = [
    {
        "chunk_id": "CHK-01",
        "doc_title": "MongoDB Architecture Overview",
        "text": "WiredTiger is the default storage engine in MongoDB, providing document-level concurrency and checkpoint durability.",
        "embedding": [0.45, 0.82, -0.12, 0.33, 0.71]  # Representative dense vector
    },
    {
        "chunk_id": "CHK-02",
        "doc_title": "Replica Set Elections",
        "text": "MongoDB replica sets use a Raft-like consensus election where priority biases the probability of winning the primary role.",
        "embedding": [0.12, 0.35, 0.88, -0.05, 0.62]
    },
    {
        "chunk_id": "CHK-03",
        "doc_title": "Sharding & Scalability",
        "text": "Hashed sharding ensures uniform write distribution across chunks, preventing monotonic key write bottlenecks.",
        "embedding": [0.75, 0.15, 0.22, 0.81, -0.19]
    }
]

def cosine_similarity(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

def get_database():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        client.admin.command("ping")
        return client, client[DB_NAME]
    except Exception:
        import mongomock
        return mongomock.MongoClient(), mongomock.MongoClient()[DB_NAME]

def main():
    print("=" * 60)
    print("ACTIVITY 17.1 - VECTOR SEARCH & RAG PIPELINE")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(KNOWLEDGE_CHUNKS)
    print(f"[OK] Ingested {len(KNOWLEDGE_CHUNKS)} vector-embedded knowledge chunks\n")

    user_query = "How does WiredTiger handle checkpoints and concurrency?"
    query_vector = [0.42, 0.80, -0.10, 0.30, 0.68]  # Semantic representation

    print(f"Incoming User Query: \"{user_query}\"")
    print("Computing Vector Similarity Retrieval (Top-K)...")

    ranked = []
    for doc in col.find():
        score = cosine_similarity(query_vector, doc["embedding"])
        ranked.append((score, doc))
    ranked.sort(key=lambda x: x[0], reverse=True)

    print("\n=== Retrieved Context Ranked by Cosine Similarity ===")
    for score, doc in ranked:
        print(f"Similarity: {score:.4f} | Document: {doc['doc_title']}")
        print(f"  Excerpt: \"{doc['text'][:75]}...\"\n")

    top_chunk = ranked[0][1]
    rag_prompt = f"Context: {top_chunk['text']}\n\nQuestion: {user_query}\nAnswer:"
    print("=== Assembled RAG Prompt for LLM Dispatch ===")
    print(rag_prompt)

    with open("rag_pipeline_17_1.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported vector chunks to rag_pipeline_17_1.json")

if __name__ == "__main__":
    main()
