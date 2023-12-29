
from .constants import (ALL_DIACRITICS, LATIN_CHARSET, SHORT_VOWELS, LONG_VOWELS, AMBIGUOUS_VOWELS, VOWELS, SPACES, PUNCTUATION)


__all__ = ["lower_and_upper",
           "is_diacritical",
           "is_letter",
           "is_short_vowel",
           "is_long_vowel",
           "is_ambiguous_vowel",
           "is_vowel",
           "is_space",
           "is_punctuation",
           "is_endpoint"]

def lower_and_upper(string: str) -> str:
    """Return a concatenation of the lower + uppercase 
    versions of a given [string]."""
    return string.lower() + string.upper()

def is_capital(char: str) -> bool:
    return char in LATIN_CHARSET.upper()

def is_diacritical(char: str) -> bool:
    return char in ALL_DIACRITICS

def is_letter(char: str) -> bool:
    return char in lower_and_upper(LATIN_CHARSET)
        
def is_short_vowel(char: str) -> bool:
    return char in lower_and_upper(SHORT_VOWELS)

def is_long_vowel(char: str) -> bool:
    return char in lower_and_upper(LONG_VOWELS)

def is_ambiguous_vowel(char: str) -> bool:
    return char in lower_and_upper(AMBIGUOUS_VOWELS)

def is_vowel(char: str) -> bool:
    return char in lower_and_upper(VOWELS)

def is_space(char: str) -> bool:
    return char in SPACES

def is_punctuation(char: str) -> bool:
    return char in PUNCTUATION

def is_endpoint(char: str) -> bool:
    return is_punctuation(char) or is_space(char)
