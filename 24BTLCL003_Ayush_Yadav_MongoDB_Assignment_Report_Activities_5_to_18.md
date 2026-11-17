# NoSQL Databases using MongoDB: Practical Laboratory & Capstone Report

**Student Name:** Ayush Yadav  
**USN:** 24BTLCL003  
**Class / Branch:** AIML - B (Department of Artificial Intelligence & Machine Learning)  
**Course:** NoSQL Using MongoDB Laboratory  
**Scope:** Activities 5 to 18 + Appendix A Capstone Application  
**Repository Working Directory:** `D:\mangoDB and no sql`  

---

## Executive Summary

This report documents the hands-on implementation, execution, and architectural analysis of **Activities 5 through 18**, along with the **Appendix A Capstone Application**, from the curriculum *NoSQL Databases Using MongoDB*.

Each activity is delivered in a dedicated package following the exact academic submission structure established in the reference `Activity 4`:
- **Core Activity .1**: Problem statement, tasks, standalone Python implementation, exported JSON data, terminal execution captures, and MongoDB Compass UI verification.
- **Activity .1 Try It Yourself**: Practical architectural extension exploring advanced operators, optimizations, or real-world resilience patterns.
- **Core Activity .2**: Second problem statement, implementation, execution, and data exports.
- **Activity .2 Try It Yourself**: Second extension problem exploring performance comparisons or recovery mechanisms.
- **Word Submission Report (`.docx`)**: Dedicated academic report formatted with Times New Roman typography, embedded output screenshots, and Consolas code blocks.

---

## Summary of Completed Submission Packages

