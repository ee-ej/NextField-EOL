# Capital Forecast Profile

Date: 2026-09-03
Status: Read-only workbook evidence; draft contract support

## Source

Workbook: `source/Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25.xlsx`

Sheet: `Output- Budget Forecasting`

## Verified Layout

| Region | Rows | Interpretation |
|---|---:|---|
| Title, explanation, threshold, equipment controls, N+1 settings | 1-46 | Configuration and presentation content; not capital fact rows |
| Aggregate row | 48 | `All (Included Only)` portfolio aggregate |
| Forecast header | 47 | `Site No.`, `Include`, `Year 1` through `Year 10`, `Sum Total`, and capacity/cost context |
| Site forecast candidates | 49-114 | Site-level forecast rows; rows 112-114 are explicitly marked `No` |
| Generated padding | 115-139 | Zero-valued generated rows; exclude |
| Chart/presentation content | 140 onward | Not part of the normalized forecast fact |

Rows 49-111 are the currently included candidate site rows in the visible table. This is a forecast coverage observation, not a claim that all 70 source sites are represented in the budget output.

## Source Grain

The visible budget source is one row per site with ten forecast-year columns. It is not an AssetId-level table. The defensible normalized fact grain is:

`SiteNo + ForecastYear + BudgetAmount + IncludeStatus`

The Year 1-Year 10 columns should be unpivoted. `Sum Total` is a derived or supplied check value and must not be double-counted with the unpivoted year amounts.

Asset-level capital attribution is not directly available from this table. Any allocation from site-level budget to assets requires a separately approved rule and must not be inferred from the table shape.

## Valid-Record Predicate

A budget fact row is eligible only when:

- the row is within the forecast table boundary;
- `Site No.` is a nonblank, nonzero site key;
- `Include` is `Yes` for included exposure measures;
- the forecast year is one of Year 1 through Year 10;
- the budget value is numeric and not a generated padding value.

The `All (Included Only)` row is an aggregate presentation row. It should be retained only as a reconciliation check, not loaded as another site fact.

## Controls To Preserve Separately

- Replacement threshold: 50.0.
- Size exponent: 0.8.
- Yearly inflation: 3.5%.
- Regional multiplier.
- Overall correction/safety factor: 0.6.

The adjustment order, missing-size treatment, forecast-year interpretation, and relationship between the site budget and asset replacement outputs remain open pending formula reconciliation.

## Reconciliation Questions

1. Which of the 70 source sites are absent from the site budget table, and is that absence intentional?
2. Does `Include = No` mean excluded from all exposure measures or only from the configurable chart?
3. Is `Sum Total` exactly the sum of Year 1 through Year 10 for every included site?
4. Is there an approved method to attribute site-level budget to assets or categories?
5. Are Year 1 through Year 10 relative planning years or calendar/fiscal years?
