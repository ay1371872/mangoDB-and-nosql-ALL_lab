"""
Activity 16.1 - Cross-Model Polyglot Data Modeling

Demonstrates:
1. Comparing Document (MongoDB), Relational (PostgreSQL),
   Wide-Column (Cassandra), and Graph (Neo4j) models
2. Access pattern suitability and schema flexibility
3. Evaluating query ergonomics for heterogeneous enterprise workloads
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "polyglot_catalog"

PARADIGM_COMPARISON = [
    {"paradigm": "Document (MongoDB)",    "primary_use_case": "Catalogs, E-Commerce, User Profiles", "scaling": "Horizontal via Sharding", "schema": "Dynamic JSON/BSON", "query_strength": "Rich nested queries & aggregations"},
    {"paradigm": "Relational (PostgreSQL)","primary_use_case": "Financial Ledgers, Accounting, ERP", "scaling": "Vertical / Read Replicas", "schema": "Strict Tabular SQL", "query_strength": "Complex multi-table relational joins"},
    {"paradigm": "Wide-Column (Cassandra)","primary_use_case": "High-write IoT Telemetry, Time-Series","scaling": "Masterless P2P Ring",   "schema": "Partitioned Tables",  "query_strength": "High throughput append-only writes"},
    {"paradigm": "Graph (Neo4j)",         "primary_use_case": "Social Networks, Fraud Rings, Recs",  "scaling": "Causal Clustering",       "schema": "Nodes & Relationships","query_strength": "Multi-hop graph relationship traversals"},
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
    print("ACTIVITY 16.1 - POLYGLOT DATA MODELING COMPARISON")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many(PARADIGM_COMPARISON)

    print("=== Polyglot Persistence Architecture Matrix ===")
    print(f"{'Paradigm':<24} {'Best Use Case':<28} {'Scaling Model':<22} {'Query Strength'}")
    print("-" * 95)
    for p in PARADIGM_COMPARISON:
        print(f"{p['paradigm']:<24} {p['primary_use_case']:<28} {p['scaling']:<22} {p['query_strength'][:20]}...")

    print("\nTakeaway: Modern architectures adopt Polyglot Persistence: MongoDB for core documents, Redis for cache, and Neo4j for graph connections.")

    with open("polyglot_16_1.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported polyglot comparison to polyglot_16_1.json")

if __name__ == "__main__":
    main()
