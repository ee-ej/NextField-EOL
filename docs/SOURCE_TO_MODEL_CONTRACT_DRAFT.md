# Source-to-Model Contract Draft

Date: 2026-09-03
Project: NextField EOL PoC
Status: Approved source-to-model contract baseline; implementation validations remain

## Purpose

This document defines the approved source-to-model contract baseline for the workbook-backed PoC. It converts validated workbook evidence into a normalized model design and a set of row-boundary and column metadata rules.

This is an approved source contract, not an approved semantic model. It removes source and boundary ambiguity before local PBIP/TMDL implementation and makes explicit what is known, what is inferred, and what remains to be validated.

## Authority and validation basis

The current contract is based on direct workbook inspection of the following source sheets:

- `Entry- Eq Database`
- `Entry- Site Data`
- `Entry- Site SPOF Data`
- `Output- Asset Scores`
- `Output- Site Scores`
- `Output- Site Risk Scores`
- `Scoring Engine`

Direct evidence from the workbook confirms the following:

- Each source sheet contains narrative, instruction, and header metadata above the actual table area.
- The output sheets contain rendering layers, not clean source tables.
- The SPOF data is a transposed matrix keyed by repeated site blocks rather than a normalized record table.
- The true business row boundary must be defined by explicit valid-row rules, not by full UsedRange or nonblank counts alone.

## Governing boundary rules

### 1. General rule: ignore workbook prose and non-data rows

The following classes of rows are excluded from the normalized contract unless a specific business rule says otherwise:

- text and overview paragraphs
- LAST UPDATED rows
- OVERVIEW rows
- instructions and directions
- title rows such as `SITE DATA`, `Output Table`, `SITE SUMMARY TABLE`, `SCORING ENGINE`
- header rows that are not part of the actual table schema
- generated zero-value rows at the tail of output tables
- footer rows and notes below the true dataset

### 2. Valid-row rule for source entry tables

A row is considered a valid source row only if it meets all of the following conditions:

- it appears after the sheet’s actual table header row
- it contains one or more valid business keys (e.g., `AssetId`, `Site No.`)
- it is not a narrative or instruction row
- it is not a sheet footer or generated row
- it passes the specific table’s null/blank and type checks

### 3. Valid-row rule for summary output tables

A row in an output table is considered valid only if it meets these conditions:

- it is in the bounded table region after the header row
- it contains a valid business key
- it is not a zero-filled generated row
- it is not a title or filler row
- it is not a notes or summary explanatory row outside the actual data region

## Candidate tables and authoritative boundaries

### A. DimSite

#### Source
- `Entry- Site Data`

#### Boundary rule
- Ignore all rows before the first true site-data header row.
- Treat the actual site table as beginning just below the instructions and title/header area.
- The first valid row is the first row where the record contains a real site identifier in the site key column, such as `Site No.` or a normalized equivalent.
- Ignore all rows below the last valid site record. This must be confirmed via a bounded scan of the table after the header row.

#### Candidate key
- `SiteNo`

#### Candidate metadata
| Column | Candidate source name | Type | Rule |
|---|---|---|---|
| SiteNo | `Site No.` or site key column in the source table | Text | Primary key; normalize to standard site identifier format |
| SiteName | `Site Name` or equivalent | Text | Descriptive attribute; not the key |
| SiteRegion | region/location fields in source table | Text | Use if present and valid |
| SiteStatus | status/inactive/test flags if present | Text | Keep separate to avoid mixing valid portfolio rows with test rows |
| SourceRowNumber | workbook row number | Integer | Preserve traceability |
| SourceSheet | `Entry- Site Data` | Text | Table provenance |

#### Validation note
- `SiteName` should not be treated as the key because the workbook evidence already shows repeated or non-unique naming patterns.
- “70 sites” is the working benchmark, but the final site count must be based on the bounded valid-site table and not on sheet UsedRange length.

### B. DimAsset

#### Source
- `Entry- Eq Database`

#### Boundary rule
- Ignore instruction and overview rows above the actual table header.
- The true asset table begins at the first valid row that contains a numeric or typed `AssetId` field and usable equipment metadata.
- Ignore any rows below the last valid asset record, including notes, footer text, and generated zero-valued rows.
- Asset rows are valid only when the asset key is a nonblank, nonzero, nontext asset identifier that matches the expected equipment population.

