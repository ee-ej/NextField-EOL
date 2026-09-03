# Source-to-Model Re-evaluation

Date: 2026-09-02

## Authority

The Excel workbook is the primary data authority for this re-evaluation. The Word documents and architecture image are supporting research and intended-output guidance. The supplied TMDL is treated as a derived proposal, not as verified model truth.

Workbook: `source/Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25.xlsx`
Starter model: `source/FlexEOL_NextField.SemanticModel.tmdl`

## Workbook Inventory

The workbook contains 33 sheets, including entry, scoring, calculation, output, risk, and transpose sheets. Key used ranges observed directly through Excel:

| Sheet | Observed used rows | Observed used columns | Notes |
|---|---:|---:|---|
| Entry- Eq Database | 10,046 | 233 | Header row 21; equipment input and asset attributes |
| Entry- Site Data | 128 | 31 | Header row 20; site attributes and derived scoring inputs |
| Entry- Operating Issues | 1,167 | 11 | Operating-issue inputs |
| Entry- Service and Support | 2,019 | 33 | Service/support inputs |
| Criteria | 45 | 19 | Nine scoring criteria and weights |
| Costs and Scoring | 157 | 16 | Equipment cost assumptions and scaling |
| Output- Asset Scores | 10,553 | 25 | Header row 16; scored asset output |
| Output- Site Scores | 104 | 30 | Site-level output |
| Output- Budget Forecasting | 140 | 116 | Ten-year forecast output area |
| Entry- Site SPOF Data | 148 | 282 | Transposed site-by-column SPOF input matrix |
| Output- Site Risk Scores | 104 | 77 | Site risk summary and SPOF detail output |

## Direct Findings

### 1. Asset input width differs from the starter-model note

The TMDL comment says the asset database has 193 columns. The current workbook used range is 233 columns. The first verified headers include:

`AssetId`, `CategoryName`, `Name`, `AssetNo`, `SerialNo`, `Make`, `Model`, `BarCode`, `RFID`, `SiteId`, `SiteNo`, `SiteName`, `ParentAssetId`, `ParentAssetName`, and additional parent, cost-center, category, location, and attribute fields.

The proposed `Dim_Asset` is therefore only a selected projection, not a complete representation of the source input. That may be appropriate, but the projection must be explicitly approved and documented.

### 2. Asset-score output names do not match the proposed model exactly

The verified Output- Asset Scores headers include:

`Original Order`, `AssetId`, `Name`, `SerialNo`, `Make`, `Model`, `SiteNo`, `SiteName`, `Eq. Category`, `Overall Score`, `Eq. Criticality`, `Eq. Operating Issues`, `Eq. Redundancy`, `Eq. Service & Support`, `Eq. Age`, `Site Business Priority`, `Eq. Efficiency`, `Eq. Main Cost`, `Eq. Loading`, `ROM Replacement Cost ($)`, `Budget Year`, and `ROM Cost ($) in Budget Year`.

The starter TMDL uses normalized names such as `EqCategory`, `OverallScore`, and `ROMCostInBudgetYear`. A deterministic rename and type-mapping specification is required before implementation. The source output also reports 25 used columns, while the visible populated header set is a multi-row/output layout rather than a clean table contract.

### 3. SPOF is structurally transposed

Entry- Site SPOF Data uses site codes as repeated column groups. The observed layout includes a `Site` row, a `SPOF` row, answer choices (`Yes`, `No`, `N/A`), comments, and question rows. Sites are represented across columns rather than as records.

The future normalized table should be validated against the actual group boundaries and question identifiers. The intended target shape remains approximately:

`[SiteNo]`, `[SPOFQuestion]`, `[Answer]`, `[DetailedComments]`

No transformation has been written yet.

### 4. Scoring weights are confirmed from the workbook

The Criteria sheet describes reverse-ranked normalized weights:

| Criterion | Rank | Weight |
|---|---:|---:|
| Criticality | 1 | 100 |
| Operating Issues | 2 | 89 |
| Redundancy | 3 | 78 |
| Service and Support | 4 | 67 |
| Age | 5 | 56 |
| Site Business Priority | 6 | 44 |
| Efficiency | 7 | 33 |
| Maintenance Cost | 8 | 22 |
| Loading / Equipment Taxing | 9 | 11 |

The TMDL’s dynamic weighted measure references these criteria, but its expression and criterion labels still require validation against the actual normalized source columns and final relationship/filter design.

### 5. Cost exponent is confirmed as 0.8

The Costs and Scoring sheet shows `Exponent Applied for Size Variance = 0.8` across the equipment classes. The proposed scaling rule is:

$Cost_B = Cost_A \\times (Size_B / Size_A)^{0.8}$

The sheet also contains an overall cost correction/safety-factor entry of `0.6`. This is separate from the size-scaling exponent and must not be conflated with it.

### 6. Starter TMDL is not executable as a validated PBIP model

The supplied TMDL is a useful skeleton, but it contains explicit TODOs in its M partitions for header renaming, data typing, and blank filtering. Its workbook file reference is also not yet a governed connection. The model has not been validated through the Power BI Modeling MCP because no semantic model connection currently exists.

## Decisions Required Before Model Creation

1. Confirm the intended source-of-record path: CMMS/EAM now, Dataverse later, or another source.
2. Approve the selected source-to-model projections, especially the reduction from 233 asset columns to the proposed dimension columns.
3. Define the exact normalized SPOF table contract and unpivot rules.
4. Decide whether the 0.6 overall correction factor belongs in the governed model, remains workbook-only, or is exposed as a separate parameter.
5. Define the KPI reconciliation rule for site count versus asset/equipment count.
6. Create or identify the initial semantic model in Fabric workspace `NextField-EOL-Dev` before MCP model validation can run.

## Status

- Local structure: approved and created.
- Source documents: preserved unchanged.
- Direct workbook review: started and material source/model drift identified.
- Starter TMDL copied into implementation area: no.
- Fabric semantic model created: no.
- Remote Fabric writes: none.
