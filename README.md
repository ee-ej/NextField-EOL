# NextField EOL PoC

This project evaluates the Flexential End of Life and Site Risk workbook as a potential NextField proof of concept.

## Current Scope

- Treat the Excel workbook and supporting Word research as the authoritative source inputs.
- Re-evaluate the proposed semantic model directly against the workbook before adopting it.
- Preserve all original inputs under `source/` unchanged.
- Keep implementation technology open until the source, model, and UI requirements are confirmed.

## Approved Workspace

- Fabric workspace: `NextField-EOL-Dev`
- Remote writes: not approved or performed

## Open Decisions

- Current PoC source: the Excel workbook is the only available source and is treated as the source of record.
- Future source strategy: CMMS/EAM is presumed as the eventual operational source; Dataverse remains a future integration option.
- Semantic model: the supplied TMDL is a derived proposal and requires direct workbook validation.
- KPI reconciliation: resolve the relationship between the 70-site count and approximately 9,070 asset/equipment rows.

## Project Areas

- `docs/UX_EVALUATION_PRINCIPLES.md`: legacy screenshot interpretation and target experience criteria.
