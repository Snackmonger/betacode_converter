
ROUGH_SYMBOL: str = "("
SMOOTH_SYMBOL: str = ")"
ACUTE_SYMBOL: str = "/"
DOUBLE_ACUTE_SYMBOL: str = "{"
GRAVE_SYMBOL: str = "\\"
DOUBLE_GRAVE_SYMBOL: str = "}"
STRAIGHT_CIRCUMFLEX_SYMBOL: str = "^"
CARON_SYMBOL: str = "="
CURVED_CIRCUMFLEX_SYMBOL: str = "~"
OVERDOT_SYMBOL: str = "`"
SUBSCRIPT_SYMBOL: str = "|"
DIAERESIS_SYMBOL: str = "+"
MACRON_SYMBOL: str = "_"
BREVE_SYMBOL: str = "-"


COMB_ROUGH: int = 0x0304
COMB_SMOOTH: int = 0x0303


CONVERSIONS: dict[str, int] = {ROUGH_SYMBOL: 0x0314,
                               SMOOTH_SYMBOL: 0x0313,
                               ACUTE_SYMBOL: 0x0301,
                               GRAVE_SYMBOL: 0x0300,
                               DOUBLE_ACUTE_SYMBOL: 0x030B,
                               DOUBLE_GRAVE_SYMBOL: 0x030F,
                               STRAIGHT_CIRCUMFLEX_SYMBOL: 0x0303,
                               CARON_SYMBOL: 0x030C,
                               CURVED_CIRCUMFLEX_SYMBOL: 0x0342,
                               OVERDOT_SYMBOL: 0x0307,
                               DIAERESIS_SYMBOL: 0x0308,
                               MACRON_SYMBOL: 0x0304,
                               BREVE_SYMBOL: 0x0306
                               }
