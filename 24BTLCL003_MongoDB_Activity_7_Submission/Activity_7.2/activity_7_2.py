"""
Activity 7.2 - Working Set Analysis & WiredTiger Cache Sizing

Demonstrates:
1. Estimating collection data size, index size, and total storage
2. Computing the Working Set RAM requirements for WiredTiger
3. Analyzing dirty cache eviction thresholds and page fault risks
"""

import json
from bson import json_util
from pymongo import MongoClient, ASCENDING

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "transactions_workingset"

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
    print("ACTIVITY 7.2 - WORKING SET ANALYSIS & WIREDTIGER CACHE")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()

    # Seed simulated transactions
    txns = []
    for i in range(1, 1001):
        txns.append({
            "txn_id": f"TXN-{i:06d}",
            "account_id": f"ACC-{i%50:03d}",
            "amount": float(i * 13.5),
            "type": "debit" if i % 2 == 0 else "credit",
            "timestamp": "2024-03-15T12:00:00Z",
            "metadata": {"ip": f"10.0.{i%255}.1", "channel": "mobile_app"}
        })
    col.insert_many(txns)
    col.create_index([("account_id", ASCENDING), ("timestamp", ASCENDING)], name="idx_acc_time")
    print(f"[OK] Inserted {len(txns)} transaction documents into '{COLLECTION_NAME}'\n")

    # Metrics calculation
    num_docs = len(txns)
    avg_obj_bytes = 210  # Approx BSON document size
    total_data_bytes = num_docs * avg_obj_bytes
    total_index_bytes = num_docs * 38  # Approx B-tree entry size

    # Sizing for 10 Million production scale projection
    scale_factor = 10000000 / num_docs
    proj_data_gb = (total_data_bytes * scale_factor) / (1024**3)
    proj_index_gb = (total_index_bytes * scale_factor) / (1024**3)

    # Active working set typically 20% frequently accessed hot data + 100% indexes
    working_set_gb = (proj_data_gb * 0.20) + proj_index_gb
    # WiredTiger cache formula: 50% of (Total RAM - 1GB)
    rec_ram_gb = (working_set_gb / 0.5) + 1.0

    print("=== Current Lab Storage Profile (1,000 Documents) ===")
    print(f"Document Count       : {num_docs}")
    print(f"Data Size (Uncomp.)  : {total_data_bytes / 1024:.2f} KB")
    print(f"Index Size           : {total_index_bytes / 1024:.2f} KB")
    print(f"Total Disk Footprint : {(total_data_bytes + total_index_bytes) / 1024:.2f} KB")

    print("\n=== Production Capacity Planning Projection (10,000,000 Documents) ===")
    print(f"Projected Raw Data   : {proj_data_gb:.2f} GB")
    print(f"Projected Indexes    : {proj_index_gb:.2f} GB")
    print(f"Hot Data Set (20%)   : {proj_data_gb * 0.20:.2f} GB")
    print(f"Active Working Set   : {working_set_gb:.2f} GB (Hot Data + All Indexes)")
    print(f"Recommended Node RAM : {rec_ram_gb:.2f} GB -> Provision: 16 GB Node")

    print("\n=== WiredTiger Memory Allocation Rules ===")
    print("1. Working Set must fit entirely in RAM to prevent disk thrashing (page faults).")
    print("2. WiredTiger reserves 50% of (RAM - 1GB) for internal cache.")
    print("3. Remaining RAM is utilized by OS Filesystem Cache for compressed pages.")

    with open("transactions_workingset_7_2.json", "w") as f:
        f.write(json.dumps(txns[:10], default=json_util.default, indent=2))
    print("\n[OK] Exported sample transactions to transactions_workingset_7_2.json")

if __name__ == "__main__":
    main()
