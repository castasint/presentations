# Medallion Architecture & Databricks Unity Catalog

---

# Part 1: The Foundation
## Understanding Data Lakehouse & Medallion Architecture

---

## Slide 1: The Modern Data Problem

- Organizations generate petabytes of data daily
- Traditional data warehouses: structured-only, expensive at scale
- Data lakes: flexible but lack governance, performance, and reliability
- **The Lakehouse Paradigm**: Best of both worlds
  - Open formats (Delta Lake / Apache Iceberg)
  - ACID transactions
  - Schema enforcement & evolution
  - Cost-effective object storage

> "The lakehouse combines the flexibility of data lakes with the reliability of data warehouses." — Databricks

---

## Slide 2: What is Medallion Architecture?

- A **data design pattern** introduced by Databricks
- Organizes data into three (or more) logical layers
- Each layer represents increasing **quality**, **aggregation**, and **business-readiness**
- Named after Olympic medals: 🥉 Bronze → 🥈 Silver → 🥇 Gold
- Also known as "multi-hop" architecture

**Key Principle**: Data flows progressively from raw ingestion to curated analytics-ready datasets.

---

## Slide 3: Why Medallion Architecture?

| Challenge | How Medallion Solves It |
|-----------|------------------------|
| Raw data quality issues | Isolates dirty data in Bronze |
| Schema drift | Bronze accepts everything; Silver enforces |
| Multiple consumer needs | Gold serves specific use cases |
| Data lineage complexity | Clear hop-by-hop traceability |
| Replay & backfill | Reprocess from any layer |
| Cost optimization | Less expensive storage for raw; compute for curated |

---

## Slide 4: The Three Layers at a Glance

```
┌─────────────────────────────────────────────────────────┐
│  🥇 GOLD LAYER                                          │
│  Business-ready, aggregated, high-performance            │
│  → ML features, BI dashboards, executive reports         │
├─────────────────────────────────────────────────────────┤
│  🥈 SILVER LAYER                                        │
│  Cleaned, conformed, deduplicated                        │
│  → Relational models, master data, validated facts       │
├─────────────────────────────────────────────────────────┤
│  🥉 BRONZE LAYER                                        │
│  Raw ingestion, schema-on-read, historical archive       │
│  → JSON, CSV, Parquet, XML, IoT streams                  │
└─────────────────────────────────────────────────────────┘
```

---

# Part 2: Deep Dive into Each Layer

---

## Slide 5: Bronze Layer — The Landing Zone

**Purpose**: Ingest everything, lose nothing

**Characteristics**:
- **Immutable append-only** storage of raw data
- Schema enforcement: **NONE** (schema-on-read)
- Data formats match source (JSON, Avro, CSV, XML, binary)
- Partitioned typically by `ingestion_date` or `_rescued_data`
- May contain duplicates, nulls, malformed records

**Storage**: Cheapest object storage (S3, ADLS, GCS)

---

## Slide 6: Bronze Layer — Ingestion Patterns

**Batch Ingestion**:
```python
# Auto Loader pattern
spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .load("/mnt/raw/events/") \
  .writeStream \
  .option("mergeSchema", "true") \
  .partitionBy("_ingestion_date") \
  .format("delta") \
  .save("/mnt/bronze/events/")
```

**Streaming Ingestion**:
- Kafka → Bronze
- Kinesis/Event Hubs → Bronze
- IoT Hub → Bronze

---

## Slide 7: Bronze Layer — Schema Evolution

- Raw data sources change schemas frequently
- **`_rescued_data` column**: Catches malformed fields
- `mergeSchema`: Automatically evolves table schema
- `rescuedDataColumn`: Stores unparseable JSON

```python
# Handling schema drift
spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .option("cloudFiles.schemaEvolutionMode", "rescue") \
  .option("rescuedDataColumn", "_rescued_data") \
  .load(source_path)
```

**Golden Rule**: Never reject data at Bronze. Capture everything.

---

## Slide 8: Silver Layer — The Refinery

**Purpose**: Clean, conform, deduplicate, and integrate data

