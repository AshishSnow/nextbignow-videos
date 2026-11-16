import os, sys
import skia, render_measles as RM
from comickit import *
from toon import W, H, R, paint, stroke
plat = sys.argv[1]
s = skia.Surface(W, H); c = s.getCanvas()
bg_flat(c, CRED, (190, 20, 30))
title(c, 'MEASLES IS', 540, 480, 128, PAPER, 1.0, 'c', rot=-2)
title(c, 'BACK IN THE U.S.', 540, 620, 104, CYEL, 1.0, 'c', rot=-2)
RM.virus(c, 540, 1060, 560, 0.0, 1.0, rot0=-8)
c.save(); c.translate(540, 1420); c.rotate(-5)
tw_ = width('ELIMINATED IN 2000', 'SpecialElite.ttf', 54)
c.drawRect(R.MakeXYWH(-tw_/2 - 34 + 10, -62 + 10, tw_ + 68, 96), paint(KINK))
c.drawRect(R.MakeXYWH(-tw_/2 - 34, -62, tw_ + 68, 96), paint(PAPER))
c.drawRect(R.MakeXYWH(-tw_/2 - 34, -62, tw_ + 68, 96), stroke(KINK, 6))
c.drawString('ELIMINATED IN 2000', -tw_/2, 4, font('SpecialElite.ttf', 54), paint(CBLU))
c.restore()
RM.strike(c, 240, 1420, 840, 1376, 1.0, col=CRED, wdt=7)
burst(c, 860, 840, 120, '5,400+ CASES', 1.0, size=30, col=CYEL, txt=CRED, rot=8)
img = s.makeImageSnapshot()
out = 'measles/cover_%s.png' % plat; img.save(out, skia.kPNG)
from PIL import Image
Image.open(out).convert('RGB').save('measles/cover_%s.jpg' % plat, quality=93)
print(out)
