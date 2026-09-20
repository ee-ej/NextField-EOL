# V1 Validated TMDL Export

This folder was exported from the offline Power BI model connection after schema validation and measure creation.

- Model: `NextFieldEOL_V1_LocalPrototype`
- Connection: `NextFieldEOL_V1_SchemaOnly_v2`
- Tables: 8
- Relationships: 5
- Measures: 15
- Mode: Import
- V2: excluded
- Fabric publication: not performed

Partition status: eight Import/M partitions were added to the offline model and are present in `NoData` state. The exported folder loads successfully as a local model, but the modeling tool cannot refresh this disconnected object: `RefreshWithAPI` requires a Fabric connection, while `RefreshWithXMLA` is read-only for the disconnected model. Data population therefore requires a connected Power BI Desktop model or another supported local runtime.

Measure layer: 15 `Ready` measures cover portfolio counts, replacement priority, capital exposure, site risk, SPOF observation coverage, coverage percentages, and validation exceptions.

The table definitions are under `tables/`. This export validates the local schema and measure layer; it does not contain populated data partitions because the schema-only connection was used.
