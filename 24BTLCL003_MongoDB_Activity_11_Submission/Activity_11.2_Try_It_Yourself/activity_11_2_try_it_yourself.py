"""
Activity 11.2 - Try It Yourself

Objective: Simulate chunk split and background balancer migrations
across 4 virtual shards to maintain equitable data density.
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "balancer_migration"

MIGRATION_STEPS = [
    {"step": 1, "action": "INITIAL_LOAD",    "shards": {"s1": 42, "s2": 10, "s3": 8, "s4": 6},  "imbalance_ratio": "4.2 (Balancer Triggered)"},
    {"step": 2, "action": "CHUNK_SPLIT",     "shards": {"s1": 56, "s2": 10, "s3": 8, "s4": 6},  "imbalance_ratio": "5.6 (Jumbo split into 14 chunks)"},
    {"step": 3, "action": "BALANCER_MIGRATE","shards": {"s1": 20, "s2": 20, "s3": 20, "s4": 20}, "imbalance_ratio": "1.0 (Cluster Rebalanced)"},
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
    print("ACTIVITY 11.2 - TRY IT YOURSELF: CHUNK BALANCER SIMULATION")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(MIGRATION_STEPS)

    print("=== Background Chunk Balancer Progression ===")
    for m in MIGRATION_STEPS:
        print(f"Step {m['step']}: {m['action']:<18} | Shards: {m['shards']} | Imbalance: {m['imbalance_ratio']}")

    print("\n[OK] Balancer achieved perfect 25% chunk parity across all 4 shards.")

    with open("balancer_11_2_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported balancer steps to balancer_11_2_try_it_yourself.json")

if __name__ == "__main__":
    main()
