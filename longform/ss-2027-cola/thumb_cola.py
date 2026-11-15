import os; os.environ['NBN_ORIENT'] = 'land'; os.environ['CO_DIR'] = 'cola'
import skia, math
import render_cola as RC
from comickit import *
from toon import W, H, R, paint, stroke
from photokit import place
s = skia.Surface(W, H); c = s.getCanvas()
bg_flat(c, CRED, (190, 20, 30))
title(c, 'YOUR 2027', 70, 230, 150, PAPER, 1.0, rot=-2)
title(c, 'RAISE:', 70, 400, 170, CYEL, 1.0, rot=-2)
title(c, '+$75?', 80, 700, 300, PAPER, 1.0, rot=-4)
c.drawLine(80, 640, 900, 560, stroke(KINK, 34)); c.drawLine(80, 640, 900, 560, stroke(CYEL, 20))
burst(c, 700, 860, 210, 'REALLY $68', 1.0, size=64, col=CYEL, txt=CRED, rot=-6)
RC.check_card(c, 1000, 150, 840, 400, 1.0, '+3.6%', 0)
place(c, 'D4_dollar_comic.png', 1420, 780, 760, rot=-8, a=1.0, shadow=True)
img = s.makeImageSnapshot()
img.save('cola/thumb_full.png', skia.kPNG)
from PIL import Image
Image.open('cola/thumb_full.png').convert('RGB').resize((1280, 720), Image.LANCZOS).save('cola/thumbnail.jpg', quality=92)
print('ok')
