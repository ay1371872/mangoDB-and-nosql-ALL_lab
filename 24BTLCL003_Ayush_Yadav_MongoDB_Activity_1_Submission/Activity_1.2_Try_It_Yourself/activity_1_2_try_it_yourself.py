"""Activity 1.2 Try It Yourself - E-commerce platform mapping."""

import os
import textwrap
from pymongo import MongoClient
from bson.json_util import dumps

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "activity_1_2_try_it_yourself.json",
)

MAPPINGS = [
    {
        "application": "E-commerce platform",
        "data_domain": "Product catalog",
        "nosql_family": "Document",
        "example_product": "MongoDB",
        "reasoning": (
            "Products have very different attributes: a phone has storage "
            "and RAM while a shirt has size and colour. A document model "
            "stores each product with its own nested fields, reviews and "
            "images, and the schema can change without migrations."
        ),
    },
    {
        "application": "E-commerce platform",
        "data_domain": "Shopping cart and sessions",
        "nosql_family": "Key-Value",
        "example_product": "Redis",
        "reasoning": (
            "A cart is read and written by session or user ID on every "
            "click and needs very low latency. Key-value lookups in memory "
            "are ideal, and built-in expiry removes abandoned sessions."
        ),
    },
    {
        "application": "E-commerce platform",
        "data_domain": "Order history and click-stream events",
        "nosql_family": "Column-Family",
        "example_product": "Cassandra",
        "reasoning": (
            "Orders and click events are append-only, arrive in huge "
            "volumes, and are queried by customer and time range. "
            "Partitioning by customer and clustering by time gives fast "
            "writes and efficient range reads at scale."
        ),
    },
    {
        "application": "E-commerce platform",
        "data_domain": "Recommendations",
        "nosql_family": "Graph",
        "example_product": "Neo4j",
        "reasoning": (
            "Suggestions like 'customers who bought this also bought' are "
            "multi-hop relationships between users, products and "
            "categories. A graph database traverses these links quickly "
            "without expensive joins."
        ),
    },
]


def banner(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main():
    print("=" * 60)
    print("ACTIVITY 1.2 - TRY IT YOURSELF")
    print("=" * 60)

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    try:
        client.admin.command("ping")
        print("[OK] Connected to Docker MongoDB")

        db = client["nosql_activity_1"]
        if "ecommerce_mapping" in db.list_collection_names():
            db["ecommerce_mapping"].drop()
        collection = db["ecommerce_mapping"]

        collection.insert_many(MAPPINGS)
        print(f"[OK] Inserted {collection.count_documents({})} mappings "
              "into nosql_activity_1.ecommerce_mapping")

        banner("E-COMMERCE PLATFORM MAPPING")
        for doc in collection.find():
            print(f"\n{doc['data_domain']}")
            print(f"  Family : {doc['nosql_family']} "
                  f"({doc['example_product']})")
            print(textwrap.fill(
                doc["reasoning"], width=76,
                initial_indent="  Reason : ", subsequent_indent=" " * 10,
            ))

        banner("DOMAINS PER FAMILY")
        for family in ["Key-Value", "Document", "Column-Family", "Graph"]:
            count = collection.count_documents({"nosql_family": family})
            print(f"{family:<15}: {count}")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(dumps(list(collection.find()), indent=2))
        print(f"\n[OK] Exported collection to {os.path.basename(OUTPUT_FILE)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
