import os, sys
import skia, render_elnino as RE
from comickit import *
from toon import W, H, R, paint, stroke
plat = sys.argv[1]
s = skia.Surface(W, H); c = s.getCanvas()
RE.flow_bg(c, 0.0, CRED, cy=1020, r0=500)
caption(c, 'NOAA . NOVEMBER 2026', 340, 285, 1.0, col=CYEL, size=30)
title(c, 'SUPER', 540, 480, 170, PAPER, 1.0, 'c', rot=-2)
title(c, 'EL NINO', 540, 640, 170, CYEL, 1.0, 'c', rot=-2)
RE.cut(c, 'E1_cut_comic.png', 540, 1060, 600, 1.0, rot=-6, t=0.0, bob=0)
g = skia.Paint(AntiAlias=True)
g.setShader(skia.GradientShader.MakeRadial((430, 1100), 300, [RE.argb(CRED, 0.75), RE.argb(RE.ORG, 0.4), RE.argb(RE.ORG, 0.0)], [0.0, 0.55, 1.0]))
c.drawCircle(430, 1100, 300, g)
RE.thermo(c, 860, 1380, 380, 0.95, 1.0, 0.0)
burst(c, 230, 1380, 120, '+2 C', 1.0, size=72, col=CYEL, txt=CRED, rot=-8)
out = 'elnino/cover_%s.png' % plat; s.makeImageSnapshot().save(out, skia.kPNG)
from PIL import Image
Image.open(out).convert('RGB').save('elnino/cover_%s.jpg' % plat, quality=93); print(out)
