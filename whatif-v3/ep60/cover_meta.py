import os, sys
os.environ.setdefault('MT_DIR', 'meta')
import skia, render_meta as RM
from comickit import *
from toon import W, H, R, paint, stroke
plat = sys.argv[1]
s = skia.Surface(W, H); c = s.getCanvas()
bg_flat(c, CRED, (190, 20, 30))
# key content inside the 4:5 feed crop (y 285-1635) and 3:4 grid crop (y 240-1680)
title(c, 'CAN APPS SEE', 540, 470, 118, PAPER, 1.0, 'c', rot=-2)
title(c, 'YOUR PHOTOS?', 540, 610, 128, CYEL, 1.0, 'c', rot=-2)
RM.phone(c, 540, 1080, 300, 1.0, 0.0, scan=1.0, rot=-5)
RM.fly_card(c, 'M3_camera', 700, 830, 300, 8, 1.0)
RM.fly_card(c, 'M4_rome', 60, 1150, 300, -7, 1.0)
burst(c, 820, 1420, 120, 'EUR 805M FINE', 1.0, size=30, col=CYEL, txt=CRED, rot=8)
img = s.makeImageSnapshot()
out = 'meta/cover_%s.png' % plat; img.save(out, skia.kPNG)
from PIL import Image
Image.open(out).convert('RGB').save('meta/cover_%s.jpg' % plat, quality=93)
print(out)
