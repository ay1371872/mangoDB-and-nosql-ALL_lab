"""
Activity 5.1 - Try It Yourself

Objective: Build a multi-faceted sales analytics pipeline using the $facet
stage to compute regional distribution, monthly trends, and basket sizes
in a single aggregation execution.
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "orders_facet"

ORDERS = [
    {"order_id": "ORD-101", "customer": "Arjun", "region": "North", "total": 2500, "items": 3, "month": "2024-01"},
    {"order_id": "ORD-102", "customer": "Sneha", "region": "South", "total": 1800, "items": 1, "month": "2024-01"},
    {"order_id": "ORD-103", "customer": "Arjun", "region": "North", "total": 3200, "items": 5, "month": "2024-02"},
    {"order_id": "ORD-105", "customer": "Rahul", "region": "West",  "total": 5600, "items": 8, "month": "2024-02"},
    {"order_id": "ORD-106", "customer": "Arjun", "region": "North", "total": 1200, "items": 2, "month": "2024-02"},
    {"order_id": "ORD-107", "customer": "Sneha", "region": "South", "total": 4100, "items": 6, "month": "2024-03"},
    {"order_id": "ORD-108", "customer": "Kavya", "region": "East",  "total": 2900, "items": 4, "month": "2024-03"},
    {"order_id": "ORD-110", "customer": "Divya", "region": "North", "total": 1500, "items": 1, "month": "2024-03"},
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
    print("ACTIVITY 5.1 - TRY IT YOURSELF: $FACET MULTI-ANALYTICS")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(ORDERS)
    print(f"[OK] Seeded {len(ORDERS)} orders for facet analysis.\n")

    facet_pipeline = [
        {"$facet": {
            "by_region": [
                {"$group": {"_id": "$region", "revenue": {"$sum": "$total"}, "count": {"$sum": 1}}},
                {"$sort": {"revenue": -1}}
            ],
            "by_month": [
                {"$group": {"_id": "$month", "revenue": {"$sum": "$total"}, "avg_items": {"$avg": "$items"}}},
                {"$sort": {"_id": 1}}
            ],
            "basket_summary": [
                {"$group": {
                    "_id": None,
                    "total_revenue": {"$sum": "$total"},
                    "avg_order": {"$avg": "$total"},
                    "max_order": {"$max": "$total"},
                    "total_items": {"$sum": "$items"}
                }}
            ]
        }}
    ]

    res = list(col.aggregate(facet_pipeline))[0]
    
    print("=== 1. Regional Breakdown ===")
    for r in res["by_region"]:
        print(f"Region: {r['_id']:<8} Revenue: Rs. {r['revenue']:<10} Orders: {r['count']}")

    print("\n=== 2. Monthly Trend ===")
    for m in res["by_month"]:
        print(f"Month: {m['_id']:<10} Revenue: Rs. {m['revenue']:<10} Avg Items: {m['avg_items']:.1f}")

    print("\n=== 3. Overall Basket Summary ===")
    b = res["basket_summary"][0]
    print(f"Total Sales: Rs. {b['total_revenue']} | Avg Order: Rs. {b['avg_order']:.2f} | Max Order: Rs. {b['max_order']} | Total Items: {b['total_items']}")

    with open("orders_5_1_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported facet dataset to orders_5_1_try_it_yourself.json")

if __name__ == "__main__":
    main()
