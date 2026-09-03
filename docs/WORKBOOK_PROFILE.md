# Workbook Profile

Date: 2026-09-02
Status: Read-only planning evidence

Workbook: `source/Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25.xlsx`

## Key Counts

| Source area | Observed result | Interpretation |
|---|---:|---|
| `Entry- Eq Database` AssetId | 9,070 nonblank and 9,070 distinct | Current equipment/asset input population candidate |
| `Entry- Site Data` Site No. | 70 nonblank and 70 distinct | Candidate portfolio site count |
| `Entry- Site Data` Site Name | 66 nonblank and 39 distinct | Names are not a reliable site key and may represent repeated/variant labels |
| `Output- Asset Scores` AssetId | 10,537 nonblank and 9,066 distinct | Output includes repeated/title/footer or duplicate asset rows; does not directly reconcile to entry population |
| `Output- Asset Scores` SiteNo | 10,406 nonblank and 70 distinct | Site coverage is present, but output row population needs clean-boundary rules |
| `Output- Site Scores` | 104 used rows and 70 distinct values in the inspected site column | Used range includes title/header rows and must be bounded explicitly |
| `Output- Site Risk Scores` | 104 used rows and 67 observed nonblank values in the inspected column | Used range includes title/header rows and requires output-grain investigation |
| `Entry- Site SPOF Data` | 148 used rows and 282 used columns | Transposed matrix with repeated site column groups and multi-row headers |

## Immediate Implications

1. The workbook supports the working statement of 70 sites and approximately 9,070 equipment rows, but the asset-score output does not reconcile directly: it has 9,066 distinct AssetId values and more nonblank rows than distinct IDs.
2. KPI definitions must distinguish entry population, scored population, distinct assets, scored rows, and output rows.
3. `SiteNo` should be the candidate site key. Site names should be descriptive attributes, not keys.
4. Output sheets cannot be modeled by simply importing their full UsedRange. Header/title/footer boundaries must be explicitly defined.
5. The SPOF matrix requires a structural parser or carefully documented transformation because the site identifier is represented in repeated column groups.

## Profiling Observations

- The entry equipment database header is at row 21 and exposes 233 used columns.
- The entry site-data header is at row 20 and exposes 31 used columns.
- The asset-score output header begins around row 16 and exposes 25 used columns.
- `Output- Site Scores` has its header at row 13 and site data beginning at row 14.
- `Output- Site Risk Scores` has a two-level header at rows 13-14 and site data beginning at row 15.
- `Entry- Site SPOF Data` has repeated site-group labels beginning at row 24, field labels at rows 25-28, and question rows beginning at row 29. Each visible site group is represented by a repeated four-column block in the inspected area.
- The inspected SPOF matrix spans columns 7-282 after the left-side question fields. At four columns per site block, that span represents 69 site blocks, which does not yet reconcile to the 70 distinct site numbers in site data.
- `Output- Asset Scores` remains populated through row 10,553 with generated rows whose asset identifier and score values are zero near the tail; these rows are padding/template output and must be excluded from business asset counts.
- The site output sheets also remain populated through original-order rows 90-91 with zero-valued measures, reinforcing that UsedRange length is not the data boundary.
- The workbook includes both visible output sheets and supporting calculation/transpose sheets; these should be treated as evidence until the authoritative input/output contracts are selected.

## Required Follow-up Checks

- Identify exact first/last data rows for every candidate fact table.
- Compare the four assets missing from the scored output with the entry database and determine whether they are intentionally excluded, blank/test rows, or scoring defects.
- Identify the additional nonblank output rows and determine whether they are repeated records, calculation rows, or footer content.
- Profile `SiteNo` consistency across entry and output sheets.
- Map repeated SPOF site groups and normalize answer markers while preserving source locations.
- Reconcile site-name variants and determine whether a canonical name mapping is needed.

## Verified Scoring and Cost Controls

The `Criteria` and `Costs and Scoring` sheets expose these source inputs:

| Control | Workbook value | Interpretation status |
|---|---:|---|
| Replacement score threshold | `50.0` | Verified input; boundary behavior still requires confirmation |
| Assumed base score for new equipment | `15.0` | Verified input; use in forecast logic only after formula reconciliation |
| Mid-score for chart coloring | `32.5` | Verified presentation input; not automatically a business decision band |
| Yearly inflation | `3.5%` | Verified forecast input |
| Overall cost correction/safety factor | `0.6` | Verified multiplier applied to calculated costs |
| Size exponent | `0.8` | Verified equipment-size scaling input |

The cost sheet also contains regional cost multipliers keyed by `Site No.`. Capital exposure therefore requires at least equipment/category, size, forecast year, and site multiplier context. The exact ordering of size scaling, inflation, regional adjustment, and the `0.6` correction factor remains a formula-reconciliation task.

## Asset Score Dependency

The first valid rows in `Output- Asset Scores` map source `AssetId` values 2-5 to site `LAS04`. The displayed score cells are formula references into the `Scoring Engine` sheet, including `Overall Score` references such as `Scoring Engine!CC21` and `Eq. Criticality` references such as `Scoring Engine!BR21`.

The corresponding `Scoring Engine` rows are aligned by source asset row for this sample: engine row 21 contains `AssetId 2`, row 22 contains `AssetId 3`, row 23 contains `AssetId 4`, and row 24 contains `AssetId 5`. This supports a candidate row-level provenance link for the sample, but the alignment must be tested across the full bounded population.

This means `Output- Asset Scores` is a presentation/output layer rather than the scoring calculation authority. Score reconciliation must inspect the `Scoring Engine` row alignment, engine-specific fields, and source lookups before treating output columns as governed facts. A deeper component-column mapping remains open because the latest COM probe was interrupted before returning complete headers.

The same sample inspection exposed formulas in the output score cells but blank displayed values through the read-only COM path. Numeric score reconciliation therefore requires a recalculated workbook state or an independently reproducible calculation path; formula presence alone is not evidence that the cached result is available or current.

No workbook data was changed by this profiling pass.
