**FCRM Risk Assessment FY2025**   |   Validation & Quality Assurance SOP   |   Internal

**TD Bank Group**

MCC Team — FCRM Risk Assessment FY2025

Standard Operating Procedure (SOP)

**Validation and Quality Assurance**

| **Attribute** | Detail |
| --- | --- |
| **Document Title** | Validation and Quality Assurance — Standard Operating Procedure |
| **Document Owner** | FCRM Enterprise Risk Assessment Reporting Team |
| **Effective Date** | June 2026 |
| **Version** | 2.2 |
| **Target Audience** | 1LOD, 2LOD, 3LOD (Internal Audit), and Regulatory Reviewers |
| **System of Record** | Jira (FY25 RA CYCLE - DATA) + GitHub + SharePoint |

# **1. Purpose**

This SOP defines the mandatory validation and quality-assurance procedures for the FY2025 Anti-Money Laundering (AML) and Sanctions Enterprise Risk Assessment (RA). It ensures that every metric output is complete, accurate, reconciled, reasonable, peer-reviewed, and formally signed off before it feeds the Inherent Risk assessment.

It also defines how **data lineage** and **automated validation** are used as quality controls: each metric must carry a documented data path, and each metric definition and lineage record must pass structural and cross-reference checks before approval.

# **2. Scope**

This SOP applies to all validation and QA activities performed by the MCC Team across the metric delivery lifecycle, including:

- Data quality measurement of Critical Data Elements (CDEs)

- Reconciliation of development outputs against business-provided numbers

- Reasonability, trend, and outlier analysis

- Peer review and privacy/compliance checks

- Data lineage validation

- Schema and cross-artifact integrity validation

- Output verification, sign-off, and risk acceptance

|  | *Out of scope: business logic and methodology decisions (owned by First Line / 1LOD), data quality of upstream source systems (owned by the source system owners), and changes to regulatory thresholds not driven by the MCC Team.* |
| --- | --- |

# **3. Key Principles**

- No metric output is accepted into the Excel mastersheet without passing validation.

- **Reviewer independence** — the reviewer must not be the preparer of the work being reviewed.

- **Data quality is measured, not assumed** — every CDE carries a recorded availability percentage.

- The **95% data-quality threshold** gates whether a CDE may feed Inherent Risk. Below threshold → formally risk-accepted → NOT AVAILABLE, which raises the AU's risk rating rather than suppressing the value.

- **Every metric has a documented data lineage.** Technical detail (source tables/columns, transformation and join logic, data-quality implementation) lives in the lineage record — not in the business metric definition.

- **Validation is evidenced** — every check produces a retained artifact.

- All decisions and assumptions are logged in Jira. Out-of-band, undocumented decisions are not authoritative and are flagged as audit findings.

# **4. Process Steps**

The validation and QA process consists of eight sequential steps. A ticket cannot transition to BUILD IN PROGRESS or BUILD COMPLETE until the prerequisite logic, privacy, and data-quality checks (Steps 3–7) are cleared.

| **Step #** | **Step Name** | **Jira State** | **Inputs** | **Actions** | **Outputs** | **Approval** |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | **Validation Planning & Decision Traceability** | BUSINESS LOGIC DESIGN DEF | Metric definitions, SOW, work-package scope | Define the validation approach. Identify datasets, target systems, and expected outputs per work package. Identify key controls and risk areas. | Validation Plan Document, Risk Assessment Matrix | No |
| **2** | **Decision & Assumption Logging** | BUSINESS LOGIC DESIGN DEF / SEMANTIC | Business logic decisions, ambiguities | Log all business-logic decisions in Jira. Record assumptions, default thresholds, and proxy-data use in the appropriate clarification states. | Jira decision and assumption tickets | No |
| **3** | **Data Quality Checks & Sourcing** | DATA SOURCE(S) IDENTIFIED | Sourced datasets, CDE list | Measure availability of each CDE. Check completeness (no missing/null critical fields), data-type integrity, and duplicates. Validate accuracy against source (95% threshold). Track sourcing lineage. | DQ check results, profiling reports, issue log | No |
| **4** | **Reconciliation** | DATA PROVISIONED IN AZ | Dev Team numbers, BA numbers | Reconcile record counts and key values: business numbers and development numbers reconcile through the static sheet to the Inherent Risk template. Investigate variances. | Reconciliation reports, variance analysis logs | No |
| **5** | **Reasonability Analysis** | BUILD IN PROGRESS | Reconciled outputs, prior-cycle data | Trend and outlier analysis across the assessment cycle. Threshold validation. Compare current hard data against historical proxy/questionnaire data to identify methodology shifts. | Trend analysis report, outlier detection log | No |
| **6** | **Peer Review & Compliance Checks** | AU REVIEW APPROVAL | Validated outputs, review checklist | Assign an independent reviewer. Review methodology, calculations, and outputs. Confirm privacy compliance is cleared before final data execution. Document review comments and resolutions. | Peer review sign-off, review comments log | Yes |
| **7** | **Output Verification** | BUILD COMPLETE | Reviewed outputs | Verify output format, structure, and key calculations against regulatory requirements. Confirm Steps 3–6 are cleared (execution gating). | Output verification report, format compliance log | No |
| **8** | **Sign-Off, Risk Acceptance & Decommissioning** | PO CONCURRENCE → PO APPROVED | Verified outputs, RAID status | Formal approval gates. Where data is below threshold, record formal risk acceptance → NOT AVAILABLE. Retire metrics/AUs as NO LONGER REQUIRED or NOT APPLICABLE with historical traceability. | Signed approval record, final validation report | Yes |

