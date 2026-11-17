"""
Activity 6.1 - Try It Yourself

Objective: Implement Partial Indexes and Time-To-Live (TTL) indexes to reduce
index storage overhead for active sessions and automate document expiration.
"""

import json
from bson import json_util
from pymongo import MongoClient, ASCENDING

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "sessions_ttl"

SESSIONS = [
    {"session_id": "SES-101", "user": "Arjun", "status": "active",   "ip": "192.168.1.10", "ttl_seconds": 3600},
    {"session_id": "SES-102", "user": "Sneha", "status": "expired",  "ip": "192.168.1.12", "ttl_seconds": 0},
    {"session_id": "SES-103", "user": "Rahul", "status": "active",   "ip": "192.168.1.15", "ttl_seconds": 1800},
    {"session_id": "SES-104", "user": "Kavya", "status": "abandoned","ip": "192.168.1.20", "ttl_seconds": 0},
    {"session_id": "SES-105", "user": "Divya", "status": "active",   "ip": "192.168.1.25", "ttl_seconds": 7200},
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
    print("ACTIVITY 6.1 - TRY IT YOURSELF: PARTIAL & TTL INDEXES")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(SESSIONS)
    print(f"[OK] Seeded {len(SESSIONS)} user session records\n")

    # 1. Partial Index: only indexes documents where status == 'active'
    print("=== 1. Creating Partial Index for Active Sessions ===")
    try:
        idx_partial = col.create_index(
            [("session_id", ASCENDING)],
            partialFilterExpression={"status": "active"},
            name="idx_partial_active_sessions"
        )
        print(f"[OK] Created partial index: {idx_partial}")
    except Exception as e:
        idx_partial = col.create_index([("session_id", ASCENDING)], name="idx_active_sessions")
        print(f"[OK] Created fallback index: {idx_partial} ({e})")

    # 2. TTL simulation
    print("\n=== 2. Creating TTL Index on Session Expiry ===")
    try:
        idx_ttl = col.create_index([("ttl_seconds", ASCENDING)], expireAfterSeconds=0, name="idx_ttl_session")
        print(f"[OK] Created TTL index: {idx_ttl}")
    except Exception as e:
        idx_ttl = col.create_index([("ttl_seconds", ASCENDING)], name="idx_ttl_session")
        print(f"[OK] Created index: {idx_ttl}")

    print("\n=== 3. Querying Active Sessions Covered by Partial Index ===")
    active_sessions = list(col.find({"status": "active"}))
    for s in active_sessions:
        print(f"Session: {s['session_id']:<10} User: {s['user']:<10} IP: {s['ip']:<16} Status: {s['status']}")

    with open("sessions_6_1_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported sessions dataset to sessions_6_1_try_it_yourself.json")

if __name__ == "__main__":
    main()
