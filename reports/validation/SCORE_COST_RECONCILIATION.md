# Score and Cost Reconciliation Baseline

Date: 2026-09-03
Status: Initial control-input validation; controlled recalculation attempted; numeric formula equality remains open

## Verified workbook controls

| Control | Verified value | Interpretation |
|---|---:|---|
| Replacement score threshold | 50.0 | Replacement-control input; inclusive/exclusive behavior remains to be tested |
| New-equipment base score | 15.0 | Forecast input |
| Chart mid-score | 32.5 | Presentation input, not automatically a business band |
| Yearly inflation | 3.5% | Forecast cost input |
| Overall cost correction/safety factor | 0.6 | Explicit workbook-derived cost parameter |
| Equipment-size exponent | 0.8 | Size-scaling input |

## Verified score weights

The `Criteria` sheet contains nine reverse-ranked weights:

`100, 88.8888889, 77.7777778, 66.6666667, 55.5555556, 44.4444444, 33.3333333, 22.2222222, 11.1111111`

These map to Criticality, Operating Issues, Redundancy, Service and Support, Age, Site Business Priority, Efficiency, Maintenance Cost, and Loading / Equipment Taxing.

## Lineage evidence

- `Output- Asset Scores` begins with AssetIds 2-5 at output rows 17-20.
- `Scoring Engine` begins with the same AssetIds 2-5 at engine rows 20-23.
- The output layer is therefore consistent with the observed sample row alignment.
- The output layer remains a derived result layer; full-population formula lineage and numeric equality are not yet proven by this artifact.

## Controlled recalculation result

A disposable copy was recalculated and saved through Excel automation. The sample output formulas remained intact and aligned to the expected engine rows:

| Output row | AssetId | Overall formula | Criticality formula | Cached values |
|---:|---:|---|---|---|
| 17 | 2 | `Scoring Engine!CC21` | `Scoring Engine!BR21` | Blank |
| 18 | 3 | `Scoring Engine!CC22` | `Scoring Engine!BR22` | Blank |
| 19 | 4 | `Scoring Engine!CC23` | `Scoring Engine!BR23` | Blank |
| 20 | 5 | `Scoring Engine!CC24` | `Scoring Engine!BR24` | Blank |

The recalculated copy did not expose numeric cached values for these formula cells. This is a validation limitation, not evidence of a score of zero or a formula failure. Numeric equality remains open and requires either an interactive Excel calculation state with visible results or an independently reproducible calculation path.

## Extracted scoring lineage

The first scoring-engine row exposes the following lineage:

- `BR:BZ`: the nine component scores, sourced from the criterion-specific lookup/calculation sheets.
- `CA`: `SUMPRODUCT($BR$19:$BZ$19,BR21:BZ21)`, the weighted component total.
- `CB`: normalized score against the maximum component total, with retired and available assets forced to zero.
- `CC`: normalized overall score, with retired, available, or blank-category assets forced to zero.
- `CD:CL`: binary category flags used by downstream output and site calculations.

The engine depends on `XLOOKUP`, `TEXTSPLIT`, and source-sheet lookup ranges. This explains why formula presence and row alignment can be validated from the package while a portable independent numeric reproduction still requires an Excel-compatible calculation engine or a deliberate reimplementation of those lookup rules.

## Full-population alignment result

The bounded output region was checked against the `Scoring Engine` package formulas:

- 9,065 valid output asset rows were examined.
- All 9,065 rows contained an engine formula reference.
- All 9,065 referenced engine rows contained the same `AssetId` as the output row.
- Alignment mismatches: 0.

This closes the source-to-engine-to-output key-lineage gate. It does not establish numeric equality for component scores or cost outputs because the formula cells do not expose reliable cached numeric values through the available automation path.

## Original cached-value comparison result

An additional package-level comparison found 5,715 output/engine overall-score pairs with values in both cache locations. Of those pairs, 5,653 differed; a representative case had a populated output score of `72.384963757544497` while the referenced engine cache was `0`. The remaining 3,350 bounded pairs lacked one or both cached values.

This original package-level result was superseded for recalculated validation by the controlled Excel result below. It remains evidence that the original stored caches were incomplete or stale.

## Recalculated full-population numeric result

The disposable copy was recalculated through Excel and then compared across the bounded output population:

- 2,013 rows had numeric values for the overall score and all nine components in both output and engine cells.
- All 2,013 fully comparable rows matched within the comparison tolerance.
- Numeric differences: 0.
- 3,351 rows lacked one or more dependent cached values and were excluded from the equality comparison.

