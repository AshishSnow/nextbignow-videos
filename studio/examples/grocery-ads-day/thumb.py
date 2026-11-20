"""YouTube Shorts first-frame thumbnail v2 (20 Nov): 2 short lines (<=3 words each) huge, one giant expressive face, one big prop, high contrast."""
import os, sys, math, random, skia
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neon import *
def cl(x): return max(0.0, min(1.0, x))
def ctext(c, s, x, y, size, rgb, fn='Montserrat-Black.ttf', a=1.0):
    f = font(fn, size); c.drawString(s, x - f.measureText(s) / 2, y, f, P(rgb, a))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scenes_grocery.py')).read()
exec(src[:src.index('def store_inside')])
s = skia.Surface(W, H); c = s.getCanvas()
c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(0, 120, 235), (60, 190, 255), (200, 240, 255)], [0, 0.55, 1]))
for i in range(18):
    a = math.radians(i * 20); p = path([(540, 1200), (540 + 2000 * math.cos(a - 0.08), 1200 + 2000 * math.sin(a - 0.08)), (540 + 2000 * math.cos(a + 0.08), 1200 + 2000 * math.sin(a + 0.08))])
    c.drawPath(p, P((255, 255, 255), 0.13))
f = font('Anton.ttf', 190)
for i, (txt, col) in enumerate((('STORES MAKE', (255, 255, 255)), ('JUST 2¢?!', (255, 220, 40)))):
    y = 470 + i * 210; tw = f.measureText(txt)
    while tw > 960: f = font('Anton.ttf', f.getSize() * 0.95); tw = f.measureText(txt)
    c.drawString(txt, 540 - tw / 2 + 14, y + 16, f, P(INK, 0.85)); c.drawString(txt, 540 - tw / 2, y, f, S(INK, 30)); c.drawString(txt, 540 - tw / 2, y, f, P(col))
milk(c, 290, 1250, 3.0, -12)
c.drawCircle(760, 1330, 380, P((255, 255, 255), 0.5, 90))
head(c, 740, 1350, 330, (255, 140, 40), 'shock', (-0.5, -0.3), 3, 0.35)
sparkle(c, 140, 900, 40); sparkle(c, 960, 860, 30); sparkle(c, 560, 1700, 34)
s.makeImageSnapshot().save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thumbnail_grocery.png'), skia.kPNG); print('ok')
