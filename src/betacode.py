from .tokenizer import TokenizingStrategy, Tokenizer
from .token import SymbolGroup
from .functions import is_vowel, is_diacritical, lower_and_upper
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
                        LONG_VOWELS, 
                        RHO,
                        ROUGH_SYMBOL,
                        SHORT_VOWELS,
                        SMOOTH_SYMBOL,
                        SUBSCRIPT_SYMBOL,
                        UPSILON,
                        VALID_BETACODE_CHARACTERS)

from .keywords import (SHORT, 
                       LONG, 
                       AMBIGUOUS)

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

    Class Overview
    --------------
    State: The basic precursors for symbol creation.
    Behaviour: Correcting conflicting character codes and forwarding the final
    codes to the betacode rendering function.
    """
    valid_radicals = VALID_BETACODE_CHARACTERS
    valid_coefficients = ALL_DIACRITICALS
        
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
    def __init__(self, textblock: str):
        super().__init__(textblock, BetacodeComplexConsonantToken)


    def trigger_condition(self, index: int) -> bool:
        """Return true if the char at the current index can begin a complex
        token."""
        self.proxy.index = index
        combination: str = self.proxy.curr_char + self.proxy.next_char
        if combination.lower() in GREEK_CONSONANT_CLUSTERS:
            return True
        if self.proxy.curr_char in lower_and_upper(RHO) and self.proxy.next_char in BREATHING_MARKS:
            return True
        return False


    def create_sequence(self, token: SymbolGroup) -> int:
        # TODO: This func does not properly combine ks > c or ps > y
        """Create a complex consonant consisting either of a consonant + a 
        diacritical mark or a consonant + a consonant."""
        combinations: list[str] =list(GREEK_CONSONANT_CLUSTERS)
        combinations.extend([x.upper() for x in combinations])
        combinations.extend([x.capitalize() for x in combinations])

        if token.radical in lower_and_upper(RHO):
            return self.create_unordered_sequence(token, [BREATHING_MARKS])
        
        return self.create_ordered_sequence(token, combinations)


class BetacodeTokenizer(Tokenizer):

    def __init__(self, textblock: str):
        super().__init__(textblock)
        self.strategies: list[TokenizingStrategy] = [
            BetacodeComplexVowelTokenizingStrategy(textblock),
            BetacodeComplexConsonantTokenizingStrategy(textblock)
            ]
        self.default_token: type[SymbolGroup] = BetacodeToken
        self.tokenize()