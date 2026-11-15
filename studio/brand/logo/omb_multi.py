import sys, os, math
sys.path.insert(0, '/home/claude/studio/projects/pet-rock/comic'); os.chdir('/home/claude/studio/projects/pet-rock/comic')
import skia, numpy as np, cv2
from toon import R, paint, stroke, poly
from comickit import dots, title, caption, font, KINK, PAPER
OUT = '/home/claude/studio/projects/omb-logo'; S = 1024
BLUE, TEAL, PURP, GRN, ORG, YEL, PINK, LIME, NAVY = (36, 99, 235), (0, 150, 136), (110, 60, 200), (30, 170, 90), (255, 120, 20), (255, 214, 10), (255, 110, 170), (190, 240, 40), (24, 40, 110)
def shade(c, k): return tuple(int(v * k) for v in c)
def save(s, n): cv2.imwrite(f'{OUT}/{n}.png', np.ascontiguousarray(s.makeImageSnapshot().toarray()[..., :4]))
def letters(c, cols, y=S / 2 + 90, size=300, rot=-8, cx=S / 2):
    f = font('LuckiestGuy.ttf', size); ws = [f.measureText(ch) for ch in 'OMB']; x = cx - sum(ws) / 2 - 20
    c.save(); c.translate(cx, y); c.rotate(rot); c.translate(-cx, -y)
    for ch, w, col in zip('OMB', ws, cols):
        title(c, ch, x, y, size, col, 1.0, 'l', shadow=14); x += w + 8
    c.restore()

# A: striped badge (6 colours) + 3-colour letters
s = skia.Surface(S, S); c = s.getCanvas(); c.clear(skia.Color(0, 0, 0, 0))
c.save(); c.translate(S / 2, S / 2); c.rotate(-8)
b = skia.RRect.MakeRectXY(R.MakeXYWH(-410, -260, 820, 520), 60, 60)
c.save(); c.translate(18, 18); c.drawRRect(b, paint(KINK)); c.restore()
c.save(); c.clipRRect(b, doAntiAlias=True)
for i, col in enumerate((BLUE, TEAL, GRN, YEL, ORG, PURP)):
    p = poly([(-420 + i * 150, -300), (-250 + i * 150, -300), (-330 + i * 150, 300), (-500 + i * 150, 300)], True) if i < 5 else poly([(-420 + i * 150, -300), (600, -300), (600, 300), (-500 + i * 150, 300)], True); c.drawPath(p, paint(col))
dots(c, (-410, -260, 820, 520), KINK, cell=20, rmax=5, grad=(0.3, 1), a=0.18)
c.restore(); c.drawRRect(b, stroke(KINK, 16)); c.restore()
letters(c, (PAPER, PINK, LIME))
title(c, '!', S / 2 + 340, S / 2 - 120, 200, YEL, 1.0, 'c', shadow=8, rot=12)
caption(c, 'OOPS MY BUSINESS', 230, 800, 1.0, col=PAPER, size=54, rot=-8)
save(s, 'omb_multi_A_stripes')

# B: navy badge, each letter its own colour, colourful halftone corners + confetti
s = skia.Surface(S, S); c = s.getCanvas(); c.clear(skia.Color(0, 0, 0, 0))
c.save(); c.translate(S / 2, S / 2); c.rotate(-8)
b = skia.RRect.MakeRectXY(R.MakeXYWH(-410, -260, 820, 520), 60, 60)
c.save(); c.translate(18, 18); c.drawRRect(b, paint(KINK)); c.restore(); c.drawRRect(b, paint(NAVY))
c.save(); c.clipRRect(b, doAntiAlias=True)
dots(c, (-410, -260, 820, 520), TEAL, cell=22, rmax=7, grad=(0.55, 1), angle=45, a=0.9)
dots(c, (-410, -260, 820, 520), PURP, cell=22, rmax=7, grad=(0.55, 1), angle=225, a=0.9)
c.restore(); c.drawRRect(b, stroke(KINK, 16)); c.restore()
for i, (x, y, col) in enumerate(((180, 230, ORG), (860, 820, GRN), (150, 700, PINK), (880, 230, LIME), (520, 150, BLUE))):
    c.save(); c.translate(x, y); c.rotate(30 * i); c.drawRect(R.MakeXYWH(-22, -10, 44, 20), paint(col)); c.drawRect(R.MakeXYWH(-22, -10, 44, 20), stroke(KINK, 4)); c.restore()
letters(c, (YEL, PINK, LIME))
title(c, '!', S / 2 + 340, S / 2 - 120, 200, ORG, 1.0, 'c', shadow=8, rot=12)
caption(c, 'OOPS MY BUSINESS', 230, 800, 1.0, col=YEL, size=54, rot=-8)
save(s, 'omb_multi_B_navy')

# C: round sticker, 6-colour ring, black centre
s = skia.Surface(S, S); c = s.getCanvas(); c.clear(skia.Color(0, 0, 0, 0))
cx = cy = S / 2; r0, r1 = 300, 470
c.drawCircle(cx + 14, cy + 14, r1, paint(KINK))
cols = (BLUE, TEAL, GRN, YEL, ORG, PINK, PURP, LIME)
for i, col in enumerate(cols):
    a0 = -90 + i * 360 / len(cols)
    p = skia.Path(); p.moveTo(cx, cy); p.arcTo(R.MakeXYWH(cx - r1, cy - r1, 2 * r1, 2 * r1), a0, 360 / len(cols), False); p.close(); c.drawPath(p, paint(col))
c.drawCircle(cx, cy, r1, stroke(KINK, 14))
c.drawCircle(cx, cy, r0, paint((28, 28, 34))); c.save(); pp = skia.Path(); pp.addCircle(cx, cy, r0); c.clipPath(pp, doAntiAlias=True)
dots(c, (cx - r0, cy - r0, 2 * r0, 2 * r0), (60, 60, 70), cell=18, rmax=5, grad=(0.4, 1), a=1.0); c.restore()
c.drawCircle(cx, cy, r0, stroke(KINK, 14))
letters(c, (YEL, PINK, LIME), y=cy + 65, size=200, rot=-6)
title(c, '!', cx + 225, cy - 95, 140, ORG, 1.0, 'c', shadow=6, rot=12)
f = font('SpecialElite.ttf', 50); txt = 'OOPS MY BUSINESS'
tw = f.measureText(txt); c.save(); c.translate(cx, cy + 175); c.drawString(txt, -tw / 2, 0, f, paint(PAPER)); c.restore()
save(s, 'omb_multi_C_ring')

ims = [cv2.imread(f'{OUT}/{n}.png', cv2.IMREAD_UNCHANGED) for n in ('omb_multi_A_stripes', 'omb_multi_B_navy', 'omb_multi_C_ring')]
sheet = np.full((560, 3 * 540 + 20, 3), (210, 241, 252), np.uint8)
for i, im in enumerate(ims):
    im = cv2.resize(im, (520, 520)); a = im[..., 3:4] / 255.0; x = 20 + i * 540
    roi = sheet[20:540, x:x + 520]; roi[:] = (roi * (1 - a) + im[..., :3] * a).astype(np.uint8)
    cv2.putText(sheet, 'ABC'[i], (x + 10, 70), 0, 1.6, (40, 40, 40), 4)
cv2.imwrite(f'{OUT}/omb_multi_compare.png', sheet); print('ok')
