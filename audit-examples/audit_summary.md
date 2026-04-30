# FCRM Risk Assessment FY2025 — Audit Summary

**Document Title:** Risk Assessment FY2025: How We Work  
**Team:** FCRM Enterprise Risk Assessment Reporting — MCC Team  
**Owner:** FCRM Enterprise Risk Assessment Reporting Team  
**Effective Date:** April 2026  
**Version:** 1.2  
**Classification:** Internal  
**Target Audience:** 1LOD, 2LOD, 3LOD (Internal Audit), Regulatory Reviewers  

---

## 1. Purpose

This document provides a plain-language summary of how the MCC Team delivers the FY2025 Anti-Money Laundering (AML) and Sanctions Risk Assessment. It gives audit reviewers a complete picture of our processes, controls, team structure, systems of record, and where evidence can be found.

This document answers five core audit questions for every process we own:

1. What is the process or control?
2. Who owns it, and how is segregation of duties maintained?
3. What happens at each step, including pre-requisites and outputs?
4. What evidence is generated?
5. Where is the evidence stored?

---

## 2. Scope

The MCC Team is responsible for **data delivery only** — sourcing, extracting, transforming, and delivering metric values for the annual Risk Assessment cycle. Business logic and methodology decisions are owned and approved by First Line (1LOD).

### 2.1 Work Packages

| Work Package | Description | Metrics | Assessable Units | Jira Stories |
|---|---|---|---|---|
| WP-01 | Inherent Risk BDEs | 52 | 35 | 1,820 |
| WP-02 | Inherent Risk Supplemental | 12 | 35 | 420 |
| WP-03 | Control Assessment Metrics | 4 | 35 | 140 |
| WP-04 | ABAC (Anti-Bribery Anti-Corruption) | 22 | 35 | 220 |
| **Total** | | **86 metric definitions** | **35 AUs** | **2,240 instances** |

### 2.2 Risk Categories Covered

- Customer Risk
- Products & Services Risk
- Transaction Volume & Value
- Account Originations
- Geographic Presence
- Emerging Risk
- Control Assessment (KYC, Investigation, Reporting)
- Anti-Bribery Anti-Corruption (ABAC)

### 2.3 Key Constraints

- Data quality < 95% and not provided by business → Inherent Risk factor = **"Not Available"**
- Data marked **"Exempt"** → MCC team cannot write queries
- Data **"Not Applicable"** to unit's model → MCC team cannot write technical queries (e.g., no cash in/out = CTR/LCTR is N/A)

---

## 3. Team Structure & Ownership

| Person | Processes Owned |
|---|---|
| Amandeep Singh Arora | Delivery Process (Steps 0–4), Data Sourcing & Lineage (Steps 5–7) |
| Karthik | Delivery Process (Steps 5–8), Data Sourcing & Lineage (Steps 1–4) |
| Sujai | Validation & QA (all steps 1–8) |
| Patty | Governance (Steps 1–4), Access Control & Security (Steps 1–3) |
| Tom Wu | Governance (Steps 5–8), Change Management (all steps) |
| Richard Ng | SOW ownership, weekly scope updates |

**Segregation of duties:** Reviewers cannot be the same individual as the preparer. All approvals require a Team Lead or Product Owner, independent of the change requester.

---

## 4. Systems of Record

| System | Purpose | What Lives Here |
|---|---|---|
| **Jira** (FY25 RA CYCLE - DATA) | Primary system of record for execution | All metric stories, workflow state transitions, decision logs, blockers, approvals |
| **SharePoint** (FCRM Risk Assessment Interactive Site) | Document & evidence storage | SOPs, process docs, evidence artifacts |
| **CA AZ** (Canada Analytical Zone) | Data storage | Extracted datasets (.csv, .parquet), ADIDO data, CDE logic query output tables |
| **Rahona** (SRZ/CZ) | Source data warehouse | 20 data sources — data pulled to AZ on 1 November 2025 |
| **ADIDO** | Business-managed files | 73 data sources from ERA and business point of contacts |
| **Databricks** | Single query environment | All notebooks and queries — no DEV/PROD split |
| **GitHub** (`TD-Universe/RAFY2025_CA`) | Query version control & audit record | Finalized query files with Jira ticket IDs in commit messages |
| **Excel Mastersheet** | Authoritative output record | Final metric results per AU, updated after each validated Databricks query run |
| **SOW** (`Scope Statement of Work (Live).docx`) | Scope reference | Weekly scope, metric definitions, AU mapping, assumptions & decisions |

