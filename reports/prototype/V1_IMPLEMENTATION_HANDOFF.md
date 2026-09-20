# V1 Implementation Handoff

Date: 2026-09-03
Status: Ready for local prototype implementation; publication gated

## Completed and validated

- V1 workbook selected as the active source; V2 parked and excluded.
- Source row boundaries and typed validity rules established.
- SLC05 restored in the derived site dimension from 41 asset records.
- Test asset 7057 identified and flagged for exclusion from governed measures.
- Asset-to-engine-to-output key alignment passed for 9,065 assets with zero mismatches.
- Numeric score comparison passed for 2,013 complete rows with zero differences.
- Site-risk threshold counts passed for 396 category counts with zero mismatches.
- Replacement threshold confirmed inclusive at 50.0.
- Site-risk threshold confirmed inclusive at 7.0.
- Representative cost outputs matched the engine for five assets.
- SPOF normalization produced 62 questions and 4,092 observations.
- Offline Power BI model schema imported successfully.
- Offline Power BI model contains 8 tables, 5 relationships, and 15 Ready measures.
- V1 report design brief created with four local prototype pages.
- Prototype composite-key validation passed: 4,092 SPOF observations have no null or duplicate `SiteNo` + `SPOFQuestionId` keys, and validation-exception keys are unique.
- Offline model metadata validation passed: 8 Import tables, 8 partitions, 5 active relationships, and 13 Ready measures; `DimSite.Ownership` is present and the site relationships resolve.
- End-to-end handoff validation passed: generated V1 tables, referential integrity, 8-table schema contract, and 15 exported measures are aligned.
- Exported TMDL folder loaded successfully as a local model with 8 tables, 15 measures, and 5 relationships; refresh remains unavailable because folder connections are disconnected/read-only.
- A live Power BI Desktop instance was detected at `localhost:49788`, but its untitled model currently has 0 tables and is unprocessed; it is not yet the V1 report runtime.
- DAX query validation is unsupported on offline connections; measure execution requires the V1 model to be loaded into a connected Power BI Desktop runtime.
- A direct Desktop DAX validation returned `DAX Evaluate queries work only on databases which have at least one table`, confirming the current Desktop model is empty rather than a V1 runtime.

## Local implementation package

- `semantic-model/V1_MODEL_SCHEMA.json`
- `semantic-model/V1_MODEL_TMDL_DRAFT.tmdl`
- `semantic-model/V1_TMDL_VALIDATED/`
- `reports/prototype/dim_site.csv`
- `reports/prototype/dim_asset.csv`
- `reports/prototype/fact_asset_score.csv`
- `reports/prototype/fact_site_risk_score.csv`
- `reports/prototype/dim_spof_question.csv`
- `reports/prototype/fact_spof_observation.csv`
- `reports/prototype/dim_model_control.csv`
- `reports/prototype/fact_validation_exception.csv`

## Remaining technical work

1. Resolve the 3,351 asset rows with incomplete dependent score values.
2. Complete SLC05 site-level attributes and SPOF treatment with SME input.
3. Validate full-population cost adjustment order beyond the five-row sample.
4. Reconcile raw SPOF answers to question-specific numeric risk scores.
5. Add populated data partitions to a connected Power BI Desktop model or supported runtime.
6. Validate report visuals against the four-page design brief.

## Next environment action

Open/import `semantic-model/V1_TMDL_VALIDATED/` into Power BI Desktop, or create a PBIP/PBIX from that validated definition. Then reconnect the modeling tool to the populated Desktop instance and run a full refresh before visual validation.

## Publication gates

Fabric publication and remote writes remain blocked until the remaining technical work is reviewed, the report specification is locked, and the target workspace and publication action are explicitly confirmed.

## Reproduction commands

```powershell
py -3 projects\build_v1_prototype_tables.py
py -3 projects\validate_v1_prototype.py
```

The source workbook under `source/` must remain unchanged.
