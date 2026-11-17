"""
Activity 18.2 - Try It Yourself

Objective: Build a Total Cost of Ownership (TCO) cloud infrastructure model
comparing monthly spend across MongoDB Atlas vs. multi-database setups at scale.
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "tco_cost_model"

TCO_COMPARISON = [
    {"workload_scale": "10M Txns / Month",  "unified_mongo_atlas_cost": "$420 / mo",  "fragmented_polyglot_cost": "$1,150 / mo", "savings_pct": "63.5% TCO Savings"},
    {"workload_scale": "100M Txns / Month", "unified_mongo_atlas_cost": "$2,850 / mo", "fragmented_polyglot_cost": "$6,900 / mo", "savings_pct": "58.7% TCO Savings"},
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
    print("ACTIVITY 18.2 - TRY IT YOURSELF: CLOUD TCO COST MODEL")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(TCO_COMPARISON)

    print("=== Total Cost of Ownership (TCO) Projection ===")
    for t in TCO_COMPARISON:
        print(f"Scale: {t['workload_scale']:<20} | MongoDB: {t['unified_mongo_atlas_cost']:<14} | Polyglot: {t['fragmented_polyglot_cost']:<16} -> {t['savings_pct']}")

    with open("tco_cost_18_2_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported TCO financial model to tco_cost_18_2_try_it_yourself.json")

if __name__ == "__main__":
    main()
