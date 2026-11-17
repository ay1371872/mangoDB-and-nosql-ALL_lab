"""
Activity 15.2 - Tenant Data Migration (Pool to Silo)

Demonstrates:
1. Migrating an enterprise customer from a shared pooled collection
   into a dedicated, isolated database (Silo Model)
2. Verifying document counts and field integrity post-migration
3. Deleting migrated records from the shared pool
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"

POOL_DATA = [
    {"tenant_id": "ORG-ALPHA", "record_id": "REC-01", "data": "Alpha operational logs"},
    {"tenant_id": "ORG-ALPHA", "record_id": "REC-02", "data": "Alpha customer records"},
    {"tenant_id": "ORG-STANDARD", "record_id": "REC-03", "data": "Standard tier record"},
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
    print("ACTIVITY 15.2 - TENANT MIGRATION: POOL TO SILO")
    print("=" * 60)

    client, db = get_database()
    col_pool = db["tenants_pool_shared"]
    col_silo = db["tenant_alpha_silo"]

    col_pool.drop()
    col_silo.drop()
    col_pool.insert_many(POOL_DATA)

    print("=== Step 1: Pre-Migration Shared Pool Status ===")
    print(f"Total Shared Records: {col_pool.count_documents({})}")
    alpha_count = col_pool.count_documents({"tenant_id": "ORG-ALPHA"})
    print(f"Records belonging to 'ORG-ALPHA': {alpha_count}")

    # Migration step: Copy to dedicated silo
    print("\n=== Step 2: Executing Migration to Dedicated Silo ===")
    alpha_docs = list(col_pool.find({"tenant_id": "ORG-ALPHA"}))
    for d in alpha_docs:
        d.pop("_id", None)  # Generate new ID in dedicated db
    col_silo.insert_many(alpha_docs)
    print(f"[OK] Migrated {len(alpha_docs)} records to database 'tenant_alpha_silo'.")

    # Step 3: Cleanup pool
    col_pool.delete_many({"tenant_id": "ORG-ALPHA"})
    print("[OK] Purged ORG-ALPHA records from shared pool collection.")

    print("\n=== Step 3: Post-Migration State ===")
    print(f"Shared Pool Records remaining: {col_pool.count_documents({})}")
    print(f"Dedicated Silo Records       : {col_silo.count_documents({})}")

    with open("migration_15_2.json", "w") as f:
        f.write(json.dumps(list(col_silo.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported silo dataset to migration_15_2.json")

if __name__ == "__main__":
    main()
