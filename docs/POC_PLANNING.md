# NextField EOL PoC Planning

Date: 2026-09-03
Status: Planning only
Target workspace: `NextField-EOL-Dev`

## Objective

Evaluate the Flexential End of Life and Site Risk workbook as the authoritative business reference, then determine the smallest governed proof of concept that can reproduce the important business decisions in a modern Power BI/Fabric experience.

The supplied TMDL is a candidate model scaffold. It is not approved as the final model until the workbook data, transformations, measures, counts, and report grains are reconciled.

## Source Strategy

Decision status: Confirmed for the current PoC

- The Excel workbook is the only available source and is the current PoC source of record.
- CMMS/EAM is the presumed eventual operational source of record, but it is not available or confirmed for this PoC.
- Dataverse is a future source/integration option and is not a current dependency.
- The initial model and report plan must therefore be workbook-grounded, with source provenance and transformation assumptions documented so a later CMMS/EAM or Dataverse transition can be evaluated without changing the business contract.

## Audience Direction

Decision status: Confirmed

Leadership is the first-use audience, with a flexible experience that can serve the role structure commonly found in datacenter operators, telecommunications providers, and large enterprises.

| Audience layer | Primary decisions | Experience emphasis |
|---|---|---|
| C-suite | Enterprise exposure, strategic risk, capital posture, and business impact | Fast portfolio scan, trend/context, exceptions, confidence and governance signals |
| VP leadership | Portfolio prioritization, investment tradeoffs, regional or business-unit comparison | Site and category comparison, budget outlook, threshold scenarios, drill paths |
| Director leadership | Program execution, remediation sequencing, accountability, and operating risk | Ranked action queues, site detail, ownership/context, evidence behind scores |
| Operations | Immediate exceptions, SPOFs, equipment condition, and remediation status | Operational monitor, filters, drillthrough, detail tables, explicit thresholds |
| Analysts | Score composition, source evidence, reconciliation, and what-if analysis | Analytical exploration, row-level evidence, model transparency, exportable detail |

The first landing experience should be leadership-oriented, while the information architecture should preserve controlled drill paths and role-appropriate detail. Personalization, audience-specific navigation, row-level security, and saved views remain design options to evaluate after the shared metric and model contracts are stable.

## Leadership Landing Decision

Decision status: Proposed from `source/NextField EOL Target Reporting.docx`

Use the combined experience with one primary answer: **Which sites/assets require investment first?** The landing page should express that as a portfolio priority view, with Invest, Validate, Sequence, and Monitor as candidate decision states.

Supporting lenses should explain the priority rather than compete with it:

- Risk concentration: where exposure is concentrated.
- Capital exposure: how much projected replacement investment is involved.
- Resiliency and SPOF posture: which reliability conditions support or challenge the priority.

The workbook currently provides replacement scores, risk scores, SPOF flags, and capital forecasts. It does not yet establish the proposed Invest/Validate/Sequence/Monitor recommendation logic. That mapping is a separate business-rule work item requiring explicit definition, confidence treatment, and SME validation.

## Guardrails

- Keep all work in planning and read-only analysis until a build plan is approved.
- Preserve the `source/` folder unchanged.
- Do not create or deploy a Fabric semantic model, Lakehouse table, report, or notebook yet.
- Do not choose CMMS/EAM or Dataverse as the source of record without an explicit decision.
- Do not treat legacy screenshots as pixel-perfect layout requirements.
- Do not accept best-practice fixes or generated DAX without review.
- Do not write to the `NextField-EOL-Dev` workspace without explicit target confirmation at implementation time.

## Planning Phases

### Phase 0: Evidence and dependencies

- Inventory the workbook, Word research, architecture image, and starter TMDL.
- Confirm Node.js, Copilot CLI, Power BI authoring skills, and Modeling MCP availability.
- Resolve the Fabric workspace and identify whether a semantic model exists.
- Record version pins and connection results in `docs/SETUP_LOG.md`.

### Phase 1: Direct workbook profiling

- Identify authoritative header rows, data regions, footer regions, and blank rows.
- Profile keys, duplicates, nulls, data types, distinct counts, and test/inactive records.
- Confirm the actual grains of asset scores, site scores, site risk, budget forecast, and SPOF outputs.
- Extract the complete scoring and cost-rule inputs.

