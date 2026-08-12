#!/usr/bin/env python3
"""Verify the repository's synthetic helper examples without modifying inputs."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"


def load_expected(relative_path: str) -> dict[str, Any]:
    return json.loads((EXAMPLES / relative_path / "expected-summary.json").read_text(encoding="utf-8"))


def run_json(command: list[str], expected_exit_code: int, label: str) -> dict[str, Any]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != expected_exit_code:
        detail = result.stderr.strip() or result.stdout.strip() or "no output"
        raise AssertionError(
            f"{label}: expected exit code {expected_exit_code}, got {result.returncode}. {detail}"
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{label}: helper did not emit JSON: {result.stdout!r}") from exc


def compact_split_report(report: dict[str, Any]) -> dict[str, Any]:
    checks = report["checks"]
    return {
        "overall_status": report["overall_status"],
        "row_counts": report["row_counts"],
        "checks": {
            name: {
                "status": checks[name]["status"],
                "shared_value_count": checks[name]["shared_value_count"],
                "samples": checks[name]["samples"],
            }
            for name in ("id", "group", "coordinate")
        },
    }


def verify_split_overlap() -> None:
    expected = load_expected("split-overlap")
    command = [
        sys.executable,
        str(ROOT / "data-leakage-audit/scripts/check_split_overlap.py"),
        "--train",
        "examples/split-overlap/train.csv",
        "--validation",
        "examples/split-overlap/validation.csv",
        "--test",
        "examples/split-overlap/test.csv",
        "--id-column",
        "sample_id",
        "--group-column",
        "event_id",
        "--x-column",
        "x",
        "--y-column",
        "y",
        "--fail-on-overlap",
    ]
    actual = compact_split_report(run_json(command, expected["expected_exit_code"], "split-overlap"))
    if actual != expected["summary"]:
        raise AssertionError(
            "split-overlap: report differs from expected summary.\n"
            f"expected={json.dumps(expected['summary'], indent=2)}\n"
            f"actual={json.dumps(actual, indent=2)}"
        )
    print("PASS split-overlap: expected ID and rounded-coordinate overlap candidates found.")


def compact_raster_report(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "overall_status": report["overall_status"],
        "compatibility": [
            {
                "candidate": Path(item["candidate"]).name,
                "status": item["status"],
                "difference_fields": sorted(item["differences"]),
            }
            for item in report["compatibility"]
        ],
    }


def verify_raster_alignment() -> None:
    try:
        import rasterio  # noqa: F401
    except ImportError as exc:
        raise RuntimeError(
            "raster-alignment requires rasterio. Install it with `python -m pip install rasterio`, "
            "or run the split-only check with `--split-only`."
        ) from exc

    expected = load_expected("raster-alignment")
    command = [
        sys.executable,
        str(ROOT / "geospatial-data-qc/scripts/inspect_raster_metadata.py"),
        "examples/raster-alignment/reference.tif",
        "examples/raster-alignment/matching.tif",
        "examples/raster-alignment/shifted.tif",
        "--reference",
        "examples/raster-alignment/reference.tif",
        "--strict",
    ]
    actual = compact_raster_report(run_json(command, expected["expected_exit_code"], "raster-alignment"))
    if actual != expected["summary"]:
        raise AssertionError(
            "raster-alignment: report differs from expected summary.\n"
            f"expected={json.dumps(expected['summary'], indent=2)}\n"
            f"actual={json.dumps(actual, indent=2)}"
        )
    print("PASS raster-alignment: matching grid accepted and shifted grid rejected.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--split-only", action="store_true", help="verify only the CSV split-overlap example")
    selection.add_argument("--raster-only", action="store_true", help="verify only the GeoTIFF alignment example")
    args = parser.parse_args()

    try:
        if not args.raster_only:
            verify_split_overlap()
        if not args.split_only:
            verify_raster_alignment()
    except (AssertionError, RuntimeError, OSError, KeyError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1

    print("All selected synthetic examples passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
