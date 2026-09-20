from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "semantic-model" / "V1_TMDL_PACKAGE"
target = ROOT / "semantic-model" / "V1_TMDL_SCHEMA_PACKAGE"
target.mkdir(parents=True, exist_ok=True)

for path in source.glob("*.tmdl"):
    content = path.read_text(encoding="utf-8")
    if path.name != "model.tmdl" and path.name != "relationships.tmdl":
        content = re.sub(r"\npartition [\s\S]*", "\n", content, count=1)
    (target / path.name).write_text(content, encoding="utf-8")

print(f"Created schema-only package at {target}")
