"""MONEY EXPLAINED (blue) N° 02: why Google pays Apple ~$20B for a default. ESSAY look; generic phone, no logos."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (36, 98, 214)
NS = 9; LABEL = 'MONEY EXPLAINED — N° 02'
WOOD = (150, 104, 70); GOLD = (222, 176, 60)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def phone(c, x, y, s=1.0, rot=0.0, glow=0.0, typing=0.0, t=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRRect(rr(-170, -330, 360, 680, 50), P(INKE, 0.15))
    shape(c, rr(-180, -340, 360, 680, 50), (40, 40, 42), 5)
    scr = rr(-160, -310, 320, 620, 36); c.drawRRect(scr, P((236, 232, 224)))
    shape(c, rr(-50, -300, 100, 24, 12), (40, 40, 42), 0)
    bar = rr(-130, -160, 260, 70, 35)
    if glow > 0: c.drawRRect(rr(-145, -175, 290, 100, 50), P(ACC[0], 0.25 * glow))
    shape(c, bar, (255, 255, 255), 4 if glow > 0 else 3)
    c.drawCircle(-90, -125, 14, S(INKE, 4)); c.drawLine(-80, -115, -70, -105, S(INKE, 4))
    if typing > 0:
        f = font(28, 'SemiBold', False); s_ = 'search...'[:max(1, int(9 * typing))]; c.drawString(s_, -55, -114, f, P(MUTE))
    for i in range(3): c.drawRRect(rr(-130, -40 + i * 110, 260, 80, 12), P((210, 204, 194)))
    c.restore()


def cheque(c, x, y, s=1.0, rot=0.0, amt='~$20 BILLION', k=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    r = skia.Rect.MakeXYWH(-400, -150, 800, 300); shape(c, r, (232, 240, 236), 4, k); hatch(c, skia.Path.Rect(r), 0.08 * k, 14)
    f = font(28, 'Bold', False); c.drawString('PAY TO', -360, -90, f, P(INKE, k)); c.drawString('APPLE', -240, -90, anton(40), P(INKE, k))
    c.drawLine(-250, -80, 120, -80, S(INKE, 2, k))
    g = anton(64); c.drawString(amt, -360, 20, g, P(ACC[0], k))
    c.drawString('FOR', -360, 100, f, P(INKE, k)); c.drawString('THE DEFAULT SEARCH BOX', -290, 100, font(30, 'Bold', False), P(INKE, k))
    p = skia.Path(); p.moveTo(170, 90); p.cubicTo(210, 50, 230, 120, 270, 80); p.cubicTo(300, 50, 320, 110, 360, 84); c.drawPath(p, S(INKE, 3, k))
    c.restore()


def gavel(c, x, y, s=1.0, k=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-150, 120, 300, 50, 10), (120, 84, 60))
    c.save(); c.rotate(-30 + 30 * eo(k))
    shape(c, rr(-20, -40, 260, 34, 10), (150, 104, 70)); shape(c, rr(-110, -100, 110, 150, 18), (120, 84, 60))
    c.restore(); c.restore()


def adcard(c, x, y, s=1.0, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-120, -60, 240, 120, 12), (248, 244, 234), 3, a)
    c.drawRRect(rr(-104, -44, 46, 24, 6), P((240, 190, 40), a)); f = font(18, 'Bold', False); c.drawString('AD', -96, -26, f, P(INKE, a))
    for i in range(2): c.drawLine(-100, 6 + i * 26, 90 - i * 50, 6 + i * 26, S(INKE, 3, 0.4 * a))
    c.restore()


# ---------------------------------------------------------------- scenes
def s_hook(c, t):
    pg(c, False, 1, t)
    tp = ph('for a setting')
    headline(c, [[('~$20B.', True), ('ONE YEAR.', False)]], 150, 520, 124, 1.0)
    k = pr(t, tp - 0.2, 0.4)
    if k > 0: headline(c, [[('FOR A', False), ('SETTING.', True)]], 150, 680, 124, k)
    cheque(c, 540, 1080, 1.0 - 0.15 * k, -5 + 2 * math.sin(t * 2), k=1.0)


def s_box(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('THE', False), ('SEARCH BOX.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5), dark=True)
    phone(c, 540, 1060, 0.95, 0, 0.5 + 0.5 * math.sin(t * 4), cl((t - t0 - 0.3) / 1.0), t)


def s_docs(c, t):
    t0 = SCENES[2][0]; pg(c, False, 3, t)
    headline(c, [[('COURT DOCS,', False)], [('2022:', False), ('$20B.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5))
    body(c, "U.S. v. GOOGLE (UNSEALED, MAY 2024; BLOOMBERG)", 150, 820, 28, MUTE, 'SemiBold', a=pr(t, t0 + 0.4, 0.4))
    for i in range(3):
        k = pr(t, t0 + 0.4 + i * 0.25, 0.4)
        c.save(); c.translate(380 + i * 160, 1150 - 30 * (1 - eo(k))); c.rotate(-8 + i * 7)
        shape(c, skia.Rect.MakeXYWH(-150, -200, 300, 400), (248, 244, 234), 4, k)
        for j in range(7): c.drawLine(-110, -150 + j * 40, 110 - (j % 3) * 40, -150 + j * 40, S(INKE, 2, 0.3 * k))
        if i == 2: c.drawRect(skia.Rect.MakeXYWH(-110, 40, 200, 40), P(ACC[0], 0.35 * k))
        c.restore()


def s_split(c, t):
    t0 = SCENES[3][0]; tp = ph('thirty six'); pg(c, True, 4, t)
    body(c, 'A GOOGLE WITNESS AT TRIAL (2023)', 150, 520, 30, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    k = pr(t, tp - 0.2, 0.6)
    if k <= 0: headline(c, [[('A WITNESS', False)], [('LET IT', False), ('SLIP.', True)]], 150, 680, 124, pr(t, t0 + 0.1, 0.5), dark=True); return
    c.drawString('%d%%' % int(36 * eo(k)), 140, 790, anton(280), P(CREAM_T, k))
    headline(c, [[('OF SAFARI', False)], [('SEARCH AD', False), ('MONEY.', True)]], 150, 920, 100, k, dark=True)
    cx, cy, r = 760, 1260, 120
    c.drawCircle(cx, cy, r, P((60, 58, 56))); c.drawCircle(cx, cy, r, S(CREAM_T, 4))
    pth = skia.Path(); pth.moveTo(cx, cy); pth.arcTo(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), -90, 360 * 0.36 * eo(k), False); pth.close(); c.drawPath(pth, P(ACC[0]))
    body(c, 'GOES TO APPLE', 260, 1280, 40, CREAM_T, 'Bold', a=k)


def s_why(c, t):
    t0 = SCENES[4][0]; pg(c, False, 5, t)
    headline(c, [[('WHY PAY THAT', False)], [('MUCH?', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5))
    phone(c, 540, 1100, 0.8, 0.04 * math.sin(t * 3), 0.0, 1.0, t)
    stamp(c, 800, 820, 'DEFAULT', pr(t, ph('the default') - 0.2, 0.35), 8, 64)


def s_ads(c, t):
    t0 = SCENES[5][0]; pg(c, True, 6, t)
    headline(c, [[('EVERY SEARCH', False)], [('= AN', False), ('AD SLOT.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5), dark=True)
    phone(c, 330, 1120, 0.7, 0, 0.6, 1.0, t)
    for i in range(5):
        u = ((t - t0) * 0.5 + i / 5) % 1
        adcard(c, 560 + 360 * u, 900 + i * 90, 0.9, (1 - u) * pr(t, t0 + 0.4, 0.4))


def s_court(c, t):
    t0 = SCENES[6][0]; tm = ph('monopolist'); pg(c, False, 7, t)
    headline(c, [[('2024: A JUDGE', False)], [('RULES', False), ('MONOPOLIST.', True)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5))
    body(c, 'U.S. DISTRICT COURT, D.C., AUG 2024', 150, 820, 28, MUTE, 'SemiBold', a=pr(t, t0 + 0.4, 0.4))
    gavel(c, 540, 1080, 1.1, pr(t, tm - 0.1, 0.25))


def s_remedy(c, t):
    t0 = SCENES[7][0]; te = ph('exclusive'); pg(c, True, 8, t)
    headline(c, [[('2025: PAYMENTS', False)], [('KEEP', True), ('COMING.', False)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5), dark=True)
    cheque(c, 540, 1050, 0.85, 4, k=pr(t, t0 + 0.4, 0.4))
    stamp(c, 600, 1300, 'NO EXCLUSIVE DEALS', pr(t, te - 0.2, 0.35), -5, 56, fill=CREAM)


def s_end(c, t):
    t0 = SCENES[8][0]; ts = ph('a setting you')
    if t < ts - 0.3:
        pg(c, False, 9, t)
        headline(c, [[('THE MOST', False)], [('VALUABLE THING', False)], [('ON YOUR', False), ('PHONE?', True)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5))
        phone(c, 540, 1160, 0.7, 0, 0.8, 1.0, t)
    else:
        final_fill(c, LABEL, num(9), t / DUR, ('A SETTING', 'YOU NEVER', 'TOUCHED.'), pr(t, ts - 0.3, 0.5), 140)
        phone(c, 540, 1160, 0.6, 0.03 * math.sin(t * 3), 1.0, 1.0, t)


SCENES = [(0.0, s_hook), (ph('the search box') - 0.15, s_box), (ph('court documents') - 0.15, s_docs), (ph('and a google') - 0.15, s_split),
          (ph('why pay') - 0.15, s_why), (ph('because every') - 0.15, s_ads), (ph('in twenty twenty four') - 0.15, s_court),
          (ph('but in twenty') - 0.15, s_remedy), (ph('so the most') - 0.15, s_end)]
DARK_S = {1, 3, 5, 7}
FILL_T = ph('a setting you') - 0.3
SHAKES = [(ph('for a setting'), 10, 0.35), (ph('thirty six'), 10, 0.35), (ph('monopolist'), 12, 0.4), (ph('a setting you'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='MONEY EXPLAINED', num='N° 02')
    headline(c, [[('$20B', True), ('FOR ONE', False)], [('SETTING.', False)]], 150, 540, 150, 1.0, maxw=860)
    phone(c, 540, 1180, 0.75, -4, 1.0, 1.0)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
