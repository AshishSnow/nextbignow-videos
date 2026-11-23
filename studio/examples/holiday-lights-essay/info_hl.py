"""BUSINESS IDEA (green) N° 01: holiday light installation. ESSAY look. Generic house, ladder, bulbs; no brands, no people."""
import sys, os, math, subprocess
sys.path.insert(0, '/home/claude/studio')
from essay_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (34, 140, 92)
NS = 9
LABEL = 'BUSINESS IDEA — N° 01'
BULBS = [(214, 52, 44), (240, 190, 40), (34, 140, 92), (36, 98, 214), (232, 150, 20)]
WOOD = (176, 128, 84)
WALL = (226, 214, 192)
ROOF = (86, 80, 74)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, *a, **k): page(c, *a, label=LABEL, **k)


def shape(c, sh, fill, ow=4, a=1.0):
    if isinstance(sh, skia.Rect): c.drawRect(sh, P(fill, a)); c.drawRect(sh, S(INKE, ow, a))
    elif isinstance(sh, skia.RRect): c.drawRRect(sh, P(fill, a)); c.drawRRect(sh, S(INKE, ow, a))
    else: c.drawPath(sh, P(fill, a)); c.drawPath(sh, S(INKE, ow, a))


def hatch(c, clip, a=0.35, step=9, ang=1):
    c.save(); c.clipPath(clip, doAntiAlias=True); b = clip.getBounds()
    for i in range(int(b.left()) - 500, int(b.right()) + 500, step): c.drawLine(i, b.bottom(), i + 250 * ang, b.top(), S(INKE, 1.3, a))
    c.restore()


def bulb(c, x, y, col, on=1.0, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if on > 0.05:
        c.drawCircle(0, 16, 30, P(col, 0.22 * on)); c.drawCircle(0, 16, 18, P(col, 0.25 * on))
    shape(c, rr(-7, -12, 14, 12, 3), (90, 90, 86), 2)
    b = skia.Path(); b.moveTo(-8, 0); b.cubicTo(-14, 10, -10, 30, 0, 36); b.cubicTo(10, 30, 14, 10, 8, 0); b.close()
    mix = tuple(int(150 + (cc - 150) * (0.35 + 0.65 * on)) for cc in col)
    c.drawPath(b, P(mix)); c.drawPath(b, S(INKE, 2.5))
    c.drawLine(-3, 8, -4, 24, S(WHITE, 3, 0.6 * on))
    c.restore()


def strand(c, pts, on=1.0, t=0.0, k=1.0, s=0.9, sag=18):
    """wire with bulbs along a polyline; k = how much is strung (0..1); on = lit; twinkle with t"""
    segs = []; tot = 0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0); segs.append((x0, y0, x1, y1, L)); tot += L
    lim = tot * k; acc_ = 0; idx = 0
    for (x0, y0, x1, y1, L) in segs:
        if acc_ >= lim: break
        u1 = min(1, (lim - acc_) / L)
        p = skia.Path(); n = max(2, int(L / 70))
        p.moveTo(x0, y0)
        for j in range(1, int(n * u1) + 1):
            ua = (j - 0.5) / n; ub = j / n
            p.quadTo(x0 + (x1 - x0) * ua, y0 + (y1 - y0) * ua + sag, x0 + (x1 - x0) * ub, y0 + (y1 - y0) * ub)
        c.drawPath(p, S((40, 60, 40), 3))
        for j in range(int(n * u1)):
            ua = (j + 0.5) / n; bx = x0 + (x1 - x0) * ua; by = y0 + (y1 - y0) * ua + sag / 2
            tw = 0.75 + 0.25 * math.sin(t * 5 + idx * 1.7)
            bulb(c, bx, by, BULBS[idx % 5], on * tw, s); idx += 1
        acc_ += L


