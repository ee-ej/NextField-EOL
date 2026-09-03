# NextField EOL PoC Work Items

Date: 2026-09-02
Status: Planning only

## Workstream 1: Workbook Source Profiling

**Objective:** Establish the actual source contracts from the Excel workbook.

Acceptance criteria:

- Every candidate source sheet has a documented header row, data region, footer/blank-row rule, and row-count profile.
- Asset input profiling covers all 233 used columns and identifies the approved projection for the governed model.
- Site, asset, score, budget, and SPOF keys are profiled for uniqueness, nulls, duplicates, and test/inactive values.
- All transformations retain source-sheet and source-column provenance.

Current evidence: header/data boundaries are verified for the principal input, asset-score, site-score, site-risk, and SPOF sheets. UsedRange padding, explanatory footers, and multi-row headers are confirmed. Full column-level profiling remains open.

## Workstream 2: Scoring Reconciliation

**Objective:** Prove whether the proposed model reproduces workbook scoring.

Acceptance criteria:

- The nine workbook weights are captured as 100, 89, 78, 67, 56, 44, 33, 22, and 11.
- Sample asset scores are recalculated from source inputs and compared with `Output- Asset Scores`.
- Sample site-risk scores are recalculated and compared with the relevant output sheets.
- Replacement threshold and SPOF threshold semantics are documented, including boundary behavior.
- Any unexplained score differences are listed as decisions or defects rather than silently corrected.

Current blocker: asset scores are rendered from `Scoring Engine` formulas, and numeric cached values were not reliable through the current read-only inspection path. Controlled recalculation or an independent calculation path is required.

## Workstream 3: SPOF Normalization

**Objective:** Define a reliable long-form representation of the transposed SPOF matrix.

Acceptance criteria:

- Site column-group boundaries are discovered from the workbook rather than assumed.
- Question identifiers, question text, answer values, comments, blanks, and `N/A` are handled explicitly.
- Case variants such as `x` and `X` are normalized without losing source traceability.
- A sample normalized output is reconciled to the workbook's risk outputs.
- The transformation design is reusable if the future source is CMMS/EAM or Dataverse.

Current blocker: the SPOF matrix presents 69 apparent four-column site blocks versus 70 distinct site numbers in site input. Coverage and any nonstandard block must be resolved before declaring normalization complete.

## Workstream 4: KPI and Capital Reconciliation

**Objective:** Make leadership metrics trustworthy and explainable.

Acceptance criteria:

- Separate definitions exist for site count, distinct asset count, equipment-row count, scored-row count, and SPOF exception count.
- The `70 sites` versus approximately `9,070` asset/equipment rows discrepancy is quantified and explained.
- Capital exposure is defined by year, site, asset, and category grain.
- The `0.8` size-scaling exponent is separated from the `0.6` overall cost correction factor.
- Any scope exclusions are visible in report context.

## Workstream 5: Leadership Decision Mapping

**Objective:** Define the business rules behind the target experience.

Acceptance criteria:

- The primary landing decision is confirmed as: which sites/assets require investment first.
- Invest, Validate, Sequence, and Monitor are defined as business states or recommendations, not assumed visual labels.
- Each state has documented inputs, thresholds, confidence behavior, and exception behavior.
- The mapping is reviewed by a business SME before becoming a governed measure.
- The landing page can explain why a site or asset received its priority.

## Workstream 6: Role-Aware UX and Page Design

**Objective:** Preserve the legacy workflow while improving current usability.

Acceptance criteria:

- The legacy screenshots are cataloged by business question, audience, grain, and drill path.
- The first page is leadership-oriented for C-suite, VP, and Director users.
- Operations and analyst users have controlled paths to exceptions, evidence, and reconciliation detail.
- The target design evaluates modern navigation, drillthrough, contextual filtering, accessibility, and confidence/freshness signals.
- A design brief specifies page regions, field bindings, semantics, and non-overlap rules.

## Workstream 7: Governance and Delivery Readiness

**Objective:** Prepare for a governed Fabric implementation without committing to one prematurely.

Acceptance criteria:

- The current source remains the Excel workbook, with CMMS/EAM as presumed future operational source and Dataverse as future option.
- The target workspace remains `NextField-EOL-Dev` unless changed by explicit approval.
- Semantic model names, report names, and other object names are proposed for review before creation.
- Security, lineage, sensitivity, refresh, and ownership requirements are documented before publication.
- The locked report specification is approved before PBIP/PBIR authoring begins.

## Recommended Sequence

1. Workbook source profiling.
2. Scoring and SPOF reconciliation.
3. KPI and capital definitions.
4. Leadership decision-state rules.
5. Role-aware page design and design brief.
6. Semantic model and report specification approval.
7. Implementation and local validation.
8. Explicit approval for publication to `NextField-EOL-Dev`.
