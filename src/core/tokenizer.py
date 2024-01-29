"""Base classes for tokenizer and tokenizing strategies."""

import re
from typing import Optional, Protocol

from .token import SymbolGroup, EscapeSequenceToken
from .functions import is_endpoint, is_space
from .constants import ESCAPE_CHAR


class TextCrawlProxy:
    """Proxy that can crawl a copy of the text without modifying the actual index.
    """
    # The proxy is pretty unnecessary for the current set-up, but maybe it will
    # be useful once we are dealing with more complex character sets?

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
    """Generic class to represent the operation of a tokenizer.
    
    The tokenizer queries the strategy's trigger condition to see whether the
    given radical is appropriate to begin a sequence, then generates a 
    sequence of coefficients based on the logic in the ``create_sequence``
    method (which must be defined in subclasses). 
    
    The class provides two generic sequencing methods that can fulfill this 
    role:
    ``create_ordered_sequence`` and ``create_unordered_sequence``
    (See those methods' docstrings for further information.)
    """

    def __init__(self, 
                 textblock: str, 
                 token_type: type[SymbolGroup]
                 ) -> None:
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
        radical of given token. 
        
        Subclasses must provide their own implementation of this method. 
        
        The class provides two generic sequencing methods that can fulfill 
        this role: 
        ``create_ordered_sequence`` and ``create_unordered_sequence``
        See those methods' docstrings for further information.
        """
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
        been fulfilled.

        This entails that a group of symbols can make up a compound symbol in
        any order, but that each category within that group can only have one
        member represented (and may have none).

        Parameters
        ----------
        token           : An initialized token (modified in-place)
        categories      : A list consisting of categories of characters

        Returns
        -------
        int             : Instruction to the tokenizer where to resume parsing.
        """
        self.proxy.index += 1
        switch: dict[str, bool] = {category: False for category in categories}
        while self.proxy.has_next:
            if not self.proxy.curr_char in "".join(categories):
                return self.proxy.index -1

            for category, already_used in switch.items():
                if self.proxy.curr_char in category:
                    if already_used:
                        return self.proxy.index -1

                    token.add_coefficient(self.proxy.curr_char)
                    switch[category] = True

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

        Parameters
        ----------
        token               : An initialized token (modified in-place)
        legal_combinations  : A list of valid character combinations.

        Returns
        -------
        int             : Instruction to the tokenizer where to resume parsing.
        """
        self.proxy.index += 1
        current_group: str = token.radical
        remaining_combinations: list[str] = legal_combinations
        while self.proxy.has_next:
            next_group: str = current_group + self.proxy.curr_char
            partial_matches: list[str] = re.findall(
                fr"({next_group}[\w]*)", 
                " ".join(remaining_combinations))
            
            if partial_matches:
                remaining_combinations = partial_matches
                current_group = next_group
                token.add_coefficient(self.proxy.curr_char)
                self.proxy.index += 1
            else:
                return self.proxy.index -1

        return self.proxy.index - 1




class EscapeSequenceTokenizingStrategy(TokenizingStrategy):
    """Strategy to allow the user to signify that the character following
    the escape character is to be rendered in its current form."""
    def __init__(self, textblock: str, token_type: type[SymbolGroup] = EscapeSequenceToken) -> None:
        super().__init__(textblock, token_type)

    def trigger_condition(self, index: int) -> bool:
        """Return true if the char at the current index can begin a complex 
        token"""
        self.proxy.index = index
        return self.proxy.curr_char == ESCAPE_CHAR and self.proxy.has_next

    def create_sequence(self, token: SymbolGroup) -> int:
        token.radical = self.proxy.curr_char
        token.coefficients = self.proxy.next_char
        return self.proxy.index + 1




class Tokenizer:
    """
    Generic tokenizer for parsing characters and character groups into tokens.
    """
    END = chr(0x2403)

    def __init__(self, textblock: str) -> None:
        self.textblock: str = textblock + self.END
        self.index: int = 0
        self.tokens: list[SymbolGroup] = []
        self.strategies: list[TokenizingStrategy] = [EscapeSequenceTokenizingStrategy(textblock)]
        self.default_token: type[SymbolGroup] = SymbolGroup

    
    def __repr__(self):
        return "".join(str(token) for token in self.tokens)

    def include_strategy(self, strategy: TokenizingStrategy) -> None:
        """Add a strategy for the class to use during parsing."""
        self.strategies.append(strategy)

    @property
    def has_next(self) -> bool:
        """True, if the text has another character after the current one."""
        return self.index < len(self.textblock) - 1


    @property
    def has_prev(self) -> bool:
        """True, if the text has another character before the current one."""
        return self.index > 0


    @property
    def prev_char(self) -> str:
        """The character that came before the current one."""
        return self.textblock[self.index - 1] if self.has_prev else ""


    @property
    def next_char(self) -> str:
        """The character that comes after the current one."""
        return self.textblock[self.index + 1] if self.has_next else ""


    @property
    def curr_char(self) -> str:
        """The current character."""
        return self.textblock[self.index]


    def new_token(self,
                  token_type: Optional[type[SymbolGroup]] = None
                  ) -> SymbolGroup:
        """Add generic information to a new token and return it for 
        further processing.
        """
        if token_type is None:
            token_type = self.default_token

        token: SymbolGroup = token_type(self.curr_char)
        self.add_position_to_token(token)
        return token
    

    def add_position_to_token(self, token: SymbolGroup) -> None:
        """Set markers for the token's position relative to other characters."""
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
        """Parse the class' textblock for tokens (as defined by the class' 
        strategies)."""
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
        # with a valid token instead of END, then keep it).
        if self.textblock[self.index] == self.END:
            return
        token = self.new_token()
        self.tokens.append(token)
            


class TokenizerProtocol(Protocol):
    """Defines the interface for all text converters used in the program."""


    def __init__(self, textblock: str) -> None:
        raise NotImplementedError
    
    def __repr__(self) -> str:
        raise NotImplementedError