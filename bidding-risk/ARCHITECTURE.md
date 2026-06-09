# Bid Risk Intelligence Platform — Solution Architecture

## 1. Executive Summary

An end-to-end AI platform that ingests bidding documents from SharePoint, extracts structured data from flexible PDF quotation tables, and performs multi-layer analysis:

| Capability | Description |
|-----------|-------------|
| **Data Ingestion** | Connects to SharePoint Online via Microsoft Graph API; crawls bid folders recursively |
| **Document Understanding** | OCR + table extraction from PDF quotes; parses email PDFs; reads Excel summaries |
| **Structured Storage** | Normalizes flexible supplier tables into a unified schema; vectorizes for semantic search |
| **Risk Analysis** | Price variance, deadline, documentation, supplier concentration risks |
| **Collusion Detection** | Identical prices, bid rotation, complementary bidding, shared indicators, price correlation |
| **Anomaly Detection** | Statistical outliers, Benford's Law deviations, time-series anomalies |
| **Compliance Engine** | Validates folder structure, required documents, approval workflows, field completeness |
| **LLM Intelligence** | Summarization, Q&A over bid documents, natural language risk explanations |
| **API & Dashboard** | REST API + frontend for analysts to query, visualize, and drill down |

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SHAREPOINT ONLINE                                  │
│  Bid Folder Structure:                                                      │
│  ├── Bid_2024_001/                                                          │
│  │   ├── L1_Quote_SupplierA.pdf    (tables with flexible schema)           │
│  │   ├── L2_Quote_SupplierB.pdf                                             │
│  │   ├── L3_Quote_SupplierC.pdf                                             │
│  │   ├── L1_Email_SupplierA.pdf    (correspondence)                        │
│  │   ├── L2_Email_SupplierB.pdf                                             │
│  │   ├── L3_Email_SupplierC.pdf                                             │
│  │   └── Bidding_Summary.xlsx      (summary sheet)                         │
│  └── ...                                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INGESTION LAYER                                      │
│  • SharePoint Graph API Client                                              │
│  • Folder crawler with regex pattern matching                               │
│  • Incremental sync (timestamp-based watermark)                             │
│  • Document downloader with retry & checksum                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      EXTRACTION & PARSING LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ PDF Table    │  │ Email PDF    │  │ Excel        │  │ OCR Fallback │   │
│  │ Extractor    │  │ Parser       │  │ Parser       │  │ (LLM/Vision) │   │
│  │ (Camelot +   │  │ (text +      │  │ (openpyxl)   │  │              │   │
│  │  Azure DI)   │  │  metadata)   │  │              │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STORAGE LAYER                                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐ │
│  │ Structured DB   │  │ Document Store  │  │ Vector Store                │ │
│  │ (PostgreSQL /   │  │ (Data Lake /    │  │ (ChromaDB /                 │ │
│  │  Azure SQL)     │  │  Azure Blob)    │  │  Azure Cognitive Search)    │ │
│  │                 │  │                 │  │                             │ │
│  │ • bids          │  │ • raw PDFs      │  │ • bid document chunks       │ │
│  │ • suppliers     │  │ • extracted     │  │ • supplier profiles         │ │
│  │ • quote_lines   │  │   JSON          │  │ • risk narratives           │ │
│  │ • bid_items     │  │                 │  │                             │ │
│  │ • risk_scores   │  │                 │  │                             │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ANALYSIS ENGINE LAYER                                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │   COLLUSION  │ │   ANOMALY    │ │    PRICE     │ │  COMPLIANCE  │       │
│  │   DETECTOR   │ │   DETECTOR   │ │   ANALYZER   │ │   CHECKER    │       │
│  │              │ │              │ │              │ │              │       │
│  │• Identical   │ │• Isolation   │ │• Cross-bid   │ │• Folder      │       │
│  │  prices      │ │  Forest      │ │  comparison  │ │  structure   │       │
│  │• Bid rotation│ │• Z-score     │ │• Variance    │ │• Doc count   │       │
│  │• Compl. bids │ │• Benford's   │ │  analysis    │ │• Approval    │       │
│  │• Shared ind. │ │  Law         │ │• Benchmark   │ │  chain       │       │
│  │• Price corr. │ │• Time-series │ │  deviation   │ │• Field       │       │
│  │• Graph nets  │ │  anomalies   │ │• Historical  │ │  completeness│       │
│  │              │ │              │ │  trends      │ │              │       │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LLM INTELLIGENCE LAYER                             │
│  • Azure OpenAI GPT-4o / GPT-4 Turbo                                        │
│  • Document summarization (per bid, per supplier, across portfolio)        │
│  • Natural language Q&A over bid documents                                  │
│  • Risk narrative generation ("Why is this bid high-risk?")                │
│  • Compliance gap explanation                                               │
│  • Entity extraction fallback for malformed tables                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      API + PRESENTATION LAYER                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐ │
│  │   FASTAPI       │  │   FRONTEND      │  │   ALERTING & REPORTING      │ │
│  │   Backend       │  │   (Streamlit/   │  │   • Email alerts            │ │
│  │                 │  │    React)       │  │   • Slack/Teams webhooks    │ │
│  │ • /upload       │  │                 │  │   • PDF risk reports        │ │
│  │ • /analyze      │  │ • Risk dashboard│  │   • Scheduled scans         │ │
│  │ • /search       │  │ • Bid comparison│  │                             │ │
│  │ • /collusion    │  │ • Collusion map │  │                             │ │
│  │ • /compliance   │  │ • Drill-down    │  │                             │ │
│  │ • /ask          │  │   tables        │  │                             │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Model

