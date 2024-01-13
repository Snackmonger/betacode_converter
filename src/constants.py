"""Common constants used by multiple modules."""

from enum import Enum

LATIN_CHARSET: str = "abcdefghijklmnopqrstuvwxyz"
LATIN_PUNCTUATION: str = ".,;:?'\"'’"
SPACES: str = " "



class TkinterEventTypes(Enum):
    """Tkinter event types used in the program's operation."""
    KEY_PRESS = "<KeyPress>"
    KEY_RELEASE = "<KeyRelease>"
