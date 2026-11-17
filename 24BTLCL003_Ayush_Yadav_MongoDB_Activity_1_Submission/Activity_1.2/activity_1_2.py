"""Activity 1.2 - Map a real-world application to NoSQL families."""

import os
import textwrap
from pymongo import MongoClient
from bson.json_util import dumps

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "activity_1_2.json"
)

MAPPINGS = [
    # ---------------- Ride-sharing application ----------------
    {
        "application": "Ride-sharing app",
        "data_domain": "Driver locations",
        "nosql_family": "Key-Value",
        "example_product": "Redis",
        "justification": (
            "Locations are written very frequently and read by driver ID, "
            "with no complex querying needed, so fast key lookups win."
        ),
    },
    {
        "application": "Ride-sharing app",
        "data_domain": "User profiles",
        "nosql_family": "Document",
        "example_product": "MongoDB",
        "justification": (
            "Each profile is a self-contained unit with nested fields such "
            "as addresses, preferences and payment methods."
        ),
    },
    {
        "application": "Ride-sharing app",
        "data_domain": "Ride history",
        "nosql_family": "Column-Family",
        "example_product": "Cassandra",
        "justification": (
            "History is append-only and queried by rider ID and date "
            "range, which suits partition and clustering keys. A document "
            "database is an acceptable alternative."
        ),
    },
    {
        "application": "Ride-sharing app",
        "data_domain": "Driver-rider relationship graph",
        "nosql_family": "Graph",
        "example_product": "Neo4j",
        "justification": (
            "Efficient traversal of connections, referral networks and "
            "fraud patterns needs relationships as first-class data."
        ),
    },
    # ---------------- Social media analytics platform ----------------
    {
        "application": "Social media analytics",
        "data_domain": "Raw post storage",
        "nosql_family": "Column-Family",
        "example_product": "Cassandra",
        "justification": (
            "Millions of posts per day need very high write throughput, "
            "and access follows a time-series pattern."
        ),
    },
    {
        "application": "Social media analytics",
        "data_domain": "Real-time analytics layer",
        "nosql_family": "Key-Value",
        "example_product": "Redis",
        "justification": (
            "Counters and trending-topic caches need in-memory speed, "
            "backed by a column-family store for durable storage."
        ),
    },
]


def banner(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def show(docs):
    for doc in docs:
        print(f"\n{doc['data_domain']}")
        print(f"  Family  : {doc['nosql_family']} ({doc['example_product']})")
        print(textwrap.fill(
            doc["justification"], width=76,
            initial_indent="  Why     : ", subsequent_indent=" " * 12,
        ))


def main():
    print("=" * 60)
    print("ACTIVITY 1.2 - MAP APPLICATIONS TO NOSQL FAMILIES")
    print("=" * 60)

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    try:
        client.admin.command("ping")
        print("[OK] Connected to Docker MongoDB")

        db = client["nosql_activity_1"]
        if "application_mapping" in db.list_collection_names():
            db["application_mapping"].drop()
        collection = db["application_mapping"]

        collection.insert_many(MAPPINGS)
        print(f"[OK] Inserted {collection.count_documents({})} mappings "
              "into nosql_activity_1.application_mapping")

        banner("RIDE-SHARING APPLICATION")
        show(collection.find({"application": "Ride-sharing app"}))

        banner("SOCIAL MEDIA ANALYTICS PLATFORM")
        show(collection.find({"application": "Social media analytics"}))

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
