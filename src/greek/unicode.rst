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


A few characters from the Coptic block supply a few missing forms:
(N.B. decomposition of a symbol with a vowel and only an acute will recompose
into a character from the Coptic block)

::

    U+03AA   Ϊ
    U+03AB   Ϋ
    U+03CA   ϊ
    U+03CB   ϋ

Note: We can have capital upsilon with no markings, or with rough breathings etc., but not with smooth breathings etc.
We have no characters to represent contradictory or self-evident things: neither circumflex nor macron can exist on short 
vowels, nor brevia on long vowels, nor diaereses on non-high vowels, nor subscripts on high vowels


Notes:

For U+1F0x to U+1F6x and U+1F8x to U+1FAx:

::

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

::

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

If we wanted to use this for the program, we would need to sort the symbols into the correct order before trying to render. 



