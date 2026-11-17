from pymongo import MongoClient


client = MongoClient(
    "mongodb://localhost:27017",
    serverSelectionTimeoutMS=5000
)

db = client["bookstore"]
books = db["books"]


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


try:

    print("=" * 60)
    print("ACTIVITY 2.2 - TRY IT YOURSELF")
    print("=" * 60)

    # Reset collection
    books.drop()

    # Insert original dataset
    result = books.insert_many(BOOKS)

    print(f"[OK] Inserted {len(result.inserted_ids)} books")

    # --------------------------------------------------
    # BEFORE UPDATE
    # --------------------------------------------------

    print("\n=== BEFORE PRICE UPDATE ===")

    for book in books.find(
        {"year": {"$lt": 2010}},
        {
            "_id": 0,
            "title": 1,
            "year": 1,
            "price": 1
        }
    ):
        print(
            f"  {book['title']} | "
            f"Year: {book['year']} | "
            f"Price: ${book['price']:.2f}"
        )

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    print("\n=== AFTER 10% PRICE UPDATE ===")

    result = books.update_many(
        {"year": {"$lt": 2010}},
        {"$mul": {"price": 1.10}}
    )

    print(f"[OK] Matched: {result.matched_count}")
    print(f"[OK] Modified: {result.modified_count}")

    # Show updated documents
    for book in books.find(
        {"year": {"$lt": 2010}},
        {
            "_id": 0,
            "title": 1,
            "year": 1,
            "price": 1
        }
    ):
        print(
            f"  {book['title']} | "
            f"Year: {book['year']} | "
            f"Price: ${book['price']:.2f}"
        )

    print("\n[OK] Clean Code is intentionally left in the")
    print("     collection for Compass verification.")

finally:
    client.close()