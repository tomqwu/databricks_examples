# FCRM Risk Assessment FY2025 — Evidence Catalogue

| Attribute | Detail |
|---|---|
| **Document Title** | Evidence Catalogue — Inputs, Outputs and Audit Artifacts |
| **Document Owner** | FCRM Enterprise Risk Assessment Reporting Team |
| **Effective Date** | May 2026 |
| **Version** | 1.0 |
| **Target Audience** | 1LOD, 2LOD, 3LOD (Internal Audit), Regulatory Reviewers, MCC developers |
| **Pairs with** | Audit Summary v1.3 · Process Inventory · Git & Databricks Best Practices v2.8 |

## Purpose

A single reference listing every named input, output and evidence artifact across the FY2025 Risk Assessment cycle, organised by category. Use this to look up **what something is, what it contains, where it lives, and which process step(s) produce or consume it.** The Audit Summary tells the story; this catalogue is the dictionary.

---

## 1. Source Data Systems

- **Rahona (SRZ / CZ)** — TD's enterprise source data warehouse. SRZ = Secured Raw Zone; CZ = Consumption Zone. 20 data sources feed the RA cycle from Rahona, pulled to CA AZ on **1 November 2025** as the fixed RA25 snapshot. Read-only to MCC team.
- **ADIDO** — Business-managed file repository for data not in Rahona. 73 data sources from ERA and business points of contact. Loads tracked via the 2025 ADIDO Load Files register.
- **CA AZ (Canada Analytical Zone)** — Working storage for extracted datasets (.csv / .parquet), ADIDO data, and CDE logic query output tables. All MCC query input/output materialises here. Retention currently undefined — open gap.
- **caedw.acct_trans** — Specific Rahona transaction table used by several metric queries. Partitioned by `post_dt`.
- **ra_fy_2025.* views** — Cycle-scoped Databricks views over source data, populated from the 1 November 2025 snapshot.

## 2. Storage & Tools

- **Databricks** — Single notebook query environment for MCC team. No DEV / PROD split. All Python / SQL / PySpark queries are written, executed and validated here.
- **GitHub — `TD-Universe/RAFY2025_CA`** — Version control for finalised queries. **Audit record only — not used for deployment.** Commits must reference a Jira ticket ID in the form `[FY25DATA-XXX]`.
- **SharePoint — FCRM Risk Assessment Interactive Site** — Primary document and evidence repository. Folder structure under `04 Metric Documentation > METRIC RA TEAM - 2026` (folders 01–08 by process).
- **Excel mastersheet** — Authoritative output record for the cycle. Final metric values per AU. Stored in SharePoint `06 - Change Management / Evidence`. Updated only after a validated Databricks run with independent reviewer sign-off.
- **Jira project — `FY25 RA CYCLE - DATA`** — Workflow system of record. All metric stories, state transitions, decisions, RAID entries and approvals flow here.

## 3. Controlling Documents (SOPs)

- **Delivery Process SOP v2.1** — Standard for the 9-step delivery workflow (Intake through Document Output).
- **QA & Governance Standard SOP v2.1** — Standard for both V&QA (8 steps) and Governance (8 steps). **Source of the 95% data-quality threshold rule** (subject to confirmation — see §6 note).
- **Data Sourcing & Lineage SOP v2.1** — Standard for the 7-step sourcing / lineage workflow.
- **Access Control SOP** — Standard for the 3-step PIA / access / matrix workflow.
- **Change Management SOP v1.1** — Standard for the 7-step change workflow. Tom Wu owner.
- **Output Validation Document v1.1** — Validation reference detail.
- **Approvals Document v1.1** — Approval workflow reference.
- **Git & Databricks Best Practices v2.8** — Coding standards: notebook header template, performance rules, DQ availability pattern, Git commit conventions, FY2025 closeout folder structure.

## 4. Working / Reference Documents

