# Git & Databricks Best Practices

**FCRM Risk Assessment — MCC Team**

| Attribute | Detail |
|---|---|
| Document Title | Git & Databricks Notebook Best Practices |
| Document Owner | FCRM Enterprise Risk Assessment Reporting Team |
| Effective Date | April 2026 |
| Version | 2.6 (supersedes v2.5). Expanded §8.4 with the 95% DQ-threshold recommendation and six worked examples (completeness, per-field, output gating, SQL, reusable helper) for developers to follow. |
| Target Audience | MCC Developers, Team Leads, 1LOD, 2LOD, Internal Audit |
| Systems of Record | GitHub (`TD-Universe/RAFY2025_CA`) + Databricks + Jira (FY25 RA CYCLE - DATA) |

---

---

## 1. Purpose

This document defines the standards for writing, organising, and version-controlling Databricks notebooks and Git commits for the FCRM Risk Assessment cycle. It opens with the two folder trees that matter most for design decisions, then provides supporting detail.

- **Sections 2–4** — the As-Is FY2025 folder tree, the proposed new separate workspace folder tree, and the line-by-line mapping between them. These are the structural lead.
- **Section 5** — what to do now to close the FY2025 audit window cleanly without disrupting in-flight work.
- **Section 6** — other current facts about the FY2025 cycle (environment, naming, workload, active constraints).
- **Section 7** — implementation detail for the new separate workspace (naming, JIRA hygiene, per-metric commits, ABAC handling, migration plan).
- **Sections 8–10** — cycle-independent standards, a checklist, and common mistakes.
- **Section 11** — open questions the author was unable to resolve from the workspace alone; these need team input before the new workspace design can be locked.

> **Governance rule** — All business logic decisions must be captured in Jira before work begins in Databricks. Unlogged changes are not authoritative and will be flagged as audit findings (Change Management SOP v1.1).

---

## 2. Folder Structure — As-Is (FY2025)

The Databricks workspace is at `Shared/RiskAssessment/FY_2025/` with the following layout (drawn from the actual workspace, not idealised):

```
Shared/RiskAssessment/FY_2025/
├── Analysis/                              ← per-AU work, organised by LOB
│   ├── CBB/
│   │   ├── ABAC/                          ← per-AU ABAC subfolder within LOB
│   │   │   ├── ABAC 301069
│   │   │   ├── ABAC 301451
│   │   │   ├── ABAC 301479
│   │   │   └── ABAC 301485 / 86 / 87 / 88 / 570
│   │   ├── 301069 Merchant Solution       ← one notebook per AU, all metrics inside
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
├── Centralized Data/                      ← cross-AU metrics computed once
│   ├── Data Load/
│   ├── 1.1 Unscored or Unrated Fy 2025 View
│   ├── 1.2 HRC Tier 1 or Tier 2 Fy 2025
│   ├── 1.3 / 1.4 / 1.5 High / Medium / Low risk customers
│   ├── 3.17 UTR
│   ├── 3.18 SAR STR
│   └── SD.6 Customer relationship less than 1 year
│
├── Configs/                               ← lineage entry point
│   ├── GAMLConnections                    (JDBC URL + connection properties)
│   ├── Create_Snapshot_Catalogue          → creates RA_FY_2025 catalogue
│   ├── Create_View_Catalogue              → creates RA_FY25_VIEW catalogue
│   ├── Create_Adhoc_Catalogue
│   ├── Create_Adido_Catalogue
│   ├── Create_Analysis_Catalogue
│   ├── RA_BUSINESS_CDEs                   (CDE registry)
│   └── Settings                           (constants, parameters)
│
├── Data_Quality_Checks/
│   ├── Lobs/                              ← per-AU DQ notebooks
│   │   ├── TDW_DATA_Quality_CHECKS
│   │   ├── LOB -- TDI-- 101522
│   │   └── TDW PT 101015
│   └── TABLE_VIEW_CREATION/               ← DDL infrastructure
│       ├── BU_DETAILS_TABLE
│       ├── CDE_DEFINITION_TABLE
│       ├── Create_Data_Ava_Table_Common_Adido_SRZ_TXNs
│       ├── Create_Data_Ava_Table_Segment
│       ├── Create_Data_Quality_Table_Entrps_Data
│       └── VIEW_CREATION
│
├── LOBs/                                  ← broader LOB tier (separate from Analysis/[LOB]/)
│   ├── CBB/  CPB/  CPB(DIGITAL)/  GMI -TDAM/  NIU/
│   └── P & T/  TDGIS/  TDI/  TDS & Cowen 2025/  TE & CE/  WEALTH/
│
├── SRZ_TO_ADLS/                           ← source ingestion (Rahona EDB → CA AZ)
│   ├── 301069- TDMS/
│   ├── 301479 CCSC(Not in scope for FY25)/
│   ├── CBB Credit(301486,301488)/
│   ├── CBB Deposits (301485, 301487)/
│   ├── CBC & SBB Distribution(301479,301570)/
│   ├── CMS(301451)/
│   ├── CZ2ADLS 700005 - TD Auto Finance
│   ├── CZ2ADLS 700005 - TD Auto Finance Full Gen
│   └── CZ2ADLS SBB & COM Data Pull(Logic change …)
│
└── Views/                                 ← consumption views (RA_FY25_VIEW catalogue)
```

