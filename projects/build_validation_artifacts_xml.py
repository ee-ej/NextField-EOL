from __future__ import annotations

import csv
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "source" / "Flex Asset EOL and Site Risk Evaluation Tool Ver 3.0 3.6.25.xlsx"
OUT = ROOT / "reports" / "validation"
NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
REL_ID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def col_number(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref).group(0)
    result = 0
    for letter in letters:
        result = result * 26 + ord(letter) - 64
    return result


def read_workbook() -> dict[str, list[list[str]]]:
    with zipfile.ZipFile(WORKBOOK) as archive:
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in root.findall("main:si", NS):
                shared.append("".join(node.text or "" for node in item.iter() if node.tag.endswith("}t")))
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
        result = {}
        for sheet in workbook.find("main:sheets", NS):
            name = sheet.attrib["name"]
            target = rel_map[sheet.attrib[REL_ID]]
            path = target if target.startswith("xl/") else "xl/" + target.lstrip("/")
            rows = []
            for row in ET.fromstring(archive.read(path)).findall(".//main:sheetData/main:row", NS):
                values = {}
                for cell in row.findall("main:c", NS):
                    ref = cell.attrib.get("r", "A1")
                    value = cell.find("main:v", NS)
                    text = ""
                    if value is not None and value.text is not None:
                        text = value.text
                        if cell.attrib.get("t") == "s":
                            text = shared[int(text)]
                    elif cell.find("main:is", NS) is not None:
                        text = "".join(node.text or "" for node in cell.iter() if node.tag.endswith("}t"))
                    values[col_number(ref)] = text
                rows.append(values)
            result[name] = rows
        return result


def text(row: dict[int, str], column: int) -> str:
    return str(row.get(column, "")).strip()


def find_header(rows: list[dict[int, str]], label: str, limit: int = 80) -> tuple[int, int]:
    for index, row in enumerate(rows[:limit], start=1):
        for column, value in row.items():
            if value.strip() == label:
                return index, column
    raise ValueError(f"Missing header {label}")


def valid_asset(value: str) -> bool:
    try:
        return float(value) > 0 and float(value).is_integer()
    except ValueError:
        return False


def valid_site(value: str, known: set[str] | None = None) -> bool:
    if not value or value in {"-", "N/A", "0"}:
        return False
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.\-]*", value):
        return False
    return known is None or value in known


