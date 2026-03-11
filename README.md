# databricks_examples

This repository contains Databricks notebooks for ABAC-related metrics. The notebooks are grouped by metric family under `abac/`:

- `00_CC_Mapping_Setup.ipynb`: builds the shared Cost Center to AU bootstrap view.
- `eba*.ipynb`: engagement / expense-based metrics.
- `emp*.ipynb`: employee / HR-based metrics.
- `geo*.ipynb`: geography / travel-based metrics.
- `tp*.ipynb`: third-party metrics.

This README is the current working spec for shared normalization and mapping behavior.

## Shared Cost Center Spec

Any metric that derives an AU from a Cost Center must normalize the Cost Center first and then map it through `vw_cost_center_mapping_bootstrap`.

Canonical Cost Center normalization:

```sql
CASE
    WHEN TRIM(cc_value) RLIKE '^[0-9]+$'
    THEN LPAD(RIGHT(TRIM(cc_value), 4), 4, '0')
    ELSE UPPER(TRIM(cc_value))
END
```

Required behavior:

- Numeric Cost Centers are canonicalized to exactly 4 digits.
- Examples: `66` -> `0066`, `0066` -> `0066`, `000066` -> `0066`.
- Alphanumeric Cost Centers are preserved as strings and only normalized with `TRIM` + `UPPER`.
- Do not cast Cost Centers to `INT`.
- Do not use subset, prefix, suffix, or partial matching.
- Cost Center comparison must be exact equality on the normalized value.

## Bootstrap View Contract

`abac/00_CC_Mapping_Setup.ipynb` is the single source of truth for Cost Center to AU mapping.

The temp view:

- Name: `vw_cost_center_mapping_bootstrap`
- Output contract: normalized `Cost_Center_ID`, `AU_ID`, `AU_Name`, `Segment_Name`
- Normalizes numeric Cost Centers to canonical 4-digit form
- Preserves alphanumeric Cost Centers

Downstream notebooks should assume:

- if a metric needs AU attribution from a Cost Center, it must bridge through this view
- mapping-side Cost Center values must be normalized using the same rule before comparison

After changing `abac/00_CC_Mapping_Setup.ipynb`, rerun it before rerunning dependent notebooks.

## Final Output Contract

Final metric output must be anchored to the filtered master AU list, not to the raw mapped transaction set.

Required behavior:

- Final output must return one row for every AU in the master list used by that metric.
- AU IDs that exist in source or mapping data but do not exist in the master list must not create extra rows in final output.
- If a master AU has no qualifying mapped records, still return the AU with the metric's default response.
- Default responses must follow metric type:
- count metrics: `0`
- boolean / yes-no metrics: `No`
- percentage metrics: `0%`
- Blank responses are not allowed in final master-anchored output unless a metric explicitly documents an exception.

Implementation pattern:

- build `Master_AUs` or equivalent filtered master list first
- aggregate qualifying records by mapped `AU_ID`
- `LEFT JOIN` aggregated results back to the master list
- apply `COALESCE` or `CASE` so every master AU gets a concrete response

## EBA Metric Rules

Shared EBA Cost Center behavior:

- If the source is Coupa, parse Cost Center from `SPLIT(Account, '-')[0]`.
- If the source is Finance, use `CostCenter`.
- Normalize the parsed Cost Center using the shared Cost Center spec before joining to mapping.
- For Coupa-based metrics, Category Code comes from `SPLIT(Account, '-')[2]` when the metric logic depends on the Account string.

Current EBA alignment:

- `eba01`, `eba02`, `eba04`, `eba06`, `eba07` now normalize Cost Centers with the shared canonical rule.
- `eba02` and `eba04` debug cells were aligned to show explicit positive and negative pipeline outcomes.
- `eba07` final output defaults unmapped / no-data master AUs to `No` rather than blank.

## EMP / GEO Metric Rules

Current shared behavior:

- `emp01`, `emp03`, `emp05`, and `geo02` normalize source-side Cost Centers with the same canonical rule.
- Mapping joins in those notebooks also use normalized mapping-side Cost Centers.
- `DeptID` in `emp03` is treated as a Cost Center key and normalized before joining.

## TP Metric Rules

`tp01` through `tp05` do not use Cost Center to AU mapping as their primary bridge. They bridge using third-party mapping fields such as `Assessable_Unit_ID` and AU names / numeric IDs, so the Cost Center normalization rule does not directly apply there.

## Debug / Review Expectations

When a metric has a debug notebook cell, it should help explain both retained and dropped records.

Preferred debug behavior:

- show the normalized Cost Center used for mapping
- show whether AU mapping succeeded
- show rule-by-rule checks where practical
- show a final kept / dropped or yes / no decision
- include positive-case explanation columns such as `Why_Yes` when the metric is boolean / decision-based

## Change Checklist

Before accepting a Cost Center-related metric change, verify:

1. Source Cost Center extraction is correct for that dataset.
2. Source Cost Center normalization uses the canonical rule above.
3. Mapping-side Cost Center normalization uses the same rule.
4. AU bridging goes through `vw_cost_center_mapping_bootstrap` when the metric is Cost Center-driven.
5. Matching is exact equality on normalized Cost Center values.
6. No `INT` casts remain on Cost Center comparison paths.
7. If `00_CC_Mapping_Setup.ipynb` changed, rerun it before validating downstream results.