## **4.1 Step 1 — Validation Planning & Decision Traceability**

Before validation begins, define a structured approach for each work package: which datasets and target systems are in scope, what the expected outputs are, and which controls and risk areas require the most scrutiny. This step is mandatory where decisions are high-risk or audit defensibility is required.

## **4.2 Step 2 — Decision & Assumption Logging**

All business-logic and methodological decisions are captured in Jira before validation outputs are relied upon. Ambiguities, default thresholds, and proxy-data assumptions are documented in the appropriate clarification states. Unlogged decisions cannot be treated as authoritative.

## **4.3 Step 3 — Data Quality Checks & Sourcing**

Every CDE used by a metric is measured for availability and checked for completeness, data-type integrity, and duplicates, and validated for accuracy against the source. The detailed availability method and its outputs are described in **Section 6 — Data Quality Check (Scope of Work)**. Sourcing lineage is tracked through the relevant Jira states and confirmed against the lineage record (Section 5).

## **4.4 Step 4 — Reconciliation**

Business-provided numbers and development-team numbers are reconciled through the static sheet into the Inherent Risk template. Record counts and key financial values are reconciled, and any variance is investigated and documented before the output proceeds.

## **4.5 Step 5 — Reasonability Analysis**

Outputs are tested for reasonability through trend and outlier analysis across the assessment cycle, threshold validation, and comparison against prior-cycle data. Material shifts are explained or escalated.

## **4.6 Step 6 — Peer Review & Compliance Checks**

An independent reviewer (not the preparer) reviews methodology, calculations, and outputs, and confirms that privacy and compliance requirements are cleared before final data execution. Review comments and their resolutions are documented, and the ticket transitions to AU REVIEW APPROVAL.

## **4.7 Step 7 — Output Verification**

The output is verified for format, structure, and key calculations against regulatory requirements. The ticket cannot proceed to the BUILD states until the prerequisite checks (Steps 3–6) are cleared.

## **4.8 Step 8 — Sign-Off, Risk Acceptance & Decommissioning**

Formal approval gates apply: PO CONCURRENCE followed by PO APPROVED. Where a CDE is below the data-quality threshold, formal risk acceptance is recorded and the AU is marked NOT AVAILABLE for that metric. Retired metrics or AUs are transitioned to NO LONGER REQUIRED or NOT APPLICABLE, with historical traceability preserved.

# **5. Data Lineage Validation**

Data lineage is a core quality control. Every metric must have a documented lineage record that traces the full data path, and validation confirms that the record is complete, resolvable, and consistent with what was actually executed.

## **5.1 What the lineage record contains**

For each metric, the lineage record documents:

- The source systems and databases the metric draws from

- The step-by-step transformation logic (filters, joins, derivations)

- References to shared reference / intermediate assets (for example cost-centre mappings, country risk ratings, occupation/industry reference lists, PEP lists)

- Query references

- The data-quality implementation for the metric's CDEs

## **5.2 Lineage rules**

- **One lineage record per metric.** A variant that sources or transforms differently from its base metric maintains its own lineage record.

- **Separation of concerns.** The business metric definition states *what* the metric is and *where* it applies. The lineage record states *how* it is built and *how data quality is implemented*. Source tables/columns, join logic, and data-quality logic do not belong in the business definition.

- **Shared assets are referenced, not embedded.** Reference/intermediate assets are shared inputs; the lineage record points to them, and the metric definition never references a data asset directly.

## **5.3 What validation confirms**

- The lineage record is complete and every documented step is accounted for.

