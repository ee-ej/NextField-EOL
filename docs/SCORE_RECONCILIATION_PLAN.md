# Score Reconciliation Plan

Date: 2026-09-03
Status: Approved execution plan under the source contract

## Objective

Prove whether the workbook's asset and site scores can be reproduced from bounded source inputs and the workbook's calculation logic before creating a governed semantic model.

## Current Evidence

- `Output- Asset Scores` is a rendered output layer whose score cells reference `Scoring Engine` cells.
- In the sample, output rows for AssetIds 2-5 reference engine rows 21-24, and the corresponding engine rows contain those same AssetIds.
- `Criteria` defines nine weighted criteria: 100, 89, 78, 67, 56, 44, 33, 22, and 11.
- `Costs and Scoring` defines replacement threshold `50.0`, new-equipment base score `15.0`, chart mid-score `32.5`, yearly inflation `3.5%`, size exponent `0.8`, overall cost factor `0.6`, and regional multipliers by `Site No.`.
- Read-only Excel and XLSX-package probes exposed formulas but did not provide a dependable numeric cache for sample score cells. Numeric equality is therefore not yet established.

## Controlled Validation Steps

1. Create a disposable working copy outside `source/`; never recalculate or save over the authoritative workbook.
2. Open the working copy in a controlled Excel calculation session and force a full calculation.
3. Export only bounded sample rows from `Entry- Eq Database`, `Scoring Engine`, and `Output- Asset Scores` to a temporary validation artifact.
4. Verify source-row to engine-row alignment across the bounded asset population using `AssetId`, `SiteNo`, category, and original order.
5. Compare each of the nine component scores and the overall score between the engine and output layer.
6. Recalculate a small sample independently from source inputs and the criteria weights; record every formula or lookup that cannot be reproduced.
7. Test assets with retired/available status, blank purchase date, multiple site numbers, missing category, and score exactly at threshold `50.0`.
8. Reconcile replacement cost using equipment type, size, exponent, regional multiplier, inflation year, and the `0.6` factor. Record the exact adjustment order.
9. Reconcile site-risk output against normalized SPOF answers and the apparent SPOF threshold `7.0`.
10. Approve the resulting formula, boundary, and exception contract before semantic-model implementation.

## Required Validation Outputs

| Output | Purpose |
|---|---|
| Bounded source-row manifest | Establish authoritative row boundaries and provenance |
| Engine alignment report | Prove or disprove AssetId/original-order alignment |
| Component score comparison | Identify reproduced, transformed, and unexplained values |
| Threshold boundary tests | Document inclusive/exclusive behavior at `50.0` and `7.0` |
| Cost formula trace | Establish adjustment order and units |
| Exception register | Capture excluded rows, zeros, blanks, duplicates, and multi-site assets |
| SME decision log | Approve business interpretations before governed measures |

## Guardrails

- Preserve `source/` unchanged.
- Do not treat formulas, UsedRange length, or cached values as sufficient evidence of a governed KPI.
- Do not implement Invest/Validate/Sequence/Monitor states until business rules are approved.
- Do not create or publish a Fabric semantic model or report during this validation phase.