- **Scope Statement of Work (Live).docx — SOW v1.32** — Authoritative scope reference. Owned by Richard Ng. Updated weekly on a Thu→Fri→Mon→Tue cadence. All in-scope metrics, AUs, assumptions and exclusions are logged here. Cited as evidence for both Delivery Step 1 (Scope) and Change Mgmt Step 7 (Scope Change Log).
- **Master_Data_source_FY2025_Segment.xlsx** — Per-metric source identification log. One row per CDE: AU, metric, source system, source table, owner. Drives data acquisition and DQ scoping. Cited at Data Sourcing Step 1.
- **FCRM Master Process Inventory FY2025.xlsx** — Live Process Inventory in SharePoint. One row per step across all 6 processes: process, sub-process, step #, step name, owner, inputs, actions, outputs, Evidence 1, Evidence 2, Jira state, SOP reference.
- **Evidence Tracker FY2025.xlsx** — Cross-process status (✅ / 🟡 / ❌) of every evidence artifact required for audit.
- **Audit Summary v1.3** — Plain-language audit-readable summary of all 6 processes and their controls.
- **DCT (Data Control / Capture Template)** — Standard intake artifact capturing purpose, CDEs, AUs, expected output, timelines. Referenced at Delivery Steps 0, 2, 3, 4 and 5. *(Exact full-name expansion to confirm.)*
- **Tech Spec Document** — Technical specifications per metric: source systems, source tables / columns, business definitions, criticality. Currently in progress — open gap per Audit Summary §9.

## 5. Code & Query Artifacts

- **Notebooks (Databricks)** — Individual notebooks per metric. Mandatory header (Jira ticket ID, metric, owner, reviewer, date, status, output location) and `[LINEAGE]` cells documenting Source / Business Logic / Output definitions.
- **Notebooks or ExtractionScripts** — Code used during Data Acquisition (Delivery Step 2).
- **Notebooks or Code Files** — Code produced during Logic Development (Delivery Step 3).
- **DEV Query Static Sheet** — Snapshot of validated query results used at Output Validation (Delivery Step 5).
- **Git commits — `TD-Universe/RAFY2025_CA`** — Per-change audit record. Required after PO APPROVED. Commit message format `[FY25DATA-XXX] description`.

## 6. DQ Pattern Artifacts (Validation & QA Step 2)

- **`RA_FY_2025.cde_da_by_lob_segment`** — Central availability table. Columns: `LOB_ID, LOB_DESC, CDE_NO, SOURCE, SRC_TABLE_NAME, DATA_ELEMENT, AVAILABILITY_PCT, today_date`. Accumulates one row per DQ measurement per run. The per-cycle history of every CDE's data quality.
- **`insertDQTable(…)`** — Python helper that writes one row to `cde_da_by_lob_segment` per measurement. Used by every metric notebook.
- **`availability_pct`** — The DQ measure. `round(100 * NNNBV / total, 2)`. 0–100 scale. **95% threshold gate** decides whether the CDE can feed Inherent Risk (≥ 95 passes; < 95 routes to NOT AVAILABLE / risk acceptance).
- **NNNBV** — "Not Null, Not Blank Value" count. Records where the cast field `IS NOT NULL AND <> ''`. The numerator of availability_pct.
- **`LOB -- TDI-- 101522`** — Reference DQ notebook in the live workspace (TD General Insurance). Canonical template other metric notebooks follow.
- **`Create_Data_Ava_Table_Segment` / `Create_Data_Ava_Table_Common_Adido_SRZ_…` / `Create_Data_Quality_Table_Entrps_Data`** — Notebooks that create and maintain the central DQ availability tables.
- *Source-of-policy note:* the 95% threshold carries forward from Audit Summary v1.2 and isn't explicitly cited in the V&QA SOP — controlling source still being traced. Pattern is policy-agnostic; only the comparison constant changes if confirmed otherwise.

## 7. Jira Workflow States (state-as-evidence)

States are themselves audit evidence — they prove which control gate was cleared and when.