- All source-system and reference-asset references resolve, and referenced assets carry the required metadata.

- The lineage record's data-quality section **agrees with the executed query and the recorded availability result** for each CDE. Confirming this spec-versus-execution agreement is a required QA check — the documented data path, the query that ran, and the data-quality figure on record must tell the same story.

|  | *Where the documented lineage and the executed query disagree, the metric is treated as not validated. The discrepancy is logged in the RAID log and the ticket is held in BLOCKED until reconciled.* |
| --- | --- |

# **6. Data Quality Check — Scope of Work**

**What it does.** The DQ check measures how complete each Critical Data Element (CDE) is — the share of records that carry a real value — and turns that into a single availability percentage. That percentage decides whether the CDE is good enough to feed the Inherent Risk calculation for its Assessable Unit (AU).

**How it works.** For each metric in scope:

1. **Identify** the controlling AU(s) and CDEs from the SOW and the master data-source sheet.

2. **Locate** the source table — Rahona SRZ/CZ (landed in CA AZ) or ADIDO — and select the specific data element to be measured.

3. **Measure** availability with a flat SELECT against the source view, under the cycle's as-of filter: count all records (total) and the records that carry a real value (NNNBV = Not Null, Not Blank Value), then compute availability_pct = round(100 * NNNBV / total, 2).

4. **Record** the result — the availability helper writes one row to the central availability table (cde_da_by_lob_segment): LOB, CDE, source, source table, data element, availability percentage, and run date.

5. **Transcribe** the same percentage into the static master sheet, against the matching AU / metric / CDE row.

**The 95% gate.** The threshold is applied directly to the availability percentage:

| **Availability** | **Result** |
| --- | --- |
| **≥ 95%** | Passes — the CDE feeds Inherent Risk. |
| **< 95%** | Fails — routed to risk acceptance. The AU is marked NOT AVAILABLE and takes the higher risk rating (the value is not artificially suppressed). |

**Evidence and rules.** The DQ check produces two retained outputs (Section 9): the **Static Master Sheet**, where each metric carries its DQ% in a dedicated column, and the **Databricks notebook** that computed it, pushed to the GitHub repository as the version-controlled audit record. These are backed by the independent reviewer sign-off on the mastersheet entry and the Jira ticket moving through BUILD COMPLETE → PO CONCURRENCE → PO APPROVED. A CDE below the threshold triggers a RAID log entry and a BLOCKED state until risk acceptance is formally recorded. No mastersheet update is permitted without a preceding DQ measurement and its written-back DQ%.

# **7. Validation Methods & Automated Checks**

Validation operates at two complementary levels, both of which produce retained evidence.

## **7.1 Artifact-level (schema) validation**

Each metric definition and each lineage record is checked against a defined structure as it is authored, catching shape, format, and required-field errors early — before the artifact enters review.

## **7.2 Cross-artifact (integrity) validation**

Before sign-off, an automated integrity check confirms the full set of artifacts is internally consistent. The check confirms that:

- Every metric identifier is unique.

- Every definition references a real, resolvable specification and lineage record.

- Fields that must be identical between a base (canonical) metric and its AU variants match exactly.

- Enumerated fields (for example lifecycle status, approval status, risk dimension) match the controlled vocabulary.

- Methodology references resolve to a registered methodology entry.

- Relationship references (parent, sibling, numerator, denominator) resolve to registered metrics.

- Lineage records conform to the required lineage structure; legacy shapes are flagged for migration.

- Reference assets and source registries expose the required metadata.

A validation report is produced and retained as audit evidence. Targeted runs (definitions-only, lineage-only, assets-only) support focused re-checks after a change.

## **7.3 Risk-readiness completeness**

Validation also confirms each metric carries the required audit-readiness fields: its risk dimension, its methodology reference, the decision thresholds and scoring bands (held with the methodology reference), and the documented assumptions, data limitations, and known issues. These fields make the risk decision behind each metric explicit and auditable.

# **8. Jira Workflow States**

| **Jira State** | **Meaning in the Validation & QA context** |
| --- | --- |
| **BUSINESS LOGIC DESIGN DEF / SEMANTIC** | Validation planning and decision/assumption logging in progress. |
| **DATA SOURCE(S) IDENTIFIED** | Sources confirmed; data quality checks underway. |
| **DATA PROVISIONED IN AZ** | Data landed; reconciliation underway. |
| **BUILD IN PROGRESS** | Reasonability analysis underway; prerequisite checks being cleared. |
| **BUILD COMPLETE** | Output verified; ready for sign-off. |
| **AU REVIEW APPROVAL** | Independent peer review signed off. |
| **PO CONCURRENCE → PO APPROVED** | Formal sign-off gates cleared. |
| **BLOCKED** | Validation failed or a discrepancy is open; RAID log entry required. |
| **NOT AVAILABLE** | CDE below threshold and formally risk-accepted; raises AU risk rating. |
| **NO LONGER REQUIRED / NOT APPLICABLE** | Metric or AU retired, with historical traceability preserved. |

