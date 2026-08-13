# GIS metric and data-quality reference

## Data-quality checks

Record the following in data_quality when relevant:

| Check | Minimum record |
| --- | --- |
| Horizontal CRS | CRS identifier, projected/geographic status, and horizontal units |
| Vertical information | vertical units and datum if known; otherwise unknown |
| Elevation source | DTM, DSM, LiDAR, photogrammetry, or other source; acquisition date if available |
| Nodata | nodata value, proportion or area, and treatment |
| Grid | pixel size, extent, alignment, resampling method, and resolution compatibility |
| Coverage | fraction of the requested extent covered by each layer |
| Vector geometry | validity, duplicate or empty geometries, CRS, and spatial index status |
| Water layer | source, date, geometry type, and whether it represents perennial or event water |

These checks are metric-specific. A missing water layer can remove or downgrade water metrics without blocking terrain-only metrics. Unknown vertical datum should be disclosed and may prevent absolute elevation comparisons.

## Metric definitions

| Metric | Operational definition | Main caveat |
| --- | --- | --- |
| Elevation | Summary or distribution of elevation in the analysis extent and directional sectors | Units and vertical datum must be known for absolute comparisons |
| Slope | Local gradient, preferably in a projected CRS with compatible horizontal and vertical units | Geographic degrees and vertical-unit mismatch can bias slope |
| Aspect | Circular direction of steepest descent or ascent according to the chosen GIS convention | Mean aspect must use circular statistics; flat cells need a policy |
| TPI or relief | Elevation relative to a declared neighborhood or local relief range | Scale and radius change the interpretation |
| Curvature or roughness | Surface form or local elevation variability from a declared neighborhood | Resolution-sensitive and not a direct cultural variable |
| Ridge and valley proxies | Terrain classification derived from TPI, curvature, flow accumulation, or a documented geomorphometry method | Thresholds and scale are model choices |
| Flow direction and accumulation | Hydrologic routing from a conditioned elevation surface and a declared algorithm | Conditioning and threshold choices materially affect results |
| Watershed or convergence | Catchment, flow concentration, or local drainage convergence within the analysis extent | Boundary truncation can create artificial edge effects |
| Water relationship | Distance, visibility, direction, or elevation relation to a supplied water layer | Water presence is not a claim about prosperity or safety |
| Enclosure or openness | Viewshed, horizon, visible-area, or directional obstruction proxy from a declared observer height and radius | A DSM can encode vegetation/buildings; visibility is not wind measurement |

## Tool routing

Prefer existing implementations:

- GDAL or rasterio for raster metadata, masking, reprojection, resampling, and windowed reads.
- GeoPandas and Shapely for vector CRS, geometry validation, spatial joins, distance, and clipping.
- WhiteboxTools, GRASS GIS, or SAGA GIS for terrain derivatives, hydrologic conditioning, flow, watershed, and terrain classification.
- A documented viewshed implementation for enclosure or openness. Record observer height, target height, radius, and surface model.

Do not replace these tools with ad hoc slope, flow, watershed, or visibility implementations in this skill. If a tool is unavailable, either use an equivalent documented implementation or omit/degrade that metric.

## Reproducibility record

For every metric, record source path or identifier, source checksum where feasible, tool and version, algorithm, parameters, units, CRS, mask/extent, nodata treatment, and output coverage. Keep GIS measurements in spatial_metrics; do not place cultural labels in the metric value itself.