This provides partial numeric validation of the score lineage. It supports using the formulas and displayed output as the current PoC result path, while retaining the incomplete-cache population as a documented validation limitation.

## Governance recommendation applied

Use `0.6` as an explicit workbook-derived parameter in the PoC. Keep it separate from the `0.8` size exponent, regional multiplier, and inflation. Record the exact adjustment order when the workbook is recalculated in a controlled copy.

## Resolved threshold and cost formula rules

The extracted `Scoring Engine` formulas establish these rules:

- Replacement threshold is inclusive: `CC >= Costs and Scoring!D62`, with `D62 = 50`.
- Base score for new equipment is read from `Costs and Scoring!D63`, with value `15`.
- Replacement year logic uses the normalized overall score and returns year `1` when the score meets or exceeds the threshold.
- Base replacement cost (`DJ`) is calculated from equipment size, equipment cost/unit, the size exponent, regional multiplier, and the correction factor (`Costs and Scoring!D66`).
- Future-year cost (`DL`) applies inflation from `Costs and Scoring!D65` and rounds to the workbook's `5,000` increment.
- The extracted cost formula references the size exponent through the equipment-cost lookup output (`DG`), while the correction factor is a separate multiplier (`DH`).

The threshold comparison is resolved from workbook formula evidence. Numeric equality for every cost row and the exact adjustment-order behavior still requires representative cost-row comparison.

## Site-risk threshold result

The site-risk output uses `COUNTIF(...,">="&$D$12)` for category exception counts, with `D12 = 7`. The site-risk threshold is therefore inclusive: a component value of exactly `7.0` is counted as an exception. The recalculated output labels the measure consistently as “Number of Items At or Greater than Threshold Above.”

Across the recalculated site-risk output, all 66 valid sites and six category count columns were checked against the underlying numeric category scores:

- Category counts checked: 396.
- Count mismatches: 0.
- Missing count values: 0.

This validates the threshold-count implementation. The mapping from raw normalized SPOF answer states to `Transpose Actual Adj` numeric risk scores remains a separate transformation-lineage task.

## SPOF answer-to-risk transformation evidence

The site-risk output reads numeric question scores from `Transpose Actual Adj`, not directly from `Yes`, `No`, or `N/A` labels in the normalized observation table. A representative recalculated DAL01 trace showed:

| Question | Raw selected answer | Transformed numeric score |
|---|---|---:|
| 1.02 | Yes | 0 |
| 1.03 | No | 6 |
| 1.04 | No | 5 |
| 1.05 | Yes | 0 |
| 1.06 | No | 6 |
| 1.07 | Yes | 0 |
| 1.08 | Yes | 6 |

The same raw answer can produce different numeric scores by question, and different raw answers can produce the same score. Therefore `AnswerValue` must remain a qualitative source field, while question-level risk scoring must be represented as a separate derived field sourced through the workbook's weighting and transformation logic.

## Remaining tests

1. Resolve the 3,351 rows with incomplete dependent values through an independent calculation path or an interactive Excel calculation review.
2. Confirm threshold examples below, equal to, and above `50.0` against recalculated output rows.
3. Compare representative cost rows to validate adjustment order: base cost, size scaling, regional multiplier, inflation, and `0.6` correction.
4. Compare the recalculated result to output values and record unexplained differences.
5. Compare the inclusive `7.0` site-risk threshold counts against normalized SPOF observations after the risk transformation is fully reconciled.

## Representative cost comparison

Five recalculated assets were compared across the output layer and the referenced `Scoring Engine` row:

| AssetId | Output ROM cost | Engine `DJ` | Output budget year | Engine `DK` | Output budget-year cost | Engine `DL` |
|---:|---:|---:|---:|---:|---:|---:|
| 788 | 140,000 | 140,000 | 1 | 1 | 140,000 | 140,000 |
| 564 | 70,000 | 70,000 | 1 | 1 | 70,000 | 70,000 |
| 565 | 70,000 | 70,000 | 1 | 1 | 70,000 | 70,000 |
| 806 | 130,000 | 130,000 | 1 | 1 | 130,000 | 130,000 |
| 807 | 130,000 | 130,000 | 1 | 1 | 130,000 | 130,000 |

All five representative cost rows matched exactly. This validates the output-to-engine cost result mapping for the sample, but does not yet prove the full-population cost adjustment order.

No workbook data was changed by this validation pass.
