from __future__ import annotations

import csv
from pathlib import Path

from build_validation_artifacts_xml import (
    ROOT,
    WORKBOOK,
    find_header,
    read_workbook,
    text,
    valid_asset,
    valid_site,
)

OUTPUT = ROOT / "reports" / "prototype"
SOURCE_NAME = WORKBOOK.name


def header_map(rows: list[dict[int, str]], header_row: int) -> dict[str, int]:
    return {value: column for column, value in rows[header_row - 1].items() if value}


def write_csv(name: str, rows: list[dict[str, object]], fields: list[str]) -> None:
    with (OUTPUT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sheets = read_workbook()

    site_rows = sheets["Entry- Site Data"]
    site_header, site_key_col = find_header(site_rows, "Site No.")
    site_headers = header_map(site_rows, site_header)
    sites: list[dict[str, object]] = []
    site_keys: set[str] = set()
    for row_number, row in enumerate(site_rows[site_header:], site_header + 1):
        site_no = text(row, site_key_col)
        if not valid_site(site_no):
            continue
        site_keys.add(site_no)
        sites.append({
            "SiteNo": site_no,
            "SiteName": text(row, site_headers.get("Site Name", 2)),
            "Ownership": text(row, site_headers.get("Ownership", 3)),
            "AssetClass": text(row, site_headers.get("Asset Class", 4)),
            "Gen": text(row, site_headers.get("Gen", 5)),
            "EBITDA": text(row, site_headers.get("EBITDA", 9)),
            "SourceWorkbook": SOURCE_NAME,
            "SourceSheet": "Entry- Site Data",
            "SourceRowNumber": row_number,
            "ValidationStatus": "Valid",
            "IsRestoredRecord": "false",
        })

    sites.append({
        "SiteNo": "SLC05",
        "SiteName": "Salt Lake City-Cottonwood",
        "Ownership": "",
        "AssetClass": "",
        "Gen": "",
        "EBITDA": "",
        "SourceWorkbook": SOURCE_NAME,
        "SourceSheet": "Entry- Eq Database",
        "SourceRowNumber": "",
        "ValidationStatus": "RestoredFromAssetEvidence",
        "IsRestoredRecord": "true",
    })

    asset_rows = sheets["Entry- Eq Database"]
    asset_header, asset_key_col = find_header(asset_rows, "AssetId")
    asset_headers = header_map(asset_rows, asset_header)
    assets: list[dict[str, object]] = []
    test_asset = "7057"
    for row_number, row in enumerate(asset_rows[asset_header:], asset_header + 1):
        asset_id = text(row, asset_key_col)
        if not valid_asset(asset_id):
            continue
        site_no = text(row, asset_headers.get("SiteNo", 11))
        assets.append({
            "AssetId": asset_id,
            "AssetName": text(row, asset_headers.get("Name", 3)),
            "CategoryName": text(row, asset_headers.get("CategoryName", 2)),
            "AssetNo": text(row, asset_headers.get("AssetNo", 4)),
            "SerialNo": text(row, asset_headers.get("SerialNo", 5)),
            "Make": text(row, asset_headers.get("Make", 6)),
            "Model": text(row, asset_headers.get("Model", 7)),
            "SiteId": text(row, asset_headers.get("SiteId", 10)),
            "SiteNo": site_no,
            "SiteName": text(row, asset_headers.get("SiteName", 12)),
            "SourceWorkbook": SOURCE_NAME,
            "SourceSheet": "Entry- Eq Database",
            "SourceRowNumber": row_number,
            "ValidationStatus": "TestRecord" if asset_id == test_asset else "Valid",
            "IsTestRecord": "true" if asset_id == test_asset else "false",
        })

    score_rows = sheets["Output- Asset Scores"]
    score_header, score_key_col = find_header(score_rows, "AssetId")
    score_headers = header_map(score_rows, score_header)
    scores: list[dict[str, object]] = []
    score_fields = [
        ("AssetId", "AssetId"), ("SiteNo", "SiteNo"), ("SiteName", "SiteName"),
        ("CategoryName", "Eq. Category"), ("OverallScore", "Overall Score"),
        ("EqCriticality", "Eq. Criticality"), ("EqOperatingIssues", "Eq. Operating Issues"),
        ("EqRedundancy", "Eq. Redundancy"), ("EqServiceSupport", "Eq. Service & Support"),
        ("EqAge", "Eq. Age"), ("SiteBusinessPriority", "Site Business Priority"),
        ("EqEfficiency", "Eq. Efficiency"), ("EqMainCost", "Eq. Main Cost"),
        ("EqLoading", "Eq. Loading"), ("ROMReplacementCost", "ROM Replacement Cost ($)"),
        ("BudgetYear", "Budget Year"), ("ROMCostInBudgetYear", "ROM Cost ($) in Budget Year"),
    ]
    for row_number, row in enumerate(score_rows[score_header:], score_header + 1):
        asset_id = text(row, score_key_col)
        if not valid_asset(asset_id):
            continue
        record = {model_name: text(row, score_headers.get(source_name, 0)) for model_name, source_name in score_fields}
        record.update({
            "SourceWorkbook": SOURCE_NAME,
            "SourceSheet": "Output- Asset Scores",
            "SourceRowNumber": row_number,
            "CalculationLayer": "Scoring Engine -> Output- Asset Scores",
            "ValidationStatus": "TestRecord" if asset_id == test_asset else "Valid",
            "IsTestRecord": "true" if asset_id == test_asset else "false",
        })
        scores.append(record)

    risk_rows = sheets["Output- Site Risk Scores"]
    risk_header, risk_key_col = find_header(risk_rows, "Site No.")
    risk_headers = header_map(risk_rows, risk_header)
    risk_fields = [
        ("SiteNo", "Site No."), ("OverallRiskScore", "Overall Score"),
        ("NumberItemsAtThreshold", "Number of Items At or Greater than Threshold Above"),
        ("GeneratorScore", "Generator"), ("UPSScore", "UPS"),
        ("UtilityScore", "Utility"), ("CoolingScore", "Cooling"),
        ("FireProtectionScore", "Fire Protection"), ("OtherScore", "Other"),
    ]
    risks: list[dict[str, object]] = []
    for row_number, row in enumerate(risk_rows[risk_header:], risk_header + 1):
        site_no = text(row, risk_key_col)
        if not valid_site(site_no, site_keys):
            continue
        record = {model_name: text(row, risk_headers.get(source_name, 0)) for model_name, source_name in risk_fields}
        record.update({
            "SourceWorkbook": SOURCE_NAME,
            "SourceSheet": "Output- Site Risk Scores",
            "SourceRowNumber": row_number,
            "CalculationLayer": "Transpose Actual Adj -> Output- Site Risk Scores",
            "ValidationStatus": "Valid",
        })
        risks.append(record)

    exceptions: list[dict[str, object]] = []
    for asset in assets:
        if asset["IsTestRecord"] == "true":
            exceptions.append({"ExceptionType": "TestRecord", "BusinessKey": asset["AssetId"], "SiteNo": asset["SiteNo"], "SourceSheet": asset["SourceSheet"], "SourceRowNumber": asset["SourceRowNumber"], "Details": "Excluded from governed portfolio measures"})
        if asset["SiteNo"] not in site_keys and asset["SiteNo"] != "SLC05":
            exceptions.append({"ExceptionType": "UnmappedSite", "BusinessKey": asset["AssetId"], "SiteNo": asset["SiteNo"], "SourceSheet": asset["SourceSheet"], "SourceRowNumber": asset["SourceRowNumber"], "Details": "Asset site key is not in source site master"})
    for row in scores:
        if row["SiteNo"] == "SLC05":
            exceptions.append({"ExceptionType": "RestoredSiteScoreContext", "BusinessKey": row["AssetId"], "SiteNo": "SLC05", "SourceSheet": row["SourceSheet"], "SourceRowNumber": row["SourceRowNumber"], "Details": "Score retained; site restored from asset evidence"})

    spof_rows = sheets["Entry- Site SPOF Data"]
    questions: list[dict[str, object]] = []
    for row_number, row in enumerate(spof_rows[29:], 30):
        question_id = text(row, 1)
        question = text(row, 2)
        if not question_id or not question:
            continue
        questions.append({
            "SPOFQuestionId": question_id,
            "SPOFQuestion": question,
            "SPOFCategory": "",
            "SourceWorkbook": SOURCE_NAME,
            "SourceSheet": "Entry- Site SPOF Data",
            "SourceRowNumber": row_number,
            "ValidationStatus": "Valid",
        })

    observations: list[dict[str, object]] = []
    group_starts = [column for column in range(7, 283) if text(spof_rows[23], column) and text(spof_rows[26], column) == "Yes"]
    for row_number, row in enumerate(spof_rows[29:], 30):
        question_id = text(row, 1)
        question = text(row, 2)
        if not question_id or not question:
            continue
        for start in group_starts:
            markers = [text(row, start + offset) for offset in range(3)]
            selected = [label for label, marker in zip(("Yes", "No", "N/A"), markers) if marker.lower() == "x"]
            observations.append({
                "SiteNo": text(spof_rows[23], start),
                "SPOFQuestionId": question_id,
                "AnswerValue": selected[0] if len(selected) == 1 else "|".join(selected) if selected else "Blank",
                "OriginalMarker": "|".join(marker for marker in markers if marker),
                "DetailedComments": text(row, start + 3),
                "SourceWorkbook": SOURCE_NAME,
                "SourceSheet": "Entry- Site SPOF Data",
                "SourceRowNumber": row_number,
                "SourceColumnStart": start,
                "SourceColumnEnd": start + 3,
                "ValidationStatus": "Valid" if len(selected) == 1 else "MultipleAnswers" if len(selected) > 1 else "Blank",
            })

    controls = [
        {"ControlName": "ReplacementScoreThreshold", "ControlValue": "50.0", "Unit": "score", "SourceSheet": "Costs and Scoring", "SourceCell": "D62"},
        {"ControlName": "NewEquipmentBaseScore", "ControlValue": "15.0", "Unit": "score", "SourceSheet": "Costs and Scoring", "SourceCell": "D63"},
        {"ControlName": "ChartMidScore", "ControlValue": "32.5", "Unit": "score", "SourceSheet": "Costs and Scoring", "SourceCell": "D64"},
        {"ControlName": "YearlyInflation", "ControlValue": "0.035", "Unit": "rate", "SourceSheet": "Costs and Scoring", "SourceCell": "D65"},
        {"ControlName": "OverallCostCorrectionFactor", "ControlValue": "0.6", "Unit": "multiplier", "SourceSheet": "Costs and Scoring", "SourceCell": "D66"},
        {"ControlName": "EquipmentSizeExponent", "ControlValue": "0.8", "Unit": "exponent", "SourceSheet": "Costs and Scoring", "SourceCell": "G15:G49"},
        {"ControlName": "SiteRiskThreshold", "ControlValue": "7.0", "Unit": "score", "SourceSheet": "Output- Site Risk Scores", "SourceCell": "D12"},
    ]
    for control in controls:
        control.update({"SourceWorkbook": SOURCE_NAME, "CalculationVersion": "V1 workbook-derived", "ValidationStatus": "VerifiedInput"})

    write_csv("dim_site.csv", sites, list(sites[0]))
    write_csv("dim_asset.csv", assets, list(assets[0]))
    write_csv("fact_asset_score.csv", scores, list(scores[0]))
    write_csv("fact_site_risk_score.csv", risks, list(risks[0]) if risks else ["SiteNo"])
    write_csv("fact_validation_exception.csv", exceptions, ["ExceptionType", "BusinessKey", "SiteNo", "SourceSheet", "SourceRowNumber", "Details"])
    write_csv("dim_spof_question.csv", questions, list(questions[0]) if questions else ["SPOFQuestionId"])
    write_csv("fact_spof_observation.csv", observations, list(observations[0]) if observations else ["SiteNo"])
    write_csv("dim_model_control.csv", controls, list(controls[0]))
    print(f"Wrote {len(sites)} DimSite rows, {len(assets)} DimAsset rows, {len(scores)} FactAssetScore rows, {len(risks)} FactSiteRiskScore rows, {len(questions)} SPOF questions, {len(observations)} SPOF observations, {len(controls)} controls, and {len(exceptions)} validation exceptions to {OUTPUT}")


if __name__ == "__main__":
    main()
