# Git & Databricks Best Practices

**FCRM Risk Assessment — MCC Team**

| Attribute | Detail |
|---|---|
| Document Title | Git & Databricks Notebook Best Practices |
| Document Owner | FCRM Enterprise Risk Assessment Reporting Team |
| Effective Date | April 2026 |
| Version | 2.0 (supersedes v1.1). Section 4 is a v2.1 working draft pending lineage detail from Databricks workspace. |
| Target Audience | MCC Developers, Team Leads, 1LOD, 2LOD, Internal Audit |
| Systems of Record | GitHub (`TD-Universe/RAFY2025_CA`) + Databricks + Jira (FY25 RA CYCLE - DATA) |

---

## 1. Purpose

This document defines the standards for writing, organising, and version-controlling Databricks notebooks and Git commits for the FCRM Risk Assessment cycle. It is structured around three time horizons:

- **Section 2 — Current Facts.** How the team is operating today (FY2025 cycle in progress).
- **Section 3 — End-of-Cycle Recommendations.** What to do now to close the FY2025 audit window cleanly without disrupting in-flight work.
- **Section 4 — Future Recommendations.** Structural and convention changes proposed for the FY2026 cycle.

Sections 5–8 hold standards that carry across cycles, a checklist, common mistakes, and related documents.

> **Governance rule** — All business logic decisions must be captured in Jira before work begins in Databricks. Unlogged changes are not authoritative and will be flagged as audit findings (Change Management SOP v1.1).

---

## 2. Current Facts (FY2025 Cycle)

This section describes how the MCC Team is actually operating today. It is the baseline against which both end-of-cycle and future recommendations are measured.

### 2.1 Environment

- **Databricks** is the single query environment — no DEV / PROD split. All work happens in one workspace.
- **GitHub** (`TD-Universe/RAFY2025_CA`) is used **as an audit record only** — not for deployment. Final approved queries are pushed for traceability after mastersheet sign-off.
- **Excel mastersheet** (SharePoint: `06 - Change Management / Evidence`) is the authoritative output record for FY2025 metric values.
- **Source data**: Rahona (SRZ/CZ, 20 sources, pulled to CA AZ on 1 November 2025) and ADIDO (73 sources).

### 2.2 Folder Structure (As-Is)

The Databricks workspace currently follows the FY2024 pattern carried into FY2025:

```
FY_2025/
├── Analysis/                           ← per-AU work, organised by LOB
│   ├── CBB/
│   │   ├── ABAC/                       ← ABAC kept as LOB-nested subfolder
│   │   ├── 301069 Merchant Solution    ← one notebook per AU (all metrics inside)
│   │   ├── 301451 CMS
│   │   ├── 700005 - centralized
│   │   ├── CBC_Distribution_301479
│   │   ├── COM_Credit_301488
│   │   ├── COM_Deposit_301487
│   │   ├── SBB_Credit_301486
│   │   ├── SBB_Deposit_301485
│   │   └── SBB_Distribution_301570
│   ├── CPB/  GMI/  P & T/  TDGIS/  TDI/  TE_CE/  WEALTH/
│
├── Centralized Data/                   ← one-query-many-AUs metrics
│   ├── 1.1 Unscored or Unrated Fy 2025 View
│   ├── 1.2 HRC Tier 1 or Tier 2 Fy 2025
│   ├── 1.3 High risk customers
│   ├── 1.4 Medium risk customers
│   ├── 1.5 Low risk customers
│   ├── 3.17 UTR
│   ├── 3.18 SAR STR
│   └── SD.6 Customer relationship less than 1 year
│
├── Configs/
│   ├── Create_Adhoc_Catalogue
│   ├── Create_Adido_Catalogue
│   ├── Create_Analysis_Catalogue
│   ├── Create_Snapshot_Catalogue
│   ├── Create_View_Catalogue
│   ├── GAMLConnections
│   ├── RA_BUSINESS_CDEs
│   └── Settings
│
├── Data_Quality_Checks/
│   ├── Lobs/
│   └── TABLE_VIEW_CREATION/
│
├── LOBs/
├── SRZ_TO_ADLS/
└── Views/
```

**Observations on the current structure:**

- Each LOB folder contains **one notebook per AU**; all metrics for that AU live inside that single notebook.
- **ABAC is duplicated** as a subfolder within each LOB.
- **Centralized Data** holds metrics that are computed once across many AUs — separate from the per-AU LOB folders.

### 2.3 Naming and Commits (As-Is)

