"""This module supplies the tokens and tokenizing strategies for parsing Greek
beta code (mixed case beta code)."""

from src.core import TokenizingStrategy, Tokenizer, SymbolGroup, lower_and_upper
from .functions import is_short_vowel, is_vowel, is_diacritical, combinations

from .constants import (ACCENT_MARKS,
                        ALL_DIACRITICALS,
                        AMBIGUOUS_VOWELS,
                        BREATHING_MARKS,
                        CIRCUMFLEX_SYMBOL,
                        DIACRITICAL_CATEGORIES,
                        DIAERESIS_SYMBOL,
                        GREEK_CONSONANT_CLUSTERS,
                        HIGH_VOWELS,
                        LENGTH_MARKS,
                        RHO,
                        ROUGH_SYMBOL,
                        SMOOTH_SYMBOL,
                        SUBSCRIPT_SYMBOL,
                        UPSILON,
                        VALID_BETACODE_CHARACTERS)

from .rendering import (render_betacode_vowel,
                        render_simple_betacode)


class BetacodeToken(SymbolGroup):
    """
    Token to represent a generic betacode monographic symbol.
    """
    valid_radicals = VALID_BETACODE_CHARACTERS
    valid_coefficients = ALL_DIACRITICALS

    def fix_character_conflicts(self) -> None:
        if self.is_monograph and self.radical == "s" and self.is_final:
            self.redefine_char("s", "j")

    def __repr__(self):
        self.fix_character_conflicts()
        conversion: str = "".join(filter(self.is_renderable, self.symbol))
        for subsymbol in conversion:
            if subsymbol in self.redefined_chars:
                conversion = conversion.replace(subsymbol,
                                                self.redefined_chars[subsymbol])

        return render_simple_betacode(conversion)


