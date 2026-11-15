import sys, os
sys.path.insert(0, '/home/claude/studio/projects/pet-rock/comic'); os.chdir('/home/claude/studio/projects/pet-rock/comic')
import skia, numpy as np, cv2
from toon import R, paint, stroke
from comickit import dots, title, font, KINK
OUT = '/home/claude/studio/projects/omb-logo/slip'; S = 1024
def dk(c, k): return tuple(min(255, int(v * k)) for v in c)
VAR = [  # name, badge, letters, strip bg, strip text
    ('A_blue_yellow', (30, 90, 230), (255, 214, 0), (255, 214, 0), (20, 40, 110)),
    ('B_black_yellow', (24, 24, 30), (255, 214, 0), (255, 214, 0), (24, 24, 30)),
    ('C_purple_mint', (92, 44, 180), (90, 235, 180), (90, 235, 180), (50, 20, 110)),
    ('D_red_cream', (225, 40, 50), (255, 244, 214), (255, 214, 0), (24, 24, 30)),
]
for name, bc, lc, sb, st in VAR:
    s = skia.Surface(S, S); c = s.getCanvas(); c.clear(0)
    c.save(); c.translate(512, 480); c.rotate(-6)
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-410, -260, 820, 480), 70, 70))
    c.save(); c.translate(16, 16); c.drawPath(p, paint(KINK)); c.restore(); c.drawPath(p, paint(bc))
    c.save(); c.clipPath(p, doAntiAlias=True); dots(c, (-410, -260, 820, 480), dk(bc, 0.72) if bc != (24, 24, 30) else (60, 60, 70), cell=20, rmax=6, grad=(0.3, 1), a=0.7); c.restore()
    c.drawPath(p, stroke(KINK, 14)); c.restore()
    title(c, 'OM', 370, 560, 280, lc, 1.0, 'c', shadow=14, rot=-6)
    title(c, 'B', 660, 525, 280, lc, 1.0, 'c', shadow=14, rot=24)      # the B slipping
    for i in range(3): c.drawLine(790 + i * 10, 335 + i * 40, 852 + i * 10, 318 + i * 40, stroke(lc, 12))
    # strip
    f = font('LuckiestGuy.ttf', 64); txt = 'OOPS MY BUSINESS'; w = f.measureText(txt) + 70; h = 96
    c.save(); c.translate(512, 790); c.rotate(-6)
    c.drawRect(R.MakeXYWH(-w / 2 + 10, -h / 2 + 10, w, h), paint(KINK)); c.drawRect(R.MakeXYWH(-w / 2, -h / 2, w, h), paint(sb))
    c.drawRect(R.MakeXYWH(-w / 2, -h / 2, w, h), stroke(KINK, 9)); c.drawString(txt, -w / 2 + 35, 24, f, paint(st)); c.restore()
    cv2.imwrite(f'{OUT}/omb_slip_{name}.png', np.ascontiguousarray(s.makeImageSnapshot().toarray()))
B = np.full((2 * 560 + 30, 2 * 560 + 30, 3), (210, 241, 252), np.uint8)
for i, (n, *_) in enumerate(VAR):
    im = cv2.resize(cv2.imread(f'{OUT}/omb_slip_{n}.png', cv2.IMREAD_UNCHANGED), (520, 520), interpolation=cv2.INTER_AREA); a = im[..., 3:4] / 255.
    y, x = 30 + (i // 2) * 560, 30 + (i % 2) * 560; r = B[y:y + 520, x:x + 520]; r[:] = (r * (1 - a) + im[..., :3] * a).astype(np.uint8)
    cv2.putText(B, 'ABCD'[i], (x + 4, y + 44), 0, 1.4, (40, 40, 40), 4)
cv2.imwrite(f'{OUT}/0_slip_colours.png', B); print('ok')
