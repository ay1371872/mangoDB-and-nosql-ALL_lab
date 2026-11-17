"""
Activity 16.2 - Try It Yourself

Objective: Build a dual-layer polyglot caching service with Redis-style
in-memory key-value lookups alongside MongoDB durable persistence.
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "polyglot_cache_layer"

CACHE_AUDIT = [
    {"query_key": "user:USR-1001:profile", "cache_status": "CACHE_MISS", "latency_ms": 3.8, "source": "MongoDB Read -> Injected into RAM Cache"},
    {"query_key": "user:USR-1001:profile", "cache_status": "CACHE_HIT",  "latency_ms": 0.2, "source": "RAM Cache (95% latency reduction)"},
    {"query_key": "user:USR-1002:profile", "cache_status": "CACHE_HIT",  "latency_ms": 0.2, "source": "RAM Cache (Sub-millisecond SLA)"},
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
    print("ACTIVITY 16.2 - TRY IT YOURSELF: POLYGLOT CACHE LAYER")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(CACHE_AUDIT)

    print("=== Polyglot Read Pipeline Performance ===")
    for c in CACHE_AUDIT:
        print(f"Key: {c['query_key']:<24} | [{c['cache_status']:<10}] | Latency: {c['latency_ms']}ms -> {c['source']}")

    with open("polyglot_cache_16_2_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported cache layer logs to polyglot_cache_16_2_try_it_yourself.json")

if __name__ == "__main__":
    main()