---

## 5. Processes Overview

### 5.1 Delivery Process

**SOP:** Delivery Process for AML v2.1 | **SharePoint:** `01 - Delivery Process`

| Step | Name | Owner | Key Actions | Artifacts |
|---|---|---|---|---|
| 0 | Intake Request | Amandeep | Raise intake with purpose, AUs in scope, expected output and timelines. Identify CDEs (ERA/FCRM/Business). Initial review (1a/1b/BAs). IR review and challenge with core business. | DCT, Jira ticket |
| 1 | Scope / Requirement Definition | Amandeep | Identify CDEs required to close RA FY2025 cycle. Deter ML/TF/sanctions misuse. | SOW |
| 2 | Data Acquisition | Amandeep | Source from Rahona (SRZ/CZ) and ADIDO. Data pulled to AZ 1 Nov 2025. Validate integrity and completeness. | DCT, Notebooks |
| 3 | Logic Development (Build) | Amandeep | Define, document, implement business and technical rules. CDE identification, business definition, source data mapping. | DCT, Notebooks |
| 4 | Technical Specification (Build) | Amandeep | Document CDE specs, source systems, source tables/columns, business definition, criticality. | DCT, Tech Spec Doc (in progress) |
| 5 | Output Validation | Karthik | Validate output against expected results. Cross-check with source data. Verify format meets regulatory requirements. | DCT, Static Sheet |
| 6 | Approval | Karthik | Obtain PO Concurrence. Transition Jira to PO APPROVED. Independent reviewer required. | Evidence folder |
| 7 | Deployment | Karthik | Deploy metric outputs. Record deployment. Confirm successful release. | Evidence folder |
| 8 | Delivery / Document Output | Karthik | Deliver final metric outputs. Document results. Store in IRAT. | Evidence folder |

**Jira States:** `BUSINESS LOGIC DESIGN DEF` → `DATA SOURCE(S) IDENTIFIED` → `DATA PROVISIONED IN AZ` → `BUILD IN PROGRESS (PART)` → `BUILD IN PROGRESS (FULL)` → `BUILD COMPLETE` → `AU REVIEW APPROVAL` → `PO CONCURRENCE` → `PO APPROVED`

**Evidence path:** `04 Metric Documentation > METRIC RA TEAM - 2026 > 01 - Delivery Process > Evidence`
**Evidence files:** Metric (JIRA) exports (x2), RAID Log Export.xls — uploaded by Amandeep, April 15

---

### 5.2 Validation & Quality Assurance

**SOP:** QA & Governance Standard v2.1 | **SharePoint:** `02 - Validation & QA`

> **Execution Gating Rule:** A ticket cannot transition to BUILD IN PROGRESS or BUILD COMPLETE until all prerequisite logic, privacy, and data QA checks (Steps 3–7 below) are cleared.

