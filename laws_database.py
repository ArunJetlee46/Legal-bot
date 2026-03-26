"""
Laws database — loads indian_laws_and_acts_v2.csv and provides search helpers.

Each row in the CSV has the following columns:
  act_name, short_name, year, category, description,
  key_provisions, enforcing_authority, helpline, portal, status

``key_provisions`` uses a pipe (|) as an item separator.
"""

from __future__ import annotations

import csv
import os
import re
from functools import lru_cache

# Path to the data file (relative to this module's directory)
_CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "indian_laws_and_acts_v2.csv")

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
    Load the CSV once and return it as an immutable tuple of dicts.
    Returns an empty tuple if the CSV cannot be read.
    """
    if not os.path.exists(_CSV_PATH):
        return ()
    laws: list[dict] = []
    with open(_CSV_PATH, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            laws.append(dict(row))
    return tuple(laws)


def _tokenise(text: str) -> set[str]:
    """Return lowercase word tokens minus stop words."""
    return set(re.findall(r"\w+", text.lower())) - _STOP_WORDS


def search_law(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the laws database for laws matching *query*.

    Scoring (higher is better):
    - Exact short_name match:              20 pts
    - short_name contained in query
      or query contained in short_name:   12 pts
    - Exact act_name match:               18 pts
    - Act-name keyword overlap:            3 pts/word
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

    scored: list[tuple[int, dict]] = []
    for law in load_laws_database():
        score = 0
        act_name = law.get("act_name", "").lower()
        short_name = law.get("short_name", "").lower()
        category = law.get("category", "").lower()
        description = law.get("description", "").lower()
        year = law.get("year", "").strip()

        # --- short_name matching (whole-word only to avoid false positives) ---
        if short_name and short_name == query_lower:
            score += 20
        elif short_name and re.search(r"\b" + re.escape(short_name) + r"\b", query_lower):
            score += 12
        else:
            # Token-level overlap with short_name (handles "POCSO" matching "POCSO Act")
            short_tokens = _tokenise(short_name)
            if short_tokens and short_tokens == query_tokens:
                # All short_name tokens exactly match query tokens
                score += 16
            elif short_tokens and short_tokens <= query_tokens:
                # All short_name tokens are contained in query
                score += 10

        # --- act_name matching ---
        if act_name and act_name == query_lower:
            score += 18

        act_tokens = _tokenise(law.get("act_name", ""))
        score += len(act_tokens & query_tokens) * 3

        # --- category matching ---
        if category and category in query_lower:
            score += 4

        # --- description keyword overlap ---
        desc_tokens = _tokenise(description)
        score += len(desc_tokens & query_tokens)

        # --- year match ---
        if year and year in query_lower:
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