### Bid (Parent Entity)
```yaml
bid:
  bid_id: str           # "BID_2024_001"
  folder_path: str      # SharePoint relative path
  bid_date: date
  category: str         # IT, Construction, Services, etc.
  department: str
  status: str           # Open, Closed, Awarded, Cancelled
  created_at: timestamp
  updated_at: timestamp
```

### Supplier
```yaml
supplier:
  supplier_id: str
  name: str
  email_domain: str
  address_hash: str     # Hashed for privacy, used for collusion detection
  phone_hash: str
  registration_number: str
  risk_profile: json
```

### Quote Document
```yaml
quote_document:
  doc_id: str
  bid_id: str -> Bid
  supplier_id: str -> Supplier
  doc_type: enum [QUOTE, EMAIL, SUMMARY]
  level: enum [L1, L2, L3]
  file_name: str
  file_hash: str
  raw_text: text
  extracted_tables: json  # Array of tables as normalized JSON
  metadata: json          # Page count, creation date, author, etc.
  ocr_confidence: float
```

### Quote Line Item (Normalized from Flexible Tables)
```yaml
quote_line_item:
  line_id: str
  doc_id: str -> QuoteDocument
  bid_id: str -> Bid
  supplier_id: str -> Supplier
  item_code: str
  description: str
  quantity: float
  unit: str
  unit_price: float
  total_price: float
  currency: str
  delivery_days: int
  warranty_months: int
  terms: text
  # Flexible fields stored as JSON for schema evolution
  custom_fields: json
```

### Risk Score
```yaml
risk_score:
  score_id: str
  bid_id: str
  supplier_id: str
  category: enum [PRICE, COLLUSION, COMPLIANCE, DOCUMENTATION, CONCENTRATION, TIMELINE]
  severity: enum [LOW, MEDIUM, HIGH, CRITICAL]
  score: float  # 0.0 - 1.0
  indicators: json  # List of specific flags
  explanation: text
  ai_narrative: text  # LLM-generated explanation
  detected_at: timestamp
```

---

## 4. Detection Algorithms

### 4.1 Collusion Detection

