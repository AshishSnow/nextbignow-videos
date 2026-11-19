def cl(x): return max(0.0, min(1.0, x))
def pr(t, t0, d): return cl((t - t0) / d)
def eo(x): return 1 - (1 - x) ** 3
def eio(x): return 3 * x * x - 2 * x * x * x
def eback(x, s=1.70158): x -= 1; return x * x * ((s + 1) * x + s) + 1
def ctext(c, s, x, y, size, rgb, fn='Montserrat-Black.ttf', a=1.0):
    f = font(fn, size); c.drawString(s, x - f.measureText(s) / 2, y, f, P(rgb, a))
def pop(c, k, x, y, fn): fn()
def blinking(t, seed=0): return False
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scenes_gift.py')).read()
exec(_src[:_src.index('# ------------------------------------------------------------------ scenes')])
for i in range(7):
    giftcard(c, 160 + i * 75, 1250 - (i % 2) * 60, 230, -30 + i * 10, CARDCOLS[i % 6], '', 1.0, t=0.5)
