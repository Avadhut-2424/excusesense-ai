# ExcuseSense AI — Project Objectives

## Primary Objective

Build a production-grade, explainable Machine Learning platform that ingests unstructured employee leave applications, classifies justifications into three distinct operational categories (**Genuine**, **Suspicious**, **Emotional**), attributes decision drivers through feature attribution, and persists full audit traces — transitioning HR leave compliance from subjective guesswork into objective, calibrated intelligence.

---

## Core Objectives

1. **Automated Leave Application Classification**
   Engineer an NLP classification pipeline using sublinear TF-IDF vectorization with n-gram extraction (1-2 ngrams) and regularized Multinomial Logistic Regression to accurately categorize any leave request into Genuine, Suspicious, or Emotional.
   - *Target: 100% test set accuracy across stratified splits.*

2. **Explainable AI (XAI) Feature Attribution**
   Implement deterministic token-level feature influence scoring (`compute_keyword_attributions`) that maps model coefficient vectors against the vocabulary of the raw input text, highlighting words with positive contribution weights to explain model decisions.
   - *Target: Top-6 feature attribution fidelity per inference.*

3. **Sub-Millisecond Inference Latency**
   Optimize vectorization and matrix scoring to deliver enterprise-grade performance suitable for real-time validation and batch processing without GPU overhead.
   - *Target: P50 latency < 1.0 ms; P99 latency < 2.5 ms.*

4. **Multi-Class Balanced Benchmark Dataset**
   Curate and maintain an enterprise-scale corpus of 1,570 real-world leave justifications distributed across medical appointments, acute illness, emotional stress/burnout, and fabricated/implausible excuses.
   - *Target: 1,570 verified samples balanced across Genuine (510), Emotional (520), and Suspicious (540).*

5. **Relational Audit Trail & Compliance Persistence**
   Persist every incoming request, predicted classification, calibrated confidence score, timestamp, class probability map, and extracted keywords into an ACID-compliant schema with SQLite (local) and PostgreSQL (production).

6. **Unified Developer Experience & Containerization**
   Containerize the full stack (API, PostgreSQL, Web UI, Streamlit legacy) via Docker and Docker Compose so the application boots with a single command (`docker compose up -d`).

7. **Production REST API with OpenAPI Specification**
   Expose asynchronous, non-blocking FastAPI endpoints (`/api/v1/analyze`, `/api/v1/batch`, `/api/v1/history`, `/api/v1/stats`, `/health`, `/metrics`) adhering to OpenAPI standards.

8. **Automated Test Suite with Duration Profiling**
   Deliver a comprehensive, unified test runner (`run_suite.py`) covering ML unit tests, attribution ordering, database transactions, API contracts, batch ingestion, and end-to-end smoke tests.
   - *Target: 100% pass rate in < 10 seconds execution.*

9. **Next-Generation Workstation Interface**
   Build a modern React + TypeScript + Vite web workstation featuring real-time interactive confidence gauges, keyword chip highlights, audit tables, and dark/light themes.

10. **Zero-Breaking-Change Legacy Support**
    Preserve backwards compatibility for existing Streamlit dashboards (`app.py`), database tables, and legacy endpoints so existing workflows continue to function without interruption.

---

## Secondary & Stretch Objectives

- **Active Learning Feedback Loop**: Allow HR administrators to submit corrected classifications to a retraining queue.
- **Multilingual Tokenization**: Expand vocabulary support to handle regional dialect excuses and multilingual text tokens.
- **Role-Based Access Control (RBAC)**: Support separate roles for Employee submitters vs. HR Compliance auditors.