**Observed lineage flow (end-to-end):**

```
Source Systems (Rahona EDB, ADIDO)
    ↓ Configs/GAMLConnections (JDBC connection)
SRZ_TO_ADLS/[AU folders] (ingestion notebooks)
    ↓ Configs/Create_Snapshot_Catalogue (RA_FY_2025) + Create_View_Catalogue (RA_FY25_VIEW)
CA AZ snapshot tables (ra_fy_2025.tdms_final_2025, ra_adido_2025.pep_list_2025_exploded, …)
    ↓
Transformations:
  · Centralized Data/[metric notebooks]      (cross-AU)
  · Centralized Data/ABAC/[eba0X]            (cross-AU ABAC, 61 AUs in one notebook per metric)
  · Analysis/[LOB]/[AU notebook]             (per-AU, all metrics in one notebook)
  · Analysis/[LOB]/ABAC/[ABAC <AU>]          (per-AU ABAC, decentralized historical pattern — deprecated in the new workspace)
    ↓
Data_Quality_Checks/Lobs/[AU DQ notebook]   (validation)
Data_Quality_Checks/TABLE_VIEW_CREATION/    (DDL infrastructure)
    ↓
Views (RA_FY25_VIEW catalogue) → Excel mastersheet
```

**Observations:**

- `Analysis/[LOB]/[AU notebook]` is one notebook per AU containing all metrics for that AU as separate cells (e.g., `301069 Merchant Solution` contains SD_1.0, SD_1.1, …).
- `Analysis/[LOB]/ABAC/` is a per-LOB subfolder with one ABAC notebook per AU (`ABAC 301069`, `ABAC 301451`, …) — **not** the cross-AU pattern Tom is targeting in the new workspace.
- `Centralized Data/` is the existing precedent for "one notebook covers many AUs" — the closest current parallel to where ABAC should live.
- `LOBs/` is a different (broader) tier than `Analysis/[LOB]/` and contains LOBs not in `Analysis/` (e.g., `CPB(DIGITAL)`, `GMI -TDAM`, `NIU`, `TDS & Cowen 2025`). Purpose to be confirmed with Team Leads.

---

## 3. Folder Structure — New Separate Workspace (FY2025)

**Per Canada RA Daily Touchbase 2026-05-13.** Raghul proposed a clean two-folder workspace structure; Tom Wu directed: *"Let's create a separate Databricks workspace structure like this."* This supersedes the earlier six-stage lineage layout (preserved in change history) in favour of a simpler design that mirrors how the work actually flows: source ingestion → final query.

**Workspace root:** `RA_FY2025_CA`  *(name from the design proposal; reuse or rename for the new cycle as appropriate)*

**Segments = LOBs.** Confirmed segment list from the touchbase: **CBB, CPB, P&T,** [remaining segments — to be filled in from `Master_Data_source_FY2025_Segment.xlsx`].

**Folder layout:**

```
RA_FY2025_CA/
├── SRZ_2_ADLS/                                ← source → ADLS ingestion
│   └── <segment_name>/                        ← ALL segments (LOBs)
│       └── Notepads/
│           └── <segment_name>_<AUID>_<AUNAME>_Source.sql
│
└── Final_query_LOBS/                          ← final query / transformation feeding mastersheet
    └── <segment_name>/                        ← ALL segments (LOBs)
        └── <AU level folder>/                 ← e.g. AU_101522
            └── Notepads/
                └── <segment_name>_<AUID>_<AUNAME>_QUERIES.sql
```

**File naming standards (Stds):**

| Folder | Pattern | Example |
|---|---|---|
| `SRZ_2_ADLS/` | `<segment_name>_<AUID>_<AUNAME>_Source.sql` | `CBB_301069_Merchant_Solution_Source.sql` |
| `Final_query_LOBS/` | `<segment_name>_<AUID>_<AUNAME>_QUERIES.sql` | `CBB_301069_Merchant_Solution_QUERIES.sql` |

**Key differences from the previous six-stage proposal:**

| Element | Previous (v2.3, six-stage) | Current (v2.4, two-folder) |
|---|---|---|
| Top-level folders | 6 (`00_Configs`, `01_Source_Ingestion`, `02_Views`, `03_Transformations`, `04_DQ_Checks`, `05_Outputs`) | 2 (`SRZ_2_ADLS`, `Final_query_LOBS`) |
| Segment definition | `<SEG_NAME>` sub-population tier under Transformations | Segments **are** LOBs (CBB, CPB, P&T, …) |
| Hierarchy in transformation | `Centralized / Segment / Per_AU` split | Uniform `segment > AU > notepads` |
| File type | `.py` (per-AU) + `.ipynb` (centralized / ABAC) | `.sql` |
| Naming standard | `<AU>_<SEG>_<DataFlow>_<date>.py` | `<segment>_<AUID>_<AUNAME>_Source.sql` / `..._QUERIES.sql` |

