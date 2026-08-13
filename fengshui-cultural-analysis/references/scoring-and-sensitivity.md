# Heuristic index, weighting, and sensitivity

## Index meaning

The heuristic_cultural_index is a transparent summary of declared cultural-reading components. It is not a probability, prediction, scientific effect size, or truth value.

Normalize each available component to [0, 1] with a stated direction and transformation. Keep the raw metric and transformation in spatial_metrics or the component provenance. Do not normalize by silently using the blind target, a future event, or an outcome label.

For available components i, use:

    index = sum(weight_i * component_i) / sum(weight_i)

Report the denominator, the component coverage, the weights, and any excluded component. A missing component is not zero. If no weighted component remains, set the index value to null and explain why.

## Weight policy

- Use equal weights by default unless the user supplies a defensible cultural lens.
- If weights are supplied, normalize or report them exactly and explain their interpretation.
- Do not infer weights from observed outcomes in the same analysis.
- Keep constraints and factors separate. A data-quality failure is not a negative cultural factor.
- Report component-level contributions so a reader can see what drives the summary.

## Sensitivity policy

Use one-at-a-time weight perturbations as a minimum local sensitivity check. The bundled helper defaults to plus or minus 20 percent for positive weights. Recompute the index while keeping component values fixed, report the range, and identify whether the qualitative band or ordering changes.

If several components are correlated, say so; one-at-a-time sensitivity does not replace a broader scenario analysis. If an interpretation depends on radius, orientation, DEM/DSM choice, flow threshold, or water date, include those as scenario dimensions when feasible.

## Uncertainty categories

Distinguish:

- measurement uncertainty: resolution, interpolation, nodata, geometry, or algorithm effects;
- model uncertainty: threshold, radius, observer height, conditioning, or weight choices;
- source uncertainty: unknown datum, date, provenance, or incomplete coverage;
- interpretation uncertainty: school, language, context, and non-unique cultural mapping.

Use conditional language such as higher under the selected scale or not assessed because the layer is unavailable. Never convert a heuristic index into definite auspiciousness.

