from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

try:
    info = client.server_info()

    print("=" * 50)
    print("DOCKER MONGODB CONNECTION TEST")
    print("=" * 50)
    print("Connection: SUCCESS")
    print("MongoDB Version:", info["version"])
    print("Git Version:", info.get("gitVersion"))

finally:
    client.close()