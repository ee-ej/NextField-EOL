# V1 and V2 Engineering Analysis

Date: 2026-09-03
Audience: Engineering and data-model implementation team
Status: V1 validated baseline; V2 candidate revision requiring clarification and repair

## Executive summary

V1 and V2 are not equivalent workbook versions that can be compared by simply refreshing rows. V1 contains the asset input, site input, transposed SPOF input, scoring engine, and rendered outputs used to establish the current source-to-model contract. V2 removes the V1 asset-input sheet, changes the visible sheet/output structure, contains widespread `#REF!` formulas, and represents a smaller site snapshot.

Recommendation: preserve V1 as the audit baseline and treat V2 as a candidate revision branch. Do not merge V2 into the model or use V2 score outputs until its missing asset source, broken dependencies, site scope, and calculation changes are explained and corrected.

## Workbooks reviewed

- **V1:** `source/Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25.xlsx`
- **V2:** `source/Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25 - Flex Input v2.xlsx`

Both workbooks were inspected read-only. Neither source workbook was modified.

## V1 validated baseline

The current V1 contract uses these source and derived layers:

- `Entry- Site Data`: bounded site input, header row 20, 66 valid site codes.
- `Entry- Eq Database`: bounded asset input, header row 21, 9,065 valid distinct assets.
- `Entry- Site SPOF Data`: transposed site/question matrix, 66 detected site groups and 62 question rows.
- `Scoring Engine`: calculation evidence and score lineage.
- `Output- Asset Scores`: derived asset score results, 9,065 distinct scored assets with full key lineage to the engine.
- `Output- Site Scores`: 66 valid site summary records.
- `Output- Site Risk Scores`: 66 valid site-risk records.

Additional V1 decisions and findings:

- `SLC05` is restored in derived artifacts from 41 asset rows, with `SiteId` 143 and site name `Salt Lake City-Cottonwood`.
- The provisional modeled site count is 67: 66 source-master sites plus restored `SLC05`.
- Asset `7057` is a test record and is excluded from governed portfolio measures.
- The provisional governed asset count is 9,064 after excluding asset `7057` from the raw 9,065 source count.
- Full source-to-engine-to-output `AssetId` alignment passed for 9,065 assets with zero mismatches.
- Recalculated score comparison passed for 2,013 complete rows with zero differences across the overall score and nine components; 3,351 rows lacked one or more dependent values.
- Replacement threshold is inclusive at `50.0`.
- Site-risk threshold counts are inclusive at `7.0`; 396 category counts passed validation.
- Representative cost outputs matched the engine for five recalculated assets.

## V2 observed structure and results

V2 contains these relevant areas:

- `Entry- Site Data`
- `Entry- Operating Issues`
- `Entry- Service and Support`
- `Entry- Refurbishment`
- `Entry- Install Complexity`
- `Scoring Engine`
- `Entry- Site SPOF Data`
- `Scores Actual`
- `Transpose Actual`
- `Site Risk Scores OG`
- `Site EOL Scores for Risk`
- `Scores Actual Adj`
- `Transpose Actual Adj`

V2 does not contain the V1 `Entry- Eq Database` sheet or the V1 visible output sheets such as `Output- Asset Scores` and `Output- Site Risk Scores`.

Read-only targeted inspection found:

| Area | V2 observation | Engineering meaning |
|---|---|---|
| Site input | 63 valid site codes | Different portfolio snapshot or reduced scope; cannot inherit V1 site KPIs |
| SLC05 | Absent from site input and SPOF groups | V1 restoration is not present in V2; scope/status must be clarified |
| SPOF | 63 detected site groups | Internally matches V2's 63-site snapshot, but does not cover V1's 66 source sites or restored SLC05 |
| Asset source | V1 asset-input sheet absent | No direct V2 asset-population reconciliation is currently possible |
| `Entry- Site Data` | 382 `#REF!` cells | Site priority and derived site fields are broken or dependent on missing content |
| `Scoring Engine` | 445,145 `#REF!` cells | V2 scoring calculations are not trustworthy or executable as inspected |
| `Scores Actual Adj` | 149 `#REF!` cells | Adjusted score output is not implementation-ready |
| Site input formulas | `#REF!` appears in priority-related columns | V2 site-level business-priority calculations require dependency repair |

V2 also shows `#REF!` values in scoring-engine rows and header/formula regions. These must be distinguished between genuinely broken formulas, intentionally removed source references, and formulas that require an external workbook or named range.

