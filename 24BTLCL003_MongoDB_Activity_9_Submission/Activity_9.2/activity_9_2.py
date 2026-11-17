"""
Activity 9.2 - Simulate Network Partition & Rollback

Demonstrates:
1. Simulating network partition isolating Primary from majority
2. Quorum loss detection and automatic Primary step-down
3. Rollback mechanics when partitioned node reconnects
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "partition_simulation"

PARTITION_STEPS = [
    {"step": 1, "phase": "STEADY_STATE", "majority_partition": "Nodes [0, 1, 2] healthy; writes with w:majority succeed"},
    {"step": 2, "phase": "PARTITIONED",  "majority_partition": "Node 0 severed from Nodes 1 & 2 by network wall"},
    {"step": 3, "phase": "QUORUM_LOST",  "majority_partition": "Node 0 loses majority, steps down to SECONDARY to prevent split-brain"},
    {"step": 4, "phase": "NEW_PRIMARY",  "majority_partition": "Node 1 elected new PRIMARY by Nodes 1 & 2"},
    {"step": 5, "phase": "REINTEGRATION", "majority_partition": "Node 0 reconnected; uncommitted local writes written to rollback file"},
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
    print("ACTIVITY 9.2 - NETWORK PARTITION & ROLLBACK SIMULATION")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(PARTITION_STEPS)

    print("=== Network Partition Lifecycle ===")
    for p in PARTITION_STEPS:
        print(f"Step {p['step']}: [{p['phase']:<14}] -> {p['majority_partition']}")

    print("\nRollback Protection: MongoDB prevents split-brain writes by enforcing majority consensus (CP architecture).")

    with open("partition_9_2.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported partition event dataset to partition_9_2.json")

if __name__ == "__main__":
    main()