class BetacodeComplexVowelToken(SymbolGroup):
    """
    Token to represent a complex vowel symbol in betacode.

    This token accommodates all combinations of vowel + diacritical mark. 

    Diacritical marks can come in any order, but they are evaluated according
    to the following hierarchy: 
        1) accent and breathing mark (can appear in any combination)
        2) subscript or diaeresis (combinations are restricted by vowel type)
        3) length marks (restricted by vowel type & cannot be combined)

    This system entails that a token will always sacrifice 3) to preserve 2), 
    and 2) to preserve 1). For instance, a diaeresis does not appear on a 
    vowel with rough breathing; if we encounter the sequence "i(+", we 
    sacrifice the "+" and preserve the "(".
    """
    valid_radicals = VALID_BETACODE_CHARACTERS
    valid_coefficients = ALL_DIACRITICALS

    @property
    def __has_subscript(self) -> bool:
        return SUBSCRIPT_SYMBOL in self.coefficients

    @property
    def __has_diaeresis(self) -> bool:
        return DIAERESIS_SYMBOL in self.coefficients

    def fix_character_conflicts(self):
        """Suppress any characters that conflict with the combined sign, or 
        re-define them so that they point to an acceptable substitute.

        Note: The actual radical and coefficients of the token never change; 
        this method simply instructs the renderer to ignore a member 
        character, or render it a different way than written. 
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

        # Preserve capital vowels at the expense of any diacritical.
        # Majuscule upsilon must have rough breathing or none at all.
        if self.radical == UPSILON.upper() and breathing_mark() == SMOOTH_SYMBOL:
            self.redefine_char(SMOOTH_SYMBOL, ROUGH_SYMBOL)
        # Uppercase vowels that have circumflex must also have a breathing mark.
        if accent_mark() == CIRCUMFLEX_SYMBOL and not breathing_mark() and self.radical.isupper():
            self.suppress_char(CIRCUMFLEX_SYMBOL)

        if is_short_vowel(self.radical):
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
        if self.__has_diaeresis and not is_high_vowel():
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
    """
    Token to represent a complex consonant in Greek.
    
    We use this so that we can supply Latin digraphs for Greek 
    double-consonants ps & ks (these are also coded for y and c,
    respectively), and so that rho may carry a breathing mark.
    """

    valid_radicals = VALID_BETACODE_CHARACTERS
    valid_coefficients = BREATHING_MARKS + lower_and_upper("s")


    def fix_character_conflicts(self) -> None:
        """Suppress any characters that conflict with the combined sign, or 
        re-define them so that they point to an acceptable substitute.

        Note: The actual radical and coefficients of the token never change; 
        this method simply instructs the renderer to ignore a member 
        character, or render it a different way than written. 
        """
        def breathing_mark():
            return self.members(BREATHING_MARKS)
        if self.is_monograph:
            return

        if self.radical in lower_and_upper(RHO):
            if breathing_mark():
                if self.radical.isupper() and breathing_mark() == SMOOTH_SYMBOL:
                    self.redefine_char(SMOOTH_SYMBOL, ROUGH_SYMBOL)

        if self.symbol in combinations():
            if self.symbol.islower():
                self.redefine_char(
                    self.radical, GREEK_CONSONANT_CLUSTERS[self.symbol])
                self.suppress_char(self.coefficients)
            else:
                self.redefine_char(
                    self.radical, GREEK_CONSONANT_CLUSTERS[self.symbol.lower()].upper())


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

        if rad in lower_and_upper(RHO):
            if coefficients == SMOOTH_SYMBOL:
                return chr(0x1FE4)
            if coefficients == ROUGH_SYMBOL:
                if rad.isupper():
                    return chr(0x1FEC)
                else:
                    return chr(0x1FE5)

        return render_simple_betacode(rad)


class BetacodeComplexVowelTokenizingStrategy(TokenizingStrategy):
    """Wrapper for Betacode vowel parsing function and parsing trigger."""


    def __init__(self, textblock: str):
        super().__init__(textblock, BetacodeComplexVowelToken)


    def trigger_condition(self, index: int) -> bool:
        """Return true if the char at the current index can begin a complex
        token."""
        self.proxy.index = index
        if is_vowel(self.proxy.curr_char) and is_diacritical(self.proxy.next_char):
            return True
        return False
    

    def create_sequence(self, token: SymbolGroup) -> int:
        """Create a sequence of diacritical marks following a vowel."""
        return self.create_unordered_sequence(token, DIACRITICAL_CATEGORIES)



class BetacodeComplexConsonantTokenizingStrategy(TokenizingStrategy):
    """Wrapper for Betacode consonant parsing function and parsing trigger."""


    def __init__(self, textblock: str):
        super().__init__(textblock, BetacodeComplexConsonantToken)


    def trigger_condition(self, index: int) -> bool:
        """Return true if the char at the current index can begin a complex
        token."""
        self.proxy.index = index
        combination: str = self.proxy.curr_char + self.proxy.next_char
        if combination in combinations():
            return True
        if self.proxy.curr_char in lower_and_upper(RHO) and self.proxy.next_char in BREATHING_MARKS:
            return True
        return False
    

    def create_sequence(self, token: SymbolGroup) -> int:
        """Create a complex consonant consisting either of a consonant + a 
        diacritical mark or a consonant + a consonant."""
        if token.radical in lower_and_upper(RHO):
            return self.create_unordered_sequence(token, [BREATHING_MARKS])
        return self.create_ordered_sequence(token, combinations())
    


class BetacodeTokenizer(Tokenizer):
    """Class that reads beta code in Latin text and converts it to Greek 
    letters and diacritical marks.
    """

    def __init__(self, textblock: str):
        super().__init__(textblock)
        self.strategies: list[TokenizingStrategy] = [
            BetacodeComplexVowelTokenizingStrategy(textblock),
            BetacodeComplexConsonantTokenizingStrategy(textblock)
        ]
        self.default_token: type[SymbolGroup] = BetacodeToken
        self.tokenize()
