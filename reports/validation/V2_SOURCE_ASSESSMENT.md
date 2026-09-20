# V2 Source Workbook Assessment

Date: 2026-09-03
Status: Candidate revision assessed; not approved as implementation source

## Compared workbook

`source/Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25 - Flex Input v2.xlsx`

V1 remains the validated baseline. V2 was analyzed read-only and neither workbook was modified.

## Material V2 findings

| Area | V2 result | Consequence |
|---|---|---|
| Asset input sheet | V1 `Entry- Eq Database` is absent | V2 cannot independently supply the approved asset source population |
| Site input | 63 valid site codes | V2 is a different portfolio snapshot and cannot inherit V1 counts |
| SLC05 | Absent from site input | The V1 SLC05 restoration is not present in V2 |
| SPOF groups | 63 groups; SLC05 absent | V2 SPOF coverage follows its 63-site snapshot, not the restored V1 contract |
| `Entry- Site Data` formulas | 382 `#REF!` cells | Site priority and derived fields are not currently trustworthy |
| `Scoring Engine` formulas | 445,145 `#REF!` cells | V2 score calculations are materially broken or missing dependencies |
| `Scores Actual Adj` | 149 `#REF!` cells | Adjusted score output is not implementation-ready |

## V2 structure

V2 contains these relevant areas:

- `Entry- Site Data`
- `Entry- Operating Issues`
- `Entry- Service and Support`
- `Entry- Refurbishment`
- `Entry- Install Complexity`
- `Scoring Engine`
- `Entry- Site SPOF Data`
- `Scores Actual`
- `Transpose Actual`
- `Site Risk Scores OG`
- `Site EOL Scores for Risk`
- `Scores Actual Adj`
- `Transpose Actual Adj`

The V1 asset database and V1 output-sheet names are not present. V2 therefore represents a structural revision, not merely refreshed input values.

## Interpretation

V2 may contain valuable data and calculation refinements, but it cannot replace V1 as the current implementation source yet. The pervasive `#REF!` values indicate broken or unavailable workbook dependencies, and the missing asset database prevents direct reconciliation to the approved V1 asset contract.

The V2 site and SPOF populations are internally aligned at 63 site codes under the current structural predicate, but that does not establish that V2 covers the V1 66-source-site plus restored-SLC05 modeled population.

## Recommended treatment

1. Preserve V1 as the audit and contract baseline.
2. Treat V2 as a candidate revision branch.
3. Identify the missing V2 asset source or determine whether V2 intentionally delegates assets to another workbook.
4. Repair or restore the dependencies producing `#REF!` before comparing scores.
5. Re-run the same boundary, KPI, SPOF, threshold, and cost tests after V2 formulas are valid.
6. Produce a V1-to-V2 change register before changing the approved model contract.
7. Do not use V2 score outputs or site-priority fields in the local prototype until the `#REF!` defects are resolved.

## Decision

V2 is approved for further read-only refinement analysis only. It is not approved as the implementation source, and no V1 contract decisions are superseded by this assessment.
