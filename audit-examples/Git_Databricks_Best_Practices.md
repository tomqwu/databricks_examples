# Git & Databricks Best Practices

**FCRM Risk Assessment — MCC Team**

| Attribute | Detail |
|---|---|
| Document Title | Git & Databricks Notebook Best Practices |
| Document Owner | FCRM Enterprise Risk Assessment Reporting Team |
| Effective Date | April 2026 |
| Version | 2.2 (supersedes v2.1). Restructured to lead with the As-Is and FY2026 folder trees. |
| Target Audience | MCC Developers, Team Leads, 1LOD, 2LOD, Internal Audit |
| Systems of Record | GitHub (`TD-Universe/RAFY2025_CA`) + Databricks + Jira (FY25 RA CYCLE - DATA) |

---

---

## 1. Purpose

This document defines the standards for writing, organising, and version-controlling Databricks notebooks and Git commits for the FCRM Risk Assessment cycle. It opens with the two folder trees that matter most for design decisions, then provides supporting detail.

- **Sections 2–4** — the As-Is FY2025 folder tree, the proposed FY2026 lineage-aligned folder tree, and the line-by-line mapping between them. These are the structural lead.
- **Section 5** — what to do now to close the FY2025 audit window cleanly without disrupting in-flight work.
- **Section 6** — other current facts about the FY2025 cycle (environment, naming, workload, active constraints).
- **Section 7** — FY2026 implementation detail (naming, JIRA hygiene, per-metric commits, ABAC handling, migration plan).
- **Sections 8–10** — cycle-independent standards, a checklist, and common mistakes.
- **Section 11** — open questions the author was unable to resolve from the workspace alone; these need team input before the FY2026 design can be locked.

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
  · Analysis/[LOB]/ABAC/[ABAC <AU>]          (per-AU ABAC, decentralized historical pattern — deprecated for FY2026)
    ↓
Data_Quality_Checks/Lobs/[AU DQ notebook]   (validation)
Data_Quality_Checks/TABLE_VIEW_CREATION/    (DDL infrastructure)
    ↓