> **Open from this proposal — needs Tom Wu / Raghul direction:**
>
> 1. **Configs** (catalogues, GAMLConnections, CDE registry) — where do they live? Implicit in `SRZ_2_ADLS/`, or as a third top-level folder alongside?
> 2. **Views** (the `02_Views` stage Raghul flagged earlier as sitting between ingestion and transformation) — are these inside `SRZ_2_ADLS/` or part of `Final_query_LOBS/`?
> 3. **DQ Checks** — folded into `Final_query_LOBS/` notebooks, or kept separate?
> 4. **ABAC** — does it become a segment alongside CBB/CPB/P&T, or stay as a special cross-AU pattern outside this structure?
> 5. **Outputs** — are the final outputs the `_QUERIES.sql` results themselves (no separate Outputs folder needed), or do they get materialised elsewhere?

---

## 4. As-Is → To-Be Mapping

Each existing FY2025 location maps to a target location in the new two-folder design. Several rows have **open questions** flagged in Section 3 — those targets will be confirmed after Tom Wu / Raghul direction.

| FY2025 location | New workspace location | Notes |
|---|---|---|
| `Configs/GAMLConnections`, `Configs/Create_*_Catalogue`, `Configs/RA_BUSINESS_CDEs`, `Configs/Settings` | **TBD** — implicit in `SRZ_2_ADLS/` setup, or a third top-level folder | Open Q1 in Section 3. |
| `SRZ_TO_ADLS/[AU folder]/` (SRZ + CZ ingestion) | `SRZ_2_ADLS/<segment>/Notepads/<segment>_<AUID>_<AUNAME>_Source.sql` | Two ingestion zones (SRZ, CZ) collapse into one folder; segment level (LOB) is the organising tier. |
| `ADIDO_OUT/` (top-level, no landing zone) | `SRZ_2_ADLS/<segment>/Notepads/` (alongside Rahona sources) | ADIDO is another source type within the same ingestion folder. |
| `Views/` (RA_FY25_VIEW catalogue) | **TBD** — likely inside `Final_query_LOBS/` or staged within `SRZ_2_ADLS/` | Open Q2 in Section 3. Raghul previously flagged Views as a distinct stage between ingestion and transformation. |
| `Centralized Data/[metric notebook]` | `Final_query_LOBS/<segment>/<AU folder>/Notepads/<segment>_<AUID>_<AUNAME>_QUERIES.sql` | Cross-AU centralized notebooks decompose per-AU under each segment in the new structure. |
| `Centralized Data/ABAC/eba0X.ipynb` *(moved here during FY2025 closeout)* | **TBD** — ABAC as a segment, or as a special cross-AU pattern | Open Q4 in Section 3. ABAC covers all 61 AUs in one notebook today; that pattern does not slot cleanly into `<segment>/<AU>/`. |
| `Analysis/[LOB]/[AU notebook]` | `Final_query_LOBS/<segment>/<AU folder>/Notepads/<segment>_<AUID>_<AUNAME>_QUERIES.sql` | One `.sql` file per AU per segment, replacing the FY2025 `.ipynb` per-AU pattern. |
| `Analysis/[LOB]/ABAC/ABAC <AU>` | (deprecated) | Decentralized historical work. Replaced by centralized ABAC handling (pending Q4). |
| `Data_Quality_Checks/Lobs/` and `Data_Quality_Checks/TABLE_VIEW_CREATION/` | **TBD** — folded into `Final_query_LOBS/` notebooks, or kept as a separate folder | Open Q3 in Section 3. |
| `LOBs/` (top-level) | Reconciled with segment list — segments are LOBs in the new design | Confirms `LOBs/` and `Analysis/[LOB]/` collapse into a single segment-organised view. |
| `RA_CDE_DQ_CHECKS/` (top-level) | Archive (FY2024 legacy) | Confirmed FY2024 DQ check tables (Tom Wu, May 2026). |
| `TEST_GITHUB`, `Sample_writing_result_into_table`, `Bit_Bucket_check_in_check_out`, `TestDF_Do_Not_Delete…`, etc. | Delete | Confirmed not in use (Tom Wu, May 2026). |
| `BACKUP_FY_2024`, `FY_2023`, `FY_2024` | Archive outside the active workspace | Move to a separate archive workspace or repo. |

---

## 5. End-of-Cycle Recommendations (FY2025 Audit Closeout)

The audit window is short and the FY2025 cycle is mid-flight. **Do not restructure folders, rename notebooks, or change commit conventions during this window.** The recommendations below are closeout-only and additive.

### 5.1 Do Not Disrupt

| Action | Status |
|---|---|
| Restructure the current Databricks workspace | ❌ Defer — build the new separate workspace instead |
| Rename notebooks in the current workspace | ❌ Defer — use new naming in the new workspace |
| Change commit format (drop `FY25DATA-XXX`) | ❌ Defer to the new workspace |
| Change branch naming | ❌ Defer to the new workspace |
| Reorganise ABAC across LOB folders | ❌ Defer to the new workspace |
| **Move user-folder ABAC notebooks (`eba01`, `eba02`) into shared `Centralized Data/ABAC/`** | ✅ **In scope for closeout** — see 5.2 |