**Characteristics**:
- **Strong schema enforcement**
- Data types corrected and standardized
- Deduplication (often using `MERGE` / Upserts)
- Referential integrity checks
- Business rule validation
- Slowly Changing Dimensions (SCD) Type 1/2

**Storage**: Still object storage, but optimized Delta format

---

## Slide 9: Silver Layer — Transformations

**Typical Operations**:
1. **Cleansing**: Trim strings, handle nulls, standardize dates
2. **Deduplication**: `ROW_NUMBER() OVER (PARTITION BY id ORDER BY timestamp DESC)`
3. **Conforming**: Common units, currency conversion, timezone normalization
4. **Enrichment**: Join with reference data, geocoding
5. **Validation**: Check constraints, referential integrity

```python
# Deduplication pattern
from pyspark.sql import Window
from pyspark.sql.functions import row_number

window_spec = Window.partitionBy("customer_id").orderBy(col("updated_at").desc())

silver_df = bronze_df \
  .filter(col("_rescued_data").isNull()) \
  .withColumn("rn", row_number().over(window_spec)) \
  .filter(col("rn") == 1) \
  .drop("rn", "_rescued_data", "_ingestion_date")
```

---

## Slide 10: Silver Layer — SCD Type 2 Implementation

```python
# Merge (upsert) with SCD Type 2
delta_table.alias("target").merge(
    silver_df.alias("source"),
    "target.customer_id = source.customer_id AND target.is_current = true"
).whenMatchedUpdate(set={
    "is_current": "false",
    "valid_to": "source.updated_at"
}).whenNotMatchedInsert(values={
    "customer_id": "source.customer_id",
    "name": "source.name",
    "email": "source.email",
    "is_current": "true",
    "valid_from": "source.updated_at",
    "valid_to": "null"
}).execute()
```

---

## Slide 11: Gold Layer — The Curated Zone

**Purpose**: Business-ready data optimized for consumption

**Characteristics**:
- **Highly aggregated** and summarized
- **Star schema** or **data vault** models
- Optimized for **query performance**
- Z-ordered and optimized for specific access patterns
- Often materialized views or pre-computed aggregates
- **Row/column-level security** applied

**Consumers**: BI tools, ML platforms, APIs, executive dashboards

---

## Slide 12: Gold Layer — Modeling Patterns

**Star Schema**:
- Fact tables: orders, transactions, events
- Dimension tables: customers, products, dates, regions

**Data Vault 2.0**:
- Hubs: Business keys
- Links: Relationships
- Satellites: Context and history

**Aggregate Tables**:
- Daily/weekly/monthly rollups
- Pre-computed KPIs
- Feature stores for ML

---

## Slide 13: Gold Layer — Performance Optimization

```sql
-- Z-Ordering for efficient filtering
OPTIMIZE gold.fact_orders ZORDER BY (customer_id, order_date);

-- Liquid clustering (Databricks 2024+)
ALTER TABLE gold.fact_orders CLUSTER BY (region, order_date);

-- Generated columns for smart partitioning
CREATE TABLE gold.fact_orders (
  order_timestamp TIMESTAMP,
  order_date DATE GENERATED ALWAYS AS (CAST(order_timestamp AS DATE)),
  ...
) PARTITIONED BY (order_date);
```

---

## Slide 14: The Complete Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Source    │────▶│   Bronze    │────▶│   Silver    │────▶│    Gold     │
│  Systems    │     │   (Raw)     │     │  (Clean)    │     │ (Curated)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
   Kafka, API          Immutable         Deduplicated      Aggregated
   Database            Append-only       Conformed         Modeled
   File Drop           Schema-on-read    SCD Type 2        Optimized
                                           Enriched          Secure
