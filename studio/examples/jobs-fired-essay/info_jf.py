"""FOUNDER MINDSET (orange) N° 03: Steve Jobs got fired. ESSAY look; no likeness, no logos, no film characters."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (232, 130, 20)
NS = 8; LABEL = 'FOUNDER MINDSET — N° 03'
WOOD = (150, 104, 70); BRASS = (214, 170, 80); BOX = (196, 160, 110)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def door(c, x, y, s=1.0, plate=0.0, t=0.0):
    """office door; plate 0..1 = nameplate falling off"""
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, skia.Rect.MakeXYWH(-180, -420, 360, 520), WOOD); hatch(c, skia.Path.Rect(skia.Rect.MakeXYWH(-180, -420, 360, 520)), 0.2, 10)
    c.drawRect(skia.Rect.MakeXYWH(-140, -380, 280, 180), S(INKE, 3, 0.5)); c.drawRect(skia.Rect.MakeXYWH(-140, -160, 280, 220), S(INKE, 3, 0.5))
    c.drawCircle(130, -60, 16, P(BRASS)); c.drawCircle(130, -60, 16, S(INKE, 3))
    c.save(); c.translate(0, -290 + 340 * plate * plate); c.rotate(25 * plate)
    shape(c, rr(-110, -34, 220, 68, 6), BRASS); f = font(30, 'Bold', False); c.drawString('FOUNDER', -f.measureText('FOUNDER') / 2, 11, f, P(INKE))
    c.restore(); c.restore()


def deskbox(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-30, -170, 16, 90, 4), (200, 196, 190)); c.drawCircle(-22, -180, 26, P((100, 160, 90))); c.drawCircle(-22, -180, 26, S(INKE, 3))
    shape(c, skia.Rect.MakeXYWH(10, -150, 90, 70), (246, 240, 230))
    b = path([(-150, -90), (150, -90), (130, 80), (-130, 80)]); shape(c, b, BOX); hatch(c, b, 0.18, 10)
    c.restore()


def cube(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, path([(-120, -60), (0, -120), (120, -60), (0, 0)]), (70, 70, 74)); shape(c, path([(-120, -60), (0, 0), (0, 140), (-120, 80)]), (30, 30, 32)); shape(c, path([(120, -60), (0, 0), (0, 140), (120, 80)]), (50, 50, 54))
    c.restore()


def clapper(c, x, y, s=1.0, k=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, skia.Rect.MakeXYWH(-130, -40, 260, 150), (40, 40, 42))
    c.save(); c.translate(-130, -40); c.rotate(-25 + 25 * eo(k))
    shape(c, skia.Rect.MakeXYWH(0, -40, 260, 40), (40, 40, 42))
    for i in range(5): c.drawPath(path([(20 + i * 50, -40), (45 + i * 50, -40), (25 + i * 50, 0), (0 + i * 50, 0)]), P(CREAM))
    c.restore(); f = font(26, 'Bold', False); c.drawString('ANIMATION', -110, 40, f, P(CREAM)); c.restore()


def s_hook(c, t):
    pg(c, False, 1, t)
    headline(c, [[('FIRED FROM HIS', False)], [('OWN', False), ('COMPANY.', True)]], 150, 520, 124, 1.0)
    door(c, 400, 1230, 0.9, cl((t - 1.2) / 0.8), t); deskbox(c, 780, 1230, 0.9)


def s_best(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('20 YEARS LATER:', False)], [('"THE BEST THING."', True)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5), dark=True)
    k = pr(t, t0 + 0.4, 0.6)
    c.save(); c.translate(540, 1120); c.scale(eback(k) if k > 0 else 0.001, eback(k) if k > 0 else 0.001)
    c.drawCircle(0, 0, 170, P(ACC[0])); c.drawCircle(0, 0, 170, S(CREAM_T, 6)); f = anton(260); c.drawString('?', -f.measureText('?') / 2, 92, f, P(CREAM_T)); c.restore()


def s_out(c, t):
    t0 = SCENES[2][0]; to = ph('i was out'); pg(c, False, 3, t)
    headline(c, [[('1985. THE BOARD', False)], [('SIDED', False), ('AGAINST HIM.', True)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5))
    deskbox(c, 540, 1300, 1.1)
    stamp(c, 540, 860, '"AND SO AT 30, I WAS OUT."', pr(t, to - 1.0, 0.4), -3, 50)


def s_what(c, t):
    t0 = SCENES[3][0]; pg(c, True, 4, t)
    headline(c, [[('SO WHAT', False)], [('DID HE', False), ('DO?', True)]], 150, 520, 150, pr(t, t0 + 0.05, 0.5), dark=True)
    deskbox(c, 540, 1300, 0.9)


def s_over(c, t):
    t0 = SCENES[4][0]; tp = ph('pixar'); pg(c, False, 5, t)
    headline(c, [[('HE STARTED', False)], [('OVER.', True)]], 150, 520, 150, pr(t, t0 + 0.05, 0.5))
    k1 = pr(t, ph('next') - 0.3, 0.4); k2 = pr(t, tp - 0.3, 0.4)
    if k1 > 0: cube(c, 320, 1120, 0.9 * eback(k1)); body(c, 'NeXT', 270, 1330, 40, INKE, 'Bold', a=k1)
    if k2 > 0: clapper(c, 770, 1120, 1.0 * eback(k2), pr(t, tp, 0.3)); body(c, 'PIXAR', 700, 1330, 40, INKE, 'Bold', a=k2)


def s_back(c, t):
    t0 = SCENES[5][0]; tb = ph('brought him back'); pg(c, True, 6, t)
    headline(c, [[('TOY STORY.', False)], [('THEN', False), ('BACK.', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5), dark=True)
    body(c, 'Apple bought NeXT, and he returned', 150, 800, 40, CREAM_T, 'SemiBold', a=pr(t, ph('then apple') - 0.2, 0.4))
    k = pr(t, ph('then apple') - 0.1, 1.2)
    cube(c, 300, 1150, 0.7); door(c, 800, 1340, 0.55, 0.0)
    p = skia.Path(); p.moveTo(380, 1060); p.cubicTo(480, 900, 640, 900, 740, 1040)
    m = skia.PathMeasure(p, False); seg = skia.Path(); m.getSegment(0, m.getLength() * eo(k), seg, True); c.drawPath(seg, S(ACC[0], 12))


def s_quote(c, t):
    t0 = SCENES[6][0]; pg(c, False, 7, t)
    body(c, 'STANFORD, 2005', 150, 520, 30, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    bigquote(c, ('"Getting fired from', 'Apple was the best', 'thing that could have', 'ever happened to me."'), pr(t, t0 + 0.3, 1.0), 'STEVE JOBS, STANFORD COMMENCEMENT', dark=False, y=780, size=70)


def s_end(c, t):
    t0 = SCENES[7][0]; ts = ph('sometimes')
    if t < ts - 0.3:
        pg(c, False, 8, t)
        headline(c, [[('PUSHED OUT ISN\'T', False)], [('THE', False), ('END.', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5))
        door(c, 540, 1240, 0.8, 1.0)
    else:
        final_fill(c, LABEL, num(8), t / DUR, ("SOMETIMES IT'S", 'CHAPTER TWO.'), pr(t, ts - 0.3, 0.5), 140)
        cube(c, 540, 1260, 0.6)


SCENES = [(0.0, s_hook), (ph('twenty years later') - 0.15, s_best), (ph('in nineteen eighty') - 0.15, s_out), (ph('so what did') - 0.15, s_what),
          (ph('he started over') - 0.15, s_over), (ph('pixar made') - 0.15, s_back), (ph('at stanford') - 0.15, s_quote), (ph('getting pushed') - 0.15, s_end)]
DARK_S = {1, 3, 5}
FILL_T = ph('sometimes') - 0.3
SHAKES = [(ph('fired'), 10, 0.35), (ph('i was out'), 8, 0.3), (ph('brought him back'), 8, 0.3), (ph('sometimes'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='FOUNDER MINDSET', num='N° 03')
    headline(c, [[('FIRED FROM HIS', False)], [('OWN', False), ('COMPANY.', True)]], 150, 540, 132, 1.0, maxw=860)
    door(c, 400, 1400, 0.9, 0.7); deskbox(c, 790, 1400, 0.9)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
