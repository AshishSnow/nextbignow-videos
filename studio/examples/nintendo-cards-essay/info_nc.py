"""CASE STUDY (red) N° 04: Nintendo started with playing cards. ESSAY look; generic cards/console, no logos or characters."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (214, 52, 44)
NS = 8; LABEL = 'CASE STUDY — N° 04'
CARD = (246, 238, 222); TAXI = (236, 190, 50); STEEL = (170, 172, 176)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def hcard(c, x, y, s=1.0, rot=0.0, motif=0, a=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    r = rr(-70, -110, 140, 220, 10); c.drawRRect(rr(-64, -102, 140, 220, 10), P(INKE, 0.15 * a)); shape(c, r, CARD, 4, a)
    c.drawRRect(rr(-58, -98, 116, 196, 6), S(ACC[0], 3, a))
    if motif == 0:   # moon over grass
        c.drawCircle(0, -20, 40, P(ACC[0], a)); c.drawRect(skia.Rect.MakeXYWH(-58, 40, 116, 58), P(INKE, 0.85 * a))
    elif motif == 1:  # plum branch
        c.drawLine(-50, 80, 40, -60, S(INKE, 6, a))
        for (dx, dy) in ((-20, 30), (10, -10), (30, -40), (-35, 60)): c.drawCircle(dx, dy, 12, P(ACC[0], a))
    else:            # crane-ish sun
        c.drawCircle(20, -40, 34, P(ACC[0], a)); c.drawPath(path([(-50, 60), (0, 10), (50, 60)]), S(INKE, 6, a))
    c.restore()


def fan(c, x, y, s, k, t):
    for i in range(5):
        d = (-32 + i * 16) * eo(k)
        c.save(); c.translate(x, y + 160 * s); c.rotate(d + 1.5 * math.sin(t * 2 + i)); hcard(c, 0, -160 * s, s, 0, i % 3); c.restore()


def taxi(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x + 6 * math.sin(t * 3), y); c.scale(s, s)
    b = skia.Path(); b.moveTo(-200, 20); b.lineTo(-190, -40); b.lineTo(-100, -50); b.lineTo(-60, -110); b.lineTo(80, -110); b.lineTo(130, -50); b.lineTo(200, -36); b.lineTo(210, 20); b.close()
    shape(c, b, TAXI); hatch(c, b, 0.15, 10)
    shape(c, rr(-40, -150, 80, 40, 6), CARD, 3); f = font(22, 'Bold', False); c.drawString('TAXI', -f.measureText('TAXI') / 2, -122, f, P(INKE))
    for i in range(6): c.drawRect(skia.Rect.MakeXYWH(-190 + i * 64, -20, 32, 16), P(INKE if i % 2 else CARD))
    for wx in (-120, 130): c.drawCircle(wx, 24, 40, P(INKE)); c.drawCircle(wx, 24, 18, P((180, 180, 176)))
    c.restore()


def bowl(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(3):
        u = (t * 0.6 + i / 3) % 1; c.drawArc(skia.Rect.MakeXYWH(-30 + i * 30, -200 - 60 * u, 30, 60), 90, 180, False, S(MUTE, 4, 1 - u))
    for i in range(14): c.drawOval(skia.Rect.MakeXYWH(-110 + (i * 37) % 210, -70 + (i % 3) * 14, 26, 14), P(WHITE))
    shape(c, path([(-150, -40), (150, -40), (110, 80), (-110, 80)]), ACC[0])
    c.restore()


def grabber(c, x, y, s=1.0, ext=0.0):
    """scissor-lattice extending arm, ext 0..1"""
    c.save(); c.translate(x, y); c.scale(s, s)
    n = 6; seg = 30 + 50 * ext
    shape(c, rr(-40, -20, 60, 120, 14), (240, 236, 226))
    xx = 20
    for i in range(n):
        c.drawLine(xx, -40, xx + seg, 40, S(ACC[0], 10)); c.drawLine(xx, 40, xx + seg, -40, S(ACC[0], 10))
        c.drawCircle(xx + seg / 2, 0, 6, P(INKE)); xx += seg
    c.drawArc(skia.Rect.MakeXYWH(xx - 10, -50, 60, 100), -70, 140, False, S(INKE, 10))
    c.restore()


def console(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    b = rr(-200, -70, 400, 140, 14); shape(c, b, (236, 230, 220)); c.drawRect(skia.Rect.MakeXYWH(-200, 10, 400, 60), P(ACC[0], 0.85)); c.drawRRect(b, S(INKE, 4))
    shape(c, rr(-120, -110, 240, 50, 6), (60, 58, 56))
    for dx in (-320, 260):
        shape(c, rr(dx, -10, 120, 60, 12), (236, 230, 220), 3); c.drawCircle(dx + 90, 20, 10, P(ACC[0])); c.drawRect(skia.Rect.MakeXYWH(dx + 18, 14, 34, 12), P(INKE)); c.drawRect(skia.Rect.MakeXYWH(dx + 29, 3, 12, 34), P(INKE))
    c.restore()


def s_hook(c, t):
    pg(c, False, 1, t)
    headline(c, [[('NINTENDO, 1889:', False)], [('PLAYING CARDS.', True)]], 150, 520, 120, 1.0)
    fan(c, 540, 1120, 1.3, cl(t / 1.2), t)


def s_hundred(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('FIRST BIG GAME HIT?', False)], [('~100 YEARS', True), ('LATER.', False)]], 150, 520, 104, pr(t, t0 + 0.05, 0.5), dark=True)
    k = pr(t, t0 + 0.3, 1.6)
    c.drawLine(150, 1100, 150 + 780 * eo(k), 1100, S(CREAM_T, 6))
    for v, xx in (('1889', 150), ('1983', 930)):
        c.drawCircle(xx, 1100, 14, P(ACC[0])); f = anton(70); c.drawString(v, xx - f.measureText(v) / 2, 1200, f, P(CREAM_T, k if v == '1983' else 1))
    hcard(c, 220, 960, 0.6, -0.1);
    if k > 0.9: console(c, 790, 980, 0.55)


def s_kyoto(c, t):
    t0 = SCENES[2][0]; pg(c, False, 3, t)
    headline(c, [[('KYOTO.', False), ('HANAFUDA.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5))
    body(c, 'Founded by Fusajiro Yamauchi', 150, 700, 44, INKE, 'SemiBold', a=pr(t, t0 + 0.4, 0.4))
    for i in range(8):
        k = pr(t, t0 + 0.4 + i * 0.1, 0.3)
        if k > 0: hcard(c, 230 + (i % 4) * 207, 980 + (i // 4) * 250, 0.75 * eback(k), -0.06 + 0.04 * (i % 3), i % 3)


def s_how(c, t):
    t0 = SCENES[3][0]; pg(c, True, 4, t)
    headline(c, [[('A CARD COMPANY', False)], [('MAKING', False), ('GAMES?', True)]], 150, 520, 116, pr(t, t0 + 0.05, 0.5), dark=True)
    hcard(c, 330, 1120, 1.0, -0.12); f = anton(140); c.drawString('?', 500, 1170, f, P(ACC[0])); console(c, 790, 1140, 0.5)


def s_tries(c, t):
    t0 = SCENES[4][0]; pg(c, False, 5, t)
    headline(c, [[('FIRST, OTHER', False)], [('THINGS.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    k1 = pr(t, ph('taxi') - 0.2, 0.4); k2 = pr(t, ph('rice') - 0.2, 0.4)
    if k1 > 0: c.save(); c.translate(-80 * (1 - eo(k1)), 0); taxi(c, 330, 1120, 0.85, t); c.restore(); body(c, 'A TAXI COMPANY', 170, 1250, 36, INKE, 'Bold', a=k1)
    if k2 > 0: bowl(c, 780, 1140, 0.8, t); body(c, 'INSTANT RICE', 660, 1250, 36, INKE, 'Bold', a=k2)
    body(c, 'THE 1960s', 150, 800, 30, MUTE, 'SemiBold', a=pr(t, t0 + 0.4, 0.4))


def s_toy(c, t):
    t0 = SCENES[5][0]; tg = ph('grab'); pg(c, True, 6, t)
    headline(c, [[("THEY DIDN'T LAST.", False)], [('THEN:', False), ('A TOY.', True)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5), dark=True)
    ext = 0.55 + 0.45 * math.sin((t - t0) * 2.2) if t > tg - 0.5 else 0.2
    grabber(c, 200, 1120, 1.6, ext)


def s_line(c, t):
    t0 = SCENES[6][0]; tf = ph('famicom'); pg(c, False, 7, t)
    headline(c, [[('CARDS. TOYS.', False)], [('THEN', False), ('CONSOLES.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5))
    c.drawLine(150, 1230, 930, 1230, S(INKE, 5))
    items = (('1889', t0 + 0.2), ('1966', t0 + 0.8), ('1983', tf - 0.2))
    for j, (y_, ti) in enumerate(items):
        k = pr(t, ti, 0.4)
        if k <= 0: continue
        xx = 230 + j * 310; c.drawCircle(xx, 1230, 14, P(ACC[0], k)); f = anton(60); c.drawString(y_, xx - f.measureText(y_) / 2, 1310, f, P(INKE, k))
        if j == 0: hcard(c, xx, 1050, 0.6 * eback(k), -0.08)
        elif j == 1: grabber(c, xx - 110, 1060, 0.45, 0.6)
        else: console(c, xx, 1080, 0.42 * eback(k))


def s_end(c, t):
    t0 = SCENES[7][0]; tt = ph('then one thing')
    if t < tt - 0.3:
        pg(c, False, 8, t)
        headline(c, [[('~100 YEARS', True)], [('OF TRYING', False), ('THINGS.', False)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5))
        fan(c, 540, 1140, 1.1, 1.0, t)
    else:
        final_fill(c, LABEL, num(8), t / DUR, ('THEN ONE THING', 'CHANGED', 'EVERYTHING.'), pr(t, tt - 0.3, 0.5), 124)
        console(c, 540, 1260, 0.6)


SCENES = [(0.0, s_hook), (ph('its first big') - 0.15, s_hundred), (ph('in kyoto') - 0.15, s_kyoto), (ph('so how does') - 0.15, s_how),
          (ph('first it tried') - 0.15, s_tries), (ph("they didn't") - 0.15, s_toy), (ph('the ultra') - 0.15, s_line), (ph('almost a hundred years of') - 0.15, s_end)]
DARK_S = {1, 3, 5}
FILL_T = ph('then one thing') - 0.3
SHAKES = [(ph('cards'), 8, 0.3), (ph('taxi'), 8, 0.3), (ph('famicom'), 12, 0.4), (ph('then one thing'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='CASE STUDY', num='N° 04')
    headline(c, [[('NINTENDO, 1889:', False)], [('PLAYING CARDS.', True)]], 150, 540, 124, 1.0, maxw=860)
    fan(c, 540, 1200, 1.3, 1.0, 0.0)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