| Technique | Implementation | Flag Threshold |
|-----------|---------------|----------------|
| **Identical Prices** | Jaccard similarity of price vectors across suppliers | > 0.95 |
| **Price Clustering** | K-Means on normalized price vectors; flag tight clusters | Within 2% variance |
| **Bid Rotation** | Markov chain on winner sequences; detect periodicity | Entropy < threshold |
| **Complementary Bidding** | Cross-bid correlation matrix; flag negative correlations | r < -0.7 |
| **Shared Indicators** | Graph analysis on hashed addresses, emails, phone numbers | Shared node degree > 1 |
| **Benford's Law** | Chi-squared test on first-digit distribution of prices | p < 0.05 |
| **Time-Series Collusion** | Change-point detection on winning margin trends | Sudden narrowing |

### 4.2 Anomaly Detection

| Technique | Implementation | Use Case |
|-----------|---------------|----------|
| **Isolation Forest** | sklearn.ensemble.IsolationForest | Outlier bids per category |
| **Z-Score** | (price - mean) / std for same item across bids | > 3σ flagged |
| **IQR** | Prices outside [Q1-1.5*IQR, Q3+1.5*IQR] | Robust outlier detection |
| **Time-Series** | Prophet / STL decomposition | Price trend breaks |
| **Mahalanobis Distance** | Multi-variate distance (price, qty, delivery) | Multivariate outliers |

### 4.3 Compliance Rules

```python
RULES = [
    "Each bid folder MUST contain exactly 3 quote PDFs",
    "Each bid folder MUST contain exactly 3 email PDFs",
    "Each bid folder MUST contain exactly 1 Excel summary",
    "Quote PDFs MUST contain at least one price table",
    "Email PDFs MUST have a sent date within bid window",
    "Excel summary MUST match sum of quote line items",
    "All L1/L2/L3 quotes MUST share same item codes",
    "Bid approval signature MUST be present in at least one email",
]
```

---

## 5. Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Language** | Python 3.11+ | Rich AI/ML ecosystem |
| **SharePoint** | Microsoft Graph API + `msgraph-sdk` | Native enterprise integration |
| **PDF Extraction** | Camelot-py + Azure Document Intelligence | Best-in-class table extraction |
| **Email Parsing** | pdfplumber + regex + LLM fallback | Handle various email PDF formats |
| **Excel** | openpyxl / pandas | Standard Python stack |
| **Database** | PostgreSQL + SQLAlchemy | Structured relational data |
| **Vector DB** | ChromaDB (local) / Azure AI Search (prod) | Semantic search |
| **LLM** | Azure OpenAI GPT-4o | Enterprise-grade, private data |
| **API** | FastAPI + Pydantic | High-performance async API |
| **Frontend** | Streamlit | Rapid analytics UI |
| **Orchestration** | Apache Airflow / Prefect / Python scripts | Pipeline scheduling |
| **Deployment** | Docker + Azure Container Apps | Cloud-native |

---

## 6. Security & Privacy

- **Data never leaves tenant**: All processing within company's Azure subscription
- **PII hashing**: Supplier addresses, phones hashed before storage for collusion detection
- **Role-based access**: Azure AD integration for API authentication
- **Audit logging**: Every analysis run logged with user identity
- **Encryption at rest**: Azure Storage Service Encryption
- **Encryption in transit**: TLS 1.2+ for all API calls

---

## 7. Implementation Phases

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| **Phase 1: Foundation** | 2 weeks | SharePoint connector, PDF extraction, basic storage |
| **Phase 2: Core Analysis** | 3 weeks | Collusion, anomaly, price comparison engines |
| **Phase 3: LLM Layer** | 2 weeks | Summarization, Q&A, narrative generation |
| **Phase 4: UI & API** | 2 weeks | FastAPI backend, Streamlit dashboard |
| **Phase 5: Production** | 2 weeks | Azure deployment, monitoring, alerting |