| Step | Name | Owner | Key Actions | Artifacts |
|---|---|---|---|---|
| 1 | Validation Planning & Decision Traceability | Sujai | Define structured approach. Identify datasets, target systems, expected outputs per WP. Used when decisions are high-risk or defensibility for audits is needed. | Validation Plan Document, Risk Assessment Matrix |
| 2 | Decision & Assumption Logging | Sujai | All business logic decisions logged in Jira (BUSINESS LOGIC DESIGN DEF + BUSINESS LOGIC SEMANTIC). Assumptions logged in METRIC DEFINITION CLARIFICATION or BAU CDE DOCUMENTATION. | Jira tickets |
| 3 | Data Quality Checks & Sourcing | Sujai | Completeness (no missing/null critical fields), data type issues (date format, masked restricted fields), eliminate duplicates, check impacted fields only. Accuracy: validate against source (95% threshold). Consistency & Uniqueness across AU populations. Sourcing lineage tracked via DATA SOURCE(S) IDENTIFIED and DAC OR ADIDO LOAD PROCESS Jira states. | DQ check output files, profiling reports |
| 4 | Reconciliation | Sujai | BA's provide numbers + Dev Team provides numbers → DCT/Static Sheet reconciles → IRAT. Reconcile record counts, validate financial metrics, identify and investigate variances. | Reconciliation Reports, Variance Analysis Logs |
| 5 | Reasonability Analysis | Sujai | Trend & Outlier Analysis across Assessment Cycle. Threshold Validation. Methodology Alignment: compare current hard-data against historical proxy data/questionnaires to identify methodology shifts. | Reasonability analysis report |
| 6 | Peer Review & Compliance Checks | Sujai | Assign independent reviewer. Privacy compliance: PIA BUILD → WITH PRIVACY TEAM → PIA APPROVED before final data execution. Document review comments and resolutions. Jira transitions to AU REVIEW APPROVAL. | Peer review sign-off, AU REVIEW APPROVAL Jira state |
| 7 | Output Verification | Sujai | Pre-Execution Check: verify format, structure, key calculations against regulatory requirements. Execution gating: cannot proceed to BUILD states until Steps 3–7 cleared. | Output verification report |
| 8 | Sign-Off, Risk Acceptance & Decommissioning | Sujai | Formal Approval Gates: PO CONCURRENCE → PO APPROVED. Risk Acceptance: data below threshold → NOT AVAILABLE → higher risk rating for AU. Decommissioning: NO LONGER REQUIRED or NOT APPLICABLE. | Signed approval record |

> ⚠️ **Current status:** All Validation & QA evidence artifacts are currently **Missing** — Sujai to produce.

---

### 5.3 Data Sourcing & Lineage Management

**SOP:** Data Sourcing and Lineage for AML Process v2.1 | **SharePoint:** `03 - Data Sourcing & Lineage`

| Step | Name | Owner | Key Actions | Artifacts |
|---|---|---|---|---|
| 1 | Source Identification | Karthik | Obtain business requirements, metric definitions and SOW. Create Master Data Source Sheet per metric. Collaborate with business stakeholders. | `Master_Data_source_FY2025_Segment.xlsx` |
| 2 | Access Enablement | Karthik | Initiate PIA per data source. Submit access requests. Track and follow up on approvals. Maintain records of access permissions and compliance checks. | `2025 PIA Approval Emails` |
| 3 | Data Extraction | Karthik | Connect to Rahona (20 sources) and ADIDO (73 sources). Extract relevant data fields. Store in CA AZ. Validate integrity and completeness post-extraction. | `2025 ADIDO Load Files` |
| 4 | Data Understanding | Karthik | Create database views or data models. Profile datasets. Document data definitions, data types, key attributes. Identify and address data quality issues. | `2025 Approved Metadata Templates` |
| 5 | Lineage Documentation | Amandeep | Define scope across AUs/Segments for all CDEs. Map data flow. Document transformations. Map data fields (CDEs) from source to target (Point of Consumption). | **WIP — MCC team does not have this yet** |
| 6 | Refresh Management | Amandeep | On-demand refresh (not fixed schedule). Document all refresh activities. Validate data integrity after each refresh. | **Missing** |
| 7 | Data Retention | Amandeep | Follow data retention policy for datasets stored in AZ environment. Periodically review organizational and regulatory requirements. | **No defined retention policy** — datasets stored in CA AZ without a defined retention period |

> ⚠️ **Data retention note:** Currently no defined retention policy MCC team is aware of — datasets are stored in CA AZ without a defined retention period.

---

### 5.4 Governance, Decision & Issue Management

**SOP:** QA & Governance Standard v2.1 | **SharePoint:** `04 - Governance & Issue Management`

