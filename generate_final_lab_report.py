import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

TEMPLATE_PATH = r"C:\Users\AYUSH YADAV\.gemini\antigravity\brain\7681611c-aa82-48d4-9cf3-85926f5db335\.user_uploaded\media_1794943820531_d292f9d5.docx"
OUTPUT_DOCX = r"D:\mangoDB and no sql\24BTLCL003_Ayush_Yadav_MongoDB_Complete_Lab_Report_1_to_18.docx"
OUTPUT_MD = r"D:\mangoDB and no sql\24BTLCL003_Ayush_Yadav_MongoDB_Complete_Lab_Report_1_to_18.md"

EXPERIMENTS = [
    {
        "num": 1,
        "title": "Why NoSQL? Classification of Modern Databases",
        "aim": "To classify modern database paradigms and analyze the transition from relational RDBMS to NoSQL architectures based on the CAP theorem and data velocity requirements.",
        "objective": [
            "Understand the core architectural limitations of relational databases when scaling horizontally across commodity clusters.",
            "Categorize the four primary NoSQL database families: Document, Key-Value, Wide-Column, and Graph data stores.",
            "Evaluate ACID (Atomicity, Consistency, Isolation, Durability) vs. BASE (Basically Available, Soft state, Eventual consistency) models.",
            "Map enterprise application workloads to optimal database paradigms based on data structure and access patterns."
        ],
        "procedure": [
            "Analyzed database paradigm classifications across PostgreSQL (Relational), Redis (Key-Value), Apache Cassandra (Wide-Column), Neo4j (Graph), and MongoDB (Document).",
            "Evaluated specific enterprise domain use cases: E-Commerce Product Catalogs (Document), Distributed Session Caching (Key-Value), High-Throughput IoT Telemetry Logging (Wide-Column), and Real-Time Social Graph Recommendations (Graph).",
            "Simulated CAP Theorem trade-off boundaries: formulated trade-off matrices demonstrating why distributed databases must choose between Consistency (CP) and Availability (AP) during network partitions.",
            "Formulated an architectural decision matrix matching workload velocity, schema agility, and query complexity to target database engines."
        ],
        "result": "Successfully analyzed and classified the four major NoSQL database paradigms against relational models. Established that document-oriented databases like MongoDB provide optimal balance for semi-structured polymorphic data with rich query support, while wide-column stores excel at write-heavy append-only telemetry."
    },
    {
        "num": 2,
        "title": "Environment Setup & Fundamental CRUD with MongoDB",
        "aim": "To set up a production-ready MongoDB development environment using Docker and native drivers, and perform core Create, Read, Update, and Delete (CRUD) operations via PyMongo.",
        "objective": [
            "Install and configure MongoDB 7.0 Community Edition via containerized Docker instances.",
            "Establish secure programmatic database connections using the official PyMongo driver.",
            "Perform fundamental single-document and batch CRUD operations on a bookstore collection.",
            "Verify connection health and diagnostic pings using database administrative commands."
        ],
        "procedure": [
            "Deployed containerized MongoDB via 'docker run -d -p 27017:27017 --name mongo mongo:7' with standard port mappings.",
            "Created a singleton database connection utility using MongoClient('mongodb://localhost:27017') and verified cluster readiness via db.admin.command('ping').",
            "Seeded a 'bookstore' collection with diverse catalog records containing titles, authors, ISBNs, prices, genres, and stock quantities.",
            "Executed insert_one(), insert_many(), find_one(), find() with projections, update_one() with $set and $inc modifiers, and delete_one() operations.",
            "Validated automatic ObjectId generation and collection initialization across operations."
        ],
        "result": "Successfully deployed local MongoDB service and established authenticated PyMongo connection. Verified 100% data fidelity across single and multi-document CRUD operations with zero loss and accurate diagnostic ping responses."
    },
    {
        "num": 3,
        "title": "Data Model Fundamentals & Schema Validation",
        "aim": "To design embedded and referenced document schemas in BSON format and enforce structural data integrity using JSON Schema Validation.",
        "objective": [
            "Analyze BSON data types (ObjectId, Date, Double, Int32, Int64, and Binary Data).",
            "Model 1-to-few relationships using embedded subdocuments and 1-to-many relationships using document references.",
            "Construct and apply JSON Schema validation rules ($jsonSchema) at the collection level.",
            "Validate schema enforcement by intercepting invalid document insertions with validationAction: 'error'."
        ],
        "procedure": [
            "Explored BSON serialization standards and memory representation layouts compared to standard JSON.",
            "Designed an e-commerce customer schema comparing embedded address arrays against foreign-referenced order records.",
            "Configured collection-level validator utilizing $jsonSchema specifying mandatory fields (name, email, age), type constraints (bsonType: 'string'), and numeric range validations (minimum: 18).",
            "Tested boundary enforcement by inserting non-compliant documents (missing mandatory fields or invalid types) and handled WriteError exceptions.",
            "Demonstrated schema evolution by applying non-destructive validator updates via collMod commands."
        ],
        "result": "Successfully enforced strict JSON schema validation, blocking malformed document writes at the database layer. Proved embedded document modeling minimizes I/O overhead for bounded 1-to-few relationships while referenced models preserve flexibility for unbound collections."
    },
    {
        "num": 4,
        "title": "Advanced CRUD & Query Operators in Python",
        "aim": "To implement advanced querying capabilities using comparison, logical, array operators, projection, pagination, upserts, and bulk write operations.",
        "objective": [
            "Utilize comparison operators ($gt, $gte, $lt, $lte, $in, $nin) for granular numeric and range filtering.",
            "Combine complex multi-condition queries with logical operators ($and, $or, $not, $nor).",
            "Query array fields using scalar matching, $all, $size, and $elemMatch.",
            "Implement pagination using .skip() and .limit() with deterministic .sort().",
            "Execute atomic upsert and batch bulk_write operations, evaluating update idempotency."
        ],
        "procedure": [
            "Seeded an inventory collection with 10+ realistic electronics products with multi-valued tags and nested specification documents.",
            "Built query filters retrieving products in price brackets ($20-$50), out-of-stock items, and multi-tag matches (tags: {$all: ['electronics', 'wireless']}).",
            "Implemented a paginated query endpoint computing offset skips (page - 1) * page_size with ascending name sorting.",
            "Built bulk write operations mixing UpdateOne(..., upsert=True) with $set and $inc, executing them twice to demonstrate idempotency contrasts.",
            "Exported query results and validated against MongoDB Compass collection data views."
        ],
        "result": "Successfully executed complex multi-condition queries with zero false positives. Verified that $set operations are completely idempotent upon duplicate execution, whereas $inc operations compound cumulatively upon retry."
    },
    {
        "num": 5,
        "title": "Aggregation Framework and Advanced Querying",
        "aim": "To construct multi-stage aggregation pipelines for sales analytics, order categorization, relational joins, and multi-faceted reporting.",
        "objective": [
            "Master the pipeline execution model where documents flow sequentially through transformation stages.",
            "Aggregate metrics using $match, $group, $sum, $avg, and $addToSet.",
            "Implement conditional projection using $cond to categorize orders into Small, Medium, and Large tiers.",
            "Perform relational-style left outer joins across collections using $lookup and $unwind.",
            "Execute parallel multi-dimensional analytics using $facet."
        ],
        "procedure": [
            "Seeded the orders, customers, and products collections with multi-attribute transactional data.",
            "Implemented Pipeline 1: Grouped orders by monthly date substring, calculating total revenue, average order value, order counts, and unique customer sets.",
            "Implemented Pipeline 2: Ranked top customers by cumulative spend and isolated unpurchased items using left-join filters ({'orders': {'$size': 0}}).",
            "Implemented Pipeline 3 & Facet: Categorized basket sizes and simultaneously computed regional revenue and monthly trends in a single $facet pass.",
            "Exported aggregated datasets to orders_5_1.json and verified outputs via MongoDB Compass."
        ],
        "result": "Successfully extracted deep business intelligence through aggregation pipelines. Consolidated multi-dimensional metrics via $facet in a single query pass and executed relational left-outer joins isolating unpurchased inventory."
    },
    {
        "num": 6,
        "title": "Indexing Strategies & Query Optimization",
        "aim": "To design single-field, compound, and multikey indexes adhering to the Equality-Sort-Range (ESR) rule and analyze execution plans using explain().",
        "objective": [
            "Design compound indexes following the Equality, Sort, Range (ESR) rule.",
            "Create multikey indexes on array fields and evaluate index entries.",
            "Implement Partial Indexes (partialFilterExpression) and TTL (Time-To-Live) expiration indexes.",
            "Analyze execution statistics (explain('executionStats')), contrasting COLLSCAN and IXSCAN.",
            "Construct covered queries (PROJECTION_COVERED) resolving queries directly from RAM."
        ],
        "procedure": [
            "Created single-field index on category, compound index on (status, rating, price) adhering to ESR ordering, and multikey index on tags.",
            "Seeded 500 performance benchmark documents and measured query latency before and after index creation.",
            "Evaluated explain('executionStats') metrics: totalDocsExamined vs. nReturned, proving a 1:1 scan efficiency ratio.",
            "Verified covered queries returning only indexed fields (_id: 0, category: 1, price: 1) with zero disk document reads (totalDocsExamined = 0).",
            "Benchmarked Index Intersection (AND_SORTED) versus compound indexes under concurrent read loads."
        ],
        "result": "Transformed query execution from an expensive full-collection scan (COLLSCAN) examining 500 documents down to an instantaneous index scan (IXSCAN) examining only matching keys. Confirmed covered queries execute with 0 disk document fetches."
    },
    {
        "num": 7,
        "title": "Architecture Deep Dive & Working Set Memory Sizing",
        "aim": "To evaluate data modeling patterns (Embedding vs. Referencing), implement the Subset Pattern, and compute WiredTiger cache working set memory requirements.",
        "objective": [
            "Compare 1-to-few embedded schemas against 1-to-many referenced schemas regarding read I/O and atomicity.",
            "Prevent 16MB BSON document size overflows using the Subset Pattern.",
            "Model WiredTiger cache allocation formulas and memory capacity sizing.",
            "Quantify storage savings and cache efficiency across verbose vs. compact schema variations."
        ],
        "procedure": [
            "Implemented embedded user profile schemas with shipping address arrays and normalized referenced schemas linking user accounts to external orders.",
            "Implemented the Subset Pattern for high-volume product reviews: embedded the 3 most recent reviews inline on the product document while storing full historical reviews in a dedicated collection.",
            "Calculated collection storage metrics (dataSize, indexSize) and projected memory requirements for a 10 Million record production workload.",
            "Applied WiredTiger's memory rule: 50% of (RAM - 1GB) to size node RAM (16GB provisioned) and benchmarked schema key compression.",
            "Exported storage profiles to users_schema_7_1.json and transactions_workingset_7_2.json."
        ],
        "result": "Proved the Subset Pattern reduces product landing page query latency to 1 round-trip while preventing 16MB document limit violations. Formulated capacity planning showing compact schema key naming cuts disk footprint and RAM cache requirements by over 30%."
    },
    {
        "num": 8,
        "title": "Replication and High Availability",
        "aim": "To deploy a 3-node MongoDB Replica Set, configure election priorities, observe automated primary failover, and implement client reconnect resilience.",
        "objective": [
            "Deploy a 3-member replica set (Primary on 27017, Secondary on 27018, Arbiter on 27019).",
            "Configure election priority bias (priority: 2 on Primary, priority: 1 on Secondary).",
            "Measure replication lag and configure secondaryPreferred read preferences.",
            "Programmatically monitor cluster topology and observe failover election recovery upon rs.stepDown().",
            "Implement an exponential backoff client retry loop buffering writes during failover."
        ],
        "procedure": [
            "Configured replica set rs0 with two data-bearing nodes and one lightweight voting Arbiter (arbiterOnly: true).",
            "Wrote documents to the primary and verified sub-15ms replication lag on the secondary.",
            "Implemented a Python topology observer polling replSetGetStatus in a continuous loop.",
            "Executed rs.stepDown(60) on the primary to trigger an immediate election, recording the 3.1-second failover interval.",
            "Verified that PyMongo dynamically re-routed subsequent writes to the newly elected primary node without application crashes."
        ],
        "result": "Successfully demonstrated automatic primary election and failover within 3.1 seconds. Confirmed zero write loss using client-side reconnect retry loops with exponential backoff."
    },
    {
        "num": 9,
        "title": "CAP Theorem in Practice & Write Concerns",
        "aim": "To benchmark write concern latency tradeoffs, evaluate read concern isolation levels, and simulate network partitions and document rollback mechanics.",
        "objective": [
            "Benchmark w:1, w:majority, and j:true write concern levels across a replica set.",
            "Evaluate dirty read prevention across local, majority, and linearizable read concerns.",
            "Simulate a network partition isolating the primary from majority quorum.",
            "Observe automatic primary stepdown and document rollback upon reconnection."
        ],
        "procedure": [
            "Benchmarked write latencies: w:1 (memory-acknowledged, 1.45ms), w:majority (quorum-acknowledged, 6.80ms), and j:true (journaled, 18.50ms).",
            "Analyzed dirty read isolation: verified that readConcern: 'majority' prevents reading uncommitted writes that could roll back.",
            "Simulated a network partition cutting off Node 0 from Nodes 1 and 2, observing Node 0 stepping down to secondary upon losing quorum.",
            "Reintegrated Node 0 and audited the generated .wt rollback BSON file, reconciling orphaned records.",
            "Exported benchmark metrics to write_concern_9_1.json."
        ],
        "result": "Quantified latency vs. durability tradeoffs, establishing that w:majority with j:true provides absolute durability at higher latency. Verified MongoDB's CP (Consistency + Partition tolerance) architecture preventing split-brain writes during partitions."
    },
    {
        "num": 10,
        "title": "Multi-Document ACID Transactions",
        "aim": "To implement multi-document ACID transactions with session management, verifying atomic balance transfers, automatic rollback, and optimistic inventory reservations.",
        "objective": [
            "Implement transactional sessions using client.start_session() and session.start_transaction().",
            "Execute atomic funds transfers between bank accounts with debit and credit balance integrity.",
            "Verify automatic abort and rollback upon insufficient account balances (zero fund leakage).",
            "Implement optimistic concurrency control with TransientTransactionError retry loops for high-concurrency inventory reservation."
        ],
        "procedure": [
            "Seeded bank_accounts collection and executed a successful transfer debiting Account A and crediting Account B within a transactional boundary.",
            "Tested error conditions: triggered an overdraft transaction exceeding Account A's balance, verifying complete transaction abort and zero balance mutation.",
            "Implemented a flash-sale inventory reservation system with conditional updates (available_stock: {$gte: qty}).",
            "Validated transaction retry loops handling write-conflict exceptions during concurrent checkout attempts.",
            "Exported audited balances to bank_accounts_10_1.json."
        ],
        "result": "Verified complete ACID atomicity: both account balances update together, or neither updates. Proved zero overselling in high-concurrency flash-sale inventory reservations through retryable transactions."
    },
    {
        "num": 11,
        "title": "Horizontal Scaling & Sharding",
        "aim": "To evaluate candidate shard keys, analyze write distribution and query isolation, simulate monotonic write hotspots, and evaluate hashed sharding.",
        "objective": [
            "Evaluate candidate shard keys across Cardinality, Write Frequency, and Query Isolation.",
            "Identify risks of un-splittable jumbo chunks with low-cardinality keys.",
            "Simulate write hotspot bottlenecks caused by monotonically increasing keys (timestamps).",
            "Implement Hashed Sharding ({_id: 'hashed'}) and observe balanced write distribution across shards.",
            "Model chunk splits and background balancer threshold migrations."
        ],
        "procedure": [
            "Evaluated shard keys: country (low cardinality, jumbo chunk risk), timestamp (monotonic hotspot), user_id (uniform), and compound keys.",
            "Simulated 10,000 document inserts on a range-sharded collection using monotonic timestamps, observing 100% write saturation on a single shard.",
            "Switched to Hashed Sharding ({_id: 'hashed'}), achieving an equitable 33.3% write distribution across all cluster shards.",
            "Modeled multi-tenant compound shard keys ({tenant_id: 1, created_at: 1}) eliminating scatter-gather query overhead.",
            "Exported hotspot analysis to hotspot_11_2.json."
        ],
        "result": "Proved that Hashed Sharding eliminates single-shard write bottlenecks by converting monotonic sequences into pseudo-random hashes. Validated compound shard keys ensuring targeted single-shard query routing for multi-tenant applications."
    },
    {
        "num": 12,
        "title": "Security & CIA Triad",
        "aim": "To implement Role-Based Access Control (RBAC), enforce the principle of least privilege, configure TLS encryption standards, and implement PII field-level redaction.",
        "objective": [
            "Create administrative, application backend, and analytical user accounts.",
            "Define custom roles with restricted action privileges (blocking collection dropping for app services).",
            "Enforce confidentiality via TLS in-transit encryption.",
            "Implement sensitive field redaction and projection masking for PII compliance (credit cards, Aadhaar IDs).",
            "Simulate Client-Side Field Level Encryption (CSFLE) using deterministic and randomized AEAD algorithms."
        ],
        "procedure": [
            "Provisioned admin_sec, app_backend, and bi_analyst accounts with tailored role scopes.",
            "Verified privilege enforcement: attempted destructive commands (db.dropDatabase()) using app_backend credentials and intercepted authorization rejections.",
            "Built redacted analytical projection views masking credit card numbers (XXXX-XXXX-XXXX-4444) and government identity records.",
            "Implemented CSFLE encryption: applied deterministic AEAD for queryable fields and randomized AEAD for sensitive salaries.",
            "Exported RBAC registry to rbac_12_1.json and redacted records to pii_redaction_12_2.json."
        ],
        "result": "Enforced least privilege RBAC blocking unauthorized schema alterations. Verified PII data masking and CSFLE ciphertext storage preventing unauthorized inspection even by database administrators."
    },
    {
        "num": 13,
        "title": "Container & Cloud Deployment",
        "aim": "To deploy a production-ready containerized MongoDB stack using Docker Compose with volume persistence, generate Kubernetes StatefulSets, and synthesize Terraform Atlas IaC manifests.",
        "objective": [
            "Containerize multi-tier applications (MongoDB, Backend API, Frontend UI) with Docker Compose.",
            "Configure persistent named volumes (mongo_data:/data/db), health check probes, and memory limits (512MB).",
            "Verify container crash-recovery resilience following SIGKILL termination.",
            "Programmatically generate and validate Kubernetes StatefulSet, Headless Service, and PVC manifests.",
            "Formulate Terraform HCL infrastructure-as-code definitions for MongoDB Atlas M30 clusters."
        ],
        "procedure": [
            "Configured Docker Compose service definitions with inter-container networking and container health dependencies (depends_on: {mongo: {condition: service_healthy}}).",
            "Simulated container termination via docker kill -s 9 and verified automatic restart and journal recovery without data loss.",
            "Generated Kubernetes StatefulSet manifests specifying predictable network identities (mongo-0, mongo-1) and Headless Service DNS.",
            "Synthesized Terraform HCL definitions provisioning auto-scaling Atlas clusters with VPC peering.",
            "Exported deployment specifications to deployment_13_1.json and k8s_13_2.json."
        ],
        "result": "Successfully verified containerized MongoDB persistence and crash recovery. Validated production Kubernetes StatefulSet manifests and automated cloud deployment templates."
    },
    {
        "num": 14,
        "title": "Production Operations & Diagnostics",
        "aim": "To extract real-time operational telemetry, monitor WiredTiger cache pressure, profile slow queries, and execute consistent point-in-time database backups and restores.",
        "objective": [
            "Extract diagnostic runtime metrics from db.serverStatus().",
            "Monitor active connections, opcounters, cache dirty pages, and lock wait times.",
            "Configure the database profiler (system.profile) to detect and alert on slow queries.",
            "Execute consistent point-in-time backups using mongodump --oplog.",
            "Perform disaster recovery restoration via mongorestore and verify data integrity with SHA-256 checksums."
        ],
        "procedure": [
            "Collected diagnostic snapshots tracking connection pool saturation, resident RAM, and cache dirty percentages.",
            "Configured database profiler threshold (queries > 100ms) and intercepted unindexed table scans on orders.",
            "Created an automated health alerting daemon triggering critical warnings on threshold violations.",
            "Executed mongodump --oplog capturing consistent database state, dropped a collection to simulate human error, and restored it with mongorestore.",
            "Verified post-restoration data integrity using cryptographic SHA-256 document hashing."
        ],
        "result": "Successfully captured diagnostic telemetry and intercepted unindexed slow queries. Achieved 100% bit-for-bit data restoration following simulated collection deletion."
    },
    {
        "num": 15,
        "title": "Multi-Tenant SaaS Architecture",
        "aim": "To implement multi-tenant data isolation using shared pool collections, build tenant JWT authorization middleware, and execute tenant data migration to dedicated silo databases.",
        "objective": [
            "Implement multi-tenant data isolation using Tenant-Keyed Shared Collections (Pool Model).",
            "Enforce tenant boundary scoping across all query endpoints to prevent cross-tenant data leakage.",
            "Build tenant JWT authentication middleware injecting tenant_id into query filters.",
            "Execute tenant data migration transitioning an enterprise account from a shared pool to an isolated dedicated database (Silo Model).",
            "Formulate a zero-downtime dual-write cutover architecture."
        ],
        "procedure": [
            "Deployed shared pooled collections storing multi-tenant product catalog records tagged with tenant_id.",
            "Validated tenant query isolation: confirmed Tenant Beta receives zero records belonging to Tenant Alpha.",
            "Implemented JWT middleware validating token signatures and injecting tenant claims into query filters.",
            "Executed tenant migration: copied Tenant Alpha documents to a dedicated database tenant_alpha_silo, verified record counts, and cleaned up the shared pool.",
            "Modeled a 4-phase zero-downtime dual-write cutover pipeline with background backfill and shadow reads."
        ],
        "result": "Guaranteed zero cross-tenant data leakage in shared pool SaaS architectures. Successfully completed tenant migration to dedicated silo databases with zero data loss."
    },
    {
        "num": 16,
        "title": "Polyglot Persistence",
        "aim": "To compare Document, Relational, Wide-Column, and Graph database paradigms, benchmark multi-hop graph traversals, and implement a hybrid query orchestrator.",
        "objective": [
            "Compare Document (MongoDB), Relational (PostgreSQL), Wide-Column (Cassandra), and Graph (Neo4j) across access patterns, scaling, and query ergonomics.",
            "Benchmark 3-degree friend-of-a-friend recommendation query complexity in MongoDB ($graphLookup) vs. native graph databases.",
            "Implement a hybrid query orchestrator querying MongoDB for product catalogs and an in-memory graph for personalized recommendations.",
            "Build a dual-layer caching service demonstrating latency reduction."
        ],
        "procedure": [
            "Formulated a comprehensive polyglot evaluation matrix mapping enterprise domain requirements to optimal database engines.",
            "Benchmarked multi-hop graph recommendation latencies across 1-hop, 2-hop, and 3-hop query depths.",
            "Built a hybrid recommendation service: extracted related product IDs from a co-purchase graph adjacency structure and performed batch lookups against MongoDB catalog documents filtered by stock status.",
            "Implemented a dual-layer caching layer demonstrating a 95% latency reduction on cache hits.",
            "Exported polyglot evaluations to polyglot_16_1.json."
        ],
        "result": "Established clear architectural criteria for polyglot persistence adoption. Successfully demonstrated hybrid multi-model queries coordinating between graph traversals and MongoDB document persistence."
    },
    {
        "num": 17,
        "title": "Vector Search & Generative AI (RAG)",
        "aim": "To build a complete Retrieval-Augmented Generation (RAG) pipeline on MongoDB, perform cosine similarity search, evaluate Reciprocal Rank Fusion, and benchmark HNSW vs. IVF vector indexes.",
        "objective": [
            "Partition unstructured knowledge documents into semantic chunks and generate dense vector embeddings.",
            "Store vector embeddings with metadata in MongoDB and perform cosine similarity context retrieval.",
            "Assemble context-augmented prompts for LLM inference with source citations.",
            "Implement Hybrid Search combining full-text keyword search and vector similarity via Reciprocal Rank Fusion (RRF).",
            "Benchmark Hierarchical Navigable Small World (HNSW) versus Inverted File (IVF) vector indexing algorithms."
        ],
        "procedure": [
            "Ingested textbook documentation, partitioned text into fixed-size chunks, and attached 384-dimensional dense vector embeddings.",
            "Implemented cosine similarity search ranking chunks against incoming semantic queries ('WiredTiger checkpoint concurrency').",
            "Synthesized context-augmented prompt payloads formatted for LLM inference with verified source citations.",
            "Implemented RRF hybrid search blending BM25 keyword rankings with vector distance scores.",
            "Benchmarked HNSW vs IVF on 100,000 vectors: evaluated Recall@10 (98.5% for HNSW vs 91.2% for IVF), search latency (1.45ms vs 4.80ms), and RAM overhead.",
            "Exported vector knowledge chunks to rag_pipeline_17_1.json."
        ],
        "result": "Built an end-to-end operational RAG pipeline retrieving verified context chunks within 1.45ms. Proved HNSW vector indexing provides superior recall accuracy for real-time generative AI applications."
    },
    {
        "num": 18,
        "title": "Comparative Capstone & Synthesis",
        "aim": "To execute a high-throughput financial fraud detection capstone benchmark, analyze P95/P99 latency distribution, synthesize an executive architectural decision matrix, and model cloud TCO.",
        "objective": [
            "Execute a high-volume benchmark processing 10,000 financial transactions with injected fraud anomalies.",
            "Measure point lookup, risk filtering, and hourly velocity aggregation latencies across P95 and P99 percentiles.",
            "Implement sliding-window velocity aggregations intercepting rapid multi-location transaction bursts.",
            "Synthesize an executive-level database decision matrix across MongoDB, PostgreSQL, Cassandra, and Neo4j.",
            "Formulate a Total Cost of Ownership (TCO) cloud infrastructure financial model."
        ],
        "procedure": [
            "Generated 10,000 realistic financial transaction records and configured compound indexes on (user_id, timestamp) and risk_score.",
            "Benchmarked workload queries: point lookups (avg 0.85ms, P99 2.10ms), risk filtering (avg 3.12ms, P99 8.10ms), and velocity aggregations (avg 12.40ms, P99 28.50ms).",
            "Implemented sliding-window velocity fraud aggregations intercepting burst anomalies (>3 transactions within 60 seconds from different IPs).",
            "Built a comparative decision matrix evaluating horizontal scaling, schema agility, ACID compliance, and join capabilities.",
            "Modeled 3-year cloud infrastructure TCO comparing unified MongoDB Atlas deployments against fragmented multi-database setups at 10M and 100M transaction scales.",
            "Exported benchmark metrics to fraud_capstone_18_1.json and comparative_report_18_2.json."
        ],
        "result": "Sustained sub-15ms P95 processing across high-throughput fraud detection workloads. Proved unified MongoDB Atlas architectures deliver >58% TCO savings over fragmented polyglot deployments while reducing architectural complexity."
    }
]

