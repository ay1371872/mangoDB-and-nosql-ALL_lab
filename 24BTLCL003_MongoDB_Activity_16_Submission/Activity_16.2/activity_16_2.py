"""
Activity 16.2 - Hybrid Query Service (Catalog + Graph)

Demonstrates:
1. Coordinating cross-model queries in application code
2. Querying MongoDB for rich product catalog documents
3. Traversing relationship graphs for personalized recommendations
4. Aggregating hybrid query results into a unified response
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"

# MongoDB Document Catalog
CATALOG_ITEMS = [
    {"product_id": "P-101", "name": "Mechanical Keyboard", "price": 4500, "category": "Electronics", "in_stock": True},
    {"product_id": "P-102", "name": "Desk Mat XXL",         "price": 800,  "category": "Accessories", "in_stock": True},
    {"product_id": "P-103", "name": "Ergonomic Wrist Rest", "price": 600,  "category": "Accessories", "in_stock": True},
    {"product_id": "P-104", "name": "USB-C Fast Cable",     "price": 350,  "category": "Cables",      "in_stock": False},
]

# Graph Adjacency ("Frequently Bought Together")
GRAPH_EDGES = {
    "P-101": ["P-102", "P-103"],
    "P-102": ["P-103"],
    "P-103": ["P-104"]
}

def get_database():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        client.admin.command("ping")
        return client, client[DB_NAME]
    except Exception:
        import mongomock
        return mongomock.MongoClient(), mongomock.MongoClient()[DB_NAME]

def get_hybrid_recommendation(db, target_product_id):
    col = db["hybrid_catalog_graph"]
    # 1. Graph lookup for related product IDs
    related_ids = GRAPH_EDGES.get(target_product_id, [])
    # 2. MongoDB batch fetch for rich documents
    recommended_items = list(col.find({"product_id": {"$in": related_ids}, "in_stock": True}))
    return recommended_items

def main():
    print("=" * 60)
    print("ACTIVITY 16.2 - HYBRID QUERY SERVICE (CATALOG + GRAPH)")
    print("=" * 60)

    client, db = get_database()
    col = db["hybrid_catalog_graph"]
    col.drop()
    col.insert_many(CATALOG_ITEMS)
    print("[OK] Seeded MongoDB product catalog\n")

    target_sku = "P-101"
    target_doc = col.find_one({"product_id": target_sku})
    print(f"Viewing Product: {target_doc['name']} (Rs. {target_doc['price']})")

    # Execute hybrid query
    recs = get_hybrid_recommendation(db, target_sku)
    print("\n=== Hybrid Graph-Powered Recommendations (In-Stock Only) ===")
    for r in recs:
        print(f"  * Recommended: {r['name']:<22} | Category: {r['category']:<12} | Price: Rs. {r['price']}")

    with open("hybrid_16_2.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported hybrid dataset to hybrid_16_2.json")

if __name__ == "__main__":
    main()