### 5.2 Closeout Checklist

Before the audit window closes, every developer must complete the following:

- [ ] **Push all final, PO APPROVED queries to GitHub.** Any query whose result is in the Excel mastersheet must have a corresponding Git commit.
- [ ] **Complete notebook headers.** Fill in metric, ticket, owner, reviewer, last-updated date, and status (PO APPROVED) per the template in Section 8.1.
- [ ] **Verify the DQ check cell exists in every notebook** — null check, record count, duplicate check, reconciliation numbers.
- [ ] **Add a README to each LOB folder** listing the AUs in scope, the dev owner, and the final status of each metric.
- [ ] **Verify commit messages carry the `[FY25DATA-XXX]` prefix.** No bare commits, no `WIP`, no `fix`.
- [ ] **Tag the audit-close commit** on `main` with `audit-close-fy2025` for fast retrieval by reviewers.
- [ ] **Move ABAC notebooks from user folder to shared workspace.** Source: `/Workspace/Users/qiang.wu@td.com/abac/`. Target: `Shared/RiskAssessment/FY_2025/Centralized Data/ABAC/`. Files: `eba01`, `eba02`, and any other `eba*` notebooks (each maps 1-to-1 to ABAC metrics M4.1, M4.2, …). The utility `00_CC_Mapping_Setup.ipynb` (a Python helper for creating reusable views) moves alongside, into `Centralized Data/ABAC/_shared/`. After the move, validate that all `%run` references inside the notebooks resolve correctly from the new path. Owner: **Qiang Wu**, with Tom Wu sign-off.

### 5.3 Audit Trail Hardening

- **Cross-reference.** For every metric in the Excel mastersheet, confirm there is (a) a Jira ticket in PO APPROVED state, and (b) a Git commit referencing that ticket ID. Any mismatch is an audit finding.
- **Lock `main`.** No further commits to `main` after audit close without explicit Team Lead approval.
- **Archive.** Export the key Databricks notebooks to SharePoint `06 - Change Management / Evidence` as a snapshot of the workspace at audit close.

### 5.4 Known Gaps to Disclose

The following are documented gaps for FY2025; **do not attempt to retroactively fix them this cycle** — they are inputs to Sections 3–4 and 7.

- JIRA tickets do not carry `metric:` or `au:` filter labels. Recovery is by title keyword search only, which is fragile.
- ABAC duplication across `Analysis/[LOB]/ABAC/` subfolders means audit traversal of WP-04 requires opening multiple folders.
- The single-notebook-per-AU pattern means commit history is **not** per-metric — a single commit can change logic for multiple metrics simultaneously.
- **GAMLConnections is invoked inconsistently.** Some notebooks reach into a user folder (`/Workspace/Users/.../GAML/GAMLConnections`) instead of the shared `Configs/GAMLConnections`. To be standardised in the new workspace.
- **ABAC notebooks `eba01`, `eba02` were initially developed in `/Workspace/Users/qiang.wu@td.com/abac/`** rather than the shared workspace. **Resolved during this cycle:** moving to `Shared/RiskAssessment/FY_2025/Centralized Data/ABAC/` as part of audit closeout (see 5.2). This makes them visible in the shared tree before audit close.
- **Heterogeneous folder/notebook naming** and **test folders mixed with production**. Cleanup absorbed into the new separate workspace.

---

## 6. Other Current Facts (FY2025 Cycle)

This section describes how the MCC Team is actually operating today. It is the baseline against which both end-of-cycle and future recommendations are measured.

### 6.1 Environment

- **Databricks** is the single query environment — no DEV / PROD split. All work happens in one workspace.
- **GitHub** (`TD-Universe/RAFY2025_CA`) is used **as an audit record only** — not for deployment. Final approved queries are pushed for traceability after mastersheet sign-off.
- **Excel mastersheet** (SharePoint: `06 - Change Management / Evidence`) is the authoritative output record for FY2025 metric values.
- **Source data**: Rahona (SRZ/CZ, 20 sources, pulled to CA AZ on 1 November 2025) and ADIDO (73 sources).

### 6.2 Naming and Commits (As-Is)

| Item | Current Convention |
|---|---|
| Notebook filename | `[AU code] [AU name]` (e.g. `301069 Merchant Solution`) |
| Commit message | `[FY25DATA-XXX] description` |
| Branch | `dev/FY25DATA-XXX-description` |

JIRA ticket IDs are embedded in commits as the audit trace anchor. Each ticket maps 1-to-1 to a (metric, AU) pair, but the metric ID and AU are currently captured **only in the ticket title** — they are not separate filterable fields or labels.

### 6.3 Workload Distribution

- **Regular metrics (WP-01 / 02 / 03)** — devs are assigned **2–3 AUs each** and write all metrics for those AUs.
- **ABAC (WP-04)** — a single query covers **61 AUs** with the same logic. One developer can carry the full ABAC scope; per-LOB ABAC subfolders are largely redundant.