#### Candidate key
- `AssetId`

#### Candidate metadata
| Column | Candidate source name | Type | Rule |
|---|---|---|---|
| AssetId | `AssetId` | Integer | Primary key for asset dimension |
| AssetName | `Name` | Text | Human-readable asset name |
| SerialNo | `SerialNo` | Text | Preserve as source attribute |
| Make | `Make` | Text | Source attribute |
| Model | `Model` | Text | Source attribute |
| SiteNo | `SiteNo` or source site key | Text | Foreign key to DimSite |
| SiteName | `SiteName` | Text | Descriptive only |
| EqCategory | category fields and equipment category column | Text | Normalize category values using workbook taxonomy |
| AssetStatus | active/inactive/test flags if present | Text | Separate valid portfolio vs test/placeholder rows |
| SourceRowNumber | workbook row number | Integer | Preserve traceability |
| SourceSheet | `Entry- Eq Database` | Text | Table provenance |

#### Validation note
- Direct workbook inspection confirms 9,070 nonblank distinct `AssetId` values in the entry sheet, which is the best current source-of-record asset count.
- The asset score output includes generated zero-value rows and repeated rows; these are not trusted as source records and should be treated as output artifacts.

### C. FactAssetScore

#### Source
- `Output- Asset Scores`
- Upstream dependency: `Scoring Engine`

#### Boundary rule
- Define the table as the bounded asset-score output region after the output header rows.
- Ignore the title text, overview text, score-weighting rows, and any footer/notes rows beneath the table.
- Rows in the output table are valid only when:
  - `AssetId` is present and nonblank
  - `Overall Score` or equivalent score column is populated or derivable
  - the row is not a zero-filled generated row
  - the row is not a title/filler row
- `Original Order` may be retained only if it provides a source-order column that must be preserved for traceability; otherwise it is treated as a workbook-order attribute, not a semantic key.

#### Candidate key
- `AssetId`
- Optional surrogate `AssetScoreRowId` for traceability if multiple rows per asset are allowed

#### Candidate metadata
| Column | Candidate source name | Type | Rule |
|---|---|---|---|
| AssetId | `AssetId` | Integer | Source business key |
| SiteNo | `SiteNo` | Text | Site relationship |
| SiteName | `SiteName` | Text | Descriptive attribute |
| EqCategory | `Eq. Category` | Text | Source category field |
| OverallScore | `Overall Score` | Decimal | Output measure |
| EqCriticality | `Eq. Criticality` | Decimal | Score component |
| EqOperatingIssues | `Eq. Operating Issues` | Decimal | Score component |
| EqRedundancy | `Eq. Redundancy` | Decimal | Score component |
| EqServiceSupport | `Eq. Service & Support` | Decimal | Score component |
| EqAge | `Eq. Age` | Decimal | Score component |
| SiteBusinessPriority | `Site Business Priority` | Decimal | Score component |
| EqEfficiency | `Eq. Efficiency` | Decimal | Score component |
| EqMainCost | `Eq. Main Cost` | Decimal | Score component |
| EqLoading | `Eq. Loading` | Decimal | Score component |
| ROMReplacementCost | `ROM Replacement Cost ($)` | Decimal | Cost output |
| BudgetYear | `Budget Year` | Integer | Year dimension |
| ROMCostInBudgetYear | `ROM Cost ($) in Budget Year` | Decimal | Forecast value |
| SourceRowNumber | workbook row number | Integer | Traceability |
| SourceSheet | `Output- Asset Scores` | Text | Provenance |
| ScoreEngineRowRef | upstream `Scoring Engine` row reference if available | Text | Optional lineage field |

#### Validation note
- This output is a rendered result layer and must not be treated as the source-of-truth table without confirming how it maps back to `Scoring Engine` and source asset rows.
- The row-level alignment from source `AssetId` to `Scoring Engine` row numbers must be validated across the full bounded population before this fact table is treated as final.

### D. DimSPOFQuestion

#### Source
- `Entry- Site SPOF Data`

#### Boundary rule
- The source is a transposed site matrix with repeated site groups and question rows.
- The true question entities are defined by the row labels in the question section, beginning below the repeating site groups.
- Preserve source question text and source question identifiers as a separate dimension.