| Item | Current Convention |
|---|---|
| Notebook filename | `[AU code] [AU name]` (e.g. `301069 Merchant Solution`) |
| Commit message | `[FY25DATA-XXX] description` |
| Branch | `dev/FY25DATA-XXX-description` |

JIRA ticket IDs are embedded in commits as the audit trace anchor. Each ticket maps 1-to-1 to a (metric, AU) pair, but the metric ID and AU are currently captured **only in the ticket title** — they are not separate filterable fields or labels.

### 2.4 Workload Distribution

- **Regular metrics (WP-01 / 02 / 03)** — devs are assigned **2–3 AUs each** and write all metrics for those AUs.
- **ABAC (WP-04)** — a single query covers **61 AUs** with the same logic. One developer can carry the full ABAC scope; per-LOB ABAC subfolders are largely redundant.

### 2.5 Active Performance Constraint

Following the **DaaS flag of 30 April 2026** — a nested SELECT on `caedw.acct_trans` caused a hanging process. The performance rules in Section 5.3 are mandatory and being enforced for the remainder of the cycle.

---

## 3. End-of-Cycle Recommendations (FY2025 Audit Closeout)

The audit window is short and the FY2025 cycle is mid-flight. **Do not restructure folders, rename notebooks, or change commit conventions during this window.** The recommendations below are closeout-only and additive.

### 3.1 Do Not Disrupt

| Action | Status |
|---|---|
| Restructure Databricks folders | ❌ Defer to FY2026 |
| Rename notebooks (AU → metric-based) | ❌ Defer to FY2026 |
| Change commit format (drop `FY25DATA-XXX`) | ❌ Defer to FY2026 |
| Change branch naming | ❌ Defer to FY2026 |
| Reorganise ABAC | ❌ Defer to FY2026 |

### 3.2 Closeout Checklist

Before the audit window closes, every developer must complete the following:

- [ ] **Push all final, PO APPROVED queries to GitHub.** Any query whose result is in the Excel mastersheet must have a corresponding Git commit.
- [ ] **Complete notebook headers.** Fill in metric, ticket, owner, reviewer, last-updated date, and status (PO APPROVED) per the template in Section 5.1.
- [ ] **Verify the DQ check cell exists in every notebook** — null check, record count, duplicate check, reconciliation numbers.
- [ ] **Add a README to each LOB folder** listing the AUs in scope, the dev owner, and the final status of each metric.
- [ ] **Verify commit messages carry the `[FY25DATA-XXX]` prefix.** No bare commits, no `WIP`, no `fix`.
- [ ] **Tag the audit-close commit** on `main` with `audit-close-fy2025` for fast retrieval by reviewers.

### 3.3 Audit Trail Hardening

- **Cross-reference.** For every metric in the Excel mastersheet, confirm there is (a) a Jira ticket in PO APPROVED state, and (b) a Git commit referencing that ticket ID. Any mismatch is an audit finding.
- **Lock `main`.** No further commits to `main` after audit close without explicit Team Lead approval.
- **Archive.** Export the key Databricks notebooks to SharePoint `06 - Change Management / Evidence` as a snapshot of the workspace at audit close.

### 3.4 Known Gaps to Disclose

The following are documented gaps for FY2025; **do not attempt to retroactively fix them this cycle** — they are inputs to Section 4.

- JIRA tickets do not carry `metric:` or `au:` filter labels. Recovery is by title keyword search only, which is fragile.
- ABAC duplication across LOB folders means audit traversal of WP-04 requires opening multiple folders.
- The single-notebook-per-AU pattern means commit history is **not** per-metric — a single commit can change logic for multiple metrics simultaneously.

---

## 4. Future Recommendations (FY2026 Cycle) — Working Draft

> **Status: provisional (v2.1 draft).** The folder layout below is a sketch of a lineage-aligned design. The naming conventions, JIRA hygiene, and ABAC handling rules in 4.2–4.5 are stable. The folder structure in 4.1 will be refined once the following are reviewed: contents of `Configs/`, `SRZ_TO_ADLS/`, `LOBs/`, `Data_Quality_Checks/Lobs/` and `TABLE_VIEW_CREATION/`, plus a representative centralized notebook and an ABAC notebook.

The following changes should be designed and agreed before FY2026 cycle kickoff. They are informed by the pain points logged during FY2025 and by the structural mismatch between regular and ABAC workloads.

### 4.1 Lineage-Aligned Folder Structure (Provisional)

