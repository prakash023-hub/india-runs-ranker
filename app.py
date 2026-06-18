"""Streamlit sandbox — India Runs candidate ranker demo."""

from __future__ import annotations

import csv
import io
from pathlib import Path

import streamlit as st

from src.ranker import run_ranking

st.set_page_config(
    page_title="India Runs Ranker",
    page_icon="🇮🇳",
    layout="wide",
)

DEMO_PATH = Path("data/demo_candidates.jsonl")
FULL_PATH = Path("data/candidates.jsonl")


def resolve_data_path(mode: str) -> tuple[Path, str]:
    if mode == "Full dataset (100k — local only)":
        if not FULL_PATH.exists():
            st.error(
                "Place `candidates.jsonl` in `data/` for the full run. "
                "See data/README.md for download instructions."
            )
            st.stop()
        return FULL_PATH, "100,000 candidates"
    if not DEMO_PATH.exists():
        st.error("Demo file missing. Run: `head -1000 data/candidates.jsonl > data/demo_candidates.jsonl`")
        st.stop()
    return DEMO_PATH, "1,000 candidates (demo subset)"


st.title("India Runs — Senior AI Engineer Ranker")
st.caption(
    "Track 1 · Redrob Data & AI Challenge · CPU-only heuristic ranker with trap-profile detection"
)

with st.sidebar:
    st.header("Run settings")
    dataset_mode = st.radio(
        "Dataset",
        ["Demo subset (bundled)", "Full dataset (100k — local only)"],
        index=0,
    )
    data_path, pool_label = resolve_data_path(dataset_mode)
    top_k = st.slider("Top K to rank", min_value=10, max_value=100, value=100, step=10)
    run_btn = st.button("Run ranking", type="primary", use_container_width=True)

    st.divider()
    st.markdown(
        "**Constraints met:** CPU only · no API calls · <5 min · <16 GB RAM  \n"
        "**Scoring:** title fit · career production signals · skills · Redrob signals · trap penalties"
    )

if run_btn:
    with st.spinner(f"Ranking top {top_k} from {pool_label}..."):
        result = run_ranking(data_path, output_path=None, top_k=top_k)

    st.success(
        f"Ranked **{result.processed:,}** profiles in **{result.elapsed_sec:.2f}s** "
        f"({result.pool_label})"
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Pool size", f"{result.processed:,}")
    col2.metric("Runtime", f"{result.elapsed_sec:.2f}s")
    col3.metric("#1 candidate", result.rows[0]["candidate_id"])

    st.subheader("Top 20 preview")
    preview = [
        {
            "rank": r["rank"],
            "candidate_id": r["candidate_id"],
            "score": r["score"],
            "title": r["title"],
            "years": r["years"],
            "reasoning": r["reasoning"][:120] + ("…" if len(r["reasoning"]) > 120 else ""),
        }
        for r in result.rows[:20]
    ]
    st.dataframe(preview, use_container_width=True, hide_index=True)

    with st.expander("Full results + download"):
        st.dataframe(result.rows, use_container_width=True, hide_index=True)
        csv_buf = io.StringIO()
        fieldnames = ["candidate_id", "rank", "score", "reasoning"]
        writer = csv.DictWriter(csv_buf, fieldnames=fieldnames)
        writer.writeheader()
        for row in result.rows:
            writer.writerow({k: row[k] for k in fieldnames})
        st.download_button(
            "Download submission.csv",
            data=csv_buf.getvalue(),
            file_name="submission.csv",
            mime="text/csv",
            use_container_width=True,
        )

else:
    st.info("Select dataset and click **Run ranking** in the sidebar.")
    st.markdown(
        """
### Approach
1. **Title relevance** — boost Senior/Lead AI & ML Engineer titles; penalize trap roles (Marketing, HR, etc.).
2. **Career evidence** — retrieval, ranking, RAG, deployment phrases in role descriptions outweigh skill-list keywords.
3. **Experience band** — peak score at 5–9 years; down-rank 11+ year research-only profiles.
4. **Redrob signals** — response rate, activity, assessments, open-to-work.
5. **Min-heap streaming** — O(n log k) pass over 100k JSONL without loading full dataset into memory.

Clone the repo and run `python rank.py` locally for the official 100k submission CSV.
        """
    )