## V1-to-V2 comparison conclusions

### 1. Source scope changed

V2 has 63 valid site codes versus V1's 66 source-master site codes, plus the V1-derived restoration of SLC05. This could mean:

- V2 intentionally represents a newer active portfolio scope.
- Three V1 sites were retired or removed.
- V2 is an input-only workbook that intentionally excludes some sites.
- Site rows were omitted accidentally.

No scope interpretation should be assumed from the count alone.

### 2. Asset scope cannot yet be compared

V1 has a 233-column asset database with 9,065 valid distinct assets. V2 has no sheet with the V1 asset database name, and no replacement asset source has been identified. This blocks:

- asset additions/removals comparison
- asset attribute corrections
- asset-to-site reconciliation
- score coverage comparison
- cost exposure comparison
- test/retired/available population comparison

### 3. Calculation architecture changed or is incomplete

V1 uses `Scoring Engine` plus rendered output sheets. V2 uses areas such as `Scores Actual`, `Scores Actual Adj`, `Transpose Actual`, and `Transpose Actual Adj`, but the inspected formulas contain extensive `#REF!` values. The V2 calculation architecture may be a redesign, a partial extraction, or a workbook with missing linked content.

### 4. SPOF structure changed in population, not necessarily in design

Both versions use a transposed SPOF matrix, but V2 has 63 detected groups and V1 has 66 source groups. V2 must be checked for question-set changes, answer-marker changes, block-width changes, comments, and missing sites before its data can be merged with V1 normalization logic.

### 5. V2 may contain meaningful refinements, but they are not yet separable from defects

Potential refinements include new input sheets for refurbishment and installation complexity, renamed score layers, and revised site data. However, those potential improvements cannot be accepted as calculation refinements while their dependencies evaluate to `#REF!`.

## Questions for engineering and the source owner

### Source and version identity

1. Is V2 intended to replace V1, supplement V1, or provide only revised input tabs?
2. What workbook/application version produced V2, and what is its authoritative effective date?
3. Was V2 saved after links, named ranges, tables, or source sheets were removed?
4. Are the missing V1 asset and output sheets stored in another workbook or external data source?
5. Which workbook is the intended source of record for this PoC after V2 review?

### Asset population and keys

6. Where is the V2 asset population located?
7. Is the V2 asset population identical to V1, a filtered subset, or a refreshed extract?
8. What is the V2 asset business key: `AssetId`, `AssetNo`, another identifier, or a composite?
9. Are asset IDs stable between V1 and V2?
10. Which assets were added, removed, retired, or reclassified?
11. Should test asset `7057` and similar records be excluded in V2?
12. How should assets with blank, `Not`, retired, available, or multi-site assignments be handled?
13. Are the new V2 sheets `Entry- Refurbishment` and `Entry- Install Complexity` asset-grain inputs, and what keys join them to assets?

### Site scope and SLC05

14. Is the V2 63-site scope intentional?
15. Which three V1 source sites are absent from V2?
16. Is `SLC05` retired, renamed, intentionally omitted, or missing due to an extraction error?
17. Should `SLC05` remain in the governed model with restored metadata, or should it be excluded as retired?
18. If SLC05 is active, where are its site attributes, SPOF responses, business-priority inputs, and risk scores in V2?
19. Are site names and site IDs stable across versions?
20. Are multiple site codes such as `DEN05.01`, `PDX01.01`, and `SLC04.01` separate sites or campus/subsite identifiers?

### Formula and dependency repair

21. What caused the 382 `#REF!` cells in `Entry- Site Data`?
22. What caused the 445,145 `#REF!` cells in `Scoring Engine`?
23. What caused the 149 `#REF!` cells in `Scores Actual Adj`?
24. Do the broken references point to deleted V1 sheets, external workbooks, renamed sheets, or removed columns?
25. Are named ranges, Excel tables, Power Query queries, connections, or VBA/macros required for V2 calculations?
26. Can the source owner provide a recalculated V2 with all dependencies present and no `#REF!` values?
27. Are V2 score layers intended to reproduce V1's nine criteria and weights, or has the scoring methodology changed?
28. Are V1's inclusive thresholds of `50.0` and `7.0` still valid in V2?
29. Is the `0.6` cost factor still applied, and in what formula position?
30. Is the `0.8` equipment-size exponent unchanged?
31. Have inflation and regional multipliers changed?
32. What is the intended relationship among `Scores Actual`, `Scores Actual Adj`, `Site EOL Scores for Risk`, and `Transpose Actual Adj`?

