"""Activity 3.1 Try It Yourself - Course prerequisites: embed or reference?

Decision: REFERENCE. Each course stores a small array of prerequisite
course CODES; the full prerequisite course is never copied (embedded).
"""

import os
import textwrap
from pymongo import MongoClient
from bson.json_util import dumps

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "activity_3_1_try_it_yourself.json",
)

VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "code", "instructor", "schedule", "prerequisites"],
        "properties": {
            "title": {"bsonType": "string"},
            "code": {"bsonType": "string", "pattern": "^[A-Z]{2,4}[0-9]{3}$"},
            "instructor": {"bsonType": "string"},
            "schedule": {"bsonType": "object"},
            "prerequisites": {
                "bsonType": "array",
                "items": {"bsonType": "string", "pattern": "^[A-Z]{2,4}[0-9]{3}$"},
            },
        },
    }
}


def course(code, title, instructor, days, start, end, room, prerequisites):
    return {
        "title": title, "code": code, "instructor": instructor,
        "schedule": {"days": days, "start_time": start,
                     "end_time": end, "room": room},
        "prerequisites": prerequisites,      # references: course codes
    }


COURSES = [
    course("CS101", "Introduction to Programming", "Dr. Anita Desai",
           ["Monday", "Wednesday"], "09:00", "10:30", "A-101", []),
    course("CS201", "Data Structures", "Dr. Rohan Mehta",
           ["Tuesday", "Thursday"], "09:00", "10:30", "A-102", ["CS101"]),
    course("CS301", "Database Systems", "Dr. Meera Iyer",
           ["Monday", "Wednesday"], "11:00", "12:30", "B-204", ["CS201"]),
    course("CS302", "Operating Systems", "Dr. Rohan Mehta",
           ["Tuesday", "Friday"], "11:00", "12:30", "B-110", ["CS201"]),
    course("CS401", "Advanced Database Systems", "Dr. Meera Iyer",
           ["Monday", "Wednesday"], "10:00", "11:30", "B-204", ["CS301"]),
    course("CS403", "Distributed Systems", "Dr. Meera Iyer",
           ["Monday", "Friday"], "14:00", "15:30", "C-305", ["CS301", "CS302"]),
]

DECISION = [
    ("Many-to-many",
     "A course can have several prerequisites and can itself be a "
     "prerequisite for several courses, so the relationship is many-to-many."),
    ("No duplication",
     "Embedding a prerequisite course would copy its title, instructor and "
     "schedule into every course that needs it; one change would need many "
     "updates and copies would go stale."),
    ("Small and bounded",
     "A course has only a handful of prerequisites, so an array of codes "
     "stays tiny and can be read together with the course."),
    ("Chains and reverse look-ups",
     "Prerequisite chains (CS403 -> CS301 -> CS201 -> CS101) and 'what does "
     "this course unlock?' work with $lookup or by querying the code array."),
    ("Trade-off",
     "Showing full prerequisite details costs an extra lookup, which is "
     "acceptable because the data is small and read-mostly."),
]


def banner(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def prerequisite_chain(courses, code, seen=None):
    """Walk the prerequisite references recursively (breadth first)."""
    seen = seen if seen is not None else []
    doc = courses.find_one({"code": code})
    for prereq in doc["prerequisites"]:
        if prereq not in seen:
            seen.append(prereq)
            prerequisite_chain(courses, prereq, seen)
    return seen


def main():
    print("=" * 60)
    print("ACTIVITY 3.1 - TRY IT YOURSELF: COURSE PREREQUISITES")
    print("=" * 60)

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    try:
        client.admin.command("ping")
        print("[OK] Connected to Docker MongoDB")

        db = client["mongodb_activity_3"]
        if "courses_with_prerequisites" in db.list_collection_names():
            db["courses_with_prerequisites"].drop()
        db.create_collection("courses_with_prerequisites", validator=VALIDATOR)
        courses = db["courses_with_prerequisites"]

        courses.insert_many(COURSES)
        print(f"[OK] Inserted {courses.count_documents({})} courses into "
              "mongodb_activity_3.courses_with_prerequisites")

        banner("DESIGN DECISION: REFERENCE (STORE PREREQUISITE CODES)")
        for heading, reason in DECISION:
            print(textwrap.fill(
                reason, width=76, initial_indent=f"* {heading}: ",
                subsequent_indent="  ",
            ))

        banner("DIRECT PREREQUISITES (USING $lookup)")
        pipeline = [
            {"$lookup": {"from": "courses_with_prerequisites",
                         "localField": "prerequisites",
                         "foreignField": "code",
                         "as": "prereq_details"}},
            {"$sort": {"code": 1}},
        ]
        for doc in courses.aggregate(pipeline):
            names = [f"{p['code']} {p['title']}" for p in doc["prereq_details"]]
            print(f"{doc['code']} {doc['title']}")
            print(f"    requires: {', '.join(names) if names else 'None'}")

        banner("FULL PREREQUISITE CHAIN FOR CS403")
        chain = prerequisite_chain(courses, "CS403")
        print("CS403 requires (in order found): " + ", ".join(chain))

        banner("WHICH COURSES DOES CS301 UNLOCK?")
        for doc in courses.find({"prerequisites": "CS301"}).sort("code", 1):
            print(f"  {doc['code']} - {doc['title']}")

        banner("ELIGIBILITY CHECK")
        completed = ["CS101", "CS201"]
        print(f"Student has completed: {', '.join(completed)}")
        print("Eligible to enrol in:")
        for doc in courses.find().sort("code", 1):
            if doc["code"] in completed:
                continue
            if all(p in completed for p in doc["prerequisites"]):
                print(f"  {doc['code']} - {doc['title']}")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(dumps(list(courses.find()), indent=2))
        print(f"\n[OK] Exported collection to {os.path.basename(OUTPUT_FILE)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
