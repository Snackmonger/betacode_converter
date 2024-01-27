"""Common constants used by multiple modules."""

from enum import Enum

LATIN_CHARSET: str = "abcdefghijklmnopqrstuvwxyz"
LATIN_VOWELS: str = "aeiouy"
LATIN_CONSONANTS: str = "bcdfghjklmnpqrstvwxyz"
LATIN_PUNCTUATION: str = ".,;:?'\"'’"
SPACES: str = " "
ESCAPE_CHAR: str = "%"



class TkinterEventTypes(Enum):
    """Tkinter event types used in the program's operation."""
    KEY_PRESS = "<KeyPress>"
    KEY_RELEASE = "<KeyRelease>"
