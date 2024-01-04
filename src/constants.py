"""
Constant values used in the program."""

# Character strings and categories
LATIN_CHARSET: str = "abcdefghijklmnopqrstuvwxyz"
GREEK_CHARSET: str = "αβξδεφγηιςκλμνοπθρστυϝωχψζ"
ALPHA: str = "a"
EPSILON: str = "e"
OMICRON: str = "o"
ETA: str = "h"
OMEGA: str = "w"
IOTA: str = "i"
UPSILON: str = "u"
RHO: str = "r"
SHORT_VOWELS: str = EPSILON + OMICRON
LONG_VOWELS: str = ETA + OMEGA
AMBIGUOUS_VOWELS: str = ALPHA + IOTA + UPSILON

ROUGH_SYMBOL: str = "("
SMOOTH_SYMBOL: str = ")"
ACUTE_SYMBOL: str = "/"
GRAVE_SYMBOL: str = "\\"
CIRCUMFLEX_SYMBOL: str = "="
SUBSCRIPT_SYMBOL: str = "|"
DIAERESIS_SYMBOL: str = "+"
MACRON_SYMBOL: str = "_"
BREVE_SYMBOL: str = "-"

LATIN_PUNCTUATION: str = ".,;:?'\"'’"
GREEK_PUNCTUATION: str = ".,·:;'\"'’"
SPACES: str = " "

HIGH_VOWELS: str = IOTA + UPSILON
LENGTH_MARKS: str = MACRON_SYMBOL + BREVE_SYMBOL
VOWELS: str = SHORT_VOWELS + LONG_VOWELS + AMBIGUOUS_VOWELS
BREATHING_MARKS: str = SMOOTH_SYMBOL + ROUGH_SYMBOL
ACCENT_MARKS: str = ACUTE_SYMBOL + GRAVE_SYMBOL + CIRCUMFLEX_SYMBOL

ALL_DIACRITICALS: str = BREATHING_MARKS + ACCENT_MARKS + \
    SUBSCRIPT_SYMBOL + DIAERESIS_SYMBOL

DIACRITICAL_CATEGORIES: list[str] = [BREATHING_MARKS,
                                     ACCENT_MARKS,
                                     SUBSCRIPT_SYMBOL,
                                     DIAERESIS_SYMBOL]

VALID_BETACODE_CHARACTERS: str = LATIN_CHARSET + LATIN_CHARSET.upper() + \
    LATIN_PUNCTUATION + ALL_DIACRITICALS + SPACES + "\n"

GREEK_CONSONANT_CLUSTERS: dict[str, str] = {"ps": "y", "ks": "c"}

# Unicode character block: rows

# This section mostly conforms to the unicode columns, below.
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

# This section needs to be treated specially.
SIMPLE_ACCENTS: int = 0x1F70

# This section also supplies empty diacritics, rho, and diaereses, so
# it needs to be treated specially.
ALPHA_SPECIAL: int = 0x1FB0
ETA_SPECIAL: int = 0x1FC0
IOTA_SPECIAL: int = 0x1FD0
UPSILON_SPECIAL: int = 0x1FE0
OMEGA_SPECIAL: int = 0x1FF0

# Unicode character block: columns

# For rows 1F0x through 1FAx, except 1F7x
LOWER_WITH_SMOOTH: int = 0x0
LOWER_WITH_ROUGH: int = 0x1
LOWER_WITH_SMOOTH_GRAVE: int = 0x2
LOWER_WITH_ROUGH_GRAVE: int = 0x3
LOWER_WITH_SMOOTH_ACUTE: int = 0x4
LOWER_WITH_ROUGH_ACUTE: int = 0x5
LOWER_WITH_SMOOTH_CIRCUMFLEX: int = 0x6
LOWER_WITH_ROUGH_CIRCUMFLEX: int = 0x7
UPPER_WITH_SMOOTH: int = 0x8
UPPER_WITH_ROUGH: int = 0x9
UPPER_WITH_SMOOTH_GRAVE: int = 0xA
UPPER_WITH_ROUGH_GRAVE: int = 0xB
UPPER_WITH_SMOOTH_ACUTE: int = 0xC
UPPER_WITH_ROUGH_ACUTE: int = 0xD
UPPER_WITH_SMOOTH_CIRCUMFLEX: int = 0xE
UPPER_WITH_ROUGH_CIRCUMFLEX: int = 0xF