| Step | Name | Owner | Key Actions | Artifacts |
|---|---|---|---|---|
| 1 | Decision Logging | Patty | All business logic, scoping, and methodological decisions captured in Jira. Unlogged out-of-band decisions not permitted. Ticket must be in BUSINESS LOGIC DESIGN DEF and BUSINESS LOGIC SEMANTIC states. | Jira tickets — Evidence folder |
| 2 | Assumption Tracking | Patty | Ambiguities, default thresholds, or proxy data assumptions formally documented. Resolved in METRIC DEFINITION CLARIFICATION or BAU CDE DOCUMENTATION state. | Jira tickets — Evidence folder |
| 3 | Issue Logging | Patty | Immediate transition to BLOCKED + RAID log entry (Risks, Assumptions, Issues, Dependencies). | RAID Log, Jira BLOCKED ticket |
| 4 | Severity Assessment | Patty | P1 = critical data gaps, P2 = systemic failures, P3 = localized logic discrepancies. | RAID Log with severity |
| 5 | Escalation Pathways | Tom Wu | Developer → Team Lead → Project Manager → Business Stakeholders / 2LOD. Escalations must categorize blocker type. All escalations documented in Jira ticket comments and RAID log — verbal escalations not sufficient. | Jira comments, 2LOD notification |
| 6 | Resolution & Unblocking | Tom Wu | Issue formally resolved only when marked "Closed" in RAID log. Only then may Jira ticket leave BLOCKED and proceed to READY FOR FINAL REVIEW. | RAID log closure, Jira state transition |
| 7 | Risk Acceptance | Tom Wu | Data below threshold → formally risk-accepted by all key stakeholders → NOT AVAILABLE Jira state → triggers higher risk rating for impacted AU (prevents artificial suppression of Inherent Risk). | Risk acceptance record |
| 8 | Decommissioning & Sign-Off | Tom Wu | Formal Approval Gates: PO CONCURRENCE → PO APPROVED. Retired metrics/AUs → NO LONGER REQUIRED or NOT APPLICABLE (historical traceability maintained). | Jira state transitions, SOW change log |

> ✅ **Current status:** All Governance evidence exists.  
> **Evidence path:** `04 Metric Documentation > METRIC RA TEAM - 2026 > 04 - Governance & Issue Mgmt > Evidence`  
> **Evidence files:** Metric (JIRA) exports (x2), RAID Log Export.xls — uploaded by Tom Wu, April 15

---

### 5.5 Access Control & Security

**SOP:** Access Control SOP | **SharePoint:** `05 - Access Control & Security`

| Step | Name | Owner | Key Actions | Artifacts |
|---|---|---|---|---|
| 1 | PIA Initiation | Patty | Initiate PIA per data source. PIA BUILD → WITH PRIVACY TEAM → PIA APPROVED before final data execution. | Canada Privacy Impact Assessment (PIA) |
| 2 | Access Request & Approval | Patty | Submit access requests for all required systems. Track and follow up on approvals. Maintain records for audit. | Request PIA for AZ Load; DAC Submitted PIAs Canada; ADIDO SST Data FY2025 CA; Jira — Canada PIA Request Status |
| 3 | Access Control Matrix | Patty | Maintain access control matrix. Document who has access to which systems. Document segregation of duties. | Canada Foundational Tracker |

> ✅ **Current status:** All Access Control evidence exists.

---

### 5.6 Change Management & Version Control

**SOP:** Change Management and Version Control v1.1 | **SharePoint:** `06 - Change Management`  
**System of Record:** Jira (FY25 RA CYCLE - DATA) + GitHub + SharePoint

**Developer workflow:** Databricks (write/run/validate query) → SharePoint (save query doc) → Excel mastersheet (update results) → GitHub (push final query as audit record — not deployment)

> **Key governance rule:** All business logic and methodology decisions must be formally captured in Jira. Unlogged decisions cannot be considered authoritative and will be flagged as audit findings.

