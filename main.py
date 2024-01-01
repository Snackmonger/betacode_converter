from src.tokenizer import BetacodeTokenizer
x = r"""mh=nin a)/eide qea\ phlhi+a/dew A)xilh=os, ou)lome/nhn, h(\ muri/’ A)xaioi=s a)/lge’ e)/qhke zhno\s e)/oi ti/ ken a)/llo para\ spondh=|sin a)ei/dein lw/ion h)\ qeo\n au)to/n, a)ei\ me/gan, ai)e\n a)/nakta, phlago/nwn e)lath=ra, dikaspo/lon ou)rani/dh|si; pw=s kai/ min, diktai=on a)ei/somen h)e\ lukai=on; rh=ma"""


y = BetacodeTokenizer(x)

print(y)