"""Custom thumbnail: big two-line title on top, one character, one key prop (owner rule), neon story look."""
import os, math
import skia
from neon import *

s = skia.Surface(W, H); c = s.getCanvas()
c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(20, 130, 235), (110, 200, 255), (225, 245, 255)], [0, 0.55, 1]))
for i in range(16):
    a = math.radians(i * 22.5); p = path([(540, 1150), (540 + 1800 * math.cos(a - 0.07), 1150 + 1800 * math.sin(a - 0.07)), (540 + 1800 * math.cos(a + 0.07), 1150 + 1800 * math.sin(a + 0.07))])
    c.drawPath(p, P((255, 255, 255), 0.12))
c.drawCircle(540, 1150, 620, P((255, 255, 255), 0.45, 120)); cloud(c, 60, 820, 0.7); cloud(c, 760, 900, 0.55)
c.drawOval(skia.Rect.MakeXYWH(-100, 1480, 1280, 700), P((120, 210, 240)))
f = font('Anton.ttf', 132)
for i, (txt, col) in enumerate((('YOUR GIFT CARD =', (255, 255, 255)), ('THEIR PROFIT?', (255, 220, 60)))):
    y = 430 + i * 180; tw = f.measureText(txt)
    c.drawString(txt, 540 - tw / 2 + 12, y + 14, f, P((0, 0, 0), 0.8)); c.drawString(txt, 540 - tw / 2, y, f, S(INK, 26)); c.drawString(txt, 540 - tw / 2, y, f, P(col))
import random
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thumb_props.py')).read())
person(c, 760, 1760, 0.95, (255, 140, 40), (36, 44, 90), mood='shock', look=(-0.6, -0.5), sweat=2, t=0.4, arm_r=(170, -120), arm_l=(-30, 230), prop=(1, lambda cc, x, y: giftcard(cc, x, y - 80, 300, 10, (255, 80, 110), '$244', 1.0)))
[sparkle(c, x, y, r) for x, y, r in ((150, 760, 34), (930, 700, 26), (820, 1050, 20), (240, 1500, 28))]
vignette(c, 0.1)
c.drawRect(skia.Rect.MakeXYWH(14, 14, W - 28, H - 28), S((255, 255, 255), 28)); c.drawRect(skia.Rect.MakeXYWH(28, 28, W - 56, H - 56), S(INK, 8))
s.makeImageSnapshot().save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thumbnail_gift_cards.png'), skia.kPNG)
print('ok')