- **BUSINESS LOGIC DESIGN DEF** — Initial business logic / metric definition captured. Required before any Databricks work.
- **BUSINESS LOGIC SEMANTIC** — Semantic refinement of business logic.
- **METRIC DEFINITION CLARIFICATION** — Ambiguities, default thresholds, proxy-data assumptions logged.
- **BAU CDE DOCUMENTATION** — BAU CDE state recorded.
- **DATA SOURCE(S) IDENTIFIED** — Sources confirmed per metric.
- **DAC OR ADIDO LOAD PROCESS** — Data load triggered.
- **DATA PROVISIONED IN AZ** — Data has landed in CA AZ.
- **BUILD IN PROGRESS (PART / FULL)** — Query under construction (cannot enter without DQ Steps 3–7 cleared).
- **BUILD COMPLETE** — Query validated, ready for review.
- **AU REVIEW APPROVAL** — Reviewer signed off at AU level.
- **PO CONCURRENCE** — Product Owner concurred with the change (Change Mgmt Step 3 gate).
- **PO APPROVED** — Final approval. Triggers GitHub push.
- **PIA BUILD → WITH PRIVACY TEAM → PIA APPROVED** — Privacy assessment chain.
- **BLOCKED** — Active impediment. Requires a RAID log entry to enter; resolution required to leave.
- **NO LONGER REQUIRED** — Metric / AU retired (historical traceability preserved).
- **NOT APPLICABLE** — Metric / AU N/A to the unit (e.g. CTR/LCTR for a unit with no cash in/out).
- **NOT AVAILABLE** — Data below 95% threshold and formally risk-accepted. Triggers higher Inherent Risk rating for the impacted AU rather than artificially suppressing the value.

## 8. PIA & Access Control Records

- **Canada Privacy Impact Assessment (PIA)** — Privacy assessment document per data source. Required before any data load.
- **Request PIA for AZ Load** — Form requesting PIA prior to a CA AZ data load.
- **DAC Submitted PIAs Canada** — Data Access Council (TD-internal abbreviation — to confirm) submission record across all data sources.
- **ADIDO SST Data FY2025 CA** — ADIDO source / system tracking data for the Canadian cycle.
- **Canada PIA Request Status (Jira)** — Live tracker of PIA approvals.
- **2025 PIA Approval Emails** — Email confirmations from the Privacy Team — Data Sourcing Step 2 evidence.
- **Canada Foundational Tracker** — Access control matrix. Records who has access to which systems / datasets / environments, plus segregation-of-duties documentation.

## 9. Validation & QA Outputs

- **Validation Plan Document** — V&QA Step 1. Scope, datasets, target systems, expected outputs.
- **Risk Assessment Matrix** — V&QA Step 1. Key controls and risk areas identified.
- **DQ check results** — V&QA Step 2. The per-CDE availability rows in `cde_da_by_lob_segment`.
- **Profiling reports** — V&QA Step 2. Statistical profile of source data.
- **Issue log** — V&QA Step 2. List of data-quality issues identified during checks.
- **Reconciliation reports** — V&QA Step 3. Source vs processed record-count reconciliation.
- **Variance analysis logs** — V&QA Step 3. Investigation of count / value variances.
- **Trend analysis report** — V&QA Step 4. Cross-cycle and cross-AU trend.
- **Outlier detection log** — V&QA Step 4. Records of identified outliers.
- **Threshold validation report** — V&QA Step 4. Confirms calculation thresholds are met.
- **Peer review sign-off** — V&QA Step 5. Reviewer's documented approval. Reviewer must be independent of preparer.
- **Review comments log** — V&QA Step 5. Comments raised and how they were resolved.
- **Output verification report** — V&QA Step 6. Format, structure, key calculations meet regulatory requirements.
- **Format compliance log** — V&QA Step 6. Output format compliance check.
- **RAID log entry / BLOCKED Jira ticket** — V&QA Step 7. New row in the RAID register and ticket transition.
- **Signed approval record** — V&QA Step 8. Final sign-off from approver.
- **Final validation report** — V&QA Step 8. End-of-cycle validation summary.

> Current status: all V&QA evidence artifacts are MISSING — Sujai to produce (Audit Summary §9).

## 10. Governance & Issue Outputs

