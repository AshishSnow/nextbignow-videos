import sys, os
sys.path.insert(0, '/home/claude/studio/projects/pet-rock/comic'); os.chdir('/home/claude/studio/projects/pet-rock/comic')
import skia, numpy as np, cv2
from toon import R, paint, stroke
from comickit import dots, title, caption, KINK, PAPER
OUT = '/home/claude/studio/projects/omb-logo'; S = 1024
def shade(c, k): return tuple(int(v * k) for v in c)
VAR = [  # name, badge, letters, bang, tape
    ('blue_yellow', (36, 99, 235), (255, 214, 10), (255, 255, 255), (255, 214, 10)),
    ('teal_orange', (0, 150, 136), (255, 140, 30), (255, 245, 220), (255, 140, 30)),
    ('purple_lime', (110, 60, 200), (190, 240, 40), (255, 255, 255), (190, 240, 40)),
    ('green_pink', (30, 170, 90), (255, 110, 170), (255, 255, 255), (255, 230, 240)),
    ('black_yellow', (28, 28, 34), (255, 214, 10), (255, 214, 10), (255, 214, 10)),
    ('orange_navy', (255, 120, 20), (24, 40, 110), (255, 255, 255), (255, 240, 210)),
]
files = []
for name, bc, lc, xc, tc in VAR:
    s = skia.Surface(S, S); c = s.getCanvas(); c.clear(skia.Color(0, 0, 0, 0))
    c.save(); c.translate(S / 2, S / 2); c.rotate(-8)
    b = skia.RRect.MakeRectXY(R.MakeXYWH(-400, -260, 800, 520), 60, 60)
    c.save(); c.translate(18, 18); c.drawRRect(b, paint(KINK)); c.restore(); c.drawRRect(b, paint(bc))
    dots(c, (-400, -260, 800, 520), shade(bc, 0.78), cell=20, rmax=6, grad=(0.3, 1), a=0.9)
    c.drawRRect(b, stroke(KINK, 16)); c.restore()
    title(c, 'OMB', S / 2, S / 2 + 90, 300, lc, 1.0, 'c', shadow=14, rot=-8)
    title(c, '!', S / 2 + 330, S / 2 - 120, 200, xc, 1.0, 'c', shadow=8, rot=12)
    caption(c, 'OOPS MY BUSINESS', 230, 800, 1.0, col=tc, size=54, rot=-8)
    f = f'{OUT}/omb_{name}.png'; cv2.imwrite(f, np.ascontiguousarray(s.makeImageSnapshot().toarray()[..., :4])); files.append(f)
sheet = np.full((2 * 540 + 20, 3 * 540 + 20, 3), (210, 241, 252), np.uint8)
for i, f in enumerate(files):
    im = cv2.resize(cv2.imread(f, cv2.IMREAD_UNCHANGED), (520, 520)); a = im[..., 3:4] / 255.0
    y, x = 20 + (i // 3) * 540, 20 + (i % 3) * 540
    roi = sheet[y:y + 520, x:x + 520]; roi[:] = (roi * (1 - a) + im[..., :3] * a).astype(np.uint8)
    cv2.putText(sheet, str(i + 1), (x + 10, y + 50), 0, 1.5, (40, 40, 40), 4)
cv2.imwrite(f'{OUT}/omb_variants_compare.png', sheet); print('ok')
