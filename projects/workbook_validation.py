from openpyxl import load_workbook
from collections import defaultdict

path = r'c:\Dev\NextField\NextField-EOL\source\Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25.xlsx'
wb = load_workbook(path, read_only=True, data_only=True)

def get_rows(ws):
    for row in ws.iter_rows():
        yield [cell.value for cell in row]

checks = [
    ('Entry- Eq Database', 'AssetId', 'AssetId'),
    ('Entry- Eq Database', 'Site No.', 'Site No.'),
    ('Entry- Site Data', 'Site No.', 'Site No.'),
    ('Output- Asset Scores', 'AssetId', 'AssetId'),
    ('Output- Asset Scores', 'SiteNo', 'SiteNo'),
    ('Output- Site Scores', 'Site No.', 'Site No.'),
    ('Output- Site Risk Scores', 'Site No.', 'Site No.'),
]

for sheet_name, col_label, target in checks:
    ws = wb[sheet_name]
    header_row = None
    header_map = {}
    for r in range(1, min(ws.max_row, 40) + 1):
        vals = [cell.value for cell in ws[r]]
        if any(v is not None for v in vals):
            for c, v in enumerate(vals, start=1):
                if isinstance(v, str) and v.strip() == col_label:
                    header_row = r
                    header_map[col_label] = c
                    break
            if header_row is not None:
                break
    if header_row is None:
        print(f'{sheet_name}: header {col_label} not found')
        continue

    values = []
    for r in range(header_row + 1, ws.max_row + 1):
        v = ws.cell(r, header_map[col_label]).value
        if v is not None and str(v).strip() != '':
            values.append(v)

    distinct = len(set(values))
    print(f'{sheet_name} | {col_label} | nonblank={len(values)} distinct={distinct} sample={values[:5]}')

# print first rows of outputs for evidence
for sheet_name in ['Entry- Eq Database', 'Entry- Site Data', 'Output- Asset Scores', 'Output- Site Scores', 'Output- Site Risk Scores']:
    ws = wb[sheet_name]
    print(f'\n--- {sheet_name} first 10 rows ---')
    for r in range(1, min(ws.max_row, 18) + 1):
        vals = [ws.cell(r, c).value for c in range(1, min(ws.max_column, 15) + 1)]
        if any(v is not None for v in vals):
            print(r, vals)
PY