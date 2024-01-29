"""Tokens used in the program (base class & default token(s))."""

from .constants import ESCAPE_CHAR

class SymbolGroup:
    """
    Base class to represent a symbolic token made up of one or more 
    sub-symbols.

    This class provides the interfaces that the token crawler uses to
    generate tokens and that the renderer uses to create the final output.

    Notes
    -----
    Subclasses are responsible for supplying their own ``valid_radicals`` and 
    ``valid_coefficients`` in their class definition. These consist of strings
    of valid characters for each category.

    Subclasses are responsible for supplying their own 
    ``fix_character_conflicts`` method to define conflict resolution for the 
    generated symbols.
    """
    valid_radicals: str
    valid_coefficients: str

    def __init__(self, radical: str):
        self.radical: str = radical
        self.coefficients: str = str()

        self.is_final: bool = False
        self.is_initial: bool = False
        self.is_medial: bool = False

        self.suppressed_chars: str = ""
        self.redefined_chars: dict[str, str] = {}

    @property
    def symbol(self) -> str:
        """The complete chain of characters in the symbol."""
        return self.radical + self.coefficients
    
    @property
    def is_monograph(self) -> bool:
        """True, if the symbol consists only of a radical."""
        return len(self.symbol) == 1

    def add_coefficient(self, coefficient: str) -> None:
        """Add a given coefficient to the symbol."""
        if self.is_valid_coefficient(coefficient) and not coefficient in self.coefficients:
            self.coefficients += coefficient

    def is_valid_radical(self, radical: str) -> bool:
        """True, if the radical is recognized."""
        return len(radical) == 1 and radical in self.valid_radicals
    
    def is_valid_coefficient(self, coefficient: str) -> bool:
        """True, if the coefficient is recognized."""
        return len(coefficient) == 1 and coefficient in self.valid_coefficients
    
    def suppress_char(self, char: str) -> None:
        """Suppress a character so that it is ignored in the rendering."""
        if not char in self.suppressed_chars:
            self.suppressed_chars += char

    def redefine_char(self, char: str, new_char: str) -> None:
        """Redefine the render mapping for a given character."""
        if not char in self.redefined_chars:
            self.redefined_chars.update({char: new_char})

    def is_renderable(self, char: str) -> bool:
        """True, if the character is recognized and not suppressed."""
        char_is_valid: bool = self.is_valid_coefficient(char) or self.is_valid_radical(char)
        return char not in self.suppressed_chars and char_is_valid
    
    def members(self, category: str) -> str:
        """Return any members of a given category found in the coefficients."""
        output: str = ""
        for member in category:
            if member in self.coefficients:
                output += member
        return output

    def keep_first_member_only(self, category: str) -> None:
        """Check the coefficient for multiple members of the given category,
        and suppress all but the first."""
        first: str = ""
        for member in self.coefficients:
            if member in category:
                first = member
                break
        suppressions: str = category.replace(first, "")
        for member in self.coefficients:
            if member in suppressions:
                self.suppress_char(member)
    
    def fix_character_conflicts(self) -> None:
        """
        Fix any character conflicts by suppressing characters or redefining
        them as a different character. (This method must be overwritten in
        subclasses to provide specific resolution strategies for their 
        rendering format.)
        """
        raise NotImplementedError


class EscapeSequenceToken(SymbolGroup):
    """Token to allow the user to signify that the character following
    the escape character is to be rendered in its current form.."""
    valid_radicals: str = ESCAPE_CHAR
    valid_coefficients: str = ""

    def __repr__(self) -> str:
        return self.coefficients
    
    # These methods are not necessary in the context of an escape sequence.
    # They're just here to fulfill the interface contract.
    def fix_character_conflicts(self) -> None:
        return 
    def is_valid_coefficient(self, coefficient: str) -> bool:
        return True
