#!/usr/bin/env python3
"""Generate submission.csv — top 100 candidates for India Runs Track 1."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.ranker import run_ranking


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank candidates for India Runs")
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("data/candidates.jsonl"),
        help="Path to candidates.jsonl",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/submission.csv"),
        help="Output CSV path",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only first N candidates (for quick tests)",
    )
    args = parser.parse_args()

    result = run_ranking(
        args.data,
        args.output,
        limit=args.limit,
        on_progress=lambda n: print(f"  processed {n:,} candidates..."),
    )

    print(f"Wrote {len(result.rows)} rows to {args.output}")
    print(
        f"Runtime: {result.elapsed_sec:.1f}s | "
        f"Top candidate: {result.rows[0]['candidate_id']} ({result.rows[0]['score']})"
    )


if __name__ == "__main__":
    main()
