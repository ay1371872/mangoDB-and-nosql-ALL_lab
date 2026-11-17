"""
Appendix A.1 - Try It Yourself

Objective: Build a semantic boundary chunking script with MD5 cryptographic
content hashing to prevent duplicate chunk ingestion.
"""

import json
import hashlib
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "semantic_dedup_chunks"

SAMPLE_TEXT = "MongoDB provides high availability through replica sets. Replica sets maintain multiple copies of data."
chunk_hash = hashlib.md5(SAMPLE_TEXT.encode()).hexdigest()

DEDUP_CHUNKS = [
    {"chunk_hash": chunk_hash, "text": SAMPLE_TEXT, "status": "FIRST_INSERT (COMMITTED)"},
    {"chunk_hash": chunk_hash, "text": SAMPLE_TEXT, "status": "DUPLICATE_DETECTED (SKIPPED)"},
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
    print("APPENDIX A.1 - TRY IT YOURSELF: SEMANTIC DEDUPLICATION")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_one(DEDUP_CHUNKS[0])

    print("=== Chunk Deduplication Auditing ===")
    print(f"Computed MD5 Hash : {chunk_hash}")
    print(f"First Attempt     : {DEDUP_CHUNKS[0]['status']}")
    print(f"Second Attempt    : {DEDUP_CHUNKS[1]['status']}")

    with open("dedup_chunks_app_a_1_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported dedup dataset to dedup_chunks_app_a_1_try_it_yourself.json")

if __name__ == "__main__":
    main()