### SPOF and risk semantics

33. Did the V2 question set change from V1's 62 questions?
34. Are V2 answer markers still `x`/`X`, and are blanks and `N/A` semantically unchanged?
35. Does V2 permit multiple answer selections for one question?
36. Are comments stored in the same fourth column of each site block?
37. Why are there 63 V2 site groups, and do they exactly match the 63 V2 site input keys?
38. What is the mapping from raw answer state to numeric risk value?
39. Are risk weights or category ranges changed in V2?
40. Is the site-risk threshold still inclusive at `7.0`?

### KPI and reporting contract

41. Which V2 count is authoritative for sites and assets?
42. Should the report show source sites, active sites, modeled sites, and scored sites separately?
43. Should restored or inferred sites such as SLC05 be included in portfolio KPIs before SME confirmation?
44. What is the governed definition of scored asset coverage when score values are blank or calculation dependencies are broken?
45. How should V2 data-quality exceptions appear in the report?
46. Should V2's new refurbishment and installation-complexity attributes affect investment priority, cost, risk, or only drillthrough detail?

## Concerns and risks

### Critical blockers

- V2 has no identified asset source equivalent to V1's `Entry- Eq Database`.
- V2 contains pervasive `#REF!` formulas in core site and scoring logic.
- V2 scope is smaller than V1 and omits SLC05.
- V2 cannot currently be reconciled to V1 at asset grain.
- Using V2 score outputs before dependency repair could publish invalid priorities or costs.

### High concerns

- V2 may have changed calculation architecture without a change log or mapping specification.
- V2 site priority fields are broken, so leadership ranking cannot be trusted.
- V2 SPOF coverage may be internally consistent but is not comparable to V1 until the question set and site scope are mapped.
- The absence of V1 output sheets makes it unclear whether V2 is input-only or intended to produce a different report contract.
- V2 may depend on hidden workbook features not preserved by the inspected file, including named ranges, external links, queries, or macros.

### Medium concerns

- V1's restored SLC05 is derived from asset evidence, not complete site/SPOF evidence; V2 may clarify its status but currently omits it.
- Formula caches differ across V1 and require controlled recalculation; V2's `#REF!` values make cache comparison even less reliable.
- New V2 input areas may require new dimensions/facts and may change the approved model grain.
- Site names are descriptive and cannot replace stable site keys.

## Data corrections or clarifications that would unblock progress

The smallest useful correction package from the source owner would contain:

1. A V2 workbook with all intended sheets and dependencies restored, saved after a full recalculation.
2. A V2 asset extract containing stable `AssetId`, `SiteNo`, category, status, and source-row provenance.
3. A site crosswalk with V1 site code, V2 site code, site name, active/retired status, and effective date.
4. An explicit SLC05 decision and its site-level attributes, SPOF responses, and status.
5. A formula/dependency map for the V2 score layers.
6. A statement of whether the nine V1 criteria, weights, thresholds, exponent, inflation, regional multipliers, and 0.6 factor changed.
7. A SPOF question crosswalk showing question ID, text, category, answer semantics, and any changed weighting.
8. A test-record register identifying records such as asset `7057` that must be excluded.
9. A V1-to-V2 change register for sites, assets, fields, formulas, and outputs.
10. A recalculated sample with expected score and cost results for at least five assets and five sites.

## Recommended engineering sequence

1. Freeze V1 as the audit baseline.
2. Repair or obtain V2 dependencies until `#REF!` counts are zero or explicitly explained.
3. Locate or receive the V2 asset source.
4. Build a V1-to-V2 site and asset crosswalk.
5. Compare schema, row boundaries, keys, statuses, and business populations.
6. Compare score formulas and representative numeric results.
7. Compare SPOF question and answer semantics.
8. Classify changes as correction, refinement, scope change, presentation change, or unresolved.
9. Update the approved source-to-model contract only after that classification.
10. Select V1, V2, or a governed combination as the implementation source.

## Current engineering decision

V1 remains the implementation and audit baseline. V2 is approved for continued read-only analysis and dependency repair only. No V2 score, cost, site-priority, or risk result should enter the local prototype until the blockers above are resolved and the V1-to-V2 change register is reviewed.
