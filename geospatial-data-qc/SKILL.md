---
name: geospatial-data-qc
description: Quality-check raster, vector, point, terrain, remote-sensing, and other geospatial datasets and pipelines for CRS, datum, units, grid alignment, resolution, temporal consistency, geometry validity, coverage, nodata, spatial joins, and cross-source compatibility. Use before geospatial analysis, ML experiments, reprojection, raster stacking, or spatial evaluation.
---

# Geospatial Data QC

## Purpose

Determine whether geospatial inputs are internally valid and mutually compatible for the intended analysis.

Preserve original data. Never silently repair, reproject, resample, shift, fill, or reinterpret data.

## Workflow

1. Inventory every source: provenance, format, geometry/raster type, CRS, horizontal and vertical datum, units, expected extent, temporal coverage, nodata, and resolution or positional precision.
2. For raster data, inspect CRS, dimensions, pixel size, affine transform, grid origin, bounds, resolution, nodata, dtype, bands, units, mask convention, orientation, and alignment.
3. Before stacking or pixel-wise comparison, verify intentionally transformed CRS, extent, resolution, grid alignment, resampling method, categorical versus continuous interpolation, and consistent nodata handling.
4. For elevation, terrain, water-level, depth, or height, verify horizontal and vertical datum, semantics, units, reference surface, sign convention, and plausible range. Never assume vertical compatibility solely because horizontal CRS matches.
5. For remote sensing, inspect acquisition time relative to event timing, sensor/band/polarization, preprocessing lineage, resolution, reprojection/resampling history, and invalid pixels.
6. For point/vector data, inspect coordinate order, geometry validity, null/empty or impossible geometries, duplicates, coverage, outliers, spatial-join cardinality, boundary effects, and unmatched features.
7. For point-to-raster relationships, verify coverage, intended-cell mapping, nodata, correct CRS/transform extraction, and duplicate points/cells.
8. Compare cross-source temporal and spatial consistency.
9. Inspect representative samples visually whenever metadata cannot establish alignment, geometry, masks, or offsets confidently.
10. Quantify defects instead of reporting only qualitative observations.

## Gate Decision

Return exactly one primary decision:

- `PASS` — relevant spatial, temporal, unit, datum, and alignment checks passed.
- `HOLD_DATA_QC` — one or more material compatibility issues remain unresolved.
- `FAIL_DATA_INCOMPATIBLE` — confirmed incompatibility makes the intended analysis invalid without correction.
- `UNKNOWN_INSUFFICIENT_METADATA` — required metadata or source information is unavailable.

## Output

Return dataset inventory; CRS/datum/unit and raster-alignment matrices where applicable; temporal consistency; quantified defects; affected artifacts; severity and likely cause; gate decision; recommended repair, quarantine, or verification. Propose, never silently perform, corrections that alter original data.

## Reusable Check

Use `scripts/inspect_raster_metadata.py` to record raster metadata and compare candidate rasters with a reference without modifying inputs. It requires `rasterio`; metadata agreement does not prove vertical-datum, semantic, or temporal compatibility.

```text
python scripts/inspect_raster_metadata.py dem.tif extent.tif label.tif --reference dem.tif --strict
```

## Example Prompt

`$geospatial-data-qc Check the DEM, flood extent, labels, and observation points for CRS, horizontal and vertical datum, units, pixel alignment, nodata, temporal consistency, and point-to-raster extraction correctness. Return exactly one gate decision.`

For a high-consequence stage transition, invoke this Skill explicitly. Do not rely only on automatic matching.
