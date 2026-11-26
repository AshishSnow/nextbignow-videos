"""MONEY EXPLAINED (blue) N° 04: why Macy's pays for the parade. ESSAY look; generic balloons/store, no logos, no character balloons."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (36, 98, 214)
NS = 7; LABEL = 'MONEY EXPLAINED — N° 04'
RED = (214, 52, 44); GOLD = (232, 180, 60); TV = (50, 48, 46)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def star_balloon(c, x, y, s=1.0, t=0.0, col=GOLD):
    c.save(); c.translate(x, y + 12 * math.sin(t * 1.6)); c.rotate(4 * math.sin(t * 1.1)); c.scale(s, s)
    p = skia.Path()
    for i in range(10):
        r = 200 if i % 2 == 0 else 90; a = -math.pi / 2 + i * math.pi / 5
        (p.moveTo if i == 0 else p.lineTo)(r * math.cos(a), r * math.sin(a))
    p.close(); shape(c, p, col, 5); hatch(c, p, 0.15, 10)
    c.drawCircle(-40, -60, 22, P(WHITE, 0.5))
    for dx in (-80, 0, 80): c.drawLine(dx, 120, dx * 1.6, 420, S(INKE, 2, 0.6))
    c.restore()


def store(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    w = skia.Rect.MakeXYWH(-320, -300, 640, 380); shape(c, w, (220, 208, 190)); hatch(c, skia.Path.Rect(w), 0.1, 12)
    for i in range(4): shape(c, skia.Rect.MakeXYWH(-280 + i * 150, -240, 110, 140), (255, 220, 130), 3)
    shape(c, skia.Rect.MakeXYWH(-60, -60, 120, 140), (120, 84, 60))
    shape(c, skia.Rect.MakeXYWH(-340, -360, 680, 60), RED); f = anton(44); s_ = 'DEPARTMENT STORE'; c.drawString(s_, -f.measureText(s_) / 2, -315, f, P(CREAM_T))
    c.restore()


def tv(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-260, -180, 520, 340, 30), TV); scr = rr(-220, -145, 440, 270, 18); c.drawRRect(scr, P((150, 190, 230)))
    c.save(); c.clipRRect(scr, doAntiAlias=True); star_balloon(c, 0, -10, 0.45, t); c.restore()
    c.drawLine(-80, 160, -140, 230, S(INKE, 8)); c.drawLine(80, 160, 140, 230, S(INKE, 8)); c.restore()


def people(c, x, y, n, k, col=INKE, sp=70, s=1.0):
    for i in range(n):
        kk = cl(k * n - i)
        if kk <= 0: continue
        px = x + (i % 8) * sp; py = y + (i // 8) * sp * 1.4
        c.drawCircle(px, py - 30 * s, 14 * s, P(col, kk)); c.drawRRect(rr(px - 16 * s, py - 14 * s, 32 * s, 44 * s, 12 * s), P(col, kk))


def s_hook(c, t):
    pg(c, False, 1, t)
    headline(c, [[('34M', True), ('WATCHED.', False)]], 150, 520, 140, 1.0)
    star_balloon(c, 540, 980, 1.15, t)


def s_asked(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('EMPLOYEES', False)], [('ASKED', True), ('FOR IT.', False)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    people(c, 290, 1080, 16, pr(t, t0 + 0.3, 1.0), CREAM_T, 72, 1.2)


def s_1924(c, t):
    t0 = SCENES[2][0]; pg(c, False, 3, t)
    headline(c, [[('1924.', True), ('THEY MISSED', False)], [('HOME.', False)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5))
    k = pr(t, t0 + 0.4, 1.4)
    p = skia.Path(); p.moveTo(160, 1150); p.cubicTo(400, 900, 680, 900, 920, 1150)
    m = skia.PathMeasure(p, False); seg = skia.Path(); m.getSegment(0, m.getLength() * eo(k), seg, True); c.drawPath(seg, S(ACC[0], 8))
    body(c, 'EUROPE', 140, 1220, 40, INKE, 'Bold', a=k); body(c, 'NEW YORK', 770, 1220, 40, INKE, 'Bold', a=k)


def s_march(c, t):
    t0 = SCENES[3][0]; ts = ph('santa'); pg(c, True, 4, t)
    headline(c, [[('COSTUMES. ZOO', False)], [('ANIMALS.', False), ('SANTA.', True)]], 150, 520, 116, pr(t, t0 + 0.05, 0.5), dark=True)
    off = (t * 120) % 140
    for i in range(8):
        x = -100 + i * 140 + off; c.drawCircle(x, 1060, 34, P(CREAM_T)); c.drawRRect(rr(x - 36, 1100, 72, 110, 24), P((i * 40 % 255, 120, 200)))
    k = pr(t, ts - 0.2, 0.5)
    if k > 0: store(c, 540, 1420, 0.5 * eback(k))


def s_why(c, t):
    t0 = SCENES[4][0]; td = ph('front door'); pg(c, False, 5, t)
    if t < (ph('arrival') - 0.5) - 0.2:
        headline(c, [[('WHY KEEP', False)], [('PAYING?', True)]], 150, 520, 150, pr(t, t0 + 0.05, 0.5))
        star_balloon(c, 540, 1080, 0.8, t)
    else:
        headline(c, [[('SANTA OPENS', False)], [('SHOPPING', True), ('SEASON.', False)]], 150, 520, 118, pr(t, (ph('arrival') - 0.5) - 0.2, 0.4))
        store(c, 540, 1230, 0.75)
        stamp(c, 540, 860, 'RIGHT OUTSIDE THE DOOR', pr(t, td - 0.3, 0.4), -4, 50)


def s_tv(c, t):
    t0 = SCENES[5][0]; pg(c, True, 6, t)
    headline(c, [[('HOURS OF', False)], [('NATIONAL', False), ('TV.', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5), dark=True)
    tv(c, 540, 1100, 0.9, t)


def s_end(c, t):
    t0 = SCENES[6][0]; ta = ph('the name on')
    if t < ta - 0.3:
        pg(c, False, 7, t)
        headline(c, [[('THE BALLOONS', False)], [('ARE THE', False), ('SHOW.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
        star_balloon(c, 540, 1100, 0.9, t)
    else:
        final_fill(c, LABEL, num(7), t / DUR, ('THE NAME ON', 'THE PARADE', 'IS THE AD.'), pr(t, ta - 0.3, 0.5), 140)
        star_balloon(c, 540, 1240, 0.5, t, CREAM)


SCENES = [(0.0, s_hook), (ph('and it only') - 0.15, s_asked), (ph('in nineteen') - 0.15, s_1924), (ph('they marched') - 0.15, s_march),
          (ph('so why') - 0.15, s_why), (ph('today') - 0.15, s_tv), (ph('the balloons') - 0.15, s_end)]
DARK_S = {1, 3, 5}
FILL_T = ph('the name on') - 0.3
SHAKES = [(ph('thirty four'), 10, 0.35), (ph('asked'), 8, 0.3), (ph('front door'), 10, 0.35), (ph('the name on'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='MONEY EXPLAINED', num='N° 04')
    headline(c, [[('THE PARADE', False)], [('IS THE', False), ('AD.', True)]], 150, 540, 150, 1.0, maxw=860)
    star_balloon(c, 540, 1120, 1.0, 0.3); store(c, 540, 1500, 0.45)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