# **9. Roles ****&**** Responsibilities**

| **Role** | **Responsibilities** |
| --- | --- |
| **Preparer / Developer** | Run DQ checks, reconciliation, and reasonability analysis. Author and maintain the lineage record. Produce validation outputs. |
| **Reviewer** | Independently review methodology, calculations, outputs, and the lineage-versus-execution agreement. Must not be the preparer. |
| **Validation & QA Lead** | Own the validation plan and the QA gate. Confirm all checks are cleared and evidence is retained before sign-off. |
| **Approver** | Formal sign-off (PO CONCURRENCE, PO APPROVED). Must be a Team Lead or Product Owner, independent of the preparer. |
| **RAID Log Owner** | Log validation failures, discrepancies, and risk-acceptance items; manage severity and escalation. |

# **10. Evidence ****&**** Audit Trail**

| **Artifact** | **What It Proves** | **Where Stored** |
| --- | --- | --- |
| **Validation Plan Document, Risk Assessment Matrix** | A structured validation approach was defined up front | *SharePoint — 02 Validation & QA / Evidence* |
| **Static Master Sheet — DQ% column, per metric** | Each metric's CDE availability was measured and recorded against the 95% threshold | *SharePoint — Static Master Sheet* |
| **DQ Databricks notebook** | Version-controlled record of how the availability figure was computed | *GitHub — TD-Universe/RAFY2025_CA* |
| **Reconciliation & variance reports** | Development numbers reconcile to business numbers and the IR template | *SharePoint — 02 Validation & QA / Evidence* |
| **Trend / outlier analysis** | Outputs were tested for reasonability against prior cycles | *SharePoint — 02 Validation & QA / Evidence* |
| **Peer review sign-off & comments log** | An independent reviewer approved the output | *Jira comments + SharePoint* |
| **Lineage record** | The metric's data path is documented and agrees with execution | *Lineage repository* |
| **Validation report (schema + integrity)** | Definitions and lineage passed structural and cross-reference checks | *Validation report output* |
| **Signed approval record / Jira state history** | Formal sign-off gates were cleared in order | *Jira — ticket timeline* |
| **RAID log (if applicable)** | Validation failures or below-threshold items were tracked and resolved | *Jira RAID Log* |

# **11. Constraints, Assumptions ****&**** Escalation**

## **11.1 Constraints**

- A ticket cannot transition to BUILD IN PROGRESS or BUILD COMPLETE until the prerequisite checks (Steps 3–7) are cleared.

- No mastersheet update is permitted without a preceding DQ measurement and its recorded availability percentage.

- The reviewer must be independent of the preparer; self-review is not permitted.

- A CDE below the 95% threshold cannot feed Inherent Risk until formal risk acceptance is recorded.

- Where the documented lineage and the executed query disagree, the metric is treated as not validated.

## **11.2 Escalation Path**

If validation cannot be completed or a discrepancy cannot be resolved within SLA:

- Preparer raises a BLOCKED ticket and a RAID log entry.

- Team Lead is notified — target resolution within one business day.

- Project Manager is engaged if unresolved after Team Lead review.

- Business Stakeholders / 2LOD are notified for systemic issues (P1).

|  | *All escalations must be documented in the Jira ticket comments and the RAID log — verbal escalations alone are not sufficient for audit purposes.* |
| --- | --- |

# **12. Related Documents**

- QA & Governance Standard SOP v2.1 — SharePoint: 02 - Validation & QA

- Delivery Process SOP v2.1 — SharePoint: 01 - Delivery Process

- Data Sourcing & Lineage Management SOP v2.1 — SharePoint: 03 - Data Sourcing & Lineage

- Change Management and Version Control SOP v1.1 — SharePoint: 06 - Change Management

- Git & Databricks Best Practices — SharePoint: 06 - Change Management

- FCRM Master Process Inventory FY2025.xlsx — SharePoint: 00 - Audit Navigation

- Evidence Tracker FY2025.xlsx — SharePoint: 00 - Audit Navigation

**Document Owner: **FCRM Enterprise Risk Assessment Reporting Team   |   **Effective: **June 2026   |   **Version: **2.2   |   **Classification: **Internal