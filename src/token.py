
from .constants import (ACCENT_MARKS,
                        ALL_DIACRITICALS,
                        AMBIGUOUS_VOWELS,
                        BREATHING_MARKS,
                        CIRCUMFLEX_SYMBOL,
                        DIAERESIS_SYMBOL, GREEK_CONSONANT_CLUSTERS,
                        HIGH_VOWELS,
                        LENGTH_MARKS,
                        LONG_VOWELS, RHO,
                        ROUGH_SYMBOL,
                        SHORT_VOWELS,
                        SMOOTH_SYMBOL,
                        SUBSCRIPT_SYMBOL,
                        UPSILON,
                        VALID_BETACODE_CHARACTERS)

from .keywords import (SHORT, 
                       LONG, 
                       AMBIGUOUS)
from .functions import lower_and_upper
from .rendering import (render_betacode_vowel, 
                        render_simple_betacode)


__all__ = ["SymbolGroup",
           "BetacodeToken",
           "BetacodeComplexVowelToken",
           ]


class SymbolGroup:
    """
    Base class to represent a symbol made up of one or more sub-symbols.

    This class provides the interfaces that the token crawler uses to
    generate tokens and that the renderer uses to create the final output.

    Notes
    -----
    Subclasses are responsible for supplying their own ``valid_radicals`` and 
    ``valid_coefficients`` in their class definition. 

    Subclasses are responsible for supplying their own 
    ``fix_character_conflicts`` method to define conflict resolution.
    """
    valid_radicals: str
    valid_coefficients: str
    def __init__(self, radical: str):
        if not self.is_valid_radical(radical):
            raise ValueError(f"Unrecognized radical: {radical}\n\
                             Valid radicals = {self.valid_radicals}")
        self.radical: str = radical
        self.coefficients: str = str()

        self.is_final: bool = False
        self.is_initial: bool = False
        self.is_medial: bool = False

        self.suppressed_chars: str = ""
        self.redefined_chars: dict[str, str] = {}

    @property
    def symbol(self) -> str:
        return self.radical+self.coefficients
    
    @property
    def is_monograph(self) -> bool:
        return len(self.symbol) == 1

    def add_coefficient(self, coefficient: str) -> None:
        if self.is_valid_coefficient(coefficient) and not coefficient in self.coefficients:
            self.coefficients += coefficient

    def remove_coefficient(self, coefficient: str) -> None:
        if coefficient in self.coefficients:
            self.coefficients.replace(coefficient, "")

    def is_valid_radical(self, radical: str) -> bool:
        return len(radical) == 1 and radical in self.valid_radicals
    
    def is_valid_coefficient(self, coefficient: str) -> bool:
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



class BetacodeToken(SymbolGroup):
    """
    Token to represent a generic betacode monographic symbol.
    """
    valid_radicals = VALID_BETACODE_CHARACTERS
    valid_coefficients = ALL_DIACRITICALS
    def __init__(self, radical: str):
        super().__init__(radical)
        
    def fix_character_conflicts(self) -> None:
        if self.is_monograph and self.radical == "s" and self.is_final:
            self.redefine_char("s", "j")

    def __repr__(self):
        self.fix_character_conflicts()
        if self.is_monograph:
            return render_simple_betacode(self.radical)
        
        # If this token was created by the tokenizer, we expect it should be
        # a monograph. If we reached this point, either the tokenizer made a
        # mistake (unlikely), or the user has injected a malformed token for
        # some reason. 
        conversion: str = "".join(filter(self.is_renderable, self.symbol))
        for subsymbol in conversion:
            if subsymbol in self.redefined_chars:
                conversion = conversion.replace(subsymbol,
                                     self.redefined_chars[subsymbol])

        return render_simple_betacode(conversion)



