# ABAC Workspace Requirements

This document is the working requirements specification for the notebooks under `abac/`.

It summarizes the current implemented logic, shared contracts, and troubleshooting expectations for:

- `00_CC_Mapping_Setup.ipynb`
- `eba01.ipynb`
- `eba02.ipynb`
- `eba04.ipynb`
- `eba06.ipynb`
- `eba07.ipynb`
- `emp01.ipynb`
- `emp03.ipynb`
- `emp05.ipynb`
- `geo02.ipynb`
- `tp01.ipynb`
- `tp02.ipynb`
- `tp03.ipynb`
- `tp04.ipynb`
- `tp05.ipynb`

## 1. Workspace Scope

The ABAC workspace produces Databricks SQL metrics for several families:

- `EBA`: expense / engagement-based metrics
- `EMP`: employee and workforce metrics
- `GEO`: travel and jurisdiction metrics
- `TP`: third-party metrics

All metric notebooks are expected to follow the shared output and mapping contracts in this document unless a notebook explicitly documents a justified exception.

## 2. Master AU Contract

Final outputs must be anchored to the filtered master AU list, not to raw source rows.

Standard master AU filter:

```sql
WHERE BusinessID IS NOT NULL
  AND UPPER(TRIM(Jurisdiction)) IN ('CANADA', 'HONG KONG', 'BARBADOS')
  AND UPPER(TRIM(US_OR_CANADA)) = 'CANADA'
```

Required behavior:

- Final output returns one row per master AU in scope.
- Source rows or mappings that do not bridge to a master AU must not create extra rows in final output.
- If a master AU has no qualifying activity, it must still appear with a default response.
- Default responses:
  - count metrics: `0`
  - yes/no metrics: `No`
  - percentage metrics: `0%`

Implementation pattern:

1. Build filtered `Master_AUs`.
2. Build source-side qualifying rows.
3. Bridge to AU.
4. Aggregate by bridged AU.
5. `LEFT JOIN` aggregated results back to `Master_AUs`.
6. `COALESCE` or `CASE` the response so every master AU has a concrete value.

## 3. Cost Center Mapping Contract

Any metric that derives AU from Cost Center must bridge through:

- `vw_cost_center_mapping_bootstrap`

Source notebook:

- `00_CC_Mapping_Setup.ipynb`

### 3.1 Canonical Cost Center Normalization

Use this normalization rule on both source-side and mapping-side Cost Center values:

```sql
CASE
    WHEN TRIM(cc_value) RLIKE '^[0-9]+$'
    THEN LPAD(RIGHT(TRIM(cc_value), 4), 4, '0')
    ELSE UPPER(TRIM(cc_value))
END
```

Required behavior:

- Numeric Cost Centers must compare as canonical 4-digit strings.
- Examples:
  - `66` -> `0066`
  - `0066` -> `0066`
  - `000066` -> `0066`
- Alphanumeric Cost Centers must remain strings.
- Do not cast Cost Centers to `INT`.
- Do not strip alphabetic characters.
- Do not use subset or prefix matching.
- Matching must be exact equality on normalized Cost Center.

### 3.2 Bootstrap View Output

`vw_cost_center_mapping_bootstrap` is the single source of truth for Cost Center to AU bridge logic.

Expected output columns:

- `Cost_Center_ID`
- `AU_ID`
- `AU_Name`
- `Segment_Name`

Operational rule:

- If `00_CC_Mapping_Setup.ipynb` changes, rerun it before rerunning dependent notebooks.

## 4. Debug Output Contract

Debug cells are for traceability. They should make record routing explainable.

Required behavior for debug outputs where practical:

- show normalized Cost Center or equivalent bridge key
- show mapped AU and bridged master AU
- show key rule-check columns
- show positive outcomes, not only dropped outcomes
- show explicit explanation columns such as `Why_Yes`, `Why_No`, or `Debug_Reason`
- place key identifiers to the left of the output:
  - Cost Center
  - mapped AU ID / name
  - bridged master AU ID / name

Debug outputs may be:

- AU-level summaries
- row-level traceability tables

Final metric output must always be master-anchored even if the debug cell is row-level.

## 5. EBA Requirements

### 5.1 Shared EBA Rules

For Coupa-based EBA metrics:

- Cost Center is derived from `SPLIT(Account, '-')[0]`
- Category Code is derived from `SPLIT(Account, '-')[2]`

For Finance-based EBA metrics:

- Cost Center comes from `CostCenter`

Where AU is Cost Center-driven:

- normalize the source Cost Center with the canonical rule
- normalize mapping Cost Center with the same rule
- bridge through `vw_cost_center_mapping_bootstrap`

### 5.2 Shared EBA Category Rule

The active high-risk EBA category code list is:

`066, 009, 012, 067, 095, 134, 168, 192, 203, 204, 208, 209, 242, 269, 270, 484, 487, 636, 637, 638, 639, 676, 782, 783, 784, 792, 793, 890, 892`

### 5.3 Shared 793 Exception

Category code `793` is only valid for AU `101016`.

Required behavior:

