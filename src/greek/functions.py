
"""Functions that make the code a bit easier to read."""

from src.core.functions import lower_and_upper
from .constants import (ACCENT_MARKS, ALL_DIACRITICALS, BREATHING_MARKS, CONSONANTS, DIAERESIS_SYMBOL, SHORT_VOWELS, LONG_VOWELS, AMBIGUOUS_VOWELS, SUBSCRIPT_SYMBOL, VOWELS, GREEK_CONSONANT_CLUSTERS)


__all__ = ["lower_and_upper",
           "is_diacritical",
           "is_short_vowel",
           "is_long_vowel",
           "is_ambiguous_vowel",
           "is_vowel",
           "combinations",
           "normalize"]


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


def normalize(textblock: str) -> str:
    r"""Convert perseus text that uses the asterisk notation to text that uses
    capital betacode letters.
    
    Examples
    --------
    >>> text: str = "/>mh=nin a)/eide qea\ *phlhi+a/dew *)axilh=os"
    >>> text = normalize(text)
    >>> text
    '/>mh=nin a)/eide qea\\ Phlhi+a/dew A)xilh=os'
    """
    patterns: dict[str, str] = {}
    for letter in CONSONANTS:
        patterns.update({"*"+letter: letter.upper()})

    for vowel in VOWELS:
        for breathing in BREATHING_MARKS:
            for accent in ACCENT_MARKS:
                patterns.update({"*" + breathing + vowel: vowel.upper() + breathing})
                patterns.update({"*" + breathing + vowel + SUBSCRIPT_SYMBOL: vowel.upper() + breathing + accent + SUBSCRIPT_SYMBOL})
                patterns.update({"*" + breathing + vowel + DIAERESIS_SYMBOL: vowel.upper() + breathing + accent + DIAERESIS_SYMBOL})
                
                patterns.update({"*" + breathing + accent + vowel: vowel.upper() + breathing + accent})
                patterns.update({"*" + breathing + accent + vowel + SUBSCRIPT_SYMBOL: vowel.upper() + breathing + accent + SUBSCRIPT_SYMBOL})
                patterns.update({"*" + breathing + accent + vowel + DIAERESIS_SYMBOL: vowel.upper() + breathing + accent + DIAERESIS_SYMBOL})
                
    for pattern, solution in patterns.items():
        textblock = textblock.replace(pattern, solution)

    return textblock