```

---

## Slide 15: Multi-Hop Beyond Three Tiers

**Extended Architecture**:
```
Bronze → Silver → Silver-Aggregated → Gold-Summary → Gold-ML-Features
```

**Specialized Layers**:
- **Platinum/Platinum+**: Real-time serving layer
- **Sandbox**: Data science experimentation
- **Archive**: Long-term cold storage
- **Quarantine**: Failed validation records

> Keep it simple. Three layers solve 80% of use cases.

---

# Part 3: Databricks & Unity Catalog

---

## Slide 16: Databricks Lakehouse Platform

**Unified Platform**:
- **Delta Lake**: Open-source storage layer
- **Apache Spark**: Distributed processing engine
- **MLflow**: Machine learning lifecycle
- **Unity Catalog**: Unified governance

**Key Innovation**: Single copy of data for ALL workloads
- Batch processing
- Streaming analytics
- SQL/BI queries
- Data science & ML
- GenAI / LLM applications

---

## Slide 17: What is Unity Catalog?

- **Unified governance solution** for data and AI
- Built into Databricks
- Manages ALL data assets: tables, volumes, models, notebooks, dashboards
- Cross-workspace and cross-cloud capability
- Based on open Delta Sharing protocol

**Three Pillars**:
1. **Unified Data & AI Asset Management**
2. **Fine-grained Access Control**
3. **Built-in Data Lineage**

---

## Slide 18: Unity Catalog — The Big Picture

```
┌─────────────────────────────────────────────────────────────┐
│                    UNITY CATALOG                              │
│                                                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐    │
│  │  Tables │  │ Volumes │  │ Models  │  │  Functions  │    │
│  │(Managed)│  │ (Files) │  │ (MLflow)│  │  (UDFs)     │    │
│  └─────────┘  └─────────┘  └─────────┘  └─────────────┘    │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Grants    │  │  Lineage    │  │  Delta Sharing      │  │
│  │(ACL/RBAC)   │  │ (End-to-end)│  │ (Open sharing)      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Slide 19: Unity Catalog vs. Legacy Hive Metastore

| Feature | Hive Metastore | Unity Catalog |
|---------|---------------|---------------|
| Governance | Per-workspace | Cross-workspace |
| Storage | External only | Managed + External |
| Security | Table-level | Row + Column-level |
| Lineage | None | Built-in, automatic |
| Sharing | Manual exports | Delta Sharing |
| Data masking | No | Dynamic views |
| Tagging | No | Unity tags & classifications |

---

## Slide 20: Unity Catalog — Key Concepts

**Metastore**: Top-level container for all data assets
- One per region
- Connects to cloud storage (S3, ADLS, GCS)

**Catalog**: Logical namespace
- `prod`, `dev`, `sandbox`, `ml_models`
- Maps to business domains

**Schema/Database**: Collection of tables and views
- `prod.sales`, `prod.finance`

**Table/View**: Data objects
- **Managed**: UC controls storage lifecycle
- **External**: Existing data, UC manages metadata only

---

## Slide 21: Unity Catalog Hierarchy

```
Metastore (us-east-1)
│
├── Catalog: prod
│   ├── Schema: bronze
│   │   ├── Table: raw_events
│   │   ├── Table: raw_customers
│   │   └── Volume: landing_zone
│   │
│   ├── Schema: silver
│   │   ├── Table: dim_customer
│   │   ├── Table: fct_orders
│   │   └── View: customer_360
│   │
│   ├── Schema: gold
│   │   ├── Table: daily_kpis
│   │   ├── Table: churn_features
│   │   └── Model: churn_prediction
│   │
│   └── Schema: ml
│       ├── Model: recommendation_v2
│       └── Feature: customer_ltv
│
└── Catalog: dev
    └── ...
```

---

## Slide 22: Managed vs. External Tables

**Managed Tables**:
```sql
-- Unity Catalog manages the storage lifecycle
CREATE TABLE prod.bronze.events (
  event_id STRING,
  payload STRING,
  event_time TIMESTAMP
);
-- Stored at: s3://uc-bucket/prod/bronze/events/
```

**External Tables**:
```sql
-- You manage storage; UC manages metadata
CREATE EXTERNAL TABLE prod.bronze.events
LOCATION 's3://company-data-lake/raw/events/';
```

**Recommendation**: Use managed tables for medallion layers; external for ingestion zones.

---

## Slide 23: Unity Catalog + Medallion — The Perfect Match

