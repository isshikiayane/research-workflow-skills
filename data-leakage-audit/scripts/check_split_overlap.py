#!/usr/bin/env python3
"""Report candidate split overlap in CSV inventories without modifying inputs."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path}: CSV has no header row")
        return list(reader)


def overlap_report(
    inventories: dict[str, list[dict[str, str]]], column: str
) -> dict[str, Any]:
    seen: dict[str, set[str]] = defaultdict(set)
    for split, rows in inventories.items():
        for row in rows:
            value = (row.get(column) or "").strip()
            if value:
                seen[value].add(split)

    shared = {
        value: sorted(splits)
        for value, splits in seen.items()
        if len(splits) > 1
    }
    samples = [
        {"value": value, "splits": splits}
        for value, splits in list(sorted(shared.items()))[:10]
    ]
    return {
        "column": column,
        "unique_values": len(seen),
        "shared_value_count": len(shared),
        "samples": samples,
        "status": "OVERLAP_FOUND" if shared else "NO_EXACT_OVERLAP_FOUND",
    }


def coordinate_report(
    inventories: dict[str, list[dict[str, str]]], x_column: str, y_column: str, decimals: int
) -> dict[str, Any]:
    normalized: dict[str, list[dict[str, str]]] = {}
    for split, rows in inventories.items():
        converted = []
        for row in rows:
            try:
                x = round(float((row.get(x_column) or "").strip()), decimals)
                y = round(float((row.get(y_column) or "").strip()), decimals)
            except ValueError:
                continue
            converted.append({"coordinate_key": f"{x:.{decimals}f},{y:.{decimals}f}"})
        normalized[split] = converted
    result = overlap_report(normalized, "coordinate_key")
    result.update({"x_column": x_column, "y_column": y_column, "decimals": decimals})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check exact IDs, groups, and rounded coordinates across split CSV files."
    )
    parser.add_argument("--train", required=True, type=Path)
    parser.add_argument("--validation", required=True, type=Path)
    parser.add_argument("--test", required=True, type=Path)
    parser.add_argument("--id-column", default="id")
    parser.add_argument("--group-column")
    parser.add_argument("--x-column")
    parser.add_argument("--y-column")
    parser.add_argument("--coordinate-decimals", type=int, default=6)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--fail-on-overlap",
        action="store_true",
        help="Exit with status 2 when any requested exact-overlap check finds candidates.",
    )
    args = parser.parse_args()

    if bool(args.x_column) != bool(args.y_column):
        parser.error("--x-column and --y-column must be supplied together")
    if args.coordinate_decimals < 0:
        parser.error("--coordinate-decimals must be non-negative")

    inventories = {
        "train": read_rows(args.train),
        "validation": read_rows(args.validation),
        "test": read_rows(args.test),
    }
    report: dict[str, Any] = {
        "inputs": {split: str(path) for split, path in {
            "train": args.train, "validation": args.validation, "test": args.test
        }.items()},
        "row_counts": {split: len(rows) for split, rows in inventories.items()},
        "checks": {"id": overlap_report(inventories, args.id_column)},
        "limitations": [
            "No exact overlap is not proof of leakage-free evaluation.",
            "Rounded coordinates are candidate duplicates, not a spatial-independence test.",
        ],
    }
    if args.group_column:
        report["checks"]["group"] = overlap_report(inventories, args.group_column)
    if args.x_column:
        report["checks"]["coordinate"] = coordinate_report(
            inventories, args.x_column, args.y_column, args.coordinate_decimals
        )

    has_overlap = any(
        check["shared_value_count"] > 0 for check in report["checks"].values()
    )
    report["overall_status"] = "CANDIDATE_OVERLAP_FOUND" if has_overlap else "NO_EXACT_OVERLAP_FOUND"
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 2 if args.fail_on_overlap and has_overlap else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)

