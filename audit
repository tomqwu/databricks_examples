# Governance, Decision & Issue Management Standard

### Document Control
| Attribute | Detail |
| :--- | :--- |
| **Document Title** | ML/TF and Sanctions Risk Assessment: Governance & Issue Management |
| **Document Owner** | FCRM Enterprise Risk Assessment Reporting Team |
| **Effective Date** | April 2026 |
| **Version** | 1.1 |
| **Target Audience** | 1LOD, 2LOD, 3LOD (Internal Audit), and Regulatory Reviewers |

---

## 1.0 Purpose
This section defines the mandatory governance protocols, issue management workflows, and decision traceability standards for the ML/TF and Sanctions Risk Assessment process. Adherence to these procedures ensures that all methodology decisions, blockers, and scope changes are transparent, auditable, and formally approved via the system of record (Jira).

## 2.0 Decision Logging & Workflow Traceability
All business logic, scoping, and methodological decisions must be captured within Jira. The transition of a metric ticket through defined workflow states serves as the immutable, auditable log of decision-making.

* **2.1 Logic Definition & Semantics:** Initial business rules and metric definitions are documented and formalized while the ticket is in **BUSINESS LOGIC DESIGN DEF** and **BUSINESS LOGIC SEMANTIC** states. 
* **2.2 Formal Approval Gates:** No execution can finalize without documented business consent. Decisions are formally logged when a ticket transitions through required approval states, including **PO CONCURRENCE**, **AU REVIEW APPROVAL**, and ultimately **PO APPROVED**.
* **2.3 Out-of-Band Decisions:** No unlogged, out-of-band decisions are permitted. All sign-offs must be reflected by transitioning the Jira ticket to the appropriate state.

## 3.0 Assumption & Data Tracking
Assumptions made during data collection, including privacy constraints, source identification, and proxy data usage, must be formally documented to ensure they are visible and validated.

* **3.1 Clarification & Documentation:** Ambiguities in requirements or assumptions regarding data usage must be resolved while the ticket is in the **METRIC DEFINITION CLARIFICATION** or **BAU CDE DOCUMENTATION** state.
* **3.2 Data Sourcing Lineage:** The identification and provisioning of data are tracked explicitly through states such as **DATA SOURCE(S) IDENTIFIED**, **DAC OR ADIDO LOAD PROCESS**, and **DATA PROVISIONED IN AZ**.
* **3.3 Privacy & Compliance:** Any metric requiring Privacy Impact Assessments (PIA) must accurately reflect its compliance status via the **PIA BUILD**, **WITH PRIVACY TEAM**, and **PIA APPROVED** states before build completion.

## 4.0 Issue Logging & The RAID Log
Anomalies, pipeline blockers, or data quality concerns identified during the assessment cycle must be centralized and documented.

* **4.1 The BLOCKED State:** If a metric cannot proceed due to an upstream issue, the Jira ticket must be immediately transitioned to **BLOCKED**. 
* **4.2 The RAID Log Integration:** Any ticket moved to **BLOCKED** must have a corresponding entry captured in the formal project RAID Log (Risks, Assumptions, Issues, Dependencies). The RAID log acts as the primary artifact for tracking the root cause and remediation plan.

## 5.0 Severity Assessment
Issues captured within the RAID log must undergo a standardized severity assessment to ensure resources are allocated to the highest-priority blockers.

* **5.1 Assessment Criteria:** The assessment evaluates the issue's potential impact on regulatory reporting timelines, data accuracy, and overall project scope. Critical data gaps or systemic execution failures are prioritized.

## 6.0 Escalation Pathways
When an issue cannot be resolved at the execution level within established Service Level Agreements (SLAs), a structured escalation matrix must be utilized.

* **6.1 Path of Escalation:** Developer -> Team Lead -> Project Manager (PM) -> Business Stakeholders / 2LOD.
* **6.2 Blocker Categorization:** Escalations must categorize the blocker (e.g., Data Issue, Timeline Constraint, Requirement Ambiguity) to trigger the correct intervention, such as targeted blocker calls or PIA process escalations.

## 7.0 Resolution & Unblocking
Strict prerequisites govern the movement of tasks blocked by identified issues.

* **7.1 Workflow Gating:** A ticket in the **BLOCKED** state cannot be transitioned to execution states (e.g., **BUILD IN PROGRESS (PART)**, **BUILD IN PROGRESS (FULL)**, or **BUILD COMPLETE**) until the underlying issue is remediated.
* **7.2 Formal Closure:** An issue is formally considered resolved only when the item is marked "Closed" within the RAID log, at which point the Jira ticket may proceed toward **READY FOR FINAL REVIEW**.

## 8.0 Risk Acceptance (Data Unavailability)
In scenarios where an issue (such as an unresolvable data gap) cannot be remediated prior to mandatory reporting deadlines, a formal Risk Acceptance process is triggered.

* **8.1 The NOT AVAILABLE State:** If data completeness falls below required thresholds and is formally risk-accepted by all key stakeholders (BA, Business Owner, Team Lead, Dev), the metric ticket is transitioned to the **NOT AVAILABLE** state.
* **8.2 Methodology Impact:** In alignment with AML methodology, metrics marked as **NOT AVAILABLE** will trigger a default to a higher risk rating for the impacted Assessable Unit to prevent artificial suppression of Inherent Risk.

## 9.0 Decommissioning & Out of Scope
When structural components of the risk assessment become obsolete or are deemed out of scope, they undergo a controlled deprecation process.

* **9.1 Deprecation States:** Metrics, Assessable Units, or specific Work Packages that are retired or no longer applicable for the current cycle must be transitioned to the **NO LONGER REQUIRED** or **NOT APPLICABLE** Jira states.
* **9.2 Historical Traceability:** This ensures the assets are systematically excluded from the current build (preventing unnecessary execution) while preserving the historical audit trail of their lifecycle.
