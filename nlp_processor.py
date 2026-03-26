"""
NLP Processor – lightweight natural-language processing for the Legal Assistant.

Uses NLTK's PorterStemmer (no corpus download needed) plus a handcrafted legal
synonym table to improve intent detection and keyword matching.
"""

from __future__ import annotations

import re
from functools import lru_cache

from nltk.stem import PorterStemmer

_stemmer = PorterStemmer()

# ---------------------------------------------------------------------------
# Legal synonym / expansion table
# Maps common user phrasings to canonical legal keywords
# ---------------------------------------------------------------------------
_SYNONYMS: dict[str, list[str]] = {
    "fired":        ["dismiss", "terminat", "sack", "remov", "laid off"],
    "fire":         ["dismiss", "terminat", "sack"],
    "job":          ["employ", "work", "labour", "labor", "wage"],
    "boss":         ["employ", "manag"],
    "pay":          ["wage", "salari", "compensat"],
    "salary":       ["wage", "pay", "earn"],
    "beat":         ["violenc", "assaul", "abus"],
    "hit":          ["violenc", "assaul", "abus"],
    "cheat":        ["fraud", "deceiv", "misrepresent"],
    "scam":         ["fraud", "cheat", "deceiv"],
    "stolen":       ["theft", "steal", "rob"],
    "theft":        ["steal", "rob", "burglari"],
    "rape":         ["sexual assaul", "molestat"],
    "harass":       ["molestat", "stalk", "sexual harass"],
    "evict":        ["evict", "tenant", "rent"],
    "house":        ["properti", "tenant", "landlord", "rent"],
    "rent":         ["tenant", "landlord", "leas"],
    "land":         ["properti", "encroach", "title"],
    "police":       ["arrest", "fir", "crimin", "jail"],
    "arrested":     ["arrest", "custodi", "detain", "bail"],
    "jail":         ["custodi", "arrest", "bail", "prison"],
    "court":        ["judici", "litigation", "lawsuit", "legal"],
    "sue":          ["lawsuit", "litigation", "legal action"],
    "help":         ["assist", "aid", "support"],
    "old":          ["senior", "elder", "pension"],
    "pension":      ["senior", "elder", "retir"],
    "disabled":     ["disabl", "handicap", "impair"],
    "disability":   ["disabl", "udid", "handicap"],
    "child":        ["minor", "children", "underage", "juvenile"],
    "kid":          ["child", "minor", "children"],
    "hack":         ["cybercrim", "cyber", "data breach"],
    "online":       ["cyber", "internet", "digit"],
    "upi":          ["cybercrim", "fraud", "payment"],
    "otp":          ["phish", "cyber", "fraud"],
    "caste":        ["sc", "st", "dalit", "atrociti", "discriminat"],
    "atrocity":     ["sc", "st", "dalit", "discriminat"],
    "information":  ["rti", "transpar", "govern"],
    "government":   ["public author", "rti", "govern"],
    "constitution": ["fundament", "right", "articl"],
    "rights":       ["fundament", "constitut", "protect"],
    "maternity":    ["women", "pregnanc", "matern"],
    "dowry":        ["domest violenc", "harass", "marriag"],
    "pregnant":     ["matern", "women"],
    "woman":        ["women", "female", "gender"],
    "women":        ["gender", "female", "posh"],
}

# Stop words excluded from scoring
_STOP_WORDS = frozenset({
    "the", "of", "and", "in", "to", "a", "an", "for", "is", "are", "was",
    "were", "what", "tell", "me", "about", "explain", "how", "does", "it",
    "its", "that", "this", "with", "by", "under", "which", "who", "when",
    "where", "why", "do", "india", "indian", "act", "law", "section",
    "right", "rights", "i", "my", "our", "we", "you", "please", "want",
    "need", "can", "should", "would", "get", "have", "been",
})


@lru_cache(maxsize=2048)
def stem(word: str) -> str:
    """Return the Porter stem of a single word (cached)."""
    return _stemmer.stem(word.lower())


def tokenise(text: str) -> list[str]:
    """
    Return a list of Porter-stemmed tokens (stop words excluded).
    Preserves duplicates so frequency can be counted by callers.
    """
    words = re.findall(r"[a-zA-Z\u0900-\u097F]+", text)
    return [stem(w) for w in words if w.lower() not in _STOP_WORDS]


def expand_synonyms(tokens: list[str]) -> set[str]:
    """
    Given a list of stemmed tokens, return a set that includes both the
    original tokens and any synonym-expanded stems.
    """
    result: set[str] = set(tokens)
    for token in tokens:
        for original, stems in _SYNONYMS.items():
            if stem(original) == token:
                result.update(stems)
    return result


def nlp_score(query_tokens: set[str], candidate_text: str) -> int:
    """
    Score *candidate_text* against a set of stemmed query tokens.
    Returns an integer score (higher = better match).
    """
    cand_tokens = set(tokenise(candidate_text))
    overlap = query_tokens & cand_tokens
    return len(overlap)


def preprocess_query(text: str) -> tuple[list[str], set[str]]:
    """
    Tokenise, stem, and expand synonyms for a query string.

    Returns (raw_tokens, expanded_token_set).
    """
    tokens = tokenise(text)
    expanded = expand_synonyms(tokens)
    return tokens, expanded


def extract_year(text: str) -> str | None:
    """Extract a four-digit year (1800-2030) from text, or return None."""
    match = re.search(r"\b(1[89]\d{2}|20[0-2]\d)\b", text)
    return match.group(1) if match else None
