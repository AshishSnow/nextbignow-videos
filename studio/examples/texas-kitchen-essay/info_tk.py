"""BUSINESS IDEA (green) N° 03: Texas cottage food law. ESSAY look; generic kitchen props."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (34, 140, 92)
NS = 7; LABEL = 'BUSINESS IDEA — N° 03'
STEEL = (196, 196, 192); CRUST = (214, 160, 90); PUMP = (214, 120, 50); BREAD = (200, 140, 80)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, dark, i, t): page(c, dark, label=LABEL, num=num(i), prog=t / DUR)


def pie(c, x, y, s=1.0, col=PUMP):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-130, -40, 260, 90), P(CRUST)); c.drawOval(skia.Rect.MakeXYWH(-130, -40, 260, 90), S(INKE, 4))
    c.drawOval(skia.Rect.MakeXYWH(-108, -30, 216, 66), P(col)); c.drawOval(skia.Rect.MakeXYWH(-108, -30, 216, 66), S(INKE, 2))
    for i in range(12): a = i / 12 * 2 * math.pi; c.drawCircle(118 * math.cos(a), 5 + 38 * math.sin(a), 9, P(CRUST))
    c.restore()


def cookie(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 0, 50, P(CRUST)); c.drawCircle(0, 0, 50, S(INKE, 4))
    for (dx, dy) in ((-18, -14), (16, -20), (6, 12), (-22, 18), (24, 14)): c.drawCircle(dx, dy, 7, P((80, 50, 30)))
    c.restore()


def loaf(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    b = rr(-110, -50, 220, 100, 46); shape(c, b, BREAD); hatch(c, skia.Path.RRect(b), 0.2, 9)
    for i in range(3): c.drawLine(-60 + i * 50, -40, -30 + i * 50, 30, S(INKE, 4)); c.restore()


def oven(c, x, y, s=1.0, open_=0.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-240, -300, 480, 560, 20), STEEL)
    for i in range(4): c.drawCircle(-160 + i * 107, -250, 18, P(INKE));
    c.drawRect(skia.Rect.MakeXYWH(-200, -200, 400, 380), P((60, 56, 52)))
    glow = 0.5 + 0.2 * math.sin(t * 3); c.drawRect(skia.Rect.MakeXYWH(-180, -180, 360, 340), P((240, 150, 60), glow * 0.5))
    pie(c, 0, 60, 1.0)
    c.save(); c.translate(0, 180); c.scale(1, 1 - 0.85 * open_)
    d = rr(-210, -380, 420, 380, 10); c.drawRRect(d, P((200, 200, 196), 0.55)); c.drawRRect(d, S(INKE, 5)); c.drawLine(-120, -340, 120, -340, S(INKE, 10))
    c.restore(); c.restore()


def label_card(c, x, y, s=1.0, k=1.0):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(-5); c.scale(eback(k) * s, eback(k) * s)
    r = skia.Rect.MakeXYWH(-230, -90, 460, 180); shape(c, r, (248, 244, 234))
    f = font(24, 'Bold', False)
    for i, ln in enumerate(('MADE IN A PRIVATE RESIDENCE', 'NOT SUBJECT TO GOVERNMENT', 'LICENSING OR INSPECTION')): c.drawString(ln, -200, -40 + i * 36, f, P(INKE))
    c.drawRect(skia.Rect.MakeXYWH(-200, 66, 160, 10), P(ACC[0])); c.restore()


def s_hook(c, t):
    pg(c, False, 1, t)
    headline(c, [[('SELL UP TO $150K', False)], [('FROM YOUR', False), ('KITCHEN.', True)]], 150, 520, 104, 1.0)
    body(c, 'TEXAS LAW: THE YEARLY SALES LIMIT', 150, 800, 30, MUTE, 'SemiBold')
    oven(c, 540, 1130, 0.85, cl((t - 0.6) / 0.8), t)


def s_permit(c, t):
    t0 = SCENES[1][0]; pg(c, True, 2, t)
    headline(c, [[('NO CITY', False), ('PERMIT.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    body(c, 'TEXAS DSHS: LOCAL GOVERNMENTS CAN\'T REQUIRE ONE', 150, 700, 28, MUTE, 'SemiBold', a=pr(t, t0 + 0.4, 0.4))
    d = skia.Rect.MakeXYWH(380, 860, 320, 420); shape(c, d, (248, 244, 234))
    f = anton(50); c.drawString('PERMIT', 540 - f.measureText('PERMIT') / 2, 940, f, P(INKE))
    for i in range(6): c.drawLine(420, 990 + i * 40, 660 - (i % 3) * 40, 990 + i * 40, S(INKE, 2, 0.35))
    k = pr(t, t0 + 0.6, 0.4)
    if k > 0:
        c.drawLine(360, 840, 360 + 360 * eo(k), 840 + 460 * eo(k), S(ACC[0], 18)); c.drawLine(720, 840, 720 - 360 * eo(k), 840 + 460 * eo(k), S(ACC[0], 18))


def s_law(c, t):
    t0 = SCENES[2][0]; tt = ph('tripled'); pg(c, False, 3, t)
    headline(c, [[('THE COTTAGE', False)], [('FOOD LAW.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    body(c, 'TEXAS SB 541, IN EFFECT SEPT 2025', 150, 800, 30, MUTE, 'SemiBold', a=pr(t, t0 + 0.4, 0.4))
    c.drawLine(150, 1300, 930, 1300, S(INKE, 4))
    for j, (v, l, ti) in enumerate(((50, 'BEFORE', t0 + 0.6), (150, 'NOW', tt - 0.2))):
        k = pr(t, ti, 0.7)
        if k <= 0: continue
        h = 2.6 * v * eo(k); x = 230 + j * 380; col = ACC[0] if j else (180, 172, 162)
        c.drawRect(skia.Rect.MakeXYWH(x, 1300 - h, 240, h), P(col)); c.drawRect(skia.Rect.MakeXYWH(x, 1300 - h, 240, h), S(INKE, 4))
        f = anton(84); s_ = '$%dK' % int(v * eo(k)); c.drawString(s_, x + 120 - f.measureText(s_) / 2, 1280 - h, f, P(INKE, k))
        g = font(32, 'Bold', False); c.drawString(l, x + 120 - g.measureText(l) / 2, 1350, g, P(INKE, k))


def s_sell(c, t):
    t0 = SCENES[3][0]; tp = ph('pumpkin'); tr = ph('register'); pg(c, True, 4, t)
    headline(c, [[('WHAT CAN', False)], [('YOU', False), ('SELL?', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    k1 = pr(t, ph('cookies') - 0.2, 0.4); k2 = pr(t, ph('bread') - 0.2, 0.4); k3 = pr(t, tp - 0.2, 0.4)
    if k1 > 0: cookie(c, 260, 1000, 1.0 * eback(k1)); cookie(c, 330, 1060, 0.9 * eback(k1))
    if k2 > 0: loaf(c, 720, 1020, 1.0 * eback(k2))
    if k3 > 0: pie(c, 330, 1180, 1.0 * eback(k3)); pie(c, 760, 1180, 0.9 * eback(k3), (244, 230, 200))
    stamp(c, 560, 1310, 'REGISTER WITH THE STATE', pr(t, tr - 0.2, 0.35), -3, 38, fill=CREAM)


def s_rules(c, t):
    t0 = SCENES[4][0]; pg(c, False, 5, t)
    headline(c, [[('THE', False), ('RULES.', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5))
    rows = (('FOOD HANDLER COURSE', 'course'), ('LABEL EVERYTHING', 'label'), ('NO MEAT. NO SEAFOOD.', 'no meat'))
    for i, (s_, w) in enumerate(rows):
        k = pr(t, ph(w) - 0.2, 0.35)
        if k <= 0: continue
        y = 780 + i * 110; c.drawRect(skia.Rect.MakeXYWH(150, y - 46, 50, 50), S(INKE, 4, k))
        q = skia.Path(); q.moveTo(158, y - 22); q.lineTo(172, y - 6); q.lineTo(196, y - 40); c.drawPath(q, S(ACC[0], 8, k))
        c.drawString(s_, 230, y, anton(64), P(INKE, k))
    label_card(c, 560, 1260, 1.0, pr(t, ph('home kitchen') - 0.3, 0.4))


def s_limit(c, t):
    t0 = SCENES[5][0]; to = ph('start with'); pg(c, True, 6, t)
    if t < to - 0.2:
        headline(c, [[('A LIMIT.', False)], [('NOT A', False), ('PROMISE.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    else:
        headline(c, [[('START WITH', False)], [('ONE THING.', True)]], 150, 520, 132, pr(t, to - 0.2, 0.4), dark=True)
        pie(c, 540, 1130, 1.4)
        body(c, 'the one your neighbors already ask for', 150, 1280, 40, CREAM_T, 'SemiBold', a=pr(t, to + 0.5, 0.4))


def s_end(c, t):
    t0 = SCENES[6][0]; tm = ph('might be')
    if t < tm - 0.3:
        pg(c, False, 7, t)
        headline(c, [[('YOUR', False), ('KITCHEN', True)]], 150, 520, 150, pr(t, t0 + 0.05, 0.5))
        oven(c, 540, 1140, 0.75, 1.0, t)
    else:
        final_fill(c, LABEL, num(7), t / DUR, ('THE CHEAPEST', 'STOREFRONT', 'IN TEXAS.'), pr(t, tm - 0.3, 0.5), 130)
        pie(c, 540, 1300, 1.0)


SCENES = [(0.0, s_hook), (ph('and no city') - 0.15, s_permit), (ph("it's called") - 0.15, s_law), (ph('so what can') - 0.15, s_sell),
          (ph('the rules') - 0.15, s_rules), (ph('that cap') - 0.15, s_limit), (ph('your kitchen') - 0.15, s_end)]
DARK_S = {1, 3, 5}
FILL_T = ph('might be') - 0.3
SHAKES = [(ph('hundred fifty'), 10, 0.35), (ph('tripled'), 10, 0.35), (ph('no meat'), 6, 0.25), (ph('might be'), 10, 0.35)]
frame = build(T, SCENES, DARK_S, SHAKES, FILL_T)


def cover(c):
    page(c, False, label='BUSINESS IDEA', num='N° 03')
    headline(c, [[('TEXAS LETS YOU', False)], [('SELL UP TO $150K', False)], [('FROM YOUR', False), ('KITCHEN.', True)]], 150, 540, 116, 1.0, maxw=860)
    oven(c, 540, 1200, 0.85, 1.0, 0.5)


if __name__ == '__main__': main(HERE, frame, cover, DUR)
