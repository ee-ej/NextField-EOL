# Workbook Risk Summary

Date: 2026-09-03
Project: NextField EOL PoC

## Summary

The workbook is useful and likely authoritative as a business source, but the current evidence shows that it is not yet a clean contract for a production-style semantic model. The project has enough information to state the likely business problem and value, but not enough consistency to treat the workbook outputs as fully trusted model inputs without additional validation.

## What is working

- The workbook is available locally and preserved under the project source folder.
- The project has identified the likely business audience and objective: leadership prioritization of site and asset investment decisions.
- The source contains explicit scoring and cost controls, including replacement threshold, size exponent, cost factor, inflation assumptions, and regional multipliers.
- The workbook appears to capture enough information to support a portfolio risk and replacement prioritization story.

## What is risky

### 1. Output tables are not clearly clean business grains

The planning notes highlight that output tables contain padded or generated rows, including zero-valued asset and site rows. This means the raw workbook output region is not necessarily the same as the actual business population.

Risk: a model built directly on workbook outputs could double-count, include false records, or misstate asset/site totals.

### 2. Score lineage is not yet fully proven

The workbook exposes scoring formulas, but direct validation of full score alignment remains incomplete. The current read-only inspection could not reliably establish equality between formula outputs and cache values.

Risk: the model may reproduce inconsistent or unverified score logic, which would undermine trust in the final prioritization model.

### 3. SPOF coverage is unresolved

The SPOF matrix appears to have repeated site blocks and possible coverage gaps. The planning notes flag that the workbook has 69 apparent four-column blocks versus 70 site numbers, and coverage remains unresolved.

Risk: a normalized SPOF table built without this validation could misrepresent site-level resiliency conditions and risk concentration.

### 4. KPI reconciliation is not settled

The project has highlighted that a 70-site count and approximately 9,070 asset/equipment rows need a reconciled definition. This is a classic data-grain problem.

Risk: different audiences may interpret the same portfolio numbers differently, which weakens executive reporting and decision confidence.

### 5. The workbook is a decision support artifact, not yet a clean semantic source contract

The workbook seems to be a rich operational and planning workbook, but its output regions are shaped to answer questions, not necessarily to provide a normalized data model contract.

Risk: using the workbook without an explicit contract will create hidden assumptions that surface later as report errors or stakeholder distrust.

## Business implications

The workbook is still valuable enough to proceed with validation, but the project should not treat it as a finished data source for a first production-grade Fabric model. The safe path is to validate workbook grains, scoring, and SPOF logic first, then establish the source-to-model contract.

## Recommended interpretation

The workbook should be treated as:
- the current evidence base,
- the benchmark for business logic,
- the authoritative reference for the PoC,
- but not the final trusted semantic model source until the contract is reconciled and approved.

## Final assessment

The risk is not that the workbook is unusable. The risk is that the workbook is currently more like a business decision workbook than a normalized source system, and the team has not yet proven the exact record-level contracts required for a first implementation.

Until that proof exists, the project should remain in decision-gating and workbook validation mode rather than report or semantic model build mode.