| Step | Name | Owner | Key Actions | Artifacts |
|---|---|---|---|---|
| 1 | Change Request | Tom Wu | Raise Jira ticket before any Databricks work. Ticket must reach BUSINESS LOGIC DESIGN DEF before work begins. | Jira change ticket |
| 2 | Impact Assessment | Tom Wu | Assess impact on metrics, AUs, and mastersheet outputs. All findings documented in Jira ticket — not email or chat. | Impact assessment notes in Jira |
| 3 | Change Approval | Tom Wu | Team Lead or Product Owner sign-off. Approver must be independent of change requester. Recorded via PO CONCURRENCE Jira state + approver comment. | Approved Jira ticket |
| 4 | Build in Databricks | Tom Wu | Write or modify query in Databricks (single environment — no DEV/PROD). Run query. Validate output results against expected values and prior cycle. | Validated query results in Databricks |
| 5 | Result Update | Tom Wu | Copy validated results into Excel mastersheet. Get independent reviewer sign-off. Document in Jira (date, who ran, what changed). Transition to PO APPROVED. | Updated Excel mastersheet — SharePoint: 06 Change Management / Evidence |
| 6 | Push Query to Git | Tom Wu | Push final query file to GitHub with Jira ticket ID in commit message. Git is the audit record — not used for deployment. | `https://github.com/TD-Universe/RAFY2025_CA` |
| 7 | Scope Change Logging | Tom Wu | Log all scope changes in SOW v1.32. Cadence: Thu → Fri → Mon → Tue (Jira Kanban updated). | `Scope Statement of Work (Live).docx` |

> ✅ **Current status:** All Change Management evidence exists.

**Jira States:** `BUSINESS LOGIC DESIGN DEF` → `PO CONCURRENCE` → `BUILD IN PROGRESS` → `BUILD COMPLETE` → `PO APPROVED`

---

## 6. Evidence Summary

| Process | Status | Primary Evidence | SharePoint Location |
|---|---|---|---|
| Delivery | ✅ Exists | DCT, Jira exports, RAID Log Export.xls | `01 - Delivery Process / Evidence` |
| Validation & QA | ❌ Missing | DQ outputs, reconciliation reports, peer review sign-offs | `02 - Validation & QA / Evidence` — to be produced by Sujai |
| Data Sourcing & Lineage | 🟡 Partial | Master data source sheet, PIA records, ADIDO load files, metadata templates | `03 - Data Sourcing & Lineage / Evidence` — Lineage WIP, Retention gap |
| Governance | ✅ Exists | Jira exports (x2), RAID Log Export.xls | `04 - Governance & Issue Mgmt / Evidence` |
| Access Control | ✅ Exists | PIA approvals, Canada Foundational Tracker, Canada PIA Request Status | `05 - Access Control / Evidence` |
| Change Management | ✅ Exists | Jira tickets, Databricks query outputs, Excel mastersheet, GitHub commit history, SOW | `06 - Change Management / Evidence` |

---

## 7. SharePoint Structure

All audit documentation is stored in **FCRM Risk Assessment Interactive Site** under:

```
04 Metric Documentation
└── METRIC RA TEAM - 2026
    ├── 00 - Audit Navigation         ← Start here. Evidence Tracker, Audit Summary, SOW.
    ├── 01 - Delivery Process
    │   ├── Standards/                ← Delivery Process SOP v2.1
    │   └── Evidence/                 ← Jira exports, RAID Log (Amandeep, April 15)
    ├── 02 - Validation & QA
    │   ├── Standards/                ← QA & Governance SOP v2.1, Output Validation Doc v1.1
    │   └── Evidence/                 ← ⚠️ Missing — Sujai to produce
    ├── 03 - Data Sourcing & Lineage
    │   ├── Standards/                ← Data Sourcing & Lineage SOP v2.1
    │   └── Evidence/                 ← Master Data Source Sheet, PIA Emails, ADIDO Load Files, Metadata Templates
    ├── 04 - Governance & Issue Mgmt
    │   ├── Standards/                ← QA & Governance SOP v2.1
    │   └── Evidence/                 ← Jira exports, RAID Log Export.xls (Tom Wu, April 15)
    ├── 05 - Access Control
    │   ├── Standards/                ← Access Control SOP
    │   └── Evidence/                 ← PIA records, Canada Foundational Tracker
    ├── 06 - Change Management
    │   ├── Standards/                ← Change Management SOP v1.1
    │   └── Evidence/                 ← Excel mastersheet, Jira tickets, SOW
    ├── 07 - Process Flow Diagrams    ← Delivery Process PPT, Peer Review PPT
    └── 08 - Archive                  ← Previous versions
```

---

## 8. Audit Navigation Guide