```
┌────────────────────────────────────────────────────────────────┐
│  Unity Catalog Metastore                                        │
│                                                                 │
│  Catalog: prod                                                  │
│  ├── Schema: bronze        <-- Landing zone                     │
│  │   ├── raw_events (managed)                                   │
│  │   ├── raw_transactions (managed)                             │
│  │   └── raw_iot (managed)                                      │
│  │                                                              │
│  ├── Schema: silver        <-- Curated, conformed               │
│  │   ├── dim_customer (managed, SCD2)                           │
│  │   ├── fct_orders (managed, Z-ordered)                        │
│  │   └── dim_product (managed)                                  │
│  │                                                              │
│  └── Schema: gold          <-- Business-ready                   │
│      ├── daily_revenue (managed, optimized)                     │
│      ├── customer_churn_features (managed)                      │
│      └── marketing_attribution (managed)                        │
│                                                                 │
│  Access: Row filtering + Column masking enforced at each layer  │
└────────────────────────────────────────────────────────────────┘
```

---

## Slide 24: Implementing Medallion with Unity Catalog

**Step 1: Create Catalogs and Schemas**
```sql
-- Create production catalog
CREATE CATALOG IF NOT EXISTS prod;
USE CATALOG prod;

-- Create medallion schemas
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
```

**Step 2: Configure Storage Locations**
```sql
-- Bronze: raw, cheap storage
CREATE EXTERNAL LOCATION bronze_location
  URL 's3://datalake-prod/bronze'
  WITH (STORAGE CREDENTIAL aws_credential);
```

---

## Slide 25: Bronze Layer in Unity Catalog

```python
# Auto Loader to UC-managed Delta table
(spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", "/Volumes/prod/bronze/checkpoints/")
  .load("s3://raw-data/events/")
  .writeStream
  .option("checkpointLocation", "/Volumes/prod/bronze/checkpoints/events/")
  .trigger(availableNow=True)
  .table("prod.bronze.raw_events"))
```

**Key Points**:
- Use `.table()` to write directly to Unity Catalog
- Checkpoints stored in UC Volumes
- Schema evolution handled automatically

---

## Slide 26: Silver Layer in Unity Catalog

```sql
-- Create cleaned customer dimension
CREATE OR REPLACE TABLE prod.silver.dim_customer AS
SELECT
  customer_id,
  TRIM(UPPER(first_name)) AS first_name,
  TRIM(UPPER(last_name)) AS last_name,
  REGEXP_REPLACE(email, '%20', '') AS email,
  CAST(created_at AS TIMESTAMP) AS registered_at,
  CURRENT_TIMESTAMP() AS processed_at
FROM prod.bronze.raw_customers
WHERE customer_id IS NOT NULL
  AND email RLIKE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';
```

---

## Slide 27: Gold Layer in Unity Catalog

```sql
-- Create business-ready aggregate
CREATE OR REPLACE TABLE prod.gold.daily_revenue AS
SELECT
  DATE(o.order_date) AS report_date,
  c.region,
  c.customer_segment,
  COUNT(DISTINCT o.order_id) AS order_count,
  SUM(o.revenue) AS total_revenue,
  AVG(o.revenue) AS avg_order_value,
  CURRENT_TIMESTAMP() AS refreshed_at
FROM prod.silver.fct_orders o
JOIN prod.silver.dim_customer c ON o.customer_id = c.customer_id
WHERE o.order_status = 'completed'
GROUP BY ALL;

-- Optimize for BI queries
OPTIMIZE prod.gold.daily_revenue ZORDER BY (report_date, region);
```

---

## Slide 28: Security — Row-Level Security

```sql
-- Create row-filter function
CREATE FUNCTION prod.gold.region_filter(region STRING)
RETURN BOOLEAN
RETURN CASE
  WHEN is_member('admins') THEN TRUE
  WHEN is_member('us_managers') AND region = 'US' THEN TRUE
  WHEN is_member('eu_managers') AND region = 'EU' THEN TRUE
  ELSE FALSE
END;

-- Apply to gold table
ALTER TABLE prod.gold.daily_revenue
SET ROW FILTER prod.gold.region_filter ON (region);
```

**Result**: Users only see rows for their authorized regions.

---

## Slide 29: Security — Column Masking

