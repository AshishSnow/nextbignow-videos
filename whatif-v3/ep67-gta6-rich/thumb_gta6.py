"""Thumbnail ep67: big two-line title, one character (streamer), one prop (phone LIVE + cash)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
sys.argv = [sys.argv[0], os.path.join(HERE, 'gta6', 'fake')]
import paint_gta6 as G
import skia
W, H = 1080, 1920
surf = skia.Surface(W, H); c = surf.getCanvas()
G.sunset_bg(c, 3.0, 980)
G.glow(c, W / 2, 1150, 650, G.PINK, .45)
G.money(c, 7.3, 11, 34, 1.0, 1.0)
G.palm(c, 90, 1500, 1.25, 1, lean=.2); G.palm(c, 1010, 1520, 1.1, 2, lean=-.3)
G.phone(c, 720, 1130, 1.05, 1, 2.0, 'live', rot=8)                    # prop
G.glow(c, 330, 1180, 360, G.TEAL, .5)
c.saveLayer(); G.person(c, 330, 1560, 1.96, G.TEAL, 'streamer', 0, 1)
c.restore()
rim = skia.Paint(); rim.setImageFilter(skia.ImageFilters.Blur(10, 10))
c.saveLayer(None, rim); G.person(c, 330, 1560, 1.97, G.TEAL, 'streamer', 0, .9); c.restore()
G.person(c, 336, 1560, 1.9, (28, 8, 40), 'streamer', 0, 1)             # character with teal rim light
G.chip(c, 'NOT JUST ROCKSTAR', W / 2, 330, (230, 40, 90), f=G.LBL)
G.neon(c, 'GTA 6 WILL', 560, 210, 1, sk=-.06)
G.neon(c, 'MAKE THEM RICH', 760, 150, 1, top=G.YEL, bot=G.GREEN, glowc=G.GREEN)
G.grain(c, .14); c.drawImage(G.WM, 0, 0)
surf.makeImageSnapshot().save(OUT + '.png', skia.kPNG)
from PIL import Image
Image.open(OUT + '.png').convert('RGB').save(OUT + '.jpg', quality=95); print(OUT)
