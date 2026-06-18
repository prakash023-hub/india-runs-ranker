# Track 2 — Ideathon PDF outline (optional, deadline 2 July 2026)

Use this structure for a 3–5 page PDF if you also compete in Track 2.

---

## Title

**Evidence-First Candidate Ranking for High-Volume AI Hiring**

---

## 1. Problem statement (½ page)

- Redrob must surface 100 strong Senior AI Engineer candidates from 100k profiles
- Keyword matching fails on trap profiles and skill-list inflation
- Recruiters need explainable rankings, not black-box scores

---

## 2. Why keyword matching fails (½ page)

- Example trap: Marketing Manager with LLM/RAG in skills, no engineering roles
- Applied Scientist with 16+ years and research keywords but no production delivery
- Skill inflation vs. career narrative mismatch

---

## 3. Proposed system architecture (1 page)

```
JSONL stream → Feature extraction → Weighted score → Min-heap top-100 → CSV + reasoning
```

- **Title tier classifier** (strong / mild / trap)
- **Career phrase matcher** (retrieval, ranking, deployment)
- **Skill corroboration** (skills only count when echoed in career text)
- **Experience band curve** (peak 5–9 years)
- **Redrob signals** (response, activity, assessments)
- **Explainability:** per-candidate reasoning string in submission CSV

Diagram: simple flowchart or mermaid in final PDF.

---

## 4. Differentiation vs. baseline TF-IDF (½ page)

| Baseline | Our approach |
|----------|--------------|
| Skills bag-of-words | Career evidence weighting |
| No trap detection | Title trap penalties |
| Opaque score | Human-readable reasoning |
| Needs GPU/embeddings | CPU streaming, 18s |

---

## 5. Product vision for Redrob (1 page)

- **Phase 1:** Heuristic ranker (this hackathon submission)
- **Phase 2:** Learn-to-rank from recruiter feedback on shortlists
- **Phase 3:** JD-specific weight tuning per customer
- **Metrics:** precision@100, trap rejection rate, recruiter time-to-shortlist

---

## 6. Business impact (½ page)

- Faster shortlisting for enterprise customers
- Reduced false positives in AI talent searches
- Explainable rankings build recruiter trust

---

## 7. Team & next steps (¼ page)

- GitHub + sandbox links
- Roadmap to production integration with Redrob platform

---

Export to PDF via Google Docs, Notion, or LaTeX. Upload on Hack2Skill Track 2 form before **2 July 2026**.
