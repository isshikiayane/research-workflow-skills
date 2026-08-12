#!/usr/bin/env python3
"""Read raster metadata and compare rasters to a reference without changing inputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def metadata(path: Path) -> dict[str, Any]:
    try:
        import rasterio
    except ImportError as error:
        raise RuntimeError("rasterio is required; install it in the active environment") from error

    with rasterio.open(path) as dataset:
        return {
            "path": str(path),
            "driver": dataset.driver,
            "crs": str(dataset.crs) if dataset.crs else None,
            "width": dataset.width,
            "height": dataset.height,
            "count": dataset.count,
            "dtypes": list(dataset.dtypes),
            "nodata": dataset.nodata,
            "transform": list(dataset.transform),
            "bounds": list(dataset.bounds),
            "resolution": list(dataset.res),
        }


def compare(candidate: dict[str, Any], reference: dict[str, Any]) -> dict[str, Any]:
    fields = ("crs", "width", "height", "transform", "resolution")
    differences = {
        field: {"reference": reference[field], "candidate": candidate[field]}
        for field in fields
        if candidate[field] != reference[field]
    }
    return {
        "reference": reference["path"],
        "candidate": candidate["path"],
        "status": "MATCH" if not differences else "DIFFERENT",
        "differences": differences,
        "note": "A DIFFERENT result requires an intentional transformation and documented resampling decision before pixel-wise use.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect raster metadata and report compatibility with a reference raster."
    )
    parser.add_argument("rasters", nargs="+", type=Path)
    parser.add_argument("--reference", type=Path, help="Reference raster; defaults to the first input.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--strict", action="store_true", help="Exit with status 2 if a raster differs from the reference.")
    args = parser.parse_args()

    paths = list(dict.fromkeys(args.rasters))
    reference_path = args.reference or paths[0]
    if reference_path not in paths:
        paths.insert(0, reference_path)

    records = [metadata(path) for path in paths]
    reference = next(record for record in records if record["path"] == str(reference_path))
    comparisons = [compare(record, reference) for record in records if record is not reference]
    has_difference = any(item["status"] == "DIFFERENT" for item in comparisons)
    report = {
        "reference": reference["path"],
        "rasters": records,
        "compatibility": comparisons,
        "overall_status": "DIFFERENCES_FOUND" if has_difference else "MATCHES_REFERENCE",
        "limitations": [
            "Metadata agreement does not establish vertical-datum, unit, semantic, or temporal compatibility.",
            "Inspect alignment visually when metadata cannot rule out offsets or mask errors.",
        ],
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 2 if args.strict and has_difference else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)

