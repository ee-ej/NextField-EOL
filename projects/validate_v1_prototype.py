from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "reports" / "prototype"


def load(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    sites = load("dim_site.csv")
    assets = load("dim_asset.csv")
    scores = load("fact_asset_score.csv")
    risks = load("fact_site_risk_score.csv")
    questions = load("dim_spof_question.csv")
    observations = load("fact_spof_observation.csv")
    controls = load("dim_model_control.csv")
    exceptions = load("fact_validation_exception.csv")

    site_keys = {row["SiteNo"] for row in sites}
    asset_keys = {row["AssetId"] for row in assets}
    question_keys = {row["SPOFQuestionId"] for row in questions}
    score_keys = {row["AssetId"] for row in scores}
    risk_keys = {row["SiteNo"] for row in risks}

    checks = {
        "site_keys_unique": len(site_keys) == len(sites),
        "asset_keys_unique": len(asset_keys) == len(assets),
        "score_keys_unique": len(score_keys) == len(scores),
        "question_keys_unique": len(question_keys) == len(questions),
        "asset_score_keys_resolve": score_keys <= asset_keys,
        "asset_site_keys_resolve": all(row["IsTestRecord"] == "true" or row["SiteNo"] in site_keys for row in assets),
        "risk_site_keys_resolve": risk_keys <= site_keys,
        "spof_question_keys_resolve": all(row["SPOFQuestionId"] in question_keys for row in observations),
        "spof_site_keys_resolve": all(row["SiteNo"] in site_keys for row in observations),
        "slc05_restored": sum(row["SiteNo"] == "SLC05" and row["IsRestoredRecord"] == "true" for row in sites) == 1,
        "test_asset_flagged": sum(row["AssetId"] == "7057" and row["IsTestRecord"] == "true" for row in assets) == 1,
        "expected_controls": len(controls) == 7,
        "expected_exceptions": len(exceptions) == 43,
    }
    for name, passed in checks.items():
        print(f"{name}={'PASS' if passed else 'FAIL'}")
    if not all(checks.values()):
        raise SystemExit(1)
    print("V1 prototype referential-integrity validation passed.")


if __name__ == "__main__":
    main()
