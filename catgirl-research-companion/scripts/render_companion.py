#!/usr/bin/env python3
"""Presentation-only renderer for immutable structured research results."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


PRESETS = {
    "gentle": {
        "identity": "warm catgirl research companion",
        "role": "explain an existing result clearly and supportively",
        "personality": "patient, encouraging, careful about uncertainty",
        "speakingStyle": "soft, concise, evidence-linked",
        "boundaries": "presentation only; no protected fact changes",
        "opening": "Here is the result as recorded. I will keep its evidence and uncertainty visible, nya.",
    },
    "tsundere": {
        "identity": "prickly but dependable catgirl research companion",
        "role": "point out what the existing result actually says",
        "personality": "direct, vigilant, secretly helpful",
        "speakingStyle": "brief, corrective, restrained playful embarrassment",
        "boundaries": "teasing targets wording or process, never people or facts",
        "opening": "I checked the recorded result. Do not make it sound more certain than it is, okay?",
    },
    "sarcastic": {
        "identity": "dry-witted catgirl research companion",
        "role": "make unsupported certainty and process errors noticeable",
        "personality": "observant, skeptical, technically grounded",
        "speakingStyle": "dry asides followed by the exact evidence-based point",
        "boundaries": "sarcasm targets unjustified claims or workflow friction",
        "opening": "Wonderful, the facts survived the personality filter. Here is what the record actually supports.",
    },
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def fact_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _value_text(value: Any) -> str:
    if value is None:
        return "not recorded"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (int, float, str)):
        return str(value)
    return "recorded in the structured result"


def _summary(facts: dict[str, Any]) -> str:
    fragments = []
    quality = facts.get("data_quality")
    if isinstance(quality, dict) and "status" in quality:
        fragments.append("data-quality status: " + _value_text(quality["status"]))
    index = facts.get("heuristic_cultural_index")
    if isinstance(index, dict) and "value" in index:
        fragments.append("heuristic index: " + _value_text(index["value"]))
    if "uncertainty" in facts:
        fragments.append("uncertainty is recorded")
    if "limitations" in facts:
        fragments.append("limitations are recorded")
    if "conclusion" in facts:
        fragments.append("conclusion: " + _value_text(facts["conclusion"]))
    return "; ".join(fragments) if fragments else "the structured result is recorded without an invented summary"


def render(structured_input: dict[str, Any], style: str) -> dict[str, Any]:
    if style not in PRESETS:
        raise ValueError("unknown style: " + style)
    if not isinstance(structured_input, dict):
        raise TypeError("structured input must be a JSON object")
    protected = copy.deepcopy(structured_input)
    preset = PRESETS[style]
    narrative = preset["opening"] + " Recorded facts: " + _summary(protected) + "."
    identity = {
        key: value
        for key, value in preset.items()
        if key != "opening"
    }
    return {
        "style": style,
        "identity": identity,
        "narrative": narrative,
        "structured_facts": protected,
        "fact_digest": fact_digest(protected),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--style", choices=sorted(PRESETS), default="gentle")
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    structured_input = json.loads(args.input.read_text(encoding="utf-8"))
    result = render(structured_input, args.style)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

