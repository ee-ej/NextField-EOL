from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple

from openpyxl import load_workbook


WORKBOOK_PATH = r"c:\Dev\NextField\NextField-EOL\source\Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25.xlsx"


def find_header_row(ws, target_values: List[str], start_row: int = 1, end_row: int = 100) -> Optional[int]:
    for r in range(start_row, min(end_row, ws.max_row) + 1):
        row_vals = [ws.cell(row=r, column=c).value for c in range(1, min(ws.max_column, 50) + 1)]
        row_text = [str(v).strip() if v is not None else "" for v in row_vals]
        if any(tv in row_text for tv in target_values):
            return r
    return None


def detect_row_block(ws, header_row: int, key_candidates: List[str]) -> Tuple[int, int]:
    # returns first_data_row, last_data_row based on direct cell evidence
    first_data_row = None
    last_data_row = header_row

    for r in range(header_row + 1, ws.max_row + 1):
        row_vals = [ws.cell(row=r, column=c).value for c in range(1, min(ws.max_column, 60) + 1)]
        row_flat = [v for v in row_vals if v is not None]
        if not row_flat:
            continue

        if first_data_row is None:
            first_data_row = r

        # break on obvious generated/summary footer rows by checking for text-only rows and blank rows
        text_like = sum(1 for v in row_vals if isinstance(v, str) and len(str(v).strip()) > 0)
        if text_like > 0 and not any(str(v).strip() in key_candidates for v in row_vals if isinstance(v, str)):
            # assume prose or note row; keep scanning unless it also contains a business key-like value
            pass

        last_data_row = r

    if first_data_row is None:
        first_data_row = header_row + 1

    return first_data_row, last_data_row


def summarize_sheet(ws, name: str) -> Dict[str, object]:
    result: Dict[str, object] = {"sheet": name, "max_row": ws.max_row, "max_col": ws.max_column}

    if name == "Entry- Site Data":
        header = find_header_row(ws, ["Site No."], 1, 40)
        result["header_row"] = header
        if header:
            first, last = detect_row_block(ws, header, ["Site No."])
            result["first_data_row"] = first
            result["last_data_row"] = last
    elif name == "Entry- Eq Database":
        header = find_header_row(ws, ["AssetId"], 1, 60)
        result["header_row"] = header
        if header:
            first, last = detect_row_block(ws, header, ["AssetId"])
            result["first_data_row"] = first
            result["last_data_row"] = last
    elif name == "Output- Asset Scores":
        header = find_header_row(ws, ["Original Order", "AssetId"], 1, 40)
        result["header_row"] = header
        if header:
            first, last = detect_row_block(ws, header, ["AssetId"])
            result["first_data_row"] = first
            result["last_data_row"] = last
    elif name == "Output- Site Scores":
        header = find_header_row(ws, ["Original Order", "Site No."], 1, 40)
        result["header_row"] = header
        if header:
            first, last = detect_row_block(ws, header, ["Site No."])
            result["first_data_row"] = first
            result["last_data_row"] = last
    elif name == "Output- Site Risk Scores":
        header = find_header_row(ws, ["Original Order", "Site No.", "Overall Score"], 1, 40)
        result["header_row"] = header
        if header:
            first, last = detect_row_block(ws, header, ["Site No.", "Overall Score"])
            result["first_data_row"] = first
            result["last_data_row"] = last
    elif name == "Entry- Site SPOF Data":
        # detect site block row and question rows
        site_row = find_header_row(ws, ["Site"], 20, 40)
        result["site_row"] = site_row
        question_row = find_header_row(ws, ["Are the generator(s) a minimum of N+1"], 1, 100)
        result["risk_question_row"] = question_row
        if site_row:
            result["sample_site_block"] = [ws.cell(site_row, c).value for c in range(1, min(ws.max_column, 20) + 1)]
    elif name == "Scoring Engine":
        header = find_header_row(ws, ["AssetId"], 15, 40)
        result["header_row"] = header
        if header:
            first, last = detect_row_block(ws, header, ["AssetId"])
            result["first_data_row"] = first
            result["last_data_row"] = last

    return result


def main() -> None:
    wb = load_workbook(WORKBOOK_PATH, read_only=True, data_only=True)
    target_names = [
        "Entry- Eq Database",
        "Entry- Site Data",
        "Entry- Site SPOF Data",
        "Scoring Engine",
        "Output- Asset Scores",
        "Output- Site Scores",
        "Output- Site Risk Scores",
    ]

    print("Workbook source validation summary")
    print(f"Path: {WORKBOOK_PATH}")
    print("\nDetected sheets:")
    for s in wb.sheetnames:
        print(f"- {s}")

    print("\nCandidate boundary summary:")
    for sheet_name in target_names:
        if sheet_name not in wb.sheetnames:
            continue
        ws = wb[sheet_name]
        summary = summarize_sheet(ws, sheet_name)
        print(f"\n[{sheet_name}]")
        for key, value in summary.items():
            print(f"  {key}: {value}")

    print("\nThese are direct workbook observations only; no workbook content was modified.")


if __name__ == "__main__":
    main()
