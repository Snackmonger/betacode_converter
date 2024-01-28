

from src.core import Tokenizer
from .constants import COMBINING_DIACRITICALS


__all__ = ["LatinCodeTokenizer"]



class LatinCodeTokenizer(Tokenizer):
    """The latin version of the program just converts the designated symbols 
    to combining diacritical marks."""
    def __init__(self, textblock: str) -> None:
        self.textblock: str = textblock

    def __repr__(self) -> str:
        conversion: str = self.textblock
        for char in conversion:
            if char in COMBINING_DIACRITICALS:
                conversion = conversion.replace(char, chr(COMBINING_DIACRITICALS[char]))
        return conversion
        

    def tokenize(self) -> None:
        """This version of the tokenizer never actually needs to call this
        function, and it might mess something up if it did, so we just 
        override it."""
        
    
