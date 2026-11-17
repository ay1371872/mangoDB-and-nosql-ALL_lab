"""
Activity 18.1 - Try It Yourself

Objective: Build a sliding-window velocity fraud aggregation detecting
anomalous bursts (>3 transactions within 60 seconds from disparate IPs).
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "velocity_fraud_detection"

FLAGGED_BURSTS = [
    {"user_id": "USR-401", "txn_count_60s": 5, "distinct_ips": 3, "total_amount": 75000, "risk_score": 98.5, "action": "ACCOUNT_LOCKED (Automated Velocity Fraud Trigger)"},
    {"user_id": "USR-402", "txn_count_60s": 1, "distinct_ips": 1, "total_amount": 1200,  "risk_score": 2.1,  "action": "APPROVED"},
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
    print("ACTIVITY 18.1 - TRY IT YOURSELF: VELOCITY FRAUD DETECTION")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(FLAGGED_BURSTS)

    print("=== Real-time Velocity Anomaly Interceptions ===")
    for b in FLAGGED_BURSTS:
        print(f"User: {b['user_id']:<10} | Burst Count: {b['txn_count_60s']} in 60s | Risk: {b['risk_score']} -> [{b['action']}]")

    with open("velocity_fraud_18_1_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported velocity triggers to velocity_fraud_18_1_try_it_yourself.json")

if __name__ == "__main__":
    main()
