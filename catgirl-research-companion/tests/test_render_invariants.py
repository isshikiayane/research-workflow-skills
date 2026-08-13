from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from render_companion import fact_digest, render  # noqa: E402


STRUCTURED_INPUT = {
    "data_quality": {
        "status": "degraded",
        "checks": [{"name": "water_layer", "result": "missing"}],
    },
    "spatial_metrics": {
        "slope_mean_degrees": 12.3456,
        "flow_accumulation": {"unit": "cells", "value": 42},
    },
    "gate": {"status": "pass", "formal_result": False},
    "evidence_level": "exploratory",
    "heuristic_cultural_index": {
        "value": 0.618,
        "scale": [0.0, 1.0],
    },
    "uncertainty": ["DSM includes vegetation"],
    "limitations": ["No water layer"],
    "conclusion": "Conditional cultural reading only.",
}


class RenderingInvariantTests(unittest.TestCase):
    def test_all_presets_preserve_exact_structured_facts(self) -> None:
        original = copy.deepcopy(STRUCTURED_INPUT)
        outputs = [render(STRUCTURED_INPUT, style) for style in ("gentle", "tsundere", "sarcastic")]
        for output in outputs:
            self.assertEqual(output["structured_facts"], original)
            self.assertEqual(output["fact_digest"], fact_digest(original))
        self.assertEqual(outputs[0]["structured_facts"], outputs[1]["structured_facts"])
        self.assertEqual(outputs[1]["structured_facts"], outputs[2]["structured_facts"])
        self.assertEqual(len({output["narrative"] for output in outputs}), 3)
        self.assertEqual(STRUCTURED_INPUT, original)

    def test_unknown_preset_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            render(STRUCTURED_INPUT, "invented")


if __name__ == "__main__":
    unittest.main()

