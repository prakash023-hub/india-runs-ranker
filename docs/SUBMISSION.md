# India Runs Track 1 — Submission Checklist

Complete every item before **28 June 2026**.

---

## 1. Generate submission CSV

```bash
cd india-runs-ranker
source .venv/bin/activate
python rank.py --output output/submission.csv
python validate_submission.py --csv output/submission.csv
```

Expected: `VALIDATION PASSED`, 100 rows, ranks 1–100.

Rename for portal upload:

```bash
cp output/submission.csv team_<YOUR_TEAM_ID>.csv
```

Get `<YOUR_TEAM_ID>` from the Hack2Skill India Runs dashboard after registration.

---

## 2. GitHub repository

1. Create repo: https://github.com/new → name `india-runs-ranker` (public)
2. Push:

```bash
git remote add origin https://github.com/prakash023-hub/india-runs-ranker.git
git push -u origin main
```

3. Confirm `candidates.jsonl` is **not** in the repo (gitignored, ~465 MB).

---

## 3. Sandbox (required)

Deploy the Streamlit app so judges can run the ranker without the full dataset.

### Option A — Streamlit Community Cloud (recommended)

1. https://share.streamlit.io → Sign in with GitHub
2. **New app** → Repository: `prakash023-hub/india-runs-ranker`, branch `main`, main file `app.py`
3. Deploy → copy public URL (e.g. `https://india-runs-ranker.streamlit.app`)

### Option B — HuggingFace Spaces

1. https://huggingface.co/new-space → SDK: **Streamlit**
2. Connect GitHub repo or upload files
3. Space URL: `https://huggingface.co/spaces/<user>/india-runs-ranker`

Paste sandbox URL into Hack2Skill submission form.

---

## 4. Hack2Skill portal upload

1. Register: https://hack2skill.com/event/india_runs
2. Complete Redrob signup: https://auth.redrob.io
3. Track 1 submission form:
   - **CSV:** `team_<id>.csv`
   - **GitHub:** repo URL
   - **Sandbox:** Streamlit/HF URL
   - **Description:** copy from `submission_metadata.yaml`

---

## 5. Optional — Track 3 (LinkedIn)

Post about your solution using the draft in [LINKEDIN_TRACK3.md](LINKEDIN_TRACK3.md). Tag #IndiaRuns #RedrobAI #Hack2Skill.

---

## 6. Optional — Track 2 (Ideathon PDF)

Deadline **2 July 2026**. Outline in [IDEOATHON_OUTLINE.md](IDEOATHON_OUTLINE.md).

---

## Pre-submit verification

- [ ] `validate_submission.py` passes on full 100k run
- [ ] Top 100 has no obvious trap titles (Marketing Manager, HR, etc.)
- [ ] GitHub repo is public and README is complete
- [ ] Sandbox loads and ranks demo subset in <30s
- [ ] CSV renamed to team ID format
- [ ] All portal fields filled

---

## Contact / support

- Hack2Skill event page: https://hack2skill.com/event/india_runs
- Dataset issues: Hack2Skill support on event page
