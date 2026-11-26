"""MIND TRICKS (purple) N° 06: in-store music picks your wine. ESSAY look; generic bottles/speaker."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (138, 66, 214)
NS = 6; LABEL = 'MIND TRICKS — N° 06'
FR = (120, 30, 60); DE = (200, 170, 70); GLASS = (40, 70, 50)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def bottle(c, x, y, s=1.0, lbl='FRANCE', col=FR, rot=0.0, a=1.0, glow=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if glow > 0: c.drawCircle(0, -60, 190, P(ACC[0], 0.18 * glow))
    b = skia.Path(); b.moveTo(-22, -300); b.lineTo(22, -300); b.lineTo(22, -200); b.cubicTo(70, -170, 75, -130, 75, -90)
    b.lineTo(75, 150); b.cubicTo(75, 170, 60, 180, 40, 180); b.lineTo(-40, 180); b.cubicTo(-60, 180, -75, 170, -75, 150); b.lineTo(-75, -90); b.cubicTo(-75, -130, -70, -170, -22, -200); b.close()
    shape(c, b, GLASS, 4, a); c.drawLine(-50, -100, -50, 140, S(WHITE, 8, 0.25 * a))
    shape(c, skia.Rect.MakeXYWH(-26, -330, 52, 40), col, 3, a)
    lab = skia.Rect.MakeXYWH(-62, -20, 124, 120); shape(c, lab, (246, 240, 228), 3, a)
    c.drawRect(skia.Rect.MakeXYWH(-62, -20, 124, 26), P(col, a))
    f = font(22, 'Bold', False); c.drawString(lbl, -f.measureText(lbl) / 2, 50, f, P(INKE, a))
    c.restore()


def speaker(c, x, y, s=1.0, t=0.0, beat=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-110, -170, 220, 340, 20), (50, 48, 46))
    for (cy, r) in ((-80, 50), (60, 80)):
        p_ = 1 + 0.06 * beat * math.sin(t * 14)
        c.drawCircle(0, cy, r * p_, P((90, 88, 84))); c.drawCircle(0, cy, r * p_, S(INKE, 4)); c.drawCircle(0, cy, r * 0.35, P((30, 30, 30)))
    c.restore()


def note(c, x, y, s=1.0, a=1.0, col=None):
    col = col or ACC[0]
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-22, -14, 34, 26), P(col, a)); c.drawLine(10, -2, 10, -70, S(col, 6, a)); c.drawLine(10, -70, 36, -56, S(col, 6, a))
    c.restore()


def notes_flow(c, x0, y0, x1, y1, t, col=None, n=5, a=1.0):
    for i in range(n):
        u = (t * 0.5 + i / n) % 1
        x = x0 + (x1 - x0) * u; y = y0 + (y1 - y0) * u - 60 * math.sin(u * math.pi)
        note(c, x, y, 0.9, a * math.sin(u * math.pi), col)


def ratio(c, x, y, a_, b_, k, dark):
    f = anton(200); s_ = '%d : %d' % (a_, b_)
    c.drawString(s_, x, y, f, P(CREAM_T if dark else INKE, k))


def s_hook(c, t):
    t5 = ph('five'); pg(c, False, 1, t)
    headline(c, [[('FRENCH', False), ('MUSIC?', True)]], 150, 520, 120, 1.0)
    speaker(c, 300, 1070, 0.95, t); notes_flow(c, 380, 950, 700, 900, t)
    bottle(c, 760, 1150, 1.05, 'FRANCE', FR, 0.04 * math.sin(t * 3), glow=pr(t, 1.0, 0.5))
    k = pr(t, t5 - 0.2, 0.4)
    if k > 0: stamp(c, 540, 760, 'FRENCH WINE: 5 TO 1', k, -5, 60)


def s_switch(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('THEN:', False), ('GERMAN MUSIC.', True)]], 150, 520, 110, pr(t, t0 + 0.05, 0.5), dark=True)
    speaker(c, 300, 1080, 0.95, t); notes_flow(c, 380, 960, 700, 900, t, DE)
    bottle(c, 760, 1150, 1.05, 'GERMANY', DE, 0.04 * math.sin(t * 3), glow=pr(t, t0 + 0.6, 0.5))


def s_lead(c, t):
    t0 = SCENES[2][0]; pg(c, False, 3, t)
    headline(c, [[('GERMAN WINE', False)], [('TOOK THE', False), ('LEAD.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5))
    k = pr(t, ph('two bottles') - 0.2, 0.5)
    for i in range(2): bottle(c, 300 + i * 150, 1180, 0.6 * eback(cl(k * 2 - i * 0.3)) if k > 0 else 0.001, 'GERMANY', DE)
    bottle(c, 760, 1180, 0.6 * eback(k) if k > 0 else 0.001, 'FRANCE', FR)
    if k > 0: f = anton(100); c.drawString('VS', 540, 1120, f, P(MUTE, k))


def s_notice(c, t):
    t0 = SCENES[3][0]; t6 = ph('only six'); pg(c, True, 4, t)
    if t < t6 - 0.2:
        headline(c, [[('DID SHOPPERS', False)], [('NOTICE?', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
        speaker(c, 540, 1100, 0.9, t)
    else:
        headline(c, [[('6 OUT OF 44', True)], [('SAID YES.', False)]], 150, 520, 132, pr(t, t6 - 0.2, 0.4), dark=True)
        k = pr(t, t6, 1.0)
        for i in range(44):
            kk = cl(k * 44 - i)
            if kk <= 0: continue
            x = 180 + (i % 11) * 72; y = 900 + (i // 11) * 100
            col = ACC[0] if i < 6 else (90, 86, 82)
            c.drawCircle(x, y - 30, 16, P(col, kk)); c.drawRRect(rr(x - 20, y - 12, 40, 50, 14), P(col, kk))
        body(c, 'NORTH, HARGREAVES & McKENDRICK, NATURE (1997)', 150, 1360, 26, MUTE, 'SemiBold', a=k)


def s_noidea(c, t):
    t0 = SCENES[4][0]; pg(c, False, 5, t)
    headline(c, [[('THE MUSIC', False)], [('CHOSE.', True)]], 150, 520, 150, pr(t, t0 + 0.05, 0.5))
    shape(c, rr(330, 1060, 420, 200, 20), (200, 196, 190)); c.drawLine(330, 1120, 750, 1120, S(INKE, 3))
    for i, (lbl, col) in enumerate((('FRANCE', FR), ('FRANCE', FR), ('GERMANY', DE))):
        bottle(c, 420 + i * 120, 1080, 0.45, lbl, col)
    for (wx) in (380, 700): c.drawCircle(wx, 1290, 28, P(INKE))
    notes_flow(c, 200, 900, 900, 880, t, None, 6)


def s_end(c, t):
    t0 = SCENES[5][0]; tp = ph('the store might')
    if t < tp - 0.3:
        pg(c, False, 6, t)
        headline(c, [[('NEXT TIME', False)], [('YOU SHOP,', False), ('LISTEN.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5))
        speaker(c, 540, 1100, 0.9, t)
    else:
        final_fill(c, LABEL, num(6), t / DUR, ('THE STORE MIGHT', 'BE PICKING', 'FOR YOU.'), pr(t, tp - 0.3, 0.5), 124)
        notes_flow(c, 200, 1250, 900, 1200, t, CREAM_T, 6)


SCENES = [(0.0, s_hook), (ph('then they switched') - 0.15, s_switch), (ph('german wine took') - 0.15, s_lead), (ph('so did') - 0.15, s_notice),
          (ph('most had') - 0.15, s_noidea), (ph('so next time') - 0.15, s_end)]
DARK_S = {1, 3}
FILL_T = ph('the store might') - 0.3
SHAKES = [(ph('five'), 10, 0.35), (ph('two bottles'), 8, 0.3), (ph('only six'), 10, 0.35), (ph('the store might'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='MIND TRICKS', num='N° 06')
    headline(c, [[('FRENCH MUSIC.', False)], [('FRENCH', False), ('WINE.', True)]], 150, 540, 140, 1.0, maxw=860)
    speaker(c, 300, 1180, 0.9, 0.0); bottle(c, 760, 1260, 1.0, 'FRANCE', FR, 0.0, glow=1.0)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
