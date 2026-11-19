def cl(x): return max(0.0, min(1.0, x))
def ctext(c, s, x, y, size, rgb, fn='Montserrat-Black.ttf', a=1.0):
    f = font(fn, size); c.drawString(s, x - f.measureText(s) / 2, y, f, P(rgb, a))
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scenes_returns.py')).read()
exec(_src[:_src.index('# ------------------------------------------------------------------ scenes')])
pallet(c, 330, 1330, 520)
for row in range(3):
    for j in range(3 - row): box(c, 330 + (j - (2 - row) / 2) * 160, 1250 - row * 118, 155, 115)
