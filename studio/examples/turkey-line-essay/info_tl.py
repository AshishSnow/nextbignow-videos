"""CASE STUDY (red) N° 05: Butterball's Turkey Talk-Line. ESSAY look; generic turkey/phone, no logos or packaging."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (214, 52, 44)
NS = 7; LABEL = 'CASE STUDY — N° 05'
SKIN = (200, 130, 60); SKIN2 = (226, 166, 90); PLATE = (240, 238, 232); ICE = (200, 226, 240)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def turkey(c, x, y, s=1.0, frozen=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-260, 40, 520, 90), P(PLATE)); c.drawOval(skia.Rect.MakeXYWH(-260, 40, 520, 90), S(INKE, 4))
    col = tuple(int(a * (1 - frozen) + b * frozen) for a, b in zip(SKIN, ICE))
    b = skia.Path(); b.addOval(skia.Rect.MakeXYWH(-190, -120, 380, 220)); shape(c, b, col); hatch(c, b, 0.18, 9)
    for sx in (-1, 1):
        lg = skia.Path(); lg.addOval(skia.Rect.MakeXYWH(sx * 150 - 60, -80, 120, 90)); shape(c, lg, col, 4)
        c.drawLine(sx * 200, -60, sx * 250, -110, S(INKE, 14)); c.drawCircle(sx * 255, -115, 14, P(PLATE)); c.drawCircle(sx * 255, -115, 14, S(INKE, 3))
    c.drawArc(skia.Rect.MakeXYWH(-120, -100, 240, 120), 200, 140, False, S(WHITE, 8, 0.4))
    if frozen > 0.3:
        for i in range(6): c.drawLine(-150 + i * 60, -110, -140 + i * 60, -70, S(WHITE, 5, frozen))
    c.restore()


def phone(c, x, y, s=1.0, t=0.0, ring=0.0):
    c.save(); c.translate(x + ring * 6 * math.sin(t * 60), y); c.scale(s, s)
    shape(c, rr(-150, -40, 300, 150, 30), ACC[0])
    c.drawCircle(0, 40, 50, P(CREAM)); c.drawCircle(0, 40, 50, S(INKE, 4))
    for i in range(10): a = i / 10 * 2 * math.pi; c.drawCircle(32 * math.cos(a), 40 + 32 * math.sin(a), 7, S(INKE, 2))
    rec = rr(-170, -110, 340, 70, 34); shape(c, rec, ACC[0])
    c.restore()
    if ring > 0:
        for j in range(3):
            r = 40 + j * 40 + 20 * ((t * 3) % 1)
            c.drawArc(skia.Rect.MakeXYWH(x - 220 - r, y - 120 - r, 2 * r, 2 * r), 200, 60, False, S(INKE, 5, 0.6 * ring))
            c.drawArc(skia.Rect.MakeXYWH(x + 220 - r, y - 120 - r, 2 * r, 2 * r), 280, 60, False, S(INKE, 5, 0.6 * ring))


def bubble(c, x, y, txt, k, left=True, dark=False):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(eback(k), eback(k))
    f = font(34, 'Bold', False); w = f.measureText(txt)
    r = rr(-w / 2 - 30, -40, w + 60, 80, 30); c.drawRRect(r, P(CREAM if left else ACC[0])); c.drawRRect(r, S(INKE, 3))
    c.drawString(txt, -w / 2, 12, f, P(INKE if left else CREAM_T)); c.restore()


def s_hook(c, t):
    th = ph('hundred thousand'); pg(c, False, 1, t)
    headline(c, [[('FREE', False), ('TURKEY HELP?', True)]], 150, 520, 112, 1.0)
    turkey(c, 540, 1180, 1.05)
    phone(c, 540, 860, 0.8, t, 1.0)
    stamp(c, 800, 1340, '100,000+ QUESTIONS', pr(t, th - 0.2, 0.4), -4, 40)


def s_since(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('SINCE', False), ('1981.', True)]], 150, 520, 150, pr(t, t0 + 0.05, 0.5), dark=True)
    phone(c, 540, 1100, 1.0, t, 0.6)


def s_start(c, t):
    t0 = SCENES[2][0]; te = ph('eleven thousand'); pg(c, False, 3, t)
    headline(c, [[('6 HOME', False)], [('ECONOMISTS.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    k = pr(t, t0 + 0.4, 0.8)
    for i in range(6):
        kk = cl(k * 6 - i)
        if kk > 0: phone(c, 230 + (i % 3) * 310, 860 + (i // 3) * 200, 0.5 * eback(kk), t + i, 0.0)
    kk = pr(t, te - 0.2, 0.6)
    if kk > 0: c.drawString('{:,}'.format(int(11000 * eo(kk))), 150, 1300, anton(120), P(ACC[0], kk)); body(c, 'QUESTIONS, FIRST SEASON', 150, 1350, 32, INKE, 'Bold', a=kk)


def s_now(c, t):
    t0 = SCENES[3][0]; pg(c, True, 4, t)
    headline(c, [[('NOW:', False), ('50+ EXPERTS.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5), dark=True)
    for i, (lbl, w) in enumerate((('PHONE', 'phone'), ('TEXT', 'text'), ('CHAT', 'chat'), ('ALEXA', 'alexa'))):
        bubble(c, 330 + (i % 2) * 420, 900 + (i // 2) * 170, lbl, pr(t, ph(w) - 0.2, 0.35), i % 2 == 0)


def s_why(c, t):
    t0 = SCENES[4][0]; pg(c, False, 5, t)
    headline(c, [[('WHY GIVE IT', False)], [('AWAY', False), ('FREE?', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    turkey(c, 540, 1160, 0.9)


def s_frozen(c, t):
    t0 = SCENES[5][0]; tn = ph('whose name'); pg(c, True, 6, t)
    headline(c, [[('STILL FROZEN', False)], [('AT', False), ('NOON.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    turkey(c, 540, 1180, 0.9, 0.9)
    c.drawCircle(860, 880, 80, P(CREAM)); c.drawCircle(860, 880, 80, S(INKE, 4)); c.drawLine(860, 880, 860, 815, S(INKE, 8)); c.drawLine(860, 880, 860 + 30 * math.sin(t), 880 - 50 * math.cos(t), S(INKE, 5))
    k = pr(t, tn - 0.2, 0.4)
    if k > 0: phone(c, 240, 900, 0.55, t, 1.0)


def s_end(c, t):
    t0 = SCENES[6][0]; ts = ph('send this')
    if t < ts - 0.3:
        pg(c, False, 7, t)
        headline(c, [[("IT DOESN'T JUST", False)], [('SELL TURKEYS.', False)], [('IT SELLS', False), ('CALM.', True)]], 150, 520, 110, pr(t, t0 + 0.05, 0.5))
        turkey(c, 540, 1200, 0.85)
    else:
        final_fill(c, LABEL, num(7), t / DUR, ('SEND THIS TO', "WHOEVER'S COOKING", 'TODAY.'), pr(t, ts - 0.3, 0.5), 118)
        phone(c, 540, 1270, 0.6, t, 1.0)


SCENES = [(0.0, s_hook), (ph("it's been") - 0.15, s_since), (ph("butterball's") - 0.15, s_start), (ph('more than fifty') - 0.5, s_now),
          (ph('so why') - 0.15, s_why), (ph('think about') - 0.15, s_frozen), (ph("butterball doesn't") - 0.15, s_end)]
DARK_S = {1, 3, 5}
FILL_T = ph('send this') - 0.3
SHAKES = [(ph('free'), 10, 0.35), (ph('eleven thousand'), 8, 0.3), (ph('frozen'), 10, 0.35), (ph('send this'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='CASE STUDY', num='N° 05')
    headline(c, [[('FREE TURKEY', False)], [('HELP. SINCE', False), ('1981.', True)]], 150, 540, 132, 1.0, maxw=860)
    turkey(c, 540, 1250, 1.0); phone(c, 540, 960, 0.7, 0.0, 0.0)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