```sql
-- Create masking function
CREATE FUNCTION prod.gold.mask_email(email STRING)
RETURN STRING
RETURN CASE
  WHEN is_member('pii_access') THEN email
  ELSE CONCAT('***@', SPLIT(email, '@')[1])
END;

-- Apply to sensitive column
ALTER TABLE prod.silver.dim_customer
ALTER COLUMN email SET MASK prod.gold.mask_email;
```

**Result**: Email shows as `***@gmail.com` for unauthorized users.

---

## Slide 30: Data Lineage in Unity Catalog

**Automatic Lineage Capture**:
- Reads and writes tracked automatically
- Visual lineage graph in Databricks UI
- Column-level lineage available
- API-accessible for custom tooling

```
┌──────────────────────────────────────────────────────┐
│                    LINEAGE GRAPH                      │
│                                                        │
│  raw_events ──▶ dim_customer ──┐                       │
│  raw_orders  ──▶ fct_orders ───┼──▶ daily_revenue     │
│  raw_products ──▶ dim_product ──┘                       │
│                                                        │
│  [Click any node to see upstream/downstream]           │
└──────────────────────────────────────────────────────┘
```

---

## Slide 31: Lineage API Example

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Get table lineage
lineage = w.lineage.get_table(
    table_name="prod.gold.daily_revenue",
    include_entity_lineage=True
)

# Upstream tables
for upstream in lineage.upstream_tables:
    print(f"Upstream: {upstream.table_name}")

# Downstream consumers
for downstream in lineage.downstream_tables:
    print(f"Downstream: {downstream.table_name}")
```

---

## Slide 32: Unity Tags & Data Classification

```sql
-- Apply tags for discovery and governance
ALTER TABLE prod.bronze.raw_events
SET TAGS ('pii' = 'false', 'retention' = '90_days', 'domain' = 'events');

ALTER TABLE prod.silver.dim_customer
SET TAGS ('pii' = 'true', 'sensitivity' = 'high', 'owner' = 'data-platform');

-- Query by tags
SELECT * FROM information_schema.tables
WHERE tag_value = 'high' AND tag_name = 'sensitivity';
```

**Use Cases**:
- GDPR/CCPA compliance tracking
- Data retention policies
- Cost allocation by domain

---

## Slide 33: Delta Sharing with Unity Catalog

**Secure Data Sharing**:
```sql
-- Create a share
CREATE SHARE revenue_share;

-- Add tables to share
ALTER SHARE revenue_share ADD TABLE prod.gold.daily_revenue;

-- Create recipient
CREATE RECIPIENT partner_company;

-- Grant access
GRANT SELECT ON SHARE revenue_share TO RECIPIENT partner_company;
```

**Receiver Side** (any Delta Sharing client):
```python
# Pandas, Spark, Power BI, Tableau — all supported
from delta_sharing import load_as_pandas

df = load_as_pandas("profile#share.schema.table")
```

---

## Slide 34: Volumes — Unstructured Data Management

```sql
-- Create volume for raw files
CREATE EXTERNAL VOLUME prod.bronze.landing_zone
LOCATION 's3://datalake-landing/';

-- Use in Python
spark.read.json("/Volumes/prod/bronze/landing_zone/events/")

-- Volume types:
-- 1. Managed: UC controls storage
-- 2. External: You control storage
```

**Use Cases**:
- Raw file landing zones
- Model artifacts
- Checkpoints and logs
- Image/video/audio files for ML

---

## Slide 35: Workflows & Orchestration

**Databricks Jobs for Medallion Pipelines**:
```yaml
# Databricks Asset Bundle (DAB)
resources:
  jobs:
    medallion_pipeline:
      name: "Medallion ETL"
      tasks:
        - task_key: bronze_ingestion
          notebook_task:
            notebook_path: ./bronze/ingest_events
          
        - task_key: silver_transform
          depends_on:
            - task_key: bronze_ingestion
          notebook_task:
            notebook_path: ./silver/transform_customers
          
        - task_key: gold_aggregate
          depends_on:
            - task_key: silver_transform
          notebook_task:
            notebook_path: ./gold/daily_kpis
```

---

## Slide 36: Streaming with Unity Catalog

```python
# Structured Streaming + UC tables
bronze_stream = (spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .load("s3://events/"))

