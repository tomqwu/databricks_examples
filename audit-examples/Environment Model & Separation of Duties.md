# Environment Model & Separation of Duties — Audit Note

| Attribute | Detail |
|---|---|
| **Document Title** | Environment Model & Separation of Duties (single-environment justification) |
| **Owner** | FCRM Enterprise Risk Assessment Reporting Team (MCC) |
| **Effective** | June 2026 |
| **Version** | 1.0 |
| **Answers** | Risk Assessment — Audit-Ready Documentation, Scope & Approach §3.6 ("DEV vs PROD separation") and the release/deployment references in §3.1 and §3.7 |

## 1. Environment reality

The MCC team operates in a **single Azure Databricks query environment**. There is **no non-production / production separation** — queries are written, executed and validated in the same workspace. This is by design for the Risk Assessment data-delivery work: the team produces metric *values*, not a deployed production application, so there is no code-promotion pipeline between environments.

Because of this, two terms in the Scope & Approach document do not map literally to MCC's work and are reframed below:
- **"Production release" (§3.1) / "deployment" (§3.7)** — there is no deploy of code to a separate production environment. "Release" here means **delivery of validated metric outputs to the Excel mastersheet and onward to IARAT.**
- **"DEV vs PROD separation" (§3.6)** — not applicable as an environment control; the assurance it normally provides is delivered through the compensating controls in §3 below.

## 2. Why a single environment is appropriate here

- The work is analytical query execution against a **fixed point-in-time snapshot** (Rahona data pulled to CA AZ on 1 November 2025), not a live transactional system.
- Outputs are **static metric values** recorded in the mastersheet — there is no running service that requires a protected production runtime.
- Git is used as an **audit record of query versions only — not for deployment**, so there is no build/promote step that an environment boundary would gate.

## 3. Compensating controls (what stands in for environment separation)

The integrity that DEV/PROD separation normally enforces is provided here by change-control gates, role separation, and an immutable version record:

| Control | What it provides | Evidence |
|---|---|---|
| **Change-control gates in Jira** | No work without a ticket; staged approval before output is accepted | Jira ticket → BUSINESS LOGIC DESIGN DEF → PO CONCURRENCE → PO APPROVED state history |
| **Segregation of duties** | Preparer ≠ reviewer ≠ approver; approver independent of the change requester | Jira approval comments; independent reviewer sign-off on the mastersheet |
| **Git version history** | Immutable record of every query version; no unapproved change reaches the audit record | `TD-Universe/RAFY2025_CA` commit history, `[FY25DATA-XXX]` messages, no force-push to main |
| **Independent output sign-off** | A second person confirms mastersheet entries before PO APPROVED | Mastersheet update record + Jira PO APPROVED transition |
| **Access control & PIA gating** | Controls who can run or modify work in the single environment | Canada Foundational Tracker; PIA approvals |
| **Reproducibility / rerun** | Any metric can be re-run against the fixed snapshot to reproduce the result (covers §3.7 "rerun capability") | Re-runnable notebooks; reproducible `RA_FY_2025.cde_da_by_lob_segment` DQ table |

## 4. Net position for audit

There is no DEV/PROD separation because the work does not involve a production code deployment. Controlled, reproducible, segregation-of-duties-enforced change management over a single Azure Databricks environment provides equivalent assurance. The Jira state history, Git commit history and mastersheet sign-off record together serve as the "deployment / release" evidence that §3.1 and §3.7 call for.
