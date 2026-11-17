"""
Activity 12.2 - Try It Yourself

Objective: Simulate Client-Side Field Level Encryption (CSFLE) with AEAD
deterministic vs randomized encryption algorithms for field security.
"""

import json
import hashlib
from bson import json_util
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "nosql_labs"
COLLECTION_NAME = "csfle_simulation"

def deterministic_enc(val, key):
    return "BIN_AEAD_DET:" + hashlib.sha256((val + key).encode()).hexdigest()[:24]

def randomized_enc(val, key, nonce):
    return "BIN_AEAD_RND:" + hashlib.sha256((val + key + nonce).encode()).hexdigest()[:24]

ENCRYPTED_DOC = {
    "account_id": "ACC-5544",
    "owner": "Ayush Yadav",
    "ssn_encrypted": deterministic_enc("123-45-6789", "KEY_SECRET"),
    "salary_encrypted": randomized_enc("125000", "KEY_SECRET", "NONCE_01")
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
    print("ACTIVITY 12.2 - TRY IT YOURSELF: CSFLE ENCRYPTION")
    print("=" * 60)

    client, db = get_database()
    col = db[COLLECTION_NAME]
    col.drop()
    col.insert_one(ENCRYPTED_DOC)

    print("=== Document Stored on MongoDB Server (Ciphertext Only) ===")
    print(f"Account ID   : {ENCRYPTED_DOC['account_id']}")
    print(f"SSN (Det.)   : {ENCRYPTED_DOC['ssn_encrypted']} (Allows Equality Queries)")
    print(f"Salary (Rnd.): {ENCRYPTED_DOC['salary_encrypted']} (Strongest Protection)")

    print("\n[OK] Even Database Administrators (DBAs) cannot inspect raw plaintexts.")

    with open("csfle_12_2_try_it_yourself.json", "w") as f:
        f.write(json.dumps(list(col.find()), default=json_util.default, indent=2))
    print("\n[OK] Exported CSFLE record to csfle_12_2_try_it_yourself.json")

if __name__ == "__main__":
    main()
