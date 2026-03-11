# databricks_examples

## Specification Principles

### 1. Establish Strict Data Contracts Upfront

Many of the issues in this workspace came from unexpected source-system changes, such as:

- missing columns like `DocumentType`
- numeric fields arriving as strings
- schema assumptions changing after logic was already written

**Requirement**

The specification must act as a binding data contract. Before engineering begins, upstream data owners must validate:

- exact schemas
- column names
- data types
- expected null and blank behavior

If the source changes, the contract should expose the mismatch before it breaks downstream logic.

### 2. Define Data Governance and Edge-Case Routing

A large amount of rework came from dirty or ambiguous data, such as:

- the string `Yes` appearing in an ID field
- blank bridge keys
- malformed account strings
- rows that could not be mapped cleanly

**Requirement**

Specifications must include explicit data quality handling rules. They should define what happens when records fail validation instead of assuming the data is clean.

At minimum, each spec should define:

- what happens when a required field is blank
- what happens when a bridge key cannot be parsed
- whether invalid rows are dropped, flagged, quarantined, or reported
- how unmapped rows appear in debug output

### 3. Translate Policy Into Deterministic Logic

Complex policy rules surfaced iteratively during implementation, including:

- the active EBA category code lists
- the strict `793 -> AU 101016` exception
- threshold rules
- master-list anchoring rules

**Requirement**

Business policy should not remain as narrative text only. It should be translated into deterministic logic that engineers can implement directly.

Preferred formats:

- decision tables
- `IF / THEN / ELSE` rules
- inclusion and exclusion matrices
- explicit source-to-output mappings

This reduces interpretation risk and keeps notebook logic aligned with compliance intent.
