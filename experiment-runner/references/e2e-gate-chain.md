# Example: Protocol-governed flood-depth experiment

Use this example only as a pattern. Replace all names, paths, criteria, and evidence with the actual governing protocol.

## 1. Freeze the task

The protocol defines one target, event-disjoint train/validation/test splits, legal inference-time inputs, primary metric, and blind-test rule. Store its path and revision in the experiment record.

## 2. Run the three admission audits explicitly

```text
$research-question-audit Compare planned run B1 with protocol.md and report one gate decision.
$data-leakage-audit Audit split_manifest.csv, preprocessing, normalization, checkpoint selection, and protected-event access before B1.
$geospatial-data-qc Check DEM, extent mask, observations, and labels for CRS, vertical datum, units, grid alignment, nodata, and event-time consistency.
```

Proceed only when all three primary decisions are `PASS`. Any HOLD, FAIL, INVALID, UNKNOWN, or missing required report produces `RUN_BLOCKED`; it is not a reason to weaken the protocol.

## 3. Execute without changing frozen dimensions

```text
$experiment-runner Run B1 using protocol.md and the three PASS audit reports. Capture the resolved config, split hash, data identifiers, source revision, seed, environment, command, logs, checkpoint, and validation metrics. Do not access blind-test data.
```

`RUN_COMPLETE` only establishes that the planned run finished with its required execution artifacts.

## 4. Audit the completed run

```text
$experiment-audit Audit B1 against protocol.md, the three upstream reports, run manifest, logs, config, split hash, checkpoint-selection evidence, and metrics.
```

Only `VALID` allows evidence review. `HOLD_AUDIT_EVIDENCE`, `INVALID_EXECUTION`, and `UNKNOWN_AUDIT_INSUFFICIENT_EVIDENCE` keep the result out of formal claims.

## 5. Review the claim

```text
$research-evidence-review Assess whether the VALID B1 result supports the claim that method B improves the frozen primary metric over the protocol baseline on the defined evaluation population.
```

Report the claim classification, uncertainty, comparison conditions, alternative explanations, and safe wording. A valid experiment may still yield `PRELIMINARY` or `UNSUPPORTED` evidence.
