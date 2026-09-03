# SPOF Normalization Plan

Date: 2026-09-03
Status: Proposed planning artifact

## Objective

Convert the transposed `Entry- Site SPOF Data` matrix into long-form evidence without losing the source location or treating incomplete coverage as complete.

## Verified Layout

- Sheet: `Entry- Site SPOF Data`
- Site-group labels begin at row 24.
- Site metadata fields occupy rows 25-27.
- Answer headings occupy row 28.
- Question rows begin at row 29.
- The inspected matrix spans columns 7-282, which forms 69 apparent four-column site blocks.
- Site input contains 70 distinct site numbers; block coverage is unresolved.

## Candidate Long-Form Contract

| Field | Rule |
|---|---|
| `SiteNo` | Site identifier from the group header; candidate business key from site input |
| `SPOFQuestionId` | Question identifier from column 1, such as `1.05` |
| `SPOFQuestion` | Question text from column 2 |
| `Answer` | Normalized selected answer: `Yes`, `No`, `N/A`, or `Blank` |
| `DetailedComments` | Comment value from the group's fourth column where present |
| `SourceSheet` | Literal source sheet name |
| `SourceColumnStart` | First source column of the four-column group |
| `SourceColumnEnd` | Last source column of the four-column group |
| `SourceRows` | Source header/question rows used to derive the record |
| `SourceDate` | Group date from row 26 when valid |
| `Lead` | Group lead from row 27 when present |
| `NormalizationStatus` | `Valid`, `UnmappedSite`, `MultipleAnswers`, `InvalidMarker`, or `BlankQuestion` |

## Transformation Rules To Validate

1. Discover group starts from row 24/25 site labels; do not assume every four-column span is populated.
2. Read answer markers from the three answer columns and comments from the fourth column.
3. Normalize `x` and `X` as selected markers while retaining the original marker in a provenance field if needed.
4. Preserve `N/A` as a distinct answer state; do not convert it to `No`.
5. Preserve blanks as missing evidence, not as a negative answer.
6. Flag multiple selected answer columns rather than choosing one silently.
7. Flag groups whose site number is not present in the site dimension.
8. Reconcile all discovered group site numbers to the 70-site input population.
9. Compare normalized question counts and selected answers to `Output- Site Risk Scores` after a controlled workbook recalculation.
10. Keep comments and source column coordinates so analysts can trace every result back to the workbook.

## Open Reconciliation Questions

- Which site number is absent from the 69 apparent groups, or is represented by a nonstandard block?
- Are all groups exactly four columns wide across the full matrix?
- Can one question have multiple selected answer markers?
- Does the risk output count `Yes`, selected `No`, blanks, or another condition?
- How does `N/A` affect the site risk score and threshold count?

No workbook data was changed by this plan.
