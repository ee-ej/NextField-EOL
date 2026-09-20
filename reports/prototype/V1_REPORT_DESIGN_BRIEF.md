# NextField EOL V1 Report Design Brief

Date: 2026-09-03
Status: Local prototype design; not approved for publication

## Primary question

The first-use experience answers: **Which sites and assets require investment first?**

The prototype uses validated workbook-derived scores and costs. Invest, Validate, Sequence, and Monitor remain deferred until their business mapping is approved.

## Page 1: Portfolio Priority

**Audience:** C-suite, VP, Director

**Purpose:** Rank the portfolio using validated replacement scores, site risk, and capital exposure.

**Core elements:**

- Modeled Site Count
- Source Site Count
- Governed Asset Count
- Scored Asset Count
- Assets At Or Above Replacement Threshold
- ROM Replacement Cost
- Ranked asset table using `OverallScore`, `ROMReplacementCost`, `SiteNo`, `CategoryName`, and `BudgetYear`
- Visible validation/confidence indicator
- Explicit distinction between source sites and restored SLC05

**Interaction:** Selecting a site filters the asset and risk views. Selecting an asset opens evidence detail.

## Page 2: Site Risk and Resiliency

**Audience:** VP, Director, Operations

**Purpose:** Show where risk is concentrated and which transformed question scores drive the result.

**Core elements:**

- Average Site Risk Score
- Sites With Risk Threshold Exceptions
- Site-risk category scores and threshold counts
- Normalized SPOF observations by site and question
- Answer state: `Yes`, `No`, `N/A`, `Blank`, or `MultipleAnswers`
- Clear threshold label: inclusive at `7.0`
- SLC05 shown as restored with missing site-risk/SPOF evidence, not zero risk

**Interaction:** Site -> category -> SPOF question and source evidence.

## Page 3: Asset Evidence and Capital

**Audience:** Director, Operations, Analysts

**Purpose:** Explain an asset’s replacement priority and projected cost.

**Core elements:**

- Asset identity, site, category, make, model, and serial number
- Overall score and nine component scores
- ROM replacement cost
- Budget year and budget-year cost
- Replacement threshold indicator, inclusive at `50.0`
- Calculation layer and source row provenance
- Test-record and incomplete-value status

**Interaction:** Asset selection provides source and score lineage context.

## Page 4: Reconciliation and Data Quality

**Audience:** Analysts and governance stakeholders

**Purpose:** Make the source contract and known exceptions inspectable.

**Core elements:**

- Source sites: 66
- Modeled sites: 67 including restored SLC05
- Raw assets: 9,065
- Provisional governed assets: 9,064 excluding test asset 7057
- Scored assets: 9,065 raw derived rows
- Complete numeric score comparisons: 2,013
- Incomplete score rows: 3,351
- SPOF observations: 4,092
- Multiple-answer observations: 4
- Blank observations: 331
- Validation exceptions: 43
- Source workbook, sheet, row, and column provenance

## Semantic bindings

| Visual need | Table/measure |
|---|---|
| Portfolio site scope | `DimSite` measures |
| Governed asset scope | `Governed Asset Count` |
| Replacement priority | `FactAssetScore[OverallScore]`, `Assets At Or Above Replacement Threshold` |
| Capital exposure | `ROM Replacement Cost` and cost columns |
| Site risk | `Average Site Risk Score`, `Sites With Risk Threshold Exceptions`, `FactSiteRiskScore` |
| SPOF evidence | `FactSPOFObservation`, `SPOF Observation Count` |
| Data quality | `Validation Exception Count`, `FactValidationException` |

## Design rules

- Use text labels alongside color for risk and threshold meaning.
- Never display blank or unavailable SLC05 facts as zero.
- Do not count test asset 7057 in governed measures.
- Keep raw SPOF answers separate from numeric transformed risk scores.
- Show data freshness and validation status in context.
- Preserve drill paths from portfolio -> site -> category/question -> asset.
- Do not implement the four candidate decision states until SME rules are approved.
- Keep report authoring local until the semantic model and report specification are explicitly approved for publication.

## Prototype acceptance criteria

- Every visual binds to an approved table or measure.
- Every KPI has a documented grain.
- Threshold labels state inclusive behavior.
- Exceptions are visible and traceable.
- SLC05 restoration is explicit.
- No visual relies on unvalidated V2 data or calculations.
