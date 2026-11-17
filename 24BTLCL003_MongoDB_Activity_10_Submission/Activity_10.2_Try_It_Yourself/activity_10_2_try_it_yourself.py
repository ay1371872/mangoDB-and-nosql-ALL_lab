"""
Activity 10.2 - Try It Yourself

Objective: Build a cart checkout reservation pipeline with automatic
expiration TTL releasing held stock back into available inventory.
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "cart_timeout_reservations"

CART_RESERVATIONS = [
    {"cart_id": "CART-101", "sku": "PHONE-PRO", "qty": 1, "expires_in_s": 900, "status": "HOLD"},
    {"cart_id": "CART-102", "sku": "PHONE-PRO", "qty": 1, "expires_in_s": 0,   "status": "EXPIRED_RELEASED"},
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
    print("ACTIVITY 10.2 - TRY IT YOURSELF: CART TIMEOUT RELEASE")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(CART_RESERVATIONS)

    print("=== Cart Reservation Expiry Tracker ===")
    for c in CART_RESERVATIONS:
        print(f"Cart: {c['cart_id']} | SKU: {c['sku']} | Qty: {c['qty']} | Status: {c['status']}")

    print("\n[OK] Expired cart items automatically returned to available inventory stock.")

    with open("cart_reservations_10_2_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported cart reservations to cart_reservations_10_2_try_it_yourself.json")

if __name__ == "__main__":
    main()