# Bronze to Silver with MERGE (upsert)
(silver_stream = bronze_stream.writeStream
  .foreachBatch(lambda df, batch_id: (
    DeltaTable.forName(spark, "prod.silver.events")
    .alias("t")
    .merge(df.alias("s"), "t.event_id = s.event_id")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
  ))
  .option("checkpointLocation", "/Volumes/prod/checkpoints/silver/")
  .trigger(availableNow=True)
  .start())
```

---

## Slide 37: Monitoring & Quality with Delta Live Tables

**DLT + Unity Catalog Integration**:
```python
import dlt
from pyspark.sql.functions import *

@dlt.table(
  name="bronze.events",
  catalog="prod",
  schema="bronze"
)
def bronze_events():
  return spark.readStream.format("cloudFiles").load("/Volumes/landing/")

@dlt.expect_or_drop("valid_id", "event_id IS NOT NULL")
@dlt.expect_or_drop("valid_timestamp", "event_time IS NOT NULL")
@dlt.table(name="silver.events", catalog="prod", schema="silver")
def silver_events():
  return dlt.read("bronze.events").dropDuplicates(["event_id"])
```

---

## Slide 38: Cost Optimization Strategies

| Layer | Storage | Compute | Optimization |
|-------|---------|---------|-------------|
| Bronze | Standard S3 | Serverless jobs | None (raw) |
| Silver | Standard S3 | Serverless/Classic | OPTIMIZE weekly |
| Gold | Premium/SSD | SQL Warehouses | ZORDER, Liquid Clustering |

```sql
-- Auto-optimize settings
ALTER TABLE prod.gold.daily_revenue
SET TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);

-- Predictive I/O for SQL warehouses
ALTER TABLE prod.gold.daily_revenue
SET TBLPROPERTIES ('delta.enablePredictiveOptimization' = 'true');
```

---

## Slide 39: Best Practices — Naming Conventions

```
{environment}.{layer}.{domain}_{entity}_{type}

Examples:
- prod.bronze.ecommerce_raw_orders
- prod.silver.customer_dim_customer (SCD2)
- prod.silver.sales_fct_order_line
- prod.gold.executive_daily_revenue_kpi
- prod.gold.ml_customer_churn_features

Prefixes:
- dim_ = Dimension table
- fct_ = Fact table
- agg_ = Aggregate table
- stg_ = Staging/intermediate
- raw_ = Raw ingestion
```

---

## Slide 40: Best Practices — Pipeline Design

1. **Idempotency**: Same input = same output. Use `MERGE`, not `INSERT`.
2. **Schema Evolution**: Plan for it at Bronze; enforce at Silver.
3. **Partitioning**: Partition by date for time-series; avoid over-partitioning.
4. **Checkpoints**: Always use external/checkpoint locations for streams.
5. **Testing**: Validate row counts, null rates, and distributions.
6. **Documentation**: Document every table in Unity Catalog comments.

```sql
COMMENT ON TABLE prod.gold.daily_revenue IS 
  'Daily revenue KPIs by region and segment. Refreshed hourly.';
```

---

## Slide 41: Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | The Fix |
|-------------|-------------|---------|
| Direct Bronze → Gold | No data quality, no reuse | Always have Silver |
| Mutating Bronze data | Loses audit trail | Append-only at Bronze |
| Over-partitioning | Too many small files | Partition by date only |
| Hardcoded credentials | Security risk | Use Unity Catalog credentials |
| No data quality checks | Garbage in, garbage out | Use DLT expectations |
| Skipping lineage docs | Compliance nightmare | Leverage automatic UC lineage |

---

## Slide 42: Real-World Architecture Example

```
┌────────────────────────────────────────────────────────────────┐
│                        INGESTION LAYER                          │
│  Kafka │ Kinesis │ Fivetran │ Airbyte │ dbt │ API → S3        │
└────────────────────────┬───────────────────────────────────────┘
                         ▼