class BetacodeComplexVowelToken(SymbolGroup):
    """
    Token to represent a complex vowel symbol in betacode.

    Class Overview
    --------------
    State: The basic precursors for symbol creation.
    Behaviour: Correcting conflicting character codes and forwarding the final
    codes to the betacode rendering function.
    """
    valid_radicals = VALID_BETACODE_CHARACTERS
    valid_coefficients = ALL_DIACRITICALS
    def __init__(self, radical: str) -> None:
        super().__init__(radical)
        
    @property
    def __length(self) -> str:
        if self.radical in lower_and_upper(LONG_VOWELS):
            return LONG
        if self.radical in lower_and_upper(SHORT_VOWELS):
            return SHORT
        if self.radical in lower_and_upper(AMBIGUOUS_VOWELS):
            return AMBIGUOUS
        else:
            raise ValueError(
                f"Radical {self.radical} cannot be resolved to a vowel.")

    @property
    def __has_subscript(self) -> bool:
        return SUBSCRIPT_SYMBOL in self.coefficients

    @property
    def __has_diaeresis(self) -> bool:
        return DIAERESIS_SYMBOL in self.coefficients

    def fix_character_conflicts(self):
        """Suppress any characters that conflict with the combined sign, or 
        re-define them so that they point to an acceptable substitute.
        
        The actual radical and coefficient of the token never change; this 
        method simply instructs the renderer to ignore a member character, 
        or render it a different way than written.
        """

        def accent_mark():
            return self.members(ACCENT_MARKS)
        def breathing_mark():
            return self.members(BREATHING_MARKS)
        def length_mark():
            return self.members(LENGTH_MARKS)
        def is_high_vowel():
            return self.radical in lower_and_upper(HIGH_VOWELS)

        # No more than one accent, breathing, or length mark.
        if len(accent_mark()) > 1:
            self.keep_first_member_only(ACCENT_MARKS)
        if len(breathing_mark()) > 1:
            self.keep_first_member_only(BREATHING_MARKS)
        if len(length_mark()) > 1:
            self.keep_first_member_only(LENGTH_MARKS)
        
        # Majuscule upsilon must have rough breathing or none at all.
        if self.radical == UPSILON.upper() and breathing_mark() == SMOOTH_SYMBOL:
            self.redefine_char(SMOOTH_SYMBOL, ROUGH_SYMBOL)

        if accent_mark() == CIRCUMFLEX_SYMBOL and not breathing_mark() and self.radical.isupper():
            self.suppress_char(CIRCUMFLEX_SYMBOL)

        if self.__length == SHORT:
            # Circumflex can only exist on long (or ambiguously long) vowels
            if accent_mark() == CIRCUMFLEX_SYMBOL:
                self.suppress_char(accent_mark())
            # Subscript can only exist on long vowels and ambiguously long alpha.
            if self.__has_subscript:
                self.suppress_char(SUBSCRIPT_SYMBOL)

        if length_mark():
            # Length marks can only exist on ambiguous vowels.
            if not self.radical in lower_and_upper(AMBIGUOUS_VOWELS):
                self.suppress_char(length_mark())
            # Length mark cannot combine with other diacriticals.
            if breathing_mark() or accent_mark() or self.__has_diaeresis \
                    or self.__has_subscript:
                self.suppress_char(length_mark())

        # Subscript cannot exist on high vowels.
        if self.__has_subscript and is_high_vowel():
            self.suppress_char(SUBSCRIPT_SYMBOL)

        # Diaeresis can only exist on high vowels.
        if self.__has_diaeresis:
            if not is_high_vowel():
                self.suppress_char(DIAERESIS_SYMBOL)


    def __repr__(self) -> str:

        self.fix_character_conflicts()
        rad: str = self.radical
        coefficients: str = "".join(filter(self.is_renderable,
                                           self.coefficients))

        if rad in self.redefined_chars:
            rad = rad.replace(rad, self.redefined_chars[rad])

        for coefficient in coefficients:
            if coefficient in self.redefined_chars:
                coefficients = coefficients.replace(coefficient,
                                     self.redefined_chars[coefficient])
                
        return render_betacode_vowel(rad, coefficients)


class BetacodeComplexConsonantToken(SymbolGroup):

    valid_radicals = VALID_BETACODE_CHARACTERS
    valid_coefficients = ALL_DIACRITICALS
    def __init__(self, radical: str) -> None:
        super().__init__(radical)

    def fix_character_conflicts(self) -> None:
        def breathing_mark():
            return self.members(BREATHING_MARKS)
        
        if self.is_monograph:
            return
        

        if self.radical in lower_and_upper(RHO):
            if breathing_mark():
                if self.radical.isupper() and breathing_mark() == SMOOTH_SYMBOL:
                    self.redefine_char(SMOOTH_SYMBOL, ROUGH_SYMBOL)


        if self.symbol.lower() in GREEK_CONSONANT_CLUSTERS:
            if self.symbol in GREEK_CONSONANT_CLUSTERS:
                self.redefine_char(self.radical, GREEK_CONSONANT_CLUSTERS[self.symbol])
                self.suppress_char(self.coefficients)
            else:
                self.redefine_char(self.radical, GREEK_CONSONANT_CLUSTERS[self.symbol.lower()].upper())



    def __repr__(self) -> str:
        self.fix_character_conflicts()
        rad: str = self.radical
        coefficients: str = "".join(filter(self.is_renderable,
                                           self.coefficients))
        row: int = 0
        col: int = 0
        if rad.isupper():
            col = 8

        if rad in self.redefined_chars:
            rad = rad.replace(rad, self.redefined_chars[rad])

        for coefficient in coefficients:
            if coefficient in self.redefined_chars:
                coefficients = coefficients.replace(coefficient,
                                                    self.redefined_chars[coefficient])
                
        if rad in lower_and_upper(RHO):
            if coefficients == SMOOTH_SYMBOL:
                return chr(0x1FE4)
            if coefficients == ROUGH_SYMBOL:
                if rad.isupper():
                    return chr(0x1FEC)
                else:
                    return chr(0x1FE5)
                
        return render_simple_betacode(rad)

