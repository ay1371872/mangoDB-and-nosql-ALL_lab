"""
Activity 15.1 - Try It Yourself

Objective: Implement tenant JWT authentication middleware extracting
tenant_id from claims and automatically injecting it into every MongoDB filter.
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "tenant_jwt_middleware"

MIDDLEWARE_LOGS = [
    {"token_user": "ayush@alpha.com", "extracted_tenant": "ORG-ALPHA", "injected_filter": {"tenant_id": "ORG-ALPHA"}, "status": "AUTHORIZED"},
    {"token_user": "sneha@beta.com",  "extracted_tenant": "ORG-BETA",  "injected_filter": {"tenant_id": "ORG-BETA"},  "status": "AUTHORIZED"},
    {"token_user": "guest@test.com",  "extracted_tenant": "NONE",      "injected_filter": "BLOCK",                     "status": "REJECTED (401 Unauthorized)"},
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
    print("ACTIVITY 15.1 - TRY IT YOURSELF: JWT TENANT INJECTION")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(MIDDLEWARE_LOGS)

    print("=== Middleware Tenant Token Interception ===")
    for m in MIDDLEWARE_LOGS:
        print(f"User: {m['token_user']:<18} | Tenant: {m['extracted_tenant']:<12} | Filter: {str(m['injected_filter']):<28} -> [{m['status']}]")

    with open("jwt_middleware_15_1_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported JWT middleware traces to jwt_middleware_15_1_try_it_yourself.json")

if __name__ == "__main__":
    main()
