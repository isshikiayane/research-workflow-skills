---
name: research-evidence-review
description: Review whether experimental results support a proposed scientific claim, with explicit evidence, uncertainty, alternatives, and reporting limits. Use before writing papers, reports, abstracts, figures, or conclusions from research experiments.
---

# Research Evidence Review

1. State each proposed claim and its scope.
2. Require a corresponding `VALID` experiment audit; otherwise classify the claim as not ready for evidentiary review.
3. Trace each claim to metrics, populations, baselines, uncertainty, and artifacts.
4. Consider statistical uncertainty, ablations, external validity, confounders, and alternative explanations.
5. Classify every claim as `SUPPORTED`, `PARTIALLY_SUPPORTED`, `PRELIMINARY`, `UNSUPPORTED`, or `CONTRADICTED`.
6. State safe wording and prohibited overclaims. Do not convert exploratory or smoke evidence into a formal scientific result.

## Example Prompt

`$research-evidence-review Given experiment B1's VALID audit, determine whether its primary metric and comparable baseline support the stated claim. Report uncertainty, alternative explanations, safe wording, and one claim classification.`

For a paper, report, or public claim, invoke this Skill explicitly.
