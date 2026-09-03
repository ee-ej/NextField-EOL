# Source Mapping Proposal

Date: 2026-09-02
Status: Proposed for review

## Purpose

Define the first validation pass from the authoritative workbook into a governed analytical model. This is a mapping proposal, not an approved semantic-model definition.

## Current Source Strategy

For this PoC, the Excel workbook is the only available source and is treated as the source of record. CMMS/EAM remains the presumed future operational source; Dataverse remains a future integration option. No source-system connector or migration assumption is part of this proposal.

## Candidate Fact Tables

| Candidate table | Workbook source | Grain to verify | Initial validation |
|---|---|---|---|
| Asset score | `Output- Asset Scores` backed by `Scoring Engine` | One scored equipment row per `AssetId` and scoring context | Treat output as a rendered result; confirm source-to-engine row alignment, duplicate AssetId behavior, blank rows, and whether `Original Order` is needed for traceability |
| Site risk | `Output- Site Risk Scores` and `Output- Site Scores` | One site/category or one site/question row, depending on the report question | Separate site summary grain from question-level SPOF evidence |
| Capital forecast | `Output- Budget Forecasting` | One asset/site/year forecast row | Confirm whether years are rows, columns, or repeated output blocks |

## Candidate Dimensions

| Candidate dimension | Workbook source | Candidate key | Validation required |
|---|---|---|---|
| Asset | `Entry- Eq Database` | `AssetId` | Profile all 233 source columns; approve the projected governed column set |
| Site | `Entry- Site Data` | `Site No.` / `SiteNo` | Resolve naming, uniqueness, inactive/test sites, and relationship to asset rows |
| Asset type | `Costs and Scoring` and category fields | Equipment/category name | Confirm category normalization and plus-one equipment categories |
| Date/year | Forecast output and source dates | Year or date | Confirm whether annual forecast requires a true date dimension |
| Scoring weights | `Criteria` | Criterion name | Preserve workbook values 100, 89, 78, 67, 56, 44, 33, 22, 11 unless SME-approved otherwise |
| Score zone | Workbook thresholds and business rules | Zone/range | Confirm score bands and inclusive/exclusive boundaries |

## SPOF Normalization Proposal

The source matrix should be converted from repeated site column groups into a long-form evidence table.

Candidate output:

| Field | Meaning |
|---|---|
| `SiteNo` | Site identifier from the site header group |
| `SPOFQuestionId` | Stable question identifier such as `1.05` or `6.02` |
| `SPOFQuestion` | Full question text |
| `Answer` | `Yes`, `No`, or `N/A` based on the marked source cell |
| `DetailedComments` | Site/question comments where present |
| `SourceSheet` | `Entry- Site SPOF Data` |
| `SourceColumnGroup` | Original site group location for traceability |

Validation must determine the exact site-group start/end columns, repeated header rows, case variants in `x`/`X`, blank versus `N/A`, and whether multiple selections are possible for one question.

The inspected matrix currently suggests 69 four-column site blocks across columns 7-282, while the site input contains 70 distinct site numbers. The block-to-site reconciliation is therefore an explicit validation item; no site should be inferred, dropped, or duplicated to force the counts to agree.

## Measures and Rules to Reconcile

- Weighted score: reproduce the nine workbook criteria using the exact workbook weights before considering dynamic model measures.
- Size-scaled cost: validate exponent `0.8` independently for each equipment class.
- Overall cost correction/safety factor: treat the workbook value `0.6` as a separate rule requiring an explicit business decision.
- SPOF threshold: validate the apparent default threshold `7.0` and whether it applies to question, category, site, or report context.
- Replacement threshold: validate the apparent default threshold `50` and whether it is applied to precomputed or recomputed overall scores.
- KPI counts: define separate measures for sites, distinct assets, equipment rows, and scored rows so the `70` versus approximately `9,070` discrepancy is explainable.

## Validation Sequence

1. Profile workbook sheets and identify clean source ranges, header rows, data rows, and blank/footer regions.
2. Produce column-level mapping from source headers to candidate model fields, including data type and transformation rule.
3. Trace sample asset rows through `Scoring Engine`, recalculate the nine criteria from source inputs, and compare the engine result to `Output- Asset Scores`.
4. Recalculate sample site risk and SPOF counts from the transposed matrix and compare them to output sheets.
5. Recalculate sample cost scaling and the separate correction factor.
6. Reconcile site, asset, equipment, and scored-row counts.
7. Review the legacy screenshots against the validated grains and measures.
8. Approve the model contract before creating local PBIP/TMDL implementation artifacts.

## Explicit Non-Assumptions

- CMMS/EAM is not yet confirmed as the source of record.
- Dataverse is not selected as a source; it remains a possible future source.
- The starter TMDL is not accepted as the final schema.
- The workbook's output sheets are not assumed to be clean fact tables until their grains are profiled.
- The legacy dashboard screenshots do not dictate a pixel-perfect layout.
- No Fabric semantic model, Lakehouse table, report, or remote object is created by this proposal.
