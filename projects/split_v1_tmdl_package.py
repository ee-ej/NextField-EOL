from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "semantic-model" / "V1_MODEL_TMDL_DRAFT.tmdl"
package = ROOT / "semantic-model" / "V1_TMDL_PACKAGE"
text = source.read_text(encoding="utf-8")

model_match = re.search(r"\A(.*?)(?=^table )", text, re.MULTILINE | re.DOTALL)
if not model_match:
    raise ValueError("Model header not found")
(package / "model.tmdl").write_text(model_match.group(1).strip() + "\n", encoding="utf-8")

table_matches = list(re.finditer(r"^table ([A-Za-z0-9_]+)\n", text, re.MULTILINE))
partition_matches = list(re.finditer(r"^partition ([A-Za-z0-9_]+) = m\n", text, re.MULTILINE))
relationship_match = re.search(r"^relationship ", text, re.MULTILINE)
end_for_tables = partition_matches[0].start() if partition_matches else (relationship_match.start() if relationship_match else len(text))
partition_end = relationship_match.start() if relationship_match else len(text)
partitions = {}
for index, match in enumerate(partition_matches):
    end = partition_matches[index + 1].start() if index + 1 < len(partition_matches) else partition_end
    partitions[match.group(1)] = text[match.start():end].rstrip()
for index, match in enumerate(table_matches):
    start = match.start()
    end = table_matches[index + 1].start() if index + 1 < len(table_matches) else end_for_tables
    table_text = text[start:end].rstrip() + "\n"
    name = match.group(1)
    if name in partitions:
        table_text += "\n" + partitions[name] + "\n"
    (package / f"{name}.tmdl").write_text(table_text, encoding="utf-8")

if relationship_match:
    (package / "relationships.tmdl").write_text(text[relationship_match.start():].strip() + "\n", encoding="utf-8")

print(f"Created model.tmdl, {len(table_matches)} table documents, and relationships.tmdl in {package}")
