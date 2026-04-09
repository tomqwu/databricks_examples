# Standard Operating Procedure (SOP)
## Validation, Quality Assurance, and Governance for AML Process

### Document Control
| Attribute | Detail |
| :--- | :--- |
| **Document Title** | ML/TF and Sanctions Risk Assessment: QA & Governance Standard |
| **Document Owner** | FCRM Enterprise Risk Assessment Reporting Team |
| **Effective Date** | April 2026 |
| **Version** | 2.1 (Current Practices Focus) |
| **Target Audience** | 1LOD, 2LOD, 3LOD (Internal Audit), and Regulatory Reviewers |

---

### 1. Purpose
This SOP outlines the mandatory validation, quality assurance (QA), and governance protocols for the FY25 Anti-Money Laundering (AML) and Sanctions Enterprise Risk Assessment process. Adherence to these procedures ensures that methodology decisions, blockers, scope changes, and data outputs are accurate, transparent, auditable, and formally approved via the system of record (Jira).

### 2. Scope
This SOP applies to all AML data processing, monitoring, reporting, and analytics activities executed within the Risk Assessment cycle. This includes the processing of the 85 defined metrics, automated Rahona data warehouse feeds, business-managed ADIDO files, and the standard data execution and aggregation processes.

---

### 3. Validation Planning & Decision Traceability
**Objective:** To define a structured approach for validating AML processes before execution and ensuring business logic is formally agreed upon.
* **Validation Scope:** Clearly identify the datasets, target systems, and expected outputs for each Work Package (e.g., WP-01 BDEs, WP-04 ABAC).
* **Governance - Decision Logging:** All business logic, scoping, and methodological decisions must be captured within Jira. No unlogged, out-of-band decisions are permitted. Initial business rules and metric definitions must be formalized while the ticket is in **BUSINESS LOGIC DESIGN DEF** and **BUSINESS LOGIC SEMANTIC** states.
* **Governance - Assumption Tracking:** Ambiguities in requirements, default thresholds, or assumptions regarding proxy data usage must be formally documented to ensure they are visible and validated. This is resolved while the ticket is in the **METRIC DEFINITION CLARIFICATION** or **BAU CDE DOCUMENTATION** state.

### 4. Data Quality Checks & Sourcing
**Objective:** To ensure data used in AML processes is accurate, complete, consistent, and traceable prior to metric calculation.
* **Completeness & Accuracy:** Validate data against source systems to ensure data availability meets the minimum 95% threshold.
* **Consistency & Uniqueness:** Cross-check values across datasets and identify duplicate records within the Assessable Unit (AU) populations.
* **Governance - Sourcing Lineage:** The identification and provisioning of data are tracked explicitly through Jira workflow states. The ticket must accurately reflect its upstream dependency via **DATA SOURCE(S) IDENTIFIED** and **DAC OR ADIDO LOAD PROCESS**.

### 5. Reconciliation
**Objective:** To ensure data consistency between source systems and final AML outputs.
* **Data Provisioning:** Track data staging and readiness via the **DATA PROVISIONED IN AZ** Jira state.
* **Record Count Validation:** Reconcile record counts between source and processed data to ensure the baseline population matches the final metric output after business rule filtering is applied.
* **Identify Variances:** Document and investigate variances or anomalies where expected records drop off during data aggregation.

### 6. Reasonability Analysis
**Objective:** To assess whether AML outputs are logical, within expected thresholds, and accurately reflect the business reality of the Assessable Unit.
* **Trend & Outlier Analysis:** Evaluate metric stability across the Assessment Cycle and identify AUs with highly abnormal risk scores.
* **Threshold Validation:** Ensure mathematical filters and business rules (e.g., specific transaction thresholds) have been applied properly according to the defined methodology.
* **Methodology Alignment:** Compare current hard-data outputs against historical proxy data/questionnaires to identify methodology shifts.

### 7. Peer Review & Compliance Checks
**Objective:** To ensure independent validation of work performed and strict adherence to privacy constraints.
* **Independent Review:** Assign a reviewer independent of the preparer to validate methodology, calculations, and assumptions.
* **Governance - Privacy Compliance:** Any metric requiring a Privacy Impact Assessment (PIA) must accurately reflect its compliance status. The ticket must pass through the **PIA BUILD**, **WITH PRIVACY TEAM**, and **PIA APPROVED** states before final data execution.
* **Review Approval:** Document review comments and resolutions, capturing all challenge discussions in the metric's Jira ticket and transitioning the state to **AU REVIEW APPROVAL**.

### 8. Output Verification
**Objective:** To confirm final outputs are accurate, properly formatted, and ready for use in downstream aggregation systems.
* **Pre-Execution Check:** Verify output format, structure, and key calculations against regulatory reporting requirements.
* **Execution Gating:** A ticket cannot transition to execution states (e.g., **BUILD IN PROGRESS (PART)**, **BUILD IN PROGRESS (FULL)**, or **BUILD COMPLETE**) until all prerequisite logic, privacy, and data QA checks outlined in Steps 3-7 are cleared.

### 9. Issue Management & The RAID Log
**Objective:** To track, escalate, and resolve anomalies, data blockers, or data quality concerns in a transparent and auditable manner.
* **Governance - Issue Logging:** If a metric cannot proceed due to an upstream QA failure or missing source file, the Jira ticket must be immediately transitioned to the **BLOCKED** state. A corresponding entry must be captured in the formal project **RAID Log** (Risks, Assumptions, Issues, Dependencies).
* **Governance - Severity Assessment:** Issues must undergo a standardized severity assessment to prioritize critical data gaps (P1) or systemic failures (P2) over localized logic discrepancies.
* **Governance - Escalation Pathways:** When an issue cannot be resolved within SLAs, utilize a structured escalation matrix (Developer -> Team Lead -> Project Manager -> Business Stakeholders / 2LOD). Escalations must clearly categorize the blocker (e.g., Data Issue, Timeline Constraint).
* **Governance - Resolution & Unblocking:** An issue is formally considered resolved only when marked "Closed" within the RAID log. Only at this point may the Jira ticket leave the `BLOCKED` state and proceed toward **READY FOR FINAL REVIEW**.

### 10. Sign-Off, Risk Acceptance & Decommissioning
**Objective:** To formally approve validation results, log risk acceptance for unresolvable issues, and cleanly deprecate obsolete scope.
* **Formal Approval Gates:** No output can be finalized without documented business consent. Decisions are formally logged when a ticket transitions through **PO CONCURRENCE** and ultimately **PO APPROVED**.
* **Governance - Risk Acceptance:** If data completeness falls below required thresholds and cannot be remediated before reporting deadlines, it must be formally risk-accepted by all key stakeholders. The metric ticket is transitioned to the **NOT AVAILABLE** state. In alignment with AML methodology, this triggers a default to a higher risk rating for the impacted AU to prevent artificial suppression of Inherent Risk.
* **Governance - Decommissioning & Out of Scope:** Metrics, Assessable Units, or Work Packages that are retired or no longer applicable for the current cycle must be transitioned to the **NO LONGER REQUIRED** or **NOT APPLICABLE** Jira states. This ensures historical traceability while systematically excluding them from the current assessment cycle execution.