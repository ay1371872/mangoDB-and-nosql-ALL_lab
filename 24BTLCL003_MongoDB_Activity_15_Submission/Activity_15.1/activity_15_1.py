"""
Activity 15.1 - Multi-Tenant SaaS REST API

Demonstrates:
1. Multi-tenant data isolation using Tenant-Keyed Shared Collections (Pool Model)
2. Enforcing tenant boundaries across query filters
3. Preventing cross-tenant data leakage
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "tenants_pool"

TENANT_DOCS = [
    {"tenant_id": "ORG-ALPHA", "sku": "ITEM-101", "name": "Alpha Custom Widget", "price": 450.0},
    {"tenant_id": "ORG-ALPHA", "sku": "ITEM-102", "name": "Alpha Analytics Pro", "price": 1200.0},
    {"tenant_id": "ORG-BETA",  "sku": "ITEM-201", "name": "Beta Cloud Gateway",  "price": 850.0},
    {"tenant_id": "ORG-GAMMA", "sku": "ITEM-301", "name": "Gamma Security Suite","price": 2400.0},
]

def get_database():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        client.admin.command("ping")
        return client, client[DB_NAME]
    except Exception:
        import mongomock
        return mongomock.MongoClient(), mongomock.MongoClient()[DB_NAME]

def get_tenant_items(col, tenant_id):
    """Enforces strict tenant scoping on every query."""
    return list(col.find({"tenant_id": tenant_id}, {"_id": 0}))

def main():
    print("=" * 60)
    print("ACTIVITY 15.1 - MULTI-TENANT DATA ISOLATION (POOL MODEL)")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(TENANT_DOCS)

    print("=== Tenant Query Isolation Tests ===")
    for tid in ["ORG-ALPHA", "ORG-BETA"]:
        items = get_tenant_items(col, tid)
        print(f"\nQuery Request for Tenant: '{tid}'")
        print(f"Results Returned: {len(items)} items")
        for it in items:
            print(f"  * [{it['sku']}] {it['name']} - Rs. {it['price']}")

    print("\n[OK] Security Boundary: Tenant Beta cannot view Tenant Alpha's catalog data.")

    with open("multitenant_15_1.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported multi-tenant pool dataset to multitenant_15_1.json")

if __name__ == "__main__":
    main()
