"""Activity 3.1 - Embedded document schema for a course enrollment system."""

import os
from pymongo import MongoClient
from pymongo.errors import WriteError
from bson.json_util import dumps

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "activity_3_1.json"
)

# Step 2: schema validation. title, code, instructor and schedule are required.
VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "code", "instructor", "schedule"],
        "properties": {
            "title": {"bsonType": "string"},
            "code": {
                "bsonType": "string",
                "pattern": "^[A-Z]{2,4}[0-9]{3}$",
                "description": "Course code such as CS401",
            },
            "instructor": {"bsonType": "string"},
            "credits": {"bsonType": "int", "minimum": 1, "maximum": 6},
            "schedule": {
                "bsonType": "object",
                "required": ["days", "start_time", "end_time", "room"],
                "properties": {
                    "days": {"bsonType": "array", "items": {"bsonType": "string"}},
                    "start_time": {"bsonType": "string"},
                    "end_time": {"bsonType": "string"},
                    "room": {"bsonType": "string"},
                },
            },
            "roster": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["name", "student_id", "grade"],
                    "properties": {
                        "name": {"bsonType": "string"},
                        "student_id": {"bsonType": "string"},
                        "grade": {"bsonType": "string"},
                    },
                },
            },
        },
    }
}

# Step 1: courses with the roster and schedule embedded inside each document.
COURSES = [
    {
        "title": "Advanced Database Systems",
        "code": "CS401",
        "instructor": "Dr. Meera Iyer",
        "credits": 4,
        "schedule": {"days": ["Monday", "Wednesday"], "start_time": "10:00",
                     "end_time": "11:30", "room": "B-204"},
        "roster": [
            {"name": "Aarav Sharma", "student_id": "S1001", "grade": "A"},
            {"name": "Diya Patel", "student_id": "S1002", "grade": "B+"},
            {"name": "Kabir Singh", "student_id": "S1003", "grade": "A"},
            {"name": "Ananya Rao", "student_id": "S1004", "grade": "B"},
        ],
    },
    {
        "title": "Machine Learning Fundamentals",
        "code": "CS402",
        "instructor": "Dr. Rohan Mehta",
        "credits": 3,
        "schedule": {"days": ["Tuesday", "Thursday"], "start_time": "09:00",
                     "end_time": "10:30", "room": "A-101"},
        "roster": [
            {"name": "Rohan Gupta", "student_id": "S1005", "grade": "A"},
            {"name": "Ishita Nair", "student_id": "S1006", "grade": "B+"},
            {"name": "Aarav Sharma", "student_id": "S1001", "grade": "B"},
        ],
    },
    {
        "title": "Distributed Systems",
        "code": "CS403",
        "instructor": "Dr. Meera Iyer",
        "credits": 4,
        "schedule": {"days": ["Monday", "Friday"], "start_time": "14:00",
                     "end_time": "15:30", "room": "C-305"},
        "roster": [
            {"name": "Diya Patel", "student_id": "S1002", "grade": "A"},
            {"name": "Vihaan Joshi", "student_id": "S1007", "grade": "B"},
            {"name": "Ananya Rao", "student_id": "S1004", "grade": "A"},
        ],
    },
    {
        "title": "Cloud Computing",
        "code": "CS404",
        "instructor": "Dr. Anita Desai",
        "credits": 3,
        "schedule": {"days": ["Wednesday"], "start_time": "11:00",
                     "end_time": "13:00", "room": "B-110"},
        "roster": [
            {"name": "Kabir Singh", "student_id": "S1003", "grade": "B+"},
            {"name": "Ishita Nair", "student_id": "S1006", "grade": "A"},
        ],
    },
]


