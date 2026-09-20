# NextField EOL Decision Log

Date: 2026-09-03
Project: NextField EOL PoC
Status: Approved decision baseline for validation and implementation planning

## Purpose

This decision log records the approved baseline for the NextField EOL proof of concept. The recommendations previously identified during planning are adopted as project decisions and will guide validation, model design, and implementation sequencing.

## Approved Decision Summary

| Decision area | Decision status | Approved decision |
|---|---|---|
| Source of record | Approved | The Excel workbook remains the current PoC source of record for this effort. CMMS/EAM is the presumed future operational source, and Dataverse remains a future integration option, but neither is a current dependency. |
| KPI definitions | Approved | KPI logic will be defined using a single documented metric grain and validated directly against the workbook before model implementation. |
| SPOF contract | Approved | SPOF will be modeled as a normalized long-form table with source traceability and explicit handling for blanks, N/A values, duplicates, and comments. |
| Cost/score factor governance | Approved | The 0.6 factor and related cost/score controls will be treated as explicit, documented model rules unless SME review proves they are workbook-only conventions. |
| Leadership landing-page objective | Approved | The primary landing-page decision is investment sequencing: which sites/assets require investment first. |
| Semantic model creation path | Approved | The project will validate the workbook-to-model contract locally before committing to a Fabric implementation. |
| Fabric deployment | Approved | No remote writes or Fabric deployment will occur before workbook validation and model contract approval are complete. |

## Current Approved Baseline

- The Excel workbook is the current PoC source of record.
- CMMS/EAM is the presumed future operational source, but it is not currently available or approved.
- Dataverse remains a future integration option, not an active dependency for this phase.
- The target Fabric workspace is approved as NextField-EOL-Dev.
- Remote writes are not approved until model-contract validation is complete.
- The supplied TMDL is a candidate scaffold and not yet approved as the final model contract.

## Decision Details

### 1. Workbook-to-model grain definition

Decision: The project will validate workbook grain definitions before implementation and will treat generated or padded rows as artifacts rather than valid business records until proven otherwise.

Approved interpretation:
- The workbook is the benchmark source and must be reconciled to a clean business grain.
- Any padded, generated, or zero-valued rows are not assumed to be valid business rows.
- Site, asset, equipment, and scored-row metrics must each be explicitly defined before use in the model.

### 2. KPI reconciliation

Decision: KPI definitions will be formally reconciled against the workbook before any model or report logic is relied on.

Approved interpretation:
- Site count, asset count, equipment-row count, and scored-row count will each use a defined business grain.
- The 70-site and approximately 9,070 asset/equipment count relationship must be explained and reconciled as a valid business rule or as a data artifact difference.
- Report measures must align to the approved KPI contract rather than ad hoc workbook outputs.

### 3. SPOF normalization and evidence handling

Decision: SPOF will be represented in a long-form, normalized data pattern with explicit source traceability.

Approved interpretation:
- Yes, No, N/A, blank, duplicate, and comment states will be handled deliberately and documented.
- SPOF evidence will retain its source provenance even when transformed into normalized operational tables.
- The normalized table will be treated as the governing operational contract for SPOF analysis.

### 4. Score and cost rule governance

Decision: The 0.6 factor and related cost/score controls are governed by an explicit, documented rule set until SME review says otherwise.

Approved interpretation:
- The workbook contains valid business logic that must be validated before implementation.
- Any transformed or parameterized business logic will be documented in the source-to-model contract.
- The model will not assume that workbook-only conventions are permanent unless they are explicitly approved.

### 5. Leadership landing-page objective

Decision: The first-use landing experience will be oriented around investment prioritization.

Approved interpretation:
- The primary answer the page must provide is: which sites/assets require investment first?
- Supporting views may explain risk concentration, capital exposure, and SPOF posture, but they do not replace the primary investment-priority question.

### 6. Implementation gate

Decision: The project will validate the workbook-to-model contract locally before any semantic model or Fabric deployment is approved.

Approved interpretation:
- Validation is required before report or semantic model implementation.
- Fabric remote writes and report publishing are blocked until the contract is approved.

## Current Evidence Summary

The current planning and analysis documents indicate the following validated conclusions:

- The workbook is usable as the authoritative benchmark source for the PoC.
- The workbook is not yet proven to be a clean normalized semantic source for implementation.
- Output tables include generated or padded rows and therefore cannot be assumed to be valid business rows.
- Score lineage remains in need of reconciliation.
- SPOF coverage and contract remain in need of validation.
- KPI definitions require explicit business agreement.

## Required Validation Sequence

1. Validate workbook grains and rule boundaries.
2. Reconcile score and cost logic, including the 0.6 adjustment.
3. Normalize and validate the SPOF table structure.
4. Finalize the KPI contract and metric semantics.
5. Approve the landing-page objective and decision logic.
6. Proceed to local semantic-model validation only after the above are complete.

## Final Status

Status: Approved baseline established

The project is now operating under the approved decision baseline described in this log. The workbook remains the PoC source of record, and the project will continue in validation-first mode until the workbook-to-model contract is fully reconciled and approved.

### 1. Workbook-to-model grain definition

The project has repeatedly flagged that the workbook contains generated or padded rows and that output tables do not necessarily reflect the true business grain. This must be explicitly resolved before model design.

Required answer:
- What is the true grain for each relevant output table?
- Which rows are business records and which are generated artifacts?
- How do we reconcile site count versus asset count versus equipment-row count?

### 2. KPI reconciliation

The project documents indicate a mismatch between the 70-site count and a roughly 9,070 asset/equipment-row count. That difference must be reconciled as a business definition issue, not left implicit in report visuals.

Required answer:
- Are KPI counts based on valid source rows, transformed rows, or output summary rows?
- Which metric is the primary count and which are supporting counts?
- What is the approved interpretation for leadership charts and operational drillthroughs?

## Final Status

Status: Approved source and boundary baseline; local implementation validation may begin

The workbook remains the current source of record for the PoC. The source-to-model decisions and authoritative row-boundary rules are approved. Local score-lineage validation, SPOF normalization, and model validation remain required before any governed publication or remote Fabric write.
