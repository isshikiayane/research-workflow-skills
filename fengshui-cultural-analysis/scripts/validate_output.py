#!/usr/bin/env python3
"""Validate the minimum fengshui-cultural-analysis output contract."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


REQUIRED = {
    "data_quality",
    "spatial_metrics",
    "cultural_interpretation",
    "heuristic_cultural_index",
    "sensitivity",
    "uncertainty",
    "limitations",
}


def _is_unit_interval(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and 0.0 <= float(value) <= 1.0
    )


def validate(payload: Any) -> list[str]:
    errors = []
    if not isinstance(payload, dict):
        return ["output must be an object"]
    missing = sorted(REQUIRED - payload.keys())
    if missing:
        errors.append("missing top-level fields: " + ", ".join(missing))
    if payload.get("not_prediction") is not True:
        errors.append("not_prediction must be true")
    index = payload.get("heuristic_cultural_index")
    if not isinstance(index, dict):
        errors.append("heuristic_cultural_index must be an object")
    else:
        if index.get("value") is not None and not _is_unit_interval(index["value"]):
            errors.append("heuristic_cultural_index.value must be null or in [0, 1]")
        if index.get("scale") != [0.0, 1.0]:
            errors.append("heuristic_cultural_index.scale must equal [0.0, 1.0]")
        if not _is_unit_interval(index.get("coverage")):
            errors.append("heuristic_cultural_index.coverage must be in [0, 1]")
        if not isinstance(index.get("components"), dict):
            errors.append("heuristic_cultural_index.components must be an object")
    for field in ("data_quality", "spatial_metrics", "heuristic_cultural_index", "sensitivity"):
        if field in payload and not isinstance(payload[field], dict):
            errors.append(f"{field} must be an object")
    for field in ("cultural_interpretation", "uncertainty", "limitations"):
        if field in payload and not isinstance(payload[field], list):
            errors.append(f"{field} must be an array")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    errors = validate(payload)
    if errors:
        print("INVALID")
        for error in errors:
            print("- " + error)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

