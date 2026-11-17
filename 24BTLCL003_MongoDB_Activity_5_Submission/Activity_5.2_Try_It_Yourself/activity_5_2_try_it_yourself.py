"""
Activity 5.2 - Try It Yourself

Objective: Implement a multi-hop aggregation join that links Customers,
Orders, and Products collections to report total expenditure and top product
category purchased per customer tier.
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"

CUSTOMERS = [
    {"customer_id": "CUST-1", "name": "Arjun Sharma", "tier": "Gold"},
    {"customer_id": "CUST-2", "name": "Sneha Patel",  "tier": "Silver"},
    {"customer_id": "CUST-3", "name": "Rahul Verma",  "tier": "Platinum"},
]

ORDERS = [
    {"order_id": "ORD-1", "customer_id": "CUST-1", "product_id": "PROD-1", "qty": 2, "amount": 9000},
    {"order_id": "ORD-2", "customer_id": "CUST-1", "product_id": "PROD-3", "qty": 1, "amount": 2200},
    {"order_id": "ORD-3", "customer_id": "CUST-2", "product_id": "PROD-2", "qty": 1, "amount": 1800},
    {"order_id": "ORD-4", "customer_id": "CUST-3", "product_id": "PROD-1", "qty": 1, "amount": 4500},
    {"order_id": "ORD-5", "customer_id": "CUST-3", "product_id": "PROD-3", "qty": 3, "amount": 6600},
]

PRODUCTS = [
    {"product_id": "PROD-1", "name": "Mechanical Keyboard", "category": "Electronics"},
    {"product_id": "PROD-2", "name": "Ergonomic Mouse",     "category": "Electronics"},
    {"product_id": "PROD-3", "name": "USB-C Hub",           "category": "Accessories"},
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
    print("ACTIVITY 5.2 - TRY IT YOURSELF: MULTI-COLLECTION JOIN")
    print("=" * 60)

    client, db = get_database()
    col_cust = db["cust_multi"]
    col_ord = db["ord_multi"]
    col_prod = db["prod_multi"]

    for c in [col_cust, col_ord, col_prod]:
        c.drop()

    col_cust.insert_many(CUSTOMERS)
    col_ord.insert_many(ORDERS)
    col_prod.insert_many(PRODUCTS)
    print("[OK] Loaded customer, order, and product collections\n")

    pipeline = [
        {"$lookup": {
            "from": "cust_multi",
            "localField": "customer_id",
            "foreignField": "customer_id",
            "as": "customer"
        }},
        {"$unwind": "$customer"},
        {"$lookup": {
            "from": "prod_multi",
            "localField": "product_id",
            "foreignField": "product_id",
            "as": "product"
        }},
        {"$unwind": "$product"},
        {"$group": {
            "_id": {
                "tier": "$customer.tier",
                "customer": "$customer.name",
                "category": "$product.category"
            },
            "total_spend": {"$sum": "$amount"},
            "total_qty": {"$sum": "$qty"}
        }},
        {"$sort": {"total_spend": -1}},
        {"$project": {
            "_id": 0,
            "tier": "$_id.tier",
            "customer": "$_id.customer",
            "category": "$_id.category",
            "total_spend": 1,
            "total_qty": 1
        }}
    ]

    res = list(col_ord.aggregate(pipeline))
    print(f"{'Tier':<10} {'Customer':<16} {'Category':<15} {'Qty':<6} {'Total Spend'}")
    print("-" * 60)
    for r in res:
        print(f"{r['tier']:<10} {r['customer']:<16} {r['category']:<15} {r['total_qty']:<6} Rs. {r['total_spend']}")

    with open("orders_5_2_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col_ord.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported multi-hop dataset to orders_5_2_try_it_yourself.json")

if __name__ == "__main__":
    main()