| Audit Question | Where to Look |
|---|---|
| What metrics are in scope? | `Scope Statement of Work (Live).docx` — SharePoint `00 - Audit Navigation` |
| What is the full delivery process? | `01 - Delivery Process / Standards / Delivery Process SOP v2.1` |
| When was data pulled from Rahona? | 1 November 2025 — see Data Acquisition step, Delivery Process SOP v2.1 |
| Who approved each metric? | Jira — filter by `PO APPROVED` state |
| Were any metrics blocked? | Jira — filter by `BLOCKED` (49 active) + RAID Log Export.xls |
| How was data quality validated? | `02 - Validation & QA / Evidence` ⚠️ in progress |
| How was reconciliation done? | BAs + Dev Team → DCT/Static Sheet → IRAT — see QA SOP v2.1 Section 4 |
| Where did the data come from? | `Master_Data_source_FY2025_Segment.xlsx` + `2025 ADIDO Load Files` |
| How were PIAs handled? | Canada PIA Request Status (Jira) + DAC Submitted PIAs Canada + `2025 PIA Approval Emails` |
| Who has access to what? | Canada Foundational Tracker — `05 - Access Control / Evidence` |
| How were queries version-controlled? | `https://github.com/TD-Universe/RAFY2025_CA` |
| Where are final metric results? | Excel Mastersheet — `06 - Change Management / Evidence` |
| How were scope changes managed? | SOW weekly change log + Jira Kanban — `00 - Audit Navigation` |
| Where are process flow diagrams? | `07 - Process Flow Diagrams` — Delivery Process PPT, Peer Review PPT |

---

## 9. Current Gaps & In-Progress Items

| Item | Status | Owner | Notes |
|---|---|---|---|
| Validation & QA evidence (all 8 steps) | ❌ Missing | Sujai | DQ outputs, reconciliation reports, peer review sign-offs not yet produced |
| Lineage Documentation | 🟡 WIP | Amandeep | End-to-end lineage docs per AU in progress — MCC team does not have this yet |
| Refresh Management evidence | ❌ Missing | Amandeep | No artifact yet |
| Data Retention formal policy | ❌ No formal policy | Amandeep | Datasets stored in CA AZ without defined retention period — MCC team is aware |
| Technical Spec Document | 🟡 In Progress | Amandeep | MCC team working on it — DCT exists as interim artifact |
| Governance Evidence item 2 | ❌ Missing | Tom Wu | RAID Log Export.xls is item 1 — item 2 in evidence list is blank |

---

## 10. Key Numbers (FY2025)

| Metric | Value |
|---|---|
| Total Work Packages | 4 |
| Total Metric Definitions | 86 |
| Total Assessable Units | 35 |
| Total Metric Instances | 2,240 |
| Jira Stories — BUILD COMPLETE | 754 |
| Jira Stories — BLOCKED (active) | 49 |
| RAID Log Items | 137 |
| Rahona Data Sources | 20 |
| ADIDO Data Sources | 73 |
| Rahona Data Pull Date | 1 November 2025 |
| GitHub Repository | `TD-Universe/RAFY2025_CA` |

---

## 11. Document Index

| Document | Version | SharePoint Location |
|---|---|---|
| Audit Summary (this document) | v1.2 | `00 - Audit Navigation` |
| Scope Statement of Work (Live) | v1.32 | `00 - Audit Navigation` |
| FCRM Master Process Inventory FY2025.xlsx | current | `00 - Audit Navigation` |
| Evidence Tracker FY2025.xlsx | current | `00 - Audit Navigation` |
| Delivery Process SOP | v2.1 | `01 - Delivery Process / Standards` |
| QA & Governance Standard SOP | v2.1 | `02 - Validation & QA / Standards` |
| Output Validation Document | v1.1 | `02 - Validation & QA / Standards` |
| Approvals Document | v1.1 | `02 - Validation & QA / Standards` |
| Data Sourcing & Lineage SOP | v2.1 | `03 - Data Sourcing & Lineage / Standards` |
| Access Control SOP | current | `05 - Access Control / Standards` |
| Change Management SOP | v1.1 | `06 - Change Management / Standards` |
| Process Flow Diagrams (PPT) | current | `07 - Process Flow Diagrams` |

---

*This document is maintained by the FCRM Enterprise Risk Assessment Reporting Team. Last updated: April 2026.*