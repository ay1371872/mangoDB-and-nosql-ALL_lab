import os
from pymongo import MongoClient

atlas_uri = os.getenv("MONGO_ATLAS_URI")

if not atlas_uri:
    print("ERROR: MONGO_ATLAS_URI is not set.")
    raise SystemExit

client = MongoClient(atlas_uri)

try:
    info = client.server_info()

    print("=" * 50)
    print("MONGODB ATLAS CONNECTION TEST")
    print("=" * 50)
    print("Connection: SUCCESS")
    print("MongoDB Version:", info["version"])
    print("Git Version:", info.get("gitVersion"))

finally:
    client.close()