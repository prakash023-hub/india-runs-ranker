#!/usr/bin/env python3
"""Basic submission.csv format validator."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def load_candidate_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                ids.add(json.loads(line)["candidate_id"])
    return ids


def validate(csv_path: Path, candidates_path: Path) -> int:
    errors: list[str] = []
    with csv_path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if len(rows) != 100:
        errors.append(f"Expected 100 data rows, got {len(rows)}")

    ranks = [int(r["rank"]) for r in rows]
    if sorted(ranks) != list(range(1, 101)):
        errors.append("Ranks must be exactly 1..100 each once")

    ids = [r["candidate_id"] for r in rows]
    if len(set(ids)) != len(ids):
        errors.append("Duplicate candidate_id found")

    scores = [float(r["score"]) for r in rows]
    for i in range(1, len(scores)):
        if scores[i] > scores[i - 1] + 1e-9:
            errors.append(f"Scores not non-increasing at rank {i + 1}")
            break

    valid_ids = load_candidate_ids(candidates_path)
    bad = [cid for cid in ids if cid not in valid_ids]
    if bad:
        errors.append(f"Unknown candidate IDs: {bad[:5]}")

    if errors:
        print("VALIDATION FAILED")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("VALIDATION PASSED")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=Path("output/submission.csv"))
    parser.add_argument("--candidates", type=Path, default=Path("data/candidates.jsonl"))
    args = parser.parse_args()
    raise SystemExit(validate(args.csv, args.candidates))


if __name__ == "__main__":
    main()
