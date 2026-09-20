# Email Draft: Resolve ADO #624 Score Reconciliation Block

**To:** Engineering Team  
**Subject:** Action needed: resolve #624 workbook score reconciliation block

Team,

We need to resolve ADO work item #624, **Recalculate sample asset and site-risk scores**, before we can treat the proposed semantic model scores as validated.

## What is already confirmed

- The authoritative workbook is `source/Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25.xlsx`.
- A disposable copy was used for validation:
  `C:\Users\EricJohnson\AppData\Local\Temp\NextField-EOL-validation\Flex-EOL-recalculation-copy.xlsx`
- The authoritative workbook was not modified.
- Output rows 17-21 contain AssetIds 2-6 for site `LAS04`.
- Those output rows reference Scoring Engine rows 21-25 respectively.
- The source asset population and row boundaries are documented: 9,070 valid numeric AssetIds begin at row 22 and end at row 10,028.
- The nine scoring weights and the cost controls are documented in the project planning artifacts.

## Current blocker

The output formulas are present, for example `='Scoring Engine'!CC21`, but the numeric values for `Overall Score`, `Eq. Criticality`, and the corresponding Scoring Engine cells remain blank after opening, recalculating, saving, and closing the disposable copy through Excel automation.

Therefore, we have proven formula references and sample row alignment, but we have not proven numeric score equality between the scoring engine and the output layer.

## Engineering action requested

Please use one of the following controlled paths:

1. Open the disposable copy manually in Excel, confirm that formulas calculate, and export the bounded sample values for:
   - Output- Asset Scores rows 17-21
   - Scoring Engine rows 21-25
   - AssetId, Original Order, SiteNo, all nine component scores, Overall Score, and replacement-cost fields
2. If the workbook still displays blank results, trace the upstream formulas and named ranges used by the Scoring Engine and identify the missing dependency.
3. If manual Excel values are unavailable, implement an independent calculation for the bounded sample using the workbook inputs and the nine criteria weights.
4. Test at least one asset with each of the following conditions where available:
   - blank purchase date
   - multiple site numbers
   - missing category or size
   - retired or unavailable status
   - overall score exactly at replacement threshold 50.0
5. Record any unexplained difference as a defect or an explicit business decision. Do not silently adjust the model to match the output.

## Required deliverables

- A bounded source-to-engine alignment report.
- A component-score comparison for the selected sample.
- An overall-score comparison for the selected sample.
- Threshold boundary results for replacement threshold 50.0.
- A short explanation of why the Excel score cells were blank, or an independent calculation trace if they remain unavailable.
- Any required updates to the score reconciliation plan and exception register.

## Definition of done for #624

#624 can move from Blocked only when the sample's numeric values are available and each component and overall score is either reconciled to the workbook or documented as an approved exception. The validation must remain bounded and must not save changes over the authoritative workbook.

Please attach the validation output to #624 and update the work item with the calculation method, workbook copy used, sample rows, results, and any remaining assumptions.

Thanks,

Eric