#### Candidate key
- `SPOFQuestionId`

#### Candidate metadata
| Column | Candidate source name | Type | Rule |
|---|---|---|---|
| SPOFQuestionId | inferred stable question key | Text | Must be derived from the workbook question identifiers or a generated normalized ID |
| SPOFQuestionText | source question text | Text | Preserve exact wording |
| SPOFCategory | category or grouping if present | Text | Optional grouping |
| SourceSheet | `Entry- Site SPOF Data` | Text | Provenance |

#### Validation note
- The workbook layout uses repeated site blocks, not a normalized table.
- The question IDs and answer labels must be normalized before this dimension is relied on in reporting.

### E. FactSPOFObservation

#### Source
- `Entry- Site SPOF Data`

#### Boundary rule
- Site blocks are repeated across columns and question ids are represented by rows.
- The normalized refrigerenced shape is a row per site/question combination.
- One row is valid only if it contains:
  - a valid site identifier
  - a valid question id
  - a valid answer or answer state

#### Candidate key
- composite of `SiteNo` + `SPOFQuestionId`

#### Candidate metadata
| Column | Candidate source name | Type | Rule |
|---|---|---|---|
| SiteNo | site header group | Text | Foreign key to DimSite |
| SPOFQuestionId | inferred or workbook identifier | Text | Foreign key to DimSPOFQuestion |
| AnswerValue | Yes / No / N/A / blank / comment | Text | Normalize to a controlled set |
| AnswerFlag | Boolean/flag or categorical value | Text | Create a normalized answer flag for analytics |
| DetailedComments | comments field in source matrix | Text | Preserve when present |
| SourceColumnGroup | repeated site block location | Text | Preserve original locational traceability |
| SourceSheet | `Entry- Site SPOF Data` | Text | Provenance |

#### Validation note
- `Entry- Site SPOF Data` is currently the table that proves the need for normalization.
- It cannot be imported directly as a clean fact table without a column-unpivot or matrix-to-long-form transformation.

### F. FactSiteRiskScore

#### Source
- `Output- Site Risk Scores`

#### Boundary rule
- Data rows begin after the two header rows and are bounded before the end-of-table filler rows.
- Valid site-risk rows must include a valid `Site No.` and a valid `Overall Score`.
- Rows with zero/default values or non-business filler rows should be excluded.

#### Candidate key
- `SiteNo`

#### Candidate metadata
| Column | Candidate source name | Type | Rule |
|---|---|---|---|
| SiteNo | `Site No.` | Text | Key |
| OverallScore | `Overall Score` | Decimal | Risk metric |
| NumberItemsAtThreshold | threshold-count column | Integer | Supporting metric |
| GeneratorScore | generator-related score field | Decimal | Component |
| SourceQuestionFields | grouped question/score columns | Decimal | Preserve as source field group |
| SourceSheet | `Output- Site Risk Scores` | Text | Provenance |

#### Validation note
- This sheet is a site summary output and should be modeled as a fact table only after its valid row boundary is confirmed.
- It is not a clean source table and its formula lineage to the SPOF and asset scoring logic should be validated before using it as the primary fact source.

### G. FactSiteScoreSummary

#### Source
- `Output- Site Scores`

#### Boundary rule
- Valid rows begin after the summary header rows and before the terminal zero-value/filler rows.
- Each row should represent one site and one summary score by category.

#### Candidate key
- `SiteNo`

#### Candidate metadata
| Column | Candidate source name | Type | Rule |
|---|---|---|---|
| SiteNo | `Site No.` | Text | Key |
| All | `All` | Decimal | Aggregate score |
| EquipmentTypeScores | category-level score columns | Decimal | Optional pivoted category facts |
| SourceSheet | `Output- Site Scores` | Text | Provenance |

#### Validation note
- This table is a summary output and should be used as a reporting fact only once its valid row boundaries and measure semantics are approved.

### H. FactBudgetForecast

#### Source
- `Output- Budget Forecasting`

#### Boundary rule
- Validate the true row and column boundaries before using as a fact table.
- Confirm whether the output is asset-level, site-level, or a time-by-category matrix.

#### Candidate key
- likely composite of `SiteNo` + `Year` + `AssetId` or `Category`

