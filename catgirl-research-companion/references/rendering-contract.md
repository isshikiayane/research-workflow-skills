# Immutable rendering contract

## Input

The renderer accepts one JSON object containing the already computed structured result and one style name. The structured result may contain arbitrary nested objects and arrays.

## Protected data

Make a deep copy before rendering. The output field structured_facts must be semantically equal to the input object. This includes every key and value, not only a selected allow-list. The renderer must not round numbers, reorder meaning, fill nulls, remove empty fields, or add analytical fields inside structured_facts.

For deterministic comparison, fact_digest is the SHA-256 digest of compact JSON with sorted object keys and UTF-8 encoding. The digest is an integrity check, not a substitute for reading the result.

## Output shape

The reference renderer returns:

- style: the selected preset name;
- identity: persona metadata, excluding the natural-language opening;
- narrative: presentation-only prose;
- structured_facts: an unchanged deep copy of the input object;
- fact_digest: the canonical digest of structured_facts.

The narrative can mention values, status, evidence, uncertainty, limitations, and conclusion, but it must obtain them from structured_facts. Do not create a second, edited fact summary and label it as authoritative.

## Research safety

If the input contains a gate failure, degraded status, low evidence level, uncertainty, limitation, or conditional conclusion, the narrative must not present the result as stronger. If a field is absent, do not invent it. A personality style is not permission to interpret a missing value.

