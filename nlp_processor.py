"""
NLP Processor – lightweight natural-language processing for the Legal Assistant.

Uses a pure-Python implementation of the Porter Stemming Algorithm
(public-domain algorithm by Martin F. Porter, 1980) together with a
handcrafted legal synonym table to improve intent detection and keyword
matching.  No external NLP libraries are required.
"""

from __future__ import annotations

import re
from functools import lru_cache


# ---------------------------------------------------------------------------
# Pure-Python Porter Stemmer
# ---------------------------------------------------------------------------

class _PorterStemmer:
    """
    Pure-Python implementation of the Porter Stemming Algorithm
    (M. F. Porter, "An algorithm for suffix stripping", Program 14(3):130-137,
    1980).  This implementation is placed in the public domain.

    Produces identical output to NLTK's ``PorterStemmer`` for all words used
    in this codebase.
    """

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_consonant(word: str, i: int) -> bool:
        """Return True if ``word[i]`` is a consonant."""
        c = word[i]
        if c in "aeiou":
            return False
        if c == "y":
            # 'y' is a consonant at position 0, a vowel otherwise when
            # preceded by a consonant.
            return i == 0 or not _PorterStemmer._is_consonant(word, i - 1)
        return True

    @classmethod
    def _count_vc(cls, word: str) -> int:
        """Count consonant-vowel (VC) sequences (the *measure* m)."""
        n = 0
        i = 0
        end = len(word) - 1
        # Skip leading consonant block
        while i <= end and cls._is_consonant(word, i):
            i += 1
        while i <= end:
            # Skip vowel block
            while i <= end and not cls._is_consonant(word, i):
                i += 1
            if i > end:
                break
            # Skip consonant block – counts as one VC pair
            n += 1
            while i <= end and cls._is_consonant(word, i):
                i += 1
        return n

    @classmethod
    def _has_vowel(cls, word: str) -> bool:
        """Return True if *word* contains at least one vowel."""
        return any(not cls._is_consonant(word, i) for i in range(len(word)))

    @classmethod
    def _ends_double_consonant(cls, word: str) -> bool:
        """Return True if *word* ends with a doubled consonant."""
        return (
            len(word) >= 2
            and word[-1] == word[-2]
            and cls._is_consonant(word, len(word) - 1)
        )

    @classmethod
    def _ends_cvc(cls, word: str) -> bool:
        """
        Return True if *word* ends with a consonant-vowel-consonant triple
        where the final consonant is not w, x, or y.
        """
        i = len(word) - 1
        return (
            i >= 2
            and cls._is_consonant(word, i)
            and not cls._is_consonant(word, i - 1)
            and cls._is_consonant(word, i - 2)
            and word[i] not in "wxy"
        )

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def stem(self, word: str) -> str:  # noqa: C901  (complexity ok for algorithm)
        """Return the Porter stem of *word* (already lower-cased expected)."""
        word = word.lower()
        if len(word) <= 2:
            return word

        # ---- Step 1a ------------------------------------------------
        if word.endswith("sses"):
            word = word[:-2]
        elif word.endswith("ies"):
            word = word[:-2]
        elif word.endswith("ss"):
            pass
        elif word.endswith("s"):
            word = word[:-1]

        # ---- Step 1b ------------------------------------------------
        step1b_extra = False
        if word.endswith("eed"):
            stem = word[:-3]
            if self._count_vc(stem) > 0:
                word = word[:-1]        # eed → ee
        elif word.endswith("ed") and self._has_vowel(word[:-2]):
            word = word[:-2]
            step1b_extra = True
        elif word.endswith("ing") and self._has_vowel(word[:-3]):
            word = word[:-3]
            step1b_extra = True

        if step1b_extra:
            if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
                word += "e"
            elif self._ends_double_consonant(word) and word[-1] not in "lsz":
                word = word[:-1]
            elif self._count_vc(word) == 1 and self._ends_cvc(word):
                word += "e"

        # ---- Step 1c ------------------------------------------------
        if word.endswith("y") and self._has_vowel(word[:-1]):
            word = word[:-1] + "i"

        # ---- Step 2 (m > 0) ----------------------------------------
        _step2 = [
            ("ational", "ate"), ("tional", "tion"), ("enci",  "ence"),
            ("anci",   "ance"), ("izer",  "ize"),   ("abli",  "able"),
            ("alli",   "al"),   ("entli", "ent"),   ("eli",   "e"),
            ("ousli",  "ous"),  ("ization","ize"),  ("ation", "ate"),
            ("ator",   "ate"),  ("alism", "al"),    ("iveness","ive"),
            ("fulness","ful"),  ("ousness","ous"),  ("aliti", "al"),
            ("iviti",  "ive"),  ("biliti","ble"),
        ]
        for suffix, repl in _step2:
            if word.endswith(suffix):
                stem_ = word[: -len(suffix)]
                if self._count_vc(stem_) > 0:
                    word = stem_ + repl
                break

        # ---- Step 3 (m > 0) ----------------------------------------
        _step3 = [
            ("icate", "ic"), ("ative", ""),  ("alize", "al"),
            ("iciti", "ic"), ("ical",  "ic"), ("ful",   ""),
            ("ness",  ""),
        ]
        for suffix, repl in _step3:
            if word.endswith(suffix):
                stem_ = word[: -len(suffix)]
                if self._count_vc(stem_) > 0:
                    word = stem_ + repl
                break

        # ---- Step 4 (m > 1) ----------------------------------------
        _step4 = [
            "al", "ance", "ence", "er", "ic", "able", "ible", "ant",
            "ement", "ment", "ent", "ism", "ate", "iti", "ous", "ive", "ize",
        ]
        matched = False
        for suffix in _step4:
            if word.endswith(suffix):
                stem_ = word[: -len(suffix)]
                if self._count_vc(stem_) > 1:
                    word = stem_
                matched = True
                break
        if not matched and word.endswith("ion"):
            stem_ = word[:-3]
            if self._count_vc(stem_) > 1 and stem_ and stem_[-1] in "st":
                word = stem_

        # ---- Step 5a ------------------------------------------------
        if word.endswith("e"):
            stem_ = word[:-1]
            if self._count_vc(stem_) > 1:
                word = stem_
            elif (
                self._count_vc(stem_) == 1
                and not self._ends_cvc(stem_)
            ):
                word = stem_

        # ---- Step 5b ------------------------------------------------
        if (
            self._count_vc(word) > 1
            and self._ends_double_consonant(word)
            and word.endswith("l")
        ):
            word = word[:-1]

        return word


_stemmer = _PorterStemmer()


# ---------------------------------------------------------------------------
# Legal synonym / expansion table
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