- **Jira decision tickets (BUSINESS LOGIC DESIGN DEF)** — Governance Step 1. All business-logic / methodology decisions captured in Jira.
- **Jira assumption tickets (METRIC DEFINITION CLARIFICATION)** — Governance Step 2.
- **RAID log entry + BLOCKED Jira ticket** — Governance Step 3.
- **RAID log with P1 / P2 / P3 classification** — Governance Step 4. P1 = critical data gap, P2 = systemic failure, P3 = localised logic discrepancy.
- **Jira escalation comments + 2LOD notification** — Governance Step 5. Escalation chain: Developer → Team Lead → Project Manager → Business Stakeholders / 2LOD. Verbal escalations are not sufficient.
- **RAID log closure + Jira state off BLOCKED** — Governance Step 6.
- **Risk acceptance record + NOT AVAILABLE Jira state** — Governance Step 7. Formal stakeholder sign-off when data is below the 95% threshold.
- **Jira state transitions (NO LONGER REQUIRED / NOT APPLICABLE) + SOW change log** — Governance Step 8. Historical traceability of retired metrics / AUs.

## 11. Change Management Outputs

- **Jira change ticket** — Change Mgmt Step 1. Must reach BUSINESS LOGIC DESIGN DEF before any Databricks work.
- **Impact assessment notes (in Jira)** — Change Mgmt Step 2. Documented in ticket comments, not in email or chat.
- **PO CONCURRENCE Jira state + approver sign-off** — Change Mgmt Step 3. Approver must be independent of requester (Team Lead or Product Owner).
- **Validated Databricks query results** — Change Mgmt Step 4. Query output reviewed before mastersheet update.
- **Updated Excel mastersheet + independent reviewer sign-off + PO APPROVED** — Change Mgmt Step 5.
- **Git commit (`TD-Universe/RAFY2025_CA`)** — Change Mgmt Step 6. Per-change record with `[FY25DATA-XXX]` format and one logical change per commit.
- **SOW v1.32 weekly change log entry** — Change Mgmt Step 7. Owned by Richard Ng. Thu→Fri→Mon→Tue update cadence.

## 12. Aggregated Evidence Files (snapshots)

- **RAID Log Export.xls** — Periodic export of the live RAID log. Used as a point-in-time evidence artifact for audit.
- **Metric (JIRA) exports (×2)** — Two exports per process, snapshotting Jira state at a point in time. Per Audit Summary, exists for Delivery and Governance.
- **Evidence folder (per process)** — SharePoint sub-folder under each `0X - Process Name` containing the snapshot exports and approval records for that process.

## 13. Acronyms & Glossary

| Term | Expansion / meaning |
|---|---|
| AU | Assessable Unit (35 in scope for FY2025) |
| CDE | Critical Data Element |
| 1LOD / 2LOD / 3LOD | First / Second / Third Line of Defence (Business / Risk / Internal Audit) |
| PIA | Privacy Impact Assessment |
| PO | Product Owner |
| SOW | Statement of Work |
| RAID | Risks, Assumptions, Issues, Dependencies |
| DCT | Data Control / Capture Template *(full name to confirm)* |
| DAC | Data Access Council *(TD-internal abbreviation — to confirm)* |
| SRZ / CZ | Secured Raw Zone / Consumption Zone (Rahona zones) |
| SST | Source-System Tracking *(ADIDO context — to confirm)* |
| ABAC | Anti-Bribery & Anti-Corruption (Work Package WP-04) |
| BAU | Business As Usual |
| NNNBV | Not Null, Not Blank Value (DQ measure) |
| BDE | Business Data Element |
| IR / IRAT | Inherent Risk / Inherent Risk Assessment Template |
| MCC | The data delivery team (FCRM Risk Assessment Reporting) |

## 14. Open Items to Confirm

A handful of items in this catalogue I'd like you to confirm so the dictionary is precise:

1. **DCT** — full-name expansion (Data Control Template vs Data Capture Template vs something else).
2. **DAC** — TD-internal acronym (Data Access Council? Data Access Committee?).
3. **SST** in `ADIDO SST Data FY2025 CA` — confirm expansion.
4. **95% threshold** — locate the authoritative source (V&QA SOP v2.1 section, or a TD-wide DQ policy).
5. **Data retention policy for CA AZ** — currently undefined; if a policy exists outside MCC's view, please flag.

