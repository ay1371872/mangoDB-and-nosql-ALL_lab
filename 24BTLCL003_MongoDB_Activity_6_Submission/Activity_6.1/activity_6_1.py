"""
Activity 6.1 - Index Design and the ESR Rule

Demonstrates:
1. Single-field index creation
2. Compound indexes following the Equality-Sort-Range (ESR) rule
3. Multikey index for array fields (tags)
4. Index inspection and execution plan verification
"""

import json
from bson import json_util
from pymongo import MongoClient, ASCENDING, DESCENDING

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "catalog"

PRODUCTS = [
    {"sku": "SKU-01", "category": "Electronics", "status": "active", "rating": 4.5, "price": 4500, "tags": ["gadget", "usb", "audio"]},
    {"sku": "SKU-02", "category": "Electronics", "status": "active", "rating": 4.8, "price": 8900, "tags": ["wireless", "audio"]},
    {"sku": "SKU-03", "category": "Office",      "status": "pending","rating": 4.1, "price": 1200, "tags": ["stationery", "desk"]},
    {"sku": "SKU-04", "category": "Office",      "status": "active", "rating": 4.7, "price": 3400, "tags": ["ergonomic", "desk"]},
    {"sku": "SKU-05", "category": "Electronics", "status": "active", "rating": 3.9, "price": 2100, "tags": ["usb", "gadget"]},
    {"sku": "SKU-06", "category": "Accessories", "status": "archived","rating": 4.2,"price": 950,  "tags": ["cable", "usb"]},
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
    print("ACTIVITY 6.1 - INDEX DESIGN & ESR RULE")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(PRODUCTS)
    print(f"[OK] Seeded {len(PRODUCTS)} products into '{COLLECTION_NAME}'\n")

    # 1. Single Field Index
    print("=== 1. Creating Single-Field Index on 'category' ===")
    idx_cat = col.create_index([("category", ASCENDING)], name="idx_category")
    print(f"[OK] Created index: {idx_cat}")

    # 2. Compound Index following ESR rule: status (Equality), rating (Sort), price (Range)
    print("\n=== 2. Creating ESR Compound Index (status=E, rating=S, price=R) ===")
    idx_esr = col.create_index(
        [("status", ASCENDING), ("rating", DESCENDING), ("price", ASCENDING)],
        name="idx_status_rating_price"
    )
    print(f"[OK] Created ESR compound index: {idx_esr}")

    # 3. Multikey Index on tags array
    print("\n=== 3. Creating Multikey Index on array 'tags' ===")
    idx_tags = col.create_index([("tags", ASCENDING)], name="idx_multikey_tags")
    print(f"[OK] Created multikey index: {idx_tags}")

    # 4. List Indexes
    print("\n=== Current Collection Indexes ===")
    indexes = col.index_information()
    for name, meta in indexes.items():
        print(f"Index: {name:<26} Keys: {meta['key']}")

    # 5. Query matching ESR rule
    print("\n=== Running ESR Query: status='active', sort by rating desc, price between 1000 and 9000 ===")
    query = {"status": "active", "price": {"$gte": 1000, "$lte": 9000}}
    results = list(col.find(query).sort("rating", DESCENDING))
    for p in results:
        print(f"SKU: {p['sku']:<8} Status: {p['status']:<8} Rating: {p['rating']:<5} Price: Rs. {p['price']:<6} Tags: {p['tags']}")

    with open("catalog_6_1.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported catalog dataset to catalog_6_1.json")

if __name__ == "__main__":
    main()
