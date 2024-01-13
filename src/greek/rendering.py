from .constants import (ACUTE_SYMBOL,
                        ALPHA,
                        ALPHA_DIACRITICALS,
                        ALPHA_SPECIAL,
                        ALPHA_SUBSCRIPT_DIACRITICALS,
                        BREVE_SYMBOL,
                        CIRCUMFLEX_SYMBOL,
                        DIAERESIS_SYMBOL,
                        EPSILON,
                        EPSILON_DIACRITICALS,
                        ETA,
                        ETA_DIACRITICALS,
                        ETA_SPECIAL,
                        ETA_SUBSCRIPT_DIACRITICALS,
                        GRAVE_SYMBOL, GREEK_CHARSET, GREEK_PUNCTUATION,
                        IOTA,
                        IOTA_DIACRITICALS,
                        IOTA_SPECIAL, LATIN_CHARSET,
                        MACRON_SYMBOL,
                        OMEGA,
                        OMEGA_DIACRITICALS,
                        OMEGA_SPECIAL,
                        OMEGA_SUBSCRIPT_DIACRITICALS,
                        OMICRON, LATIN_PUNCTUATION, OMICRON_DIACRITICALS,
                        ROUGH_SYMBOL,
                        SIMPLE_ACCENTS,
                        SMOOTH_SYMBOL,
                        SUBSCRIPT_SYMBOL,
                        UPSILON, UPSILON_DIACRITICALS,
                        UPSILON_SPECIAL)

from .functions import lower_and_upper

def get_greek_vowel_special_row(vowel: str) -> int:
    rows: list[tuple[str, int]] = [
                      (ALPHA, ALPHA_SPECIAL),
                      (ETA, ETA_SPECIAL),
                      (EPSILON, ETA_SPECIAL),
                      (IOTA, IOTA_SPECIAL),
                      (UPSILON, UPSILON_SPECIAL),
                      (OMICRON, OMEGA_SPECIAL),
                      (OMEGA, OMEGA_SPECIAL)]
    for vowel_, row in rows:
        if vowel in lower_and_upper(vowel_):
            return row

    raise ValueError(f"Unrecognized vowel symbol {vowel}")


def get_greek_vowel_simple_accent_offset(radical: str) -> int:
    """Correct the column for long and ambiguous vowels."""
    if radical.lower() in [EPSILON, OMICRON]:
        return 0
    else:
        return 2


def render_rho(radical: str, coefficients: str) -> str:
    """Rho may take a breathing mark and no other diacriticals."""
    if coefficients == ROUGH_SYMBOL:
        if radical.isupper():
            return chr(0x1FEC)
        else:
            return chr(0x1FE5)
    return chr(0x1FE4)


def render_simple_betacode(symbol: str) -> str:
    """Render a simple 1:1 equivalence between Greek and Latin characters."""
    for i, latchar in enumerate(lower_and_upper(LATIN_CHARSET)):
        greekchar: str = lower_and_upper(GREEK_CHARSET)[i]
        if latchar in symbol:
            symbol = symbol.replace(latchar, greekchar)

    for i, latpunct in enumerate(LATIN_PUNCTUATION):
        greekpunct: str = GREEK_PUNCTUATION[i]
        if latpunct in symbol:
            symbol = symbol.replace(latpunct, greekpunct)

    return symbol


def render_betacode_vowel(radical: str, coefficients: str) -> str:
    """Render a vowel symbol in beta code format. 
    
    Handle any combinations that have an unpredictable spot in the unicode
    table, then refer any predictable combinations to their appropriate spot.
    """
    row: int = 0
    col: int = 0
    vowels = [ALPHA, EPSILON, ETA, IOTA, OMICRON, UPSILON, OMEGA]
    if radical.isupper():
        col = 8

    # Vowel + grave or acute
    if coefficients in ACUTE_SYMBOL + GRAVE_SYMBOL:
        if radical.islower():
            row = SIMPLE_ACCENTS
            col = vowels.index(radical.lower()) * 2
        elif radical.isupper():
            row = get_greek_vowel_special_row(radical)
            col += get_greek_vowel_simple_accent_offset(radical)
        if coefficients == ACUTE_SYMBOL:
            col += 1
        return chr(row + col)

    # Vowel + length mark
    if coefficients in MACRON_SYMBOL + BREVE_SYMBOL:
        row = get_greek_vowel_special_row(radical)
        if coefficients == MACRON_SYMBOL:
            col += 1
        return chr(row + col)

    # Lower case vowel + circumflex
    # N.B. Cannot have upper case circumflex without a breathing.
    if coefficients == CIRCUMFLEX_SYMBOL:
        col = 6
        row = get_greek_vowel_special_row(radical)
        return chr(row + col)

    # Supplements borrowed from the coptic block
    if coefficients == DIAERESIS_SYMBOL:
        num: int
        if radical.isupper():
            num = 0x03AA
        else:
            num = 0x03CA
        if radical in lower_and_upper(UPSILON):
            num += 1
        return chr(num)
    
    # Subscript without accent
    if coefficients == SUBSCRIPT_SYMBOL:
        row = get_greek_vowel_special_row(radical)
        col += 3
        return chr(row + col)


    # Symbols in the special ranges: diaeresis
    # N.B. Diaeresis can only exist on lower case upsilon and iota.
    if len(coefficients) == 2 and DIAERESIS_SYMBOL in coefficients:
        row = get_greek_vowel_special_row(radical)
        switch = [(GRAVE_SYMBOL, 2),
                    (ACUTE_SYMBOL, 3),
                    (CIRCUMFLEX_SYMBOL, 7)]
        for char, colnum in switch:
            if char in coefficients:
                col = colnum
        return chr(row + col)


    # Symbols in the special ranges: subscript with accent, without breathing
    # N.B. Lower case only.
    if len(coefficients) == 2 and SUBSCRIPT_SYMBOL in coefficients:
        if not any([SMOOTH_SYMBOL in coefficients, ROUGH_SYMBOL in coefficients]):
            switch = [(ALPHA, ALPHA_SPECIAL),
                        (ETA, ETA_SPECIAL),
                        (OMEGA, OMEGA_SPECIAL)]
            for char, rownum in switch:
                if radical == char:
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
    if radical in lower_and_upper(ALPHA):
        row = ALPHA_DIACRITICALS
        if SUBSCRIPT_SYMBOL in coefficients:
            row = ALPHA_SUBSCRIPT_DIACRITICALS
    elif radical in lower_and_upper(ETA):
        row = ETA_DIACRITICALS
        if SUBSCRIPT_SYMBOL in coefficients:
            row = ETA_SUBSCRIPT_DIACRITICALS
    elif radical in lower_and_upper(OMEGA):
        row = OMEGA_DIACRITICALS
        if SUBSCRIPT_SYMBOL in coefficients:
            row = OMEGA_SUBSCRIPT_DIACRITICALS
    elif radical in lower_and_upper(EPSILON):
        row = EPSILON_DIACRITICALS
    elif radical in lower_and_upper(IOTA):
        row = IOTA_DIACRITICALS
    elif radical in lower_and_upper(OMICRON):
        row = OMICRON_DIACRITICALS
    elif radical in lower_and_upper(UPSILON):
        row = UPSILON_DIACRITICALS

    return chr(row + col)