### 6.4 Active Performance Constraint

Following the **DaaS flag of 30 April 2026** — a nested SELECT on `caedw.acct_trans` caused a hanging process. The performance rules in Section 8.3 are mandatory and being enforced for the remainder of the cycle.

---

## 7. Implementation Detail for the New Workspace

> **Status: lineage-aligned design confirmed against FY2025 workspace.** Sections 3 and 4 above hold the target layout and as-is → to-be mapping. The subsections below cover naming, JIRA hygiene, per-metric commits, ABAC handling, and the migration plan.

### 7.1 Unified Naming Convention

A single convention applied at every level of the workspace and every Git artifact. The rules are designed so that a folder path or filename, read in isolation, tells the reader exactly what it represents.

**Folders:**

| Element | Pattern | Example |
|---|---|---|
| Top-level workspace folder | `SRZ_2_ADLS`, `Final_query_LOBS` | as proposed by Raghul, touchbase 2026-05-13 |
| Segment folder (LOB) | `UPPERCASE` (preserves existing LOB acronyms) | `CBB`, `CPB`, `P&T`, `WEALTH`, `TDGIS`, `TDI` |
| AU folder *(inside `Final_query_LOBS/<segment>/`)* | `<AUID>_<AUNAME>` or `AU_<code>_<Name_With_Underscores>` | `301069_Merchant_Solution`, `101522_TDI_Capital` |
| Notepads folder | `Notepads` | `Notepads/` |

**Files (`.sql`):**

| Element | Pattern | Example |
|---|---|---|
| Source ingestion query | `<segment>_<AUID>_<AUNAME>_Source.sql` | `CBB_301069_Merchant_Solution_Source.sql` |
| Final transformation query | `<segment>_<AUID>_<AUNAME>_QUERIES.sql` | `CBB_301069_Merchant_Solution_QUERIES.sql` |
| Centralized / ABAC notebooks | *(structure pending — see Section 3 open Qs)* | — |

All query artifacts are `.sql` files in the new design. The earlier `.py` / `.ipynb` proposal is superseded; ABAC and centralized notebooks remain `.ipynb` in their current form pending the structural decision (Section 3 open Q4).

**Branches and commits:**

| Element | FY2025 (current) | New design |
|---|---|---|
| File (per-AU) | `FY25DATA-126_unscored.ipynb` | `CBB_301069_Merchant_Solution_QUERIES.sql` |
| File (source) | `FY25DATA-126_source.ipynb` | `CBB_301069_Merchant_Solution_Source.sql` |
| Commit (per-AU) | `[FY25DATA-126] Add filter` | `[CBB / 301069] Add filter` |
| Branch | `dev/FY25DATA-126-unscored` | `dev/CBB-301069-merchant` |

**Underlying principles:**

1. **Segment + AUID + AUNAME in every query filename** — a file read in isolation tells the reader segment, AU, and AU name without opening it.
2. **`UPPERCASE` reserved for established acronyms** — LOBs / segments (`CBB`, `CPB`, `P&T`), `ABAC`. Don't invent new uppercase tokens.
3. **`Source` vs `QUERIES` suffix** is the only distinction between the two folders — one file maps cleanly to one folder and one purpose.
4. **JIRA ticket IDs dropped from filenames, branches, and commits.** JIRA tickets are 1-to-1 with (segment, AU); embedding the ticket ID is redundant. Audit traceability moves to JIRA labels — see Section 7.2.

### 7.2 JIRA Hygiene — Add Filterable Labels

To preserve audit traceability after dropping ticket IDs from commits, add two labels to every Jira ticket:

- `metric:M1.1` (or `metric:eba01` for ABAC)
- `au:301069` (or `au:ABAC` for centralized ABAC)

Audit recovery path becomes:

> commit `[M1.1 / 301069]` → Jira filter `metric:M1.1 AND au:301069` → approved ticket

Without these labels, recovery falls back to keyword search on ticket titles, which is fragile.

### 7.3 Per-Metric Commits — Strict

One commit per (metric, AU) change. Never bundle two metric IDs in a single commit, even within the same AU folder. This is the structural reason for splitting AU-as-notebook into AU-as-folder-with-metric-notebooks.

### 7.4 ABAC Special Handling

- One notebook per ABAC metric. **`eba01` = M4.1, `eba02` = M4.2, …** through M4.22 — clean 1-to-1 mapping with the ABAC metric definitions.
- Each notebook iterates over the **canonical 61-AU list** (broader population than the 35-AU base used elsewhere in the cycle).
- `_shared/abac_au_list.py` holds the 61-AU list — every ABAC notebook imports it. **No copy-paste.**
- `_shared/abac_utils.py` for shared transformations.
- `_shared/00_CC_Mapping_Setup.ipynb` (or `.py` once converted) — utility for creating reusable views, dependency of the `eba0X` notebooks.
- `README.md` in `03_Transformations/Centralized/ABAC/` carries the eba# → M4.x mapping table for auditors.

### 7.5 Migration Plan to the New Workspace

