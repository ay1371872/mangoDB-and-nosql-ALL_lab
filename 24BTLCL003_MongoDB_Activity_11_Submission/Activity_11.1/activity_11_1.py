"""
Activity 11.1 - Shard Key Evaluation

Demonstrates:
1. Evaluating candidate shard keys on Cardinality, Frequency, and Write Distribution
2. Identifying jumbo chunk risks with low-cardinality keys
3. Evaluating scatter-gather query overhead vs targeted shard routing
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "shard_key_eval"

CANDIDATE_KEYS = [
    {"key": "country",       "cardinality": "Very Low (~195)", "frequency": "High write skew on top countries", "routing": "Scatter-gather for user queries", "verdict": "POOR - High risk of un-splittable jumbo chunks"},
    {"key": "created_at",    "cardinality": "Infinite",        "frequency": "Monotonically increasing writes",   "routing": "Targeted by date ranges",          "verdict": "POOR - Single shard write bottleneck (hotspot)"},
    {"key": "user_id",       "cardinality": "High (Millions)", "frequency": "Evenly distributed user actions",   "routing": "Targeted point queries to 1 shard","verdict": "GOOD - Uniform data & write distribution"},
    {"key": "{_id: 'hashed'}","cardinality": "Maximum",        "frequency": "Perfect pseudo-random spread",     "routing": "Scatter-gather for range queries",  "verdict": "EXCELLENT for writes, poor for date ranges"}
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
    print("ACTIVITY 11.1 - SHARD KEY EVALUATION CRITERIA")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(CANDIDATE_KEYS)

    print("=== Shard Key Analysis Matrix ===")
    print(f"{'Candidate Key':<18} {'Cardinality':<18} {'Write Skew Risk':<25} {'Verdict'}")
    print("-" * 80)
    for k in CANDIDATE_KEYS:
        print(f"{k['key']:<18} {k['cardinality']:<18} {k['frequency'][:23]:<25} {k['verdict'][:30]}")

    print("\nConclusion: Compound shard keys like {tenant_id: 1, user_id: 1} or Hashed keys yield optimal throughput.")

    with open("shard_key_eval_11_1.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported shard evaluation matrix to shard_key_eval_11_1.json")

if __name__ == "__main__":
    main()
