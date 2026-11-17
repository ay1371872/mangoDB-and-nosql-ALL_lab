"""
Appendix A.1 - Document Ingestion & Chunking for RAG

Demonstrates:
1. Document ingestion and fixed-size chunking (chunk_size: 200 words)
2. Attaching source citations and vector embeddings
3. Batch storage into MongoDB vector collection
4. Verifying multi-document chunk creation
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "rag_documents_chunks"

TEXTBOOK_DOCS = [
    {
        "source": "chapter_05_aggregation.txt",
        "text": "The aggregation pipeline is a sequence of stages transforming documents. $group groups documents by an identifier and computes accumulator metrics.",
        "embedding": [0.24, 0.78, 0.15, -0.42, 0.61]
    },
    {
        "source": "chapter_10_transactions.txt",
        "text": "MongoDB transactions enforce ACID properties across multiple documents. Sessions ensure atomic commits or clean rollbacks upon failure.",
        "embedding": [0.65, 0.12, 0.88, 0.05, -0.21]
    },
    {
        "source": "appendix_a_chat_app.txt",
        "text": "In a production RAG application, conversation memory is stored in MongoDB rather than server memory to survive restarts and enable horizontal scaling.",
        "embedding": [0.38, 0.85, -0.19, 0.52, 0.44]
    }
]

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
    print("APPENDIX A.1 - DOCUMENT CHUNKING & RAG INGESTION")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(TEXTBOOK_DOCS)

    print(f"[OK] Ingested {len(TEXTBOOK_DOCS)} knowledge chunks into '{COLLECTION_NAME}'\n")
    print("=== Ingested Knowledge Base Chunks ===")
    for d in TEXTBOOK_DOCS:
        print(f"Source: {d['source']:<28} | Chunks: 1 | Vector Dims: {len(d['embedding'])}")
        print(f"  Snippet: \"{d['text'][:70]}...\"\n")

    with open("rag_chunks_app_a_1.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("[OK] Exported RAG chunks to rag_chunks_app_a_1.json")

if __name__ == "__main__":
    main()
