import os; os.environ['NBN_ORIENT'] = 'land'
import skia, math
import render_mlong as RM
from comickit import *
from toon import W, H, R, paint, stroke
from photokit import place
s = skia.Surface(W, H); c = s.getCanvas()
bg_flat(c, CRED, (190, 20, 30))
title(c, 'MEASLES IS', 70, 250, 160, PAPER, 1.0, rot=-2)
title(c, 'BACK.', 70, 470, 260, CYEL, 1.0, rot=-3)
RM.stamp(c, 'ELIMINATED 2000', 470, 700, 64, CBLU, 1.0, rot=-5, fill=PAPER)
c.drawLine(140, 700, 800, 640, stroke(KINK, 14)); c.drawLine(140, 700, 800, 640, stroke(CRED, 8))
burst(c, 760, 880, 150, '5,412', 1.0, size=80, col=CYEL, txt=CRED, rot=-6)
caption(c, 'US CASES IN 2026:', 120, 900, 1.0, col=CYEL, size=44, rot=-2)
RM.virus(c, 1400, 520, 820, 0.0, 1.0, rot0=-8)
s.makeImageSnapshot().save('mlong/thumb_full.png', skia.kPNG)
from PIL import Image
Image.open('mlong/thumb_full.png').convert('RGB').resize((1280, 720), Image.LANCZOS).save('mlong/thumbnail.jpg', quality=92)
print('ok')
