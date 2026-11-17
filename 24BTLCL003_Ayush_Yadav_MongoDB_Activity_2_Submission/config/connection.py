"""MongoDB connection utilities for Activity 2."""

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)


def get_client():
    """Create a MongoDB client."""
    return MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000
    )


def get_db(database_name):
    """Return a MongoDB database."""
    client = get_client()
    client.admin.command("ping")
    return client[database_name]


def reset_collection(database_name, collection_name):
    """Drop the existing collection and return a fresh collection."""
    client = get_client()

    try:
        client.admin.command("ping")

        db = client[database_name]

        if collection_name in db.list_collection_names():
            db[collection_name].drop()
            print(
                f"[OK] Reset collection: "
                f"{database_name}.{collection_name}"
            )

        return db[collection_name]

    except ConnectionFailure as e:
        print(f"[ERROR] Could not connect to MongoDB: {e}")
        raise


def banner(title):
    """Print a formatted banner."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_json(document):
    """Pretty-print a MongoDB document."""
    from pprint import pprint
    pprint(document)