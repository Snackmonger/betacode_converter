The unicode block for Greek Extended characters containing diacritics.

::

      	0 	1 	2 	3 	4 	5 	6 	7 	8 	9 	A 	B 	C 	D 	E 	F
U+1F0x 	ἀ 	ἁ 	ἂ 	ἃ 	ἄ 	ἅ 	ἆ 	ἇ 	Ἀ 	Ἁ 	Ἂ 	Ἃ 	Ἄ 	Ἅ 	Ἆ 	Ἇ
U+1F1x 	ἐ 	ἑ 	ἒ 	ἓ 	ἔ 	ἕ 			Ἐ 	Ἑ 	Ἒ 	Ἓ 	Ἔ 	Ἕ 		
U+1F2x 	ἠ 	ἡ 	ἢ 	ἣ 	ἤ 	ἥ 	ἦ 	ἧ 	Ἠ 	Ἡ 	Ἢ 	Ἣ 	Ἤ 	Ἥ 	Ἦ 	Ἧ
U+1F3x 	ἰ 	ἱ 	ἲ 	ἳ 	ἴ 	ἵ 	ἶ 	ἷ 	Ἰ 	Ἱ 	Ἲ 	Ἳ 	Ἴ 	Ἵ 	Ἶ 	Ἷ
U+1F4x 	ὀ 	ὁ 	ὂ 	ὃ 	ὄ 	ὅ 			Ὀ 	Ὁ 	Ὂ 	Ὃ 	Ὄ 	Ὅ 		
U+1F5x 	ὐ 	ὑ 	ὒ 	ὓ 	ὔ 	ὕ 	ὖ 	ὗ 		Ὑ 		Ὓ 		Ὕ 		Ὗ
U+1F6x 	ὠ 	ὡ 	ὢ 	ὣ 	ὤ 	ὥ 	ὦ 	ὧ 	Ὠ 	Ὡ 	Ὢ 	Ὣ 	Ὤ 	Ὥ 	Ὦ 	Ὧ
U+1F7x 	ὰ 	ά 	ὲ 	έ 	ὴ 	ή 	ὶ 	ί 	ὸ 	ό 	ὺ 	ύ 	ὼ 	ώ 		
U+1F8x 	ᾀ 	ᾁ 	ᾂ 	ᾃ 	ᾄ 	ᾅ 	ᾆ 	ᾇ 	ᾈ 	ᾉ 	ᾊ 	ᾋ 	ᾌ 	ᾍ 	ᾎ 	ᾏ
U+1F9x 	ᾐ 	ᾑ 	ᾒ 	ᾓ 	ᾔ 	ᾕ 	ᾖ 	ᾗ 	ᾘ 	ᾙ 	ᾚ 	ᾛ 	ᾜ 	ᾝ 	ᾞ 	ᾟ
U+1FAx 	ᾠ 	ᾡ 	ᾢ 	ᾣ 	ᾤ 	ᾥ 	ᾦ 	ᾧ 	ᾨ 	ᾩ 	ᾪ 	ᾫ 	ᾬ 	ᾭ 	ᾮ 	ᾯ
U+1FBx 	ᾰ 	ᾱ 	ᾲ 	ᾳ 	ᾴ 		ᾶ 	ᾷ 	Ᾰ 	Ᾱ 	Ὰ 	Ά 	ᾼ 	᾽ 	ι 	᾿
U+1FCx 	῀ 	῁ 	ῂ 	ῃ 	ῄ 		ῆ 	ῇ 	Ὲ 	Έ 	Ὴ 	Ή 	ῌ 	῍ 	῎ 	῏
U+1FDx 	ῐ 	ῑ 	ῒ 	ΐ 			ῖ 	ῗ 	Ῐ 	Ῑ 	Ὶ 	Ί 		῝ 	῞ 	῟
U+1FEx 	ῠ 	ῡ 	ῢ 	ΰ 	ῤ 	ῥ 	ῦ 	ῧ 	Ῠ 	Ῡ 	Ὺ 	Ύ 	Ῥ 	῭ 	΅ 	`
U+1FFx 			ῲ 	ῳ 	ῴ 		ῶ 	ῷ 	Ὸ 	Ό 	Ὼ 	Ώ 	ῼ 	´ 	῾ 	


Rules for creating vowel + diacritic tokens
-------------------------------------------

A combination is triggered when the parser reaches a symbol that might be combined with the following symbol(s). For Greek, this 
really just affects vowels (but just to make things a bit more challenging, I wanted to allow this for a few consonant combinations too.)

In these tokens, the trigger symbol is considered the "radical" element, and the 

1. A diacritic must come AFTER the vowel it modifies.
    Exception: if the strict betacode formatting is followed, the diacritic comes after the capitalization sign instead of the vowel.
2. A diacritic may be combined with another diacritic, provided they are of different classes.
3. The order of diacritics is irrelevant (for us, but in strict betacode it is fixed)
4. A diacritic that cannot be combined with the preceding characters will be interpreted as a separate token in which the diacritic itself is the radical.
5. A diacritic that can theoretically be combined with the preceding characters, but can't actually be displayed, 
will be ignored in the rendering but will not be interpreted as a separate character.
    Explanation: We have 4 classes of diacritic: breathing, accent, diaeresis, and subscript. Each category can have one and only one mark. 
    But some combinations can only allow for 2 or 3 categories. The extra categories are ignored, but don't cause an error. As far as the 
    tokenizer is concerned, it's a valid combination; it's up to the rendering strategy to decide how to reconcile the conflict.




Notes:

For U+1F0x to U+1F6x and U+1F8x to U+1FAx:

    0, 8 = smooth breathing
    1, 9 = rough breathing
    2, A = smooth + grave
    3, B = rough + grave
    4, C = smooth + acute
    5, D = rough + acute
    6, E = smooth + circumflex
    7, F = rough + circumflex

    Except that:
    1) Naturally short vowels have no circumflected forms of either breathing
    2) Upsilon has no capital forms with smooth breathing.


U+1F0-(0-7): Alpha lowercase
U+1F0-(8-F): Alpha uppercase
U+1F1-(0-5): Epsilon lower
U+1F1-(8-D): Epsilon lower
U+1F2-(0-7): Eta uppercase
U+1F2-(8-F): Eta lowercase
U+1F3-(0-7): Iota uppercase
U+1F3-(8-F): Iota lowercase
U+1F4-(0-5): Omicron lower
U+1F4-(8-D): Omicron lower

For U+1FBx. U+1FDx, U+1fEx

Combining diacritical marks
---------------------------

The unicode block U+0300 to U+036F supplies combining diacritical marks.
The correct display depends on the correct sequence of characters:

.. codeblock:: python

    >> alpha = "α"
    >> grave = "\u0300"
    >> rough = "\u0314"
    >> print(alpha + rough + grave)
    ἃ
    >> print(alpha + grave + rough)    
    ὰ̔



