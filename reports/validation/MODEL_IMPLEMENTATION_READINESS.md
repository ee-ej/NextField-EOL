# Model Implementation Readiness

Date: 2026-09-03
Status: Ready for local prototype; not approved for Fabric publication

## Approved inputs

- Workbook source and row-boundary contract are approved.
- Entry source records exclude metadata, narrative rows, footers, placeholders, and test records from governed measures.
- `SLC05` is restored as a derived site using `SiteId` 143, site name `Salt Lake City-Cottonwood`, and 41 supporting asset records.
- Raw bounded source population: 66 site-master records and 9,065 asset records.
- Derived modeled site population: 67 sites after the SLC05 restoration.
- Provisional governed asset population: 9,064 after excluding confirmed test asset `7057`.
- Full source-to-engine-to-output key alignment passed for 9,065 asset identifiers with zero mismatches.
- Recalculated numeric score comparison passed for 2,013 complete rows with zero differences across the overall score and nine components.
- Site-risk threshold counts passed for 396 category counts across 66 source sites with zero mismatches.
- Replacement and site-risk thresholds are inclusive at `50.0` and `7.0` respectively.
- Representative cost outputs matched the engine for five recalculated assets.
- SPOF normalization produced 4,092 observations across 66 source site groups.

## Required model behavior

- Treat entry tables as source facts and score/output sheets as derived result facts.
- Retain `Scoring Engine` and `Transpose Actual Adj` provenance for lineage and reconciliation.
- Keep raw SPOF `AnswerValue` separate from derived numeric risk scores.
- Preserve `Yes`, `No`, `N/A`, and `Blank` distinctly.
- Keep multiple-answer observations and incomplete mappings in a quarantine or validation layer.
- Keep the `0.6` correction factor explicit and workbook-derived until SME policy confirmation.
- Publish site, asset, equipment-row, scored-asset, and scored-row measures separately.

## Open exceptions carried into the prototype

- 41 valid assets reference restored site `SLC05`; site-level attributes and SPOF evidence are not present in the source site/SPOF tables.
- Test asset `7057` must be excluded from governed portfolio measures.
- 3,351 asset score rows lacked one or more dependent cached values during recalculated comparison.
- Full cost adjustment-order validation is not complete beyond the representative sample.
- Four SPOF observations have multiple selected answers; 331 have blank selected answers.
- Exact raw-answer-to-numeric-risk weighting is preserved as transformation logic, not inferred from answer labels.

## Local prototype authorization

The project may now create local, reviewable model and transformation artifacts using the approved contract. The prototype must expose validation status and source provenance rather than silently filling missing values.

## Publication gate

Fabric publication and remote writes remain blocked until:

1. The incomplete score population is classified or independently recalculated.
2. SLC05 site-level attributes and SPOF coverage receive SME treatment.
3. Cost adjustment order is validated beyond the representative sample.
4. The report specification and semantic model names are approved.
5. The target workspace and publication action are explicitly confirmed.
