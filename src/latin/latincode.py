

from src.latin.constants import CONVERSIONS

class LatinCodeTokenizer:
    """The latin version of the program just converts the designated symbols 
    to combining diacritical marks."""
    def __init__(self, textblock: str) -> None:
        self.textblock: str = textblock

    def __repr__(self) -> str:
        conversion: str = self.textblock
        for char in conversion:
            if char in CONVERSIONS:
                conversion = conversion.replace(char, chr(CONVERSIONS[char]))
        return conversion
        
