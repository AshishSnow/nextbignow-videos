"""MIND TRICKS (purple) N° 03: the endowed progress effect (Nunes & Dreze 2006, car wash cards). ESSAY look."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (138, 66, 214)
NS = 7; LABEL = 'MIND TRICKS — N° 03'
CARBODY = (90, 150, 200)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def card(c, x, y, slots, pre, filled, s=1.0, rot=0.0, title='CAR WASH CLUB', a=1.0):
    """slots total, pre = pre-stamped count, filled = extra stamps (float for anim)"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    cols = 5; rows = (slots + cols - 1) // cols
    w = 440; h = 130 + rows * 92
    r = rr(-w / 2, -h / 2, w, h, 20); c.drawRRect(rr(-w / 2 + 10, -h / 2 + 12, w, h, 20), P(INKE, 0.15 * a)); shape(c, r, (248, 244, 234), 4, a)
    f = font(28, 'Bold', False); c.drawString(title, -w / 2 + 28, -h / 2 + 50, f, P(INKE, a))
    c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2 + 68, w, 8), P(ACC[0], a))
    for i in range(slots):
        cx = -w / 2 + 56 + (i % cols) * 82; cy = -h / 2 + 130 + (i // cols) * 92
        c.drawCircle(cx, cy, 32, S(INKE, 3, 0.6 * a))
        kk = 1.0 if i < pre else cl(filled - (i - pre))
        if kk > 0:
            c.save(); c.translate(cx, cy); c.scale(eback(kk), eback(kk)); c.rotate(-12 + i * 9)
            c.drawCircle(0, 0, 30, P(ACC[0] if i >= pre else (230, 160, 40), a)); g = anton(30); c.drawString('✓' if False else '*', -g.measureText('*') / 2, 14, g, P(CREAM_T, a)); c.restore()
            if i < pre:
                pass
    c.restore()


def car(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    b = skia.Path(); b.moveTo(-220, 20); b.lineTo(-200, -40); b.lineTo(-110, -50); b.lineTo(-60, -110); b.lineTo(90, -110); b.lineTo(150, -50); b.lineTo(220, -36); b.lineTo(230, 20); b.close()
    shape(c, b, CARBODY); hatch(c, b, 0.15, 10)
    shape(c, path([(-50, -100), (10, -100), (10, -54), (-90, -54)]), (200, 225, 240), 3); shape(c, path([(24, -100), (84, -100), (126, -54), (24, -54)]), (200, 225, 240), 3)
    for wx in (-130, 140): c.drawCircle(wx, 24, 44, P(INKE)); c.drawCircle(wx, 24, 20, P((180, 180, 176)))
    for i in range(10):
        u = (t * 0.9 + i / 10) % 1; c.drawCircle(-200 + i * 44, -170 + 220 * u, 7, P((120, 180, 230), 0.8 * (1 - u)))
    c.restore()


def bar(c, x, y, w, h, frac, col, lbl, val, k, dark=False):
    c.drawRect(skia.Rect.MakeXYWH(x, y - h * frac * eo(k), w, h * frac * eo(k)), P(col)); c.drawRect(skia.Rect.MakeXYWH(x, y - h * frac * eo(k), w, h * frac * eo(k)), S(INKE, 4))
    f = anton(96); c.drawString(val, x + w / 2 - f.measureText(val) / 2, y - h * frac * eo(k) - 20, f, P(CREAM_T if dark else INKE, k))
    g = font(32, 'Bold', False); c.drawString(lbl, x + w / 2 - g.measureText(lbl) / 2, y + 50, g, P(CREAM_T if dark else INKE, k))


# ---------------------------------------------------------------- scenes
def s_hook(c, t):
    pg(c, False, 1, t)
    headline(c, [[('2 FREE STAMPS.', False)], [('ALMOST', False), ('2X.', True)]], 150, 520, 124, 1.0)
    card(c, 540, 1060, 10, 2, cl((t - 0.6) * 2.5) * 3, 1.15, -4 + 2 * math.sin(t * 2))


def s_nosave(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('SAVED:', False)], [('ZERO', True), ('WASHES.', False)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    car(c, 540, 1150, 1.3, t)


def s_two(c, t):
    t0 = SCENES[2][0]; t1 = ph('card one'); t2 = ph('card two'); pg(c, False, 3, t)
    headline(c, [[('TWO', False), ('CARDS.', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5))
    k1 = pr(t, min(t1 - 0.3, t0 + 0.6), 0.5); k2 = pr(t, t2 - 0.3, 0.5)
    if k1 > 0:
        c.save(); c.translate(0, 60 * (1 - eo(k1))); card(c, 540, 860, 8, 0, 0, 0.95, -2, 'CARD 1: 8 STAMPS', k1); c.restore()
    if k2 > 0:
        c.save(); c.translate(0, 60 * (1 - eo(k2))); card(c, 540, 1190, 10, 2 if t > ph('already') - 0.1 else 0, 0, 0.95, 2, 'CARD 2: 10 STAMPS', k2); c.restore()
        stamp(c, 860, 1060, '2 ALREADY FILLED', pr(t, ph('already') - 0.1, 0.35), 8, 40)


def s_same(c, t):
    t0 = SCENES[3][0]; pg(c, True, 4, t)
    headline(c, [[('SAME 8 WASHES.', False)], [('SO WHAT', False), ('HAPPENED?', True)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5), dark=True)
    for i in range(8):
        k = pr(t, t0 + 0.4 + i * 0.12, 0.3)
        if k > 0: c.save(); c.translate(200 + (i % 4) * 230, 980 + (i // 4) * 220); c.scale(eback(k), eback(k)); car(c, 0, 0, 0.42, t + i); c.restore()


def s_result(c, t):
    t0 = SCENES[4][0]; t1 = ph('nineteen'); t2 = ph('thirty four'); pg(c, False, 5, t)
    body(c, 'SHARE WHO FINISHED THE CARD (NUNES & DREZE, 2006)', 150, 520, 28, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    c.drawLine(150, 1250, 930, 1250, S(INKE, 4))
    bar(c, 230, 1250, 240, 1600, 0.19, (180, 172, 162), 'CARD 1', '19%', pr(t, t1 - 0.2, 0.6))
    bar(c, 610, 1250, 240, 1600, 0.34, ACC[0], 'CARD 2', '34%', pr(t, t2 - 0.2, 0.6))


def s_name(c, t):
    t0 = SCENES[5][0]; th = ph('a head start'); pg(c, True, 6, t)
    body(c, "IT'S CALLED", 150, 520, 32, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    headline(c, [[('THE ENDOWED', False)], [('PROGRESS', True)], [('EFFECT.', False)]], 150, 680, 124, pr(t, t0 + 0.1, 0.6), dark=True)
    k = pr(t, th - 0.2, 1.4)
    c.drawLine(150, 1180, 930, 1180, S(CREAM_T, 4, 0.4)); c.drawLine(150, 1180, 150 + 200 + 580 * eo(k), 1180, S(ACC[0], 10))
    c.drawRect(skia.Rect.MakeXYWH(150, 1180 - 6, 200, 12), P((230, 160, 40)))
    f = font(30, 'Bold', False); c.drawString('HEAD START', 150, 1240, f, P((230, 160, 40), pr(t, th, 0.3))); c.drawString('FINISH', 840, 1240, f, P(CREAM_T, pr(t, th, 0.3)))
    c.drawLine(930, 1130, 930, 1200, S(CREAM_T, 6))


def s_end(c, t):
    t0 = SCENES[6][0]; ts = ph("it's a head") - 0.1
    if t < ts - 0.3:
        pg(c, False, 7, t)
        headline(c, [[("STARTS YOU AT 2?", False)], [("NOT A", False), ('GIFT.', True)]], 150, 520, 116, pr(t, t0 + 0.05, 0.5))
        card(c, 540, 1080, 10, 2, 0, 1.1, 3)
    else:
        final_fill(c, LABEL, num(7), t / DUR, ("IT'S A HEAD START", 'THAT KEEPS YOU', 'COMING BACK.'), pr(t, ts - 0.3, 0.5), 116)
        card(c, 540, 1180, 10, 2, cl((t - ts) * 1.5) * 8, 0.9, -3)


SCENES = [(0.0, s_hook), (ph('and those free') - 0.15, s_nosave), (ph('researchers') - 0.15, s_two), (ph('same eight') - 0.15, s_same),
          (ph('nineteen') - 0.4, s_result), (ph("it's called") - 0.15, s_name), (ph('so when a card') - 0.15, s_end)]
NS = 7
DARK_S = {1, 3, 5}
FILL_T = ph("it's a head") - 0.4
SHAKES = [(ph('doubled'), 10, 0.35), (ph('already'), 6, 0.25), (ph('thirty four'), 12, 0.4), (ph("it's a head") - 0.1, 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='MIND TRICKS', num='N° 03')
    headline(c, [[('2 FREE STAMPS.', False)], [('ALMOST', False), ('2X.', True)]], 150, 540, 130, 1.0, maxw=840)
    card(c, 540, 1150, 10, 2, 0, 1.2, -4)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