def banner(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main():
    print("=" * 60)
    print("ACTIVITY 3.1 - EMBEDDED COURSE ENROLLMENT SCHEMA")
    print("=" * 60)

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    try:
        client.admin.command("ping")
        print("[OK] Connected to Docker MongoDB")

        db = client["mongodb_activity_3"]
        if "courses" in db.list_collection_names():
            db["courses"].drop()

        # Create the collection WITH validation (Step 2)
        db.create_collection("courses", validator=VALIDATOR)
        courses = db["courses"]
        print("[OK] Created collection mongodb_activity_3.courses "
              "with schema validation")
        print("     Required fields: title, code, instructor, schedule")

        # ----------------------------------------------------------
        # Step 1: insert the course documents
        # ----------------------------------------------------------
        banner("STEP 1 - INSERT COURSES (ROSTER + SCHEDULE EMBEDDED)")
        courses.insert_many(COURSES)
        print(f"[OK] Inserted {courses.count_documents({})} courses")
        for c in courses.find().sort("code", 1):
            s = c["schedule"]
            print(f"  {c['code']} | {c['title']:<30} | {len(c['roster'])} students"
                  f" | {'/'.join(d[:3] for d in s['days'])} {s['start_time']}")

        # ----------------------------------------------------------
        # Step 1: courses that meet on Monday
        # ----------------------------------------------------------
        banner("QUERY - COURSES THAT MEET ON MONDAY")
        for c in courses.find({"schedule.days": "Monday"},
                              {"_id": 0, "code": 1, "title": 1, "schedule": 1}):
            s = c["schedule"]
            print(f"  {c['code']} - {c['title']}")
            print(f"      Days: {', '.join(s['days'])} | "
                  f"{s['start_time']}-{s['end_time']} | Room {s['room']}")

        # ----------------------------------------------------------
        # Step 2: prove the validation works
        # ----------------------------------------------------------
        banner("STEP 2 - SCHEMA VALIDATION TESTS")

        missing_instructor = {
            "title": "Operating Systems", "code": "CS405",
            "schedule": {"days": ["Monday"], "start_time": "08:00",
                         "end_time": "09:00", "room": "A-100"},
        }
        bad_code = {
            "title": "Compilers", "code": "compilers101",
            "instructor": "Dr. Anita Desai",
            "schedule": {"days": ["Friday"], "start_time": "08:00",
                         "end_time": "09:00", "room": "A-100"},
        }
        for label, bad in [("Missing 'instructor'", missing_instructor),
                           ("Invalid code 'compilers101'", bad_code)]:
            try:
                courses.insert_one(bad)
                print(f"[FAIL] {label}: document was accepted")
            except WriteError as e:
                print(f"[OK] {label}: rejected "
                      f"(error code {e.code} - Document failed validation)")

        print(f"Documents in collection after tests: "
              f"{courses.count_documents({})}")

        # ----------------------------------------------------------
        # Step 3: students enrolled in courses taught by an instructor
        # ----------------------------------------------------------
        instructor = "Dr. Meera Iyer"
        banner(f"STEP 3 - STUDENTS TAUGHT BY {instructor.upper()}")

        pipeline = [
            {"$match": {"instructor": instructor}},
            {"$unwind": "$roster"},
            {"$project": {"_id": 0, "course": "$code",
                          "name": "$roster.name",
                          "student_id": "$roster.student_id",
                          "grade": "$roster.grade"}},
            {"$sort": {"course": 1, "name": 1}},
        ]
        print(f"{'Course':<8}{'Student ID':<12}{'Name':<16}Grade")
        print("-" * 44)
        for row in courses.aggregate(pipeline):
            print(f"{row['course']:<8}{row['student_id']:<12}"
                  f"{row['name']:<16}{row['grade']}")

        unique = courses.aggregate([
            {"$match": {"instructor": instructor}},
            {"$unwind": "$roster"},
            {"$group": {"_id": "$roster.student_id",
                        "name": {"$first": "$roster.name"},
                        "courses": {"$push": "$code"}}},
            {"$sort": {"_id": 1}},
        ])
        print("\nUnique students (with the courses they take):")
        for s in unique:
            print(f"  {s['_id']} {s['name']:<14} -> {', '.join(s['courses'])}")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(dumps(list(courses.find()), indent=2))
        print(f"\n[OK] Exported collection to {os.path.basename(OUTPUT_FILE)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
