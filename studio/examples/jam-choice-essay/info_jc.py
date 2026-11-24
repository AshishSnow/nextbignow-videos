"""MIND TRICKS (purple) N° 04: the jam study (choice overload). ESSAY look; generic jars, no brands."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (138, 66, 214)
NS = 9; LABEL = 'MIND TRICKS — N° 04'
JAMS = [(170, 40, 60), (214, 90, 40), (120, 30, 90), (220, 150, 40), (90, 20, 40), (200, 60, 90)]
WOOD = (176, 128, 84)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def jar(c, x, y, s=1.0, col=(170, 40, 60), a=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    shape(c, rr(-34, -96, 68, 22, 5), (240, 236, 226), 3, a)
    for i in range(5): c.drawLine(-30 + i * 15, -96, -34 + i * 15, -74, S(INKE, 1.5, 0.5 * a))
    b = rr(-44, -74, 88, 110, 16); shape(c, b, col, 4, a)
    c.drawRect(skia.Rect.MakeXYWH(-30, -46, 60, 44), P((246, 240, 228), a)); c.drawRect(skia.Rect.MakeXYWH(-30, -46, 60, 44), S(INKE, 2, a))
    c.drawLine(-22, -30, 22, -30, S(INKE, 2, 0.5 * a)); c.drawLine(-22, -18, 12, -18, S(INKE, 2, 0.5 * a))
    c.drawLine(-32, -60, -28, 20, S(WHITE, 5, 0.45 * a))
    c.restore()


def table(c, x, y, w, n, t=0.0, k=1.0, s=1.0, rows=1):
    """table of n jars; k = reveal"""
    shape(c, skia.Rect.MakeXYWH(x - w / 2, y, w, 26), WOOD); hatch(c, skia.Path.Rect(skia.Rect.MakeXYWH(x - w / 2, y, w, 26)), 0.3, 8)
    for lx in (x - w / 2 + 20, x + w / 2 - 40): shape(c, skia.Rect.MakeXYWH(lx, y + 26, 20, 140), WOOD)
    per = (n + rows - 1) // rows
    for r in range(1, rows):
        sy = y - r * 150 * s + 34 * s; shape(c, skia.Rect.MakeXYWH(x - w / 2 + 10, sy, w - 20, 14), WOOD, 3)
    for i in range(n):
        r = i // per; q = i % per
        kk = cl(k * n * 1.2 - i * 1.0 * 1.2 / 1.2) if k < 1 else 1.0
        kk = cl((k - i / (n * 1.3)) * 3)
        if kk <= 0: continue
        gap = (w - 40) / per
        jx = x - w / 2 + 20 + gap * (q + 0.5); jy = y - 6 - r * 150 * s
        c.save(); c.translate(0, -30 * (1 - eo(kk))); jar(c, jx, jy, s, JAMS[i % 6], kk, 0.04 * math.sin(t * 2 + i)); c.restore()


def shopper(c, x, y, s=1.0, col=INKE, a=1.0, cart=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, -120, 26, P(col, a)); shape(c, rr(-30, -90, 60, 100, 26), col, 0, a)
    c.drawLine(-12, 10, -16, 70, S(col, 12, a)); c.drawLine(12, 10, 16, 70, S(col, 12, a))
    if cart: shape(c, rr(30, -40, 70, 50, 6), (240, 236, 226), 3, a)
    c.restore()


def bars(c, t, k1, k2, v1, v2, l1, l2, title, dark, hi=2):
    body(c, title, 150, 520, 30, MUTE, 'SemiBold', a=max(k1, 0.0001) ** 0.1 if k1 > 0 else 0)
    base = 1250; H_ = 640
    c.drawLine(150, base, 930, base, S(CREAM_T if dark else INKE, 4))
    for j, (k, v, l) in enumerate(((k1, v1, l1), (k2, v2, l2))):
        if k <= 0: continue
        x = 230 + j * 380; h = H_ * v / 100 * eo(k)
        col = ACC[0] if j + 1 == hi else ((180, 172, 162) if not dark else (110, 106, 100))
        c.drawRect(skia.Rect.MakeXYWH(x, base - h, 240, h), P(col)); c.drawRect(skia.Rect.MakeXYWH(x, base - h, 240, h), S(INKE, 4))
        f = anton(110); s_ = '%d%%' % int(round(v * eo(k))); c.drawString(s_, x + 120 - f.measureText(s_) / 2, base - h - 24, f, P(CREAM_T if dark else INKE, k))
        g = font(32, 'Bold', False); c.drawString(l, x + 120 - g.measureText(l) / 2, base + 50, g, P(CREAM_T if dark else INKE, k))


# ---------------------------------------------------------------- scenes
def s_hook(c, t):
    pg(c, False, 1, t)
    headline(c, [[('24 JAMS.', False)], [('3%', True), ('BOUGHT.', False)]], 150, 520, 140, 1.0)
    table(c, 540, 1180, 820, 24, t, cl(t / 1.4), 0.62, 3)
    for i in range(3):
        u = ((t * 0.22) + i / 3) % 1
        shopper(c, -80 + 1240 * u, 1420, 0.7, (90, 86, 80), 0.9)


def s_six(c, t):
    t0 = SCENES[1][0]; tj = ph('jumped'); pg(c, True, 2, t)
    headline(c, [[('THEN 6 JAMS.', False)], [('SALES', False), ('JUMPED.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5), dark=True)
    table(c, 540, 1180, 640, 6, t, pr(t, t0 + 0.2, 0.8), 1.0)
    k = pr(t, tj - 0.1, 0.4)
    if k > 0:
        p = skia.Path(); p.moveTo(700, 1000); p.lineTo(780, 900); p.lineTo(830, 940); p.lineTo(920, 820)
        m = skia.PathMeasure(p, False); seg = skia.Path(); m.getSegment(0, m.getLength() * eo(k), seg, True); c.drawPath(seg, S(ACC[0], 14))
        if k > 0.9: c.drawPath(path([(920, 820), (880, 826), (912, 856)]), P(ACC[0]))


def s_real(c, t):
    t0 = SCENES[2][0]; pg(c, False, 3, t)
    headline(c, [[('A REAL', False)], [('EXPERIMENT.', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5))
    body(c, 'IYENGAR & LEPPER (2000), A CALIFORNIA GROCERY STORE', 150, 820, 28, MUTE, 'SemiBold', a=pr(t, t0 + 0.4, 0.4))
    # store front with two tasting tables
    k = pr(t, t0 + 0.3, 0.8)
    table(c, 330, 1180, 380, 12, t, k, 0.5, 2); table(c, 790, 1180, 260, 6, t, k, 0.7, 1)
    body(c, '24', 310, 1290, 44, INKE, 'Bold', a=k); body(c, '6', 782, 1290, 44, INKE, 'Bold', a=k)


def s_stop(c, t):
    t0 = SCENES[3][0]; t6 = ph('sixty'); t4 = ph('forty'); pg(c, True, 4, t)
    bars(c, t, pr(t, t6 - 0.2, 0.6), pr(t, t4 - 0.2, 0.6), 60, 40, '24 JAMS', '6 JAMS', 'WHO STOPPED TO TASTE', True, hi=1)
    headline(c, [[('MORE', True), ('STOPPED.', False)]], 150, 660, 110, pr(t, t0 + 0.05, 0.5), dark=True)


def s_won(c, t):
    t0 = SCENES[4][0]; pg(c, False, 5, t)
    headline(c, [[('SO THE BIG', False)], [('TABLE', False), ('WON?', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5))
    table(c, 540, 1200, 820, 24, t, 1.0, 0.62, 3)
    stamp(c, 780, 840, '?', pr(t, t0 + 0.4, 0.35), 8, 100)


def s_bought(c, t):
    t0 = SCENES[5][0]; t3 = ph('three percent'); t30 = ph('thirty percent'); pg(c, True, 6, t)
    bars(c, t, pr(t, t3 - 0.2, 0.6), pr(t, t30 - 0.2, 0.6), 3, 30, '24 JAMS', '6 JAMS', 'OF THOSE WHO STOPPED, WHO BOUGHT', True, hi=2)
    if t > t30 - 0.2: headline(c, [[('FEWER', False), ('WON.', True)]], 150, 660, 110, pr(t, t30 - 0.2, 0.4), dark=True)
    else: headline(c, [[('NOPE.', True)]], 150, 660, 110, pr(t, t0 + 0.05, 0.4), dark=True)


def s_name(c, t):
    t0 = SCENES[6][0]; to = ph('choice overload'); pg(c, False, 7, t)
    if t < to - 0.2:
        headline(c, [[('~6X MORE', True)], [('LIKELY TO BUY.', False)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5))
        body(c, 'with fewer choices', 150, 820, 44, INKE, 'SemiBold', a=pr(t, t0 + 0.6, 0.4))
        table(c, 540, 1200, 560, 6, t, 1.0, 0.95)
    else:
        body(c, "IT'S CALLED", 150, 520, 32, MUTE, 'SemiBold', a=pr(t, to - 0.2, 0.4))
        headline(c, [[('CHOICE', False)], [('OVERLOAD.', True)]], 150, 680, 150, pr(t, to - 0.2, 0.4))
        for i in range(12):
            a_ = i / 12 * 2 * math.pi + t * 0.6; r = 260 + 30 * math.sin(t * 2 + i)
            jar(c, 540 + r * math.cos(a_), 1180 + 0.45 * r * math.sin(a_), 0.55, JAMS[i % 6], 0.9)
        shopper(c, 540, 1300, 0.9, INKE)
        f = anton(60); c.drawString('?', 590, 1110, f, P(ACC[0]))


def s_always(c, t):
    t0 = SCENES[7][0]; tn = ph('no later'); ts = ph('stuck'); pg(c, True, 8, t)
    if t < tn - 0.2:
        headline(c, [[('DOES IT', False)], [('ALWAYS', True), ('WORK?', False)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    else:
        headline(c, [[('NOT', False), ('ALWAYS.', True)]], 150, 520, 132, pr(t, tn - 0.2, 0.4), dark=True)
        body(c, 'Later studies: it depends on', 150, 760, 42, CREAM_T, 'SemiBold', a=pr(t, tn + 0.3, 0.4))
        body(c, 'how hard the choice feels.', 150, 815, 42, CREAM_T, 'SemiBold', a=pr(t, tn + 0.3, 0.4))
        body(c, 'SCHEIBEHENNE ET AL. (2010)', 150, 870, 26, MUTE, 'SemiBold', a=pr(t, tn + 0.5, 0.4))
        k = pr(t, ts - 0.3, 0.4)
        if k > 0:
            shopper(c, 400, 1300, 1.0, CREAM_T, k); f = anton(110)
            for i in range(3): c.drawString('?', 470 + i * 70, 1120 - i * 30 + 6 * math.sin(t * 4 + i), f, P(ACC[0], k))
            stamp(c, 760, 1220, 'YOUR CLUE', k, 6, 56)


def s_end(c, t):
    t0 = SCENES[8][0]; ta = ph('take one')
    if t < ta - 0.3:
        pg(c, False, 9, t)
        headline(c, [[("DON'T ADD", False)], [('ANOTHER', False), ('FLAVOR.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5))
        table(c, 540, 1200, 640, 6, t, 1.0, 1.0)
    else:
        final_fill(c, LABEL, num(9), t / DUR, ('TAKE ONE', 'AWAY.'), pr(t, ta - 0.3, 0.5), 170)
        k = pr(t, ta, 0.8)
        shape(c, skia.Rect.MakeXYWH(220, 1200, 640, 26), WOOD)
        for i in range(6):
            jx = 270 + i * 108
            if i == 5: jar(c, jx + 200 * eo(k), 1194 - 120 * math.sin(eo(k) * math.pi), 0.9, JAMS[i], 1 - 0.8 * k, 0.6 * k)
            else: jar(c, jx, 1194, 0.9, JAMS[i])


SCENES = [(0.0, s_hook), (ph('then they cut') - 0.15, s_six), (ph('it was a real') - 0.15, s_real), (ph('the big table pulled') - 0.15, s_stop),
          (ph('so the big') - 0.15, s_won), (ph('nope') - 0.15, s_bought), (ph('shoppers were') - 0.15, s_name),
          (ph('does it always') - 0.15, s_always), (ph('so if people') - 0.15, s_end)]
DARK_S = {1, 3, 5, 7}
FILL_T = ph('take one') - 0.3
SHAKES = [(ph('nobody'), 10, 0.35), (ph('jumped'), 8, 0.3), (ph('thirty percent'), 12, 0.4), (ph('take one'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='MIND TRICKS', num='N° 04')
    headline(c, [[('24 JAMS.', False)], [('3%', True), ('BOUGHT.', False)]], 150, 540, 160, 1.0, maxw=860)
    table(c, 540, 1220, 820, 24, 0.5, 1.0, 0.62, 3)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
