# KPI Reconciliation Notes

Date: 2026-09-02
Status: Read-only planning evidence

## Important Correction

A naive scan from the asset header row to the end of the Excel UsedRange incorrectly treats explanatory notes below the asset table as AssetId values. The apparent five IDs missing from the score output were text notes, not equipment records.

The workbook therefore requires explicit table-end rules. A column's UsedRange and nonblank count are not sufficient to define the data population.

## Observed Population Signals

- `Entry- Eq Database` contains 9,065 valid numeric `AssetId` values under the approved typed boundary.
- `Entry- Site Data` contains 66 valid site codes; four tail rows are narrative notes rather than site records.
- `Output- Asset Scores` contains output rows with `AssetId = 0`; these should not automatically count as real assets.
- The output also contains title/header/footer material inside its UsedRange.
- A simple full-range distinct count reported 9,066 scored IDs, but this is not yet a trusted business KPI because output boundary and default-zero rules are unresolved.
- `Output- Site Scores` begins its data table at row 14 after a row 13 header.
- `Output- Site Risk Scores` begins its data table at row 15 after two header rows at 13-14.
- `Entry- Site SPOF Data` begins repeated site groups at row 24, with four columns per inspected site group and question rows beginning at row 29.
- The tail of `Output- Asset Scores` contains generated zero-ID rows through row 10,553, and the site outputs contain zero-valued padded rows near their tails. These rows require an explicit valid-record predicate rather than a UsedRange-based import.
- The SPOF matrix has 66 detected four-column blocks across columns 7-282, matching the 66 valid site codes in the bounded site input. Forty-two scored asset rows reference `SLC05`, which is absent from that bounded site master.

## KPI Definitions to Establish

The future reporting contract should define and display these separately:

| KPI | Candidate definition | Status |
|---|---|---|
| Sites in portfolio | Distinct valid `SiteNo` values from bounded site-data rows | Candidate |
| Assets in source | Distinct valid numeric/nonblank `AssetId` values from bounded equipment rows | Candidate |
| Scored assets | Distinct valid nonzero `AssetId` values from bounded asset-score rows | Candidate |
| Equipment rows | Bounded source rows, including or excluding duplicates by explicit rule | Open |
| Scored rows | Bounded output rows with valid asset/site context | Open |
| SPOF exceptions | Valid normalized SPOF answers meeting the approved risk rule | Open |

## Required Reconciliation Tests

1. Determine the final asset input table boundary before the notes section.
2. Determine the final asset-score data boundary before output notes and footer rows.
3. Count valid numeric/nonzero IDs separately from zero/default and text values.
4. Compare source assets to scored assets after applying the same validity rules.
5. List any true source assets absent from scores.
6. Explain all duplicate asset IDs and multi-site asset rows.
7. Reconcile site numbers separately from site names; site names are not unique in the observed source.
8. Publish the KPI definitions with the report so business users can see what each count means.

## Verified Formula Inputs

The workbook's control sheets confirm:

- Replacement score threshold: `50.0`.
- Assumed base score for new equipment: `15.0`.
- Mid-score used for chart coloring: `32.5`.
- Yearly inflation: `3.5%`.
- Overall cost correction/safety factor: `0.6`.
- Equipment size exponent: `0.8`.
- Regional cost multipliers keyed by `Site No.`.

These values are source facts, not yet a complete approved formula contract. Reconciliation must establish the order and scope of each adjustment and must test inclusive/exclusive threshold behavior.

## Scoring Engine Dependency

The first valid asset-score rows use formulas that point into `Scoring Engine` rather than calculating scores locally on `Output- Asset Scores`. The output sheet should therefore be treated as a rendered result with an upstream calculation dependency. The next score test must verify source row to scoring-engine row alignment, then compare the engine result to the displayed output.

For the initial sample, engine rows 21-24 contain source AssetIds 2-5, matching the output formulas that reference those same engine rows. This is evidence of row alignment for the sample only, not yet a full-population guarantee.

The sample output cells exposed formulas but no displayed numeric values through the read-only COM inspection. Treat cached score values as unavailable or unverified until the workbook is recalculated in a controlled validation step, or until an equivalent calculation can reproduce the result from source inputs.

## Modeling Consequence

Do not encode the headline counts directly from UsedRange row counts or unrestricted `DISTINCTCOUNT`. The implementation must first establish bounded, typed, valid-row source tables and then define measures over those tables.

No workbook data was changed by this analysis.
