from pymongo import MongoClient
import re
import json

# ---------------------------------------------------------
# MongoDB Connection
# ---------------------------------------------------------

MONGO_URI = "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)

db = client["nosql_labs"]
collection = db["products_regex"]

# ---------------------------------------------------------
# Product Data
# ---------------------------------------------------------

products = [
    {
        "sku": "PROD-A",
        "title": "Wireless Headphones",
        "price": 49.99,
        "stock": 25,
        "tags": ["electronics", "wireless"],
        "image": "https://via.placeholder.com/150?text=Headphones"
    },
    {
        "sku": "PROD-B",
        "title": "Bluetooth Speaker",
        "price": 35.99,
        "stock": 40,
        "tags": ["electronics", "wireless", "audio"],
        "image": "https://via.placeholder.com/150?text=Speaker"
    },
    {
        "sku": "PROD-C",
        "title": "Mechanical Keyboard",
        "price": 89.99,
        "stock": 15,
        "tags": ["electronics", "mechanical"],
        "image": "https://via.placeholder.com/150?text=Keyboard"
    },
    {
        "sku": "PROD-D",
        "title": "Gaming Mouse",
        "price": 29.99,
        "stock": 0,
        "tags": ["electronics", "wireless"],
        "image": "https://via.placeholder.com/150?text=Mouse"
    },
    {
        "sku": "PROD-E",
        "title": "4K Monitor",
        "price": 299.99,
        "stock": 8,
        "tags": ["electronics", "premium"],
        "image": "https://via.placeholder.com/150?text=Monitor"
    },
    {
        "sku": "PROD-F",
        "title": "Gaming Laptop",
        "price": 1299.99,
        "stock": 5,
        "tags": ["electronics", "premium", "gaming"],
        "image": "https://via.placeholder.com/150?text=Laptop"
    },
    {
        "sku": "PROD-G",
        "title": "USB-C Hub",
        "price": 24.99,
        "stock": 60,
        "tags": ["electronics", "accessory"],
        "image": "https://via.placeholder.com/150?text=USB-Hub"
    },
    {
        "sku": "PROD-H",
        "title": "Smart Watch",
        "price": 199.99,
        "stock": 0,
        "tags": ["electronics", "wireless", "premium"],
        "image": "https://via.placeholder.com/150?text=Watch"
    },
    {
        "sku": "PROD-I",
        "title": "Laptop Stand",
        "price": 45.00,
        "stock": 20,
        "tags": ["office", "ergonomic"],
        "image": "https://via.placeholder.com/150?text=Stand"
    },
    {
        "sku": "PROD-J",
        "title": "Wireless Charger",
        "price": 39.99,
        "stock": 35,
        "tags": ["electronics", "wireless"],
        "image": "https://via.placeholder.com/150?text=Charger"
    },
    {
        "sku": "PROD-K",
        "title": "Premium Webcam",
        "price": 149.99,
        "stock": 12,
        "tags": ["electronics", "premium"],
        "image": "https://via.placeholder.com/150?text=Webcam"
    },
    {
        "sku": "PROD-L",
        "title": "Desk Lamp",
        "price": 19.99,
        "stock": 0,
        "tags": ["office", "lighting"],
        "image": "https://via.placeholder.com/150?text=Lamp"
    },
    {
    "sku": "PROD-M",
    "title": "Cotton Shirt",
    "price": 24.99,
    "stock": 30,
    "tags": ["clothing", "cotton"],
    "image": "https://via.placeholder.com/150?text=Cotton-Shirt"
    },
    {
    "sku": "PROD-N",
    "title": "Cotton T-Shirt",
    "price": 19.99,
    "stock": 50,
    "tags": ["clothing", "cotton"],
    "image": "https://via.placeholder.com/150?text=Cotton-TShirt"
    },
    {
    "sku": "PROD-O",
    "title": "Premium Cotton Pants",
    "price": 39.99,
    "stock": 20,
    "tags": ["clothing", "cotton"],
    "image": "https://via.placeholder.com/150?text=Cotton-Pants"
    }
]

# ---------------------------------------------------------
# Reset Collection
# ---------------------------------------------------------

collection.drop()

collection.insert_many(products)

print("=" * 65)
print("Activity 4.1 - Try It Yourself: Text Search with $regex")
print("=" * 65)

print(f"\nInserted {collection.count_documents({})} products.")

# ---------------------------------------------------------
# Create Index on title
# ---------------------------------------------------------

collection.create_index([("title", 1)])

print("\nIndex created on field: title")

# ---------------------------------------------------------
# Function for Safe Regex Search
# ---------------------------------------------------------

