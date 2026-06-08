# Data Retention — Corrected Inventory Wording + SOP Section (DRAFT v0.1)

**FCRM Risk Assessment FY2025 — MCC Team**
**Purpose:** ready-to-paste replacement for the false retention statement in the Process Inventory, plus the Data Retention SOP section.
**Anchor:** the **live screenshot** state is authoritative. See the divergence note below before pasting.

---

## ⚠️ Divergence to reconcile first

| | Live (screenshot, 6/8/2026) | Project copy (Master Inventory xlsx) |
|---|---|---|
| Step # | **6** | 7 |
| Owner | **?** (unassigned — open for anyone to pick up) | (was Raghul) |
| False claim phrasing | "…no data retention policy has been set for expiry." | "Currently no defined retention policy — datasets stored in CA AZ without a defined retention period." |

Same false claim, two versions. Correction below anchors to the **live (step 6)** row. Owner is deliberately left as **?** — open for anyone to take. Reconcile the step-number mismatch as part of the broader Data Sourcing step-count drift (7→6) before final paste.

---

## 1. Corrected inventory cell wording (ready to paste)

**Step:** Data Retention

**Owner:** ? *(unassigned — open for anyone to pick up)*

**Inputs**
> CA AZ datasets; organizational retention policies; Curated Data Zone (year-over-year RA data); Rahona SRZ.

**Description / Activities** *(replaces the false statement)*
> RA data retention is governed by external standards — this team references them, it does not set them. Curated Data Zone / CA AZ RA data follows the **CA AZ Privacy Impact Assessment (PIA)** retention standard (currently **5 years**); source-zone data follows the **Rahona SRZ Data Retention Policy**. On a defined cadence the assigned reviewer verifies that RA data in the Curated Data Zone is within the retention window, completes the retention check template, confirms completion by email, and files the evidence in SharePoint. Items approaching or exceeding the window are raised via RAID / Jira to the retention owner for a decision (remove / retain with justification / risk acceptance).

**Outputs / Evidence**
> Data retention statement (PIA reference); completed retention check template; confirmation email filed in SharePoint; RAID / Jira entries for any flagged items.

**Reference**
> CA AZ PIA · Rahona SRZ Data Retention Policy · DaaS AZ retention standard *(Patty locating — add reference once shared)*.

> **Do not** restore any "no policy / no expiry set" language, and **do not** state a 10-year figure (discussed, never confirmed). The standard is 5 years per the PIA.

---

## 2. Data Retention — SOP section (content for Data Sourcing & Lineage SOP)

### 2.x Data Retention

**Principle.** Retention is set by policy, not by this team's procedure. The MCC team's role is to reference the authoritative standard and to evidence that adherence is checked on a defined cadence.

**Governing standards**

| Zone | Standard | Source |
|---|---|---|
| CA AZ / Curated Data Zone (RA data) | 5 years | Updated CA AZ PIA (confirmed) |
| Rahona SRZ | per policy | Rahona SRZ Data Retention Policy |
| DaaS AZ | AZ retention standard | DaaS AZ retention policy standard *(to be cited — Patty locating)* |

**Procedure**

1. On the defined cadence, the assigned reviewer confirms RA data in the Curated Data Zone is within the 5-year window and that nothing has aged past the standard without a decision.
2. The reviewer completes the retention check template (below).
3. The reviewer emails the completed template confirming the check was done.
4. Template + email are filed in SharePoint.
5. Any item approaching/exceeding the window is raised via RAID + Jira to the retention owner for a decision (remove / retain with justification / risk acceptance). No silent removal.

**Retention check template (fillable)**

| Field | Entry |
|---|---|
| Check date | |
| Reviewer | |
| Cycle / period covered | |
| Zone checked | CA AZ / Curated Data Zone · Rahona SRZ |
| Governing standard applied | 5-year (CA AZ PIA) / [DaaS AZ standard ref] |
| Oldest RA data found (as-of date) | |
| Within standard? | Yes / No |
| Items flagged | |
| Decision on flagged items | Remove / Retain w/ justification / Risk acceptance / N/A |
| RAID / Jira ref | |
| Confirmation email filed in SP at | |
| Reviewer sign-off | |

**Honesty note (internal — not for the SOP body).** No retention check has run historically and removal has never been facilitated. This section defines the go-forward procedure; do not present past check evidence that does not exist.

