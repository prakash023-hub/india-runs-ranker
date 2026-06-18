"""Fast CPU feature extraction aligned with JD + trap guidance."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from src.jd_profile import (
    CAREER_PRODUCTION_PHRASES,
    CORE_SKILLS,
    NEGATIVE_PHRASES,
    TITLE_MILD,
    TITLE_STRONG,
    TITLE_TRAP,
    experience_score,
)

AI_SKILL_HINTS = {
    "nlp", "llm", "llms", "rag", "retrieval", "embedding", "embeddings",
    "ranking", "pytorch", "tensorflow", "vector", "faiss", "pgvector",
    "machine learning", "deep learning", "fine-tuning", "fine tuning",
    "information retrieval", "xgboost",
}


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def _profile_text(candidate: dict[str, Any]) -> str:
    profile = candidate.get("profile", {})
    return " ".join(
        [
            profile.get("headline", ""),
            profile.get("summary", ""),
            profile.get("current_title", ""),
        ]
    ).lower()


def _career_text(candidate: dict[str, Any]) -> str:
    parts: list[str] = []
    for role in candidate.get("career_history", []):
        parts.extend(
            [
                role.get("title", ""),
                role.get("description", ""),
                role.get("company", ""),
                role.get("industry", ""),
            ]
        )
    return " ".join(parts).lower()


def _skill_names(candidate: dict[str, Any]) -> list[str]:
    return [s.get("name", "").lower() for s in candidate.get("skills", [])]


def title_relevance_score(candidate: dict[str, Any]) -> float:
    title = candidate.get("profile", {}).get("current_title", "").lower()
    score = 0.0

    for phrase, bonus in TITLE_STRONG.items():
        if phrase in title:
            score = max(score, bonus)

    if score == 0.0:
        for phrase, bonus in TITLE_MILD.items():
            if phrase in title:
                score = max(score, bonus)

    if any(trap in title for trap in TITLE_TRAP):
        score -= 10.0

    if "architect" in title and "ai" not in title and "ml" not in title:
        score -= 3.0

    return score


def career_fit_score(candidate: dict[str, Any]) -> float:
    """Reward production ML / retrieval / ranking work in career history."""
    career = _career_text(candidate)
    score = 0.0
    for phrase, weight in CAREER_PRODUCTION_PHRASES.items():
        if phrase in career:
            score += weight

    # Product-company shipping signals
    product_markers = ("product company", "startup", "series a", "users", "customers", "production traffic")
    if any(m in career for m in product_markers):
        score += 2.0

    for phrase in NEGATIVE_PHRASES:
        if phrase in career or phrase in _profile_text(candidate):
            score -= 3.0

    return score


def skill_match_score(candidate: dict[str, Any], title: str) -> float:
    """
    Skills matter, but less when title is a trap role.
    Career + summary weighted higher than raw skill list stuffing.
    """
    profile_blob = _profile_text(candidate)
    career_blob = _career_text(candidate)
    combined = f"{profile_blob} {career_blob}"

    score = 0.0
    for keyword, weight in CORE_SKILLS.items():
        if keyword in combined:
            score += weight
        elif keyword in " ".join(_skill_names(candidate)):
            # Skills listed but not evidenced in narrative — lower weight
            score += weight * 0.35

    # Verified assessments from Redrob platform
    assessments = candidate.get("redrob_signals", {}).get("skill_assessment_scores", {})
    if assessments:
        relevant = [
            v for k, v in assessments.items()
            if any(h in k.lower() for h in AI_SKILL_HINTS)
        ]
        if relevant:
            score += (sum(relevant) / len(relevant)) / 100.0 * 5.0

    is_trap_title = any(trap in title for trap in TITLE_TRAP)
    ai_skill_count = sum(
        1 for name in _skill_names(candidate)
        if any(h in name for h in AI_SKILL_HINTS)
    )

    if is_trap_title:
        score *= 0.15
        if ai_skill_count >= 5:
            score -= 8.0

    # Scientist/research titles: discount skill-list inflation
    if any(x in title for x in ("scientist", "research", "phd", "postdoc")):
        score *= 0.45
        if candidate.get("profile", {}).get("years_of_experience", 0) > 12:
            score -= 6.0

    return score


def engagement_score(signals: dict[str, Any]) -> float:
    if not signals:
        return 0.0

    today = date.today()
    last_active = _parse_date(signals.get("last_active_date"))
    days_inactive = (today - last_active).days if last_active else 365

    score = 0.0
    score += min(signals.get("profile_completeness_score", 0) / 100.0, 1.0) * 1.5
    score += signals.get("recruiter_response_rate", 0) * 5.0
    score += min(signals.get("saved_by_recruiters_30d", 0) / 8.0, 1.0) * 2.5
    score += min(signals.get("search_appearance_30d", 0) / 15.0, 1.0) * 2.0
    score += min(signals.get("profile_views_received_30d", 0) / 20.0, 1.0) * 1.0
    score += signals.get("interview_completion_rate", 0) * 2.5

    gh = signals.get("github_activity_score", -1)
    if gh >= 0:
        score += min(gh / 100.0, 1.0) * 2.0

    if signals.get("open_to_work_flag"):
        score += 1.5
    if signals.get("willing_to_relocate"):
        score += 0.5
    if signals.get("verified_email"):
        score += 0.2
    if signals.get("verified_phone"):
        score += 0.2
    if signals.get("linkedin_connected"):
        score += 0.2

    notice = signals.get("notice_period_days", 90)
    if notice <= 60:
        score += 0.8
    elif notice > 120:
        score -= 1.0

    if days_inactive > 180:
        score -= 4.0
    elif days_inactive > 90:
        score -= 2.0
    elif days_inactive <= 14:
        score += 1.5

    resp = signals.get("recruiter_response_rate", 1)
    if resp < 0.05:
        score -= 6.0
    elif resp < 0.1:
        score -= 3.0

    return score


def trap_penalty(candidate: dict[str, Any]) -> float:
    signals = candidate.get("redrob_signals", {})
    profile = candidate.get("profile", {})
    title = profile.get("current_title", "").lower()
    penalty = 0.0

    if any(trap in title for trap in TITLE_TRAP):
        penalty += 12.0

    ai_skills = sum(1 for n in _skill_names(candidate) if any(h in n for h in AI_SKILL_HINTS))
    if ai_skills >= 7 and not any(k in title for k in ("engineer", "scientist", "developer", "architect")):
        penalty += 10.0

    if signals.get("recruiter_response_rate", 1) < 0.05:
        penalty += 8.0
    if not signals.get("open_to_work_flag", True):
        penalty += 3.0

    last_active = _parse_date(signals.get("last_active_date"))
    if last_active and (date.today() - last_active).days > 180:
        penalty += 6.0

    completeness = signals.get("profile_completeness_score", 100)
    if completeness < 30:
        penalty += 4.0

    years = float(profile.get("years_of_experience", 0))
    if years > 14:
        penalty += 3.0 + 0.5 * max(0, years - 14)

    if "scientist" in title and years > 10:
        penalty += 5.0

    if "langchain" in _profile_text(candidate) and "production" not in _career_text(candidate):
        penalty += 2.0

    return penalty


def total_score(candidate: dict[str, Any]) -> float:
    profile = candidate.get("profile", {})
    title = profile.get("current_title", "").lower()
    years = float(profile.get("years_of_experience", 0))

    score = 0.0
    score += title_relevance_score(candidate) * 1.0
    score += career_fit_score(candidate) * 1.2
    score += skill_match_score(candidate, title)
    score += experience_score(years) * 7.0
    score += engagement_score(candidate.get("redrob_signals", {}))
    score -= trap_penalty(candidate)
    return score


def reasoning(candidate: dict[str, Any], score: float) -> str:
    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})
    title = profile.get("current_title", "Professional")
    years = profile.get("years_of_experience", 0)

    career = _career_text(candidate)
    career_hits = [p for p in ("retrieval", "ranking", "production", "embedding", "rag") if p in career][:2]
    career_txt = ", ".join(career_hits) if career_hits else "applied ML delivery"

    ai_skills = [
        s["name"] for s in candidate.get("skills", [])
        if any(h in s.get("name", "").lower() for h in AI_SKILL_HINTS)
    ][:2]
    skill_txt = ", ".join(ai_skills) if ai_skills else "core AI stack"
    resp = signals.get("recruiter_response_rate", 0)

    return (
        f"{title} with {years:.1f} yrs; production signals in {career_txt}; "
        f"skills include {skill_txt}; response rate {resp:.2f}."
    )