Views (RA_FY25_VIEW catalogue) → Excel mastersheet
```

**Observations:**

- `Analysis/[LOB]/[AU notebook]` is one notebook per AU containing all metrics for that AU as separate cells (e.g., `301069 Merchant Solution` contains SD_1.0, SD_1.1, …).
- `Analysis/[LOB]/ABAC/` is a per-LOB subfolder with one ABAC notebook per AU (`ABAC 301069`, `ABAC 301451`, …) — **not** the cross-AU pattern Tom is targeting for FY2026.
- `Centralized Data/` is the existing precedent for "one notebook covers many AUs" — the closest current parallel to where ABAC should live.
- `LOBs/` is a different (broader) tier than `Analysis/[LOB]/` and contains LOBs not in `Analysis/` (e.g., `CPB(DIGITAL)`, `GMI -TDAM`, `NIU`, `TDS & Cowen 2025`). Purpose to be confirmed with Team Leads.

---

## 3. Folder Structure — FY2026 Recommended

**Design principle:** the folder structure should mirror the data lineage flow. An auditor tracing source → transformation → output should be able to walk the folder tree in the same order. This makes the workspace self-documenting and aligns directly with the V&QA SOP (Sujai) Step 2 (Data Quality Checks) and Step 6 (Output Verification).

**Lineage stages (FCRM RA cycle):**

```
[1] Configs & Catalogues          → schema, CDEs, connections
[2] Source Ingestion              → Rahona (SRZ/CZ) + ADIDO → CA AZ snapshot tables
[3] Views                         → stable read layer over snapshot tables
[4] Transformations               → per-AU + centralized + ABAC
[5] Data Quality Checks           → completeness, accuracy, reconciliation
[6] Outputs                       → CA AZ tables → Static Sheet → IRAT → Excel mastersheet
```

> **Note (Raghul, May 2026):** Views sit between ingestion and transformations — they are the stable interface that downstream metric notebooks read from. Putting Views immediately after ingestion in the folder tree mirrors the actual read path and keeps lineage traceable.

**Folder layout mapped to those stages:**

```
RAFY2026_CA/
├── 00_Configs/                          ← [1] catalogues, connections, CDE registry
│   ├── Catalogues/                      (Create_Adhoc, Create_Adido, Create_Analysis, etc.)
│   ├── Connections/                     (GAMLConnections, Settings)
│   └── CDE_Registry/                    (RA_BUSINESS_CDEs)
│
├── 01_Source_Ingestion/                 ← [2] source → CA AZ landing
│   ├── Rahona_SRZ/                      ← SRZ → ADLS ingestion notebooks
│   ├── Rahona_CZ/                       ← CZ → ADLS ingestion notebooks (e.g. CZ2ADLS 700005)
│   └── ADIDO_Load/
│
├── 02_Views/                            ← [3] stable read layer (RA_FY26_VIEW catalogue)
│   └── [LOB-segmented views]            (centralized notebooks read multiple LOB views; per-AU notebooks read one)
│
├── 03_Transformations/                  ← [4] business logic per metric (reads from 02_Views)
│   ├── Centralized/                     ← one notebook per metric, cross-AU
│   │   ├── Regular/                     ← ML/TF centralized metrics (LOB-differentiated sources, unified output)
│   │   │   ├── M1.1_Unscored_View.ipynb
│   │   │   └── M1.2_HRC_Tier12.ipynb
│   │   └── ABAC/                        ← always centralized across all 61 AUs (no LOB split, unified source)
│   │       ├── eba01.ipynb
│   │       ├── eba02.ipynb
│   │       └── _shared/
│   │           ├── abac_au_list.py      ← canonical 61-AU list
│   │           └── abac_utils.py
│   ├── Segment/                         ← grouping tier between Centralized and Per_AU (sub-populations / cross-AU groups)
│   └── Per_AU/                          ← per-AU dev work (2–3 AUs / dev)
│       ├── CBB/
│       │   ├── AU_301069_Merchant_Solution/
│       │   │   ├── M1.1_301069.ipynb
│       │   │   └── M1.2_301069.ipynb
│       │   └── AU_301451_CMS/
│       └── CPB/  GMI/  P_and_T/  TDGIS/  TDI/  TE_CE/  WEALTH/
│
├── 04_DQ_Checks/                        ← [5] validation layer
│
└── 05_Outputs/                          ← [6] what feeds the Excel mastersheet
```

> **Note (Raghul, May 2026):** ML/TF centralized metrics differ by LOB at the data-source level — the metric logic is centralized in one notebook, but the inputs come from LOB-specific views. The centralized notebook pattern is therefore: read multiple LOB-segmented views from `02_Views/`, apply the unified metric logic, then aggregate across LOBs into a single output.
>
> **Note (Tom Wu, May 2026):** ABAC centralized notebooks (`eba01`, `eba02`, …) are always centralized across all 61 AUs — no LOB differentiation at the source level. This is distinct from ML/TF Regular centralized notebooks above. ABAC reads a unified source against the canonical 61-AU list (`_shared/abac_au_list.py`) and produces a single output covering the full ABAC population.

**Why lineage-aligned beats workload-aligned:**

- An auditor opens `00_Configs/` first to understand the schema, then walks down to `05_Outputs/` to see what was produced. The folder tree itself answers the audit question "where did the data come from and how did it become this number?".
- Views (`02_Views/`) sit immediately after ingestion because transformations read from views, not raw snapshot tables. Putting Views before Transformations in the folder tree matches the actual data flow.
- The three transformation tiers — `Centralized/`, `Segment/`, and `Per_AU/` — all sit under `03_Transformations/` because they are the same lineage stage, just different workload scopes: cross-AU (Centralized), grouped sub-population (Segment), and single-AU (Per_AU). Centralized ≠ "single source"; it means "single notebook" that may aggregate LOB-segmented inputs.
- DQ Checks have a clear home as a distinct lineage stage rather than being scattered inside transformation notebooks (though notebook-level DQ cells stay — see Section 8.4).

---

## 4. As-Is → To-Be Mapping

Each existing FY2025 location maps to a target FY2026 location. This is a reorganisation, not a rewrite — every artifact moves to a stage that reflects its lineage role.

| FY2025 location | FY2026 location | Notes |
|---|---|---|
| `Configs/GAMLConnections` | `00_Configs/Connections/GAMLConnections` | All notebooks must `%run` from here only — no user-folder copies. |
| `Configs/Create_*_Catalogue` | `00_Configs/Catalogues/` | Adhoc, Adido, Analysis, Snapshot, View catalogues all sit here. |
| `Configs/RA_BUSINESS_CDEs` | `00_Configs/CDE_Registry/` | CDE registry. |
| `Configs/Settings` | `00_Configs/Connections/Settings` | Constants and parameters; co-located with connections. |
| `SRZ_TO_ADLS/[AU folder]/` (SRZ notebooks) | `01_Source_Ingestion/Rahona_SRZ/[AU folder]/` | SRZ → ADLS ingestion only. Split out from current mixed folder (Tom Wu, May 2026). |
| `SRZ_TO_ADLS/CZ2ADLS *` (CZ notebooks) | `01_Source_Ingestion/Rahona_CZ/[AU folder]/` | CZ → ADLS ingestion only. Currently mixed with SRZ ingestion in the FY2025 `SRZ_TO_ADLS/` folder; separated for FY2026 to reflect that Rahona has two distinct zones (Tom Wu, May 2026). |
| `ADIDO_OUT/` (top-level, no landing zone) | `01_Source_Ingestion/ADIDO_Out/` | Distinct from ADIDO IN — only IN has a landing zone. Confirmed Tom Wu, May 2026. |
| `Views/` | `02_Views/` | Renumbered to sit immediately after ingestion (Raghul, May 2026). Stable read layer over snapshot tables. |
| `Centralized Data/[metric notebook]` | `03_Transformations/Centralized/Regular/M<#.#>_<Descriptor>.ipynb` | Rename to metric-prefixed convention. Reads multiple LOB-specific views from `02_Views/` and aggregates into a single cross-AU output (Raghul, May 2026 — ML/TF centralized metrics differ by LOB at the source level). |
| *(new tier)* | `03_Transformations/Segment/` | New tier between Centralized and Per_AU (Tom Wu, May 2026). For transformations applied to a defined segment / sub-population / cross-AU grouping that is broader than a single AU but narrower than the full population. |
| `Centralized Data/ABAC/eba0X.ipynb` *(moved here during FY2025 closeout)* | `03_Transformations/Centralized/ABAC/eba0X.ipynb` | Source location after the closeout move described in 5.2. FY2026 just preserves it under the new top-level naming. Adds `_shared/abac_au_list.py`. |
| `Analysis/[LOB]/[AU notebook]` | `03_Transformations/Per_AU/[LOB]/AU_<code>_<Name>/M<#.#>_<au>.ipynb` | Single AU notebook splits into one notebook per metric inside an AU folder. AU-level analysis (incl. `700005 - centralized`, `nmm_transactions-2025`) reads from `02_Views/`. |
| `Analysis/[LOB]/ABAC/ABAC <AU>` | (deprecated) | Decentralized historical work by individual devs in past cycles, not a canonical pattern. Replaced by `03_Transformations/Centralized/ABAC/eba0X.ipynb` covering all 61 ABAC AUs in one notebook per metric. |
| `Data_Quality_Checks/Lobs/` | `04_DQ_Checks/Per_AU/[LOB]/` | Same pattern, renamed for consistency. |
| `Data_Quality_Checks/TABLE_VIEW_CREATION/` | `04_DQ_Checks/Infrastructure/` | DDL kept distinct from DQ logic. |
| `LOBs/` (top-level) | **To be confirmed with Team Leads** — keep as `06_LOB_Reference/` if it serves a distinct purpose, or merge into `03_Transformations/Per_AU/` if duplicative. | Open question; not blocking. |
| `RA_CDE_DQ_CHECKS/` (top-level) | Archive (FY2024 legacy) | Confirmed FY2024 DQ check tables (Tom Wu, May 2026). Move to FY2024 archive, not in FY2026 active tree. |
| `TEST_GITHUB`, `Sample_writing_result_into_table`, `Bit_Bucket_check_in_check_out`, `TestDF_Do_Not_Delete…`, etc. | Delete | Confirmed not in use (Tom Wu, May 2026). Safe to delete during FY2026 cleanup. |
| `BACKUP_FY_2024`, `FY_2023`, `FY_2024` | Archive outside the active workspace | Move to a separate archive workspace or repo. Not in active tree. |

