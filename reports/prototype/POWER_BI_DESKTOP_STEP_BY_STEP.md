# Power BI Desktop V1 Step-by-Step Guide

Date: 2026-09-03
Status: Local execution guide; publication gated

## Objective

Load the validated V1 prototype into Power BI Desktop, refresh the generated CSV tables, validate the model, and build the first local report pages.

## 1. Create the local report

1. Open Power BI Desktop.
2. Select **File > New**.
3. Save the report outside the `source` folder, for example:
   - `NextField_EOL_V1_Local.pbix`

## 2. Load the eight CSV tables

Use **Home > Get data > Text/CSV** for each file:

- `reports/prototype/dim_site.csv`
- `reports/prototype/dim_asset.csv`
- `reports/prototype/fact_asset_score.csv`
- `reports/prototype/fact_site_risk_score.csv`
- `reports/prototype/dim_spof_question.csv`
- `reports/prototype/fact_spof_observation.csv`
- `reports/prototype/dim_model_control.csv`
- `reports/prototype/fact_validation_exception.csv`

Promote the first row as headers and rename the queries to:

- `DimSite`
- `DimAsset`
- `FactAssetScore`
- `FactSiteRiskScore`
- `DimSPOFQuestion`
- `FactSPOFObservation`
- `DimModelControl`
- `FactValidationException`

## 3. Set data types

Confirm these types before selecting **Close & Apply**:

- `AssetId`, `SiteNo`, and `SPOFQuestionId`: Text
- Score, cost, risk, and EBITDA fields: Decimal number
- `BudgetYear`, source row numbers, and source column numbers: Whole number
- Validation and test/restoration flags: Text or Boolean, consistently across the model

## 4. Create relationships

In **Model view**, create single-direction relationships:

- `DimSite[SiteNo]` -> `DimAsset[SiteNo]`
- `DimSite[SiteNo]` -> `FactAssetScore[SiteNo]`
- `DimSite[SiteNo]` -> `FactSiteRiskScore[SiteNo]`
- `DimSite[SiteNo]` -> `FactSPOFObservation[SiteNo]`
- `DimAsset[AssetId]` -> `FactAssetScore[AssetId]`
- `DimSPOFQuestion[SPOFQuestionId]` -> `FactSPOFObservation[SPOFQuestionId]`

## 5. Add measures

Use the measure definitions under `semantic-model/V1_TMDL_VALIDATED/tables/` or create the 15 measures in the validated offline model:

- Modeled Site Count
- Source Site Count
- Governed Asset Count
- Scored Asset Count
- Assets At Or Above Replacement Threshold
- ROM Replacement Cost
- Average Site Risk Score
- Sites With Risk Threshold Exceptions
- SPOF Observation Count
- Valid SPOF Observation Count
- Blank SPOF Observation Count
- Multiple Answer SPOF Count
- Scored Asset Coverage
- SPOF Answer Completeness
- Validation Exception Count

## 6. Refresh and verify counts

After **Close & Apply**, refresh the model and verify:

- 67 modeled sites
- 66 source sites
- 9,065 raw assets
- 9,064 governed assets after excluding test asset `7057`
- 9,065 scored asset rows before test exclusion
- 66 site-risk rows
- 4,092 SPOF observations
- 3,757 valid SPOF observations
- 331 blank SPOF observations
- 4 multiple-answer SPOF observations
- 43 validation exceptions

## 7. Verify data rules

- `SLC05` exists as `Salt Lake City-Cottonwood` with `IsRestoredRecord = true`.
- SLC05 site-risk and SPOF facts remain blank where unavailable, not zero.
- Asset `7057` is flagged as a test record and excluded from governed measures.
- Blank and `N/A` SPOF answers remain distinct.
- Replacement threshold logic is inclusive at `50.0`.
- Site-risk threshold logic is inclusive at `7.0`.
- No governed KPI counts metadata, narrative rows, padding, or test records.

## 8. Run DAX validation

Run the queries in [V1_DAX_VALIDATION_QUERIES.md](V1_DAX_VALIDATION_QUERIES.md) against the connected Desktop model.

The queries validate model inventory, SLC05, test exclusion, SPOF quality, and threshold behavior.

## 9. Build the local report pages

Use [V1_REPORT_DESIGN_BRIEF.md](V1_REPORT_DESIGN_BRIEF.md):

1. Portfolio Priority
2. Site Risk and Resiliency
3. Asset Evidence and Capital
4. Reconciliation and Data Quality

Use [V1_REPORT_BUILD_CHECKLIST.md](V1_REPORT_BUILD_CHECKLIST.md) for visual bindings, drill paths, accessibility, and acceptance tests.

## 10. Reproduce the source tables

From the repository root:

```powershell
py -3 projects\build_v1_prototype_tables.py
py -3 projects\validate_v1_prototype.py
```

These commands regenerate the local CSV tables and verify their keys and relationships without modifying the source workbook.

## Current environment note

The modeling tool can validate the offline TMDL schema and measures, but offline connections cannot execute DAX or refresh data. A connected Power BI Desktop model is required for populated-data validation.

## Publication guardrail

Do not publish to Fabric or perform remote writes until:

- Desktop refresh succeeds.
- DAX validation queries pass.
- Report visuals and drill paths pass the build checklist.
- Remaining score, SLC05, SPOF, and cost exceptions are reviewed.
- The target workspace and publication action are explicitly approved.
