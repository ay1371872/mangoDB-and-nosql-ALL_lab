"""Activity 3.2 - Migrate a blog system from referenced to embedded design."""

import os
from datetime import datetime
from pymongo import MongoClient
from bson.json_util import dumps

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "activity_3_2.json"
)

POSTS = [
    {"_id": 1, "title": "Getting Started with MongoDB", "author": "Neha Kapoor",
     "tags": ["mongodb", "basics"], "created_at": datetime(2026, 9, 1, 9, 0)},
    {"_id": 2, "title": "Schema Design Patterns", "author": "Arjun Rao",
     "tags": ["schema", "design"], "created_at": datetime(2026, 9, 3, 10, 30)},
    {"_id": 3, "title": "Understanding Indexes", "author": "Neha Kapoor",
     "tags": ["indexes", "performance"], "created_at": datetime(2026, 9, 5, 14, 15)},
    {"_id": 4, "title": "Aggregation Pipeline Basics", "author": "Sana Khan",
     "tags": ["aggregation"], "created_at": datetime(2026, 9, 8, 11, 0)},
    {"_id": 5, "title": "Replication and Sharding Explained", "author": "Arjun Rao",
     "tags": ["replication", "sharding"], "created_at": datetime(2026, 9, 10, 16, 45)},
]

COMMENTS = [
    {"post_id": 1, "author": "Rahul", "text": "Great introduction, very clear!",
     "created_at": datetime(2026, 9, 1, 12, 0)},
    {"post_id": 1, "author": "Priya", "text": "Helped me set up my first database.",
     "created_at": datetime(2026, 9, 1, 15, 30)},
    {"post_id": 1, "author": "Imran", "text": "Could you cover Compass next?",
     "created_at": datetime(2026, 9, 2, 8, 10)},
    {"post_id": 2, "author": "Priya", "text": "Embedding vs referencing finally makes sense.",
     "created_at": datetime(2026, 9, 3, 13, 0)},
    {"post_id": 2, "author": "Karan", "text": "What about the bucket pattern?",
     "created_at": datetime(2026, 9, 4, 9, 20)},
    {"post_id": 3, "author": "Rahul", "text": "The compound index tip saved me.",
     "created_at": datetime(2026, 9, 5, 18, 0)},
    {"post_id": 3, "author": "Sneha", "text": "Please explain index intersection.",
     "created_at": datetime(2026, 9, 6, 10, 45)},
    {"post_id": 4, "author": "Imran", "text": "$lookup examples were helpful.",
     "created_at": datetime(2026, 9, 8, 14, 0)},
    {"post_id": 4, "author": "Karan", "text": "More on $group please.",
     "created_at": datetime(2026, 9, 9, 7, 30)},
    {"post_id": 5, "author": "Sneha", "text": "Clear explanation of shard keys.",
     "created_at": datetime(2026, 9, 11, 9, 5)},
]


class QueryCounter:
    """Counts the number of requests sent to the database."""

    def __init__(self):
        self.count = 0

    def run(self, func):
        self.count += 1
        return func()


def banner(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main():
    print("=" * 60)
    print("ACTIVITY 3.2 - REFERENCED TO EMBEDDED MIGRATION")
    print("=" * 60)

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    try:
        client.admin.command("ping")
        print("[OK] Connected to Docker MongoDB")

        db = client["mongodb_activity_3"]
        for name in ["posts", "comments", "posts_embedded"]:
            if name in db.list_collection_names():
                db[name].drop()
        posts, comments, posts_embedded = (
            db["posts"], db["comments"], db["posts_embedded"]
        )

        # ----------------------------------------------------------
        # Step 1: referenced design
        # ----------------------------------------------------------
        banner("STEP 1 - REFERENCED DESIGN (posts + comments)")
        posts.insert_many(POSTS)
        comments.insert_many(COMMENTS)
        comments.create_index("post_id")
        print(f"[OK] Inserted {posts.count_documents({})} posts")
        print(f"[OK] Inserted {comments.count_documents({})} comments "
              "(each holds post_id)")
        print("[OK] Created index on comments.post_id")

        # ----------------------------------------------------------
        # Step 2: $lookup - post with its comments in ONE query
        # ----------------------------------------------------------
        banner("STEP 2 - POST WITH COMMENTS USING $lookup")
        pipeline = [
            {"$match": {"_id": 1}},
            {"$lookup": {"from": "comments", "localField": "_id",
                         "foreignField": "post_id", "as": "comments"}},
        ]
        result = list(posts.aggregate(pipeline))[0]
        print(f"Post    : {result['title']} (by {result['author']})")
        print(f"Comments: {len(result['comments'])}")
        for c in result["comments"]:
            print(f"  - {c['author']}: {c['text']}")

        # ----------------------------------------------------------
        # Step 3: migrate to embedded design (Python script)
        # ----------------------------------------------------------
        banner("STEP 3 - MIGRATE TO EMBEDDED DESIGN")
        migrated = 0
        for post in posts.find().sort("_id", 1):
            post["comments"] = list(
                comments.find({"post_id": post["_id"]},
                              {"_id": 0, "post_id": 0}).sort("created_at", 1)
            )
            posts_embedded.insert_one(post)
            migrated += len(post["comments"])
            print(f"  Post {post['_id']}: embedded "
                  f"{len(post['comments'])} comment(s)")

        embedded_total = sum(
            len(p["comments"]) for p in posts_embedded.find()
        )
        print(f"[OK] Migrated {posts_embedded.count_documents({})} posts "
              f"and {embedded_total} comments")
        if embedded_total == comments.count_documents({}):
            print("[OK] Verification passed: no comments lost")

        # ----------------------------------------------------------
        # Step 4: compare the number of database queries
        # ----------------------------------------------------------
        banner("STEP 4 - NUMBER OF QUERIES TO SHOW POST 1 + COMMENTS")

        ref = QueryCounter()
        post = ref.run(lambda: posts.find_one({"_id": 1}))
        post_comments = ref.run(
            lambda: list(comments.find({"post_id": 1}).sort("created_at", 1))
        )
        ref_shown = len(post_comments)

        look = QueryCounter()
        looked = look.run(lambda: list(posts.aggregate(pipeline)))
        look_shown = len(looked[0]["comments"])

        emb = QueryCounter()
        embedded = emb.run(lambda: posts_embedded.find_one({"_id": 1}))
        emb_shown = len(embedded["comments"])

        print(f"{'Design':<34}{'Queries':<9}{'Comments shown'}")
        print("-" * 60)
        print(f"{'Referenced (two separate queries)':<34}{ref.count:<9}{ref_shown}")
        print(f"{'Referenced (single $lookup)':<34}{look.count:<9}{look_shown}")
        print(f"{'Embedded (one document read)':<34}{emb.count:<9}{emb_shown}")
        print("\nNote: $lookup needs 1 request but the server still performs")
        print("a join; the embedded read fetches one document, no join.")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(dumps(list(posts_embedded.find()), indent=2))
        print(f"\n[OK] Exported posts_embedded to "
              f"{os.path.basename(OUTPUT_FILE)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
