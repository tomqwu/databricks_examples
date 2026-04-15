# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

An Anti-Bribery Anti-Corruption (ABAC) metrics workspace for a financial crime risk assessment. All logic lives in Databricks SQL notebooks (`.ipynb`) executed in a Databricks workspace -- there is no local build system, package manager, or CI pipeline. The `spec-as-code/` YAML files define organizational structure, metric taxonomy, and scoping rules.

## Read Order

1. This file
2. `abac/README.md` -- the working requirements spec (contracts, normalization rules, metric-specific logic)
3. The target notebook(s) under `abac/`
4. `audit.md` -- QA/governance SOP (Jira workflow states, validation gates)

Treat repo files as source of truth, not chat history.

## Repository Layout

```
abac/                        # 16 Databricks SQL notebooks + tests/
  00_CC_Mapping_Setup.ipynb  # Creates vw_cost_center_mapping_bootstrap (run first)
  eba01-07, emp01-07, geo02, tp01-05  # Metric notebooks
  tests/scrambles.ipynb      # AU mapping consistency test
spec-as-code/                # YAML policy inputs (org_structure, metric taxonomy, scoping)
audit.md                     # Validation & governance SOP
```

## Running & Testing

All notebooks execute in Databricks SQL, not locally. There is no `make`, `pytest`, or local test runner.

- **Bootstrap dependency**: If `00_CC_Mapping_Setup.ipynb` changes, rerun it before any downstream notebook that uses `vw_cost_center_mapping_bootstrap`.
- **Validation test**: `abac/tests/scrambles.ipynb` checks AU mapping consistency (Master AU list vs Cost Center mapped AUs).

## Architecture: Three Core Contracts

### 1. Master AU Anchoring

Every metric notebook follows this pattern:
1. Build filtered `Master_AUs` (`WHERE BusinessID IS NOT NULL AND Jurisdiction IN ('CANADA','HONG KONG','BARBADOS') AND US_OR_CANADA = 'CANADA'`)
2. Extract and filter source data
3. Bridge source rows to AU (via Cost Center or TP mapping)
4. Aggregate by bridged AU
5. `LEFT JOIN` back to `Master_AUs`
6. `COALESCE`/`CASE` so every master AU gets a concrete default (`0` for counts, `No` for yes/no, `0%` for percentages)

### 2. Cost Center Normalization

All CC-driven metrics (EBA, EMP, GEO families) must apply this canonical rule on **both** source-side and mapping-side values:

```sql
CASE
    WHEN TRIM(cc) RLIKE '^[0-9]+$'
    THEN LPAD(RIGHT(TRIM(cc), 4), 4, '0')   -- 66 -> 0066, 000066 -> 0066
    ELSE UPPER(TRIM(cc))                      -- alphanumeric preserved
END
```

Never cast to INT, never prefix-match, never strip alpha chars. Exact equality on normalized string only. Bridge is always through `vw_cost_center_mapping_bootstrap`.

### 3. Third-Party (TP) Fan-Out

TP metrics bridge through `third_party_unit_mapping`, not Cost Center. One engagement can map to multiple AUs. The fan-out must happen **before** aggregation -- do not collapse to a single AU first. Each mapped AU independently receives the response.

## Metric Families

| Family | Bridge Method | Notebooks |
|--------|--------------|-----------|
| **EBA** (expense/engagement) | Cost Center via Coupa `Account` split or Finance `CostCenter` | eba01, eba02, eba04, eba06, eba07 |
| **EMP** (employee/workforce) | Cost Center or DeptID | emp01, emp03, emp04, emp05, emp07 |
| **GEO** (travel/jurisdiction) | Cost Center | geo02 |
| **TP** (third-party) | `third_party_unit_mapping` / `Assessable_Unit_ID` | tp01-tp05 |

## Key Business Rules

- **EBA category codes**: `066, 009, 012, 067, 095, 134, 168, 192, 203, 204, 208, 209, 242, 269, 270, 484, 487, 636, 637, 638, 639, 676, 782, 783, 784, 792, 793, 890, 892`
- **793 exception**: Category code `793` is only valid for AU `101016`. Exclude if bridged AU differs.
- **EBA02 PublicOfficial**: must be `Y` or `YES`
- **EBA04 PublicOfficial**: must be `N` or `NO`; amount threshold `> 250`

## Debug Output Standard

Debug/reasoning cells follow a columnar convention:
- Left: `BusinessID`, `AU_Name`, `Business_Segment`, `QuestionID`
- Middle: `Response`, bridge key list, calculation columns
- Right: explanation (`Why_Yes`/`Why_No`/`Calculation_Formula`/`Debug_Reason`), `In_ABAC_AU_List`

If a debug query's output columns change, update the inline `-- Output columns:` comment block above that query's final `SELECT` in the same commit.

## Change Checklist

Before accepting a metric change, verify per `abac/README.md` Section 10:
1. Source extraction logic is correct for that dataset
2. Output is anchored to filtered master AU list
3. CC normalization applied on both sides (source + mapping)
4. CC metrics bridge through `vw_cost_center_mapping_bootstrap`
5. TP metrics preserve one-to-many fan-out
6. Every in-scope master AU has a concrete default response
7. Debug output explains both positive and negative routing
8. Threshold/amount parsing is deterministic and documented in-notebook
9. If bootstrap changed, rerun `00_CC_Mapping_Setup.ipynb` first

## Editing Conventions

- Prefer comment-only notebook edits for documentation-only requests.
- Keep `abac/README.md` aligned with shared conventions; don't leave important context only in notebooks.
- Data quality: prefer deterministic handling over silent drops. Malformed keys, mapping failures, and out-of-scope rows should surface in debug output.