1. **Confirm `LOBs/` purpose** with Team Leads — keep as reference tier (`06_LOB_Reference/`) or merge into `03_Transformations/Per_AU/`.
2. **Lock the lineage-aligned structure** with Team Leads and 1LOD before cycle kickoff.
3. **Pre-create** the `RA_FY2025_CA` repository and seed the folder skeleton matching the six lineage stages.
4. **Standardise `GAMLConnections` invocations.** Inventory every notebook that calls `GAMLConnections`, replace any user-folder paths (`/Workspace/Users/.../GAML/GAMLConnections`) with the shared path. Going forward, only the shared path is permitted; user-folder copies should be deleted.
5. **ABAC notebooks already in shared workspace** at `Centralized Data/ABAC/` (moved during FY2025 closeout — see 5.2). in the new workspace this just sits under `03_Transformations/Centralized/ABAC/`.
6. **Delete test / scratch folders** (`TEST_GITHUB`, `Sample_writing_result_into_table`, `Bit_Bucket_check_in_check_out`, `TestDF_Do_Not_Delete…`, redundant `SAS_DATA_LOAD`) — confirmed not in use (Tom Wu, May 2026). Archive `BACKUP_FY_2024`, `FY_2023`, `FY_2024`, and `RA_CDE_DQ_CHECKS` (FY2024 legacy) outside the active workspace.
7. **Migrate** the canonical 61-AU list and shared utilities into `03_Transformations/Centralized/ABAC/_shared/` so all ABAC notebooks import a single source.
8. **Apply Jira labels retroactively** to a sample of FY2025 tickets to validate the filter recovery path before going live.
9. **Update** Change Management SOP, Audit Summary, and onboarding docs to reflect the new conventions.

---

## 8. Standards Carried Forward (Cycle-Independent)

These standards apply across both the current workspace and the new separate workspace. They are technical hygiene that does not depend on folder structure or naming conventions.

### 8.1 Notebook Header (Mandatory)

Every notebook must start with a header cell:

```python
# =============================================================
# FCRM Risk Assessment FY[YYYY]
# Metric: [M_X.X] [Metric Name]
# AU: [AU code or "Centralized" or "ABAC"]
# Jira Ticket: [ticket ID]                # current workspace only — drop in new workspace
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

### 8.2 Notebook Structure

Organise every notebook into clearly labelled cells:

| Cell | Purpose |
|---|---|
| 1 | Header & Metadata (see 8.1) |
| 2 | Imports & Configuration (constants at top) |
| 3 | `[LINEAGE]` Source Definition — source system, fields used, pull date |
| 4 | Data Extraction — pull only from sources defined in cell 3 |
| 5 | `[LINEAGE]` Business Logic & Transformations — every filter and rule documented |
| 6 | Data Quality Checks (see 8.4) |
| 7 | `[LINEAGE]` Output Definition — output table, downstream consumers |
| 8 | Write to CA AZ |
| 9 | Reconciliation Summary — print Dev Team count for BA reconciliation |

The three `[LINEAGE]` cells are the foundation for formal lineage documentation. Writing them clearly means lineage docs can be generated from the notebook without re-investigation.

### 8.3 Performance Rules (Mandatory)

Following the DaaS flag of 30 April 2026.

#### 8.3.1 No Unnecessary Nested SELECTs

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

#### 8.3.2 Only SELECT Columns You Need

Never `SELECT *` on large tables. List only the columns the metric requires.

#### 8.3.3 Always Filter on Partition Keys First

```sql
-- ✅ Do — partition (post_dt) first
WHERE post_dt >= '2025-11-01'
  AND post_dt <  '2026-05-01'
  AND trans_type_id = 'XYZ'

-- ❌ Avoid
WHERE trans_type_id = 'XYZ'
  AND post_dt >= '2025-11-01'
```

#### 8.3.4 Cache Intermediate Results When Reused

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

#### 8.3.5 Test on a Sample Before Full Run

Add `.limit(1000)` during development. Remove before final run.

### 8.4 Data Quality Check Cell (Mandatory)

Every notebook must include a DQ check cell before writing output. This is the evidence for V&QA Step 2 (Data Quality Checks).

#### 8.4.1 The 95% Threshold — Recommendation

The Inherent Risk constraint is: *data quality < 95% and not provided by business → Inherent Risk factor = "Not Available"* (Audit Summary §2.3). To make this implementable and consistent across developers:

1. **Define the 95% as two separate gates**, because "data quality" is ambiguous on its own:
   - **Completeness** — ≥ 95% of records in the AU population have all critical fields populated and valid.
   - **Accuracy / reconciliation** — Dev output reconciles to the source or BA-provided number within ±5% (i.e. ≥ 95% match).
2. **Set the threshold as a single constant** at the top of the notebook — `DQ_THRESHOLD = 0.95`. Never hardcode `0.95` in the middle of logic.
3. **Fail loud.** Print the exact percentage and an explicit `PASS` / `FAIL`. The printed cell output is the audit evidence — an auditor should see the number, not infer it.
4. **On FAIL (< 95%):** do not write output silently. Stop, print the shortfall, and route to the NOT AVAILABLE / risk-acceptance path (Governance §5.4 Step 7) so the AU gets the higher risk rating rather than a suppressed value.

> **Source note:** the controlling policy behind the 95% figure is still being traced (it carries forward from Audit Summary v1.2 and is not in the V&QA SOP). Implement against `DQ_THRESHOLD = 0.95` now; if the authoritative policy specifies a different number, only the one constant changes.

#### 8.4.2 Base DQ Check Cell (PySpark)

```python
# =============================================================
# DATA QUALITY CHECKS — [Metric / AU]
# =============================================================
DQ_THRESHOLD = 0.95          # single source of truth — do not hardcode elsewhere
CRITICAL_FIELDS = ['acct_id', 'trans_am', 'post_dt']

