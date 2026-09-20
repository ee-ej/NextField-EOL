# V1 TMDL Package

This folder packages the local V1 semantic-model schema draft for Power BI tooling import review.

- `model.tmdl` is copied from `../V1_MODEL_TMDL_DRAFT.tmdl`.
- Source partitions point to the generated V1 prototype CSVs under `reports/prototype/`.
- V2 is excluded.
- No import, Fabric deployment, or remote write has been performed.

Before import, validate the package with the Power BI TMDL tooling and confirm whether the local relative CSV paths resolve from the intended model location.

Import status: the Power BI importer parses the model header and table documents, but rejects the current partition declaration inside a table document. The schema draft and generated CSVs remain valid local artifacts; the remaining packaging task is to use the importer's partition-document layout, which was not inferred or applied automatically.
