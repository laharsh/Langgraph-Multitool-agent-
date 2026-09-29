# Analyst workflows (P2)

These map to `benchmark/tasks.json` `workflow` ids and resume talking points.

## 1. `regulatory_brief`

**Who:** Compliance analyst  
**Goal:** Answer from official regulations with citations  
**Tool:** `knowledge_search` → Project 1 `/ask`  
**Example:** NIST four functions, EU Article 5, DPDP personal data

## 2. `risk_register`

**Who:** AI governance lead  
**Goal:** Query internal AI system inventory  
**Tool:** `sql_query` on `ai_systems` (risk_tier, primary_framework)  
**Example:** Count of `high` risk systems

## 3. `audit_prep`

**Who:** Internal audit  
**Goal:** Open findings by framework/quarter  
**Tool:** `sql_query` on `compliance_findings`  
**Example:** Open NIST Q3 findings

## 4. `ops_metrics`

**Who:** Ops / finance (demo data)  
**Goal:** Numeric answers from `sales` or calculator  
**Example:** Q3 product revenue, tax calculations

## 5. `internal_policy`

**Who:** Support / policy  
**Goal:** Short policy text without full RAG  
**Tool:** `web_search` (mock snippets — replace with P1 doc ingest in production)

## 6. `combined`

**Who:** GRC analyst in a single thread  
**Goal:** Regulation + internal metrics in one answer  
**Tools:** `knowledge_search` + `sql_query` (+ `calculator` when needed)

Re-seed demo data after schema changes: `python scripts/seed_db.py`
