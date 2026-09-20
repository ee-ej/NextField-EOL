# NextField EOL Governance Recommendations

Date: 2026-09-03
Status: Recommended resolutions for approval

## Purpose

This document explains the four governance items that remain after approval of the workbook source contract and row-boundary rules. The recommendations are intended to unblock local transformation and model validation while preserving a clear distinction between workbook evidence, derived results, and governed business rules.

## Recommendation Summary

| Governance item | Recommendation | Why this lets the project move forward |
|---|---|---|
| 0.6 cost factor | Carry the factor as an explicit, versioned parameter in the PoC cost calculation, with provenance and a visible assumption flag. | It preserves workbook parity without silently claiming that the factor is permanently governed policy. |
| Output score authority | Treat entry sheets as source facts, `Scoring Engine` as calculation evidence, and output score sheets as derived result facts. | It preserves the displayed workbook result while keeping the calculation lineage testable. |
| KPI counts | Use bounded valid rows and distinct business keys; publish site, asset, equipment-row, and scored-asset measures separately. | It prevents the 70-versus-9,070 relationship from being presented as a contradiction or hidden by one ambiguous count. |
| SPOF normalization | Normalize to one row per site/question, preserve all answer states and source coordinates, and quarantine unresolved groups. | It produces an analyzable fact table without inventing coverage or collapsing missing evidence into a negative answer. |

## 1. The 0.6 cost factor

### What the question is

The workbook exposes an overall cost correction or safety factor of `0.6`. It is distinct from the equipment-size exponent of `0.8`, inflation, and regional multipliers. The question is whether `0.6` should become permanent governed business logic or remain a workbook-specific convention.

### Recommendation

Use `0.6` in the PoC as an explicit parameter named `OverallCostCorrectionFactor`, defaulted from the workbook, with these controls:

- Record the source sheet, source cell or range, workbook version, and effective date.
- Apply it as a separate step after the component cost calculation and document the exact order with size scaling, regional adjustment, and inflation.
- Expose the factor and an `AssumptionStatus` of `Workbook-derived` in validation artifacts.
- Do not hide it inside a measure or hard-code it without provenance.
- Require SME confirmation before treating it as permanent enterprise policy.

### Why

This gives the PoC reproducible workbook parity and makes the assumption visible. Removing the factor now would change results without evidence; silently making it permanent would overstate governance.

### Required test

Recalculate representative costs with and without the factor, compare both to the workbook output, and record the adjustment order and any unexplained difference.

## 2. Authority of the output score tables

### What the question is

`Output- Asset Scores` and `Output- Site Risk Scores` contain useful business results, but they include rendered output structure, formulas, padding, and dependencies on `Scoring Engine`. The question is whether they should be treated as authoritative fact tables.

### Recommendation

Use a three-layer authority model:

1. **Source facts:** bounded rows from the entry sheets, including asset and site inputs.
2. **Calculation evidence:** `Scoring Engine`, retained for lineage and reconciliation, not presented as the user-facing fact source.
3. **Derived result facts:** cleaned rows from the output score sheets, linked to source keys and source row references.

The derived result facts may drive the first report only after the bounded output rows and engine alignment pass. They must include:

- `AssetId` or `SiteNo`
- score context and calculation version
- source sheet and source row
- engine row reference where available
- validation status

### Why

The output sheets are the closest available representation of the workbook's intended result, but their formulas and padding make them unsafe as unqualified source tables. This recommendation preserves the business result while keeping it replaceable by a future independently calculated model.

### Required test

Validate source-to-engine-to-output alignment across the full bounded population. Report missing keys, duplicate keys, zero identifiers, and score differences instead of silently correcting them.

## 3. KPI count rules

### What the question is

The workbook contains approximately 70 sites and 9,070 asset records. These are different grains, not competing versions of one KPI. Output row counts are further distorted by generated and padded rows.

### Recommendation

Publish these measures separately:

| Measure | Definition | Use |
|---|---|---|
| Sites in portfolio | Distinct valid `SiteNo` from bounded `Entry- Site Data` rows | Portfolio scope |
| Assets in source | Distinct valid nonblank, typed `AssetId` from bounded `Entry- Eq Database` rows | Source population |
| Equipment rows | Count of bounded valid asset input rows | Input-row volume and data-quality checks |
| Scored assets | Distinct valid nonzero `AssetId` in bounded derived score rows | Score coverage |
| Scored rows | Count of bounded derived score rows with valid asset and site context | Output grain and duplicate detection |
| SPOF observations | Count of normalized site/question rows by normalization status | Evidence coverage |
| SPOF exceptions | Count of normalized observations meeting the approved risk rule | Risk exceptions, after rule validation |

The leadership page should show the first two as portfolio context and show scored-asset coverage separately. It should never label 9,070 as a site count or use output UsedRange rows as a KPI.

### Why

Distinct business keys answer population questions; row counts answer data-quality and processing questions. Keeping both makes reconciliation visible and prevents padding or duplicate rows from changing the headline story.

### Required test

Produce a bounded KPI manifest with counts, duplicate counts, excluded rows, missing source-to-score keys, and the exact validity predicate used for every measure.

## 4. SPOF normalization

### What the question is

The SPOF input is a transposed matrix with repeated site groups. It includes answer markers, comments, blanks, and `N/A` values. One site appears not to map to the 69 apparent four-column groups, so coverage must not be forced to match.

### Recommendation

Create a normalized `FactSPOFObservation` with one row per `SiteNo` and `SPOFQuestionId`, plus provenance:

- Preserve `Yes`, `No`, `N/A`, and `Blank` as distinct states.
- Normalize `x` and `X` as selected markers while retaining the original marker.
- Preserve comments even when the answer is blank or `N/A`.
- Flag multiple selected answers as `MultipleAnswers`; do not choose silently.
- Flag an unknown or missing site group as `UnmappedSite`; do not infer the missing site.
- Retain source sheet, source column start/end, source rows, group date, and lead where available.
- Keep invalid, incomplete, and unmapped records in a quarantine output for reconciliation, separate from governed exception measures.

### Why

A blank means missing evidence, not `No`. `N/A` means not applicable, not a negative response. Provenance and quarantine allow the team to reconcile the apparent 69-versus-70 coverage gap without corrupting the risk model.

### Required test

Reconcile discovered site groups to the 70-site input population, verify group widths, count question rows, normalize answer markers, and compare normalized results to the recalculated site-risk output. Document the missing or nonstandard group explicitly.

## Recommended implementation sequence

1. Generate a bounded source and KPI manifest using the approved row predicates.
2. Build the SPOF normalization artifact with valid and quarantine outputs.
3. Run the full source-to-engine-to-output alignment check.
4. Recalculate representative scores and costs, including threshold boundary tests.
5. Use only validated derived facts in the local model prototype.
6. Keep the 0.6 factor, score authority, and SPOF risk semantics versioned until SME confirmation.
7. Request publication approval only after local model and report validation is complete.

## Decision boundary

These recommendations are suitable for local PoC implementation under the approved source contract. They do not authorize Fabric publication, permanent enterprise policy, or remote writes. Those remain separate approvals.
