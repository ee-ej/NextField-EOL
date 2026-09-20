# V1 TMDL Schema Package

This package contains the importer-validated V1 table and relationship schema without data partitions.

Validation result:

- Imported offline as `NextFieldEOL_V1_SchemaOnly`.
- Retrieved model name: `NextFieldEOL_V1_LocalPrototype`.
- Model mode: `Import`.
- Culture: `en-US`.
- Table and relationship parsing succeeded.
- The imported model reports all 8 prototype tables, including the corrected 8-column `DimSite` definition.

The data-backed package remains under `V1_TMDL_PACKAGE`. Its partition declarations require the importer-specific partition-document layout and were not applied here. No Fabric deployment or remote write was performed.
