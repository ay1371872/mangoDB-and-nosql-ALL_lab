from pymongo import MongoClient


# Connect to Docker MongoDB
client = MongoClient(
    "mongodb://localhost:27017",
    serverSelectionTimeoutMS=5000
)

print("=" * 60)
print("ACTIVITY 2.2 - BOOKSTORE CRUD OPERATIONS")
print("=" * 60)

try:
    # Test connection
    client.admin.command("ping")
    print("[OK] Connected to Docker MongoDB")

    # Database and collection
    db = client["bookstore"]

    # Start fresh for every run
    if "books" in db.list_collection_names():
        db["books"].drop()

    books = db["books"]

    # --------------------------------------------------
    # CREATE
    # --------------------------------------------------

    BOOKS = [
        {
            "title": "The Pragmatic Programmer",
            "author": "David Thomas & Andrew Hunt",
            "year": 2019,
            "genre": "Software Engineering",
            "price": 49.99,
            "isbn": "978-0135957059",
            "tags": ["programming", "career", "best-practices"],
            "publisher": {
                "name": "Addison-Wesley",
                "location": "Boston"
            }
        },
        {
            "title": "Designing Data-Intensive Applications",
            "author": "Martin Kleppmann",
            "year": 2017,
            "genre": "Databases",
            "price": 45.99,
            "isbn": "978-1449373320",
            "tags": ["databases", "distributed-systems", "architecture"],
            "publisher": {
                "name": "O'Reilly Media",
                "location": "Sebastopol"
            }
        },
        {
            "title": "Deep Learning",
            "author": "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
            "year": 2016,
            "genre": "Machine Learning",
            "price": 72.00,
            "isbn": "978-0262035613",
            "tags": ["AI", "neural-networks", "theory"],
            "publisher": {
                "name": "MIT Press",
                "location": "Cambridge"
            }
        },
        {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "year": 2008,
            "genre": "Software Engineering",
            "price": 39.99,
            "isbn": "978-0132350884",
            "tags": ["programming", "clean-code", "refactoring"],
            "publisher": {
                "name": "Prentice Hall",
                "location": "Upper Saddle River"
            }
        },
        {
            "title": "Hands-On Machine Learning",
            "author": "Aurelien Geron",
            "year": 2022,
            "genre": "Machine Learning",
            "price": 59.99,
            "isbn": "978-1098125974",
            "tags": ["AI", "scikit-learn", "tensorflow", "practical"],
            "publisher": {
                "name": "O'Reilly Media",
                "location": "Sebastopol"
            }
        }
    ]

    result = books.insert_many(BOOKS)

    print("\n=== CREATE: Inserting 5 books ===")
    print(f"[OK] Inserted {len(result.inserted_ids)} books")

    # --------------------------------------------------
    # READ: year > 2020
    # --------------------------------------------------

    print("\n=== READ: Books published after 2020 ===")

    recent = books.find(
        {"year": {"$gt": 2020}},
        {"_id": 0, "title": 1, "year": 1, "price": 1}
    )

    for book in recent:
        print(
            f"  {book['title']:<45} "
            f"({book['year']}) - ${book['price']:.2f}"
        )

    # --------------------------------------------------
    # UPDATE: year < 2010
    # --------------------------------------------------

    print("\n=== UPDATE: 10% price increase for books before 2010 ===")

    # Save prices before update
    before = {}

    for book in books.find(
        {"year": {"$lt": 2010}},
        {"_id": 0, "title": 1, "price": 1}
    ):
        before[book["title"]] = book["price"]

    # IMPORTANT: Only books before 2010
    update_result = books.update_many(
        {"year": {"$lt": 2010}},
        {"$mul": {"price": 1.10}}
    )

    print(f"[OK] Matched {update_result.matched_count} book(s)")
    print(f"[OK] Updated {update_result.modified_count} book(s)")

    # Display updated prices
    for book in books.find(
        {"year": {"$lt": 2010}},
        {"_id": 0, "title": 1, "price": 1}
    ):
        old_price = before[book["title"]]
        new_price = book["price"]

        print(
            f"  {book['title']:<45} "
            f"${old_price:.2f} -> ${new_price:.2f}"
        )

    # --------------------------------------------------
    # DELETE: Clean Code
    # --------------------------------------------------

    print("\n=== DELETE: Removing 'Clean Code' ===")

    delete_result = books.delete_one(
        {"title": "Clean Code"}
    )

    print(
        f"[OK] Deleted {delete_result.deleted_count} document(s)"
    )

    print(
        f"  Remaining books: {books.count_documents({})}"
    )

    # --------------------------------------------------
    # FINAL COLLECTION
    # --------------------------------------------------

    print("\n=== Final Collection State ===")

    for book in books.find(
        {},
        {"_id": 0, "title": 1}
    ):
        print(f"  {book['title']}")

    print("\n" + "=" * 60)
    print("ACTIVITY 2.2 COMPLETE")
    print("=" * 60)

except Exception as e:
    print("\n[ERROR]")
    print(type(e).__name__, ":", e)

finally:
    client.close()