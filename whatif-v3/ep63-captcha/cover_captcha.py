import os, sys
import skia, render_captcha as RC
from comickit import *
from toon import W, H, R, paint, stroke
plat = sys.argv[1]
s = skia.Surface(W, H); c = s.getCanvas()
bg_flat(c, CRED, (190, 20, 30))
title(c, "DON'T CLICK", 540, 470, 140, PAPER, 1.0, 'c', rot=-2)
title(c, 'THIS BOX', 540, 620, 150, CYEL, 1.0, 'c', rot=-2)
def body(cc, w, h):
    cc.drawRect(R.MakeWH(w, h), paint((230, 234, 240)))
    RC.verify_box(cc, 50, 40, w - 100, 150, 0.0)
RC.browser(c, 150, 760, 780, 330, 1.0, -1.5, body)
for i, k in enumerate(('WIN+R', 'CTRL+V', 'ENTER')):
    RC.keycap(c, 230 + i * 310, 1260, k, 1.0, w=270)
burst(c, 860, 760, 110, 'SCAM!', 1.0, size=48, col=CYEL, txt=CRED, rot=8)
out = 'captcha/cover_%s.png' % plat; s.makeImageSnapshot().save(out, skia.kPNG)
from PIL import Image
Image.open(out).convert('RGB').save('captcha/cover_%s.jpg' % plat, quality=93); print(out)
