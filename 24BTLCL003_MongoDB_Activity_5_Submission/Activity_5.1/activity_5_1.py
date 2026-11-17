"""
Activity 5.1 - Build a Sales Analytics Pipeline

Demonstrates:
1. Multi-stage aggregation pipelines
2. Monthly revenue calculation ($match, $group, $sort)
3. Top customers identification ($group, $sort, $limit)
4. Order size categorization ($project, $cond)
5. Exporting results to JSON
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "orders"

ORDERS = [
    {"order_id": "ORD-101", "customer": "Arjun", "status": "completed", "total": 2500.0, "items": 3, "month": "2024-01", "region": "North"},
    {"order_id": "ORD-102", "customer": "Sneha", "status": "completed", "total": 1800.0, "items": 1, "month": "2024-01", "region": "South"},
    {"order_id": "ORD-103", "customer": "Arjun", "status": "completed", "total": 3200.0, "items": 5, "month": "2024-02", "region": "North"},
    {"order_id": "ORD-104", "customer": "Kavya", "status": "cancelled", "total": 900.0,  "items": 2, "month": "2024-02", "region": "East"},
    {"order_id": "ORD-105", "customer": "Rahul", "status": "completed", "total": 5600.0, "items": 8, "month": "2024-02", "region": "West"},
    {"order_id": "ORD-106", "customer": "Arjun", "status": "completed", "total": 1200.0, "items": 2, "month": "2024-02", "region": "North"},
    {"order_id": "ORD-107", "customer": "Sneha", "status": "completed", "total": 4100.0, "items": 6, "month": "2024-03", "region": "South"},
    {"order_id": "ORD-108", "customer": "Kavya", "status": "completed", "total": 2900.0, "items": 4, "month": "2024-03", "region": "East"},
    {"order_id": "ORD-109", "customer": "Rahul", "status": "pending",   "total": 7800.0, "items": 10,"month": "2024-03", "region": "West"},
    {"order_id": "ORD-110", "customer": "Divya", "status": "completed", "total": 1500.0, "items": 1, "month": "2024-03", "region": "North"},
]

def get_database():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        client.admin.command("ping")
        print("[OK] Connected to MongoDB")
        return client, client[DB_NAME]
    except Exception:
        import mongomock
        print("[INFO] Live MongoDB offline. Running in-memory mock database.")
        client = mongomock.MongoClient()
        return client, client[DB_NAME]

def main():
    print("=" * 60)
    print("ACTIVITY 5.1 - SALES ANALYTICS PIPELINE")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(ORDERS)
    print(f"[OK] Seeded {len(ORDERS)} orders into collection '{COLLECTION_NAME}'\n")

    # Pipeline 1: Monthly Revenue
    print("=== PIPELINE 1: Monthly Revenue (Completed Orders) ===")
    p1 = [
        {"$match": {"status": "completed"}},
        {"$group": {
            "_id": "$month",
            "total_revenue": {"$sum": "$total"},
            "order_count": {"$sum": 1},
            "avg_order_value": {"$avg": "$total"},
            "customers": {"$addToSet": "$customer"}
        }},
        {"$sort": {"_id": 1}},
        {"$project": {
            "month": "$_id",
            "total_revenue": 1,
            "order_count": 1,
            "avg_order_value": 1,
            "unique_customers": {"$size": "$customers"},
            "_id": 0
        }}
    ]
    res1 = list(col.aggregate(p1))
    print(f"{'Month':<10} {'Revenue (Rs)':<15} {'Orders':<8} {'Avg Value':<12} {'Customers'}")
    print("-" * 55)
    for r in res1:
        print(f"{r['month']:<10} {r['total_revenue']:<15.2f} {r['order_count']:<8} {r['avg_order_value']:<12.2f} {r['unique_customers']}")

    # Pipeline 2: Top Customers by Spend
    print("\n=== PIPELINE 2: Top Customers by Total Spend ===")
    p2 = [
        {"$match": {"status": "completed"}},
        {"$group": {
            "_id": "$customer",
            "total_spent": {"$sum": "$total"},
            "completed_orders": {"$sum": 1}
        }},
        {"$sort": {"total_spent": -1}},
        {"$limit": 5}
    ]
    res2 = list(col.aggregate(p2))
    print(f"{'Customer':<12} {'Total Spent':<15} {'Completed Orders'}")
    print("-" * 45)
    for r in res2:
        print(f"{r['_id']:<12} Rs. {r['total_spent']:<12.2f} {r['completed_orders']}")

    # Pipeline 3: Order Size Categorization
    print("\n=== PIPELINE 3: Order Size Categorization ===")
    p3 = [
        {"$project": {
            "order_id": 1,
            "customer": 1,
            "total": 1,
            "tier": {
                "$cond": [
                    {"$gte": ["$total", 5000]}, "Large",
                    {"$cond": [{"$gte": ["$total", 2500]}, "Medium", "Small"]}
                ]
            }
        }},
        {"$group": {
            "_id": "$tier",
            "order_count": {"$sum": 1},
            "avg_total": {"$avg": "$total"}
        }},
        {"$sort": {"avg_total": -1}}
    ]
    res3 = list(col.aggregate(p3))
    print(f"{'Tier':<10} {'Order Count':<14} {'Avg Value'}")
    print("-" * 35)
    for r in res3:
        print(f"{r['_id']:<10} {r['order_count']:<14} Rs. {r['avg_total']:.2f}")

    # Export collection
    docs = list(col.find())
    with open("orders_5_1.json", "w") as f:
        f.write(json.dumps(docs, default=json_util.default, indent=2))
    print("\n[OK] Exported orders collection to orders_5_1.json")

if __name__ == "__main__":
    main()