**Design principle:** the folder structure should mirror the data lineage flow. An auditor tracing source → transformation → output should be able to walk the folder tree in the same order. This makes the workspace self-documenting and aligns directly with the V&QA SOP (Sujai) Step 2 (Data Quality Checks) and Step 6 (Output Verification).

**Lineage stages (FCRM RA cycle):**

```
[1] Configs & Catalogues          → schema, CDEs, connections
[2] Source Ingestion              → Rahona (SRZ/CZ) + ADIDO → CA AZ
[3] Transformations               → per-AU + centralized + ABAC
[4] Data Quality Checks           → completeness, accuracy, reconciliation
[5] Views                         → consumption layer
[6] Outputs                       → CA AZ tables → Static Sheet → IRAT → Excel mastersheet
```

**Provisional folder layout mapped to those stages:**

```
RAFY2026_CA/
├── 00_Configs/                          ← [1] catalogues, connections, CDE registry
│   ├── Catalogues/                      (Create_Adhoc, Create_Adido, Create_Analysis, etc.)
│   ├── Connections/                     (GAMLConnections, Settings)
│   └── CDE_Registry/                    (RA_BUSINESS_CDEs)
│
├── 01_Source_Ingestion/                 ← [2] source → CA AZ landing
│   ├── Rahona_SRZ_to_ADLS/
│   └── ADIDO_Load/
│
├── 02_Transformations/                  ← [3] business logic per metric
│   ├── Centralized/                     ← one query, many AUs
│   │   ├── Regular/
│   │   │   ├── M1.1_Unscored_View.ipynb
│   │   │   └── M1.2_HRC_Tier12.ipynb
│   │   └── ABAC/
│   │       ├── eba01.ipynb
│   │       ├── eba02.ipynb
│   │       └── _shared/
│   │           ├── abac_au_list.py      ← canonical 61-AU list
│   │           └── abac_utils.py
│   └── Per_AU/                          ← per-AU dev work (2–3 AUs / dev)
│       ├── CBB/
│       │   ├── AU_301069_Merchant_Solution/
│       │   │   ├── M1.1_301069.ipynb
│       │   │   └── M1.2_301069.ipynb
│       │   └── AU_301451_CMS/
│       └── CPB/  GMI/  P_and_T/  TDGIS/  TDI/  TE_CE/  WEALTH/
│
├── 03_DQ_Checks/                        ← [4] validation layer
│
├── 04_Views/                            ← [5] consumption views
│
└── 05_Outputs/                          ← [6] what feeds the Excel mastersheet
```

**Why lineage-aligned beats workload-aligned:**

- An auditor opens `00_Configs/` first to understand the schema, then walks down to `05_Outputs/` to see what was produced. The folder tree itself answers the audit question "where did the data come from and how did it become this number?".
- Per-AU (`Per_AU/`) and one-query-many-AUs (`Centralized/`, including ABAC) both sit under `02_Transformations/` because they are the same lineage stage — just different workload patterns. The split is preserved as subfolders.
- DQ Checks have a clear home as a distinct lineage stage rather than being scattered inside transformation notebooks (though notebook-level DQ cells stay — see Section 5.4).

### 4.2 Open Questions (To Resolve Before Locking 4.1)

The following need to be confirmed against the actual Databricks workspace before this layout is final:

| Question | Why it matters |
|---|---|
| What lives in `LOBs/` (top-level) vs `Analysis/[LOB]/`? | Determines whether `LOBs/` is reference data, a separate transformation tier, or duplication. |
| What is in `SRZ_TO_ADLS/` — is it pure ingestion code, or does it include transformations? | Decides whether stage [2] is just `Rahona_SRZ_to_ADLS/` or needs sub-stages. |
| How do `Data_Quality_Checks/Lobs/` and `TABLE_VIEW_CREATION/` relate? | DQ-as-stage [4] vs DQ-embedded-in-transformations is a design choice. |
| How is lineage currently captured inside a centralized notebook? | If `[LINEAGE]` cells already exist (per Section 5.2), they become the lineage anchor. If not, the convention needs to be retrofitted. |
| Is `eba01`, `eba02`, … an independent numbering or does it map cleanly to M4.1, M4.2, …? | Determines whether the README mapping table in `02_Transformations/Centralized/ABAC/` is one-line or full-table. |

### 4.3 Unified Naming Convention

A single convention applied at every level of the workspace and every Git artifact. The rules are designed so that a folder path or filename, read in isolation, tells the reader exactly what they are looking at.

**Folders:**