---

## 5. End-of-Cycle Recommendations (FY2025 Audit Closeout)

The audit window is short and the FY2025 cycle is mid-flight. **Do not restructure folders, rename notebooks, or change commit conventions during this window.** The recommendations below are closeout-only and additive.

### 5.1 Do Not Disrupt

| Action | Status |
|---|---|
| Restructure Databricks folders | ❌ Defer to FY2026 |
| Rename notebooks (AU → metric-based) | ❌ Defer to FY2026 |
| Change commit format (drop `FY25DATA-XXX`) | ❌ Defer to FY2026 |
| Change branch naming | ❌ Defer to FY2026 |
| Reorganise ABAC across LOB folders | ❌ Defer to FY2026 |
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
- **GAMLConnections is invoked inconsistently.** Some notebooks reach into a user folder (`/Workspace/Users/.../GAML/GAMLConnections`) instead of the shared `Configs/GAMLConnections`. To be standardised in FY2026.
- **ABAC notebooks `eba01`, `eba02` were initially developed in `/Workspace/Users/qiang.wu@td.com/abac/`** rather than the shared workspace. **Resolved during this cycle:** moving to `Shared/RiskAssessment/FY_2025/Centralized Data/ABAC/` as part of audit closeout (see 5.2). This makes them visible in the shared tree before audit close.
- **Heterogeneous folder/notebook naming** and **test folders mixed with production**. Cleanup deferred to FY2026 cycle kickoff.

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

