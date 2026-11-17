"""Activity 1.1 Try It Yourself - Classify ArangoDB, ScyllaDB and InfluxDB."""

import os
import textwrap
from pymongo import MongoClient
from bson.json_util import dumps

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "activity_1_1_try_it_yourself.json",
)

PRODUCTS = [
    {
        "product": "ArangoDB",
        "primary_family": "Document",
        "families": ["Document", "Graph", "Key-Value"],
        "fits_one_family": False,
        "reasoning": (
            "ArangoDB is a native multi-model database. JSON documents are "
            "its core storage, edges turn them into a graph that is "
            "queried with AQL traversals, and the same collections can be "
            "read by key like a key-value store."
        ),
    },
    {
        "product": "ScyllaDB",
        "primary_family": "Column-Family",
        "families": ["Column-Family"],
        "fits_one_family": True,
        "reasoning": (
            "ScyllaDB is a Cassandra-compatible wide-column store. Data is "
            "partitioned by key into rows with column families, tuned for "
            "very high write throughput and low latency."
        ),
    },
    {
        "product": "InfluxDB",
        "primary_family": "Time-Series (closest: Column-Family)",
        "families": ["Column-Family"],
        "fits_one_family": False,
        "reasoning": (
            "InfluxDB is built for timestamped measurements with tags and "
            "fields, stored column-wise. It is closest to column-family "
            "but is a specialised time-series model that does not fit "
            "neatly into the four classic families."
        ),
    },
]


def banner(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main():
    print("=" * 60)
    print("ACTIVITY 1.1 - TRY IT YOURSELF")
    print("=" * 60)

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    try:
        client.admin.command("ping")
        print("[OK] Connected to Docker MongoDB")

        db = client["nosql_activity_1"]
        if "classification_try_it_yourself" in db.list_collection_names():
            db["classification_try_it_yourself"].drop()
        collection = db["classification_try_it_yourself"]

        collection.insert_many(PRODUCTS)
        print(f"[OK] Inserted {collection.count_documents({})} products "
              "into nosql_activity_1.classification_try_it_yourself")

        documents = list(collection.find())

        banner("CLASSIFICATION")
        for doc in documents:
            print(f"\n{doc['product']}")
            print(f"  Primary family : {doc['primary_family']}")
            print(f"  Families       : {', '.join(doc['families'])}")
            verdict = "Yes" if doc["fits_one_family"] else "No"
            print(f"  Fits one family: {verdict}")
            print(textwrap.fill(
                doc["reasoning"], width=76,
                initial_indent="  Reasoning      : ",
                subsequent_indent=" " * 18,
            ))

        banner("CONCLUSION")
        single = collection.count_documents({"fits_one_family": True})
        multi = collection.count_documents({"fits_one_family": False})
        print(f"Fit neatly into one family : {single}")
        print(f"Span or sit outside families: {multi}")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(dumps(documents, indent=2))
        print(f"\n[OK] Exported collection to {os.path.basename(OUTPUT_FILE)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
