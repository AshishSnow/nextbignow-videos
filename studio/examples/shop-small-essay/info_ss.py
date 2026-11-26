"""BUSINESS IDEA (green) N° 04: Small Business Saturday was invented by a card company. ESSAY look; generic card/store, no logos."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (34, 140, 92)
NS = 7; LABEL = 'BUSINESS IDEA — N° 04'
CARDC = (60, 110, 170); GOLD = (222, 176, 60); WOOD = (176, 128, 84)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def card(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    b = rr(-180, -115, 360, 220, 22); shape(c, b, CARDC, 5)
    c.save(); c.clipRRect(b, doAntiAlias=True)
    for i in range(-400, 400, 14): c.drawLine(i, 120, i + 160, -120, S(WHITE, 1.4, 0.16))
    c.restore(); shape(c, rr(-140, -50, 64, 48, 8), GOLD, 3)
    for i in range(4): c.drawRect(skia.Rect.MakeXYWH(-140 + i * 72, 30, 56, 14), P(CREAM_T, 0.85))
    c.restore()


def calendar(c, x, y, s=1.0, k=1.0, stamp_k=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-200, -220, 400, 440, 16), (248, 244, 234))
    c.drawRect(skia.Rect.MakeXYWH(-200, -220, 400, 90), P(ACC[0])); c.drawRect(skia.Rect.MakeXYWH(-200, -220, 400, 90), S(INKE, 4))
    f = font(40, 'Bold', False); c.drawString('NOVEMBER', -f.measureText('NOVEMBER') / 2, -160, f, P(CREAM_T))
    g = anton(200); c.drawString('28', -g.measureText('28') / 2, 80, g, P(INKE))
    h = font(40, 'Bold', False); c.drawString('SATURDAY', -h.measureText('SATURDAY') / 2, 170, h, P(INKE))
    if stamp_k > 0:
        c.save(); c.rotate(-14); c.scale(eback(stamp_k), eback(stamp_k)); c.drawCircle(0, 0, 170, S(ACC[0], 10)); c.restore()
    c.restore()


def store(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    w = skia.Rect.MakeXYWH(-260, -220, 520, 300); shape(c, w, (236, 226, 206)); hatch(c, skia.Path.Rect(w), 0.1, 12)
    shape(c, skia.Rect.MakeXYWH(-280, -280, 560, 70), ACC[0])
    for i in range(8): c.drawArc(skia.Rect.MakeXYWH(-280 + i * 70, -230, 70, 70), 0, 180, False, S(INKE, 3))
    shape(c, skia.Rect.MakeXYWH(-200, -120, 180, 140), (255, 220, 130), 3); shape(c, skia.Rect.MakeXYWH(60, -150, 120, 230), (120, 84, 60))
    f = anton(54); c.drawString('OPEN', -f.measureText('OPEN') / 2, -232, f, P(CREAM_T)); c.restore()


def popup(c, x, y, s=1.0, k=1.0):
    c.save(); c.translate(x, y); c.scale(s * max(0.001, eback(k)), s * max(0.001, eback(k)))
    shape(c, skia.Rect.MakeXYWH(-200, -10, 400, 30), WOOD)
    for lx in (-180, 160): shape(c, skia.Rect.MakeXYWH(lx, 20, 20, 140), WOOD)
    shape(c, rr(-60, -110, 120, 100, 14), (214, 120, 50))
    sign = skia.Rect.MakeXYWH(80, -150, 130, 90); shape(c, sign, CREAM); f = font(26, 'Bold', False); c.drawString('$12', 110, -95, f, P(INKE))
    shape(c, rr(-170, -60, 70, 50, 8), (50, 50, 54), 3)
    c.restore()


def s_hook(c, t):
    pg(c, False, 1, t)
    headline(c, [[('INVENTED BY', False), ('AMEX?', True)]], 150, 520, 120, 1.0)
    k = pr(t, ph('credit card') - 0.3, 0.6)
    calendar(c, 540, 1130, 0.95, 1.0, k)
    card(c, 540 + 300 * (1 - eo(k)), 860 - 120 * (1 - eo(k)), 0.7, -10 + 10 * eo(k))


def s_2010(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('AMERICAN EXPRESS,', False)], [('2010.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5), dark=True)
    card(c, 540, 1100, 1.2, -6 + 3 * math.sin(t * 2))


def s_date(c, t):
    t0 = SCENES[2][0]; pg(c, False, 3, t)
    headline(c, [[('THE SATURDAY AFTER', False)], [('THANKSGIVING.', True)]], 150, 520, 104, pr(t, t0 + 0.05, 0.5))
    calendar(c, 540, 1140, 0.9, 1.0, pr(t, ph('eighth') - 0.3, 0.4))


def s_22b(c, t):
    t0 = SCENES[3][0]; tb = ph('billion'); pg(c, True, 4, t)
    body(c, "AMEX'S OWN SURVEY, 2024 (SELF-REPORTED)", 150, 520, 28, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    k = pr(t, tb - 0.4, 0.8)
    c.drawString('~$%dB' % int(22 * eo(k)), 140, 790, anton(250), P(CREAM_T, max(0.15, k)))
    headline(c, [[('AT SMALL', False), ('BUSINESSES.', True)]], 150, 930, 104, k, dark=True)
    store(c, 540, 1330, 0.6)


def s_idea(c, t):
    t0 = SCENES[4][0]; tt = ph('team up'); pg(c, False, 5, t)
    if t < tt - 0.2:
        headline(c, [[("WHAT'S THE", False)], [('IDEA?', True)]], 150, 520, 150, pr(t, t0 + 0.05, 0.5))
        store(c, 540, 1200, 0.9)
    else:
        headline(c, [[('NO SHOP?', False)], [('TEAM', False), ('UP.', True)]], 150, 520, 140, pr(t, tt - 0.2, 0.4))
        store(c, 400, 1180, 0.75); popup(c, 760, 1220, 0.8, pr(t, ph('table') - 0.8, 0.5))


def s_bring(c, t):
    t0 = SCENES[5][0]; pg(c, True, 6, t)
    headline(c, [[('BRING', False), ('THREE THINGS.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5), dark=True)
    items = (('ONE PRODUCT', 'product'), ('ONE SIGN', 'sign'), ('A WAY TO TAKE CARDS', 'take cards'))
    for i, (s_, w) in enumerate(items):
        k = pr(t, ph(w) - 0.2, 0.35)
        if k <= 0: continue
        y = 860 + i * 150; c.drawCircle(185, y - 30, 32, P(ACC[0], k)); g = anton(42); c.drawString(str(i + 1), 185 - g.measureText(str(i + 1)) / 2, y - 14, g, P(CREAM_T, k))
        c.drawString(s_, 240, y, anton(70), P(CREAM_T, k))


def s_end(c, t):
    t0 = SCENES[6][0]; ts = ph('you just')
    if t < ts - 0.3:
        pg(c, False, 7, t)
        headline(c, [[('A CARD COMPANY', False)], [('INVENTED THE', False), ('DAY.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5))
        card(c, 540, 1120, 1.1, -5)
    else:
        final_fill(c, LABEL, num(7), t / DUR, ('YOU JUST HAVE', 'TO SHOW UP', 'FOR IT.'), pr(t, ts - 0.3, 0.5), 130)
        popup(c, 540, 1190, 0.8, 1.0)


SCENES = [(0.0, s_hook), (ph('american express') - 0.15, s_2010), (ph("now it's") - 0.15, s_date), (ph("amex's") - 0.15, s_22b),
          (ph("so what's") - 0.15, s_idea), (ph('bring one') - 0.15, s_bring), (ph('a credit card company invented') - 0.15, s_end)]
DARK_S = {1, 3, 5}
FILL_T = ph('you just') - 0.3
SHAKES = [(ph('credit card'), 10, 0.35), (ph('eighth'), 8, 0.3), (ph('billion'), 10, 0.35), (ph('you just'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='BUSINESS IDEA', num='N° 04')
    headline(c, [[('SMALL BUSINESS', False)], [('SATURDAY?', False)], [('AMEX', True), ('MADE IT UP.', False)]], 150, 540, 118, 1.0, maxw=860)
    calendar(c, 540, 1260, 0.8, 1.0, 1.0)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
