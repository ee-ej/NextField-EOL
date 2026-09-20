# Workbook Validation Execution Findings

Date: 2026-09-03
Status: Initial artifact run under the approved source contract; SLC05 restored in derived artifacts

## Scope

The artifacts in this folder were generated from the authoritative workbook using read-only targeted XLSX XML parsing. The source workbook was not modified.

## KPI and boundary results

| Table | Header row | First valid row | Last valid row | Valid rows | Distinct keys |
|---|---:|---:|---:|---:|---:|
| `Entry- Site Data` | 20 | 21 | 86 | 66 | 66 `SiteNo` |
| `Entry- Eq Database` | 21 | 22 | 9,086 | 9,065 | 9,065 `AssetId` |
| `Output- Asset Scores` | 16 | 17 | 10,296 | 9,065 | 9,065 `AssetId` |
| `Output- Site Scores` | 13 | 14 | 80 | 66 | 66 `SiteNo` |
| `Output- Site Risk Scores` | 13 | 15 | 80 | 66 | 66 `SiteNo` |

## Initial reconciliation conclusions

- The bounded source population is 9,065 distinct valid assets, not 9,070.
- Asset `7057` is a confirmed test record; therefore the governed portfolio asset count is provisionally 9,064 after excluding that test record, while 9,065 remains the raw bounded source count.
- `SLC05` is restored in the derived site contract from 41 asset rows: `SiteId` 143 and `Salt Lake City-Cottonwood`. This produces 67 modeled sites while preserving 66 source-master sites.
- The previously reported 70-site figure includes four narrative rows at the tail of `Entry- Site Data`; the typed site-key predicate yields 66 valid site codes.
- The bounded asset-score output contains the same 9,065 distinct asset identifiers; no source asset identifiers were absent from the scored output under the current key predicate.
- Only 9,023 scored rows have both a valid asset identifier and a site identifier found in the 66-site source population. Of the remaining 42 rows, 41 belong to restored site `SLC05`; one is test asset `7057` with site `Not` and site name `Larry's Test Site`.
- Site summary outputs contain 66 valid site keys and now reconcile to the 66 valid site keys in the site input.

## SPOF normalization results

- Header/group metadata is read from rows 24-27; answer labels are read from row 27; question rows begin at row 30.
- 66 four-column site groups were detected using a populated site label and a `Yes` answer-column header; this reconciles to the 66 valid site codes in the bounded site input.
- 62 question rows produced 4,092 site/question observations.
- Answer states were preserved as `Yes`, `No`, `N/A`, or `Blank`.
- 3,757 observations had one selected answer.
- 4 observations had multiple selected answer markers and were retained as `MultipleAnswers`.
- 331 observations had no selected marker and were retained as `Blank`.
- The 66 detected SPOF groups reconcile to the 66 valid site codes in the bounded site input. No missing site was inferred or added.

## Artifacts

- `bounded_kpi_manifest.json`: machine-readable boundaries, counts, duplicates, and source-to-score key comparison.
- `spof_observations.csv`: normalized site/question observations with source columns and normalization status.
- `restored_site_overrides.csv`: evidence-backed SLC05 site restoration with missing attributes marked for SME review.
- `artifact_build_output.txt`: captured execution summary.

## Next validation actions

1. Classify the four narrative rows excluded from the site master and retain them as source-boundary evidence.
2. Resolve whether `SLC05` should be restored to the site master and SPOF matrix, or explicitly excluded as a retired site.
3. Exclude test asset `7057` from governed portfolio measures and retain it in the exception register.
4. Reconcile the four multiple-answer SPOF observations and determine whether the workbook permits multi-select.
5. Continue score/cost formula reconciliation; these artifacts do not prove numeric score equality or threshold semantics.