| Element | Pattern | Example |
|---|---|---|
| Top-level (lineage stage) | `NN_Title_Case_With_Underscores` | `00_Configs`, `02_Transformations`, `05_Outputs` |
| Subfolder (within a stage) | `Title_Case_With_Underscores` | `Per_AU`, `Centralized`, `CDE_Registry`, `Source_Ingestion` |
| LOB folder | `UPPERCASE` (preserves existing LOB acronyms) | `CBB`, `CPB`, `WEALTH`, `TDGIS` |
| AU folder | `AU_<code>_<Name_With_Underscores>` | `AU_301069_Merchant_Solution`, `AU_301479_CBC_Distribution` |
| Shared / utility folder | `_shared/` (underscore prefix sorts to top, signals internal) | `_shared/` |

**Notebooks:**

| Element | Pattern | Example |
|---|---|---|
| Per-AU metric notebook | `M<#.#>_<au_code>.ipynb` | `M1.1_301069.ipynb` |
| Centralized metric notebook | `M<#.#>_<Descriptor>.ipynb` | `M1.1_Unscored_View.ipynb` |
| ABAC notebook | `eba<NN>.ipynb` (existing convention) | `eba01.ipynb`, `eba02.ipynb` |
| Shared module | `<descriptor>.py` | `abac_au_list.py`, `abac_utils.py` |

**Branches and commits:**

| Element | FY2025 (current) | FY2026 (proposed) |
|---|---|---|
| Notebook (per-AU) | `FY25DATA-126_unscored.ipynb` | `M1.1_301069.ipynb` |
| Notebook (centralized) | `FY25DATA-126_unscored_view.ipynb` | `M1.1_Unscored_View.ipynb` |
| Notebook (ABAC) | `FY25DATA-359_abac.ipynb` | `eba01.ipynb` |
| Commit (per-AU) | `[FY25DATA-126] Add filter` | `[M1.1 / 301069] Add filter` |
| Commit (centralized) | `[FY25DATA-126] Add view` | `[M1.1 / Centralized] Add view` |
| Commit (ABAC) | `[FY25DATA-359] Fix date range` | `[eba01] Fix date range` |
| Branch | `dev/FY25DATA-126-unscored` | `dev/M1.1-301069-unscored` |

**Underlying principles:**

1. **Lineage stage prefix (`NN_`) only at top level** — reinforces the six-stage flow without polluting deeper paths.
2. **`Title_Case_With_Underscores` for hierarchical folders** — readable, sortable, no ambiguity about word breaks.
3. **`UPPERCASE` reserved for established acronyms** — LOBs (`CBB`, `CPB`), `ABAC`. Don't invent new uppercase tokens.
4. **`AU_` prefix on AU folders** — self-documenting; no risk of mistaking `301069_Merchant_Solution` for a date or a ticket ID.
5. **Type prefix in filenames** — `M` = metric, `eba` = ABAC. A file named `M1.1_301069.ipynb` is unambiguous on sight.
6. **JIRA ticket IDs dropped from filenames, branches, and commits.** JIRA tickets are 1-to-1 with (metric, AU); embedding the ticket ID is redundant. Audit traceability moves to JIRA labels — see Section 4.4.

### 4.4 JIRA Hygiene — Add Filterable Labels

To preserve audit traceability after dropping ticket IDs from commits, add two labels to every Jira ticket:

- `metric:M1.1` (or `metric:eba01` for ABAC)
- `au:301069` (or `au:ABAC` for centralized ABAC)

Audit recovery path becomes:

> commit `[M1.1 / 301069]` → Jira filter `metric:M1.1 AND au:301069` → approved ticket

Without these labels, recovery falls back to keyword search on ticket titles, which is fragile.

### 4.5 Per-Metric Commits — Strict

One commit per (metric, AU) change. Never bundle two metric IDs in a single commit, even within the same AU folder. This is the structural reason for splitting AU-as-notebook into AU-as-folder-with-metric-notebooks.

### 4.6 ABAC Special Handling

- One notebook per ABAC metric (`eba01.ipynb`, `eba02.ipynb`, …); each notebook iterates over the canonical 61-AU list.
- `_shared/abac_au_list.py` holds the AU list — every ABAC notebook imports it. **No copy-paste.**
- `_shared/abac_utils.py` for shared transformations.
- `README.md` in `02_Transformations/Centralized/ABAC/` carries the `eba# → M4.x` mapping so any auditor can resolve an ABAC notebook to its metric definition without guessing.

### 4.7 Migration Plan (Pre-FY2026 Kickoff)

