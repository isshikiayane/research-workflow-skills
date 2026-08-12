---
name: experiment-runner
description: Run reproducible research experiments under an explicit governing protocol with frozen inputs, splits, metrics, seeds, environment capture, isolated outputs, audit gates, artifacts, and resumability. Use when executing planned research experiments or experiment matrices.
---

# Experiment Runner

## Purpose

Execute experiments reproducibly without silently changing the scientific question, evaluation protocol, or information boundaries. Execution is subordinate to the governing research protocol.

## Preflight

Before a confirmatory or protocol-governed experiment:

1. Locate the research question, experiment protocol, hypotheses, dataset version, split manifest, target definition, allowed inference-time inputs, preprocessing specification, baseline, primary metrics, stopping rule, and test/blind-test policy.
2. Verify required upstream quality gates where applicable: research-question alignment, data-leakage audit, geospatial-data QC, and project-specific preflight checks. Use the relevant audit skill when available.
3. If a required gate is HOLD, FAIL, INVALID, UNKNOWN, or absent when the protocol requires it, do not start the confirmatory experiment. Return `RUN_BLOCKED` with blocking evidence.

## Frozen Dimensions

Never silently change the research question, inference-time inputs, target, supervision, dataset version, split manifest, preprocessing, model-selection policy, baselines, primary metrics, stopping rule, test policy, or blind-test policy. Record an explicitly approved amendment before any change.

## Execution

1. Create a unique experiment ID and isolated output directory.
2. Capture the command, resolved configuration, code revision or source hash, dataset and split identifiers/hashes, environment, hardware, random seeds, and input checksums where practical.
3. Run only the approved training, validation, and checkpoint-selection process. Do not inspect or tune on protected test or blind-test data.
4. Preserve logs, configurations, checkpoints, metrics, failures, and resumption state. Label smoke, rehearsal, exploratory, and formal runs truthfully.
5. On interruption or failure, preserve evidence and report the actual state; do not infer completion from partial artifacts.

## Gate Decision

Return exactly one primary execution status:

- `RUN_COMPLETE` — the approved run completed and required execution artifacts were captured; this does not validate scientific claims.
- `RUN_BLOCKED` — a required gate or governing artifact blocked execution.
- `RUN_FAILED` — execution started but did not complete successfully.
- `RUN_INCOMPLETE_ARTIFACTS` — execution ended but required reproducibility artifacts are missing.

Only `RUN_COMPLETE` may proceed to `experiment-audit`; it is not equivalent to `VALID`.

## Output

Return experiment ID; governing protocol and upstream gates; exact command; frozen-dimension record; environment and seed capture; output paths; result summary; execution status; and required next action.

## Reference and Example Prompt

Read [the end-to-end gate-chain example](references/e2e-gate-chain.md) when starting a protocol-governed research stage.

`$experiment-runner Run B1 only if protocol.md and the current research-question, leakage, and geospatial QC reports are all PASS. Freeze config, split hash, data identifiers, seed, environment, command, logs, checkpoint, and metrics; never access blind-test data.`
