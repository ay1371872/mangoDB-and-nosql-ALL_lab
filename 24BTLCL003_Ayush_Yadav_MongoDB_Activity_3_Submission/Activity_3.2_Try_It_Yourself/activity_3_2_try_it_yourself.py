"""Activity 3.2 Try It Yourself - A post with 10,000 comments.

Why embedding becomes a problem, and the alternative design
(reference + subset pattern with paginated comments).
"""

import json
import os
import random
import textwrap
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.json_util import dumps

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "activity_3_2_try_it_yourself.json",
)

MAX_DOC_BYTES = 16 * 1024 * 1024          # MongoDB 16 MB document limit
TOTAL_COMMENTS = 10000
LATEST_COUNT = 5
PAGE_SIZE = 20

AUTHORS = ["Rahul", "Priya", "Imran", "Karan", "Sneha", "Meera", "Vikram"]
PHRASES = [
    "Really enjoyed this post, thanks for sharing the details.",
    "Could you explain the indexing part with one more example?",
    "This cleared up my confusion about schema design.",
    "I tried this in my project and it worked well.",
    "Looking forward to the next article in this series.",
    "Is there a performance difference on very large collections?",
]

PROBLEMS = [
    ("Document size limit",
     "A BSON document cannot exceed 16 MB. Comments grow without bound, so "
     "a popular post can eventually fail to accept new comments."),
    ("Large reads",
     "Every read of the post loads all comments, wasting memory and "
     "network even when the page shows only a few of them."),
    ("Expensive writes",
     "Each new comment grows the document, which can force it to be "
     "rewritten and increases write amplification."),
    ("No pagination",
     "Comments inside one document cannot be efficiently paged, sorted "
     "or filtered without loading the whole array first."),
    ("Write contention",
     "Many users commenting at once all update the same document."),
]


def banner(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def size_bytes(obj):
    """Approximate document size using its JSON text (sandbox-independent)."""
    return len(json.dumps(obj, default=str).encode("utf-8"))


def make_comments(post_id):
    random.seed(7)
    start = datetime(2026, 9, 1, 8, 0)
    return [
        {
            "post_id": post_id,
            "author": random.choice(AUTHORS),
            "text": random.choice(PHRASES),
            "created_at": start + timedelta(minutes=i),
        }
        for i in range(TOTAL_COMMENTS)
    ]


def main():
    print("=" * 60)
    print("ACTIVITY 3.2 - TRY IT YOURSELF: 10,000 COMMENTS")
    print("=" * 60)

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    try:
        client.admin.command("ping")
        print("[OK] Connected to Docker MongoDB")

        db = client["mongodb_activity_3"]
        for name in ["viral_posts", "viral_comments"]:
            if name in db.list_collection_names():
                db[name].drop()
        posts, comments = db["viral_posts"], db["viral_comments"]

        base_post = {
            "_id": 1, "title": "Why MongoDB Schema Design Matters",
            "author": "Neha Kapoor", "tags": ["mongodb", "schema"],
        }
        all_comments = make_comments(1)

        # ----------------------------------------------------------
        # Part 1: what would embedding cost?
        # ----------------------------------------------------------
        banner("PART 1 - IF ALL 10,000 COMMENTS WERE EMBEDDED")
        embedded_doc = dict(base_post)
        embedded_doc["comments"] = [
            {k: v for k, v in c.items() if k != "post_id"}
            for c in all_comments
        ]
        embedded_size = size_bytes(embedded_doc)
        per_comment = size_bytes(embedded_doc["comments"]) / TOTAL_COMMENTS
        print(f"Comments embedded      : {TOTAL_COMMENTS:,}")
        print(f"Approx. document size  : {embedded_size / 1024 / 1024:.2f} MB")
        print(f"Approx. bytes/comment  : {per_comment:.0f}")
        print(f"MongoDB document limit : {MAX_DOC_BYTES / 1024 / 1024:.0f} MB")
        print(f"Share of limit used    : "
              f"{embedded_size / MAX_DOC_BYTES * 100:.1f}%")
        print(f"Limit reached at about : "
              f"{int(MAX_DOC_BYTES / per_comment):,} comments")

        banner("WHY EMBEDDING IS PROBLEMATIC")
        for heading, reason in PROBLEMS:
            print(textwrap.fill(
                reason, width=76, initial_indent=f"* {heading}: ",
                subsequent_indent="  ",
            ))

        # ----------------------------------------------------------
        # Part 2: alternative = reference + subset pattern
        # ----------------------------------------------------------
        banner("PART 2 - ALTERNATIVE: REFERENCE + SUBSET PATTERN")
        comments.insert_many(all_comments)
        comments.create_index([("post_id", 1), ("created_at", -1)])
        print(f"[OK] Stored {comments.count_documents({'post_id': 1}):,} "
              "comments in their own collection")
        print("[OK] Created index on (post_id, created_at)")

        latest = list(
            comments.find({"post_id": 1}, {"_id": 0, "post_id": 0})
            .sort("created_at", -1).limit(LATEST_COUNT)
        )
        post_doc = dict(base_post)
        post_doc["comment_count"] = comments.count_documents({"post_id": 1})
        post_doc["latest_comments"] = latest
        posts.insert_one(post_doc)
        print(f"[OK] Post stores comment_count and the {LATEST_COUNT} "
              "latest comments only")

        # first page of the post = one small document
        first_page = posts.find_one({"_id": 1})
        first_page_size = size_bytes(first_page)

        # a user opens page 3 of the full comment list
        page = 3
        page_docs = list(
            comments.find({"post_id": 1}, {"_id": 0, "post_id": 0})
            .sort("created_at", -1)
            .skip((page - 1) * PAGE_SIZE).limit(PAGE_SIZE)
        )
        page_size = size_bytes(page_docs)

        banner("PERFORMANCE COMPARISON (DATA LOADED PER PAGE VIEW)")
        print(f"{'Design':<36}{'Comments loaded':<17}{'Approx. size'}")
        print("-" * 60)
        print(f"{'Embedded: open the post':<36}{TOTAL_COMMENTS:<17,}"
              f"{embedded_size / 1024:,.0f} KB")
        print(f"{'Subset: open the post':<36}{LATEST_COUNT:<17}"
              f"{first_page_size / 1024:.1f} KB")
        print(f"{'Subset: comments page ' + str(page):<36}{len(page_docs):<17}"
              f"{page_size / 1024:.1f} KB")

        print(f"\nLatest {LATEST_COUNT} comments shown with the post:")
        for c in first_page["latest_comments"]:
            print(f"  {c['created_at']:%Y-%m-%d %H:%M} {c['author']:<7} "
                  f"{c['text'][:34]}")

        banner("RECOMMENDED DESIGN")
        print("* posts collection   : post + comment_count + latest comments")
        print("* comments collection: one document per comment, with post_id")
        print("* index              : (post_id, created_at) for paging")
        print("* bucket pattern     : optional, group ~100 comments/document")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(dumps(list(posts.find()), indent=2))
        print(f"\n[OK] Exported viral_posts to {os.path.basename(OUTPUT_FILE)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
