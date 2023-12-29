

from typing import Callable

from .constants import (ACCENTS,
                        ACUTE_SYMBOL,
                        ALPHA, ALPHA_DIACRITICS,
                        ALPHA_SPECIAL, ALPHA_SUBSCRIPT_DIACRITICS,
                        AMBIGUOUS_VOWELS,
                        BREATHINGS, BREVE_SYMBOL,
                        CIRCUMFLEX_SYMBOL,
                        DIACRITICAL_CATEGORIES,
                        DIAERESIS_SYMBOL,
                        EPSILON, EPSILON_DIACRITICS,
                        ETA, ETA_DIACRITICS,
                        ETA_SPECIAL, ETA_SUBSCRIPT_DIACRITICS,
                        GRAVE_SYMBOL,
                        GREEK_CHARSET,
                        HIGH_VOWELS,
                        IOTA, IOTA_DIACRITICS,
                        IOTA_SPECIAL,
                        LATIN_CHARSET,
                        LENGTHS,
                        LONG_VOWELS, MACRON_SYMBOL,
                        OMEGA, OMEGA_DIACRITICS,
                        OMEGA_SPECIAL, OMEGA_SUBSCRIPT_DIACRITICS,
                        OMICRON,
                        ROUGH_SYMBOL,
                        SHORT_VOWELS,
                        SIMPLE_ACCENTS,
                        SMOOTH_SYMBOL,
                        SUBSCRIPT_SYMBOL,
                        UPSILON, UPSILON_DIACRITICS,
                        UPSILON_SPECIAL,)

from .keywords import (SHORT,
                       LONG,
                       AMBIGUOUS)

from .functions import (lower_and_upper,
                        is_capital,
                        is_endpoint,
                        is_vowel,
                        is_space,
                        is_diacritical)


__all__ = ["SymbolGroup",
           "BetacodeToken",
           "BetacodeComplexVowelToken",
           "BetacodeTokenizer"]


class SymbolGroup:
    """
    Base class to represent a symbol made up of one or more sub-symbols.
    """

    def __init__(self, radical: str):
        if len(radical) > 1:
            raise ValueError("Radical must consist of a single character.")
        self.radical: str = radical
        self.coefficients: str = ""

    @property
    def symbol(self) -> str:
        return self.radical+self.coefficients

    def add_coefficient(self, coefficient: str) -> None:
        if not coefficient in self.coefficients:
            self.coefficients += coefficient

    def remove_coefficient(self, coefficient: str) -> None:
        if coefficient in self.coefficients:
            self.coefficients.replace(coefficient, "")


class BetacodeToken(SymbolGroup):
    """Basic token used for simple 1:1 character mappings."""

    def __init__(self, radical: str):
        super().__init__(radical)
        self.is_final: bool = False
        self.is_initial: bool = False
        self.is_medial: bool = False

    def __repr__(self):
        conversion: str = self.symbol
        for i, latchar in enumerate(lower_and_upper(LATIN_CHARSET)):
            greekchar: str = lower_and_upper(GREEK_CHARSET)[i]
            if latchar in conversion:
                conversion = conversion.replace(latchar, greekchar)
        return conversion


