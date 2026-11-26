"""FOUNDER MINDSET (orange) N° 04: Walt Disney's first company went bankrupt. ESSAY look; no likeness, no characters, no logos."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (232, 130, 20)
NS = 7; LABEL = 'FOUNDER MINDSET — N° 04'
LEATHER = (150, 96, 60); BRASS = (214, 170, 80); REEL = (60, 60, 64); TRAIN = (60, 70, 80)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def suitcase(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRRect(rr(-70, -200, 140, 60, 24), S(INKE, 14)); c.drawRRect(rr(-70, -200, 140, 60, 24), S(LEATHER, 8))
    b = rr(-230, -150, 460, 300, 26); shape(c, b, LEATHER, 5); hatch(c, skia.Path.RRect(b), 0.14, 11)
    for sx in (-130, 130): shape(c, skia.Rect.MakeXYWH(sx - 18, -150, 36, 300), (110, 70, 44), 3)
    for sx in (-170, 170): shape(c, rr(sx - 22, -130, 44, 30, 6), BRASS, 3)
    c.restore()


def reel(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(t * 60)
    c.drawCircle(0, 0, 150, P(REEL)); c.drawCircle(0, 0, 150, S(INKE, 5))
    for i in range(6):
        a = i * math.pi / 3; c.drawCircle(90 * math.cos(a), 90 * math.sin(a), 32, P(CREAM))
    c.drawCircle(0, 0, 22, P(CREAM)); c.drawCircle(0, 0, 22, S(INKE, 3)); c.restore()


def train(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-300, -120, 360, 160, 14), TRAIN); shape(c, rr(60, -180, 200, 220, 14), TRAIN)
    shape(c, skia.Rect.MakeXYWH(-260, -140, 40, 40), (40, 40, 44), 3); shape(c, skia.Rect.MakeXYWH(-250, -220, 40, 90), (40, 40, 44), 3)
    for i in range(3): shape(c, skia.Rect.MakeXYWH(-200 + i * 80, -90, 50, 50), (255, 220, 130), 3)
    shape(c, skia.Rect.MakeXYWH(110, -150, 110, 80), (255, 220, 130), 3)
    for wx in (-220, -80, 60, 200):
        c.drawCircle(wx, 60, 44, P((40, 40, 44))); c.drawCircle(wx, 60, 44, S(INKE, 4))
        a = t * 6; c.drawLine(wx, 60, wx + 36 * math.cos(a), 60 + 36 * math.sin(a), S(CREAM, 5))
    for j in range(3):
        u = (t * 0.8 + j / 3) % 1; c.drawCircle(-230 - 60 * u, -240 - 140 * u, 30 + 40 * u, P(MUTE, 0.5 * (1 - u)))
    c.restore()


def sign(c, x, y, txt, s=1.0, crossed=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    f = anton(70); w = f.measureText(txt)
    shape(c, rr(-w / 2 - 40, -70, w + 80, 120, 10), (236, 226, 206), 5)
    c.drawString(txt, -w / 2, 25, f, P(INKE))
    if crossed > 0:
        L = (w + 60) * eo(crossed); c.drawLine(-w / 2 - 30, 30, -w / 2 - 30 + L, 30 - 60 * eo(crossed), S(ACC[0], 14))
    c.restore()


def s_hook(c, t):
    tb = ph('bankrupt'); pg(c, False, 1, t)
    headline(c, [[('DISNEY:', False), ('BANKRUPT.', True)]], 150, 520, 112, 1.0)
    suitcase(c, 540, 1180, 1.0, 2 * math.sin(t * 1.5)); reel(c, 540, 880, 0.75, t)
    k = pr(t, tb - 0.2, 0.4)
    if k > 0: stamp(c, 540, 1180, 'BANKRUPT', k, -8, 90)


def s_21(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('HE WAS', False), ('21.', True)]], 150, 520, 160, pr(t, t0 + 0.05, 0.5), dark=True)
    suitcase(c, 540, 1160, 0.9)


def s_kc(c, t):
    t0 = SCENES[2][0]; tm = ph('money'); pg(c, False, 3, t)
    headline(c, [[('KANSAS CITY,', False)], [('1923.', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5))
    sign(c, 540, 960, 'LAUGH-O-GRAM FILMS', 0.9, pr(t, tm - 0.3, 0.5))
    k = pr(t, tm - 0.2, 0.4)
    if k > 0: stamp(c, 540, 1240, 'OUT OF MONEY', k, -5, 70)


def s_what(c, t):
    t0 = SCENES[3][0]; pg(c, True, 4, t)
    headline(c, [[('SO WHAT', False)], [('DID HE', False), ('DO?', True)]], 150, 520, 150, pr(t, t0 + 0.05, 0.5), dark=True)
    suitcase(c, 540, 1200, 0.8)


def s_train(c, t):
    t0 = SCENES[4][0]; tr = ph('reel'); pg(c, False, 5, t)
    headline(c, [[('TRAIN TO', False)], [('LOS', False), ('ANGELES.', True)]], 150, 520, 136, pr(t, t0 + 0.05, 0.5))
    k = pr(t, t0 + 0.2, 1.6)
    train(c, 1300 - 760 * eo(k), 930, 0.9, t)
    kk = pr(t, tr - 0.3, 0.5)
    if kk > 0:
        suitcase(c, 360, 1200, 0.45 * eback(kk)); reel(c, 720, 1195, 0.55 * eback(kk), t)
        body(c, 'ONE SUITCASE + ONE REEL OF FILM', 150, 1340, 34, INKE, 'Bold', a=kk)


def s_same(c, t):
    t0 = SCENES[5][0]; tn = ph('you know'); pg(c, True, 6, t)
    headline(c, [[('SAME YEAR:', False)], [('A NEW', False), ('STUDIO.', True)]], 150, 520, 136, pr(t, t0 + 0.05, 0.5), dark=True)
    k = pr(t, ph('brother') - 0.3, 0.5)
    for i, x in enumerate((420, 660)):
        kk = cl(k * 2 - i * 0.4)
        if kk > 0:
            c.drawCircle(x, 980, 46, P(CREAM_T, kk)); c.drawRRect(rr(x - 60, 1035, 120, 170, 40), P(CREAM_T, kk))
    kn = pr(t, tn - 0.2, 0.4)
    if kn > 0: stamp(c, 540, 1340, 'YOU KNOW THE NAME.', kn, -4, 64)


def s_end(c, t):
    t0 = SCENES[6][0]; ts = ph('send this')
    if t < ts - 0.3:
        pg(c, False, 7, t)
        rows = (('ONE BANKRUPT COMPANY.', 'one bankrupt'), ('ONE SUITCASE.', 'one suitcase'), ('ONE MORE TRY.', 'one more'))
        for i, (s_, w) in enumerate(rows):
            k = pr(t, ph(w) - 0.2, 0.35)
            if k > 0: c.drawString(s_, 150, 640 + i * 140, anton(86), P(ACC[0] if i == 2 else INKE, k))
        suitcase(c, 540, 1300, 0.6)
    else:
        final_fill(c, LABEL, num(7), t / DUR, ('SEND THIS TO', 'SOMEONE WHOSE', 'FIRST TRY FAILED.'), pr(t, ts - 0.3, 0.5), 112)
        reel(c, 540, 1280, 0.5, t)


SCENES = [(0.0, s_hook), (ph('he was twenty') - 0.15, s_21), (ph('it was called') - 0.15, s_kc), (ph('so what did') - 0.15, s_what),
          (ph('he got on') - 0.15, s_train), (ph('that same year') - 0.15, s_same), (ph('one bankrupt') - 0.15, s_end)]
DARK_S = {1, 3, 5}
FILL_T = ph('send this') - 0.3
SHAKES = [(ph('bankrupt'), 10, 0.35), (ph('money'), 8, 0.3), (ph('you know'), 8, 0.3), (ph('send this'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='FOUNDER MINDSET', num='N° 04')
    headline(c, [[("DISNEY'S FIRST", False)], [('COMPANY', False), ('FAILED.', True)]], 150, 540, 132, 1.0, maxw=860)
    suitcase(c, 540, 1350, 1.0); reel(c, 540, 1050, 0.7)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
