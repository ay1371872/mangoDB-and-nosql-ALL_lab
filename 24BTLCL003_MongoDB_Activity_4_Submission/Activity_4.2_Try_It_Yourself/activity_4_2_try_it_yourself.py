"""
Activity 4.2 - Try It Yourself

Idempotent bulk import using upsert logic.

The same import can be executed multiple times without
creating duplicate products.

SKU is used as the unique product identifier.
$set is used because setting the same values repeatedly
does not change the document.
"""

from pymongo import MongoClient, UpdateOne


# ============================================================
# CONFIGURATION
# ============================================================

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "idempotent_import"


# ============================================================
# IMPORT DATA
# ============================================================

IMPORT_PRODUCTS = [
    {
        "sku": "IMP-001",
        "name": "Smartphone X",
        "price": 699.99,
        "stock": 50,
        "category": "Electronics",
        "is_active": True
    },
    {
        "sku": "IMP-002",
        "name": "Wireless Earbuds",
        "price": 89.99,
        "stock": 100,
        "category": "Audio",
        "is_active": True
    },
    {
        "sku": "IMP-003",
        "name": "Gaming Keyboard",
        "price": 129.99,
        "stock": 40,
        "category": "Accessories",
        "is_active": True
    },
    {
        "sku": "IMP-004",
        "name": "Smart Monitor",
        "price": 349.99,
        "stock": 25,
        "category": "Monitors",
        "is_active": True
    },
    {
        "sku": "IMP-005",
        "name": "USB-C Charger",
        "price": 39.99,
        "stock": 150,
        "category": "Accessories",
        "is_active": True
    }
]


# ============================================================
# IDEMPOTENT BULK IMPORT FUNCTION
# ============================================================

def idempotent_bulk_import(col, products):
    """
    Import products using UpdateOne with upsert=True.

    If the SKU already exists:
        update the existing document.

    If the SKU does not exist:
        insert a new document.

    $set makes the operation idempotent because running
    the same import again sets the same values.
    """

    operations = []

    for product in products:

        operations.append(
            UpdateOne(
                {"sku": product["sku"]},
                {
                    "$set": product
                },
                upsert=True
            )
        )

    result = col.bulk_write(
        operations,
        ordered=True
    )

    return result


# ============================================================
# PRINT BULK RESULT
# ============================================================

def print_bulk_result(result):

    print(f"  Matched:      {result.matched_count}")
    print(f"  Modified:     {result.modified_count}")
    print(f"  Upserted:     {result.upserted_count}")
    print(f"  Upserted IDs: {result.upserted_ids}")


# ============================================================
# PRINT COLLECTION
# ============================================================

def print_inventory(col):

    print("\n=== CURRENT IMPORTED PRODUCTS ===")

    for product in col.find(
        {},
        {"_id": 0}
    ).sort("sku", 1):

        print(
            f"  {product['sku']:<10} "
            f"{product['name']:<22} "
            f"${product['price']:<8.2f} "
            f"stock={product['stock']:<3} "
            f"active={product['is_active']}"
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 60)
    print("ACTIVITY 4.2 - TRY IT YOURSELF")
    print("IDEMPOTENT BULK IMPORT USING UPSERT")
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

    products = db[COLLECTION_NAME]

    # Unique SKU index
    products.create_index(
        "sku",
        unique=True
    )

    print("[OK] Created idempotent_import collection")
    print("[OK] Unique index created on SKU")

    # --------------------------------------------------------
    # FIRST IMPORT
    # --------------------------------------------------------

    print("\n=== FIRST BULK IMPORT ===")

    result1 = idempotent_bulk_import(
        products,
        IMPORT_PRODUCTS
    )

    print_bulk_result(result1)

    print_inventory(products)

    # --------------------------------------------------------
    # SECOND IMPORT
    # --------------------------------------------------------

    print("\n=== SECOND BULK IMPORT ===")
    print("Running the exact same import again...")

    result2 = idempotent_bulk_import(
        products,
        IMPORT_PRODUCTS
    )

    print_bulk_result(result2)

    print_inventory(products)

    # --------------------------------------------------------
    # VERIFY IDEMPOTENCY
    # --------------------------------------------------------

    print("\n=== IDEMPOTENCY VERIFICATION ===")

    total_products = products.count_documents({})

    print(
        f"  Products after first import : "
        f"{result1.upserted_count}"
    )

    print(
        f"  Products after second import: "
        f"{total_products}"
    )

    print(
        f"  Second import upserted      : "
        f"{result2.upserted_count}"
    )

    print(
        f"  Second import modified      : "
        f"{result2.modified_count}"
    )

    if (
        total_products == len(IMPORT_PRODUCTS)
        and result1.upserted_count == len(IMPORT_PRODUCTS)
        and result2.upserted_count == 0
        and result2.modified_count == 0
    ):
        print(
            "\n[OK] Import is idempotent."
        )

        print(
            "[OK] Running the same import again "
            "does not create duplicates."
        )

    else:
        print(
            "\n[ERROR] Idempotency verification failed."
        )

    # --------------------------------------------------------
    # FINAL DATABASE STATE
    # --------------------------------------------------------

    print("\n=== FINAL DATABASE STATE ===")

    print(
        f"Total documents: "
        f"{products.count_documents({})}"
    )

    print(
        f"Unique SKUs: "
        f"{len(products.distinct('sku'))}"
    )

    if (
        products.count_documents({})
        == len(products.distinct("sku"))
    ):
        print(
            "[OK] No duplicate SKUs found."
        )

    print(
        "\n[OK] Activity 4.2 Try-It-Yourself "
        "completed successfully."
    )

    client.close()


if __name__ == "__main__":
    main()