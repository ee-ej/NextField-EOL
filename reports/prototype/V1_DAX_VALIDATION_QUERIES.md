# V1 DAX Validation Queries

Date: 2026-09-03
Status: Ready for execution after Power BI Desktop load

Run these queries against the connected `NextFieldEOL_V1_LocalPrototype` model after the validated V1 definition is loaded and refreshed in Power BI Desktop.

## Model inventory

```DAX
EVALUATE
ROW(
    "ModeledSites", [Modeled Site Count],
    "SourceSites", [Source Site Count],
    "GovernedAssets", [Governed Asset Count],
    "ScoredAssets", [Scored Asset Count],
    "ThresholdAssets", [Assets At Or Above Replacement Threshold],
    "ROMCost", [ROM Replacement Cost],
    "SiteRiskExceptions", [Sites With Risk Threshold Exceptions],
    "SPOFObservations", [SPOF Observation Count],
    "ValidSPOFObservations", [Valid SPOF Observation Count],
    "BlankSPOFObservations", [Blank SPOF Observation Count],
    "MultipleAnswerSPOF", [Multiple Answer SPOF Count],
    "ValidationExceptions", [Validation Exception Count]
)
```

Expected structural results are 67 modeled sites, 66 source sites, 9,064 governed assets, 9,065 raw scored assets before test exclusion, 4,092 SPOF observations, and 43 validation exceptions. Score and cost totals depend on the populated runtime values.

## SLC05 restoration

```DAX
EVALUATE
FILTER(
    SELECTCOLUMNS(
        DimSite,
        "SiteNo", DimSite[SiteNo],
        "SiteName", DimSite[SiteName],
        "ValidationStatus", DimSite[ValidationStatus],
        "IsRestoredRecord", DimSite[IsRestoredRecord]
    ),
    [SiteNo] = "SLC05"
)
```

Expected result: one row with `Salt Lake City-Cottonwood`, `RestoredFromAssetEvidence`, and `IsRestoredRecord = true`.

## Test asset exclusion

```DAX
EVALUATE
FILTER(
    SELECTCOLUMNS(
        DimAsset,
        "AssetId", DimAsset[AssetId],
        "SiteNo", DimAsset[SiteNo],
        "IsTestRecord", DimAsset[IsTestRecord]
    ),
    [AssetId] = "7057"
)
```

Expected result: one row flagged as a test record and excluded by governed asset measures.

## SPOF quality breakdown

```DAX
EVALUATE
SUMMARIZECOLUMNS(
    FactSPOFObservation[ValidationStatus],
    "ObservationCount", [SPOF Observation Count]
)
```

Expected statuses: `Valid`, `Blank`, and `MultipleAnswers`. Expected counts are 3,757 valid, 331 blank, and 4 multiple-answer observations.

## Threshold spot check

```DAX
EVALUATE
FILTER(
    SELECTCOLUMNS(
        FactAssetScore,
        "AssetId", FactAssetScore[AssetId],
        "OverallScore", FactAssetScore[OverallScore]
    ),
    [OverallScore] >= 50
)
```

The replacement threshold is inclusive at `50.0`. Site-risk category counts use the inclusive `7.0` threshold in the workbook-derived output.

## Execution note

These queries cannot run against offline or empty connections. They require a populated Power BI Desktop or Fabric-connected model. No Fabric publication is authorized by this query pack.
