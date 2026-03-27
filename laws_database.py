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
import heapq
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
def _load_preprocessed_laws() -> tuple[dict, ...]:
    """
    Load laws and pre-compute expensive operations like lowercasing and NLP tokens.
    This avoids redundant computation in every search.
    Returns tuple of dicts with additional preprocessed fields.
    """
    laws = load_laws_database()
    preprocessed = []
    for law in laws:
        # Pre-compute lowercase versions
        act_name = law.get("act_name", "")
        short_name = law.get("short_name", "")
        category = law.get("category", "")
        description = law.get("description", "")

        # Pre-compute NLP tokens for act_name (most expensive operation)
        _, act_nlp = preprocess_query(act_name)

        # Pre-compute tokenized versions
        act_tokens = _tokenise(act_name)
        short_tokens = _tokenise(short_name)
        desc_tokens = _tokenise(description)

        preprocessed.append({
            "law": law,
            "act_name_lower": act_name.lower(),
            "short_name_lower": short_name.lower(),
            "category_lower": category.lower(),
            "description_lower": description.lower(),
            "year": law.get("year", "").strip(),
            "act_tokens": act_tokens,
            "short_tokens": short_tokens,
            "desc_tokens": desc_tokens,
            "act_nlp": act_nlp,
        })
    return tuple(preprocessed)


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


@lru_cache(maxsize=1)
def _load_preprocessed_kanoon() -> tuple[dict, ...]:
    """
    Load Kanoon database and pre-compute expensive operations.
    Returns tuple of dicts with preprocessed fields.
    """
    laws = load_kanoon_database()
    preprocessed = []
    for law in laws:
        title = law.get("title", "")
        source = law.get("source", "")
        place = law.get("place", "")

        # Pre-compute NLP tokens for title
        _, title_nlp = preprocess_query(title)

        preprocessed.append({
            "law": law,
            "title": title,
            "title_lower": title.lower(),
            "source_lower": source.lower(),
            "place_lower": place.lower(),
            "pub_date": law.get("published_date", ""),
            "title_nlp": title_nlp,
        })
    return tuple(preprocessed)


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

    # Use preprocessed data to avoid redundant computation
    preprocessed_laws = _load_preprocessed_laws()

    # Pre-compile regex pattern if needed for short_name matching
    scored: list[tuple[int, dict]] = []

    for prep in preprocessed_laws:
        score = 0
        law = prep["law"]

        # Use precomputed lowercase values
        act_name_lower = prep["act_name_lower"]
        short_name_lower = prep["short_name_lower"]
        category_lower = prep["category_lower"]
        year = prep["year"]

        # --- short_name matching ---
        if short_name_lower and short_name_lower == query_lower:
            score += 20
        elif short_name_lower and re.search(r"\b" + re.escape(short_name_lower) + r"\b", query_lower):
            score += 12
        else:
            short_tokens = prep["short_tokens"]
            if short_tokens and short_tokens == query_tokens:
                score += 16
            elif short_tokens and short_tokens <= query_tokens:
                score += 10

        # --- act_name matching ---
        if act_name_lower and act_name_lower == query_lower:
            score += 18

        # Use precomputed act_tokens
        act_tokens = prep["act_tokens"]
        score += len(act_tokens & query_tokens) * 3

        # --- NLP stemmed overlap (use precomputed NLP tokens) ---
        act_nlp = prep["act_nlp"]
        score += len(act_nlp & nlp_tokens) * 2

        # --- category matching ---
        if category_lower and category_lower in query_lower:
            score += 4

        # --- description keyword overlap (use precomputed tokens) ---
        desc_tokens = prep["desc_tokens"]
        score += len(desc_tokens & query_tokens)

        # --- year match ---
        if year and year_hint and year == year_hint:
            score += 2

        if score > 0:
            scored.append((score, law))

    # Use heap for efficient top-k selection instead of full sort
    if len(scored) <= max_results:
        scored.sort(key=lambda x: x[0], reverse=True)
        return [law for _, law in scored]
    else:
        # Get top max_results using heapq (more efficient than sorting all)
        top_scored = heapq.nlargest(max_results, scored, key=lambda x: x[0])
        return [law for _, law in top_scored]


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

    # Use preprocessed data
    preprocessed_kanoon = _load_preprocessed_kanoon()

    scored: list[tuple[int, dict]] = []
    for prep in preprocessed_kanoon:
        law = prep["law"]
        title_lower = prep["title_lower"]
        source_lower = prep["source_lower"]
        place_lower = prep["place_lower"]
        pub_date = prep["pub_date"]

        score = 0

        if title_lower == query_lower:
            score += 30
        elif query_lower in title_lower:
            score += 15
        elif title_lower in query_lower:
            score += 8

        # NLP token overlap with title (use precomputed)
        title_nlp = prep["title_nlp"]
        overlap = len(title_nlp & nlp_tokens)
        score += overlap * 3

        # Source / place match
        if query_lower in source_lower or query_lower in place_lower:
            score += 2

        # Year hint
        if year_hint and year_hint in pub_date:
            score += 2

        if score > 0:
            scored.append((score, law))

    # Use heap for efficient top-k selection
    if len(scored) <= max_results:
        scored.sort(key=lambda x: x[0], reverse=True)
        return [law for _, law in scored]
    else:
        top_scored = heapq.nlargest(max_results, scored, key=lambda x: x[0])
        return [law for _, law in top_scored]


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