def profile(rows: list[dict[int, str]], header: int, key_col: int, predicate, known: set[str] | None = None) -> tuple[dict, list[dict]]:
    valid = []
    excluded = 0
    for row_number, row in enumerate(rows[header:], start=header + 1):
        key = text(row, key_col)
        if predicate(key, known) if known is not None else predicate(key):
            valid.append({"row": row_number, "key": key})
        else:
            excluded += 1
    keys = [item["key"] for item in valid]
    duplicates = {key: count for key, count in Counter(keys).items() if count > 1}
    return ({"header_row": header, "first_valid_row": valid[0]["row"] if valid else None, "last_valid_row": valid[-1]["row"] if valid else None, "valid_row_count": len(valid), "distinct_key_count": len(set(keys)), "duplicate_keys": duplicates, "excluded_row_count": excluded, "used_range_max_row": len(rows)}, valid)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sheets = read_workbook()
    site_rows = sheets["Entry- Site Data"]
    site_header, site_col = find_header(site_rows, "Site No.")
    site_profile, sites = profile(site_rows, site_header, site_col, valid_site)
    known_sites = {item["key"] for item in sites}

    asset_rows = sheets["Entry- Eq Database"]
    asset_header, asset_col = find_header(asset_rows, "AssetId")
    asset_profile, assets = profile(asset_rows, asset_header, asset_col, valid_asset)
    score_rows = sheets["Output- Asset Scores"]
    score_header, score_col = find_header(score_rows, "AssetId")
    score_profile, scored = profile(score_rows, score_header, score_col, valid_asset)
    score_site_col = find_header(score_rows, "SiteNo")[1]
    scored_context = [row for row in score_rows[score_header:] if valid_asset(text(row, score_col)) and valid_site(text(row, score_site_col), known_sites)]
    scored_without_site = [{"asset_id": text(row, score_col), "site_no": text(row, score_site_col)} for row in score_rows[score_header:] if valid_asset(text(row, score_col)) and not valid_site(text(row, score_site_col), known_sites)]

    site_score_rows = sheets["Output- Site Scores"]
    site_score_header, site_score_col = find_header(site_score_rows, "Site No.")
    site_score_profile, site_score_valid = profile(site_score_rows, site_score_header, site_score_col, valid_site, known_sites)
    risk_rows = sheets["Output- Site Risk Scores"]
    risk_header, risk_col = find_header(risk_rows, "Site No.")
    risk_profile, risk_valid = profile(risk_rows, risk_header, risk_col, valid_site, known_sites)

    source_keys = {item["key"] for item in assets}
    scored_keys = {item["key"] for item in scored}
    restored_site = {"SiteNo": "SLC05", "SiteId": "143", "SiteName": "Salt Lake City-Cottonwood", "Ownership": "", "AssetClass": "", "Gen": "", "EBITDA": "", "SourceSheet": "Entry- Eq Database", "SourceEvidence": "41 asset rows", "RestorationStatus": "RestoredFromAssetEvidence", "NeedsSMEReview": "true"}
    manifest = {"workbook": str(WORKBOOK), "validity_rules": {"asset": "numeric AssetId greater than zero", "site": "nonblank site code matching the approved site-code pattern", "output": "valid nonzero business key; output rows are derived facts"}, "kpis": {"sites_in_portfolio_source": len(known_sites), "sites_in_portfolio_with_restored_slc05": len(known_sites) + 1, "assets_in_source": len(source_keys), "equipment_rows": len(assets), "scored_assets": len(scored_keys), "scored_rows_with_site_context": len(scored_context), "source_assets_absent_from_scored_output": sorted(source_keys - scored_keys)}, "restored_sites": [restored_site], "tables": {"Entry- Site Data": site_profile, "Entry- Eq Database": asset_profile, "Output- Asset Scores": score_profile, "Output- Site Scores": site_score_profile, "Output- Site Risk Scores": risk_profile}}

    spof = sheets["Entry- Site SPOF Data"]
    starts = [column for column in range(7, 283) if text(spof[23], column) and text(spof[26], column) == "Yes"]
    observations = []
    questions = 0
    for row_number in range(29, len(spof)):
        question_id = text(spof[row_number], 1)
        question = text(spof[row_number], 2)
        if not re.fullmatch(r"\d+(\.\d+)?", question_id) or not question:
            continue
        questions += 1
        for start in starts:
            markers = [text(spof[row_number], start + offset) for offset in range(3)]
            selected = [label for label, marker in zip(("Yes", "No", "N/A"), markers) if marker.lower() == "x"]
            status = "Valid" if len(selected) == 1 else "Blank" if not selected else "MultipleAnswers"
            observations.append({"SiteNo": text(spof[23], start), "SPOFQuestionId": question_id, "SPOFQuestion": question, "AnswerValue": selected[0] if len(selected) == 1 else "|".join(selected) or "Blank", "OriginalMarker": "|".join(marker for marker in markers if marker), "DetailedComments": text(spof[row_number], start + 3), "SourceSheet": "Entry- Site SPOF Data", "SourceColumnStart": start, "SourceColumnEnd": start + 3, "SourceRows": f"24,25,26,27,{row_number + 1}", "NormalizationStatus": status})
    spof_sites = {row["SiteNo"] for row in observations if row["SiteNo"]}
    site_score_sites = {row["key"] for row in site_score_valid}
    risk_sites = {row["key"] for row in risk_valid}
    manifest["reconciliation"] = {
        "sites_missing_from_site_scores": sorted(known_sites - site_score_sites),
        "sites_missing_from_site_risk_scores": sorted(known_sites - risk_sites),
        "sites_missing_from_spof_groups": sorted(known_sites - spof_sites),
        "restored_site_missing_from_site_scores": ["SLC05"],
        "restored_site_missing_from_site_risk_scores": ["SLC05"],
        "restored_site_missing_from_spof_groups": ["SLC05"],
        "scored_rows_without_valid_site_context": scored_without_site,
    }
    manifest["spof"] = {"group_row": 24, "question_start_row": 30, "group_count": len(starts), "question_count": questions, "observation_count": len(observations), "group_sites": sorted(spof_sites), "status_counts": dict(Counter(row["NormalizationStatus"] for row in observations))}
    (OUT / "bounded_kpi_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    with (OUT / "restored_site_overrides.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = list(restored_site)
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow(restored_site)
    with (OUT / "spof_observations.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = list(observations[0]) if observations else ["SiteNo"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(observations)
    print(json.dumps(manifest, indent=2))
    print(f"Wrote artifacts to {OUT}")


if __name__ == "__main__":
    main()
