# NextField EOL Continuation Plan

Date: 2026-09-03
Status: Active continuation from workbook-backed baseline

## Verified baseline

The working project baseline is now stabilized and grounded in the actual workbook and source documentation rather than generic assumptions.

- Source of record for this PoC: the Excel workbook at `source/Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25.xlsx`
- Supporting source docs are present under `source/` and `docs/`
- The semantic model proposal is present in `source/FlexEOL_NextField_SemanticModel_TMDL.txt`
- The workbook is confirmed open and visible in Excel; no remote writes were performed
- The project is scoped as a governance-first validation before any semantic-model or Fabric implementation is finalized

## Current evidence summary

### Confirmed working facts

- The initial workbook estimate was 70 sites and 9,070 equipment rows; the approved typed boundary currently yields 66 valid sites and 9,065 valid assets.
- The model proposal explicitly references a 9-criteria weighted score and a size exponent of 0.8.
- The workbook evidence shows the SPOF input is stored in a transposed matrix format rather than in normalized long-form rows.
- The output layers are not yet direct 1:1 reconciliations of the entry population; row boundaries and zero-padding rows must be filtered out explicitly.
- The replacement threshold and SPOF risk threshold are both visible as business controls in the workbook.

### Relevant source findings

- `docs/WORKBOOK_PROFILE.md` identifies the major data-boundary gaps and the fact that output rows include padded or generated rows that should not be counted as business data.
- `docs/SOURCE_MODEL_REEVALUATION.md` explicitly documents the structural mismatch between the workbook and the proposed TMDL naming/shape.
- `docs/SPOF_NORMALIZATION_PLAN.md` identifies the required long-form normalization for site-based SPOF evidence.
- `docs/KPI_RECONCILIATION_NOTES.md` records the central issue: the score outputs do not yet reconcile cleanly to the source asset population without defined valid-record rules.

## Status table

| Step | Status | Notes |
|---|---|---|
| Step 0: Source orientation | Done | Source docs reviewed and the core model assumptions were restated and validated against project evidence. |
| Step 1: Tooling and MCP verification | Done | Node.js and Copilot CLI were verified; Power BI authoring component installed; Power BI Modeling MCP responded. |
| Step 2: Workspace scaffolding | In place | Repository structure exists and remains technology-neutral until the source model is confirmed. |
| Step 3: Model validation against workbook | Ready to begin locally | The source-to-model contract and row-boundary rules are approved; formula lineage and output mappings still require execution validation. |
| Step 4: Fabric/Power BI target confirmation | Needs decision | The intended remote workspace and write permissions must be confirmed before any remote fabric actions are taken. |

## Immediate next actions

1. Validate the workbook’s authoritative score boundaries
   - Confirm the exact first/last data rows for `Entry- Eq Database`, `Output- Asset Scores`, and the site-risk outputs.
   - Exclude padded rows, zero-ID rows, and footer content from all KPI calculations.

2. Reconcile the KPI definition before modeling
   - Define whether the business metric is based on input rows, scored rows, distinct assets, distinct sites, or output rows.
   - Preserve the 66-site and 9,065-asset execution counts, and document the excluded narrative rows and any orphaned site references.

3. Normalize the SPOF matrix into a governed long-form table
   - Preserve question text, site reference, answer, comments, and source location.
   - Treat the transposed site-block layout as a transformation problem, not as the final schema.

4. Validate the TMDL against the workbook logic
   - Align the TMDL names and measures to the actual workbook columns.
   - Confirm the weighted score formula, the threshold logic, and the cost model exponent against the workbook’s `Criteria` and `Costs and Scoring` controls.

5. Confirm the write target before any remote actions
   - Choose the intended Fabric workspace and permission path.
   - Avoid remote writes until that target is explicitly approved.

## Decisions now approved

1. Source of record for the current PoC
   - Current PoC source: Excel workbook
   - Future source assumption: CMMS/EAM, with Dataverse as a later integration option

2. KPI and row-boundary basis
   - Use bounded valid source rows and distinct business keys for portfolio counts; treat output rows as derived and exclude padded, zero-ID, and explanatory rows.

3. Exact Fabric or Power BI write target
   - The candidate workspace remains `NextField-EOL-Dev`; publication still requires explicit confirmation at implementation time.

## Recommended working posture

The project may now proceed to local, workbook-first transformation and reconciliation work under the approved contract. Remote Fabric writes remain gated until score logic, SPOF normalization, and local model validation are complete.
