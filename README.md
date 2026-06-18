# India Runs — Candidate Ranker (Track 1)

**Rank the top 100 Senior AI Engineer candidates from 100,000 profiles** for the [India Runs by Redrob AI](https://hack2skill.com/event/india_runs) Data & AI Challenge.

Built for **CPU-only**, **≤5 min**, **≤16 GB RAM**, with **no API calls** during ranking.

---

## Highlights

| Metric | Result |
|--------|--------|
| Full run time | ~18s on 100k candidates |
| Memory | Streaming min-heap (O(n log k)) |
| Trap profiles in top 100 | 0 (Marketing/HR keyword-stuffed profiles filtered) |
| Validation | `validate_submission.py` passes on full output |

**Scoring philosophy:** career evidence beats skill-list keywords. A Marketing Manager who listed "LLM" and "RAG" in skills but never built retrieval systems ranks far below a Senior AI Engineer with production ranking/RAG experience.

---

## Quick start

```bash
git clone https://github.com/prakash023-hub/india-runs-ranker.git
cd india-runs-ranker
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Download `[PUB] India_runs_data_and_ai_challenge.zip` from Hack2Skill and place `candidates.jsonl` in `data/` (~465 MB, gitignored).

```bash
# Full submission run
python rank.py --output output/submission.csv
python validate_submission.py --csv output/submission.csv

# Interactive sandbox
streamlit run app.py
```

---

## Project structure

```
rank.py                  # CLI — generates submission.csv
app.py                   # Streamlit sandbox for judges
src/
  ranker.py              # Core ranking engine (heap + CSV export)
  features.py            # Scoring: title, career, skills, signals, traps
  jd_profile.py          # JD keywords, title tiers, experience bands
validate_submission.py   # Format + ID validation
data/
  demo_candidates.jsonl  # 1k subset for sandbox (no full download needed)
  sample_candidates.json
docs/SUBMISSION.md       # End-to-end submit checklist
submission_metadata.yaml # Portal metadata template
```

---

## Scoring (v2)

1. **Title fit** — Strong boost: Senior/Lead/Staff AI Engineer, ML Engineer. Penalties: Marketing Manager, HR, Sales traps.
2. **Career production signals** — retrieval, ranking, RAG, embeddings, deployment in role descriptions.
3. **Skills** — Listed skills count less unless echoed in career history.
4. **Experience band** — Peak at 5–9 years; penalties for 11+ research-only profiles.
5. **Redrob behavioral signals** — response rate, activity, assessments, open-to-work.
6. **Trap penalties** — Keyword stuffing without engineering career evidence.

---

## Sandbox deployment

Deploy `app.py` to **Streamlit Community Cloud** or **HuggingFace Spaces** (Streamlit SDK):

1. Push this repo to GitHub.
2. New app → point at repo → main file: `app.py`.
3. Paste the public URL into Hack2Skill submission as **sandbox link**.

Demo mode uses bundled `data/demo_candidates.jsonl` (1,000 profiles). Full 100k run requires local `candidates.jsonl`.

---

## Submission (before 28 June 2026)

See **[docs/SUBMISSION.md](docs/SUBMISSION.md)** for the full checklist.

1. `output/submission.csv` → rename to `team_<your_id>.csv` on portal
2. GitHub repo URL
3. Sandbox URL (Streamlit/HF)
4. `submission_metadata.yaml` fields

---

## Constraints

- CPU only
- ≤ 5 minutes runtime
- ≤ 16 GB RAM
- No external API calls during ranking
- Output: exactly 100 rows, ranks 1–100, non-increasing scores

---

## License

MIT — hackathon submission for India Runs Track 1.