┌────────────────────────────────────────────────────────────────┐
│  prod.bronze                      (Auto Loader + UC Tables)     │
│  ├── raw_clicks      (JSON, 5TB, partitioned by _date)         │
│  ├── raw_orders      (Avro, 2TB, partitioned by _date)         │
│  └── raw_iot         (Parquet, 10TB, partitioned by _date)     │
└────────────────────────┬───────────────────────────────────────┘
                         ▼
┌────────────────────────────────────────────────────────────────┐
│  prod.silver                      (Spark + SQL, MERGE/SCD2)     │
│  ├── dim_customer    (SCD Type 2, 50M rows)                    │
│  ├── dim_product     (SCD Type 1, 2M rows)                     │
│  ├── fct_orders      (ZORDER by customer_id, 500M rows)        │
│  └── fct_page_views  (Liquid clustering, 2B rows)              │
└────────────────────────┬───────────────────────────────────────┘
                         ▼
┌────────────────────────────────────────────────────────────────┐
│  prod.gold                        (Aggregated, Secure, Fast)    │
│  ├── daily_kpis         (Tableau, Power BI)                    │
│  ├── customer_ltv       (ML Feature Store)                     │
│  ├── churn_prediction   (MLflow model input)                   │
│  └── marketing_attribution   (Looker, custom API)              │
└────────────────────────────────────────────────────────────────┘
```

---

## Slide 43: Governance at Scale

**Cross-Workspace Unity Catalog**:
```
Workspace A (Data Engineering)
    │
    ├── Creates: prod.bronze.*, prod.silver.*
    └── Grants: SELECT on silver to Workspace B

Workspace B (Data Science)
    │
    ├── Reads: prod.silver.*
    ├── Creates: prod.gold.ml_features
    └── Grants: USE on ml_features to Workspace C

Workspace C (BI/Analytics)
    │
    └── Reads: prod.gold.* (with row/column filters)
```

**Result**: Single source of truth, zero data copies.

---

## Slide 44: Compliance & Auditing

```sql
-- Audit log queries
SELECT
  user_name,
  action_name,
  request_params.table_name,
  event_time
FROM system.access.audit
WHERE action_name IN ('createTable', 'deleteTable', 'commandSubmit')
  AND event_date >= CURRENT_DATE() - INTERVAL 7 DAYS
ORDER BY event_time DESC;

-- Table access history
SELECT
  user_name,
  table_name,
  operation,
  query_start_time
FROM system.access.table_lineage
WHERE table_name = 'prod.gold.daily_revenue';
```

---

## Slide 45: Migration to Unity Catalog

**Migration Path from Hive Metastore**:
```python
# Step 1: Upgrade external tables
spark.sql("""
  SYNC TABLE prod.bronze.events
  FROM hive_metastore.bronze.events
""")

# Step 2: Migrate managed tables
spark.sql("""
  CREATE TABLE prod.silver.customers
  DEEP CLONE hive_metastore.silver.customers
""")

# Step 3: Update pipelines
# Change all references from hive_metastore.* to prod.*
```

**Tools**: UCX (Unity Catalog Migration Toolkit) — open source from Databricks Labs

---

## Slide 46: GenAI & Unity Catalog

**Vector Search Integration**:
```python
from databricks.vector_search.client import VectorSearchClient

client = VectorSearchClient()

