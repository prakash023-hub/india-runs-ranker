"""Core ranking engine — importable by CLI and Streamlit sandbox."""

from __future__ import annotations

import csv
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator

from src.features import reasoning, total_score

TOP_K = 100


@dataclass
class RankResult:
    rows: list[dict]
    processed: int
    elapsed_sec: float
    pool_label: str


def iter_candidates(path: Path, limit: int | None = None) -> Iterator[dict]:
    with path.open(encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            if limit and idx > limit:
                break
            line = line.strip()
            if line:
                yield json.loads(line)


def rank_candidate_pool(
    data_path: Path,
    limit: int | None = None,
    top_k: int = TOP_K,
    on_progress: Callable[[int], None] | None = None,
) -> RankResult:
    started = time.time()
    heap: list[tuple[float, str, dict]] = []
    processed = 0

    for candidate in iter_candidates(data_path, limit=limit):
        processed += 1
        if on_progress and processed % 10000 == 0:
            on_progress(processed)
        cid = candidate["candidate_id"]
        score = total_score(candidate)
        entry = (score, cid, candidate)
        if len(heap) < top_k:
            heap.append(entry)
            if len(heap) == top_k:
                heap.sort(key=lambda x: (x[0], x[1]))
        elif score > heap[0][0]:
            heap[0] = entry
            heap.sort(key=lambda x: (x[0], x[1]))

    ranked = sorted(heap, key=lambda x: (-x[0], x[1]))[:top_k]
    max_score = ranked[0][0] if ranked else 1.0
    min_score = ranked[-1][0] if ranked else 0.0
    span = max(max_score - min_score, 1e-6)

    rows: list[dict] = []
    for rank, (raw_score, cid, candidate) in enumerate(ranked, start=1):
        norm = 0.2 + 0.8 * ((raw_score - min_score) / span)
        display_score = round(max(0.2, 1.0 - (rank - 1) * 0.008), 4)
        rows.append(
            {
                "candidate_id": cid,
                "rank": rank,
                "score": display_score,
                "reasoning": reasoning(candidate, norm),
                "title": candidate.get("profile", {}).get("current_title", ""),
                "years": candidate.get("profile", {}).get("years_of_experience", 0),
            }
        )

    elapsed = time.time() - started
    label = data_path.name
    if limit:
        label = f"{label} (first {limit:,})"
    return RankResult(rows=rows, processed=processed, elapsed_sec=elapsed, pool_label=label)


def write_submission_csv(rows: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["candidate_id", "rank", "score", "reasoning"]
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in fieldnames})


def run_ranking(
    data_path: Path,
    output_path: Path | None = None,
    limit: int | None = None,
    top_k: int = TOP_K,
    on_progress: Callable[[int], None] | None = None,
) -> RankResult:
    result = rank_candidate_pool(
        data_path, limit=limit, top_k=top_k, on_progress=on_progress
    )
    if output_path:
        write_submission_csv(result.rows, output_path)
    return result
