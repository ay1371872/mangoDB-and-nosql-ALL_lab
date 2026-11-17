"""
Activity 16.1 - Try It Yourself

Objective: Benchmark query complexity and execution hops for a 3-degree
friend-of-a-friend recommendation in MongoDB ($graphLookup) vs. Graph DB.
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "graph_query_comparison"

GRAPH_BENCHMARK = [
    {"query_depth": "1-Hop (Direct Friends)",   "mongo_operator": "$lookup / direct match", "mongo_latency_ms": 1.2, "graph_db_latency_ms": 0.8, "recommendation": "Either engine performs exceptionally"},
    {"query_depth": "2-Hop (Mutual Friends)",   "mongo_operator": "$graphLookup (maxDepth=1)","mongo_latency_ms": 4.5, "graph_db_latency_ms": 1.4, "recommendation": "MongoDB handles comfortably"},
    {"query_depth": "3-Hop (Extended Network)", "mongo_operator": "$graphLookup (maxDepth=2)","mongo_latency_ms": 18.2,"graph_db_latency_ms": 2.1, "recommendation": "Graph DB index-free adjacency wins at deep depths"},
]

def get_database():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        client.admin.command("ping")
        return client, client[DB_NAME]
    except Exception:
        import mongomock
        return mongomock.MongoClient(), mongomock.MongoClient()[DB_NAME]

def main():
    print("=" * 60)
    print("ACTIVITY 16.1 - TRY IT YOURSELF: GRAPH TRAVERSAL BENCHMARK")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(GRAPH_BENCHMARK)

    print("=== Multi-Hop Recommendation Latency Comparison ===")
    for g in GRAPH_BENCHMARK:
        print(f"Depth: {g['query_depth']:<28} | MongoDB: {g['mongo_latency_ms']:>4.1f}ms | Graph DB: {g['graph_db_latency_ms']:>4.1f}ms")

    with open("graph_comp_16_1_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported graph benchmark to graph_comp_16_1_try_it_yourself.json")

if __name__ == "__main__":
    main()
