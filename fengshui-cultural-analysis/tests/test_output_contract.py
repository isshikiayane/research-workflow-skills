from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPUTE = ROOT / "scripts" / "compute_heuristic_index.py"
VALIDATE = ROOT / "scripts" / "validate_output.py"


class OutputContractTests(unittest.TestCase):
    def test_compute_and_validate_complete_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            input_path = directory_path / "components.json"
            output_path = directory_path / "index.json"
            input_path.write_text(
                json.dumps({
                    "components": {
                        "backing": {"value": 0.8, "source_metrics": ["elevation.rear"]},
                        "openness": 0.6,
                        "water_relation": 0.4,
                    },
                    "weights": {"backing": 2.0, "openness": 1.0, "water_relation": 1.0},
                }),
                encoding="utf-8",
            )
            subprocess.run(
                [sys.executable, str(COMPUTE), str(input_path), "-o", str(output_path)],
                check=True,
            )
            index = json.loads(output_path.read_text(encoding="utf-8"))
            output = {
                "not_prediction": True,
                "data_quality": {"status": "pass"},
                "spatial_metrics": {"elevation.rear": {"value": 0.8}},
                "cultural_interpretation": [],
                "heuristic_cultural_index": index,
                "sensitivity": index["sensitivity"],
                "uncertainty": [],
                "limitations": ["Heuristic cultural reading only."],
            }
            full_path = directory_path / "full.json"
            full_path.write_text(json.dumps(output), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(VALIDATE), str(full_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertIn("VALID", completed.stdout)
            self.assertGreaterEqual(index["value"], 0.0)
            self.assertLessEqual(index["value"], 1.0)

    def test_validator_rejects_prediction_flag(self) -> None:
        invalid = {
            "not_prediction": False,
            "data_quality": {},
            "spatial_metrics": {},
            "cultural_interpretation": [],
            "heuristic_cultural_index": {
                "value": 0.5,
                "scale": [0.0, 1.0],
                "coverage": 1.0,
                "components": {},
            },
            "sensitivity": {},
            "uncertainty": [],
            "limitations": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text(json.dumps(invalid), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(VALIDATE), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("not_prediction must be true", completed.stdout)


if __name__ == "__main__":
    unittest.main()