class BetacodeComplexVowelToken(BetacodeToken):
    """
    Token to represent a complex vowel symbol in betacode.

    A vowel may bear any of five types of diacritical marks, and many
    combinations of marks. Certain combinations are forbidden. This class
    stores the basic symbolic character data, corrects any potential 
    conflicts, and renders the conversion (as the ``__repr__`` method)
    """

    def __init__(self, radical: str):
        super().__init__(radical)
        self.suppressed_chars: str = ""
        self.redefined_chars: dict[str, str] = {}
        self.__fix_character_conflicts()

    def __members(self, category: str) -> str:
        """Return any members of a given category found in the coefficients."""
        # Theoretically, the tokenizer should not be able to generate a
        # coefficient with more than one member per category, so this method
        # should only return a len > 1 if the token was injected by a user.
        output: str = ""
        for member in category:
            if member in self.coefficients:
                output += member
        return output

    def __keep_first_member_only(self, category: str) -> None:
        """
        Check the coefficient for multiple members of the given category,
        and suppress all but the first.
        """
        first: str = ""
        for member in self.coefficients:
            if member in category:
                first = member
                break
        suppressions: str = category.replace(first, "")
        for member in self.coefficients:
            if member in suppressions:
                self.__suppress_char(member)

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

    def __suppress_char(self, char: str) -> None:
        """Suppress a coefficient character so that it is ignored in the rendering."""
        if not char in self.suppressed_chars:
            self.suppressed_chars += char

    def __redefine_char(self, char: str, new_char: str) -> None:
        """Redefine the render mapping for a given coefficient character."""
        if not char in self.redefined_chars:
            self.redefined_chars.update({char: new_char})

    def __is_renderable(self, char: str) -> bool:
        return char not in self.suppressed_chars

    def __fix_character_conflicts(self):
        def accent_mark(): return self.__members(ACCENTS)
        def breathing_mark(): return self.__members(BREATHINGS)
        def length_mark(): return self.__members(LENGTHS)
        def is_high_vowel(): return self.radical in lower_and_upper(HIGH_VOWELS)

        # No more than one accent, breathing, or length mark.
        if len(accent_mark()) > 1:
            self.__keep_first_member_only(ACCENTS)
        if len(breathing_mark()) > 1:
            self.__keep_first_member_only(BREATHINGS)
        if len(length_mark()) > 1:
            self.__keep_first_member_only(LENGTHS)

        if self.radical.isupper() and not breathing_mark():
            self.coefficients += SMOOTH_SYMBOL

        # Majuscule upsilon must have rough breathing.
        if self.radical == UPSILON.upper() and breathing_mark() == SMOOTH_SYMBOL:
            self.__redefine_char(SMOOTH_SYMBOL, ROUGH_SYMBOL)

        if self.__length == SHORT:
            # Circumflex can only exist on long (or ambiguously long) vowels
            if accent_mark() == CIRCUMFLEX_SYMBOL:
                self.__suppress_char(accent_mark())
            # Subscript can only exist on long vowels and ambiguously long alpha.
            if self.__has_subscript:
                self.__suppress_char(SUBSCRIPT_SYMBOL)

        if length_mark():
            # Length marks can only exist on ambiguous vowels.
            if not self.radical in lower_and_upper(AMBIGUOUS_VOWELS):
                self.__suppress_char(length_mark())
            # Length mark cannot combine with other diacriticals.
            if breathing_mark() or accent_mark() or self.__has_diaeresis \
                    or self.__has_subscript:
                self.__suppress_char(length_mark())

        # Subscript cannot exist on high vowels.
        if self.__has_subscript and is_high_vowel():
            self.__suppress_char(SUBSCRIPT_SYMBOL)

        # Diaeresis can only exist on high vowels.
        if self.__has_diaeresis:
            if not is_high_vowel() or self.is_initial or is_capital(self.radical):
                self.__suppress_char(DIAERESIS_SYMBOL)


    def __repr__(self) -> str:

        # NOTE: Possible conflicts not covered by the conditions
        # below have already been resolved by ``fix_character_conflicts``

        coefficients: str = "".join(filter(self.__is_renderable,
                                           self.coefficients))
        for coefficient in coefficients:
            if coefficient in self.redefined_chars:
                coefficients.replace(coefficient,
                                     self.redefined_chars[coefficient])

        row: int = 0
        col: int = 0
        rad: str = self.radical
        vowels = [ALPHA, EPSILON, ETA, IOTA, OMICRON, UPSILON, OMEGA]
        if rad.isupper():
            col = 8

        # Vowel + grave or acute
        if coefficients in ACUTE_SYMBOL + GRAVE_SYMBOL:
            if rad.islower():
                row = SIMPLE_ACCENTS
                col = vowels.index(self.radical.lower()) * 2

            if rad.isupper():
                switch = [(ALPHA.upper(), ALPHA_SPECIAL, 2),
                          (ETA.upper(), ETA_SPECIAL, 2),
                          (EPSILON.upper(), ETA_SPECIAL, 0),
                          (IOTA.upper(), IOTA_SPECIAL, 2),
                          (UPSILON.upper(), UPSILON_SPECIAL, 2),
                          (OMICRON.upper(), OMEGA_SPECIAL, 0),
                          (OMEGA.upper(), OMEGA_SPECIAL, 2)]
                for radical, row_, offset in switch:
                    if rad == radical:
                        row = row_
                        col += offset

            if coefficients == ACUTE_SYMBOL:
                col += 1

            return chr(row + col)

        # Vowel + length mark
        if coefficients in MACRON_SYMBOL + BREVE_SYMBOL:
            if rad in lower_and_upper(ALPHA):
                row = ALPHA_SPECIAL
            elif rad in lower_and_upper(IOTA):
                row = IOTA_SPECIAL
            elif rad in lower_and_upper(UPSILON):
                row = UPSILON_SPECIAL

            if coefficients == MACRON_SYMBOL:
                col += 1

            return chr(row + col)

        # Lower case vowel + circumflex
        if coefficients == CIRCUMFLEX_SYMBOL:
            col = 6
            switch = [(ALPHA, ALPHA_SPECIAL),
                      (ETA, ETA_SPECIAL),
                      (IOTA, IOTA_SPECIAL),
                      (UPSILON, UPSILON_SPECIAL),
                      (OMEGA, OMEGA_SPECIAL)]

            for char, rownum in switch:
                if rad == char:
                    return chr(rownum + col)

        # Symbols in the special ranges: diaeresis
        if len(coefficients) == 2 and DIAERESIS_SYMBOL in coefficients:
            switch = [(IOTA, IOTA_SPECIAL),
                      (UPSILON, UPSILON_SPECIAL)]
            for char, rownum in switch:
                if rad == char:
                    row = rownum
            switch = [(GRAVE_SYMBOL, 2),
                      (ACUTE_SYMBOL, 3),
                      (CIRCUMFLEX_SYMBOL, 7)]
            for char, colnum in switch:
                if char in coefficients:
                    col = colnum
            return chr(row + col)

        # Symbols in the special ranges: subscript without breathing
        if len(coefficients) == 2 and SUBSCRIPT_SYMBOL in coefficients:
            if not any([SMOOTH_SYMBOL in coefficients, ROUGH_SYMBOL in coefficients]):
                switch = [(ALPHA, ALPHA_SPECIAL),
                          (ETA, ETA_SPECIAL),
                          (OMEGA, OMEGA_SPECIAL)]
                for char, rownum in switch:
                    if rad == char:
                        row = rownum
                switch = ["null", "null", GRAVE_SYMBOL, "null",
                          ACUTE_SYMBOL, "null", "null", CIRCUMFLEX_SYMBOL]
                for char in switch:
                    if char in coefficients:
                        col = switch.index(char)
                return chr(row + col)

        # If the symbol has not met any condition by now, it must
        # have a predictable place in the table.
        switch = ['null', GRAVE_SYMBOL, ACUTE_SYMBOL, CIRCUMFLEX_SYMBOL]
        for char in switch:
            if char in coefficients:
                col += switch.index(char) * 2
        if ROUGH_SYMBOL in coefficients:
            col += 1
        if rad in lower_and_upper(ALPHA):
            row = ALPHA_DIACRITICS
            if SUBSCRIPT_SYMBOL in coefficients:
                row = ALPHA_SUBSCRIPT_DIACRITICS
        elif rad in lower_and_upper(ETA):
            row = ETA_DIACRITICS
            if SUBSCRIPT_SYMBOL in coefficients:
                row = ETA_SUBSCRIPT_DIACRITICS
        elif rad in lower_and_upper(OMEGA):
            row = OMEGA_DIACRITICS
            if SUBSCRIPT_SYMBOL in coefficients:
                row = OMEGA_SUBSCRIPT_DIACRITICS
        elif rad in lower_and_upper(EPSILON):
            row = EPSILON_DIACRITICS
        elif rad in lower_and_upper(IOTA):
            row = IOTA_DIACRITICS
        elif rad in lower_and_upper(OMICRON):
            row = OMEGA_DIACRITICS
        elif rad in lower_and_upper(UPSILON):
            row = UPSILON_DIACRITICS

        return chr(row + col)


