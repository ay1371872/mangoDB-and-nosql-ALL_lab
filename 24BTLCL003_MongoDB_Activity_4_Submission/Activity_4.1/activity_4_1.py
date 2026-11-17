"""
Lab 4.1 - Build a Product Query API

Demonstrates:
1. Schema validation
2. Product insertion
3. Comparison operators
4. Logical operators
5. Array operators
6. Pagination with sorting
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from pymongo.errors import CollectionInvalid


# ============================================================
# CONFIGURATION
# ============================================================

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "products"


# ============================================================
# SAMPLE PRODUCTS
# ============================================================

PRODUCTS = [
    {
        "sku": "PROD-A",
        "name": "Wireless Headphones",
        "price": 49.99,
        "stock": 25,
        "tags": ["electronics", "wireless"],
        "category": "Audio"
    },
    {
        "sku": "PROD-B",
        "name": "Bluetooth Speaker",
        "price": 35.99,
        "stock": 40,
        "tags": ["electronics", "wireless", "audio"],
        "category": "Audio"
    },
    {
        "sku": "PROD-C",
        "name": "Mechanical Keyboard",
        "price": 89.99,
        "stock": 15,
        "tags": ["electronics", "mechanical"],
        "category": "Keyboards"
    },
    {
        "sku": "PROD-D",
        "name": "Gaming Mouse",
        "price": 29.99,
        "stock": 0,
        "tags": ["electronics", "wireless"],
        "category": "Accessories"
    },
    {
        "sku": "PROD-E",
        "name": "4K Monitor",
        "price": 299.99,
        "stock": 8,
        "tags": ["electronics", "premium"],
        "category": "Monitors"
    },
    {
        "sku": "PROD-F",
        "name": "Gaming Laptop",
        "price": 1299.99,
        "stock": 5,
        "tags": ["electronics", "premium", "gaming"],
        "category": "Laptops"
    },
    {
        "sku": "PROD-G",
        "name": "USB-C Hub",
        "price": 24.99,
        "stock": 60,
        "tags": ["electronics", "accessory"],
        "category": "Accessories"
    },
    {
        "sku": "PROD-H",
        "name": "Smart Watch",
        "price": 199.99,
        "stock": 0,
        "tags": ["electronics", "wireless", "premium"],
        "category": "Wearables"
    },
    {
        "sku": "PROD-I",
        "name": "Laptop Stand",
        "price": 45.00,
        "stock": 20,
        "tags": ["office", "ergonomic"],
        "category": "Office"
    },
    {
        "sku": "PROD-J",
        "name": "Wireless Charger",
        "price": 39.99,
        "stock": 35,
        "tags": ["electronics", "wireless"],
        "category": "Accessories"
    },
    {
        "sku": "PROD-K",
        "name": "Premium Webcam",
        "price": 149.99,
        "stock": 12,
        "tags": ["electronics", "premium"],
        "category": "Cameras"
    },
    {
        "sku": "PROD-L",
        "name": "Desk Lamp",
        "price": 19.99,
        "stock": 0,
        "tags": ["office", "lighting"],
        "category": "Office"
    }
]


# ============================================================
# DATABASE SETUP
# ============================================================

def get_database():
    """Connect to MongoDB."""
    client = MongoClient(MONGO_URI)
    client.admin.command("ping")
    print("[OK] Connected to MongoDB")
    return client, client[DB_NAME]


def create_validated_collection(db):
    """Create products collection with JSON Schema validation."""

    if COLLECTION_NAME in db.list_collection_names():
        db.drop_collection(COLLECTION_NAME)

    validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "price", "stock", "tags"],
            "properties": {
                "name": {
                    "bsonType": "string"
                },
                "price": {
                    "bsonType": ["int", "long", "double", "decimal"],
                    "minimum": 0.01
                },
                "stock": {
                    "bsonType": "int",
                    "minimum": 0
                },
                "tags": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "string"
                    }
                }
            }
        }
    }

    try:
        db.create_collection(
            COLLECTION_NAME,
            validator=validator,
            validationLevel="strict",
            validationAction="error"
        )
    except CollectionInvalid:
        pass

    print("[OK] Created products collection")
    print("[OK] JSON Schema validation enabled")

    return db[COLLECTION_NAME]


# ============================================================
# PAGINATION FUNCTION
# ============================================================

def get_products_page(col, page_number, items_per_page):
    """
    Return one page of products sorted by name.
    """

    if page_number < 1:
        raise ValueError("Page number must be at least 1.")

    if items_per_page < 1:
        raise ValueError("Items per page must be at least 1.")

    skip = (page_number - 1) * items_per_page

    results = list(
        col.find(
            {},
            {
                "_id": 0,
                "sku": 1,
                "name": 1,
                "price": 1,
                "stock": 1
            }
        )
        .sort("name", 1)
        .skip(skip)
        .limit(items_per_page)
    )

    total = col.count_documents({})

    return results, total


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 60)
    print("ACTIVITY 4.1 - BUILD A PRODUCT QUERY API")
    print("=" * 60)

    client, db = get_database()
    products = create_validated_collection(db)

    # --------------------------------------------------------
    # INSERT PRODUCTS
    # --------------------------------------------------------

    print("\n=== INSERT: Product Documents ===")

    result = products.insert_many(PRODUCTS)

    print(f"[OK] Inserted {len(result.inserted_ids)} products")

    # --------------------------------------------------------
    # COMPARISON OPERATORS
    # --------------------------------------------------------

    print("\n=== COMPARISON: Price between $20 and $50 ===")

    results = products.find(
        {
            "price": {
                "$gte": 20,
                "$lte": 50
            }
        },
        {
            "_id": 0,
            "name": 1,
            "price": 1
        }
    ).sort("price", 1)

    for product in results:
        print(
            f"  {product['name']:<25} "
            f"${product['price']:.2f}"
        )

    print("\n=== COMPARISON: Out of Stock ===")

    results = products.find(
        {"stock": {"$eq": 0}},
        {
            "_id": 0,
            "name": 1,
            "stock": 1
        }
    ).sort("name", 1)

    for product in results:
        print(
            f"  {product['name']:<25} "
            f"stock={product['stock']}"
        )

    # --------------------------------------------------------
    # LOGICAL OPERATORS
    # --------------------------------------------------------

    print("\n=== LOGICAL: Out of Stock OR Price above $100 ===")

    results = products.find(
        {
            "$or": [
                {"stock": 0},
                {"price": {"$gt": 100}}
            ]
        },
        {
            "_id": 0,
            "name": 1,
            "price": 1,
            "stock": 1
        }
    ).sort("name", 1)

    for product in results:
        print(
            f"  {product['name']:<25} "
            f"${product['price']:.2f} "
            f"stock={product['stock']}"
        )

    print("\n=== LOGICAL: In Stock AND tagged 'premium' ===")

    results = products.find(
        {
            "$and": [
                {"stock": {"$gt": 0}},
                {"tags": "premium"}
            ]
        },
        {
            "_id": 0,
            "name": 1,
            "stock": 1,
            "tags": 1
        }
    ).sort("name", 1)

    for product in results:
        print(
            f"  {product['name']:<25} "
            f"stock={product['stock']} "
            f"tags={product['tags']}"
        )

    # --------------------------------------------------------
    # ARRAY OPERATORS
    # --------------------------------------------------------

    print("\n=== ARRAY: BOTH 'electronics' AND 'wireless' ===")

    results = products.find(
        {
            "tags": {
                "$all": [
                    "electronics",
                    "wireless"
                ]
            }
        },
        {
            "_id": 0,
            "name": 1,
            "tags": 1
        }
    ).sort("name", 1)

    for product in results:
        print(
            f"  {product['name']:<25} "
            f"{product['tags']}"
        )

    print("\n=== ARRAY: Exactly 2 Tags ===")

    results = products.find(
        {
            "tags": {
                "$size": 2
            }
        },
        {
            "_id": 0,
            "name": 1,
            "tags": 1
        }
    ).sort("name", 1)

    for product in results:
        print(
            f"  {product['name']:<25} "
            f"{product['tags']}"
        )

    # --------------------------------------------------------
    # PAGINATION
    # --------------------------------------------------------

    page_number = 1
    items_per_page = 5

    print(
        f"\n=== PAGINATION: Page {page_number}, "
        f"{items_per_page} items per page ==="
    )

    page_results, total = get_products_page(
        products,
        page_number,
        items_per_page
    )

    for product in page_results:
        print(
            f"  {product['name']:<25} "
            f"${product['price']:.2f} "
            f"stock={product['stock']}"
        )

    print(
        f"  Showing {len(page_results)} "
        f"of {total} products"
    )

    # --------------------------------------------------------
    # SECOND PAGE
    # --------------------------------------------------------

    page_number = 2

    print(
        f"\n=== PAGINATION: Page {page_number}, "
        f"{items_per_page} items per page ==="
    )

    page_results, total = get_products_page(
        products,
        page_number,
        items_per_page
    )

    for product in page_results:
        print(
            f"  {product['name']:<25} "
            f"${product['price']:.2f} "
            f"stock={product['stock']}"
        )

    print(
        f"  Showing {len(page_results)} "
        f"of {total} products"
    )

    # --------------------------------------------------------
    # FINAL STATE
    # --------------------------------------------------------

    print("\n=== FINAL COLLECTION STATE ===")

    count = products.count_documents({})

    print(f"Total products: {count}")

    for product in products.find(
        {},
        {
            "_id": 0,
            "sku": 1,
            "name": 1,
            "price": 1,
            "stock": 1
        }
    ).sort("name", 1):

        print(
            f"  {product['sku']:<10} "
            f"{product['name']:<25} "
            f"${product['price']:.2f} "
            f"stock={product['stock']}"
        )

    print("\n[OK] Activity 4.1 completed successfully.")

    client.close()


if __name__ == "__main__":
    main()