from src.core import Tokenizer, LATIN_CHARSET
from src.latin import COMBINING_DIACRITICALS
from .constants import GREEK_CHARSET


class BetacodeCombiningTokenizer(Tokenizer):
    """This is a simplified version of the tokenizer that simply maps 
    designated characters to the combining diacritical marks. 
    
    For Greek text, if the diacriticals are entered in the wrong order, 
    the symbol might end up malformed, or diacriticals might be rendered 
    as separate characters. For this reason, the main tokenizer only allows 
    conversion to pre-combined characters. This class allows the user to 
    play around with the representation of symbols by adjusting the order of
    diacritical marks. 
    
    Note: combining diacriticals may not render the same way on every 
    computer!
    
    """

    def __init__(self, textblock: str) -> None:
        self.textblock: str = textblock

    def __repr__(self) -> str:
        conversion: str = self.textblock
        for char in conversion:
            if char in COMBINING_DIACRITICALS:
                conversion = conversion.replace(char, chr(COMBINING_DIACRITICALS[char]))

            if char in LATIN_CHARSET:
                conversion = conversion.replace(char, GREEK_CHARSET[LATIN_CHARSET.index(char)])
        return conversion
        

    def tokenize(self) -> None:
        """This version of the tokenizer never actually needs to call this
        function, and it might mess something up if it did, so we just 
        override it."""