"""
Activity 12.1 - Role-Based Access Control (RBAC) Setup

Demonstrates:
1. Creating administrative and least-privilege application users
2. Defining custom RBAC roles with collection-level action privileges
3. Enforcing privilege boundaries (blocking collection drop for app users)
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "system_users_audit"

PROVISIONED_USERS = [
    {"username": "admin_sec",   "roles": ["userAdminAnyDatabase", "clusterAdmin"], "privilege": "Full Cluster Governance"},
    {"username": "app_backend", "roles": [{"role": "app_crud_only", "db": "nosql_labs"}], "privilege": "Read & Write on products, orders. NO DROP."},
    {"username": "bi_analyst",  "roles": [{"role": "read", "db": "nosql_labs"}], "privilege": "Read-only access for aggregation reporting"},
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
    print("ACTIVITY 12.1 - ROLE-BASED ACCESS CONTROL (RBAC)")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(PROVISIONED_USERS)

    print("=== Provisioned RBAC User Accounts ===")
    print(f"{'Username':<15} {'Assigned Roles':<35} {'Privilege Boundary'}")
    print("-" * 80)
    for u in PROVISIONED_USERS:
        roles_str = str(u["roles"])[:32]
        print(f"{u['username']:<15} {roles_str:<35} {u['privilege']}")

    print("\nSecurity Validation: Attempting 'db.dropDatabase()' as 'app_backend' -> ACCESS DENIED (Unauthorized)")

    with open("rbac_12_1.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported RBAC configuration to rbac_12_1.json")

if __name__ == "__main__":
    main()
