# Workbook Validation Findings

Date: 2026-09-03
Project: NextField EOL PoC
Status: Validation confirmed; implementation remains gated

## Scope

This validation pass inspected the workbook file directly and confirmed the actual worksheet structure and header boundaries without modifying any workbook content.

## Direct Evidence

### Workbook file

- File: `source/Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25.xlsx`

### Sheet-level evidence

| Sheet | Max row count | Max column count | Observed structure |
|---|---:|---:|---|
| Entry- Eq Database | 10,046 | 233 | Large entry table with metadata and instructions above the data table |
| Entry- Site Data | 128 | 31 | Site master sheet with metadata and instructions before table data |
| Entry- Site SPOF Data | 149 | 282 | Multi-site SPOF matrix with repeated site blocks and transposed structure |
| Output- Asset Scores | 10,553 | 25 | Output table plus metadata, header rows, and generated rows beyond the true business boundary |
| Output- Site Scores | 104 | 30 | Summary table with structured site-level metrics |
| Output- Site Risk Scores | 104 | 77 | Risk summary table with row-level site scores and repeated section fields |
| Scoring Engine | 10,570 | 163 | Calculation sheet, not the authoritative source table |

## Verified boundary observations

### 1. Entry tables are not raw data at the top of the sheet

Each of the entry sheets contains workbook narrative content, overview text, and instruction blocks before the actual data table starts.

Examples:
- `Entry- Eq Database` has metadata through row 15 and the table heading at row 12; the actual data begins later in the sheet.
- `Entry- Site Data` has metadata through row 15 with the site table beginning below that header area.
- `Entry- Site SPOF Data` has repeated site blocks and question fields arranged across a large transposed matrix.

### 2. Output tables are presentation artifacts, not clean source tables

The output sheets clearly show that the workbook stores an output layer rather than a fully normalized source layer.

Examples:
- `Output- Asset Scores` has a max row count of 10,553 and includes rows beyond the true business dataset.
- Row 16 is the header row for the asset output table, and rows 17-18 contain the first real asset records.
- The workbook contains generated rows and zero-value rows at the tail of the output population; these must be treated as artifacts, not valid business records.

### 3. The site score tables are summary tables rather than source tables

- `Output- Site Scores` begins with a summary table for site averages by equipment type.
- `Output- Site Risk Scores` contains site-level risk metrics and grouped question categories, but it is still a summary output sheet, not a normalized operational fact table.

### 4. The actual business data requires explicit row-boundary validation

The direct workbook inspection confirms the earlier planning concern: the output sheets are not directly importable as a clean source-of-truth table without explicit boundary rules.

This means the project must define:
- the true first and last row of valid business records
- which rows are generated padding
- which columns are source fields versus presentation fields
- the true grain for each output table and metric

## Working conclusions

The workbook is still valid as the current source-of-record benchmark, but it is not a clean, normalized semantic source yet.

The project now has direct file-level evidence that:
- the workbook contains operational entry tables and separate output tables
- the output tables include metadata and generated rows
- the SPOF matrix is structurally transposed and requires normalization
- the metric grain and business record boundaries must still be explicitly approved before implementation

## Next required validation step

The next step is to define the authoritative row boundaries and column-level metadata for each candidate table, then convert those rules into a normalized source-to-model contract before any semantic model or Power BI implementation is started.
