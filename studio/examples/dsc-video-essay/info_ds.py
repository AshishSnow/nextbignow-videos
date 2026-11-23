"""CASE STUDY (red) N° 03: Dollar Shave Club — the cheap launch video. ESSAY look; generic razor, no logos, never the video's title."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (214, 52, 44)
NS = 9; LABEL = 'CASE STUDY — N° 03'
WOOD = (176, 128, 84); BOX = (196, 160, 110); STEEL = (170, 172, 176)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def razor(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    h = rr(-22, -20, 44, 320, 20); shape(c, h, (60, 60, 64)); hatch(c, skia.Path.RRect(h), 0.25, 8)
    shape(c, rr(-110, -90, 220, 80, 16), STEEL); c.drawLine(-96, -60, 96, -60, S(INKE, 3)); c.drawLine(-96, -40, 96, -40, S(INKE, 3))
    c.drawLine(-80, -76, -40, -76, S(WHITE, 5, 0.6)); c.restore()


def crate(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    b = skia.Rect.MakeXYWH(-110, -90, 220, 180); shape(c, b, BOX); hatch(c, skia.Path.Rect(b), 0.18, 10)
    c.drawLine(-110, -20, 110, -20, S(INKE, 3)); c.drawRect(skia.Rect.MakeXYWH(-40, -90, 80, 40), P((236, 226, 206))); c.restore()


def camera(c, x, y, s=1.0, rec=True, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx in (-60, 60): c.drawLine(0, 60, dx * 2, 300, S(INKE, 8))
    c.drawLine(0, 60, 0, 300, S(INKE, 8))
    shape(c, rr(-150, -70, 230, 140, 16), (50, 50, 54)); shape(c, path([(80, -40), (170, -80), (170, 80), (80, 40)]), (70, 70, 74))
    c.drawCircle(-120, -100, 46, S(INKE, 6)); c.drawCircle(10, -100, 46, S(INKE, 6))
    if rec and int(t * 2) % 2 == 0: c.drawCircle(-110, -30, 14, P(ACC[0]))
    c.restore()


def laptop(c, x, y, s=1.0, err=0.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-260, -200, 520, 340, 16), (50, 50, 54)); scr = skia.Rect.MakeXYWH(-236, -176, 472, 292)
    c.drawRect(scr, P((236, 232, 224)) if err < 0.5 else P(ACC[0]))
    if err >= 0.5:
        f = anton(70); s_ = 'SITE DOWN'; c.drawString(s_, -f.measureText(s_) / 2, 0, f, P(CREAM_T))
        g = font(30, 'Bold', False); s2 = 'too much traffic'; c.drawString(s2, -g.measureText(s2) / 2, 50, g, P(CREAM_T))
    else:
        for i in range(4): c.drawRect(skia.Rect.MakeXYWH(-200, -140 + i * 60, 400 - i * 60, 30), P((210, 204, 194)))
    shape(c, path([(-300, 140), (300, 140), (330, 180), (-330, 180)]), (80, 80, 84)); c.restore()


def counter(c, x, y, n, size, col, k):
    s_ = '{:,}'.format(int(n * eo(k))); f = anton(size); c.drawString(s_, x, y, f, P(col, max(0.15, k)))


# ---------------------------------------------------------------- scenes
def s_hook(c, t):
    pg(c, False, 1, t)
    tc = ph('crashed his')
    headline(c, [[('A $4,500', False), ('VIDEO.', True)]], 150, 520, 118, 1.0)
    k = pr(t, tc - 0.2, 0.3)
    laptop(c, 540, 1080, 1.0, 1.0 if k > 0.5 else 0.0, t)
    if k > 0: headline(c, [[('SITE:', False), ('CRASHED.', True)]], 150, 680, 118, k)


def s_billion(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('4 YEARS LATER:', False)], [('~$1B', True), ('DEAL.', False)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5), dark=True)
    body(c, 'REPORTED PRICE (FORTUNE, 2016)', 150, 820, 30, MUTE, 'SemiBold', a=pr(t, t0 + 0.4, 0.4))
    razor(c, 540, 1080, 1.1, 0.2 * math.sin(t * 1.5))


def s_dubin(c, t):
    t0 = SCENES[2][0]; ti = ph('improv'); pg(c, False, 3, t)
    headline(c, [[('MARKETING', False), ('BY DAY.', True)]], 150, 520, 118, pr(t, t0 + 0.05, 0.5))
    k = pr(t, ti - 0.2, 0.4)
    if k > 0: headline(c, [[('IMPROV', True), ('AT NIGHT.', False)]], 150, 680, 118, k)
    c.drawCircle(540, 1120, 160, P((246, 242, 232))); c.drawCircle(540, 1120, 160, S(INKE, 5))
    c.drawArc(skia.Rect.MakeXYWH(440, 1060, 200, 160), 20, 140, False, S(INKE, 8)); c.drawCircle(480, 1070, 14, P(INKE)); c.drawCircle(600, 1070, 14, P(INKE))


def s_ware(c, t):
    t0 = SCENES[3][0]; pg(c, True, 4, t)
    headline(c, [[('A WAREHOUSE', False)], [('OF', False), ('UNSOLD', True), ('BLADES.', False)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5), dark=True)
    for r in range(3):
        for q in range(4 - (r == 2)):
            k = pr(t, t0 + 0.3 + (r * 4 + q) * 0.07, 0.3)
            if k > 0: c.save(); c.translate(0, -40 * (1 - eo(k))); crate(c, 230 + q * 180 + (r % 2) * 90, 1320 - r * 150, 0.78); c.restore()


def s_idea(c, t):
    t0 = SCENES[4][0]; td = ph('a dollar'); pg(c, False, 5, t)
    headline(c, [[('RAZORS', False), ('BY MAIL.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5))
    env = skia.Rect.MakeXYWH(220, 900, 640, 380); shape(c, env, (246, 240, 230)); c.drawPath(path([(220, 900), (540, 1100), (860, 900)]), S(INKE, 4))
    razor(c, 540, 1060, 0.6, -1.2)
    stamp(c, 760, 840, 'FROM $1 / MONTH', pr(t, td - 0.15, 0.35), 8, 60)


def s_shoot(c, t):
    t0 = SCENES[5][0]; pg(c, True, 6, t)
    headline(c, [[('HE WROTE IT.', False)], [('STARRED.', False), ('SHOT IT', True)], [('IN THE WAREHOUSE.', False)]], 150, 520, 100, pr(t, t0 + 0.05, 0.5), dark=True)
    camera(c, 340, 1050, 0.9, True, t)
    for i in range(3): crate(c, 700 + (i % 2) * 120, 1250 - i * 150 + (i == 2) * 150, 0.8)


def s_live(c, t):
    t0 = SCENES[6][0]; tc = ph('the site crashed'); t6 = ph('six hours'); pg(c, False, 7, t)
    if t < tc - 0.2:
        headline(c, [[('SO WHAT', False)], [('HAPPENED?', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5))
        laptop(c, 540, 1100, 0.9, 0.0, t)
    else:
        headline(c, [[('SITE CRASHED.', True)]], 150, 520, 124, pr(t, tc - 0.2, 0.4))
        laptop(c, 540, 1050, 0.8, 1.0, t)
        stamp(c, 540, 1330, 'OUT OF RAZORS IN 6 HOURS', pr(t, t6 - 0.3, 0.35), -3, 52, fill=CREAM)


def s_signups(c, t):
    t0 = SCENES[7][0]; tu = ph('unilever'); pg(c, True, 8, t)
    if t < tu - 0.2:
        body(c, 'SIGN-UPS IN THE FIRST 48 HOURS (PER THE COMPANY)', 150, 520, 28, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
        counter(c, 140, 790, 12000, 250, CREAM_T, pr(t, ph('twelve thousand') - 0.2, 0.8))
        for i in range(12):
            if pr(t, ph('twelve thousand') - 0.2, 0.8) > i / 12: c.drawRect(skia.Rect.MakeXYWH(150 + (i % 6) * 130, 920 + (i // 6) * 140, 100, 100), P(ACC[0] if i % 5 == 0 else (70, 66, 62)))
    else:
        headline(c, [[('2016:', True), ('UNILEVER', False)], [('BUYS IT.', False)]], 150, 520, 132, pr(t, tu - 0.2, 0.4), dark=True)
        body(c, 'for a reported ~$1 billion', 150, 860, 44, CREAM_T, 'SemiBold', a=pr(t, tu + 0.2, 0.4))
        razor(c, 540, 1160, 0.9, 0.3)


def s_end(c, t):
    t0 = SCENES[8][0]; ts = ph('being impossible')
    if t < ts - 0.3:
        pg(c, False, 9, t)
        headline(c, [[('THE VIDEO', False)], [('WAS', False), ('CHEAP.', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5))
        camera(c, 540, 1000, 0.9, True, t)
    else:
        final_fill(c, LABEL, num(9), t / DUR, ('BEING IMPOSSIBLE', 'TO FORGET WAS THE', 'EXPENSIVE PART.'), pr(t, ts - 0.3, 0.5), 112)
        razor(c, 540, 1180, 0.8, 0.2 * math.sin(t * 2))


SCENES = [(0.0, s_hook), (ph('four years') - 0.15, s_billion), (ph('michael') - 0.15, s_dubin), (ph('at a party') - 0.15, s_ware),
          (ph('his idea') - 0.15, s_idea), (ph('he wrote') - 0.15, s_shoot), (ph('so what happened') - 0.15, s_live),
          (ph('the company said') - 0.15, s_signups), (ph('the video was') - 0.15, s_end)]
DARK_S = {1, 3, 5, 7}
FILL_T = ph('being impossible') - 0.3
SHAKES = [(ph('crashed his'), 12, 0.4), (ph('the site crashed'), 10, 0.35), (ph('twelve thousand'), 8, 0.3), (ph('being impossible'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='CASE STUDY', num='N° 03')
    headline(c, [[('$4,500 VIDEO.', False)], [('~$1B', True), ('DEAL.', False)]], 150, 540, 140, 1.0, maxw=860)
    camera(c, 540, 1120, 0.9, True, 0.0)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
