import re
from typing import Optional

from .token import SymbolGroup
from .functions import is_endpoint, is_space


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




class Tokenizer:
    """
    Generic tokenizer for parsing characters and character groups into tokens.
    """
    END = chr(0x2403)

    def __init__(self, textblock: str) -> None:
        self.textblock: str = textblock + self.END
        self.index: int = 0
        self.tokens: list[SymbolGroup] = []
        self.strategies: list[TokenizingStrategy] = []
        self.default_token: type[SymbolGroup] = SymbolGroup

    
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
                  token_type: Optional[type[SymbolGroup]] = None
                  ) -> SymbolGroup:
        
        if token_type is None:
            token_type = self.default_token

        token: SymbolGroup = token_type(self.curr_char)
        self.add_position_to_token(token)
        return token
    

    def add_position_to_token(self, token: SymbolGroup) -> None:
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
        """Parse the class' textblock for tokens as defined by the class' 
        strategies."""
        self.index = 0
        while self.has_next:
            token = self.new_token()

            # Strategies for complex tokens
            for strategy in self.strategies:
                if strategy.trigger_condition(self.index):
                    token = self.new_token(strategy.token_type)
                    self.index = strategy.create_sequence(token)
                    break

            # Default simple token
            self.tokens.append(token)
            if self.has_next:
                self.index += 1
    
        # END token is to be discarded (but if we somehow got here
        # with a valid token, then keep it).
        if self.textblock[self.index] == self.END:
            return
        token = self.new_token()
        self.tokens.append(token)
            
