"""Functions that make the syntax easier to read."""

from src.functions import lower_and_upper
from .constants import (ALL_DIACRITICALS, SHORT_VOWELS, LONG_VOWELS, AMBIGUOUS_VOWELS, VOWELS, GREEK_CONSONANT_CLUSTERS)


__all__ = ["lower_and_upper",
           "is_diacritical",
           "is_short_vowel",
           "is_long_vowel",
           "is_ambiguous_vowel",
           "is_vowel"]


def is_diacritical(char: str) -> bool:
    return char in ALL_DIACRITICALS

def is_short_vowel(char: str) -> bool:
    return char in lower_and_upper(SHORT_VOWELS)

def is_long_vowel(char: str) -> bool:
    return char in lower_and_upper(LONG_VOWELS)

def is_ambiguous_vowel(char: str) -> bool:
    return char in lower_and_upper(AMBIGUOUS_VOWELS)

def is_vowel(char: str) -> bool:
    return char in lower_and_upper(VOWELS)

def combinations() -> list[str]:
        """ks Ks kS KS, etc."""
        combinations_: list[str] = list(GREEK_CONSONANT_CLUSTERS)
        combinations_.extend([x.capitalize() for x in combinations_])
        combinations_.extend([x[:-1] + x[-1].upper() for x in combinations_])
        return combinations_
