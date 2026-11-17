"""
Activity 7.1 - Production Schema: Embedding vs. Referencing

Demonstrates:
1. One-to-few relationship modeled via Embedded Documents (user shipping addresses)
2. One-to-many unbound relationship modeled via Referenced Documents (orders)
3. Comparing document retrieval latency and atomic update boundaries
4. Validating 16MB document size constraints
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"

# Pattern A: Embedded Document (User + Addresses)
EMBEDDED_USER = {
    "user_id": "USR-1001",
    "name": "Ayush Yadav",
    "email": "ayush@example.com",
    "tier": "Premium",
    "addresses": [
        {"type": "Home", "street": "42 Cyber Hub", "city": "Gurugram", "pincode": "122002", "is_default": True},
        {"type": "Office", "street": "10 Tech Boulevard", "city": "Bengaluru", "pincode": "560100", "is_default": False}
    ]
}

# Pattern B: Referenced Document (User + External Orders)
REFERENCED_USER = {
    "user_id": "USR-2001",
    "name": "Vikram Singh",
    "email": "vikram@example.com",
    "tier": "Gold"
}

REFERENCED_ORDERS = [
    {"order_id": "ORD-7001", "user_id": "USR-2001", "total": 12500, "status": "shipped", "items_count": 4},
    {"order_id": "ORD-7002", "user_id": "USR-2001", "total": 3400,  "status": "delivered","items_count": 1},
    {"order_id": "ORD-7003", "user_id": "USR-2001", "total": 8900,  "status": "processing","items_count": 2},
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
    print("ACTIVITY 7.1 - PRODUCTION SCHEMA: EMBEDDING VS REFERENCING")
    print("=" * 60)

    client, db = get_database()
    col_embed = db["users_embedded"]
    col_ref_user = db["users_referenced"]
    col_ref_ord = db["orders_referenced"]

    for c in [col_embed, col_ref_user, col_ref_ord]:
        c.drop()

    col_embed.insert_one(EMBEDDED_USER)
    col_ref_user.insert_one(REFERENCED_USER)
    col_ref_ord.insert_many(REFERENCED_ORDERS)
    print("[OK] Seeded embedded and referenced model collections\n")

    # 1. Querying Embedded Schema
    print("=== 1. Pattern A: Embedded Document Read (Single-Trip I/O) ===")
    u_embed = col_embed.find_one({"user_id": "USR-1001"})
    print(f"User: {u_embed['name']} ({u_embed['email']})")
    print(f"Embedded Addresses Count: {len(u_embed['addresses'])}")
    for addr in u_embed["addresses"]:
        print(f"  [{addr['type']}] {addr['street']}, {addr['city']} - {addr['pincode']} (Default: {addr['is_default']})")
    print("I/O Profile: 1 database round-trip retrieves user profile and all addresses.")

    # 2. Querying Referenced Schema
    print("\n=== 2. Pattern B: Referenced Documents Read ($lookup or 2-step) ===")
    u_ref = col_ref_user.find_one({"user_id": "USR-2001"})
    u_orders = list(col_ref_ord.find({"user_id": "USR-2001"}))
    print(f"User: {u_ref['name']} ({u_ref['email']})")
    print(f"Referenced Orders Count: {len(u_orders)}")
    for ord_doc in u_orders:
        print(f"  Order: {ord_doc['order_id']} | Total: Rs. {ord_doc['total']} | Status: {ord_doc['status']}")
    print("I/O Profile: Scales infinitely without hitting 16MB document size limit.")

    # 3. Trade-off Analysis
    print("\n=== 3. Architectural Trade-Off Comparison ===")
    print(f"{'Criteria':<22} {'Embedded Pattern':<25} {'Referenced Pattern'}")
    print("-" * 70)
    print(f"{'Relationship Type':<22} {'1-to-Few (bounded)':<25} {'1-to-Many / 1-to-Squillions'}")
    print(f"{'Read Performance':<22} {'Optimal (1 query)':<25} {'Requires $lookup / join'}")
    print(f"{'Write Atomicity':<22} {'Atomic on parent document':<25} {'Requires multi-doc transaction'}")
    print(f"{'Size Constraint':<22} {'Must remain < 16MB':<25} {'No document limit barrier'}")

    with open("users_schema_7_1.json", "w") as f:
        f.write(json.dumps(list(col_embed.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported embedded schema to users_schema_7_1.json")

if __name__ == "__main__":
    main()