#### Candidate metadata
| Column | Candidate source name | Type | Rule |
|---|---|---|---|
| SiteNo | site key if present | Text | Foreign key |
| AssetId | asset key if present | Integer | Optional asset-level forecast |
| BudgetYear | year dimension | Integer | Time grain |
| ReplacementCost | cost forecast value | Decimal | Output measure |
| SourceSheet | `Output- Budget Forecasting` | Text | Provenance |

#### Validation note
- This table needs explicit validation before it becomes a governed fact table because the workbook output may be matrix-based rather than normalized.

## Normalized source-to-model conceptual model

The normalized target model should look approximately like this:

- `DimSite`
  - `SiteNo` (PK)
  - `SiteName`
  - `SiteRegion`
  - `SourceSheet`

- `DimAsset`
  - `AssetId` (PK)
  - `SiteNo` (FK)
  - `AssetName`
  - `EqCategory`
  - `Make`
  - `Model`
  - `SerialNo`

- `DimSPOFQuestion`
  - `SPOFQuestionId` (PK)
  - `SPOFQuestionText`

- `FactAssetScore`
  - `AssetId` (FK)
  - `SiteNo` (FK)
  - `OverallScore`
  - `EqCriticality`
  - `EqOperatingIssues`
  - `EqRedundancy`
  - `EqServiceSupport`
  - `EqAge`
  - `BudgetYear`
  - `ROMReplacementCost`
  - `ScoreEngineRowRef`

- `FactSPOFObservation`
  - `SiteNo` (FK)
  - `SPOFQuestionId` (FK)
  - `AnswerValue`
  - `AnswerFlag`
  - `DetailedComments`

- `FactSiteRiskScore`
  - `SiteNo` (FK)
  - `OverallScore`
  - `ThresholdCount`

- `FactSiteScoreSummary`
  - `SiteNo` (FK)
  - `AllScore`
  - `CategoryScores`

- `FactBudgetForecast`
  - `SiteNo` or `AssetId` (FK)
  - `BudgetYear`
  - `ReplacementCost`

## Column-level metadata standard

Each model column should carry the following metadata when created:

- `SourceSheet`
- `SourceColumnName`
- `ColumnRole` (key, descriptive, measure, dimension, derived)
- `DataType`
- `Nullable`
- `BusinessMeaning`
- `TransformationRule`
- `ValidityRule`
- `TraceabilityNote`

## Example: source metadata pattern

| Target Column | Source Sheet | Source Column | Type | Transformation |
|---|---|---|---|---|
| SiteNo | `Entry- Site Data` | `Site No.` | Text | Trim and standardize site identifiers |
| AssetId | `Entry- Eq Database` | `AssetId` | Integer | Convert to integer; reject blanks and nonnumeric values |
| OverallScore | `Output- Asset Scores` | `Overall Score` | Decimal | Cast to decimal; exclude zero-generated rows |
| AnswerValue | `Entry- Site SPOF Data` | matrix answer area | Text | Normalize `Yes`, `No`, `N/A`, and blank states |
| SourceSheet | all | workbook metadata | Text | Set to the source table name |

## Approved contract assumptions for this draft

The following assumptions are treated as current working rules for the draft contract:

- The workbook remains the authoritative source of record for this PoC.
- `SiteNo` is the designated site key; `SiteName` is descriptive, not the business key.
- `AssetId` is the designated asset key; any output rows with zero or blank IDs are not valid asset records.
- SPOF must be normalized into a long-form fact table before useful analysis is possible.
- Output tables are treated as rendered/layered outputs, not clean source tables, until validated.
- Summary and output sheets may remain in the model as reporting facts only after their valid-row boundaries and measure logic are confirmed.

## Open validation items before approval

The following items remain open and must be resolved prior to final semantic-model sign-off:

1. Exact row start/end boundaries for every source table.
2. Exact field names and column order for the full asset input table.
3. The exact first valid row for each output table.
4. The full site-to-SPOF block mapping for the repeated matrix.
5. The valid-record predicate for zero/default generated rows.
6. The approved granular definitions for site count, asset count, scored-row count, and equipment-row count.
7. The model-level governance of the 0.6 cost multiplier and any other workbook-only adjustment factors.

## Status

This document is a draft source-to-model contract based on direct workbook validation and the best currently available evidence. It should be treated as the working baseline for model design, but not as final implementation truth until the open validation items above are approved.