1. **Resolve open questions** in 4.2 by reviewing the actual Databricks workspace contents.
2. **Lock the lineage-aligned structure** with Team Leads and 1LOD before cycle kickoff.
3. **Pre-create** the `RAFY2026_CA` repository and seed the folder skeleton matching the six lineage stages.
4. **Migrate** the canonical 61-AU list and shared utilities into `02_Transformations/Centralized/ABAC/_shared/` early so all ABAC notebooks import a single source.
5. **Apply Jira labels retroactively** to a sample of FY2025 tickets to validate the filter recovery path before going live.
6. **Update** Change Management SOP, Audit Summary, and onboarding docs to reflect the new conventions.

---

## 5. Standards Carried Forward (Cycle-Independent)

These standards apply in both FY2025 and FY2026 cycles. They are technical hygiene that does not depend on folder structure or naming conventions.

### 5.1 Notebook Header (Mandatory)

Every notebook must start with a header cell:

```python
# =============================================================
# FCRM Risk Assessment FY[YYYY]
# Metric: [M_X.X] [Metric Name]
# AU: [AU code or "Centralized" or "ABAC"]
# Jira Ticket: [ticket ID]                # FY2025 only — drop in FY2026
# Work Package: [WP-XX]
# Owner: [name]
# Reviewer: [name]
# Last Updated: [YYYY-MM-DD]
# Status: [BUILD / AU REVIEW / PO APPROVED]
# =============================================================
#
# Description:
# [Plain-language description of what the notebook does]
#
# Data Sources:
#   - [source.table] ([Rahona / ADIDO])
#
# Output: [target table] / [Static Sheet location]
# =============================================================
```

The header is audit evidence. An auditor reading the notebook must immediately understand what it does, who approved it, and where the output goes.

### 5.2 Notebook Structure

Organise every notebook into clearly labelled cells:

| Cell | Purpose |
|---|---|
| 1 | Header & Metadata (see 5.1) |
| 2 | Imports & Configuration (constants at top) |
| 3 | `[LINEAGE]` Source Definition — source system, fields used, pull date |
| 4 | Data Extraction — pull only from sources defined in cell 3 |
| 5 | `[LINEAGE]` Business Logic & Transformations — every filter and rule documented |
| 6 | Data Quality Checks (see 5.4) |
| 7 | `[LINEAGE]` Output Definition — output table, downstream consumers |
| 8 | Write to CA AZ |
| 9 | Reconciliation Summary — print Dev Team count for BA reconciliation |

The three `[LINEAGE]` cells are the foundation for formal lineage documentation. Writing them clearly means lineage docs can be generated from the notebook without re-investigation.

### 5.3 Performance Rules (Mandatory)

Following the DaaS flag of 30 April 2026.

#### 5.3.1 No Unnecessary Nested SELECTs

```sql
-- ✅ Do
SELECT acct_id, trans_am
FROM caedw.acct_trans
WHERE post_dt >= '2025-11-01'
  AND post_dt <  '2026-05-01'

-- ❌ Avoid
SELECT acct_id, trans_am
FROM (
  SELECT acct_id, trans_am
  FROM caedw.acct_trans
  WHERE post_dt >= '2025-11-01'
) WHERE post_dt < '2026-05-01'
```

#### 5.3.2 Only SELECT Columns You Need

Never `SELECT *` on large tables. List only the columns the metric requires.

#### 5.3.3 Always Filter on Partition Keys First

```sql
-- ✅ Do — partition (post_dt) first
WHERE post_dt >= '2025-11-01'
  AND post_dt <  '2026-05-01'
  AND trans_type_id = 'XYZ'

-- ❌ Avoid
WHERE trans_type_id = 'XYZ'
  AND post_dt >= '2025-11-01'
```

#### 5.3.4 Cache Intermediate Results When Reused

```python
base_df = spark.sql("""
    SELECT acct_id, post_dt, trans_am, chanel_mn
    FROM caedw.acct_trans
    WHERE post_dt >= '2025-11-01'
      AND post_dt <  '2026-05-01'
""").cache()

metric_1 = base_df.filter(F.col('chanel_mn') == 'BRANCH')
metric_2 = base_df.filter(F.col('chanel_mn') == 'ATM')
```

#### 5.3.5 Test on a Sample Before Full Run

Add `.limit(1000)` during development. Remove before final run.

### 5.4 Data Quality Check Cell (Mandatory)

Every notebook must include a DQ check cell before writing output. This is the evidence for V&QA Step 2 (Data Quality Checks).