## 7. FY2026 Implementation Detail

> **Status: lineage-aligned design confirmed against FY2025 workspace.** Sections 3 and 4 above hold the target layout and as-is → to-be mapping. The subsections below cover naming, JIRA hygiene, per-metric commits, ABAC handling, and the migration plan.

### 7.1 Unified Naming Convention

A single convention applied at every level of the workspace and every Git artifact. The rules are designed so that a folder path or filename, read in isolation, tells the reader exactly what they are looking at.

**Folders:**

| Element | Pattern | Example |
|---|---|---|
| Top-level (lineage stage) | `NN_Title_Case_With_Underscores` | `00_Configs`, `03_Transformations`, `05_Outputs` |
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
6. **JIRA ticket IDs dropped from filenames, branches, and commits.** JIRA tickets are 1-to-1 with (metric, AU); embedding the ticket ID is redundant. Audit traceability moves to JIRA labels — see Section 7.2.

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

### 7.5 Migration Plan (Pre-FY2026 Kickoff)

1. **Confirm `LOBs/` purpose** with Team Leads — keep as reference tier (`06_LOB_Reference/`) or merge into `03_Transformations/Per_AU/`.
2. **Lock the lineage-aligned structure** with Team Leads and 1LOD before cycle kickoff.
3. **Pre-create** the `RAFY2026_CA` repository and seed the folder skeleton matching the six lineage stages.
4. **Standardise `GAMLConnections` invocations.** Inventory every notebook that calls `GAMLConnections`, replace any user-folder paths (`/Workspace/Users/.../GAML/GAMLConnections`) with the shared path. Going forward, only the shared path is permitted; user-folder copies should be deleted.
5. **ABAC notebooks already in shared workspace** at `Centralized Data/ABAC/` (moved during FY2025 closeout — see 5.2). FY2026 step is just renaming under the new lineage stage `03_Transformations/Centralized/ABAC/`.
6. **Delete test / scratch folders** (`TEST_GITHUB`, `Sample_writing_result_into_table`, `Bit_Bucket_check_in_check_out`, `TestDF_Do_Not_Delete…`, redundant `SAS_DATA_LOAD`) — confirmed not in use (Tom Wu, May 2026). Archive `BACKUP_FY_2024`, `FY_2023`, `FY_2024`, and `RA_CDE_DQ_CHECKS` (FY2024 legacy) outside the active workspace.
7. **Migrate** the canonical 61-AU list and shared utilities into `03_Transformations/Centralized/ABAC/_shared/` so all ABAC notebooks import a single source.
8. **Apply Jira labels retroactively** to a sample of FY2025 tickets to validate the filter recovery path before going live.
9. **Update** Change Management SOP, Audit Summary, and onboarding docs to reflect the new conventions.

---

## 8. Standards Carried Forward (Cycle-Independent)

These standards apply in both FY2025 and FY2026 cycles. They are technical hygiene that does not depend on folder structure or naming conventions.

### 8.1 Notebook Header (Mandatory)

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
| (FY2026) Missing JIRA labels | Audit recovery falls back to fragile keyword search | Add `metric:` and `au:` labels to every ticket |

---

## 11. Open Questions for Team Resolution

Items that the author was unable to confirm from the FY2025 workspace alone. Each is tagged by priority. Resolving the **P1** items is a prerequisite for locking the FY2026 design; **P2** sharpens audit narrative; **P3** is cleanup-grade.

### 11.1 Workspace Organisation

| ID | Pri | Question | Why it matters |
|---|---|---|---|
| Q1 | P1 | What is the purpose of `LOBs/` (top-level) versus `Analysis/[LOB]/`? They have overlapping but non-identical LOB lists. | Determines whether `LOBs/` is a reference tier, alternate transformation tier, or duplication. Drives Section 3 layout. |
| Q3 | P2 | `SAS_DATA_LOAD` appears at two levels (top-level under `RiskAssessment` and inside `FY_2025`). Both active? Which is canonical? | Affects archive vs delete decision. |

### 11.2 Connections & Dependencies

| ID | Pri | Question | Why it matters |
|---|---|---|---|
| Q11 | P1 | Why does `Analysis/CBB/301069 Merchant Solution` call `/Users/priyanshi.chakraborty@td.com/GAML/GAMLConnections` instead of the shared `Configs/GAMLConnections`? Is there a functional difference, or is it leftover? | Determines whether user-folder GAML copies can be deleted or need to be merged into the shared version. |

---