print('=== DQ CHECK RESULTS ===')

# 1. Record count
total = result_df.count()
print(f'Total records: {total}')

# 2. Completeness — % of records with ALL critical fields populated
complete = result_df.dropna(subset=CRITICAL_FIELDS).count()
completeness = complete / total if total else 0
print(f'Completeness: {completeness:.2%}  (threshold: {DQ_THRESHOLD:.0%})  '
      f'{"PASS" if completeness >= DQ_THRESHOLD else "FAIL"}')

# 3. Duplicate check
dupes = total - result_df.dropDuplicates(['acct_id']).count()
print(f'Duplicate acct_ids: {dupes}  (expected: 0)')

# 4. Reconciliation vs BA-provided number (±5% tolerance = 95% match)
ba_count = 12450             # BA-provided expected count for this AU
variance = abs(total - ba_count) / ba_count if ba_count else 1
print(f'Reconciliation variance: {variance:.2%}  (tolerance: {1-DQ_THRESHOLD:.0%})  '
      f'{"PASS" if variance <= (1 - DQ_THRESHOLD) else "FAIL"}')
```

#### 8.4.3 Per-Field Completeness Breakdown (PySpark)

When overall completeness fails, this shows which field is dragging the score down — so you know exactly what to fix or escalate.

```python
print('=== PER-FIELD COMPLETENESS ===')
for field in CRITICAL_FIELDS:
    populated = result_df.filter(F.col(field).isNotNull()).count()
    pct = populated / total if total else 0
    flag = 'PASS' if pct >= DQ_THRESHOLD else 'FAIL'
    print(f'  {field:<20} {pct:6.2%}   {flag}')
```

#### 8.4.4 Gate the Output Write on the Threshold (PySpark)

The check should *block* the write, not just report. This is what turns the 95% into an actual control.

```python
if completeness >= DQ_THRESHOLD and variance <= (1 - DQ_THRESHOLD):
    result_df.write.mode('overwrite').saveAsTable(CA_AZ_OUTPUT_TABLE)
    print(f'DQ PASSED — output written to {CA_AZ_OUTPUT_TABLE}')
else:
    print('DQ FAILED — output NOT written.')
    print(f'  Completeness {completeness:.2%}, Reconciliation variance {variance:.2%}')
    print('  Action: route to NOT AVAILABLE / risk acceptance (Governance §5.4 Step 7).')
    print('  Do not manually override — raise a RAID log entry and a BLOCKED Jira ticket.')
```

#### 8.4.5 SQL Equivalent (for `_QUERIES.sql` in the new workspace)

The same completeness gate expressed in SQL, for the `Final_query_LOBS/` query files.

```sql
-- DQ: completeness check against the 95% threshold
SELECT
    COUNT(*)                                                AS total_records,
    SUM(CASE WHEN acct_id IS NOT NULL
              AND trans_am IS NOT NULL
              AND post_dt  IS NOT NULL
             THEN 1 ELSE 0 END)                             AS complete_records,
    ROUND(
        SUM(CASE WHEN acct_id IS NOT NULL
                  AND trans_am IS NOT NULL
                  AND post_dt  IS NOT NULL
                 THEN 1 ELSE 0 END) * 1.0 / COUNT(*),
    4)                                                      AS completeness_ratio,
    CASE WHEN SUM(CASE WHEN acct_id IS NOT NULL
                        AND trans_am IS NOT NULL
                        AND post_dt  IS NOT NULL
                       THEN 1 ELSE 0 END) * 1.0 / COUNT(*) >= 0.95
         THEN 'PASS' ELSE 'FAIL' END                        AS dq_status
FROM ra_fy_2025.<segment>_<auid>_output;
```

#### 8.4.6 Reusable Helper (optional, for `_shared/`)

To keep the threshold and logic identical across all notebooks, factor it into one shared function rather than copy-pasting the cell.

```python
# _shared/dq_utils.py
DQ_THRESHOLD = 0.95

def check_completeness(df, critical_fields, threshold=DQ_THRESHOLD):
    total = df.count()
    if total == 0:
        return 0.0, 'FAIL'
    complete = df.dropna(subset=critical_fields).count()
    ratio = complete / total
    return ratio, ('PASS' if ratio >= threshold else 'FAIL')

