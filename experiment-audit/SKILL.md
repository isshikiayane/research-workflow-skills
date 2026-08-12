---
name: experiment-audit
description: Independently audit completed research experiments for protocol compliance, reproducibility, split integrity, artifact completeness, metric validity, and claim readiness. Use after an experiment run and before results are accepted, compared, reported, or used as scientific evidence.
---

# Experiment Audit

## Purpose

Determine whether a completed experiment can be treated as a valid execution of its governing protocol. Do not rerun, repair, or upgrade a result silently during the audit.

## Preconditions

Accept an upstream `RUN_COMPLETE` only. If the runner reported `RUN_BLOCKED`, `RUN_FAILED`, or `RUN_INCOMPLETE_ARTIFACTS`, preserve that status and do not convert it to valid evidence.

## Workflow

1. Locate the governing protocol, approved amendments, upstream gate reports, run manifest, configuration, logs, code revision, environment, dataset/split identifiers, checkpoints, metrics, and result artifacts.
2. Verify the executed inputs, target, splits, preprocessing, seed, model-selection process, stopping rule, metrics, baseline, and test policy against the governing protocol.
3. Check reproducibility evidence: exact command, configuration, code/data/split identity, environment, seeds, logs, checkpoints, outputs, and metric provenance.
4. Check evaluation integrity: protected data were not used for selection or tuning; metric population and aggregation match the protocol; comparisons use compatible conditions; smoke or rehearsal runs are not represented as formal results.
5. Record missing, inconsistent, or unverifiable evidence and identify affected results.

## Gate Decision

Return exactly one primary decision:

- `VALID` — the completed run is protocol-compliant, sufficiently evidenced, and may proceed to evidence review.
- `HOLD_AUDIT_EVIDENCE` — material evidence or verification remains unresolved.
- `INVALID_EXECUTION` — confirmed protocol, reproducibility, or evaluation violation invalidates the affected result.
- `UNKNOWN_AUDIT_INSUFFICIENT_EVIDENCE` — required artifacts cannot be inspected.

Only `VALID` may be supplied to `research-evidence-review`. VALID confirms execution validity, not the strength of a scientific claim.

## Output

Return the upstream run status, artifact inventory, protocol-compliance matrix, reproducibility matrix, evaluation-integrity findings, affected results, gate decision, and required remediation or next action.

## Example Prompt

`$experiment-audit Audit B1 using protocol.md, the upstream PASS reports, run manifest, config, source revision, split hash, logs, checkpoint-selection evidence, and metrics. Return exactly one audit decision.`

For a high-consequence result acceptance, invoke this Skill explicitly. Do not rely only on automatic matching.
