# Repository Agent Guide

This repository is documentation-heavy and notebook-heavy. Future agents should treat the repo files, not chat history, as the source of truth.

## Read Order

1. [`README.md`](./README.md)
2. [`abac/README.md`](./abac/README.md)
3. The target notebook(s) under [`abac/`](./abac)

## Primary Working Area

The main maintained implementation area is [`abac/`](./abac).

Key files:

- [`abac/00_CC_Mapping_Setup.ipynb`](./abac/00_CC_Mapping_Setup.ipynb): creates `vw_cost_center_mapping_bootstrap`
- [`abac/README.md`](./abac/README.md): current ABAC implementation contract
- [`spec-as-code/`](./spec-as-code): structured policy/taxonomy inputs

## ABAC Non-Negotiables

- Final metric outputs are anchored to filtered `Master_AUs`.
- Cost Center-driven metrics bridge through `vw_cost_center_mapping_bootstrap`.
- Canonical Cost Center normalization is shared across source-side and mapping-side logic.
- TP notebooks preserve one-to-many fan-out from `third_party_unit_mapping`.
- Final outputs must still return every in-scope master AU with a concrete default response.

## Debug And Reasoning Output Standard

Customer-facing ABAC debug/reasoning queries follow this pattern:

- AU-level summary table first, when practical
- key identifiers on the left: `BusinessID`, `AU_Name`, `Business_Segment`, `QuestionID`
- result column: `Response`
- bridge or trace columns next
- calculation detail columns next
- explanation column such as `Calculation_Formula`, `Debug_Reason`, `Why_Yes`, or `Why_No`
- `In_ABAC_AU_List` at the end for master-list confirmation

Required maintenance rule:

- if a debug/reasoning query output changes, update the inline `-- Output columns:` comment block immediately above that query's final `SELECT` in the same change

## Notebook Inventory

- `eba01`: Coupa + Finance EBA logic with AU-level debug review
- `eba02`: Public Official EBA logic
- `eba04`: non-Public Official / threshold EBA logic
- `eba06`: donation-focused finance logic
- `eba07`: marketing-focused finance logic
- `emp01`: Canadian PEP yes/no logic
- `emp03`: lower-of ABAC and CoC training compliance
- `emp04`: flagged investigation/case routing count
- `emp05`: contingent-worker high-risk logic
- `emp07`: flagged OBA employee routing count
- `geo02`: high-risk travel logic
- `tp01`: high-risk jurisdiction engagement count
- `tp02`: high-value engagement percentage
- `tp03`: targeted KPI / product-service yes-no logic
- `tp04`: sole-source plus jurisdiction-risk count
- `tp05`: government interaction / permit / approval count

## Change Hygiene

- If `00_CC_Mapping_Setup.ipynb` changes, downstream notebooks depending on `vw_cost_center_mapping_bootstrap` should be rerun.
- Prefer comment-only notebook edits when the request is documentation-only.
- Keep [`abac/README.md`](./abac/README.md) aligned with shared conventions rather than leaving important context only inside notebooks or chat.
