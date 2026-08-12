---
name: research-question-audit
description: Audit whether a research plan, experiment, model, dataset, evaluation, or scientific claim remains aligned with the governing research question and frozen protocol. Use before major experimental stages, when inputs or targets change, when interpreting results, or whenever research-question drift is possible.
---

# Research Question Audit

## Purpose

Detect research-question drift before work proceeds.

When a frozen research question, protocol, decision record, experiment plan, or other governing artifact exists, treat it as authoritative unless the user explicitly requests that it be revised or refrozen.

Do not silently rewrite, broaden, narrow, reinterpret, or improve a frozen research question.

## Workflow

1. Locate the governing research artifacts:
   - frozen research question
   - technical or experimental protocol
   - hypotheses
   - decision records
   - dataset and split definitions
   - planned inference-time inputs
   - prediction target
   - evaluation population
   - primary metrics
   - intended scientific claim
2. State the frozen research question exactly or as a faithful one-sentence paraphrase. Clearly identify the source.
3. Reconstruct the current proposed or completed experiment: training inputs, supervision, inference-time inputs, prediction target, spatial or temporal scope, evaluation population, primary metrics, assumptions, and intended claim.
4. Compare the experiment against the governing protocol dimension by dimension.
5. Classify every difference as implementation detail, protocol-consistent extension, unresolved ambiguity, material research-question drift, or explicit approved refreeze.
6. Pay special attention to changes that alter information available at inference time, predicted quantity, supervision, evaluation population, success metric, or scientific conclusion.
7. Do not treat a scientifically interesting experiment as aligned merely because it uses the same dataset, model family, study area, or general topic.
8. If required governing artifacts cannot be found, do not invent them. Report the missing authority and stop the drift audit at UNKNOWN.

## Gate Decision

Return exactly one primary decision:

- `PASS` — the experiment answers the frozen research question without material protocol drift.
- `HOLD_RESEARCH_QUESTION_REFREEZE` — the experiment changes the scientific task or depends on an unresolved reinterpretation that requires explicit approval.
- `FAIL_PROTOCOL_VIOLATION` — the experiment contradicts a governing frozen protocol and cannot be treated as compliant.
- `UNKNOWN_MISSING_GOVERNING_ARTIFACT` — alignment cannot be established from available evidence.

Do not convert HOLD, FAIL, or UNKNOWN into PASS through inference or convenience.

## Output

Return:

1. Governing research question and source
2. Current experiment definition
3. Alignment matrix:

| Dimension | Frozen | Current | Status | Evidence |
|---|---|---|---|---|
| Research question | | | | |
| Training information | | | | |
| Inference-time information | | | | |
| Target | | | | |
| Supervision | | | | |
| Evaluation population | | | | |
| Primary metric | | | | |
| Scientific claim | | | | |

4. Material deviations
5. Unresolved ambiguities
6. Gate decision
7. Required action before proceeding

Never propose a revised frozen question unless the user explicitly asks to refreeze or redesign the research question.

## Example Prompt

`$research-question-audit Compare planned experiment B1 with protocol.md. Verify inference-time inputs, target, supervision, evaluation population, primary metric, and permitted claim; return exactly one gate decision.`

For a high-consequence stage transition, invoke this Skill explicitly. Do not rely only on automatic matching.
