import re
from .token import BetacodeComplexConsonantToken, SymbolGroup, BetacodeComplexVowelToken, BetacodeToken
from .functions import *
from .constants import BREATHING_MARKS, DIACRITICAL_CATEGORIES, GREEK_CONSONANT_CLUSTERS, RHO


class TextCrawlProxy:
    """Proxy that can crawl a copy of the text without modifying the actual index."""

    def __init__(self, textblock: str):
        self.textblock: str = textblock
        self.index: int = 0

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


class TokenizingStrategy:
    def __init__(self, textblock: str, token_type: type[SymbolGroup]) -> None:
        self.proxy: TextCrawlProxy = TextCrawlProxy(textblock)
        self.token_type: type[SymbolGroup] = token_type

    def trigger_condition(self, index: int) -> bool:
        """Return true if the char at the current index can begin a complex 
        token (Subclasses must provide their own implementation of this
        method)."""
        self.proxy.index = index
        raise NotImplementedError

    def create_sequence(self, token: SymbolGroup) -> int:
        """Generate a sequence of coefficient characters to attatch to the 
        radical of given token. (Subclasses must provide their own 
        implementation of this method)."""
        raise NotImplementedError

    def create_unordered_sequence(self,
                                  token: SymbolGroup,
                                  categories: list[str]
                                  ) -> int:
        """
        Generic method for creating an unordered sequence. 

        Add a sequence of coefficient symbols to a given token based 
        on the premise that the sequence will terminate when a non-categorical
        symbol is met, or when a symbol is met for a category that has already 
        been encountered.

        This entails that a group of symbols can make up a compound symbol in
        any order, but that each category within that group can only have one
        member represented (and may have none).

        Parameters
        ----------
        token           : An initialized token (modified in-place)
        categories      : A list consisting of categories of characters

        Returns
        -------
        int             : Instruction to the tokenizer where to resume.
        """
        self.proxy.index += 1
        switch: list[tuple[str, bool]] = [
            (category, False) for category in categories]
        while self.proxy.has_next:
            if not self.proxy.curr_char in "".join(categories):
                return self.proxy.index -1

            for category, already_used in switch:
                if self.proxy.curr_char in category:
                    if already_used:
                        return self.proxy.index -1

                    token.add_coefficient(self.proxy.curr_char)
                    already_used = True

            self.proxy.index += 1

        return self.proxy.index -1


    def create_ordered_sequence(self,
                                token: SymbolGroup,
                                legal_combinations: list[str]):
        """
        Generic method for creating an ordered sequence. 

        Add a sequence of coefficient symbols to a given token based
        on the premise that the sequence will terminate when the next item
        can no longer be reconciled into a legal sequence.

        This entails that a group of symbols can make up a compound symbol in
        specific orders, and that each subsequent symbol narrows the number of
        remaining legal combinations.
        """
        self.proxy.index += 1
        current_group: str = token.radical
        remaining_combinations: list[str] = legal_combinations
        while self.proxy.has_next:
            continued_group: str = current_group + self.proxy.next_char
            partial_matches: list[str] = re.findall(
                fr"({continued_group}[\w]*)", " ".join(remaining_combinations))
            if partial_matches:
                remaining_combinations = partial_matches
                token.add_coefficient(self.proxy.next_char)
                self.proxy.index += 1

            else:
                return self.proxy.index -1
            
        return self.proxy.index - 1


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
        # NOTE: pick up here: debug this function, which seems to become trapped
        # in an inescapable loop.


        """Create a complex consonant consisting either of a consonant + a 
        diacritical mark or a consonant + a consonant."""
        combinations: list[str] = [x for x in GREEK_CONSONANT_CLUSTERS]
        for x in combinations:
            for char in x:
                combinations.append(x.replace(char, char.upper()))
        if token.radical in lower_and_upper(RHO):
            return self.create_unordered_sequence(token, [BREATHING_MARKS])
        return self.create_ordered_sequence(token, combinations)





class BetacodeTokenizer:

    def __init__(self, textblock: str):
        self.textblock: str = textblock
        self.index: int = 0
        self.strategies: list[TokenizingStrategy] = [
            BetacodeComplexVowelTokenizingStrategy(textblock),
            BetacodeComplexConsonantTokenizingStrategy(textblock)
            ]
        self.tokens: list[SymbolGroup] = []
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
                  token_type: type[SymbolGroup] = BetacodeToken
                  ) -> SymbolGroup:
        token: SymbolGroup = token_type(self.curr_char)
        self.__add_position_to_token(token)
        return token
    

    def __add_position_to_token(self, token: SymbolGroup) -> None:
        if not self.has_next:
            token.is_final = True
            return

        if is_endpoint(self.next_char):
            token.is_final = True

        if not self.has_prev:
            token.is_initial = True
            return

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

            for strategy in self.strategies:
                if strategy.trigger_condition(self.index):
                    token = self.new_token(strategy.token_type)
                    self.index = strategy.create_sequence(token)
                    break

            # Any token that has not already been appended + continue
            # must be a simple token that takes no coefficients.
            self.tokens.append(token)
            if self.has_next:
                self.index += 1

        # Catch the last index (which, by definition, cannot begin any
        # sequence).
        token = self.new_token()
        self.tokens.append(token)