def house(c, x, y, s=1.0, on=0.0, t=0.0, k=1.0, night=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-330, 250, 660, 40), P(INKE, 0.15))
    wall = skia.Rect.MakeXYWH(-260, -20, 520, 280); shape(c, wall, WALL); hatch(c, skia.Path.Rect(wall), 0.12, 11)
    roof = path([(-310, -10), (0, -230), (310, -10)]); shape(c, roof, ROOF); hatch(c, roof, 0.3, 8)
    shape(c, skia.Rect.MakeXYWH(150, -200, 50, 100), (150, 70, 56), 3)
    shape(c, skia.Rect.MakeXYWH(-40, 120, 80, 140), (120, 84, 60))
    for wx in (-200, 110):
        win = skia.Rect.MakeXYWH(wx, 50, 90, 80); shape(c, win, (255, 220, 120) if night else (180, 200, 210), 3)
        c.drawLine(wx + 45, 50, wx + 45, 130, S(INKE, 3)); c.drawLine(wx, 90, wx + 90, 90, S(INKE, 3))
    c.restore()
    # lights along roof edges + gutter, in world coords
    P0 = lambda px, py: (x + px * s, y + py * s)
    strand(c, [P0(-310, -10), P0(0, -230), P0(310, -10)], on, t, k, 0.9 * s / 1.0, 14 * s)
    if k > 0.5: strand(c, [P0(-260, -16), P0(260, -16)], on, t + 1, (k - 0.5) * 2, 0.8 * s, 16 * s)