# Create vector index on Gold documentation
client.create_delta_sync_index(
  endpoint_name="prod-endpoint",
  index_name="prod.gold.documentation_index",
  source_table_name="prod.gold.knowledge_base",
  pipeline_type="TRIGGERED",
  primary_key="id",
  embedding_vector_column="embedding",
  embedding_source_column="content"
)
```

**Result**: Your medallion data becomes the foundation for RAG applications.

---

## Slide 47: Key Takeaways

1. **Medallion Architecture** provides a structured, layered approach to data quality
2. **Bronze** = raw ingestion, **Silver** = cleansed/conformed, **Gold** = business-ready
3. **Unity Catalog** unifies governance across ALL data and AI assets
4. **Row/column-level security** is automatic and transparent
5. **Lineage** is captured without extra work
6. **Delta Sharing** enables secure cross-organization collaboration
7. **Single copy** of data serves ALL workloads

---

## Slide 48: Resources & Next Steps

**Documentation**:
- Databricks Medallion Architecture Guide
- Unity Catalog Documentation
- Delta Lake Protocol Specification

**Training**:
- Databricks Data Engineer Associate/Professional
- Databricks Platform Administrator

**Tools**:
- UCX: Migration toolkit
- Terraform: Infrastructure as code for UC
- dbt-databricks: Analytics engineering

**Community**:
- Databricks Community Edition (free)
- Delta Lake Slack / GitHub

---

## Slide 49: Summary Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      MEDALLION + UNITY CATALOG                   │
│                                                                  │
│   Sources          Bronze          Silver         Gold           │
│      │               │                │             │            │
│   ┌──┴──┐      ┌────┴────┐     ┌─────┴────┐  ┌─────┴────┐      │
│   │Kafka│─────▶│ UC Table│────▶│ UC Table │─▶│ UC Table │      │
│   │ API │      │  (Raw)  │     │ (Clean)  │  │(Curated) │      │
│   │ S3  │      │Managed  │     │Managed   │  │Managed   │      │
│   └──┬──┘      └────┬────┘     └────┬─────┘  └────┬─────┘      │
│      │              │               │             │             │
│      └──────────────┴───────────────┴─────────────┘             │
│                        Unity Catalog                             │
│                   (Governance + Lineage)                         │
│                                                                  │
│   Security: Row filters │ Column masks │ Tags                   │
│   Sharing: Delta Sharing │ MLflow │ Vector Search               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Slide 50: Q&A

### Thank You!

**Medallion Architecture + Databricks Unity Catalog**

_Building trustworthy, governed, and scalable data platforms._

---

# Appendix

---

## A1: Complete Bronze-to-Gold Code Example

```python
# BRONZE: Auto Loader ingestion
(spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .load("s3://raw/events/")
  .writeStream
  .option("mergeSchema", "true")
  .option("checkpointLocation", "/Volumes/prod/checkpoints/bronze/")
  .toTable("prod.bronze.raw_events"))

# SILVER: Clean and deduplicate
spark.sql("""
  CREATE OR REPLACE TABLE prod.silver.events AS
  SELECT DISTINCT *
  FROM (
    SELECT *,
      ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY _ingestion_time DESC) as rn
    FROM prod.bronze.raw_events
    WHERE event_id IS NOT NULL
  )
  WHERE rn = 1
""")

# GOLD: Business aggregate
spark.sql("""
  CREATE OR REPLACE TABLE prod.gold.daily_metrics AS
  SELECT 
    DATE(event_time) as day,
    event_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users
  FROM prod.silver.events
  GROUP BY ALL
""")

# Optimize
spark.sql("OPTIMIZE prod.gold.daily_metrics ZORDER BY (day, event_type)")
```

---

## A2: Terraform for Unity Catalog Infrastructure

```hcl
resource "databricks_catalog" "prod" {
  name    = "prod"
  comment = "Production catalog for medallion architecture"
}

resource "databricks_schema" "bronze" {
  catalog_name = databricks_catalog.prod.name
  name         = "bronze"
  comment      = "Raw ingestion layer"
}

resource "databricks_schema" "silver" {
  catalog_name = databricks_catalog.prod.name
  name         = "silver"
  comment      = "Cleaned and conformed layer"
}

resource "databricks_schema" "gold" {
  catalog_name = databricks_catalog.prod.name
  name         = "gold"
  comment      = "Business-ready curated layer"
}
```

---

## A3: Checklist for Production Deployment

- [ ] Unity Catalog metastore configured per region
- [ ] Storage credentials and external locations defined
- [ ] Catalogs created: `prod`, `dev`, `sandbox`
- [ ] Schemas created: `bronze`, `silver`, `gold`, `ml`
- [ ] Row-level security functions tested
- [ ] Column masking applied to PII
- [ ] Tags and classifications applied
- [ ] Delta Sharing recipients configured (if needed)
- [ ] Checkpoints stored in UC Volumes
- [ ] Auto-optimize enabled for Gold tables
- [ ] Monitoring and alerting configured
- [ ] Documentation in UC table comments
- [ ] Backup and disaster recovery tested