def search_products(term):
    """
    Performs case-insensitive regex search on product title.

    re.escape() protects user input from being interpreted
    as an unintended regular expression.
    """

    escaped_term = re.escape(term)

    filter_document = {
        "title": {
            "$regex": escaped_term,
            "$options": "i"
        }
    }

    print("\nFilter document:")
    print(json.dumps(filter_document, indent=2))

    results = list(
        collection.find(
            filter_document,
            {"_id": 0, "sku": 1, "title": 1, "price": 1}
        )
    )

    print(f"\nSearch term: {term}")
    print(f"Matches found: {len(results)}")

    for product in results:
        print(
            f"  {product['sku']} | "
            f"{product['title']} | "
            f"${product['price']}"
        )

    return filter_document, results


# ---------------------------------------------------------
# Required Regex Searches
# ---------------------------------------------------------

print("\n" + "-" * 65)
print("1. Case-insensitive regex search")
print("-" * 65)

search_products("wireless")

search_products("LAPTOP")

search_products("MONITOR")

# ---------------------------------------------------------
# Case-insensitivity Verification
# ---------------------------------------------------------

print("\n" + "-" * 65)
print("2. Case-insensitivity verification")
print("-" * 65)

_, lower_results = search_products("wireless")
_, upper_results = search_products("WIRELESS")

print(
    f"\nwireless matches: {len(lower_results)}"
)

print(
    f"WIRELESS matches: {len(upper_results)}"
)

if len(lower_results) == len(upper_results):
    print("[OK] Case-insensitive search verified.")
else:
    print("[ERROR] Case-insensitive search failed.")

# ---------------------------------------------------------
# re.escape() Demonstration
# ---------------------------------------------------------

print("\n" + "-" * 65)
print("3. re.escape() protection")
print("-" * 65)

unsafe_term = "(pack)"

escaped_term = re.escape(unsafe_term)

print(f"Original user input : {unsafe_term}")
print(f"Escaped search term : {escaped_term}")

filter_document = {
    "title": {
        "$regex": escaped_term,
        "$options": "i"
    }
}

print("\nSafe filter:")
print(json.dumps(filter_document, indent=2))

safe_results = list(
    collection.find(
        filter_document,
        {"_id": 0, "sku": 1, "title": 1}
    )
)

print(f"Matches found: {len(safe_results)}")
print("[OK] User input was safely escaped using re.escape().")

# ---------------------------------------------------------
# Explain Query Performance
# ---------------------------------------------------------

print("\n" + "-" * 65)
print("4. Regex query performance using explain()")
print("-" * 65)


def explain_regex(regex_pattern, options=None):

    filter_document = {
        "title": {
            "$regex": regex_pattern
        }
    }

    if options:
        filter_document["title"]["$options"] = options

    # Run explain with executionStats verbosity
    explanation = db.command(
        "explain",
        {
            "find": collection.name,
            "filter": filter_document,
            "hint": {"title": 1}
        },
        verbosity="executionStats"
    )

    execution_stats = explanation["executionStats"]

    print("\nRegex:", regex_pattern)

    if options:
        print("Options:", options)

    print(
        "Execution stage:",
        execution_stats.get("executionStages", {}).get("stage")
    )

    print(
        "Total keys examined:",
        execution_stats.get("totalKeysExamined")
    )

    print(
        "Total documents examined:",
        execution_stats.get("totalDocsExamined")
    )

    print(
        "Returned documents:",
        execution_stats.get("nReturned")
    )

    return execution_stats


# ---------------------------------------------------------
# Regex Comparison
# ---------------------------------------------------------

print("\nA. Case-insensitive substring search: /cotton/i")

stats_1 = explain_regex(
    "cotton",
    "i"
)

print("\nB. Case-sensitive anchored search: /^Cotton/")

stats_2 = explain_regex(
    "^Cotton"
)

print("\nC. Case-insensitive anchored search: /^Cotton/i")

stats_3 = explain_regex(
    "^Cotton",
    "i"
)

# ---------------------------------------------------------
# Explain Findings
# ---------------------------------------------------------

print("\n" + "-" * 65)
print("5. Explanation of index behavior")
print("-" * 65)

print("""
The execution plan may show a top-level FETCH stage even when
an IXSCAN is used underneath it. Therefore, the stage name alone
does not tell us how efficiently the index was used.

The important metric is totalKeysExamined.

For /cotton/i, MongoDB examined all 15 index keys because the
case-insensitive substring search cannot be converted into a
narrow index range.

For /^Cotton/, MongoDB examined only 3 index keys because the
case-sensitive anchored prefix can be converted into an index
range.

For /^Cotton/i, MongoDB again examined all 15 index keys because
the case-insensitive option prevents the same narrow prefix
range optimization.

Therefore, totalKeysExamined clearly demonstrates the difference
in index efficiency between these regex patterns.
""")

# ---------------------------------------------------------
# Final Status
# ---------------------------------------------------------

print("\n" + "=" * 65)
print("[OK] Activity 4.1 Try-It-Yourself completed successfully.")
print("=" * 65)

client.close()