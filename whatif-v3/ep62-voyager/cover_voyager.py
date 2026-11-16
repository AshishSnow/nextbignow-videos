import os, sys
import skia, render_voyager as RV
from comickit import *
from toon import W, H, R, paint, stroke
plat = sys.argv[1]
s = skia.Surface(W, H); c = s.getCanvas()
bg_flat(c, KINK, (40, 36, 30))
caption(c, 'VOYAGER 1 . NOV 18, 2026', 330, 300, 1.0, col=CYEL, size=30)
title(c, 'LIGHT NEEDS', 540, 470, 120, PAPER, 1.0, 'c', rot=-2)
title(c, 'A FULL DAY', 540, 610, 130, CYEL, 1.0, 'c', rot=-2)
title(c, 'TO REACH IT', 540, 740, 100, PAPER, 1.0, 'c', rot=-2)
RV.earth(c, 200, 1380, 60)
RV.beam(c, 270, 1360, 700, 1180, 1.0)
RV.probe(c, 640, 1090, 620, 0.0, 1.0, rot0=-8)
burst(c, 830, 1400, 130, '16B MILES', 1.0, size=44, col=CRED, txt=CYEL, rot=6)
out = 'voyager/cover_%s.png' % plat; s.makeImageSnapshot().save(out, skia.kPNG)
from PIL import Image
Image.open(out).convert('RGB').save('voyager/cover_%s.jpg' % plat, quality=93); print(out)
