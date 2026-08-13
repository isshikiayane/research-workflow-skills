---
name: fengshui-cultural-analysis
description: Perform reproducible GIS-based cultural interpretation of traditional fengshui spatial concepts. Use when a user asks to interpret a location, site, terrain, water relationship, enclosure, ridge, valley, or related spatial pattern through traditional fengshui concepts while keeping GIS measurements, cultural mapping, uncertainty, and limitations separate. This skill does not predict real fortune, prove fengshui causality, or give definite auspiciousness.
---

# Fengshui Cultural Analysis

## Overview

Use objective spatial measurements as evidence for a transparent cultural interpretation. The result is an explicitly heuristic cultural reading, not divination, a scientific causal model, or a site-selection oracle.

Compute and report GIS measurements first. Map those measurements to named traditional concepts only after the measurements are structured. Write the human-readable interpretation last, and state what the data cannot establish.

## Workflow

1. Define the location or analysis extent, analysis scale, orientation convention, available layers, and the cultural lens. Record assumptions.
2. Run only the data-quality checks needed by the metrics that will be used. Check CRS and horizontal units, vertical units and datum when known, nodata, raster alignment, coverage, DTM versus DSM, and water-layer date or provenance.
3. Prefer mature tools such as GDAL, rasterio, GeoPandas, Shapely, WhiteboxTools, GRASS GIS, or SAGA GIS. Do not reimplement established GIS algorithms in this skill.
4. Calculate a structured spatial_metrics object before applying cultural language. Every metric should include units, source, method or tool, parameters, coverage, and a missing-data note when relevant.
5. Use references/cultural-mapping.md to map measurements to cultural concepts. Keep the measurement statement, cultural interpretation, and non-claim boundary visibly separate.
6. Use references/scoring-and-sensitivity.md and scripts/compute_heuristic_index.py for a transparent heuristic index. The index is a normalized summary of declared components, not a probability or prediction.
7. Recalculate under the documented sensitivity scenarios. Report which conclusions are stable, conditional, or dependent on a missing or weakly supported component.
8. Validate the required output contract with references/output-schema.md and scripts/validate_output.py before presenting results.

## Minimum quality policy

- Do not use a horizontal CRS as proof that vertical units or vertical datum are compatible.
- Do not treat nodata as elevation, and do not silently interpolate large missing areas.
- Treat aspect as circular data. Record the north convention and whether the calculation is planar or geographic.
- Treat a DSM as a surface model: buildings and vegetation can affect terrain, visibility, and hydrology.
- Check alignment and resolution before combining rasters. Check geometry validity and CRS before spatial joins.
- A failed optional layer should normally downgrade only the affected metric. Continue with the remaining metrics and mark the degradation.
- Hold the analysis only when a necessary input or a unit/CRS incompatibility makes the requested metric unreliable.
- Never describe the output as a confirmed favorable or unfavorable fate, physical qi, health/economic outcome, or scientific causation.

## Output contract

Return a structured object with at least these top-level fields:

- data_quality
- spatial_metrics
- cultural_interpretation
- heuristic_cultural_index
- sensitivity
- uncertainty
- limitations

Include not_prediction: true and preserve metric provenance. The human-readable explanation must be traceable to the structured fields. Missing metrics and degraded checks must remain visible.

## Bundled helpers

The bundled scripts are deliberately narrow:

- compute_heuristic_index.py combines already-computed normalized components; it is not a GIS engine.
- validate_output.py checks the minimum output contract and index bounds.

Read only the reference files needed for the selected metrics and cultural lens.

