"""Activity 1.1 - Classify Database Products into NoSQL families."""

import os
import textwrap
from pymongo import MongoClient
from bson.json_util import dumps

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "activity_1_1.json"
)

PRODUCTS = [
    {
        "product": "Amazon S3",
        "family": "Key-Value",
        "reasoning": (
            "Objects are stored and fetched by a unique object key, and "
            "there is no way to query inside the object's contents."
        ),
        "use_case": "Storing and serving user-uploaded photos and videos "
                    "for a media-sharing website.",
        "why_best": "Access is always by key, objects are large and opaque, "
                    "and S3 gives near-unlimited size with high durability.",
        "best_for": "Large binary objects, backups, static assets",
        "limitation": "No queries or indexes on object contents",
    },
    {
        "product": "Couchbase",
        "family": "Document",
        "reasoning": (
            "It stores JSON documents and supports secondary indexes and "
            "SQL-like (N1QL) queries on document fields."
        ),
        "use_case": "Product catalog and user-profile store for an "
                    "e-commerce site.",
        "why_best": "Each product or profile is a self-contained JSON "
                    "document, the schema evolves often, and a built-in "
                    "cache keeps reads fast.",
        "best_for": "Flexible JSON data with low-latency access",
        "limitation": "Complex joins and deep relationship queries are weak",
    },
    {
        "product": "Apache HBase",
        "family": "Column-Family",
        "reasoning": (
            "Data is organised into column families inside wide, sparse "
            "rows that can hold millions of columns."
        ),
        "use_case": "Storing billions of time-stamped sensor readings "
                    "from IoT devices.",
        "why_best": "Writes are very heavy, rows are sparse, and reads are "
                    "mostly row-key range scans which HBase handles well.",
        "best_for": "Massive, write-heavy, sparse, time-series data",
        "limitation": "Efficient only for row-key access; no rich queries",
    },
    {
        "product": "Amazon Neptune",
        "family": "Graph",
        "reasoning": (
            "It is purpose-built to store and query property-graph and RDF "
            "data using Gremlin, openCypher and SPARQL."
        ),
        "use_case": "Fraud detection by traversing links between accounts, "
                    "devices and addresses.",
        "why_best": "Finding fraud rings needs multi-hop traversals that "
                    "would need many expensive joins in other families.",
        "best_for": "Highly connected data and relationship traversal",
        "limitation": "Single writer node limits write scaling",
    },
    {
        "product": "Memcached",
        "family": "Key-Value",
        "reasoning": (
            "It maps string keys to opaque byte values held in memory, "
            "with no query capability at all."
        ),
        "use_case": "Caching rendered web pages and database query results "
                    "for a high-traffic website.",
        "why_best": "Pure in-memory key lookups give sub-millisecond "
                    "latency and take load off the main database.",
        "best_for": "Ultra-fast, volatile caching",
        "limitation": "No persistence, replication or querying",
    },
]


def banner(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def wrap(label, text):
    return textwrap.fill(
        text, width=76, initial_indent=f"  {label:<10}: ",
        subsequent_indent=" " * 14,
    )


def print_table(rows):
    widths = [16, 14, 34, 36]
    heads = ["Product", "Family", "Best For", "Limitation"]
    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(line)
    print("| " + " | ".join(h.ljust(w) for h, w in zip(heads, widths)) + " |")
    print(line)
    for r in rows:
        cells = [r["product"], r["family"], r["best_for"], r["limitation"]]
        wrapped = [textwrap.wrap(c, w) for c, w in zip(cells, widths)]
        for i in range(max(len(c) for c in wrapped)):
            parts = [(c[i] if i < len(c) else "").ljust(w)
                     for c, w in zip(wrapped, widths)]
            print("| " + " | ".join(parts) + " |")
        print(line)


def main():
    print("=" * 60)
    print("ACTIVITY 1.1 - CLASSIFY DATABASE PRODUCTS")
    print("=" * 60)

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    try:
        client.admin.command("ping")
        print("[OK] Connected to Docker MongoDB")

        db = client["nosql_activity_1"]
        if "product_classification" in db.list_collection_names():
            db["product_classification"].drop()
        collection = db["product_classification"]

        collection.insert_many(PRODUCTS)
        print(f"[OK] Inserted {collection.count_documents({})} products "
              "into nosql_activity_1.product_classification")

        documents = list(collection.find())

        banner("CLASSIFICATION AND REASONING")
        for doc in documents:
            print(f"\n{doc['product']}")
            print(wrap("Family", doc["family"]))
            print(wrap("Reason", doc["reasoning"]))
            print(wrap("Use case", doc["use_case"]))
            print(wrap("Why best", doc["why_best"]))

        banner("COMPARISON TABLE")
        print_table(documents)

        banner("PRODUCTS PER FAMILY")
        for family in ["Key-Value", "Document", "Column-Family", "Graph"]:
            count = collection.count_documents({"family": family})
            print(f"{family:<15}: {count}")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(dumps(documents, indent=2))
        print(f"\n[OK] Exported collection to {os.path.basename(OUTPUT_FILE)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