def ladder(c, x, y, s=1.0, rot=0.0, a=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for rx in (-50, 50): shape(c, rr(rx - 9, -440, 18, 460, 6), WOOD, 3, a)
    for i in range(8): c.drawRect(skia.Rect.MakeXYWH(-45, -410 + i * 56, 90, 12), P(WOOD, a)); c.drawRect(skia.Rect.MakeXYWH(-45, -410 + i * 56, 90, 12), S(INKE, 2.5, a))
    c.restore()


def tag(c, x, y, txt, s=1.0, rot=-8, col=(255, 214, 40), k=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(eback(k) * s, eback(k) * s)
    f = anton(84); w = f.measureText(txt)
    shape(c, path([(-30, -60), (w + 40, -60), (w + 40, 60), (-30, 60), (-80, 0)]), col, 4)
    c.drawCircle(-40, 0, 10, P(CREAM)); c.drawCircle(-40, 0, 10, S(INKE, 3))
    c.drawString(txt, 0, 30, f, P(INKE)); c.restore()


def calpage(c, x, y, mon, k, check, sub=None):
    if k <= 0: return
    c.save(); c.translate(x, y + 40 * (1 - eo(k))); a = eo(k)
    shape(c, rr(-110, -120, 220, 240, 12), (246, 240, 230), 4, a)
    c.drawRect(skia.Rect.MakeXYWH(-110, -120, 220, 60), P(ACC[0], a)); c.drawRect(skia.Rect.MakeXYWH(-110, -120, 220, 60), S(INKE, 4, a))
    for rx in (-60, 60): c.drawLine(rx, -138, rx, -100, S(INKE, 6, a))
    f = font(34, 'Bold', False); c.drawString(mon, -f.measureText(mon) / 2, -76, f, P(CREAM_T, a))
    for r in range(3):
        for q in range(5): c.drawRect(skia.Rect.MakeXYWH(-90 + q * 37, -40 + r * 40, 28, 28), S(INKE, 1.5, 0.35 * a))
    if check > 0:
        p = skia.Path(); p.moveTo(-50, 20); p.lineTo(-10, 60); p.lineTo(70, -30)
        m = skia.PathMeasure(p, False); seg = skia.Path(); m.getSegment(0, m.getLength() * eo(check), seg, True)
        c.drawPath(seg, S(ACC[0], 16))
    if sub: body(c, sub, -f.measureText(sub) / 2 - 10, 170, 30, INKE, 'SemiBold', a=a)
    c.restore()


def shield(c, x, y, s=1.0, k=1.0):
    c.save(); c.translate(x, y); c.scale(eback(k) * s, eback(k) * s)
    p = skia.Path(); p.moveTo(0, -130); p.lineTo(110, -90); p.cubicTo(110, 20, 70, 100, 0, 140); p.cubicTo(-70, 100, -110, 20, -110, -90); p.close()
    shape(c, p, ACC[0], 5); hatch(c, p, 0.2, 10)
    q = skia.Path(); q.moveTo(-45, 0); q.lineTo(-10, 40); q.lineTo(55, -40); c.drawPath(q, S(CREAM_T, 16))
    c.restore()


def tape(c, x0, y0, x1, k):
    L = (x1 - x0) * eo(k)
    shape(c, rr(x0 - 70, y0 - 50, 100, 100, 18), (240, 190, 40), 4)
    c.drawCircle(x0 - 20, y0, 18, S(INKE, 4))
    if L > 0:
        c.drawRect(skia.Rect.MakeXYWH(x0 + 30, y0 - 14, L, 28), P((250, 220, 90))); c.drawRect(skia.Rect.MakeXYWH(x0 + 30, y0 - 14, L, 28), S(INKE, 3))
        for i in range(int(L / 30)): c.drawLine(x0 + 30 + i * 30, y0 - 14, x0 + 30 + i * 30, y0 - (2 if i % 2 else 6), S(INKE, 2))


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    pg(c, False, num=num(1), prog=t / DUR)
    headline(c, [[('160 A DAY.', False)], [('HURT', False), ('DECORATING.', True)]], 150, 520, 118, 1.0)
    k = pr(t, 1.2, 1.4)
    ladder(c, 600, 1330, 0.95, -6 - 22 * eio(k) + 1.5 * math.sin(t * 3))
    strand(c, [(220, 800), (420, 860), (520, 1010), (470, 1240)], 0.9, t, 1.0, 0.85)
    c.drawLine(180, 1335, 900, 1335, S(INKE, 4))
    for i in range(3):
        kk = pr(t, 1.6 + i * 0.12, 0.25); a = (1 - pr(t, 2.2 + i * 0.1, 0.4)) * kk
        if a > 0: c.drawLine(800 + i * 30, 900 + i * 40, 840 + i * 40, 880 + i * 46, S(INKE, 5, a))


def s_start(c, t):
    t0 = SCENES[1][0]
    pg(c, True, num=num(2), prog=t / DUR)
    headline(c, [[("THAT'S WHERE", False)], [('THE', False), ('BUSINESS', True)], [('STARTS.', False)]], 150, 520, 118, pr(t, t0 + 0.05, 0.5), dark=True)
    on = pr(t, ph('business') - 0.1, 0.4)
    house(c, 540, 1130, 0.95, on, t, 1.0, night=True)


def s_idea(c, t):
    t0 = SCENES[2][0]
    pg(c, False, num=num(3), prog=t / DUR)
    headline(c, [[('YOU CLIMB.', False)], [('THEY', False), ("DON'T.", True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    k = pr(t, t0 + 0.2, 1.6)
    house(c, 500, 1150, 0.85, 0.3 + 0.7 * k, t, k)
    ladder(c, 860, 1360, 0.9, -12)


def s_falls(c, t):
    t0 = SCENES[3][0]; tl = ph('ladders')
    pg(c, True, num=num(4), prog=t / DUR)
    headline(c, [[('A LOT OF THEM', False)], [('ARE', False), ('FALLS.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5), dark=True)
    items = [('LADDERS', ph('ladders')), ('ROOFS', ph('roofs')), ('GUTTERS', ph('gutters'))]
    for i, (s_, ti) in enumerate(items):
        k = pr(t, ti - 0.15, 0.35)
        if k <= 0: continue
        y = 860 + i * 150; c.save(); c.translate(-60 * (1 - eo(k)), 0)
        c.drawRect(skia.Rect.MakeXYWH(150, y - 80, 14, 100), P(ACC[0], k))
        c.drawString(s_, 200, y, anton(110), P(CREAM_T, k)); c.restore()
    ladder(c, 860, 1330, 0.7, 10 + 8 * math.sin(t * 2.2), a=pr(t, tl, 0.4))


def s_price(c, t):
    t0 = SCENES[4][0]; tq = ph('just to hang')
    pg(c, False, num=num(5), prog=t / DUR)
    body(c, 'AVERAGE PRO INSTALL (HOMEADVISOR, 2025)', 150, 520, 30, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    k = pr(t, ph('four hundred') - 0.2, 0.7)
    s_ = '$%d' % int(round(440 * eo(k))); c.drawString(s_, 140, 760, anton(240), P(INKE, max(0.15, k)))
    house(c, 540, 1160, 0.75, 1.0 if k > 0.9 else 0.3, t, 1.0)
    if t > tq - 0.2:
        kk = pr(t, tq - 0.2, 0.35); c.save(); c.translate(760, 620); c.rotate(-9); c.scale(eback(kk), eback(kk))
        r = rr(-190, -60, 380, 120, 14); c.drawRRect(r, P(CREAM)); c.drawRRect(r, S(ACC[0], 8)); f2 = anton(70); s2 = 'FOR LIGHTS?'
        c.drawString(s2, -f2.measureText(s2) / 2, 26, f2, P(ACC[0])); c.restore()


def s_foot(c, t):
    t0 = SCENES[5][0]; td = ph('taking them')
    pg(c, True, num=num(6), prog=t / DUR)
    headline(c, [[('PRICED BY THE', False)], [('FOOT.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    k = pr(t, t0 + 0.4, 1.3)
    strand(c, [(150, 860), (930, 860)], 1.0, t, k, 0.9)
    tape(c, 200, 980, 900, k)
    if t > td - 0.2:
        kk = pr(t, td - 0.2, 0.4)
        body(c, 'TAKEDOWN: OFTEN INCLUDED', 150, 1180, 46, CREAM_T, 'Bold', a=kk)
        c.drawRect(skia.Rect.MakeXYWH(150, 1205, 590 * eo(kk), 8), P(ACC[0]))


def s_cal(c, t):
    t0 = SCENES[6][0]
    pg(c, False, num=num(7), prog=t / DUR)
    headline(c, [[('ONE CUSTOMER.', False)], [('THREE', False), ('VISITS.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5))
    marks = [('NOV', ph('november'), 'put up'), ('JAN', ph('january'), 'take down'), ('NOV', ph('next year'), 'next year')]
    for i, (m, ti, sub) in enumerate(marks):
        calpage(c, 250 + i * 290, 960, m, pr(t, ti - 0.35, 0.4), pr(t, ti, 0.4), sub)
    for i in range(2):
        kk = pr(t, marks[i + 1][1] - 0.5, 0.4)
        if kk > 0: dotted(c, 370 + i * 290, 960, 370 + i * 290 + 50 * kk, 960, 1.0)


def s_catch(c, t):
    t0 = SCENES[7][0]; ti = ph('get liability')
    pg(c, True, num=num(8), prog=t / DUR)
    if t < ti - 0.3:
        headline(c, [[('THE', False), ('CATCH?', True)]], 150, 520, 150, pr(t, t0 + 0.05, 0.5), dark=True)
        for i, (s_, w) in enumerate((('SHORT SEASON', 'short season'), ('COLD', 'cold'), ('ROOFS', "you're on"))):
            k = pr(t, ph(w) - 0.15, 0.35)
            if k > 0:
                y = 860 + i * 140; c.drawString(s_, 150 + 40 * (1 - eo(k)), y, anton(100), P(CREAM_T, k))
                c.drawLine(150, y + 18, 150 + (anton(100).measureText(s_)) * eo(pr(t, ph(w) + 0.2, 0.3)), y + 18, S(ACC[0], 8, k))
    else:
        k = pr(t, ti - 0.3, 0.5)
        headline(c, [[('BEFORE YOU', False)], [('CLIMB:', True)]], 150, 520, 130, k, dark=True)
        shield(c, 300, 950, 1.1, pr(t, ti, 0.4)); body(c, 'LIABILITY', 440, 930, 56, CREAM_T, 'Bold', a=pr(t, ti, 0.4)); body(c, 'INSURANCE', 440, 995, 56, CREAM_T, 'Bold', a=pr(t, ti, 0.4))
        ks = pr(t, ph('solid ladder') - 0.2, 0.4)
        if ks > 0: ladder(c, 300, 1360, 0.6, 0, a=ks); body(c, 'A SOLID LADDER', 440, 1240, 56, CREAM_T, 'Bold', a=ks)


def s_end(c, t):
    t0 = SCENES[8][0]; ts = ph('the smart')
    if t < ts - 0.3:
        pg(c, False, num=num(9), prog=t / DUR)
        headline(c, [[('PEOPLE RISK', False)], [('THE LADDER', False)], [('FOR', False), ('FREE.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5))
        ladder(c, 540, 1360, 0.9, -8 + 4 * math.sin(t * 3))
    else:
        page(c, False, label=LABEL, num=num(9), prog=t / DUR, fill=ACC[0])
        k = pr(t, ts - 0.3, 0.5); f = anton(130)
        for i, s_ in enumerate(('THE SMART ONES', 'PAY SOMEONE', 'TO CLIMB IT.')):
            kk = eo(cl(k * 1.6 - i * 0.2)); c.save(); c.translate(0, 40 * (1 - kk)); c.drawString(s_, 150, 580 + i * 140, f, P(CREAM_T if i < 2 else INKE, kk)); c.restore()
        house(c, 540, 1110, 0.7, 1.0, t, 1.0, night=True)


SCENES = [(0.0, s_hook), (ph("and that's") - 0.15, s_start), (ph('the idea') - 0.15, s_idea), (ph('a lot of') - 0.15, s_falls),
          (ph('so people pay') - 0.15, s_price), (ph('pros often') - 0.15, s_foot), (ph('so you show') - 0.15, s_cal),
          (ph('the catch') - 0.15, s_catch), (ph('every december') - 0.15, s_end)]
DARK_S = {1, 3, 5, 7}
SHAKES = [(ph('hurt'), 10, 0.35), (ph('falls'), 10, 0.35), (ph('four hundred'), 8, 0.3), (ph('the catch'), 8, 0.3), (ph('the smart'), 12, 0.4)]
TR = 0.3


def draw_scene(c, i, t): SCENES[i][1](c, t)


def frame(t):
    s = skia.Surface(W, H); c = s.getCanvas(); sx = sy = 0.0
    for (ts, a, d) in SHAKES:
        if ts <= t < ts + d: k = 1 - (t - ts) / d; sx += a * k * math.sin(t * 90); sy += a * k * math.cos(t * 77)
    c.save(); c.translate(sx, sy)
    i = max(j for j, (t0, _) in enumerate(SCENES) if t >= t0)
    draw_scene(c, i, t)
    if i > 0 and t < SCENES[i][0] + TR:
        k = eio((t - SCENES[i][0]) / TR); c.save(); c.translate(-W * k, 0); draw_scene(c, i - 1, t); c.restore()
    c.restore()
    dark = i in DARK_S or (i == len(SCENES) - 1 and t >= ph('the smart') - 0.3)
    if 0.2 < t < END + 0.1: esubs(c, T, t, dark, 1440)
    return s


def cover(out):
    s = skia.Surface(W, H); c = s.getCanvas()
    page(c, False, label='BUSINESS IDEA', num='N° 01')
    headline(c, [[('GET PAID', False)], [('TO HANG', False), ('LIGHTS.', True)]], 150, 540, 150, 1.0, maxw=820)
    house(c, 540, 1200, 0.9, 1.0, 0.7, 1.0, night=True); ladder(c, 900, 1420, 0.75, -12)
    s.makeImageSnapshot().save(out, skia.kPNG)


def to_np(img): return img.toarray(colorType=skia.kRGBA_8888_ColorType)[:, :, :3]


if __name__ == '__main__':
    out = os.path.join(HERE, 'out'); os.makedirs(out, exist_ok=True)
    if sys.argv[1] == 'still':
        for v in sys.argv[2:]: frame(float(v)).makeImageSnapshot().save(os.path.join(out, 'ig_%06.2f.png' % float(v)), skia.kPNG)
    elif sys.argv[1] == 'nframes': print(int(DUR * FPS))
    elif sys.argv[1] == 'cover': cover(sys.argv[2])
    elif sys.argv[1] == 'range':
        f0, f1 = int(sys.argv[2]), int(sys.argv[3])
        enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
                                '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', os.path.join(out, 'ig_%05d.mp4' % f0)], stdin=subprocess.PIPE)
        for fi in range(f0, f1): enc.stdin.write(np.ascontiguousarray(to_np(frame(fi / FPS).makeImageSnapshot())).tobytes())
        enc.stdin.close(); enc.wait()
