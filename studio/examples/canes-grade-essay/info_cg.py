"""CASE STUDY (red) N° 02: Raising Cane's — the lowest grade in the class. ESSAY look; generic food/buildings, no logos."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (214, 52, 44)
NS = 10; LABEL = 'CASE STUDY — N° 02'
GOLD = (222, 160, 70); STONE = (220, 210, 192); WOOD = (176, 128, 84); STEEL = (150, 150, 146)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def report(c, x, y, s=1.0, grade='?', k=1.0, rot=-4, ring=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Rect.MakeXYWH(-230, -300, 460, 600); shape(c, p, (248, 244, 234))
    f = font(30, 'Bold', False); c.drawString('BUSINESS PLAN', -200, -240, f, P(INKE))
    for i in range(9): c.drawLine(-200, -190 + i * 44, 200 - (i % 3) * 60, -190 + i * 44, S(INKE, 2, 0.3))
    g = anton(220); w = g.measureText(grade); c.drawString(grade, 40 - w / 2, 240, g, P(ACC[0], k))
    if ring > 0:
        r = skia.Path(); r.addOval(skia.Rect.MakeXYWH(-90, 30, 260, 250)); m = skia.PathMeasure(r, False); seg = skia.Path(); m.getSegment(0, m.getLength() * eo(ring), seg, True)
        c.drawPath(seg, S(ACC[0], 10))
    c.restore()


def finger(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(-90, -18); p.cubicTo(-60, -34, 60, -30, 92, -12); p.cubicTo(104, 0, 96, 20, 80, 24); p.cubicTo(30, 34, -60, 30, -92, 16); p.cubicTo(-104, 4, -100, -10, -90, -18); p.close()
    shape(c, p, GOLD, 3); hatch(c, p, 0.3, 7)
    for i in range(6): c.drawCircle(-60 + i * 26, -4 + (i % 2) * 10, 3, P(INKE, 0.35))
    c.restore()


def basket(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i, (dx, r) in enumerate(((-90, -0.5), (-30, -0.25), (30, 0.2), (90, 0.45), (0, 0.0))): finger(c, dx, -60 - (i == 4) * 30, 1.0, r + 0.03 * math.sin(t * 2 + i))
    shape(c, path([(-220, -40), (220, -40), (180, 120), (-180, 120)]), ACC[0])
    for i in range(7): c.drawLine(-200 + i * 66, -40, -170 + i * 58, 120, S(INKE, 3, 0.5))
    c.restore()


def bank(c, x, y, s=1.0, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, path([(-170, -150), (0, -240), (170, -150)]), STONE, 4, a); shape(c, skia.Rect.MakeXYWH(-170, -150, 340, 30), STONE, 4, a)
    for i in range(4): shape(c, skia.Rect.MakeXYWH(-140 + i * 80, -120, 40, 200), (238, 230, 214), 3, a)
    shape(c, skia.Rect.MakeXYWH(-190, 80, 380, 34), STONE, 4, a); c.restore()


def refinery(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i, (dx, h) in enumerate(((-200, 320), (-120, 260))):
        shape(c, skia.Rect.MakeXYWH(dx - 22, -h, 44, h), STEEL)
        for j in range(3):
            u = ((t * 0.5 + j / 3 + i * 0.2) % 1); c.drawCircle(dx + 20 * u, -h - 30 - 120 * u, 26 + 30 * u, P((120, 116, 110), 0.5 * (1 - u)))
    for dx in (20, 170): sh = skia.Rect.MakeXYWH(dx - 70, -200, 140, 200); shape(c, sh, (200, 198, 190)); hatch(c, skia.Path.Rect(sh), 0.25, 9)
    c.drawLine(-250, -80, 250, -80, S(INKE, 6)); c.drawLine(-250, 0, 260, 0, S(INKE, 5)); c.restore()


def fish(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    b = skia.Path(); b.moveTo(-110, 0); b.cubicTo(-60, -50, 60, -50, 100, 0); b.cubicTo(60, 50, -60, 50, -110, 0); b.close()
    shape(c, b, (214, 110, 90), 3); hatch(c, b, 0.25, 8)
    shape(c, path([(96, 0), (150, -40), (140, 0), (150, 40)]), (214, 110, 90), 3); c.drawCircle(-70, -8, 7, P(INKE)); c.restore()


def store(c, x, y, s=1.0, on=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    w = skia.Rect.MakeXYWH(-260, -220, 520, 300); shape(c, w, (236, 226, 206)); hatch(c, skia.Path.Rect(w), 0.1, 12)
    shape(c, skia.Rect.MakeXYWH(-280, -280, 560, 70), ACC[0])
    for i in range(8): c.drawLine(-280 + i * 70, -210, -245 + i * 70, -170, S(INKE, 3)); c.drawArc(skia.Rect.MakeXYWH(-280 + i * 70, -230, 70, 70), 0, 180, False, S(INKE, 3))
    shape(c, skia.Rect.MakeXYWH(-200, -120, 180, 140), (255, 220, 130) if on > 0.5 else (180, 200, 210), 3)
    shape(c, skia.Rect.MakeXYWH(60, -150, 120, 230), (120, 84, 60))
    f = anton(54); c.drawString('CHICKEN', -f.measureText('CHICKEN') / 2, -232, f, P(CREAM_T)); c.restore()


def menu(c, x, y, s=1.0, k=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    m = skia.Rect.MakeXYWH(-230, -280, 460, 560); shape(c, m, (36, 34, 32))
    f = anton(60); c.drawString('MENU', -f.measureText('MENU') / 2, -200, f, P(CREAM_T))
    c.drawLine(-180, -170, 180, -170, S(CREAM_T, 3))
    finger(c, 0, -60, 1.2, -0.1)
    g = font(40, 'Bold', False); s_ = 'CHICKEN FINGER MEAL'; c.drawString(s_, -g.measureText(s_) / 2, 70, g, P(CREAM_T))
    for i in range(3):
        c.drawLine(-160, 140 + i * 40, 160, 140 + i * 40, S(CREAM_T, 3, 0.25 * (1 - k)))
    c.restore()


# ---------------------------------------------------------------- scenes
def s_hook(c, t):
    pg(c, False, 1, t)
    headline(c, [[('LOWEST GRADE', False)], [('IN THE', False), ('CLASS.', True)]], 150, 520, 124, 1.0)
    report(c, 540, 1060, 0.95, '?', 1.0, -4 + 2 * math.sin(t * 2))


def s_sold(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    body(c, '2025 SYSTEM SALES (TECHNOMIC)', 150, 520, 30, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    k = pr(t, ph('five billion') - 0.3, 0.6)
    c.drawString('$5B+', 140, 770, anton(250), P(CREAM_T, max(0.15, k)))
    headline(c, [[('OF', False), ('CHICKEN.', True)]], 150, 900, 120, k, dark=True)
    basket(c, 540, 1240, 0.8, t)


def s_plan(c, t):
    t0 = SCENES[2][0]; pg(c, False, 3, t)
    headline(c, [[('CHICKEN FINGERS.', False)], [('NOTHING', True), ('ELSE.', False)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5))
    basket(c, 540, 1130, 1.1, t)


def s_banks(c, t):
    t0 = SCENES[3][0]; tb = ph('every bank'); pg(c, True, 4, t)
    if t < tb - 0.2:
        headline(c, [[('DID ANYONE', False)], [('BELIEVE', True), ('HIM?', False)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    else:
        headline(c, [[('EVERY BANK:', False)], [('NO.', True)]], 150, 520, 140, pr(t, tb - 0.2, 0.4), dark=True)
    for i in range(3):
        k = pr(t, tb + i * 0.18, 0.3)
        bank(c, 230 + i * 310, 1150, 0.62, 1.0)
        stamp(c, 230 + i * 310, 1080, 'NO', k, -12 + i * 8, 80, fill=CREAM)


def s_work(c, t):
    t0 = SCENES[4][0]; tf = ph('fished'); pg(c, False, 5, t)
    if t < tf - 0.2:
        headline(c, [[('90-HOUR', True)], [('WEEKS.', False)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5))
        body(c, 'California oil refinery', 150, 820, 44, INKE, 'SemiBold', a=pr(t, t0 + 0.4, 0.4))
        refinery(c, 560, 1300, 1.2, t)
    else:
        headline(c, [[('20-HOUR', True)], [('DAYS.', False)]], 150, 520, 140, pr(t, tf - 0.2, 0.4))
        body(c, 'Salmon fishing in Alaska', 150, 820, 44, INKE, 'SemiBold', a=pr(t, tf, 0.4))
        for i in range(4):
            u = (t * 0.4 + i / 4) % 1; fish(c, 160 + 760 * u, 1100 + 80 * math.sin(u * 6 + i), 0.8, 0.2 * math.sin(t * 4 + i))
        for i in range(8): c.drawArc(skia.Rect.MakeXYWH(80 + i * 120, 1250, 120, 40), 180, 180, False, S(INKE, 3, 0.6))


def s_open(c, t):
    t0 = SCENES[5][0]; pg(c, True, 6, t)
    headline(c, [[('1996.', True), ('NEAR LSU.', False)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5), dark=True)
    body(c, 'savings + a small business loan', 150, 640, 40, CREAM_T, 'SemiBold', a=pr(t, t0 + 0.4, 0.4))
    store(c, 540, 1160, 1.0, pr(t, ph('opened') - 0.1, 0.3))


def s_menu(c, t):
    t0 = SCENES[6][0]; pg(c, False, 7, t)
    headline(c, [[('THE WHOLE', False)], [('MENU.', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5))
    menu(c, 540, 1070, 0.95, pr(t, t0 + 0.3, 0.6))
    stamp(c, 820, 800, "THAT'S IT", pr(t, ph("that's it") - 0.1, 0.35), 10, 56)


def s_scale(c, t):
    t0 = SCENES[7][0]; tf = ph('fifteen million'); pg(c, True, 8, t)
    k = pr(t, t0 + 0.1, 0.8)
    c.drawString('%d+' % int(900 * eo(k)), 140, 700, anton(220), P(CREAM_T, max(0.15, k)))
    body(c, 'RESTAURANTS (END OF 2025)', 150, 780, 32, MUTE, 'SemiBold', a=k)
    kk = pr(t, tf - 0.2, 0.6)
    if kk > 0:
        c.drawString('$%dM' % int(round(15 * eo(kk))), 140, 1020, anton(200), P(ACC[0], kk))
        body(c, 'IN SALES A DAY, ON AVERAGE (2025)', 150, 1090, 32, MUTE, 'SemiBold', a=kk)
    for i in range(10):
        if k > i / 10: store(c, 170 + i * 82, 1300, 0.14)


def s_grade(c, t):
    t0 = SCENES[8][0]; tm = ph('minus'); pg(c, False, 9, t)
    headline(c, [[('THAT LOWEST', False)], [('GRADE?', True)]], 150, 520, 130, pr(t, t0 + 0.05, 0.5))
    k = pr(t, tm - 0.4, 0.4)
    report(c, 540, 1060, 0.95, 'B-' if k > 0 else '?', 1.0, -4, pr(t, tm, 0.6))


def s_end(c, t):
    t0 = SCENES[9][0]; ts = ph('sometimes')
    if t < ts - 0.3:
        pg(c, False, 10, t)
        headline(c, [[("A BAD GRADE", False)], [("ISN'T A", False), ('VERDICT.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5))
        report(c, 540, 1080, 0.8, 'B-', 1.0, 3, 1.0)
    else:
        final_fill(c, LABEL, num(10), t / DUR, ('SOMETIMES', "IT'S JUST THE", 'FIRST NO.'), pr(t, ts - 0.3, 0.5), 130)
        basket(c, 540, 1240, 0.7, t)


SCENES = [(0.0, s_hook), (ph('last year that') - 0.15, s_sold), (ph('the plan') - 0.15, s_plan), (ph('so did anyone') - 0.15, s_banks),
          (ph('so todd') - 0.15, s_work), (ph('with his savings') - 0.15, s_open), (ph('he kept') - 0.15, s_menu),
          (ph('over nine') - 0.15, s_scale), (ph('and that lowest') - 0.15, s_grade), (ph('a bad grade') - 0.15, s_end)]
DARK_S = {1, 3, 5, 7}
FILL_T = ph('sometimes') - 0.3
SHAKES = [(ph('five billion'), 10, 0.35), (ph('every bank'), 10, 0.35), (ph('minus'), 12, 0.4), (ph('sometimes'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='CASE STUDY', num='N° 02')
    headline(c, [[('LOWEST GRADE.', False)], [('$5B', True), ('A YEAR.', False)]], 150, 540, 140, 1.0, maxw=840)
    report(c, 540, 1150, 0.9, 'B-', 1.0, -4, 1.0)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
