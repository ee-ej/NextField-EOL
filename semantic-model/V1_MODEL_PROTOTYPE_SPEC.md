# NextField EOL V1 Model Prototype Specification

Date: 2026-09-03
Status: Local prototype specification; not approved for Fabric publication

## Objective

Build the smallest local V1-based model that supports portfolio investment prioritization, site risk, asset evidence, capital exposure, and source reconciliation. The prototype must preserve workbook provenance and show unresolved exceptions explicitly.

## Source selection

- Active source: `source/Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25.xlsx`
- V2 source: parked; no V2 fields or calculations enter this prototype.
- Source folder: unchanged.
- Remote writes: prohibited by this specification.

## Prototype tables

| Model table | Source | Grain | Key/status |
|---|---|---|---|
| `DimSite` | `Entry- Site Data` plus approved SLC05 override | One row per modeled site | 67 modeled sites; SLC05 flagged as restored and SME-review required |
| `DimAsset` | `Entry- Eq Database` | One row per valid asset input row | 9,065 raw assets; test asset 7057 excluded from governed measures |
| `FactAssetScore` | `Output- Asset Scores` | One row per scored asset result | Derived output; 9,065 distinct AssetIds; retain engine row reference |
| `DimSPOFQuestion` | `Entry- Site SPOF Data` | One row per question | 62 questions |
| `FactSPOFObservation` | normalized `Entry- Site SPOF Data` | One row per site/question | 4,092 observations; retain answer and provenance status |
| `FactSiteRiskScore` | `Output- Site Risk Scores` | One row per site risk result | 66 source sites; SLC05 has no source result and remains explicitly missing |
| `DimModelControl` | `Criteria`, `Costs and Scoring` | One row per control/version | Include weights, thresholds, exponent, inflation, and 0.6 factor |
| `FactValidationException` | generated validation artifacts | One row per exception | Missing site context, test records, blank/multiple SPOF answers, incomplete score values |

## Relationships

- `DimSite[SiteNo]` -> `DimAsset[SiteNo]`
- `DimSite[SiteNo]` -> `FactAssetScore[SiteNo]`
- `DimSite[SiteNo]` -> `FactSPOFObservation[SiteNo]`
- `DimSite[SiteNo]` -> `FactSiteRiskScore[SiteNo]`
- `DimAsset[AssetId]` -> `FactAssetScore[AssetId]`
- `DimSPOFQuestion[SPOFQuestionId]` -> `FactSPOFObservation[SPOFQuestionId]`

SLC05 is a modeled site override. Its missing site-risk and SPOF facts must remain null, not zero.

## Governed measures

- `Sites in Portfolio`: distinct modeled `DimSite[SiteNo]`, with source and restored counts shown separately.
- `Source Sites`: 66 valid site-master keys.
- `Restored Sites`: 1 (`SLC05`).
- `Assets in Source`: 9,065 raw valid assets.
- `Governed Assets`: 9,064 after excluding test asset 7057.
- `Scored Assets`: distinct valid `FactAssetScore[AssetId]`, with test asset excluded from governed views.
- `Scored Rows`: valid derived score rows with asset and site context.
- `SPOF Observations`: count of normalized observations by status.
- `SPOF Exceptions`: only after an approved risk predicate is applied to derived risk scores; do not count raw `No` or blank answers as exceptions by assumption.
- `Replacement Priority`: use the validated derived `OverallScore`; replacement threshold is inclusive at 50.0.
- `Site Risk Threshold Count`: use derived numeric category scores; threshold is inclusive at 7.0.
- `ROM Replacement Cost`: use derived output cost fields; retain the 0.6 correction factor as a workbook-derived control.

## Required provenance fields

Every fact and exception record should retain, where applicable:

- `SourceWorkbook`
- `SourceSheet`
- `SourceRowNumber`
- `SourceColumnStart`
- `SourceColumnEnd`
- `CalculationLayer`
- `CalculationVersion`
- `ValidationStatus`
- `IsTestRecord`
- `IsRestoredRecord`

## Exclusions and quarantine

- Exclude workbook metadata, instructions, narrative rows, footers, padding, zero IDs, and test asset 7057 from governed measures.
- Keep 41 SLC05 asset records in the model after restoring the site dimension row.
- Keep SLC05 site-level missing data as null and flag it for SME review.
- Keep 4 multiple-answer SPOF observations and 331 blank observations in the validation layer.
- Keep 3,351 incomplete score rows visible in validation status until their dependent values are resolved.
- Do not convert blank or `N/A` SPOF answers to `No`.

## First local prototype views

1. Portfolio Priority: ranked assets/sites using validated score, cost, site risk, and confidence status.
2. Site Risk and Resiliency: site risk categories, inclusive threshold counts, and normalized SPOF evidence.
3. Asset Evidence: nine component scores, replacement cost, budget year, source attributes, and provenance.
4. Reconciliation: source/derived counts, excluded records, missing context, restored SLC05, and validation status.

The Invest/Validate/Sequence/Monitor labels remain deferred until their business mapping is approved.

## Prototype acceptance criteria

- All prototype tables use the approved row-boundary rules.
- Source and derived grains are documented and testable.
- No governed measure counts padding, narrative rows, or test asset 7057.
- SLC05 is visible as a restored site with missing facts clearly indicated.
- Threshold semantics are encoded as inclusive at 50.0 and 7.0.
- Raw SPOF answer values and derived numeric risk scores are separate.
- Every score/cost result has source and calculation provenance.
- Local validation artifacts can be regenerated without modifying the workbook.
- Fabric publication remains disabled until the remaining exceptions and report specification are approved.

## Validated offline model layer

The schema-only V1 model was imported successfully into the Power BI modeling tool and received seven `Ready` measures:

- Modeled Site Count
- Source Site Count
- Governed Asset Count
- Scored Asset Count
- Assets At Or Above Replacement Threshold
- ROM Replacement Cost
- Validation Exception Count

The exported definition is in `semantic-model/V1_TMDL_VALIDATED/`. It validates the local schema and measure layer; populated data partitions remain a separate packaging task.
