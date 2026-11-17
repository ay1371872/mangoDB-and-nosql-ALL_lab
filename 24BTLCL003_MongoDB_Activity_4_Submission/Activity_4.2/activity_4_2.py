"""
Activity 4.2 - Implement Upsert and Bulk Operations

Demonstrates:
1. Upsert using update_one(upsert=True)
2. Conditional update/insert by SKU
3. Bulk operations using UpdateOne
4. Bulk write result verification
"""

from pymongo import MongoClient, UpdateOne


# ============================================================
# CONFIGURATION
# ============================================================

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "inventory"


# ============================================================
# INITIAL PRODUCTS
# ============================================================

PRODUCTS = [
    {
        "sku": "A",
        "name": "Wireless Headphones",
        "price": 49.99,
        "stock": 50,
        "is_active": True
    },
    {
        "sku": "B",
        "name": "Bluetooth Speaker",
        "price": 79.99,
        "stock": 40,
        "is_active": True
    },
    {
        "sku": "C",
        "name": "Mechanical Keyboard",
        "price": 89.99,
        "stock": 30,
        "is_active": True
    },
    {
        "sku": "D",
        "name": "Gaming Mouse",
        "price": 39.99,
        "stock": 25,
        "is_active": True
    },
    {
        "sku": "E",
        "name": "USB-C Hub",
        "price": 29.99,
        "stock": 60,
        "is_active": True
    }
]


# ============================================================
# UPSERT FUNCTION
# ============================================================

def upsert_product(col, sku, price):
    """
    Update the price if the SKU exists.
    Otherwise insert a new product with default values.
    """

    result = col.update_one(
        {"sku": sku},
        {
            "$set": {
                "price": price
            },
            "$setOnInsert": {
                "sku": sku,
                "name": "New Product",
                "stock": 0,
                "is_active": True
            }
        },
        upsert=True
    )

    if result.matched_count > 0:
        action = "UPDATED"
    else:
        action = "INSERTED"

    print(
        f"  [{action}] SKU={sku} | "
        f"matched={result.matched_count} | "
        f"modified={result.modified_count} | "
        f"upserted_id="
        f"{'YES' if result.upserted_id else 'NO'}"
    )

    return result


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 60)
    print("ACTIVITY 4.2 - UPSERT AND BULK OPERATIONS")
    print("=" * 60)

    # --------------------------------------------------------
    # CONNECT TO MONGODB
    # --------------------------------------------------------

    client = MongoClient(MONGO_URI)
    client.admin.command("ping")

    print("[OK] Connected to MongoDB")

    db = client[DB_NAME]

    # --------------------------------------------------------
    # RESET COLLECTION
    # --------------------------------------------------------

    if COLLECTION_NAME in db.list_collection_names():
        db.drop_collection(COLLECTION_NAME)

    inventory = db[COLLECTION_NAME]

    print("[OK] Created inventory collection")

    # --------------------------------------------------------
    # INSERT INITIAL PRODUCTS
    # --------------------------------------------------------

    print("\n=== INSERT: Initial Inventory ===")

    result = inventory.insert_many(PRODUCTS)

    print(f"[OK] Inserted {len(result.inserted_ids)} products")

    # --------------------------------------------------------
    # UPSERT: EXISTING SKU
    # --------------------------------------------------------

    print("\n=== UPSERT: Existing SKU A ===")

    upsert_product(
        inventory,
        "A",
        44.99
    )

    document = inventory.find_one(
        {"sku": "A"},
        {"_id": 0}
    )

    print(f"  Result: {document}")

    # --------------------------------------------------------
    # UPSERT: NEW SKU
    # --------------------------------------------------------

    print("\n=== UPSERT: New SKU F ===")

    upsert_product(
        inventory,
        "F",
        59.99
    )

    document = inventory.find_one(
        {"sku": "F"},
        {"_id": 0}
    )

    print(f"  Result: {document}")

    # --------------------------------------------------------
    # BULK WRITE
    # --------------------------------------------------------

    print("\n=== BULK WRITE: 5 UpdateOne Operations ===")

    operations = [

        # Product A: increase stock by 10
        UpdateOne(
            {"sku": "A"},
            {"$inc": {"stock": 10}}
        ),

        # Product B: increase stock by 10
        UpdateOne(
            {"sku": "B"},
            {"$inc": {"stock": 10}}
        ),

        # Product C: increase stock by 10
        UpdateOne(
            {"sku": "C"},
            {"$inc": {"stock": 10}}
        ),

        # Product D: deactivate
        UpdateOne(
            {"sku": "D"},
            {"$set": {"is_active": False}}
        ),

        # Product E: deactivate
        UpdateOne(
            {"sku": "E"},
            {"$set": {"is_active": False}}
        )
    ]

    bulk_result = inventory.bulk_write(
        operations
    )

    print(
        f"  Matched:   "
        f"{bulk_result.matched_count}"
    )

    print(
        f"  Modified:  "
        f"{bulk_result.modified_count}"
    )

    print(
        f"  Upserted:  "
        f"{bulk_result.upserted_count}"
    )

    print(
        f"  Upserted IDs: "
        f"{bulk_result.upserted_ids}"
    )

    # --------------------------------------------------------
    # VERIFY BULK OPERATIONS
    # --------------------------------------------------------

    print("\n=== VERIFYING BULK UPDATES ===")

    for sku in ["A", "B", "C", "D", "E"]:

        document = inventory.find_one(
            {"sku": sku},
            {"_id": 0}
        )

        if document is not None:
            print(
                f"  SKU={sku} | "
                f"stock={document['stock']} | "
                f"is_active={document['is_active']}"
            )
        else:
            print(f"  [ERROR] SKU={sku} was not found")

    # --------------------------------------------------------
    # FINAL INVENTORY
    # --------------------------------------------------------

    print("\n=== FINAL INVENTORY STATE ===")

    total = inventory.count_documents({})

    print(f"Total products: {total}")

    for document in inventory.find(
        {},
        {"_id": 0}
    ).sort("sku", 1):

        print(
            f"  {document['sku']:<5} "
            f"{document['name']:<25} "
            f"${document['price']:.2f} "
            f"stock={document['stock']:<4} "
            f"is_active={document['is_active']}"
        )

    print("\n=== BULK RESULT VERIFICATION ===")

    if (
        bulk_result.matched_count == 5
        and bulk_result.modified_count == 5
        and bulk_result.upserted_count == 0
    ):
        print(
            "[OK] Bulk write result verified successfully"
        )
    else:
        print(
            "[WARNING] Review the bulk write result"
        )

    print("\n[OK] Activity 4.2 completed successfully.")

    client.close()


if __name__ == "__main__":
    main()