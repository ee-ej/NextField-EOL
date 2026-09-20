# Source-to-Model Decision Set

Date: 2026-09-03
Project: NextField EOL PoC
Status: Approved source-to-model decision set

## Decision 1: source of record

The workbook remains the source of record for the current PoC.

Rationale:
- It is the only validated workbook available in the current project state.
- Direct inspection confirms that the workbook contains both entry tables and generated output tables.
- The starter TMDL is treated as a proposal, not as governing truth.

## Decision 2: valid data starts only after workbook metadata

The following rows are excluded from the data contract because they are workbook metadata, instructions, or presentation rows:

- title blocks
- overview narrative blocks
- LAST UPDATED rows
- row labels such as OUTPUT TABLE and SITE SUMMARY TABLE
- footers and notes outside the actual data boundary
- generated zero-filled or placeholder rows beyond the valid business population

## Decision 3: authoritative data starts and grains

### Entry- Eq Database
- header row: 21
- first business row: 22
- business grain: one row per asset record
- key: AssetId
- current workbook evidence: 10,046 rows total; business records begin after row 21 and continue through the valid asset population only

### Entry- Site Data
- header row: 20
- first business row: 21
- business grain: one row per site record
- key: Site No.
- current workbook evidence: 128 rows total; valid site records begin at row 21

### Entry- Site SPOF Data
- site block row: 24
- question and answer matrix begins immediately after the site-block header area
- business grain: one row per site + SPOF question
- normalized long-form target: SiteNo + SPOFQuestionId + AnswerValue + DetailedComments
- not importable as-is; it must be unpivoted from a transposed site matrix

### Output- Asset Scores
- visible output header row: 16
- first valid scored asset row: 17
- business grain: one row per scored asset
- key: AssetId
- output is treated as a rendered score layer, not a source record table

### Output- Site Scores
- visible summary header row: 13
- first valid site summary row: 14
- business grain: one row per site summary
- output is treated as a reporting summary, not a source fact table

### Output- Site Risk Scores
- visible summary header row: 13
- first valid risk row: 15
- business grain: one row per site risk record
- output is treated as a derived risk summary layer

## Decision 4: model target shape

The normalized source model should be built around these entities:

### DimSite
- SiteNo
- SiteName
- Ownership
- AssetClass
- supporting site attributes

### DimAsset
- AssetId
- SiteNo
- AssetName
- CategoryName
- Make
- Model
- SerialNo
- supporting asset attributes

### DimSPOFQuestion
- SPOFQuestionId
- SPOFQuestionText
- SPOFCategory

### FactSPOFObservation
- SiteNo
- SPOFQuestionId
- AnswerValue
- AnswerFlag
- DetailedComments

### FactAssetScore
- AssetId
- SiteNo
- OverallScore
- EqCriticality
- EqOperatingIssues
- EqRedundancy
- EqServiceSupport
- EqAge
- SiteBusinessPriority
- EqEfficiency
- EqMainCost
- EqLoading
- ROMReplacementCost
- BudgetYear
- ROMCostInBudgetYear

### FactSiteRiskScore
- SiteNo
- OverallScore
- NumberOfItemsAtThreshold
- category detail scores

## Decision 5: extracted feature set for current model build

For the current PoC, the model should use only the fields that can be directly validated from the workbook and mapped to a stable grain.

Approved minimum feature set:
- Site master data from Entry- Site Data
- Asset master data from Entry- Eq Database
- Asset score output from Output- Asset Scores
- SPOF normalized long-form observations from Entry- Site SPOF Data
- Site risk summary from Output- Site Risk Scores

Not approved yet as a final governed source table:
- the calculation sheet Scoring Engine as a source-of-record table
- the output summary sheets as source-of-truth tables
- any workbook-generated zero rows or filler rows

## Decision 6: implementation validations that remain

The source contract and row-boundary decisions are approved. The following validations remain required before governed measures and publication:

1. Recalculate and document the exact score and cost formula lineage, including the 0.6 factor.
2. Confirm output-to-engine alignment across the full bounded population.
3. Apply the approved KPI definitions to the validated source and derived tables.
4. Execute and reconcile the SPOF transformation, including the apparent missing site block.
5. Confirm the first model slice from the approved 233-column asset projection.

## Approved next action

Proceed with local transformation and reconciliation artifacts using this approved contract. Do not publish to Fabric until the implementation validations above are complete and the target is explicitly confirmed.
