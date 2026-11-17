"""Activity 2.1 - Compare Docker and MongoDB Atlas server information."""

import os
from datetime import datetime
from pymongo import MongoClient


DOCKER_URI = "mongodb://localhost:27017"
ATLAS_URI = os.getenv("MONGO_ATLAS_URI")


def get_server_info(name, uri):
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    client = MongoClient(
        uri,
        serverSelectionTimeoutMS=5000
    )

    try:
        client.admin.command("ping")
        print("[OK] Connection successful!")

        info = client.server_info()

        print(f"MongoDB Version : {info['version']}")
        print(f"Git Version     : {info.get('gitVersion', 'N/A')}")

        return info

    finally:
        client.close()


def save_result(uri, collection_name, document):
    client = MongoClient(
        uri,
        serverSelectionTimeoutMS=5000
    )

    try:
        db = client["mongodb_activity_2"]
        collection = db[collection_name]

        collection.delete_many({})
        collection.insert_one(document)

    finally:
        client.close()


def main():

    print("=" * 60)
    print("ACTIVITY 2.1 - SERVER VERSION COMPARISON")
    print("=" * 60)

    if not ATLAS_URI:
        print("[ERROR] MONGO_ATLAS_URI is not configured.")
        return

    docker_info = get_server_info(
        "DOCKER MONGODB",
        DOCKER_URI
    )

    atlas_info = get_server_info(
        "MONGODB ATLAS",
        ATLAS_URI
    )

    print("\n" + "=" * 60)
    print("VERSION COMPARISON")
    print("=" * 60)

    print(f"Docker MongoDB : {docker_info['version']}")
    print(f"MongoDB Atlas  : {atlas_info['version']}")

    same_version = (
        docker_info["version"] ==
        atlas_info["version"]
    )

    if same_version:
        print("Result: Both servers have the same MongoDB version.")
    else:
        print("Result: The servers have different MongoDB versions.")

    # Store Docker server information in Docker MongoDB
    docker_document = {
        "activity": "2.1",
        "server": "Docker MongoDB",
        "version": docker_info["version"],
        "gitVersion": docker_info.get("gitVersion"),
        "platform": docker_info.get("platform"),
        "pid": docker_info.get("pid"),
        "recordedAt": datetime.now().isoformat()
    }

    save_result(
        DOCKER_URI,
        "activity_2_1_docker",
        docker_document
    )

    # Store Atlas server information in Atlas MongoDB
    atlas_document = {
        "activity": "2.1",
        "server": "MongoDB Atlas",
        "version": atlas_info["version"],
        "gitVersion": atlas_info.get("gitVersion"),
        "platform": atlas_info.get("platform"),
        "pid": atlas_info.get("pid"),
        "recordedAt": datetime.now().isoformat()
    }

    save_result(
        ATLAS_URI,
        "activity_2_1_atlas",
        atlas_document
    )

    print("\n[OK] Docker result saved to:")
    print("     mongodb_activity_2.activity_2_1_docker")

    print("[OK] Atlas result saved to:")
    print("     mongodb_activity_2.activity_2_1_atlas")


if __name__ == "__main__":
    main()