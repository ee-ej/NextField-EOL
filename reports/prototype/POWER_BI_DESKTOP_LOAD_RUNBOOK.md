# Power BI Desktop V1 Load Runbook

Date: 2026-09-03
Status: Required environment handoff

## Purpose

Load the validated V1 model into Power BI Desktop so populated CSV partitions, DAX measures, and report visuals can be tested in a connected local runtime.

## Inputs

- Validated TMDL folder: `semantic-model/V1_TMDL_VALIDATED/`
- Local prototype CSVs: `reports/prototype/`
- V1 schema contract: `semantic-model/V1_MODEL_SCHEMA.json`
- Report design brief: `reports/prototype/V1_REPORT_DESIGN_BRIEF.md`

## Current Desktop state

A Power BI Desktop instance is available at `localhost:49788`, but its current untitled model is empty and unprocessed. Do not use that empty model for validation until the V1 definition has been loaded.

## Load sequence

1. Open Power BI Desktop.
2. Open or create a local PBIP/PBIX model from the validated V1 definition.
3. Confirm the eight tables are present.
4. Confirm the eight Import/M partitions point to the CSV files under `reports/prototype/`.
5. Refresh the model.
6. Confirm the model reports 67 modeled sites, 9,065 raw assets, 66 site-risk rows, 4,092 SPOF observations, and 43 validation exceptions.
7. Reconnect the modeling tool to the Desktop Analysis Services endpoint shown by the active Desktop instance.
8. Run DAX validation for the 15 measures.
9. Validate the report pages against `V1_REPORT_BUILD_CHECKLIST.md`.

## Expected model inventory

- Tables: 8
- Relationships: 5
- Measures: 15
- Modeled sites: 67, including restored SLC05
- Source-master sites: 66
- Raw assets: 9,065
- Governed assets: 9,064 after excluding test asset 7057
- Site-risk rows: 66
- SPOF observations: 4,092
- Validation exceptions: 43

## Acceptance checks

- `DimSite[SiteNo]` contains SLC05 with `IsRestoredRecord=true`.
- Asset 7057 is flagged as a test record.
- Replacement threshold uses inclusive `>= 50.0`.
- Site-risk threshold uses inclusive `>= 7.0`.
- Blank and `N/A` SPOF answers are not converted to `No`.
- No governed KPI counts metadata, padding, or test records.
- Missing SLC05 site-risk and SPOF facts remain blank, not zero.

## Tooling limitation

The Power BI modeling tool can load and inspect the TMDL folder and can create measures and partitions in an offline model. It cannot refresh disconnected folder models, and it cannot populate the currently empty Desktop model by transferring the offline model automatically. Desktop loading is therefore an environment action.

No Fabric publication or remote write is authorized by this runbook.
