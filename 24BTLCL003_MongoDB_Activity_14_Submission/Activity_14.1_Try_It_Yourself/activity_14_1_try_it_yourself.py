"""
Activity 14.1 - Try It Yourself

Objective: Build an operational alerting daemon that checks system health
metrics and triggers critical warnings when thresholds are breached.
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "alert_thresholds"

ALERTS = [
    {"metric": "connection_pool",  "value": "88%",  "threshold": "80%",  "level": "WARNING",  "message": "Connection pool usage exceeded safe threshold."},
    {"metric": "dirty_cache_pct",  "value": "18.5%","threshold": "20%",  "level": "NORMAL",   "message": "Eviction threads keeping pace with writes."},
    {"metric": "slow_query_count", "value": "14/m",  "threshold": "5/m",  "level": "CRITICAL", "message": "Spike in unindexed table scans detected!"},
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
    print("ACTIVITY 14.1 - TRY IT YOURSELF: MONITORING ALERT DAEMON")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(ALERTS)

    print("=== Health Diagnostic Alarm Triggers ===")
    for a in ALERTS:
        print(f"[{a['level']:<8}] Metric: {a['metric']:<18} | Value: {a['value']:<6} (Limit: {a['threshold']}) -> {a['message']}")

    with open("alerts_14_1_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported alert definitions to alerts_14_1_try_it_yourself.json")

if __name__ == "__main__":
    main()
