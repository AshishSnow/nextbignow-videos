"""Custom thumbnail: big two-line title on top, one character, one key prop (owner rule), neon story look."""
import os, math
import skia
from neon import *

s = skia.Surface(W, H); c = s.getCanvas()
c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(30, 14, 60), (90, 30, 110), (20, 10, 40)], [0, 0.55, 1]))
for i in range(16):
    a = math.radians(i * 22.5); p = path([(540, 1150), (540 + 1800 * math.cos(a - 0.07), 1150 + 1800 * math.sin(a - 0.07)), (540 + 1800 * math.cos(a + 0.07), 1150 + 1800 * math.sin(a + 0.07))])
    c.drawPath(p, P((255, 120, 255), 0.07))
c.drawCircle(540, 1150, 620, P((255, 80, 200), 0.35, 120))
f = font('Anton.ttf', 150)
for i, (txt, col) in enumerate((('DEALERS EARN', (255, 255, 255)), ('~5% ON CARS?', (255, 220, 60)))):
    y = 430 + i * 180; tw = f.measureText(txt)
    c.drawString(txt, 540 - tw / 2 + 12, y + 14, f, P((0, 0, 0), 0.8)); c.drawString(txt, 540 - tw / 2, y, f, S(INK, 26)); c.drawString(txt, 540 - tw / 2, y, f, P(col))
car(c, 470, 1250, 900, t=0.3)
person(c, 760, 1760, 0.95, (255, 140, 40), (36, 44, 90), mood='worried', look=(-0.6, -0.5), sweat=3, t=0.4, arm_r=(60, -200), arm_l=(-30, 230), prop=(1, keys))
vignette(c, 0.45); grain(c, 5, 0.04)
s.makeImageSnapshot().save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thumbnail_car_dealer.png'), skia.kPNG)
print('ok')
