"""
Activity 2.1 - Try It Yourself

Connect to both Docker MongoDB and MongoDB Atlas,
retrieve server information using server_info(),
compare their versions, and store the results
in MongoDB collections so they can be exported
as JSON using MongoDB Compass.
"""

import os
from datetime import datetime
from pymongo import MongoClient


# ---------------------------------------------------------
# CONNECTION STRINGS
# ---------------------------------------------------------

DOCKER_URI = "mongodb://localhost:27017"
ATLAS_URI = os.getenv("MONGO_ATLAS_URI")


# ---------------------------------------------------------
# GET SERVER INFORMATION
# ---------------------------------------------------------

def get_server_info(server_name, uri):

    print("\n" + "=" * 60)
    print(server_name)
    print("=" * 60)

    client = MongoClient(
        uri,
        serverSelectionTimeoutMS=5000
    )

    try:
        # Test connection
        client.admin.command("ping")

        print("[OK] Connection successful!")

        # Get MongoDB server information
        info = client.server_info()

        print(f"MongoDB Version : {info['version']}")
        print(f"Git Version     : {info.get('gitVersion', 'N/A')}")

        return info

    finally:
        client.close()


# ---------------------------------------------------------
# SAVE RESULTS TO MONGODB
# ---------------------------------------------------------

def save_result(uri, collection_name, document):

    client = MongoClient(
        uri,
        serverSelectionTimeoutMS=5000
    )

    try:

        db = client["mongodb_activity_2"]

        collection = db[collection_name]

        # Clear previous result so every run is clean
        collection.delete_many({})

        collection.insert_one(document)

    finally:
        client.close()


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("ACTIVITY 2.1 - TRY IT YOURSELF")
    print("=" * 60)

    # Check Atlas environment variable
    if not ATLAS_URI:

        print("\n[ERROR] MONGO_ATLAS_URI is not configured.")

        print(
            "Set the Atlas URI in PowerShell before running "
            "this script."
        )

        return

    # -----------------------------------------------------
    # DOCKER
    # -----------------------------------------------------

    docker_info = get_server_info(
        "DOCKER MONGODB",
        DOCKER_URI
    )

    # -----------------------------------------------------
    # ATLAS
    # -----------------------------------------------------

    atlas_info = get_server_info(
        "MONGODB ATLAS",
        ATLAS_URI
    )

    # -----------------------------------------------------
    # VERSION COMPARISON
    # -----------------------------------------------------

    same_version = (
        docker_info["version"] ==
        atlas_info["version"]
    )

    print("\n" + "=" * 60)
    print("VERSION COMPARISON")
    print("=" * 60)

    print(
        f"Docker MongoDB : "
        f"{docker_info['version']}"
    )

    print(
        f"MongoDB Atlas  : "
        f"{atlas_info['version']}"
    )

    if same_version:

        comparison_result = (
            "Both servers use the same MongoDB version."
        )

    else:

        comparison_result = (
            "The servers use different MongoDB versions."
        )

    print(f"Result: {comparison_result}")

    # -----------------------------------------------------
    # DOCUMENT FOR DOCKER
    # -----------------------------------------------------

    docker_document = {
        "activity": "2.1",
        "section": "Try It Yourself",
        "server": "Docker MongoDB",
        "version": docker_info["version"],
        "gitVersion": docker_info.get("gitVersion"),
        "platform": docker_info.get("platform"),
        "pid": docker_info.get("pid"),
        "recordedAt": datetime.now().isoformat()
    }

    # -----------------------------------------------------
    # DOCUMENT FOR ATLAS
    # -----------------------------------------------------

    atlas_document = {
        "activity": "2.1",
        "section": "Try It Yourself",
        "server": "MongoDB Atlas",
        "version": atlas_info["version"],
        "gitVersion": atlas_info.get("gitVersion"),
        "platform": atlas_info.get("platform"),
        "pid": atlas_info.get("pid"),
        "recordedAt": datetime.now().isoformat()
    }

    # -----------------------------------------------------
    # SAVE TO DOCKER
    # -----------------------------------------------------

    save_result(
        DOCKER_URI,
        "activity_2_1_try_it_yourself",
        docker_document
    )

    # -----------------------------------------------------
    # SAVE TO ATLAS
    # -----------------------------------------------------

    save_result(
        ATLAS_URI,
        "activity_2_1_try_it_yourself",
        atlas_document
    )

    # -----------------------------------------------------
    # FINISH
    # -----------------------------------------------------

    print("\n" + "=" * 60)

    print(
        "[OK] Docker result saved to:"
    )

    print(
        "     mongodb_activity_2."
        "activity_2_1_try_it_yourself"
    )

    print(
        "[OK] Atlas result saved to:"
    )

    print(
        "     mongodb_activity_2."
        "activity_2_1_try_it_yourself"
    )

    print("=" * 60)
    print("ACTIVITY 2.1 TRY IT YOURSELF COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()