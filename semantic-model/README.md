# Semantic Model

Reserved for the validated V1-based semantic model representation.

V2 is parked and excluded from the prototype. The starter TMDL remains in `source/` until the local V1 prototype is validated against the approved contract.

Current artifact: [V1 model prototype specification](V1_MODEL_PROTOTYPE_SPEC.md).

Machine-readable schema contract: [V1 model schema](V1_MODEL_SCHEMA.json).

Generated local tables are documented in [the prototype tables README](../reports/prototype/README.md).

Local TMDL draft: [V1 model TMDL draft](V1_MODEL_TMDL_DRAFT.tmdl). It is currently a single-file schema draft; a complete PBIP/TMDL folder is required before Power BI tooling import.

Schema validation package: [V1 TMDL schema package](V1_TMDL_SCHEMA_PACKAGE/README.md). This package imported successfully offline; the data-partition package remains separate pending importer-specific partition packaging.

Validated offline model: [V1 TMDL validated export](V1_TMDL_VALIDATED/README.md). It contains the accepted schema, seven measures, and eight local partition definitions; refresh remains blocked by the disconnected-model limitation.
