"""
Activity 11.1 - Try It Yourself

Objective: Evaluate Compound Shard Keys combining tenant_id and created_at
to balance multi-tenant data locality with uniform time-series distribution.
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "compound_shard_key"

TENANT_SHARD_ROUTING = [
    {"tenant_id": "TNT-A", "chunk_count": 14, "target_shard": "shard-01", "query_routing": "Targeted (Single Shard)"},
    {"tenant_id": "TNT-B", "chunk_count": 18, "target_shard": "shard-02", "query_routing": "Targeted (Single Shard)"},
    {"tenant_id": "TNT-C", "chunk_count": 12, "target_shard": "shard-03", "query_routing": "Targeted (Single Shard)"},
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
    print("ACTIVITY 11.1 - TRY IT YOURSELF: COMPOUND SHARD KEY ROUTING")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(TENANT_SHARD_ROUTING)

    print("=== Multi-Tenant Compound Shard Key Routing ===")
    for t in TENANT_SHARD_ROUTING:
        print(f"Tenant: {t['tenant_id']} -> Routed to {t['target_shard']} ({t['chunk_count']} chunks) | {t['query_routing']}")

    print("\nBenefit: Eliminates scatter-gather queries for all tenant-scoped operations.")

    with open("compound_shard_11_1_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported compound routing to compound_shard_11_1_try_it_yourself.json")

if __name__ == "__main__":
    main()
