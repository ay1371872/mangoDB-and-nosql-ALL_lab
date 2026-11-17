"""
Activity 7.2 - Try It Yourself

Objective: Compare data compression efficiency across schema variations
(Verbose JSON vs Flattened Schema vs Dense Arrays) to quantify disk savings.
"""

import json
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "compression_benchmark"

# Three schema designs for identical business data
RECORD_VERBOSE = {
    "transaction_identifier": "TXN-998877",
    "customer_full_name": "Ayush Yadav",
    "customer_financial_institution": "State Bank of India",
    "transaction_monetary_amount": 15450.75,
    "transaction_currency_code": "INR"
}

RECORD_FLATTENED = {
    "txn_id": "TXN-998877",
    "name": "Ayush Yadav",
    "bank": "SBI",
    "amount": 15450.75,
    "curr": "INR"
}

RECORD_DENSE = {
    "_id": "TXN-998877",
    "d": ["Ayush Yadav", "SBI", 15450.75, "INR"]
}

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
    print("ACTIVITY 7.2 - TRY IT YOURSELF: SCHEMA COMPRESSION BENCHMARK")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_many([RECORD_VERBOSE, RECORD_FLATTENED, RECORD_DENSE])

    # Calculate raw JSON string sizes
    len_v = len(json.dumps(RECORD_VERBOSE, default=json_util.default))
    len_f = len(json.dumps(RECORD_FLATTENED, default=json_util.default))
    len_d = len(json.dumps(RECORD_DENSE, default=json_util.default))

    print("=== Document Footprint Comparison ===")
    print(f"1. Verbose Schema    : {len_v} bytes | 100.0% (Baseline)")
    print(f"2. Flattened Schema  : {len_f} bytes | {len_f/len_v*100:.1f}% ({len_v - len_f} bytes saved per doc)")
    print(f"3. Dense Array Schema: {len_d} bytes | {len_d/len_v*100:.1f}% ({len_v - len_d} bytes saved per doc)")

    print("\n=== Impact at 100 Million Documents Scale ===")
    gb_v = (len_v * 100000000) / (1024**3)
    gb_f = (len_f * 100000000) / (1024**3)
    gb_d = (len_d * 100000000) / (1024**3)

    print(f"Verbose Storage      : {gb_v:.2f} GB")
    print(f"Flattened Storage    : {gb_f:.2f} GB (Saves {gb_v - gb_f:.2f} GB of Disk & RAM!)")
    print(f"Dense Storage        : {gb_d:.2f} GB (Saves {gb_v - gb_d:.2f} GB)")

    print("\nConclusion: Shortening repetitive key names significantly shrinks both disk and WiredTiger working set RAM.")

    with open("compression_7_2_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported compression dataset to compression_7_2_try_it_yourself.json")

if __name__ == "__main__":
    main()