- if `CatCode = '793'` and bridged AU is not `101016`, the row must be excluded
- if `CatCode = '793'` and bridged AU is `101016`, the row may continue through the rest of the logic

### 5.4 EBA Notebook-Specific Requirements

#### EBA01

- combines Coupa and Finance signals
- final response type: yes/no
- debug traces parsed Cost Center, mapped AU, category, and 793 handling

#### EBA02

- Coupa-driven
- final response type: yes/no
- `PublicOfficial` rule: must be `Y` or `YES`
- final output must return all master AUs
- debug is master-anchored at AU level and must explain both yes and no outcomes

#### EBA04

- Coupa-driven
- final response type: count
- `PublicOfficial` rule: must be `N` or `NO`
- amount rule: parse amount-like tokens from `Total`, normalize locale variants, and use the maximum parsed amount
- threshold rule: `Numeric_Total > 250`
- mixed currency labels do not control inclusion; if any parsed amount exceeds `250`, the row qualifies
- debug must expose parse-stage failures, amount parsing, mapping outcome, and final yes/no decision per row

#### EBA06

- Finance-driven
- final response type: count
- Cost Center-driven AU mapping must use the shared canonical Cost Center rule

#### EBA07

- Finance-driven
- final response type: yes/no
- final output must return all master AUs and default missing AUs to `No`

## 6. EMP Requirements

### 6.1 Shared EMP Rules

EMP metrics using Cost Center or department-based AU attribution must normalize source-side and mapping-side values with the canonical Cost Center rule before bridging.

### 6.2 Current EMP Notebook Expectations

#### EMP01

- source-side extracted Cost Center is normalized with canonical rule
- mapping-side Cost Center is normalized with the same rule

#### EMP03

- `DeptID` is treated as the Cost Center bridge key
- `DeptID` must remain string-based
- numeric `DeptID` values normalize to canonical 4-digit strings
- alphanumeric `DeptID` values must be preserved

#### EMP05

- contingent worker logic
- Cost Center normalization and AU bridging follow the shared Cost Center contract

## 7. GEO Requirements

### GEO02

- unions AMEX and CWT travel data
- high-risk country logic uses exact jurisdiction match against the risk-rating table
- Cost Center normalization and AU bridge follow the shared Cost Center contract
- final output is master-anchored

## 8. TP Requirements

TP metrics do not primarily bridge by Cost Center. They bridge through:

- `third_party_unit_mapping`
- `Assessable_Unit_ID`
- `TPRM_Units`
- master AU `BusinessID` or `AU_Name`

### 8.1 Shared TP Mapping Contract

`third_party_unit_mapping` may represent a one-to-many relationship:

- one `TPRM_Units` value can map to multiple assessable units
- one matched third-party row can therefore fan out to multiple AUs

Required behavior:

- do not collapse a mapping to a single AU before aggregation
- when one source row bridges to multiple valid master AUs, each bridged AU must receive the response
- the fan-out must happen before aggregation by AU

This means:

- count metrics may count the same engagement once in each mapped AU
- yes/no metrics may return `Yes` for each mapped AU touched by the engagement
- percentage metrics may include the same engagement in numerator/denominator for each mapped AU it validly bridges to

### 8.2 Shared TP Parsing Rules

TP notebooks commonly apply:

- comma-protection dictionary for `owning_lob` and `lob_using`
- `explode(split(...))` to flatten LOB strings
- wildcard match from expanded LOB to `TPRM_Units`
- dual bridge from mapping to master AU:
  - match on `Assessable_Unit_ID = BusinessID`
  - or match on `Assessable_Unit_ID = AU_Name`

### 8.3 Current TP Notebook Expectations

#### TP01

- high-risk jurisdiction engagement count
- if all jurisdiction columns are blank, row is treated as high risk
- final response type: count

#### TP02

- high-value engagement percentage
- final response type: percentage

#### TP03

- high-risk services / targeted KPI signal
- final response type: yes/no

#### TP04

- sole-source plus jurisdiction risk logic
- final response type: count

#### TP05

- government interaction / permit / approval logic
- final response type: count

## 9. Data Quality Requirements

The notebooks must prefer deterministic handling over silent drops.

Required behavior:

- malformed bridge keys should surface in debug outputs where practical
- mapping failures should be distinguishable from business-rule failures
- rows outside the filtered master AU list should be explainable in debug output
- blanks and nulls should resolve to explicit default output behavior in final metric outputs

## 10. Change Checklist

Before accepting a metric change, verify:

1. The source extraction logic is correct for that dataset.
2. The metric is anchored to the filtered master AU list.
3. Cost Center-driven metrics normalize both source-side and mapping-side values with the canonical rule.
4. Cost Center-driven metrics bridge through `vw_cost_center_mapping_bootstrap`.
5. TP metrics preserve one-to-many AU fan-out from `third_party_unit_mapping`.
6. Final outputs return every in-scope master AU with a concrete default response.
7. Debug output explains both positive and negative routing where practical.
8. Key identifiers appear early in debug tables for troubleshooting.
9. Any threshold or amount parsing logic is deterministic and documented in the notebook.
10. If bootstrap mapping logic changed, rerun `00_CC_Mapping_Setup.ipynb` before downstream validation.
