import os, sys
os.environ.setdefault('NBN_WM', 'brand_logo_port.png')
import skia, render_juliane as RJ
from toon import W, H, R, paint
s = skia.Surface(W, H); c = s.getCanvas()
RJ.shot(c, 'J3_storm', 0, 0, 1, 'night', 1.2, 1.2, 0.5, 0.5, 0.45, 0.45)
RJ.vignette(c, 0.7); RJ.band(c, 700, 1500, 0.85)
RJ.tag(c, 'TRUE STORY . 1971', 1.0, x=90, y=420)
RJ.big(c, 'SHE FELL FROM THE SKY', '2 MILES', 1.0, y=1080, size=230, col=RJ.WHITE)
RJ.big(c, None, '...AND LIVED.', 1.0, y=1250, size=140, col=RJ.YEL)
out = 'juliane/cover.png'; s.makeImageSnapshot().save(out, skia.kPNG)
from PIL import Image; Image.open(out).convert('RGB').save('juliane/cover.jpg', quality=93); print('ok')
