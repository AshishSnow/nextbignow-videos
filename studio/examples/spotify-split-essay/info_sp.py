"""MONEY EXPLAINED (blue) N° 03: where your streaming money goes (Spotify). ESSAY look; generic phone/record, no logos or brand colors."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (36, 98, 214)
NS = 7; LABEL = 'MONEY EXPLAINED — N° 03'
BILL = (196, 222, 190); GOLD = (222, 176, 60)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def record(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(t * 90)
    c.drawCircle(0, 0, 200, P((30, 30, 32))); c.drawCircle(0, 0, 200, S(INKE, 4))
    for r in range(70, 190, 18): c.drawCircle(0, 0, r, S((80, 80, 84), 2))
    c.drawCircle(0, 0, 60, P(ACC[0])); c.drawCircle(0, 0, 10, P(CREAM)); c.drawLine(-30, -30, 0, -50, S(CREAM, 4))
    c.restore()


def bill(c, x, y, s=1.0, rot=0.0, a=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    r = rr(-150, -70, 300, 140, 8); shape(c, r, BILL, 3, a); c.drawRRect(rr(-134, -56, 268, 112, 6), S((60, 110, 70), 2, a))
    c.drawCircle(0, 0, 40, S((60, 110, 70), 3, a)); f = anton(56); c.drawString('$', -f.measureText('$') / 2, 20, f, P((60, 110, 70), a))
    c.restore()


def phone(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-160, -300, 320, 600, 44), (40, 40, 42), 5); c.drawRRect(rr(-140, -270, 280, 540, 30), P((236, 232, 224)))
    c.drawRRect(rr(-110, -230, 220, 220, 14), P(ACC[0], 0.8))
    for i in range(14):
        h = 30 + 50 * abs(math.sin(t * 5 + i * 0.7)); c.drawRect(skia.Rect.MakeXYWH(-100 + i * 15, -40 - h, 9, h), P(CREAM, 0.8))
    c.drawLine(-100, 60, 100, 60, S(INKE, 4, 0.3)); c.drawLine(-100, 60, -100 + 200 * ((t * 0.1) % 1), 60, S(INKE, 6))
    c.drawCircle(0, 160, 50, P(INKE)); c.drawPath(path([(-14, 135), (-14, 185), (24, 160)]), P(CREAM))
    c.restore()


def receiver(c, x, y, lbl, k, t, dark=False):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(eback(k), eback(k))
    shape(c, rr(-130, -70, 260, 140, 16), (248, 244, 234)); f = font(25, 'Bold', False); c.drawString(lbl, -f.measureText(lbl) / 2, 12, f, P(INKE)); c.restore()
    for i in range(2):
        u = ((t * 0.8) + i / 2) % 1; cx = 540 + (x - 540) * u; cy = 900 + (y - 900) * u
        c.drawCircle(cx, cy - 90, 20, P(GOLD, 1 - u)); c.drawCircle(cx, cy - 90, 20, S(INKE, 2, 1 - u))


def s_hook(c, t):
    pg(c, False, 1, t)
    headline(c, [[('PAID OUT', False), ('$10B+.', True)]], 150, 520, 132, 1.0)
    body(c, 'TO THE MUSIC INDUSTRY, 2024', 150, 680, 32, MUTE, 'SemiBold')
    record(c, 540, 1100, 1.0, t)
    for i in range(5):
        u = ((t * 0.45) + i / 5) % 1; a_ = i * 1.25
        bill(c, 540 + math.cos(a_) * 420 * u, 1100 + math.sin(a_) * 300 * u, 0.5, a_ + u, 1 - u)


def s_years(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('18 YEARS', True), ('TO ONE', False)], [('PROFITABLE YEAR.', False)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5), dark=True)
    k = pr(t, t0 + 0.3, 2.0)
    for i in range(18):
        kk = cl(k * 18 - i)
        if kk <= 0: continue
        col = ACC[0] if i == 17 else (90, 86, 82)
        c.drawRect(skia.Rect.MakeXYWH(150 + (i % 6) * 130, 860 + (i // 6) * 130, 100, 100), P(col, kk))
    body(c, 'FIRST FULL YEAR OF PROFIT: 2024', 150, 1300, 32, CREAM_T, 'Bold', a=pr(t, t0 + 2.0, 0.4))


def s_fee(c, t):
    t0 = SCENES[2][0]; tb = ph('right back'); pg(c, False, 3, t)
    headline(c, [[('WHERE DOES', False)], [('YOUR', False), ('FEE GO?', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    phone(c, 330, 1130, 0.75, t)
    k = pr(t, tb - 0.2, 0.8)
    bill(c, 640 + 220 * eo(k), 1000 - 40 * math.sin(eo(k) * math.pi), 0.8, 0.2 + 0.4 * eo(k))
    if k > 0: c.drawLine(560, 1050, 560 + 300 * eo(k), 1050, S(ACC[0], 8))


def s_split(c, t):
    t0 = SCENES[3][0]; tt = ph('two thirds'); pg(c, True, 4, t)
    body(c, "SPOTIFY'S ALEX NORSTRÖM, 2025", 150, 520, 28, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    headline(c, [[('~2/3 OF EVERY', False)], [('DOLLAR', True), ('GOES OUT.', False)]], 150, 660, 112, pr(t, tt - 0.4, 0.5), dark=True)
    k = pr(t, tt - 0.2, 0.8); cx, cy, r = 540, 1080, 170
    c.drawCircle(cx, cy, r, P((70, 66, 62))); c.drawCircle(cx, cy, r, S(CREAM_T, 4))
    p = skia.Path(); p.moveTo(cx, cy); p.arcTo(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), -90, 240 * eo(k), False); p.close(); c.drawPath(p, P(ACC[0]))
    body(c, 'RIGHTS HOLDERS', 160, 1310, 34, CREAM_T, 'Bold', a=k); body(c, 'SPOTIFY', 760, 1310, 34, MUTE, 'Bold', a=k)


def s_who(c, t):
    t0 = SCENES[4][0]; pg(c, False, 5, t)
    headline(c, [[('PAID WHEN YOU', False)], [('PRESS', False), ('PLAY.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5))
    c.drawCircle(540, 900, 60, P(INKE)); c.drawPath(path([(522, 870), (522, 930), (568, 900)]), P(CREAM))
    for i, (lbl, w) in enumerate((('LABELS', 'labels'), ('PUBLISHERS', 'publishers'), ('SONGWRITERS', 'songwriters'))):
        receiver(c, 250 + i * 290, 1200, lbl, pr(t, ph(w) - 0.2, 0.35), t)


def s_how(c, t):
    t0 = SCENES[5][0]; ts = ph('huge scale'); pg(c, True, 6, t)
    if t < ts - 0.2:
        headline(c, [[('SO HOW DOES IT', False)], [('MAKE', False), ('MONEY?', True)]], 150, 520, 116, pr(t, t0 + 0.05, 0.5), dark=True)
        record(c, 540, 1140, 0.8, t)
    else:
        headline(c, [[('HUGE', False), ('SCALE.', True)], [('THEN CUTS.', False)]], 150, 520, 132, pr(t, ts - 0.2, 0.4), dark=True)
        k = pr(t, ph('first full') - 0.3, 0.6)
        p = skia.Path(); p.moveTo(170, 1300); p.lineTo(400, 1260); p.lineTo(560, 1290); p.lineTo(720, 1150); p.lineTo(910, 980)
        m = skia.PathMeasure(p, False); seg = skia.Path(); m.getSegment(0, m.getLength() * eo(pr(t, ts, 1.5)), seg, True); c.drawPath(seg, S(CREAM_T, 8))
        c.drawLine(150, 1200, 930, 1200, S(MUTE, 2)); body(c, 'BREAK-EVEN', 160, 1190, 24, MUTE, 'SemiBold')
        stamp(c, 720, 900, '2024: FIRST FULL-YEAR PROFIT', k, -4, 40, fill=CREAM)


def s_end(c, t):
    t0 = SCENES[6][0]; tr = ph('it rents')
    if t < tr - 0.3:
        pg(c, False, 7, t)
        headline(c, [[("IT DOESN'T", False)], [('OWN THE', False), ('MUSIC.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
        record(c, 540, 1130, 0.9, t)
    else:
        final_fill(c, LABEL, num(7), t / DUR, ('IT RENTS IT,', 'ONE PLAY', 'AT A TIME.'), pr(t, tr - 0.3, 0.5), 140)
        record(c, 540, 1300, 0.55, t)


SCENES = [(0.0, s_hook), (ph('and it took') - 0.15, s_years), (ph('so where does') - 0.15, s_fee), (ph('spotify says') - 0.15, s_split),
          (ph('labels') - 0.15, s_who), (ph('so how does') - 0.15, s_how), (ph("it doesn't own") - 0.15, s_end)]
DARK_S = {1, 3, 5}
FILL_T = ph('it rents') - 0.3
SHAKES = [(ph('ten billion'), 10, 0.35), (ph('eighteen'), 8, 0.3), (ph('two thirds'), 10, 0.35), (ph('it rents'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='MONEY EXPLAINED', num='N° 03')
    headline(c, [[('PAID OUT $10B.', False)], [('18 YEARS TO', False), ('PROFIT.', True)]], 150, 540, 132, 1.0, maxw=860)
    record(c, 540, 1180, 1.0, 0.3)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