class BetacodeTokenizer:

    def __init__(self, textblock: str):
        self.textblock: str = textblock
        self.index: int = 0
        self.tokens: list[BetacodeToken] = []
        self.tokenize()

    def __repr__(self):
        return "".join(str(token) for token in self.tokens)

    @property
    def has_next(self) -> bool:
        return self.index < len(self.textblock) - 1

    @property
    def has_prev(self) -> bool:
        return self.index > 0

    @property
    def prev_char(self) -> str:
        return self.textblock[self.index - 1] if self.has_prev else ""

    @property
    def next_char(self) -> str:
        return self.textblock[self.index + 1] if self.has_next else ""

    @property
    def curr_char(self) -> str:
        return self.textblock[self.index]

    def new_token(self,
                  token_type: type[BetacodeToken] = BetacodeToken
                  ) -> BetacodeToken:
        token: BetacodeToken = token_type(self.curr_char)
        self.__add_position_to_token(token)
        return token

    def __add_position_to_token(self, token: BetacodeToken) -> None:
        if not self.has_next:
            token.is_final = True
            return

        if not self.has_prev:
            token.is_initial = True
            return

        if is_endpoint(self.next_char):
            token.is_final = True

        if is_space(self.prev_char):
            token.is_initial = True

        if not is_endpoint(self.next_char) \
                and not is_space(self.prev_char):
            token.is_medial = True

        return

    def tokenize(self) -> None:
        self.index = 0
        while self.has_next:
            token = self.new_token()

            # A vowel + diacritical -> complex token, unordered sequence
            if is_vowel(self.curr_char):
                if is_diacritical(self.next_char):
                    token = self.new_token(BetacodeComplexVowelToken)
                    self.index += 1
                    self.unordered_sequence(
                        token, DIACRITICAL_CATEGORIES, is_diacritical)
                    self.tokens.append(token)
                    continue

            # Capitalization symbol + letter or diacritical -> complex token
            # if self.curr_char == "*":

            # Consonant + consonant -> complex token

            # Any token that has not already been appended + continue
            # must be a simple token that takes no coefficients.
            self.tokens.append(token)
            self.index += 1

        # Catch the last index (which, by definition, cannot begin any
        # sequence).
        token = self.new_token()
        self.tokens.append(token)

    def unordered_sequence(self,
                           token: SymbolGroup,
                           categories: list[str],
                           category_test: Callable[[str], bool]
                           ) -> None:
        """
        Add a sequence of coefficient symbols to a given [token] based 
        on the premise that the sequence will terminate when a non-categorical
        symbol is met (as defined by the [category_test]), or when a symbol is 
        met for a category that has already been encountered.

        This entails that a group of symbols can make up a compound symbol in
        any order, but that each category within that group can only have one
        member represented (and may have none).
        """

        switch: list[tuple[str, bool]] = [
            (category, False) for category in categories]
        while self.has_next:
            if not category_test(self.curr_char):
                return

            for category, already_used in switch:
                if self.curr_char in category:
                    if already_used:
                        return

                    token.add_coefficient(self.curr_char)
                    already_used = True

            self.index += 1

        return

    def consonant_sequence(self):
        ...  # placeholder
