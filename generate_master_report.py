import os
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

BASE_DIR = r"D:\mangoDB and no sql"

def generate_master_consolidated_report():
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    def add_para(text, bold=False, size=11, font_name="Times New Roman", space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.bold = bold
        run.font.name = font_name
        run.font.size = Pt(size)
        return p

    # Cover Title
    add_para("NoSQL Databases using MongoDB", bold=True, size=24, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_para("Consolidated Laboratory & Capstone Assignment Report", bold=True, size=16, space_after=20, align=WD_ALIGN_PARAGRAPH.CENTER)

    # Student Card
    add_para("Student Profile & Academic Metadata", bold=True, size=13, space_after=4)
    add_para("Student Name   : Ayush Yadav", bold=True, size=12, space_after=2)
    add_para("USN            : 24BTLCL003", bold=True, size=12, space_after=2)
    add_para("Class / Branch : AIML - B (Artificial Intelligence & Machine Learning)", bold=True, size=12, space_after=2)
    add_para("Course Code    : NoSQL Using MongoDB Laboratory", bold=True, size=12, space_after=2)
    add_para("Scope Covered  : Activities 5 through 18 + Appendix A (Capstone)", bold=True, size=12, space_after=20)

    # Table of Contents Summary
    add_para("Table of Contents / Curriculum Mapping", bold=True, size=14, space_after=8)
    curriculum = [
        ("Activity 5",  "Aggregation Framework and Advanced Querying", "Pipelines, $group, $lookup, $unwind, $facet"),
        ("Activity 6",  "Indexing Strategies & Query Optimization",   "ESR Rule, Compound Indexes, Multikey, explain(), Covered Queries"),
        ("Activity 7",  "Architecture Deep Dive & Data Modeling",     "Embedded vs. Referenced Schemas, Subset Pattern, WiredTiger Sizing"),
        ("Activity 8",  "Replication and High Availability",          "3-Node Replica Set, Election Priority, Failover Observer, Lag"),
        ("Activity 9",  "CAP Theorem in Practice & Consistency",      "Write Concerns (w:1, w:majority, j:true), Network Partitions, Rollback"),
        ("Activity 10", "Multi-Document ACID Transactions",           "Atomic Bank Transfers, Concurrency, Flash-sale Inventory Reservations"),
        ("Activity 11", "Horizontal Scaling & Sharding",              "Shard Key Cardinality, Hotspot Avoidance, Hashed Sharding, Balancer"),
        ("Activity 12", "Security & CIA Triad",                       "Role-Based Access Control (RBAC), Least Privilege, TLS, PII Redaction"),
        ("Activity 13", "Container & Cloud Deployment",               "Production Docker Compose, Volume Persistence, Kubernetes StatefulSets"),
        ("Activity 14", "Production Operations & Diagnostics",        "Real-Time Telemetry Dashboard, Slow Query Profiling, mongodump Backup"),
        ("Activity 15", "Multi-Tenant SaaS Architecture",             "Tenant Data Isolation (Pool vs Silo), Tenant Migrations, JWT Enforcer"),
        ("Activity 16", "Polyglot Persistence",                       "Cross-Model Comparison (Document vs Relational vs Wide vs Graph), Hybrid"),
        ("Activity 17", "Vector Search & Generative AI (RAG)",        "Semantic Vector Embeddings, Cosine Similarity, RAG Prompting, HNSW vs IVF"),
        ("Activity 18", "Comparative Capstone & Synthesis",           "10,000 Txn Fraud Detection Benchmark, Architectural Decision Matrix"),
        ("Appendix A",  "Full-Stack LLM Chat Application Capstone",   "FastAPI RAG Backend, Vector Ingestion, Streamlit UI, Session Memory"),
    ]

    for code, title, focus in curriculum:
        add_para(f"• {code}: {title} — {focus}", size=11, space_after=3)

    add_para("Detailed Experiment Reports", bold=True, size=16, space_after=14)

    # Compile excerpts from each activity
    for code, title, focus in curriculum:
        act_num_str = code.replace("Activity ", "").replace("Appendix ", "")
        add_para(f"{code.upper()} — {title.upper()}", bold=True, size=14, space_after=6)
        add_para(f"Core Concepts Covered: {focus}", bold=False, size=11, space_after=4)

        folder_name = f"24BTLCL003_MongoDB_Activity_{act_num_str}_Submission" if act_num_str != "A" else "24BTLCL003_MongoDB_Appendix_A_Submission"
        folder_path = os.path.join(BASE_DIR, folder_name)

        if os.path.exists(folder_path):
            add_para(f"Deliverable Repository: ./{folder_name}", bold=True, size=11, space_after=4)
            # List files
            items = os.listdir(folder_path)
            for item in items:
                if os.path.isdir(os.path.join(folder_path, item)):
                    add_para(f"  ├── Sub-Activity Folder: {item}", size=10, font_name="Consolas", space_after=2)
                elif item.endswith(".docx"):
                    add_para(f"  └── Formal Submission Document: {item}", bold=True, size=10, font_name="Consolas", space_after=4)

        add_para("-" * 70, size=10, font_name="Consolas", space_after=10)

    out_docx = os.path.join(BASE_DIR, "24BTLCL003_Ayush_Yadav_MongoDB_Consolidated_Master_Report.docx")
    doc.save(out_docx)
    print(f"[OK] Created Master Consolidated Word Document: {out_docx}")

if __name__ == "__main__":
    generate_master_consolidated_report()
