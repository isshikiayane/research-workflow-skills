---
name: data-leakage-audit
description: Audit ML and research pipelines for train-validation-test contamination, temporal and spatial leakage, target leakage, duplicate or group leakage, proxy leakage, preprocessing leakage, oracle information, and evaluation contamination. Use before experiments, after pipeline changes, and before accepting reported results.
---

# Data Leakage Audit

## Purpose

Determine whether an experiment preserves the information boundaries required for a valid evaluation.

Do not describe an experiment as leakage-free merely because no obvious leakage was found.

## Workflow

1. Identify the governing prediction setting: prediction or inference time; information legally available at inference; target construction; train/validation/test, grouping, temporal, spatial, blind-test, and project-specific leakage policies.
2. Locate and inspect, where available: raw-data inventory; split manifests; IDs and group identifiers; preprocessing, feature-generation, label-generation, interpolation, aggregation, normalization, augmentation, model-selection, threshold-tuning, checkpoint-selection, and evaluation code.
3. Verify identity and group isolation: exact ID overlap; duplicate and near-duplicate observations; entity/group, event, locality/site, temporal, and spatial overlap where prohibited.
4. Verify transformation boundaries: splitting occurs before learned transformations; statistics use only authorized training data; imputation, encoding, feature selection, PCA, clustering, learned preprocessing, and augmentation do not access held-out data; interpolation, smoothing, neighborhood, and graph operations do not incorporate held-out targets.
5. Verify target and proxy isolation: target values and target-derived rasters, masks, extents, statistics, labels, rankings, and proxies are not used unless explicitly legal; post-event, future, and oracle information is checked against deployment conditions.
6. Verify evaluation isolation: validation/test data do not affect training, hyperparameter tuning, early stopping, checkpoint or threshold selection, preprocessing decisions; blind-test observations are not manually inspected before final evaluation.
7. For geospatial research, explicitly check point identity, coordinate duplicates, raster cells or interpolation surfaces influenced by held-out observations, neighborhoods crossing forbidden boundaries, event/locality dependence, target-derived extent or mask information, and temporal mismatch between observations and predictors.
8. Prefer reproducible checks over qualitative judgment. Record commands, scripts, queries, counts, hashes, or examples whenever possible.

## Severity

Classify findings as:

- Critical — confirmed contamination that compromises evaluation validity
- High — probable leakage or an evaluation-boundary violation
- Medium — leakage risk requiring additional verification
- Low — weakness unlikely to change validity but worth documenting

## Gate Decision

Return exactly one primary decision:

- `PASS` — relevant leakage boundaries were inspected and no material violation was found.
- `HOLD_LEAKAGE_RISK` — material leakage risk remains unresolved.
- `INVALID_CONTAMINATED` — confirmed contamination invalidates the affected evaluation.
- `UNKNOWN_INSUFFICIENT_EVIDENCE` — required artifacts or boundaries could not be inspected.

Unknown is not PASS.

## Output

Return evaluation boundary definition; artifacts inspected; a matrix containing check, evidence, severity, affected stage/data, and status; contamination paths; affected results; gate decision; remediation; and uninspected artifacts.

If contamination is confirmed, explicitly state which existing results can no longer be treated as valid evidence.

## Reusable Check

Use `scripts/check_split_overlap.py` when split inventories are CSV files. It reports exact ID, optional group, and rounded-coordinate overlap candidates without modifying inputs. It is not proof of spatial independence or a leakage-free result.

```text
python scripts/check_split_overlap.py --train train.csv --validation val.csv --test test.csv --id-column sample_id --group-column event_id --x-column x --y-column y --fail-on-overlap
```

## Example Prompt

`$data-leakage-audit Audit split_manifest.csv, preprocessing, normalization, interpolation, checkpoint selection, and blind-test access for B1. Quantify overlap and return exactly one gate decision.`

For a high-consequence stage transition, invoke this Skill explicitly. Do not rely only on automatic matching.
