"""
Activity 5.2 - Join Data with $lookup

Demonstrates:
1. $lookup across collections (Orders and Customers)
2. Left outer join pattern to find unpurchased products
3. Enriching order records with customer details
4. Projecting and flattening nested array fields
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"

CUSTOMERS = [
    {"customer_id": "CUST-1", "name": "Arjun Sharma", "tier": "Gold",   "city": "Delhi"},
    {"customer_id": "CUST-2", "name": "Sneha Patel",  "tier": "Silver", "city": "Mumbai"},
    {"customer_id": "CUST-3", "name": "Rahul Verma",  "tier": "Platinum","city": "Bengaluru"},
    {"customer_id": "CUST-4", "name": "Pooja Reddy",  "tier": "Bronze", "city": "Hyderabad"},
]

PRODUCTS = [
    {"product_id": "PROD-1", "name": "Mechanical Keyboard", "price": 4500, "category": "Electronics"},
    {"product_id": "PROD-2", "name": "Ergonomic Mouse",     "price": 1800, "category": "Electronics"},
    {"product_id": "PROD-3", "name": "USB-C Hub",           "price": 2200, "category": "Accessories"},
    {"product_id": "PROD-4", "name": "Monitor Stand",        "price": 1200, "category": "Accessories"},
    {"product_id": "PROD-5", "name": "Desk Mat",            "price": 800,  "category": "Accessories"},
]

ORDERS = [
    {"order_id": "ORD-201", "customer_id": "CUST-1", "product_ids": ["PROD-1", "PROD-2"], "total": 6300},
    {"order_id": "ORD-202", "customer_id": "CUST-2", "product_ids": ["PROD-2"],           "total": 1800},
    {"order_id": "ORD-203", "customer_id": "CUST-3", "product_ids": ["PROD-1", "PROD-3"], "total": 6700},
    {"order_id": "ORD-204", "customer_id": "CUST-1", "product_ids": ["PROD-3"],           "total": 2200},
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
    print("ACTIVITY 5.2 - RELATIONAL JOINS WITH $LOOKUP")
    print("=" * 60)

    client, db = get_database()
    c_cust = db["customers_join"]
    c_prod = db["products_join"]
    c_ord = db["orders_join"]

    for c in [c_cust, c_prod, c_ord]:
        c.drop()

    c_cust.insert_many(CUSTOMERS)
    c_prod.insert_many(PRODUCTS)
    c_ord.insert_many(ORDERS)
    print("[OK] Seeded customers, products, and orders collections\n")

    print("=== PIPELINE 1: Enriched Orders with Customer Details ===")
    p1 = [
        {"$lookup": {
            "from": "customers_join",
            "localField": "customer_id",
            "foreignField": "customer_id",
            "as": "customer"
        }},
        {"$unwind": "$customer"},
        {"$project": {
            "order_id": 1,
            "total": 1,
            "customer_name": "$customer.name",
            "tier": "$customer.tier",
            "city": "$customer.city",
            "items_count": {"$size": "$product_ids"},
            "_id": 0
        }}
    ]
    res1 = list(c_ord.aggregate(p1))
    print(f"{'Order ID':<10} {'Customer':<16} {'Tier':<10} {'City':<12} {'Total (Rs)':<10}")
    print("-" * 60)
    for r in res1:
        print(f"{r['order_id']:<10} {r['customer_name']:<16} {r['tier']:<10} {r['city']:<12} Rs. {r['total']}")

    print("\n=== PIPELINE 2: Unpurchased Products (Left Outer Join) ===")
    p2 = [
        {"$lookup": {
            "from": "orders_join",
            "localField": "product_id",
            "foreignField": "product_ids",
            "as": "orders"
        }},
        {"$match": {"orders": {"$size": 0}}},
        {"$project": {"_id": 0, "product_id": 1, "name": 1, "price": 1, "category": 1}}
    ]
    res2 = list(c_prod.aggregate(p2))
    print(f"{'Product ID':<12} {'Name':<20} {'Category':<15} {'Price'}")
    print("-" * 55)
    for r in res2:
        print(f"{r['product_id']:<12} {r['name']:<20} {r['category']:<15} Rs. {r['price']}")

    with open("orders_5_2.json", "w") as f:
        f.write(json.dumps(list(c_ord.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported orders join dataset to orders_5_2.json")

if __name__ == "__main__":
    main()