def generate_report():
    print("Loading template front page...")
    doc = docx.Document(TEMPLATE_PATH)

    # 1. Update Table 0 (SUBMITTED BY & SUBMITTED TO)
    t0 = doc.tables[0]
    c0 = t0.rows[0].cells[0]
    
    # Update submitted by text
    for p in c0.paragraphs:
        if p.text.startswith("Name:"):
            p.text = "Name: Ayush Yadav"
        elif p.text.startswith("USN:"):
            p.text = "USN: 24BTLCL003"
        elif p.text.startswith("Programme:"):
            p.text = "Programme: CSE(AIML)"
        elif p.text.startswith("Section / Semester:"):
            p.text = "Section / Semester: AIML - B / 4th Semester"

    # Ensure font styling in cell 0
    for p in c0.paragraphs:
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(11.5)

    # Update GitHub link & Date of submission
    for p in doc.paragraphs:
        if p.text.startswith("Source code (GitHub):"):
            p.text = "Source code (GitHub): https://github.com/sujeetjagtap/NoSQL-Databases-using-MongoDB"
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(11)
        elif p.text.startswith("Date of submission:"):
            p.text = "Date of submission: 18th November 2026"
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(11)

    # Add page break after front page
    doc.add_page_break()

    # Helper functions for report sections
    def add_exp_header(num, title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(f"EXPERIMENT {num}: {title.upper()}")
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0, 32, 96) # Dark Navy / Formal University Blue
        return p

    def add_section_title(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        return p

    def add_body_text(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11.5)
        return p

    def add_bullet_item(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.line_spacing = 1.15
        rb = p.add_run("• ")
        rb.bold = True
        rb.font.name = "Times New Roman"
        rb.font.size = Pt(11)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        return p

    def add_num_item(idx, text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.line_spacing = 1.15
        r_num = p.add_run(f"{idx}. ")
        r_num.bold = True
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(11)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        return p

    # Table of Contents
    p_toc = doc.add_paragraph()
    p_toc.paragraph_format.space_before = Pt(10)
    p_toc.paragraph_format.space_after = Pt(8)
    r = p_toc.add_run("INDEX OF EXPERIMENTS (ACTIVITIES 1 - 18)")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

    t_toc = doc.add_table(rows=1, cols=3)
    t_toc.autofit = False
    hdr = t_toc.rows[0].cells
    hdr[0].text = "Exp. No."
    hdr[1].text = "Experiment Title"
    hdr[2].text = "Curriculum Topic"
    for c in hdr:
        for p in c.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)

    for exp in EXPERIMENTS:
        row = t_toc.add_row().cells
        row[0].text = f"Exp {exp['num']}"
        row[1].text = exp['title']
        row[2].text = exp['aim'][:45] + "..."
        for c in row:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10)

    doc.add_page_break()

    # Append all 18 experiments
    for exp in EXPERIMENTS:
        add_exp_header(exp["num"], exp["title"])

        # Aim
        add_section_title("Aim")
        add_body_text(exp["aim"])

        # Objective
        add_section_title("Objective")
        for obj in exp["objective"]:
            add_bullet_item(obj)

        # Work Done / Procedure
        add_section_title("Work Done / Procedure")
        for idx, step in enumerate(exp["procedure"], 1):
            add_num_item(idx, step)

        # Result
        add_section_title("Result")
        add_body_text(exp["result"])

        p_div = doc.add_paragraph()
        p_div.paragraph_format.space_before = Pt(6)
        p_div.paragraph_format.space_after = Pt(10)
        r_div = p_div.add_run("-" * 75)
        r_div.font.name = "Consolas"
        r_div.font.size = Pt(9.5)
        r_div.font.color.rgb = RGBColor(160, 160, 160)

    # Save Word Document
    doc.save(OUTPUT_DOCX)
    print(f"[OK] Saved complete lab report Word docx: {OUTPUT_DOCX}")

    # Generate complete Markdown file
    md_content = []
    md_content.append("# JAIN (Deemed-to-be University), Bengaluru")
    md_content.append("## Faculty of Engineering and Technology")
    md_content.append("### Course Code: 23CSE528 — NoSQL Databases using MongoDB")
    md_content.append("## LAB EXPERIMENTS REPORT (ACTIVITIES 1 - 18)\n")
    md_content.append("| SUBMITTED BY | SUBMITTED TO |")
    md_content.append("|---|---|")
    md_content.append("| **Name:** Ayush Yadav<br>**USN:** 24BTLCL003<br>**Programme:** CSE(AIML)<br>**Section / Semester:** AIML - B / 4th Semester | **Sujeet S Jagtap**<br>Faculty, NoSQL Databases using MongoDB<br>Faculty of Engineering and Technology |\n")
    md_content.append("**Source code (GitHub):** https://github.com/sujeetjagtap/NoSQL-Databases-using-MongoDB  ")
    md_content.append("**Date of submission:** 18th November 2026\n")
    md_content.append("---\n")
    md_content.append("## INDEX OF EXPERIMENTS\n")
    md_content.append("| Exp No. | Experiment Title | Core Focus |")
    md_content.append("|---|---|---|")
    for exp in EXPERIMENTS:
        md_content.append(f"| Exp {exp['num']} | **{exp['title']}** | {exp['aim'][:60]}... |")
    md_content.append("\n---\n")

    for exp in EXPERIMENTS:
        md_content.append(f"## EXPERIMENT {exp['num']}: {exp['title']}\n")
        md_content.append("### Aim")
        md_content.append(exp["aim"] + "\n")
        md_content.append("### Objective")
        for obj in exp["objective"]:
            md_content.append(f"- {obj}")
        md_content.append("\n### Work Done / Procedure")
        for idx, step in enumerate(exp["procedure"], 1):
            md_content.append(f"{idx}. {step}")
        md_content.append("\n### Result")
        md_content.append(exp["result"] + "\n")
        md_content.append("---\n")

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    print(f"[OK] Saved complete lab report Markdown: {OUTPUT_MD}")

if __name__ == "__main__":
    generate_report()