### Phase 2: Source-to-model contract

- Map workbook fields to candidate facts and dimensions.
- Explicitly approve the projected asset field set from the 233-column source.
- Define the normalized SPOF evidence table and preserve source-column traceability.
- Define score thresholds, inclusive boundaries, and the separate 0.6 correction-factor treatment.
- Define measures for sites, assets, equipment rows, scored rows, and exceptions.

### Phase 3: Legacy UX evaluation

- Catalog each screenshot by audience, decision, grain, visual, filter, and drill path.
- Preserve familiar terminology and decision hierarchy where it helps adoption.
- Evaluate modern alternatives for navigation, drillthrough, tooltips, filtering, context summaries, accessibility, and governed explanations.
- Produce a target page map and a legacy-to-target comparison before report authoring.

### Phase 4: PoC design approval

- Select a narrow first-build scope, likely centered on portfolio/site risk and asset replacement prioritization.
- Lock the semantic model contract and report design brief.
- Confirm source-of-record direction and delivery target.
- Confirm whether the first build is workbook-seeded, source-system-connected, or both.

### Phase 5: Implementation, after approval

- Create the selected local PBIP/TMDL structure.
- Build transformations and scoring validation artifacts.
- Author report pages from the approved design brief.
- Validate model and report locally with Power BI Desktop and the Modeling MCP.
- Publish to `NextField-EOL-Dev` only after explicit approval.

## Current Dependency Status

| Dependency | Status |
|---|---|
| Authoritative XLSX | Available locally |
| Supporting Word research | Available locally |
| Legacy dashboard screenshots | Available in Word source documents |
| Starter TMDL | Available locally; derived proposal |
| Node.js | Available, `v24.18.0` |
| Copilot CLI | Available, `1.0.75` |
| Power BI authoring plugin | Installed, `0.3.14` |
| Power BI Modeling MCP | Responding |
| Power BI Desktop connection | Not currently connected |
| Fabric workspace | Target confirmed as `NextField-EOL-Dev` |
| Fabric semantic model | Not yet created or resolved |
| Remote write approval | Not granted for implementation |

## Current Evidence Status

Phase 1 profiling has established reliable structural findings but has not completed reconciliation:

- Output tables contain padded/generated rows, including zero-valued asset and site rows; UsedRange boundaries are not business-data boundaries.
- `Output- Asset Scores` is backed by `Scoring Engine` formulas. Sample engine rows 21-24 align to AssetIds 2-5, but full-population alignment is unproven.
- The workbook exposes verified scoring and cost controls, including weights, replacement threshold `50.0`, size exponent `0.8`, cost factor `0.6`, inflation `3.5%`, and regional multipliers.
- The SPOF matrix presents 69 apparent four-column site blocks across columns 7-282 versus 70 distinct site numbers in site input. Coverage is unresolved.
- Numeric score cache values were not reliable through the current read-only inspection path, so score equality is not yet established.

Phase 2 source-to-model contracting and Phase 3 UX evaluation remain blocked from finalization until these structural and scoring questions are resolved.

## Decisions Needed Before Phase 4

1. Future source-of-record path: validate the presumed CMMS/EAM direction and evaluate Dataverse as a future integration option after the workbook PoC.
2. KPI scope: define how site count, asset count, equipment-row count, and scored-row count should be presented and reconciled.
3. SPOF contract: approve the long-form normalized table shape and treatment of `Yes`, `No`, `N/A`, comments, blanks, and duplicate selections.
4. Cost governance: decide whether the 0.6 correction factor is governed model logic, an explicit parameter, or workbook-only context.
5. Leadership landing-page success criteria and the dominant decision it must support in the first 10 seconds.
6. Semantic model creation point: local first, Fabric first, or local validation followed by approved deployment.

## Planning Outputs

- `docs/SOURCE_MODEL_REEVALUATION.md`
- `docs/SOURCE_MAPPING_PROPOSAL.md`
- `docs/UX_EVALUATION_PRINCIPLES.md`
- `docs/SETUP_LOG.md`

No implementation artifacts are approved by this document.
