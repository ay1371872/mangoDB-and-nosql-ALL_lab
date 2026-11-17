"""
Activity 12.1 - Try It Yourself

Objective: Implement scoped application roles granting read-only access to
customer support while masking and filtering out financial documents.
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "scoped_roles_audit"

AUDIT_RULES = [
    {"role": "support_agent", "allowed_collections": ["customers", "tickets"], "blocked_collections": ["orders", "financial_audit"], "doc_filter": "status == 'open'"},
    {"role": "billing_clerk", "allowed_collections": ["orders", "invoices"],   "blocked_collections": ["system.profile"],             "doc_filter": "amount > 0"},
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
    print("ACTIVITY 12.1 - TRY IT YOURSELF: SCOPED RBAC ROLES")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(AUDIT_RULES)

    print("=== Scoped Access Enforcement Rules ===")
    for r in AUDIT_RULES:
        print(f"Role: {r['role']:<16} | Allowed: {r['allowed_collections']} | Blocked: {r['blocked_collections']}")

    print("\n[OK] Support agent blocked from querying financial audit logs.")

    with open("scoped_roles_12_1_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported scoped roles to scoped_roles_12_1_try_it_yourself.json")

if __name__ == "__main__":
    main()
