# V1 Report Build Checklist

Date: 2026-09-03
Status: Ready for local report authoring; data refresh and publication gated

## Shared validation requirements

- [x] Use V1 only; V2 remains excluded.
- [x] Use the validated model `NextFieldEOL_V1_LocalPrototype`.
- [x] Use only the 15 Ready measures documented in the validated model export.
- [x] Display KPI grain and validation status in report context.
- [x] Exclude test asset 7057 from governed measures.
- [x] Show restored SLC05 explicitly and do not render missing facts as zero.
- [x] Use inclusive replacement threshold 50.0.
- [x] Use inclusive site-risk threshold 7.0.
- [x] Keep raw SPOF answer states separate from derived risk scores.
- [ ] Provide drill paths from portfolio to site, category/question, and asset evidence.

## Model-layer status

- [x] V1 schema imported and validated offline.
- [x] Eight local Import/M partitions defined.
- [x] Fifteen governed measures validated in the offline model.
- [x] Five active relationships validated.
- [ ] Load the validated definition into Power BI Desktop for populated-data refresh.
- [ ] Run DAX measure validation after connecting to the populated Power BI Desktop model.
- [ ] Validate visuals against populated data.

## Page 1: Portfolio Priority

- [ ] Bind site and asset context cards to the approved count measures.
- [ ] Bind the priority table to `FactAssetScore`.
- [ ] Include `OverallScore`, `ROMReplacementCost`, `SiteNo`, `CategoryName`, and `BudgetYear`.
- [ ] Sort by validated priority logic and document the sort order.
- [ ] Include a validation/confidence indicator.
- [ ] Provide site selection and asset drillthrough.

## Page 2: Site Risk and Resiliency

- [ ] Bind average risk to `Average Site Risk Score`.
- [ ] Bind exception count to `Sites With Risk Threshold Exceptions`.
- [ ] Show category scores and threshold counts from `FactSiteRiskScore`.
- [ ] Show `SPOF Observation Count`.
- [ ] Show answer states `Yes`, `No`, `N/A`, `Blank`, and `MultipleAnswers`.
- [ ] Provide site-to-question evidence drillthrough.
- [ ] Mark SLC05 risk/SPOF values as unavailable rather than zero.

## Page 3: Asset Evidence and Capital

- [ ] Show all nine component score fields.
- [ ] Show overall score and inclusive replacement threshold status.
- [ ] Show ROM replacement cost, budget year, and budget-year cost.
- [ ] Show asset identity and site context.
- [ ] Show source workbook, source sheet, and source row provenance.
- [ ] Show test/incomplete validation status.

## Page 4: Reconciliation and Data Quality

- [ ] Show source site count and modeled site count separately.
- [ ] Show raw asset count and governed asset count separately.
- [ ] Show score coverage and incomplete-value counts.
- [ ] Show SPOF observation status distribution.
- [ ] Show `Validation Exception Count`.
- [ ] Provide exception detail with source provenance.
- [ ] Explain the SLC05 restoration and asset 7057 exclusion.

## Acceptance tests

- [ ] Every visual has an approved table/measure binding.
- [ ] Every KPI has an explicit grain.
- [ ] No governed KPI counts padding, metadata, or test records.
- [ ] Threshold labels state inclusive behavior.
- [ ] Missing values remain distinguishable from zero.
- [ ] Keyboard navigation and contrast are checked.
- [ ] Desktop and reduced-width layouts are checked.
- [ ] Local model data refresh succeeds in a supported connected runtime.
- [ ] Report specification receives approval before publication.

## Current blocker

The offline modeling connection is disconnected/read-only. Its partitions exist but remain `NoData`, so visual authoring can proceed against the contract and schema, while populated-data validation requires a connected Power BI Desktop model or supported runtime.