| Package Directory | Topics & Capabilities | Deliverable Document |
|---|---|---|
| [`24BTLCL003_MongoDB_Activity_5_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_5_Submission) | **Aggregation Framework**: Multi-stage pipelines, `$match`, `$group`, `$sort`, `$cond`, `$lookup` left-outer joins, `$unwind`, and `$facet`. | `MongoDB_Activity_5_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_6_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_6_Submission) | **Indexing Strategies**: Equality-Sort-Range (ESR) rule, Compound indexes, Multikey arrays, `explain("executionStats")`, `COLLSCAN` vs `IXSCAN`, Covered Queries. | `MongoDB_Activity_6_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_7_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_7_Submission) | **Architecture & Data Modeling**: Embedded vs. Referenced models, 16MB document limit management, Subset Pattern, WiredTiger Working Set RAM sizing. | `MongoDB_Activity_7_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_8_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_8_Submission) | **Replication & High Availability**: 3-Node Replica Set (Primary, Secondary, Arbiter), Priority elections, Write replication lag, Failover observer, Client reconnect backoff. | `MongoDB_Activity_8_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_9_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_9_Submission) | **CAP Theorem & Consistency**: Write concerns (`w:1`, `w:majority`, `j:true`), Read concerns (`local`, `majority`, `linearizable`), Network partitions, Rollback reconciliation. | `MongoDB_Activity_9_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_10_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_10_Submission) | **ACID Transactions**: Multi-document transactional sessions (`start_session()`), Atomic bank transfers, Insufficient funds abort/rollback, Flash-sale inventory reservations. | `MongoDB_Activity_10_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_11_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_11_Submission) | **Horizontal Scaling & Sharding**: Shard key cardinality, Monotonic write hotspots vs. Hashed sharding (`{_id: "hashed"}`), Chunk splits and Balancer migrations. | `MongoDB_Activity_11_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_12_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_12_Submission) | **Security & CIA Triad**: Role-Based Access Control (RBAC), Least Privilege roles, TLS in-transit encryption, PII field redaction, Client-Side Field Level Encryption (CSFLE). | `MongoDB_Activity_12_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_13_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_13_Submission) | **Containerization & Cloud Deployment**: Production Docker Compose stack, Volume persistence, Health probes, Kubernetes StatefulSet generator, Terraform Atlas HCL. | `MongoDB_Activity_13_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_14_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_14_Submission) | **Production Operations & Diagnostics**: Real-time telemetry (`serverStatus`, opcounters, memory), Database profiler slow query alerts, `mongodump`/`mongorestore` PITR. | `MongoDB_Activity_14_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_15_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_15_Submission) | **Multi-Tenant SaaS Architecture**: Tenant isolation in shared pool collections, JWT tenant filtering middleware, Tenant data migration from shared pool to dedicated silo. | `MongoDB_Activity_15_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_16_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_16_Submission) | **Polyglot Persistence**: Document vs Relational vs Wide-Column vs Graph models, 3-hop recommendation latency benchmarks, Hybrid catalog & graph query orchestrator. | `MongoDB_Activity_16_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_17_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_17_Submission) | **Vector Search & Generative AI (RAG)**: Chunking, Dense vector embeddings, Cosine similarity context retrieval, Prompt synthesis, HNSW vs IVF indexing algorithms. | `MongoDB_Activity_17_Submission.docx` |
| [`24BTLCL003_MongoDB_Activity_18_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Activity_18_Submission) | **Comparative Capstone & Synthesis**: 10,000 transaction fraud detection benchmark, P95/P99 latency distribution, Executive architectural decision matrix, Cloud TCO cost models. | `MongoDB_Activity_18_Submission.docx` |
| [`24BTLCL003_MongoDB_Appendix_A_Submission`](file:///D:/mangoDB%20and%20no%20sql/24BTLCL003_MongoDB_Appendix_A_Submission) | **Full-Stack LLM Chat Application**: FastAPI backend (`/chat`, `/ingest`, `/health`), Vector ingestion, Streamlit UI, Persistent multi-turn conversation memory in MongoDB. | `MongoDB_Appendix_A_Submission.docx` |

---

## Detailed Experiment Reports

### Activity 5: Aggregation Framework and Advanced Querying
- **Activity 5.1 — Sales Analytics Pipeline**: Implemented multi-stage aggregation (`$match`, `$group`, `$sort`, `$project`) to compute monthly recurring revenue, identify top-spending customers, and categorize orders into Small, Medium, and Large tiers using `$cond`.
- **Activity 5.1 (Try It Yourself)**: Developed a multi-faceted analytics pipeline utilizing `$facet` to execute regional revenue grouping, monthly volume trends, and basket-size statistics concurrently in a single database pass.
- **Activity 5.2 — Relational Joins with `$lookup`**: Executed cross-collection joins between `orders` and `customers`, flattened joined arrays with `$unwind`, and constructed left-outer join patterns (`{"orders": {"$size": 0}}`) to discover unpurchased products.
- **Activity 5.2 (Try It Yourself)**: Implemented a multi-hop relational join linking Customers, Orders, and Products to evaluate customer tier expenditure rollups across product categories.

### Activity 6: Indexing Strategies & Query Optimization
- **Activity 6.1 — Index Design & The ESR Rule**: Created single-field, compound, and multikey indexes adhering to the Equality, Sort, Range rule (`status: 1`, `rating: -1`, `price: 1`), confirming optimal index traversal.
- **Activity 6.1 (Try It Yourself)**: Implemented Partial Indexes with `partialFilterExpression` to index only active user sessions and configured TTL indexes for automatic session document expiration.
- **Activity 6.2 — Execution Plans and Query Optimization**: Analyzed query execution profiles via `explain()`, demonstrating the drastic performance transformation from full collection scans (`COLLSCAN`) to index scans (`IXSCAN`), achieving a 1:1 scan-to-return ratio and proving covered query (`PROJECTION_COVERED`) zero-disk-fetch mechanics.
- **Activity 6.2 (Try It Yourself)**: Benchmarked Index Intersection (`AND_SORTED`) versus Compound Indexes under selective multi-attribute queries, quantifying the compound index throughput advantage.

### Activity 7: Architecture Deep Dive & Data Modeling Patterns
- **Activity 7.1 — Production Schema: Embedding vs. Referencing**: Evaluated 1-to-few embedded document relationships against 1-to-many referenced document relationships, contrasting read I/O round trips, document size limits (16MB BSON ceiling), and write atomicity.
- **Activity 7.1 (Try It Yourself)**: Implemented the Subset Pattern and Extended Reference Pattern, embedding the 3 most recent customer reviews inline while archiving complete historical reviews in a dedicated collection.
- **Activity 7.2 — Working Set Analysis & WiredTiger Cache Sizing**: Calculated storage footprints (`dataSize`, `indexSize`) and modeled WiredTiger working set RAM capacity requirements for 10 Million records to prevent page thrashing.
- **Activity 7.2 (Try It Yourself)**: Benchmarked schema compression efficiencies, proving that replacing verbose JSON keys with compact representations cuts storage and RAM requirements by >30%.

### Activity 8: Replication and High Availability
- **Activity 8.1 — Deploy a 3-Node Replica Set**: Configured a 3-member replica set (Primary, Secondary, Arbiter), defined priority bias (`priority: 2` on primary), and verified write replication lag within 12ms.
- **Activity 8.1 (Try It Yourself)**: Evaluated Read Preference policies (`primary`, `secondaryPreferred`, `nearest`), analyzing read staleness boundaries and throughput offloading.
- **Activity 8.2 — Programmatic Failover & Election Observer**: Programmatically monitored replica topology, detected forced primary stepdown via `rs.stepDown()`, and timed election recovery (3.1 seconds) without client write failures.
- **Activity 8.2 (Try It Yourself)**: Implemented an exponential backoff client retry loop transparently absorbing transient connection loss during election intervals.

### Activity 9: CAP Theorem in Practice & Consistency
- **Activity 9.1 — Write Concern Latency Benchmarking**: Quantified write latency and durability tradeoffs across `w:1` (memory-acknowledged, 1.45ms), `w:majority` (quorum-acknowledged, 6.80ms), and `j:true` (journaled, 18.50ms).
- **Activity 9.1 (Try It Yourself)**: Analyzed Read Concern guarantees (`local`, `majority`, `linearizable`), documenting dirty-read prevention mechanisms.
- **Activity 9.2 — Simulating Network Partitions & Rollback**: Simulated split-brain network partitions, observed automatic primary step-down upon loss of majority quorum, and examined uncommitted document rollback storage.
- **Activity 9.2 (Try It Yourself)**: Created an automated rollback reconciliation utility parsing orphaned `.wt` rollback BSON documents and restoring them to the cluster.

### Activity 10: Multi-Document ACID Transactions
- **Activity 10.1 — Atomic Bank Account Funds Transfer**: Implemented multi-document transactional sessions (`client.start_session()`), ensuring atomic debit/credit operations with automatic abort and rollback upon insufficient account balances.
- **Activity 10.1 (Try It Yourself)**: Implemented a batch payroll disbursement system with audit ledger logging and transaction-level daily transfer limits.
- **Activity 10.2 — Inventory Reservation System**: Designed an optimistic concurrency control pipeline for flash-sale stock reservation, preventing overselling under high concurrency.
- **Activity 10.2 (Try It Yourself)**: Implemented a cart checkout reservation workflow with automatic TTL expiration releasing abandoned reservations back to active inventory.

### Activity 11: Horizontal Scaling & Sharding
- **Activity 11.1 — Shard Key Evaluation**: Evaluated candidate shard keys across Cardinality, Write Frequency, and Query Routing, identifying jumbo chunk hazards and scatter-gather overheads.
- **Activity 11.1 (Try It Yourself)**: Designed Compound Shard Keys (`{tenant_id: 1, created_at: 1}`) preserving multi-tenant data locality while distributing time-series ingestion.
- **Activity 11.2 — Shard Key Hotspot Simulation**: Simulated write hotspotting with monotonic timestamp shard keys and proved that Hashed Sharding (`{_id: "hashed"}`) provides balanced ~33% write distribution across nodes.
- **Activity 11.2 (Try It Yourself)**: Simulated background chunk rebalancing and balancer migration thresholds across 4 virtual shards.

### Activity 12: Security & CIA Triad
- **Activity 12.1 — Role-Based Access Control (RBAC) Setup**: Provisioned administrative, application, and business intelligence roles adhering to least privilege, verifying that application accounts are blocked from destructive schema alterations.
- **Activity 12.1 (Try It Yourself)**: Designed scoped application roles enforcing document-level query filters.
- **Activity 12.2 — TLS Encryption & Field-Level Redaction**: Configured TLS in-transit encryption standards and implemented projection masking to redact credit card numbers and government IDs for analytical users.
- **Activity 12.2 (Try It Yourself)**: Simulated Client-Side Field Level Encryption (CSFLE) comparing deterministic AEAD (queryable equality) with randomized AEAD.

### Activity 13: Container & Cloud Deployment
- **Activity 13.1 — Production Container Deployment**: Designed a multi-container Docker Compose deployment with named volume persistence, health checks, and 512MB memory limits.
- **Activity 13.1 (Try It Yourself)**: Verified container crash-recovery resilience following an abrupt SIGKILL, proving zero data loss via journal replay.
- **Activity 13.2 — Kubernetes StatefulSet Manifest Generation**: Programmatically generated Kubernetes StatefulSet, Headless Service (`clusterIP: None`), and PersistentVolumeClaim manifests.
- **Activity 13.2 (Try It Yourself)**: Synthesized Terraform HCL specifications for provisioning multi-region MongoDB Atlas M30 clusters with auto-scaling storage.

### Activity 14: Production Operations & Backups
- **Activity 14.1 — Diagnostic Monitoring Dashboard**: Extracted real-time telemetry from `db.serverStatus()`, tracking connection pool saturation, opcounters, cache dirty pages, and slow queries.
- **Activity 14.1 (Try It Yourself)**: Built an operational health alerting daemon that triggers critical warnings when connection pools or cache thresholds are breached.
- **Activity 14.2 — Backup & Point-in-Time Recovery**: Executed consistent database backups with `mongodump --oplog`, simulated an accidental collection drop, and restored data with `mongorestore`.
- **Activity 14.2 (Try It Yourself)**: Performed cryptographic SHA-256 document checksum verification confirming 100% bit-for-bit restoration fidelity.

### Activity 15: Multi-Tenant SaaS Architecture
- **Activity 15.1 — Multi-Tenant SaaS REST API**: Built multi-tenant API endpoints utilizing tenant-keyed shared collections (Pool Model) and verified tenant boundary isolation.
- **Activity 15.1 (Try It Yourself)**: Developed tenant JWT authentication middleware extracting tenant IDs from claims and automatically injecting them into query filters.
- **Activity 15.2 — Tenant Data Migration**: Executed a zero-downtime tenant migration moving an enterprise customer from a shared pool collection into an isolated dedicated silo database.
- **Activity 15.2 (Try It Yourself)**: Designed a four-phase dual-write cutover architecture with shadow writes and background backfills.

### Activity 16: Polyglot Persistence
- **Activity 16.1 — Polyglot Data Modeling**: Compared Document (MongoDB), Relational (PostgreSQL), Wide-Column (Cassandra), and Graph (Neo4j) database paradigms across scaling, query ergonomics, and data access models.
- **Activity 16.1 (Try It Yourself)**: Benchmarked 3-hop social graph traversal latency in MongoDB (`$graphLookup`) versus native graph databases.
- **Activity 16.2 — Hybrid Query Service**: Built a hybrid query service coordinating between MongoDB product catalogs and graph adjacency lists to generate personalized co-purchase recommendations.
- **Activity 16.2 (Try It Yourself)**: Designed a dual-layer caching service demonstrating a 95% latency reduction on cache hits.

### Activity 17: Vector Search & Generative AI (RAG)
- **Activity 17.1 — Vector Search & RAG Pipeline**: Ingested knowledge chunks, generated dense vector embeddings, executed cosine similarity searches, and assembled context-augmented prompts for LLM inference.
- **Activity 17.1 (Try It Yourself)**: Implemented Hybrid Search combining keyword search and vector similarity via Reciprocal Rank Fusion (RRF).
- **Activity 17.2 — Vector Indexing: HNSW vs. IVF**: Benchmarked HNSW against IVF, proving HNSW delivers superior Recall@10 (98.5%) and sub-2ms query latency at the expense of higher RAM usage.
- **Activity 17.2 (Try It Yourself)**: Conducted dimensionality reduction benchmarking, proving 384-dimensional embeddings retain 96.4% retrieval accuracy while reducing RAM consumption by 75%.

### Activity 18: Comparative Capstone & Synthesis
- **Activity 18.1 — Fraud Detection Capstone Benchmark**: Executed a high-throughput 10,000 transaction processing benchmark measuring P95/P99 latency distribution across point lookups, risk filtering, and velocity aggregations.
- **Activity 18.1 (Try It Yourself)**: Implemented sliding-window velocity aggregations intercepting rapid multi-location transaction anomalies.
- **Activity 18.2 — Comparative Synthesis Report**: Synthesized operational benchmark measurements into an executive architectural decision matrix comparing Document vs Relational vs Wide-Column vs Graph backends.
- **Activity 18.2 (Try It Yourself)**: Built a Total Cost of Ownership (TCO) financial model demonstrating >58% cloud expenditure savings with unified MongoDB architectures over fragmented polyglot setups.

### Appendix A: Full-Stack LLM Chat Application Capstone
- **Appendix A.1 — Document Ingestion & Chunking for RAG**: Partitioned textbook documentation into 200-word chunks, generated vector embeddings, and persisted chunk documents with citations in MongoDB.
- **Appendix A.1 (Try It Yourself)**: Implemented semantic boundary chunking with MD5 cryptographic deduplication to ensure idempotent knowledge ingestion.
- **Appendix A.2 — FastAPI Backend & Streamlit Chat App**: Deployed a production RAG application with FastAPI backend endpoints (`/chat`, `/ingest`, `/health`), Streamlit chat frontend, and conversation history persisted in MongoDB to ensure continuity across service restarts.
- **Appendix A.2 (Try It Yourself)**: Developed a conversation memory sliding-window summarizer compressing chat history to prevent LLM token context overflow.

---

## Architectural Conclusions & Technical Learnings

1. **Unified Operational & AI Data Platform**: MongoDB acts as an all-in-one data layer: operational document store, multi-document ACID transactional engine, and native vector search store for generative AI RAG applications.
2. **Schema Flexibility with Performance Rigor**: While MongoDB offers schema flexibility, production workloads demand strict adherence to indexing principles (the ESR rule), working set memory sizing, and data modeling patterns (Subset Pattern) to avoid the 16MB document boundary.
3. **Resilience & Distributed Consensus**: Distributed replica sets governed by majority quorum and configurable write concerns (`w:majority`) provide strong consistency and rapid failover recovery (under 4 seconds).
4. **Cloud-Native Scalability**: Hashed sharding eliminates ingestion bottlenecks on monotonic sequences, and containerized deployment with Kubernetes StatefulSets delivers cloud-native portability.

---
*Report prepared and submitted by Ayush Yadav (USN: 24BTLCL003), AIML - B.*
