
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


COMBINING_DIACRITICALS: dict[str, int] = {ROUGH_SYMBOL: 0x0314,
                               SMOOTH_SYMBOL: 0x0313,
                               GRAVE_SYMBOL: 0x0300,
                               ACUTE_SYMBOL: 0x0301,
                               STRAIGHT_CIRCUMFLEX_SYMBOL: 0x0302,
                               CURVED_CIRCUMFLEX_SYMBOL: 0x0303,
                               MACRON_SYMBOL: 0x0304,
                               BREVE_SYMBOL: 0x0306,
                               OVERDOT_SYMBOL: 0x0307,
                               DIAERESIS_SYMBOL: 0x0308,
                               DOUBLE_ACUTE_SYMBOL: 0x030B,
                               CARON_SYMBOL: 0x030C,
                               DOUBLE_GRAVE_SYMBOL: 0x030F}

ITALIC_KEY: str = "abcdevzhQiklmnZopSqrstuxFKfRCIU"
OLD_ITALIC: str = "𐌀𐌁𐌂𐌃𐌄𐌅𐌆𐌇𐌈𐌉𐌊𐌋𐌌𐌍𐌎𐌏𐌐𐌑𐌒𐌓𐌔𐌕𐌖𐌗𐌘𐌙𐌚𐌛𐌜𐌝𐌞"
