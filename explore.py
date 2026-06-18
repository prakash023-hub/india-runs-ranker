#!/usr/bin/env python3
"""Quick dataset exploration."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

DATA = Path("data/sample_candidates.json")


def main() -> None:
    candidates = json.loads(DATA.read_text(encoding="utf-8"))
    titles = Counter(c["profile"]["current_title"] for c in candidates)
    print(f"Sample candidates: {len(candidates)}")
    print("\nTop titles:")
    for title, count in titles.most_common(10):
        print(f"  {count:2d}  {title}")

    exp = [c["profile"]["years_of_experience"] for c in candidates]
    print(f"\nExperience range: {min(exp):.1f} - {max(exp):.1f} yrs")

    low_resp = sum(
        1 for c in candidates if c["redrob_signals"].get("recruiter_response_rate", 1) < 0.1
    )
    print(f"Low response rate (<0.1): {low_resp}/{len(candidates)}")


if __name__ == "__main__":
    main()
