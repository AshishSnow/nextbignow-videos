"""MIND TRICKS (purple) N° 05: the IKEA effect. ESSAY look; generic flat-pack box, no logos."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (138, 66, 214)
NS = 8; LABEL = 'MIND TRICKS — N° 05'
PLY = (222, 196, 150); PLY2 = (196, 166, 118); STEEL = (150, 150, 150)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def box(c, x, y, s=1.0, k=1.0, a=1.0, half=False):
    """storage box assembling: k 0..1 brings panels in"""
    c.save(); c.translate(x, y); c.scale(s, s)
    parts = [(-200, -180, 400, 24, (0, -260)), (-200, 156, 400, 24, (0, 260)), (-200, -180, 24, 360, (-300, 0)),
             (176, -180, 24, 360, (300, 0)), (-176, -12, 352, 20, (420, -120))]
    if half: parts = parts[:3]
    for i, (px, py, w, h, (dx, dy)) in enumerate(parts):
        kk = eo(cl(k * 1.6 - i * 0.15))
        r = skia.Rect.MakeXYWH(px + dx * (1 - kk), py + dy * (1 - kk), w, h)
        shape(c, r, PLY, 3, a * max(0.2, kk)); hatch(c, skia.Path.Rect(r), 0.18 * a, 7)
    if k > 0.95 and not half:
        c.drawRect(skia.Rect.MakeXYWH(-176, -156, 352, 144), P(PLY2, 0.35 * a)); c.drawRect(skia.Rect.MakeXYWH(-176, 8, 352, 148), P(PLY2, 0.35 * a))
    c.restore()


def allen(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, 0); p.lineTo(0, -140); p.lineTo(50, -140)
    c.drawPath(p, S(INKE, 22)); c.drawPath(p, S(STEEL, 14)); c.restore()


def tag(c, x, y, txt, k, col=None, rot=-6):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(eback(k), eback(k))
    f = anton(80); w = f.measureText(txt)
    shape(c, path([(-30, -60), (w + 40, -60), (w + 40, 60), (-30, 60), (-80, 0)]), col or (255, 214, 40), 4)
    c.drawCircle(-40, 0, 10, P(CREAM)); c.drawString(txt, 0, 28, f, P(INKE)); c.restore()


def s_hook(c, t):
    pg(c, False, 1, t)
    headline(c, [[('YOU BUILT IT.', False)], [('YOU PAY', False), ('MORE.', True)]], 150, 520, 124, 1.0)
    k = cl(t / 2.2); box(c, 540, 1120, 1.0, k)
    allen(c, 800, 1000 + 20 * math.sin(t * 6), 1.0, 0.4 * math.sin(t * 6))
    tag(c, 720, 860, '+63%', pr(t, 2.3, 0.4), ACC[0])


def s_proved(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('PROVEN WITH', False)], [('IKEA BOXES.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5), dark=True)
    body(c, 'NORTON, MOCHON & ARIELY (2012)', 150, 820, 30, MUTE, 'SemiBold', a=pr(t, t0 + 0.4, 0.4))
    box(c, 540, 1140, 0.9, 1.0)


def s_groups(c, t):
    t0 = SCENES[2][0]; tb = ph('already built'); pg(c, False, 3, t)
    headline(c, [[('BUILDERS', True), ('VS.', False)], [('LOOKERS.', False)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5))
    k = pr(t, t0 + 0.3, 2.0); box(c, 310, 1120, 0.6, k); allen(c, 440, 1040, 0.6, 0.5 * math.sin(t * 6))
    body(c, 'BUILT IT', 230, 1300, 36, INKE, 'Bold', a=pr(t, t0 + 0.4, 0.4))
    kk = pr(t, tb - 0.3, 0.4)
    if kk > 0: box(c, 780, 1120, 0.6, 1.0, kk); body(c, 'PRE-BUILT', 690, 1300, 36, INKE, 'Bold', a=kk)


def s_same(c, t):
    t0 = SCENES[3][0]; pg(c, True, 4, t)
    headline(c, [[('SAME BOX.', False)], [('WHO PAYS', False), ('MORE?', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    box(c, 330, 1140, 0.55, 1.0); box(c, 760, 1140, 0.55, 1.0)
    f = anton(120); c.drawString('?', 520, 1180, f, P(ACC[0], pr(t, t0 + 0.4, 0.3)))


def s_63(c, t):
    t0 = SCENES[4][0]; tk = ph('sixty three'); pg(c, False, 5, t)
    headline(c, [[('THE', False), ('BUILDERS.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    k = pr(t, tk - 0.2, 0.8)
    c.drawLine(150, 1300, 930, 1300, S(INKE, 4))
    for j, (v, l, col) in enumerate(((100, 'PRE-BUILT', (180, 172, 162)), (163, 'BUILT IT', ACC[0]))):
        h = 3.0 * v * (eo(k) if j else eo(pr(t, t0 + 0.3, 0.5)))
        c.drawRect(skia.Rect.MakeXYWH(230 + j * 380, 1300 - h, 240, h), P(col)); c.drawRect(skia.Rect.MakeXYWH(230 + j * 380, 1300 - h, 240, h), S(INKE, 4))
        g = font(32, 'Bold', False); c.drawString(l, 350 + j * 380 - g.measureText(l) / 2, 1350, g, P(INKE))
    if k > 0:
        s_ = '+%d%%' % int(63 * eo(k)); f = anton(150); c.drawString(s_, 600, 760, f, P(ACC[0], k))
    body(c, 'WILLING TO PAY', 610, 800, 28, MUTE, 'SemiBold', a=k)


def s_name(c, t):
    t0 = SCENES[5][0]; pg(c, True, 6, t)
    body(c, "IT'S CALLED", 150, 520, 32, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    headline(c, [[('THE', False), ('IKEA EFFECT.', True)]], 150, 680, 124, pr(t, t0 + 0.1, 0.5), dark=True)
    box(c, 540, 1160, 0.75, 1.0)
    k = pr(t, ph('love') - 0.2, 0.4)
    if k > 0:
        c.save(); c.translate(540, 980 - 20 * math.sin(t * 3)); c.scale(eback(k) * 1.4, eback(k) * 1.4)
        h = skia.Path(); h.moveTo(0, 30); h.cubicTo(-60, -10, -40, -60, 0, -30); h.cubicTo(40, -60, 60, -10, 0, 30); h.close()
        c.drawPath(h, P(ACC[0])); c.drawPath(h, S(CREAM_T, 4)); c.restore()


def s_catch(c, t):
    t0 = SCENES[6][0]; ts = ph('in the study'); pg(c, False, 7, t)
    if t < ts - 0.2:
        headline(c, [[('THE', False), ('CATCH?', True)]], 150, 520, 150, pr(t, t0 + 0.05, 0.5))
        box(c, 540, 1140, 0.8, 1.0)
    else:
        headline(c, [[("DIDN'T FINISH?", False)], [('NO', False), ('EFFECT.', True)]], 150, 520, 124, pr(t, ts - 0.2, 0.4))
        box(c, 540, 1160, 0.8, 0.6 + 0.1 * math.sin(t * 2), 1.0, half=True)
        allen(c, 760, 1260, 0.8, 1.2)


def s_end(c, t):
    t0 = SCENES[7][0]; tj = ph('just make')
    if t < tj - 0.3:
        pg(c, False, 8, t)
        headline(c, [[('LET THEM', False)], [('BUILD A', False), ('LITTLE.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
        box(c, 540, 1140, 0.8, cl((t - t0) / 1.5)); allen(c, 780, 1060, 0.8, 0.4 * math.sin(t * 6))
    else:
        final_fill(c, LABEL, num(8), t / DUR, ('JUST MAKE SURE', 'THEY FINISH.'), pr(t, tj - 0.3, 0.5), 130)
        box(c, 540, 1240, 0.55, 1.0)


SCENES = [(0.0, s_hook), (ph('researchers proved') - 0.15, s_proved), (ph('some people') - 0.15, s_groups), (ph('same box') - 0.15, s_same),
          (ph('the builders') - 0.15, s_63), (ph("it's called") - 0.15, s_name), (ph('the catch') - 0.15, s_catch), (ph('so let') - 0.15, s_end)]
DARK_S = {1, 3, 5}
FILL_T = ph('just make') - 0.3
SHAKES = [(ph('badly'), 8, 0.3), (ph('sixty three'), 12, 0.4), (ph("didn't finish"), 8, 0.3), (ph('just make'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='MIND TRICKS', num='N° 05')
    headline(c, [[('YOU BUILT IT.', False)], [('YOU PAY', False), ('63% MORE.', True)]], 150, 540, 124, 1.0, maxw=860)
    box(c, 540, 1200, 0.95, 1.0); allen(c, 820, 1100, 1.0, 0.3)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
