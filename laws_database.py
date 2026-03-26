"""
Laws database — loads indian_laws_and_acts_v2.csv and provides search helpers.

Two data sources are supported:

1. **Structured database** (``data/indian_laws_and_acts_v2.csv``)
   Columns: act_name, short_name, year, category, description,
            key_provisions, enforcing_authority, helpline, portal, status

2. **Kanoon index** (``indian_laws_and_acts_v2.csv`` at the repo root)
   Columns: title, source, place, published_date, commencement_date, url
   Contains 10 000+ entries sourced from IndianKanoon.

``key_provisions`` in the structured database uses a pipe (|) as an item separator.
NLP-enhanced scoring is applied via :mod:`nlp_processor`.
"""

from __future__ import annotations

import csv
import os
import re
from functools import lru_cache

from nlp_processor import preprocess_query, extract_year

# ---------------------------------------------------------------------------
# File paths
# ---------------------------------------------------------------------------
_BASE_DIR = os.path.dirname(__file__)
_STRUCTURED_CSV = os.path.join(_BASE_DIR, "data", "indian_laws_and_acts_v2.csv")
_KANOON_CSV = os.path.join(_BASE_DIR, "indian_laws_and_acts_v2.csv")

# Common words excluded from keyword scoring
_STOP_WORDS = frozenset({
    "the", "of", "and", "in", "to", "a", "an", "for", "is", "are", "was", "were",
    "what", "tell", "me", "about", "explain", "how", "does", "it", "its", "that",
    "this", "with", "by", "under", "which", "who", "when", "where", "why", "do",
    "india", "indian", "act", "law", "section", "right", "rights",
})


@lru_cache(maxsize=1)
def load_laws_database() -> tuple[dict, ...]:
    """
    Load the structured CSV once and return it as an immutable tuple of dicts.
    Returns an empty tuple if the CSV cannot be read.
    """
    if not os.path.exists(_STRUCTURED_CSV):
        return ()
    laws: list[dict] = []
    with open(_STRUCTURED_CSV, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            laws.append(dict(row))
    return tuple(laws)


@lru_cache(maxsize=1)
def load_kanoon_database() -> tuple[dict, ...]:
    """
    Load the root Kanoon CSV (10 000+ entries) deduped by title.
    Returns an immutable tuple of dicts with keys:
      title, source, place, published_date, commencement_date, url
    """
    if not os.path.exists(_KANOON_CSV):
        return ()
    seen: set[str] = set()
    laws: list[dict] = []
    with open(_KANOON_CSV, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            title = row.get("title", "").strip()
            if title and title not in seen:
                seen.add(title)
                laws.append(dict(row))
    return tuple(laws)


def _tokenise(text: str) -> set[str]:
    """Return lowercase word tokens minus stop words."""
    return set(re.findall(r"\w+", text.lower())) - _STOP_WORDS


def search_law(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the structured laws database for laws matching *query*.

    Scoring (higher is better):
    - Exact short_name match:              20 pts
    - short_name contained in query
      or query contained in short_name:   12 pts
    - Exact act_name match:               18 pts
    - Act-name keyword overlap:            3 pts/word
    - NLP-stemmed keyword overlap:         2 pts/word
    - Category match:                      4 pts
    - Description keyword overlap:         1 pt/word
    - Year exact match:                    2 pts

    Returns up to *max_results* matching law dicts sorted by descending score.
    """
    query_stripped = query.strip()
    if not query_stripped:
        return []

    query_lower = query_stripped.lower()
    query_tokens = _tokenise(query_stripped)
    _, nlp_tokens = preprocess_query(query_stripped)
    year_hint = extract_year(query_stripped)

    scored: list[tuple[int, dict]] = []
    for law in load_laws_database():
        score = 0
        act_name = law.get("act_name", "").lower()
        short_name = law.get("short_name", "").lower()
        category = law.get("category", "").lower()
        description = law.get("description", "").lower()
        year = law.get("year", "").strip()

        # --- short_name matching ---
        if short_name and short_name == query_lower:
            score += 20
        elif short_name and re.search(r"\b" + re.escape(short_name) + r"\b", query_lower):
            score += 12
        else:
            short_tokens = _tokenise(short_name)
            if short_tokens and short_tokens == query_tokens:
                score += 16
            elif short_tokens and short_tokens <= query_tokens:
                score += 10

        # --- act_name matching ---
        if act_name and act_name == query_lower:
            score += 18

        act_tokens = _tokenise(law.get("act_name", ""))
        score += len(act_tokens & query_tokens) * 3

        # --- NLP stemmed overlap (catches plurals, verb forms) ---
        _, act_nlp = preprocess_query(law.get("act_name", ""))
        score += len(act_nlp & nlp_tokens) * 2

        # --- category matching ---
        if category and category in query_lower:
            score += 4

        # --- description keyword overlap ---
        desc_tokens = _tokenise(description)
        score += len(desc_tokens & query_tokens)

        # --- year match ---
        if year and year_hint and year == year_hint:
            score += 2

        if score > 0:
            scored.append((score, law))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [law for _, law in scored[:max_results]]


def search_kanoon(query: str, max_results: int = 10) -> list[dict]:
    """
    Search the Kanoon index (root CSV, 7 500+ unique laws) for matching laws.

    Scoring (higher is better):
    - Exact title match:          30 pts
    - Title contains query:       15 pts
    - NLP stemmed token overlap:   3 pts/token
    - Source/place match:          2 pts
    - Year hint match:             2 pts

    Returns up to *max_results* dicts (keys: title, source, place,
    published_date, commencement_date, url).
    (Source CSV contains 7,500+ unique laws from IndianKanoon.)
    """
    query_stripped = query.strip()
    if not query_stripped:
        return []

    query_lower = query_stripped.lower()
    _, nlp_tokens = preprocess_query(query_stripped)
    year_hint = extract_year(query_stripped)

    scored: list[tuple[int, dict]] = []
    for law in load_kanoon_database():
        title = law.get("title", "")
        title_lower = title.lower()
        source = law.get("source", "").lower()
        place = law.get("place", "").lower()
        pub_date = law.get("published_date", "")

        score = 0

        if title_lower == query_lower:
            score += 30
        elif query_lower in title_lower:
            score += 15
        elif title_lower in query_lower:
            score += 8

        # NLP token overlap with title
        _, title_nlp = preprocess_query(title)
        overlap = len(title_nlp & nlp_tokens)
        score += overlap * 3

        # Source / place match
        if query_lower in source or query_lower in place:
            score += 2

        # Year hint
        if year_hint and year_hint in pub_date:
            score += 2

        if score > 0:
            scored.append((score, law))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [law for _, law in scored[:max_results]]


def get_law_by_short_name(short_name: str) -> dict | None:
    """Return a law dict whose short_name matches exactly (case-insensitive), or None."""
    target = short_name.strip().lower()
    for law in load_laws_database():
        if law.get("short_name", "").lower() == target:
            return law
    return None


def get_all_laws() -> list[dict]:
    """Return all laws as a list of dicts."""
    return list(load_laws_database())


def get_law_categories() -> list[str]:
    """Return a sorted list of unique law categories."""
    return sorted({law.get("category", "").strip() for law in load_laws_database() if law.get("category")})
