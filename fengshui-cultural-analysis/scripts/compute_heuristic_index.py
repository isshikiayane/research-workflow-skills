#!/usr/bin/env python3
"""Compute a transparent index from precomputed normalized components.

This helper intentionally does not read rasters or implement GIS algorithms.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path
from typing import Any


def _number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _component_value(raw: Any, name: str) -> float:
    if isinstance(raw, dict):
        raw = raw.get("value")
    value = _number(raw, f"component {name}")
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"component {name} must be between 0 and 1")
    return value


def _positive_weight(value: Any, name: str) -> float:
    weight = _number(value, f"weight {name}")
    if weight < 0.0:
        raise ValueError(f"weight {name} must be non-negative")
    return weight


def _index(values: dict[str, float], weights: dict[str, float]) -> float | None:
    active = [(name, values[name], weights.get(name, 1.0)) for name in values]
    active = [(name, value, weight) for name, value, weight in active if weight > 0.0]
    denominator = sum(weight for _, _, weight in active)
    if denominator == 0.0:
        return None
    return sum(value * weight for _, value, weight in active) / denominator


def compute(payload: dict[str, Any]) -> dict[str, Any]:
    raw_components = payload.get("components")
    if not isinstance(raw_components, dict) or not raw_components:
        raise ValueError("components must be a non-empty object")

    values = {
        str(name): _component_value(raw, str(name))
        for name, raw in raw_components.items()
    }
    raw_weights = payload.get("weights", {})
    if not isinstance(raw_weights, dict):
        raise ValueError("weights must be an object")
    weights = {
        name: _positive_weight(raw_weights.get(name, 1.0), name)
        for name in values
    }
    value = _index(values, weights)
    active_weight = sum(weight for weight in weights.values() if weight > 0.0)
    coverage = sum(1 for name, weight in weights.items() if weight > 0.0 and name in values) / len(values)

    contributions = {}
    if value is not None and active_weight:
        contributions = {
            name: (values[name] * weights[name]) / active_weight
            for name in values
            if weights[name] > 0.0
        }

    perturbation = _number(payload.get("perturbation", 0.2), "perturbation")
    if perturbation < 0.0:
        raise ValueError("perturbation must be non-negative")

    scenarios = []
    for name, weight in weights.items():
        if weight <= 0.0:
            continue
        for direction, multiplier in (
            ("low", max(0.0, 1.0 - perturbation)),
            ("high", 1.0 + perturbation),
        ):
            scenario_weights = copy.deepcopy(weights)
            scenario_weights[name] = weight * multiplier
            scenarios.append({
                "component": name,
                "direction": direction,
                "weights": scenario_weights,
                "value": _index(values, scenario_weights),
            })

    scenario_values = [item["value"] for item in scenarios if item["value"] is not None]
    all_values = ([value] if value is not None else []) + scenario_values
    value_range = [min(all_values), max(all_values)] if all_values else [None, None]
    spread = (value_range[1] - value_range[0]) if all_values else None
    if value is None:
        stability = "unavailable"
    elif spread is None or spread <= 0.05:
        stability = "stable"
    elif spread <= 0.15:
        stability = "conditional"
    else:
        stability = "unstable"

    return {
        "value": value,
        "scale": [0.0, 1.0],
        "components": raw_components,
        "weights": weights,
        "coverage": coverage,
        "contributions": contributions,
        "sensitivity": {
            "method": "one-at-a-time weight perturbation",
            "perturbation": perturbation,
            "scenarios": scenarios,
            "range": value_range,
            "stability": stability,
        },
        "meaning": "heuristic cultural summary, not prediction",
        "not_prediction": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = compute(payload)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

