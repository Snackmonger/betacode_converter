"""Functions to make the syntax prettier."""

from .constants import LATIN_CHARSET, LATIN_PUNCTUATION, SPACES

def is_endpoint(char: str) -> bool:
    return is_punctuation(char) or is_space(char)

def is_space(char: str) -> bool:
    return char in SPACES

def is_punctuation(char: str) -> bool:
    return char in LATIN_PUNCTUATION

def is_letter(char: str) -> bool:
    return char in lower_and_upper(LATIN_CHARSET)
        
def lower_and_upper(string: str) -> str:
    """Return a concatenation of the lower + uppercase 
    versions of a given [string]."""
    return string.lower() + string.upper()

def is_capital(char: str) -> bool:
    return char in LATIN_CHARSET.upper()