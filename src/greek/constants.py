"""
Constant values used for parsing and rendering Greek beta code."""

from src.core.constants import LATIN_CHARSET, SPACES, LATIN_PUNCTUATION

# Character strings and categories
GREEK_CHARSET: str = "αβξδεφγηιςκλμνοπθρστυϝωχψζ"
GREEK_PUNCTUATION: str = ".,·:;'\"'’"

# Symbols that can serve as the radical of a complex character.
ALPHA: str = "a"
EPSILON: str = "e"
OMICRON: str = "o"
ETA: str = "h"
OMEGA: str = "w"
IOTA: str = "i"
UPSILON: str = "u"
RHO: str = "r"
CONSONANTS: str = "bcdfgjklmnpqrstwxyz"

# Symbols that can serve as coefficients of a radical, or if they are not
# attached to a radical, as radicals themselves.
ROUGH_SYMBOL: str = "("
SMOOTH_SYMBOL: str = ")"
ACUTE_SYMBOL: str = "/"
GRAVE_SYMBOL: str = "\\"
CIRCUMFLEX_SYMBOL: str = "="
SUBSCRIPT_SYMBOL: str = "|"
DIAERESIS_SYMBOL: str = "+"
MACRON_SYMBOL: str = "_"
BREVE_SYMBOL: str = "-"

# Categories used in the program
SHORT_VOWELS: str = EPSILON + OMICRON
LONG_VOWELS: str = ETA + OMEGA
AMBIGUOUS_VOWELS: str = ALPHA + IOTA + UPSILON
HIGH_VOWELS: str = IOTA + UPSILON
LENGTH_MARKS: str = MACRON_SYMBOL + BREVE_SYMBOL
VOWELS: str = SHORT_VOWELS + LONG_VOWELS + AMBIGUOUS_VOWELS
BREATHING_MARKS: str = SMOOTH_SYMBOL + ROUGH_SYMBOL
ACCENT_MARKS: str = ACUTE_SYMBOL + GRAVE_SYMBOL + CIRCUMFLEX_SYMBOL
ALL_DIACRITICALS: str = BREATHING_MARKS + ACCENT_MARKS + \
    SUBSCRIPT_SYMBOL + DIAERESIS_SYMBOL + LENGTH_MARKS


DIACRITICAL_CATEGORIES: list[str] = [BREATHING_MARKS,
                                     ACCENT_MARKS,
                                     SUBSCRIPT_SYMBOL,
                                     DIAERESIS_SYMBOL,
                                     LENGTH_MARKS]

VALID_BETACODE_CHARACTERS: str = LATIN_CHARSET + LATIN_CHARSET.upper() + \
    LATIN_PUNCTUATION + ALL_DIACRITICALS + SPACES + "\n"


GREEK_CONSONANT_CLUSTERS: dict[str, str] = {"ps": "y", "ks": "c"}

# Unicode character rows
# ----------------------
# See /docs/unicode.rst for details.
ALPHA_DIACRITICALS: int = 0x1F00
EPSILON_DIACRITICALS: int = 0x1F10
ETA_DIACRITICALS: int = 0x1F20
IOTA_DIACRITICALS: int = 0x1F30
OMICRON_DIACRITICALS: int = 0x1F40
UPSILON_DIACRITICALS: int = 0x1F50
OMEGA_DIACRITICALS: int = 0x1F60
ALPHA_SUBSCRIPT_DIACRITICALS: int = 0x1F80
ETA_SUBSCRIPT_DIACRITICALS: int = 0x1F90
OMEGA_SUBSCRIPT_DIACRITICALS: int = 0x1FA0

# Simple accents: This section needs to be treated specially.
SIMPLE_ACCENTS: int = 0x1F70

# Special accents: This section needs to be treated specially.
ALPHA_SPECIAL: int = 0x1FB0
ETA_SPECIAL: int = 0x1FC0
IOTA_SPECIAL: int = 0x1FD0
UPSILON_SPECIAL: int = 0x1FE0
OMEGA_SPECIAL: int = 0x1FF0