def check_reconciliation(dev_count, ba_count, threshold=DQ_THRESHOLD):
    if ba_count == 0:
        return 1.0, 'FAIL'
    variance = abs(dev_count - ba_count) / ba_count
    return variance, ('PASS' if variance <= (1 - threshold) else 'FAIL')
```

### 8.5 What NOT to Commit

> Never commit credentials, passwords, connection strings, or personal access tokens. Never commit raw data files or query output files. These belong only in CA AZ or Databricks.

- No `.env` files or config files with passwords
- No raw data extracts (`.csv`, `.parquet`)
- No Databricks `.dbc` export files — commit `.ipynb` instead
- No personal scratch notebooks
- Add a `.gitignore` to exclude these automatically

---

## 9. Quick Reference Checklist

Before pushing to Git and updating the mastersheet:

| Check | Requirement |
|---|---|
| Jira ticket | In PO APPROVED state. ID in commit (current workspace) **or** filterable by `metric:` / `au:` labels (new workspace) |
| Notebook header | Metric, AU, owner, reviewer, date, status, output location all filled in |
| No nested SELECTs | Query is flat — no unnecessary subqueries |
| Only needed columns | `SELECT` lists only the columns the metric requires |
| Partition filter first | `WHERE` clause starts with date / partition filter |
| DQ check cell | Completeness % and reconciliation variance printed with explicit PASS/FAIL against the 95% threshold (see §8.4) |
| DQ threshold gate | If completeness < 95% or reconciliation variance > 5%, output NOT written — routed to NOT AVAILABLE / risk acceptance |
| Output confirmed | CA AZ table write confirmed; record count matches expectation |
| Mastersheet updated | Results in correct rows / columns of Excel mastersheet |
| Reviewer sign-off | Independent reviewer has confirmed mastersheet entries |
| Git commit | Correct format per cycle convention |
| No sensitive data | No passwords, tokens, raw data |

---

## 10. Common Mistakes & Fixes

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
| (new workspace) Missing JIRA labels | Audit recovery falls back to fragile keyword search | Add `metric:` and `au:` labels to every ticket |

---

## 11. Open Questions for Team Resolution

Items that the author was unable to confirm from the FY2025 workspace alone. Each is tagged by priority. Resolving the **P1** items is a prerequisite for locking the new workspace design; **P2** sharpens audit narrative; **P3** is cleanup-grade.

### 11.1 Workspace Organisation

| ID | Pri | Question | Why it matters |
|---|---|---|---|
| Q1 | P1 | What is the purpose of `LOBs/` (top-level) versus `Analysis/[LOB]/`? They have overlapping but non-identical LOB lists. | Determines whether `LOBs/` is a reference tier, alternate transformation tier, or duplication. Drives Section 3 layout. |
| Q3 | P2 | `SAS_DATA_LOAD` appears at two levels (top-level under `RiskAssessment` and inside `FY_2025`). Both active? Which is canonical? | Affects archive vs delete decision. |

### 11.2 Connections & Dependencies

| ID | Pri | Question | Why it matters |
|---|---|---|---|
| Q11 | P1 | Why does `Analysis/CBB/301069 Merchant Solution` call `/Users/priyanshi.chakraborty@td.com/GAML/GAMLConnections` instead of the shared `Configs/GAMLConnections`? Is there a functional difference, or is it leftover? | Determines whether user-folder GAML copies can be deleted or need to be merged into the shared version. |

### 11.3 Daily Touchbase 2026-05-13 — Items to Reconcile

The 2026-05-13 touchbase introduced proposals from the wider team that overlap with conventions already in this doc. Tom Wu's 13 May clarification resolves the per-AU transformation naming (see Section 3 and 7.1); other items still need confirmation before locking the new workspace design.

| ID | Pri | Proposal from touchbase | Status |
|---|---|---|---|
| Q23 | P1 | **File naming standard:** `<AU_UNIT_ID>_<SEG_NAME>_<Notepad details>_<date>.py`. | **Partially resolved (Tom Wu, 13 May 2026).** `03_Transformations/Per_AU/` uses the simpler `<AU_code>.ipynb` (e.g. `301069.ipynb`). The longer `<AU>_<SEG>_<flow>_<date>.py` pattern applies to per-stage AU notebooks under `01_Source_Ingestion/`, `02_Views/`, and `05_Outputs/`. Confirm whether the two-pattern split is acceptable or whether one convention should win across all stages. |
| Q24 | P2 | **Segment-based AU hierarchy:** `SEGMENT > AU > Notepad_<data_flow>`. | Currently implemented as `<LOB>/AU_<code>/` sub-grouping inside each lineage stage (see Section 3). Confirm SEGMENT vs LOB terminology — they appear interchangeable in the touchbase examples (`TDI`, `CBB`). |
| Q25 | P2 | **AZ data layout:** within CA AZ, organise output tables as `Source to AZ > AU`, `Views > AU`, `Transformation > AU`, `Output > AU`. | This is about how output **tables in CA AZ** are organised, distinct from how **notebooks in Databricks** are organised. Confirm whether this AZ layout is a separate concern or whether it should mirror the Databricks folder structure. |
