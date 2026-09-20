# Next Validation Plan

Date: 2026-09-03
Project: NextField EOL PoC
Status: Ready to execute in read-only validation mode

## Objective

Complete the minimum workbook validation needed to convert the current planning evidence into an approved source-to-model contract before any Fabric semantic model or report implementation begins.

## Validation Principle

Do not build the semantic model until the workbook business grain, score lineage, and SPOF contract are validated and approved. This is a controlled proof-of-concept gate, not a rapid build step.

## Phase 1: Workbook structural validation

### Goal

Establish the true business grains and the boundaries between valid data and generated padding.

### Tasks

1. Identify authoritative header rows and data blocks.
2. Distinguish valid business rows from padded, blank, or zero-filled generated rows.
3. Confirm the real grains for:
   - site records
   - asset records
   - equipment rows
   - scored rows
   - exception rows
4. Validate whether output tables are workbook-generated summaries or stable source records.
5. Document the column-level lineage from source workbook input to scoring/output tables.

### Exit criteria

- Every output table has a documented grain.
- Generated rows are explicitly classified and excluded from KPI logic.
- The project can state which rows are valid business records and which are artifacts.

## Phase 2: Score and cost validation

### Goal

Prove that score outputs are traceable to the workbook scoring engine and business rules.

### Tasks

1. Reconcile sample engine rows with asset IDs and site IDs.
2. Confirm whether the output scoring tables are strictly aligned to the engine rows or if there are dropped or duplicated records.
3. Validate the logic behind:
   - replacement threshold = 50.0
   - size exponent = 0.8
   - cost factor = 0.6
   - inflation = 3.5%
   - regional multipliers
4. Confirm whether the 0.6 value is a true governed model rule or a workbook-only convention.
5. Document the exact inputs to each score and cost calculation.

### Exit criteria

- Score lineage is proven or explicitly called out as unproven.
- Cost logic is approved or flagged for rule negotiation.
- A clear model parameter strategy exists for any workbook-only tuning factor.

## Phase 3: SPOF reconciliation

### Goal

Establish a trustworthy normalized SPOF evidence model.

### Tasks

1. Trace each site-level SPOF block to the underlying site number.
2. Confirm the actual coverage and duplication count across the matrix.
3. Define the canonical representation for:
   - Yes
   - No
   - N/A
   - blank values
   - comments
   - duplicate selections
4. Model the SPOF evidence as a normalized long-form table with source-column traceability.
5. Determine whether the business decision is site-level risk, asset-level risk, or both.

### Exit criteria

- The SPOF matrix is reconciled to actual site coverage.
- The normalized table shape is approved.
- The record-level meaning of all flags is documented.

## Phase 4: KPI and metric contract

### Goal

Create a single authoritative metric contract for all leadership and operational views.

### Tasks

1. Define the count rules for site count, asset count, scored site count, scored asset count, and exception count.
2. Decide whether KPI counts are based on source rows, valid flagged rows, or transformed output rows.
3. Document how the 70-site count and ~9,070 asset/equipment count relate.
4. Agree on the metric semantics before any DAX or report measure work begins.

### Exit criteria

- A single KPI contract is approved.
- Every report measure follows that contract.
- No KPI is left as an implicit workbook interpretation.

## Phase 5: Decision gate and implementation readiness

### Goal

Move from validation to a controlled build decision.

### Gate conditions

The project should proceed only if all of the following are true:

- Grain definitions are approved.
- Score lineage is reconciled.
- SPOF contract is approved.
- KPI contract is approved.
- Leadership landing-page goal is confirmed.
- Local validation has been completed without unresolved source conflicts.

### If unresolved

If any gate remains unresolved:
- stop implementation,
- document the open issue,
- capture the proposed resolution,
- escalate for business approval before building.

## Recommended execution order

1. Structural validation
2. Score/cost validation
3. SPOF reconciliation
4. KPI contract
5. Decision gate

## Final status

This is the approved next-step plan for the project. It is intentionally conservative and is designed to prevent a semantic model or report from being based on unproven workbook assumptions.
