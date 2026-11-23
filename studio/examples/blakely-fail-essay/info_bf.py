"""FOUNDER MINDSET (orange) N° 02: Sara Blakely's dinner-table question. ESSAY look; no likeness, no logos."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (232, 130, 20)
NS = 8; LABEL = 'FOUNDER MINDSET — N° 02'
WOOD = (176, 128, 84); SKIN = (226, 180, 140); PLATE = (246, 244, 238)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def table(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    top = skia.Rect.MakeXYWH(-380, -40, 760, 60); shape(c, top, WOOD); hatch(c, skia.Path.Rect(top), 0.3, 8)
    for lx in (-330, 310): shape(c, skia.Rect.MakeXYWH(lx, 20, 24, 220), WOOD)
    for px in (-220, 0, 220):
        c.drawOval(skia.Rect.MakeXYWH(px - 90, -80, 180, 50), P(PLATE)); c.drawOval(skia.Rect.MakeXYWH(px - 90, -80, 180, 50), S(INKE, 3))
        c.drawOval(skia.Rect.MakeXYWH(px - 50, -70, 100, 28), S(INKE, 2, 0.4))
    shape(c, skia.Rect.MakeXYWH(-30, -170, 60, 110), (240, 236, 226)); c.drawPath(path([(0, -200), (-10, -176), (10, -176)]), P(ACC[0]))
    fl = 6 * math.sin(t * 9); c.drawOval(skia.Rect.MakeXYWH(-9 + fl * 0.2, -205, 18, 30), P((250, 200, 60), 0.9))
    c.restore()


def hand(c, x, y, s=1.0, rot=0.0, flip=1):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * flip, s)
    palm = rr(-60, -60, 120, 130, 30); shape(c, palm, SKIN)
    for i, (dx, h) in enumerate(((-45, 90), (-15, 110), (15, 110), (45, 90))): shape(c, rr(dx - 14, -60 - h, 28, h + 20, 14), SKIN, 3)
    shape(c, rr(-110, -30, 70, 28, 14), SKIN, 3)
    shape(c, skia.Rect.MakeXYWH(-44, 66, 88, 120), (90, 110, 150))
    c.restore()


def fax(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    b = rr(-200, -80, 400, 160, 16); shape(c, b, (210, 206, 196)); hatch(c, skia.Path.RRect(b), 0.15, 10)
    shape(c, rr(-160, -130, 320, 60, 10), (190, 186, 176))
    for i in range(9): c.drawRRect(rr(60 + (i % 3) * 40, -50 + (i // 3) * 36, 30, 24, 5), P((120, 118, 112)))
    shape(c, rr(-160, -40, 180, 80, 8), (150, 190, 160), 3)
    u = (t * 0.3) % 1; shape(c, skia.Rect.MakeXYWH(-120, -130 - 160 * u, 240, 160 * u + 2), (248, 244, 234), 3)
    c.restore()


def door(c, x, y, s=1.0, open_=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, skia.Rect.MakeXYWH(-140, -360, 280, 380), (80, 70, 64))
    c.save(); c.translate(-130, 0); c.scale(1 - 0.6 * open_, 1)
    d = skia.Rect.MakeXYWH(0, -350, 260, 370); shape(c, d, ACC[0]); hatch(c, skia.Path.Rect(d), 0.2, 10)
    c.drawCircle(220, -160, 12, P((222, 176, 60))); c.restore()
    c.restore()


# ---------------------------------------------------------------- scenes
def s_hook(c, t):
    pg(c, False, 1, t)
    tq = ph('what did you fail')
    headline(c, [[('ONE STRANGE', False)], [('QUESTION.', True)]], 150, 520, 132, 1.0)
    table(c, 540, 1180, 1.0, t)
    stamp(c, 540, 900, 'WHAT DID YOU FAIL AT THIS WEEK?', pr(t, tq - 0.2, 0.4), -4, 46)


def s_spanx(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('THAT QUESTION', False)], [('HELPED BUILD', False), ('SPANX.', True)]], 150, 520, 118, pr(t, t0 + 0.05, 0.5), dark=True)
    k = pr(t, t0 + 0.4, 0.6); c.save(); c.translate(540, 1100); c.scale(eback(k) if k > 0 else 0.001, eback(k) if k > 0 else 0.001)
    c.drawCircle(0, 0, 170, P(ACC[0])); c.drawCircle(0, 0, 170, S(CREAM_T, 6)); f = anton(260); c.drawString('?', -f.measureText('?') / 2, 92, f, P(CREAM_T)); c.restore()


def s_five(c, t):
    t0 = SCENES[2][0]; tw = ph('way to go'); pg(c, False, 3, t)
    headline(c, [[('SHE FAILED?', False)], [('HIGH', False), ('FIVE.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    k = pr(t, ph('high five') - 0.5, 0.5)
    hand(c, 540 - 280 * (1 - eo(k)) - 70, 1120, 1.3, 0.3 - 0.3 * eo(k), 1)
    hand(c, 540 + 280 * (1 - eo(k)) + 70, 1120, 1.3, -0.3 + 0.3 * eo(k), -1)
    if k > 0.95:
        for i in range(8):
            a = i / 8 * 2 * math.pi; kk = pr(t, ph('high five'), 0.4)
            c.drawLine(540 + 120 * math.cos(a), 960 + 120 * math.sin(a), 540 + (120 + 60 * kk) * math.cos(a), 960 + (120 + 60 * kk) * math.sin(a), S(ACC[0], 8, 1 - pr(t, ph('high five') + 0.5, 0.4)))
    stamp(c, 800, 820, '"WAY TO GO!"', pr(t, tw - 0.1, 0.35), 8, 56)


def s_why(c, t):
    t0 = SCENES[3][0]; tb = ph('because to him'); pg(c, True, 4, t)
    if t < tb - 0.2:
        headline(c, [[('WHY CHEER', False)], [('FOR', False), ('FAILING?', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    else:
        headline(c, [[('FAILING =', False)], [('YOU', False), ('TRIED.', True)]], 150, 520, 140, pr(t, tb - 0.2, 0.4), dark=True)
        kk = pr(t, ph('not trying') - 0.2, 0.4)
        if kk > 0:
            c.drawString('NOT TRYING =', 150, 1000, anton(96), P(CREAM_T, kk)); c.drawString('THE REAL FAILURE.', 150, 1110, anton(96), P(ACC[0], kk))


def s_fax(c, t):
    t0 = SCENES[4][0]; pg(c, False, 5, t)
    headline(c, [[('YEARS LATER:', False)], [('FAX MACHINES,', True)], [('DOOR TO DOOR.', False)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5))
    door(c, 300, 1340, 0.85, 0.5 + 0.5 * math.sin(t * 1.5))
    fax(c, 720, 1160, 0.75, t)


def s_side(c, t):
    t0 = SCENES[5][0]; pg(c, True, 6, t)
    headline(c, [[('SPANX, BUILT', False)], [('ON THE', False), ('SIDE.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5), dark=True)
    body(c, 'while still working her full-time job', 150, 820, 40, CREAM_T, 'SemiBold', a=pr(t, ph('full time') - 0.2, 0.4))
    # clock + notebook
    c.drawCircle(320, 1120, 150, P((246, 242, 232))); c.drawCircle(320, 1120, 150, S(INKE, 5))
    a1 = t * 2; a2 = t * 0.4
    c.drawLine(320, 1120, 320 + 110 * math.sin(a1), 1120 - 110 * math.cos(a1), S(INKE, 6)); c.drawLine(320, 1120, 320 + 70 * math.sin(a2), 1120 - 70 * math.cos(a2), S(INKE, 9))
    nb = skia.Rect.MakeXYWH(560, 960, 340, 320); shape(c, nb, (248, 244, 234))
    for i in range(6): c.drawLine(590, 1010 + i * 44, 870, 1010 + i * 44, S(ACC[0], 2, 0.6))
    k = pr(t, t0 + 0.6, 2.0); p = skia.Path(); p.moveTo(600, 1100); p.cubicTo(680, 1030, 760, 1180, 860, 1080)
    m = skia.PathMeasure(p, False); seg = skia.Path(); m.getSegment(0, m.getLength() * eo(k), seg, True); c.drawPath(seg, S(INKE, 5))


def s_def(c, t):
    t0 = SCENES[6][0]; pg(c, False, 7, t)
    body(c, 'HOW SHE DEFINES FAILURE', 150, 520, 30, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    headline(c, [[('NOT', False), ('TRYING.', True)]], 150, 700, 150, pr(t, t0 + 0.2, 0.5))
    k = pr(t, ph('the outcome') - 0.2, 0.4)
    f = anton(120); s_ = 'NOT THE OUTCOME.'; c.drawString(s_, 150, 940, f, P(INKE, k * 0.45))
    if k > 0: c.drawLine(150, 900, 150 + f.measureText(s_) * eo(pr(t, ph('the outcome') + 0.2, 0.3)), 900, S(ACC[0], 10))


def s_end(c, t):
    t0 = SCENES[7][0]; ts = ph('if the answer')
    if t < ts - 0.3:
        pg(c, False, 8, t)
        headline(c, [[('WHAT DID YOU', False)], [('FAIL AT', False), ('THIS WEEK?', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5))
        table(c, 540, 1200, 0.9, t)
    else:
        final_fill(c, LABEL, num(8), t / DUR, ('NOTHING?', "THEN YOU", "DIDN'T TRY."), pr(t, ts - 0.3, 0.5), 140)
        table(c, 540, 1230, 0.75, t)


SCENES = [(0.0, s_hook), (ph('and that question') - 0.15, s_spanx), (ph('when sara') - 0.15, s_five), (ph('why cheer') - 0.15, s_why),
          (ph('years later') - 0.15, s_fax), (ph('she built') - 0.15, s_side), (ph('she says') - 0.15, s_def), (ph('so what did') - 0.15, s_end)]
DARK_S = {1, 3, 5}
FILL_T = ph('if the answer') - 0.3
SHAKES = [(ph('high five'), 10, 0.35), (ph('real failure'), 8, 0.3), (ph('if the answer'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='FOUNDER MINDSET', num='N° 02')
    headline(c, [[('WHAT DID YOU', False)], [('FAIL AT', False), ('THIS WEEK?', True)]], 150, 540, 124, 1.0, maxw=860)
    table(c, 540, 1200, 0.95, 0.3)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