```python
# =============================================================
# DATA QUALITY CHECKS — [Metric / AU]
# =============================================================
print('=== DQ CHECK RESULTS ===')

# 1. Completeness — no null critical fields
null_check = result_df.filter(
    F.col('acct_id').isNull() | F.col('trans_am').isNull()
).count()
print(f'Null critical fields: {null_check}  (expected: 0)')

# 2. Record count
total = result_df.count()
print(f'Total records: {total}')

# 3. Duplicate check
dupes = total - result_df.dropDuplicates(['acct_id']).count()
print(f'Duplicate acct_ids: {dupes}  (expected: 0)')

# 4. Reconciliation summary (for BA comparison)
print('--- RECONCILIATION NUMBERS ---')
print(f'Dev Team count: {total}')
print(f'Date range: 2025-11-01 to 2026-04-30')
print(f'Source: caedw.acct_trans')
```

### 5.5 What NOT to Commit

> Never commit credentials, passwords, connection strings, or personal access tokens. Never commit raw data files or query output files. These belong only in CA AZ or Databricks.

- No `.env` files or config files with passwords
- No raw data extracts (`.csv`, `.parquet`)
- No Databricks `.dbc` export files — commit `.ipynb` instead
- No personal scratch notebooks
- Add a `.gitignore` to exclude these automatically

---

## 6. Quick Reference Checklist

Before pushing to Git and updating the mastersheet:

| Check | Requirement |
|---|---|
| Jira ticket | In PO APPROVED state. ID in commit (FY2025) **or** filterable by `metric:` / `au:` labels (FY2026) |
| Notebook header | Metric, AU, owner, reviewer, date, status, output location all filled in |
| No nested SELECTs | Query is flat — no unnecessary subqueries |
| Only needed columns | `SELECT` lists only the columns the metric requires |
| Partition filter first | `WHERE` clause starts with date / partition filter |
| DQ check cell | Null, record count, duplicate, reconciliation numbers all printed |
| Output confirmed | CA AZ table write confirmed; record count matches expectation |
| Mastersheet updated | Results in correct rows / columns of Excel mastersheet |
| Reviewer sign-off | Independent reviewer has confirmed mastersheet entries |
| Git commit | Correct format per cycle convention |
| No sensitive data | No passwords, tokens, raw data |

---

## 7. Common Mistakes & Fixes

| Mistake | Impact | Fix |
|---|---|---|
| Bundling multiple metrics in one commit | Cannot trace per-metric changes — audit finding | One Jira ticket / metric-AU pair = one commit |
| `SELECT *` on large tables | Query hangs, DaaS flags it, blocks others | List only required columns |
| Nested `SELECT` with no transformation | Performance degradation | Flatten to a single SELECT |
| Hardcoded dates mid-logic | Hard to maintain | Define dates as constants at top |
| Committing before PO APPROVED | Unapproved change in audit record | Push only after Jira reaches PO APPROVED |
| Updating mastersheet before reviewer confirms | Unreviewed data in authoritative output | Reviewer sign-off first, then mastersheet |
| Copy-pasting logic between notebooks | Drift when one updates and the other doesn't | Put shared logic in `_shared/utils.py` and import |
| Missing DQ check cell | Cannot produce V&QA evidence | Add DQ check cell before output write |
| (FY2025) No JIRA ticket ID in commit | Cannot trace to approval | Always `[FY25DATA-XXX]` prefix |
| (FY2026) Missing JIRA labels | Audit recovery falls back to fragile keyword search | Add `metric:` and `au:` labels to every ticket |

---

## 8. Related Documents

- **Audit Summary v1.3** — SharePoint: `00 - Audit Navigation`
- **Change Management and Version Control SOP v1.1** — SharePoint: `06 - Change Management`
- **Validation and Quality Assurance for AML Process v2.1** (Sujai) — SharePoint: `02 - Validation & QA`
- **QA & Governance Standard SOP v2.1** — SharePoint: `04 - Governance & Issue Mgmt`
- **Delivery Process SOP v2.1** — SharePoint: `01 - Delivery Process`
- **Data Sourcing & Lineage SOP v2.1** — SharePoint: `03 - Data Sourcing & Lineage`
- **GitHub Repository (FY2025)** — `https://github.com/TD-Universe/RAFY2025_CA`

---

**Document Owner:** FCRM Enterprise Risk Assessment Reporting Team  
**Effective:** April 2026  |  **Version:** 2.0  |  **Classification:** Internal