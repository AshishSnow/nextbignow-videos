"""BUSINESS IDEA (green) N° 02: mobile notary — the fee is capped, the drive isn't. ESSAY look; generic props."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (34, 140, 92)
NS = 8; LABEL = 'BUSINESS IDEA — N° 02'
WOOD = (150, 104, 70); ROAD = (70, 66, 62); CARC = (214, 160, 60)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def rstamp(c, x, y, s=1.0, press=0.0, a=1.0):
    """rubber stamp; press 0..1 moves it down"""
    c.save(); c.translate(x, y + 60 * math.sin(math.pi * press)); c.scale(s, s)
    shape(c, rr(-40, -260, 80, 120, 30), WOOD, 4, a); hatch(c, skia.Path.RRect(rr(-40, -260, 80, 120, 30)), 0.2 * a, 8)
    shape(c, skia.Rect.MakeXYWH(-24, -150, 48, 80), (120, 84, 60), 4, a)
    shape(c, rr(-120, -80, 240, 60, 10), (90, 90, 86), 4, a); shape(c, skia.Rect.MakeXYWH(-110, -22, 220, 22), ACC[0], 3, a)
    c.restore()


def doc(c, x, y, s=1.0, rot=0.0, sealed=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    shape(c, skia.Rect.MakeXYWH(-200, -260, 400, 520), (248, 244, 234))
    for i in range(8): c.drawLine(-160, -200 + i * 44, 160 - (i % 3) * 50, -200 + i * 44, S(INKE, 2, 0.3))
    p = skia.Path(); p.moveTo(-150, 190); p.cubicTo(-110, 150, -80, 220, -40, 180); p.cubicTo(-10, 150, 20, 210, 60, 186); c.drawPath(p, S(INKE, 3))
    if sealed > 0:
        c.save(); c.translate(110, 170); c.rotate(-14); c.scale(eback(sealed), eback(sealed))
        c.drawCircle(0, 0, 70, S(ACC[0], 8)); c.drawCircle(0, 0, 52, S(ACC[0], 3)); f = font(26, 'Bold', False); c.drawString('NOTARY', -f.measureText('NOTARY') / 2, 10, f, P(ACC[0])); c.restore()
    c.restore()


def car(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y + 3 * math.sin(t * 9)); c.scale(s, s)
    b = skia.Path(); b.moveTo(-200, 20); b.lineTo(-190, -40); b.lineTo(-100, -50); b.lineTo(-50, -110); b.lineTo(80, -110); b.lineTo(140, -50); b.lineTo(200, -36); b.lineTo(210, 20); b.close()
    shape(c, b, CARC); hatch(c, b, 0.15, 10)
    shape(c, path([(-40, -100), (10, -100), (10, -54), (-80, -54)]), (200, 225, 240), 3); shape(c, path([(24, -100), (74, -100), (116, -54), (24, -54)]), (200, 225, 240), 3)
    for wx in (-120, 130): c.drawCircle(wx, 24, 40, P(INKE)); c.drawCircle(wx, 24, 18, P((180, 180, 176)))
    c.restore()


def road(c, y, t, speed=220):
    c.drawRect(skia.Rect.MakeXYWH(0, y - 70, W, 140), P(ROAD)); c.drawRect(skia.Rect.MakeXYWH(0, y - 70, W, 140), S(INKE, 4))
    off = (t * speed) % 120
    for i in range(-1, 11): c.drawRect(skia.Rect.MakeXYWH(W - (i * 120 + off), y - 6, 60, 12), P(CREAM_T, 0.8))


def pin(c, x, y, s=1.0, k=1.0, lbl=None, dark=False):
    if k <= 0: return
    c.save(); c.translate(x, y - 30 * (1 - eo(k))); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, 0); p.cubicTo(-60, -60, -60, -130, 0, -130); p.cubicTo(60, -130, 60, -60, 0, 0); p.close()
    shape(c, p, ACC[0]); c.drawCircle(0, -86, 18, P(CREAM_T))
    c.restore()
    if lbl: body(c, lbl, x - font(30, 'Bold', False).measureText(lbl) / 2, y + 44, 30, CREAM_T if dark else INKE, 'Bold', a=k)


# ---------------------------------------------------------------- scenes
def s_hook(c, t):
    pg(c, False, 1, t)
    headline(c, [[('THE STAMP:', False)], [('$10', True), ('MAX.', False)]], 150, 520, 140, 1.0)
    body(c, 'FLORIDA, PER NOTARIZATION (NNA)', 150, 820, 30, MUTE, 'SemiBold')
    doc(c, 520, 1180, 0.72, -4, pr(t, 2.0, 0.3))
    rstamp(c, 640, 1150, 0.9, cl((t - 1.4) / 0.6))


def s_drive(c, t):
    t0 = SCENES[1][0]; td = ph('in the drive'); pg(c, True, 2, t)
    headline(c, [[("THE MONEY'S", False)], [('IN THE', False), ('DRIVE.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5), dark=True)
    road(c, 1150, t); car(c, 540, 1110, 1.0, t)


def s_where(c, t):
    t0 = SCENES[2][0]; pg(c, False, 3, t)
    headline(c, [[('YOU GO TO', False)], [('THE', False), ('SIGNER.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    c.drawLine(150, 1150, 930, 1150, S(INKE, 3, 0.3))
    for i, (w, lbl) in enumerate((('hospital', 'HOSPITAL'), ('office', 'OFFICE'), ('kitchen', 'KITCHEN TABLE'))):
        pin(c, 250 + i * 290, 1100, 1.0, pr(t, ph(w) - 0.15, 0.35), lbl)
    k = pr(t, t0 + 0.3, 3.0); car(c, 150 + 700 * eo(k), 1230, 0.5, t)


def s_rule(c, t):
    t0 = SCENES[3][0]; tt = ph('travel fees'); pg(c, True, 4, t)
    headline(c, [[('FEE: CAPPED.', False)], [('TRAVEL:', False), ('NOT.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5), dark=True)
    body(c, "FLORIDA DOESN'T REGULATE NOTARY TRAVEL FEES (NNA)", 150, 820, 28, MUTE, 'SemiBold', a=pr(t, tt, 0.4))
    rstamp(c, 330, 1250, 0.8)
    c.save(); c.translate(330, 1000); stamp(c, 0, 0, '$10 CAP', pr(t, t0 + 0.6, 0.35), -6, 56); c.restore()
    road(c, 1300, t * pr(t, tt, 0.3)); car(c, 760, 1262, 0.55, t)
    stamp(c, 760, 1060, 'NO CAP', pr(t, tt + 0.1, 0.35), 6, 56)


def s_charge(c, t):
    t0 = SCENES[4][0]; tb = ph('before you go'); pg(c, False, 5, t)
    if t < ph('you set') - 0.2:
        headline(c, [[('SO WHAT DO', False)], [('YOU', False), ('CHARGE?', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    else:
        headline(c, [[('AGREE ON THE', False)], [('TOTAL', True), ('FIRST.', False)]], 150, 520, 124, pr(t, ph('you set') - 0.2, 0.4))
    k = pr(t, ph('you set'), 0.5)
    c.save(); c.translate(540, 1080); c.scale(eo(k) if k > 0 else 0.001, eo(k) if k > 0 else 0.001)
    shape(c, skia.Rect.MakeXYWH(-320, -220, 640, 440), (248, 244, 234))
    f = font(34, 'Bold', False)
    for i, (a_, b_) in enumerate((('NOTARY FEE', 'STATE CAP'), ('TRAVEL FEE', 'YOU SET'))):
        c.drawString(a_, -280, -120 + i * 100, f, P(INKE)); c.drawString(b_, 280 - f.measureText(b_), -120 + i * 100, f, P(ACC[0]))
    c.drawLine(-280, 60, 280, 60, S(INKE, 3)); c.drawString('TOTAL', -280, 140, anton(60), P(INKE)); c.drawString('AGREED', 280 - anton(60).measureText('AGREED'), 140, anton(60), P(ACC[0]))
    c.restore()
    if t > tb - 0.2:
        q = skia.Path(); q.moveTo(700, 1290); q.lineTo(750, 1340); q.lineTo(860, 1220); kk = pr(t, tb - 0.2, 0.4)
        m = skia.PathMeasure(q, False); seg = skia.Path(); m.getSegment(0, m.getLength() * eo(kk), seg, True); c.drawPath(seg, S(ACC[0], 16))


def s_states(c, t):
    t0 = SCENES[5][0]; tn = ph('new york'); pg(c, True, 6, t)
    headline(c, [[('EVERY STATE IS', False)], [('DIFFERENT.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5), dark=True)
    rows = (('CALIFORNIA', '$15', t0 + 0.6), ('FLORIDA', '$10', t0 + 0.8), ('NEW YORK', '$2', tn - 0.1))
    for i, (st, v, ti) in enumerate(rows):
        k = pr(t, ti, 0.35)
        if k <= 0: continue
        y = 860 + i * 150; c.save(); c.translate(-50 * (1 - eo(k)), 0)
        c.drawString(st, 150, y, anton(84), P(CREAM_T, k)); f = anton(110); c.drawString(v, 930 - f.measureText(v), y + 8, f, P(ACC[0] if i == 2 else CREAM_T, k))
        c.drawLine(150, y + 34, 930, y + 34, S(CREAM_T, 2, 0.25 * k)); c.restore()
    body(c, 'MAX FEE PER NOTARIZATION (NNA, 2026)', 150, 1340, 28, MUTE, 'SemiBold', a=pr(t, t0 + 0.8, 0.4))


def s_start(c, t):
    t0 = SCENES[6][0]; pg(c, False, 7, t)
    headline(c, [[('HOW DO YOU', False)], [('START?', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5))
    for i, (w, lbl) in enumerate((('commission', 'STATE COMMISSION'), ('bond', 'BOND + STAMP'), ('rules', "YOUR STATE'S FEE RULES"))):
        k = pr(t, ph(w) - 0.15, 0.35)
        if k <= 0: continue
        y = 860 + i * 140; c.drawCircle(185, y - 28, 30, P(ACC[0], k)); g = anton(40); c.drawString(str(i + 1), 185 - g.measureText(str(i + 1)) / 2, y - 14, g, P(CREAM_T, k))
        c.drawString(lbl, 240, y, anton(64), P(INKE, k))


def s_end(c, t):
    t0 = SCENES[7][0]; ts = ph('showing up')
    if t < ts - 0.3:
        pg(c, False, 8, t)
        headline(c, [[('THE STAMP', False)], [('IS', False), ('CHEAP.', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5))
        rstamp(c, 540, 1200, 1.0, cl((t - t0 - 0.3) / 0.6))
    else:
        final_fill(c, LABEL, num(8), t / DUR, ('SHOWING UP', 'IS THE', 'BUSINESS.'), pr(t, ts - 0.3, 0.5), 140)
        road(c, 1250, t); car(c, 540, 1212, 0.6, t)


SCENES = [(0.0, s_hook), (ph('but the money') - 0.15, s_drive), (ph('a mobile') - 0.15, s_where), (ph('florida caps') - 0.15, s_rule),
          (ph('so what do') - 0.15, s_charge), (ph('every state') - 0.15, s_states), (ph('how do you') - 0.15, s_start), (ph('the stamp is') - 0.15, s_end)]
DARK_S = {1, 3, 5}
FILL_T = ph('showing up') - 0.3
SHAKES = [(ph('ten dollars'), 10, 0.35), (ph('in the drive'), 8, 0.3), (ph('two dollars'), 10, 0.35), (ph('showing up'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='BUSINESS IDEA', num='N° 02')
    headline(c, [[('$10 STAMP.', False)], [('THE', False), ('DRIVE', True), ('PAYS.', False)]], 150, 540, 140, 1.0, maxw=860)
    doc(c, 420, 1160, 0.7, -5, 1.0); rstamp(c, 760, 1180, 0.9)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
