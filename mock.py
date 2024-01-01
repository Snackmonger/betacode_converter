# import re

# x = ['red', 'debd', 'redeemer', 'eem', 'dream', 'drefs']


# search = "redeemert"
# y = re.findall(fr"({search}[\w]*)", " ".join(x))
# print(y)


from src.constants import *
from src.tokenizer import BetacodeTokenizer

lis_t: list[str] = []
for vowel in VOWELS:
    for diacritical in ALL_DIACRITICALS:
        lis_t.append(vowel+diacritical)
lis_t += [x.upper() for x in lis_t]


y = BetacodeTokenizer(" ".join(lis_t))
print(y)