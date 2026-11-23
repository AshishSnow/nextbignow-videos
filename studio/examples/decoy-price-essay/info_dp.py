"""Decoy pricing (Ariely / The Economist offer) in the ESSAY look, accent RED. No magazine logo or trade dress (name as plain text only)."""
import sys, os, math, subprocess
sys.path.insert(0, '/home/claude/studio')
from essay_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (214, 52, 44)
NS = 7
OPTS = [('ONLINE', '$59'), ('PRINT', '$125'), ('PRINT + ONLINE', '$125')]
XS = [215, 540, 865]


def num(i): return '%02d / %02d' % (i, NS)


def shape(c, sh, fill, ow=4):
    if isinstance(sh, skia.Rect): c.drawRect(sh, P(fill)); c.drawRect(sh, S(INKE, ow))
    elif isinstance(sh, skia.RRect): c.drawRRect(sh, P(fill)); c.drawRRect(sh, S(INKE, ow))
    else: c.drawPath(sh, P(fill)); c.drawPath(sh, S(INKE, ow))


def hatch_rect(c, r, a=0.35, step=9):
    c.save(); c.clipRect(r)
    for i in range(int(r.left()) - 400, int(r.right()) + 400, step): c.drawLine(i, r.bottom(), i + 200, r.top(), S(INKE, 1.3, a))
    c.restore()


def icon(c, kind, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if kind in ('screen', 'both'):
        ox = -30 if kind == 'both' else 0
        shape(c, rr(ox - 60, -50, 120, 80, 8), (250, 246, 236), 4); c.drawRect(skia.Rect.MakeXYWH(ox - 48, -40, 96, 58), P(ACC[0], 0.25))
        c.drawLine(ox - 20, 46, ox + 20, 46, S(INKE, 5)); c.drawLine(ox, 30, ox, 46, S(INKE, 4))
    if kind in ('paper', 'both'):
        ox = 40 if kind == 'both' else 0; oy = 14 if kind == 'both' else 0
        r = skia.Rect.MakeXYWH(ox - 46, oy - 56, 92, 112); shape(c, r, (250, 246, 236), 4)
        c.drawRect(skia.Rect.MakeXYWH(ox - 34, oy - 44, 68, 16), P(INKE))
        for i in range(5): c.drawLine(ox - 34, oy - 16 + i * 14, ox + 34, oy - 16 + i * 14, S(INKE, 2, 0.6))
    c.restore()


def card(c, i, x, y, k=1.0, hl=False, dim=False, cross=0.0):
    if k <= 0: return
    lab, price = OPTS[i]; kind = ['screen', 'paper', 'both'][i]
    def d():
        r = rr(x - 140, y - 190, 280, 380, 18)
        c.drawRRect(rr(x - 132, y - 180, 280, 380, 18), P(INKE, 0.18))
        c.drawRRect(r, P(ACC[0] if hl else (250, 246, 236))); c.drawRRect(r, S(INKE, 4))
        if not hl: hatch_rect(c, skia.Rect.MakeXYWH(x - 140, y + 110, 280, 80), 0.25)
        icon(c, kind, x, y - 70, 1.0)
        f = font(30 if i < 2 else 26, 'Bold', False); c.drawString(lab, x - f.measureText(lab) / 2, y + 60, f, P(CREAM_T if hl else INKE))
        g = anton(84); c.drawString(price, x - g.measureText(price) / 2, y + 170, g, P(CREAM_T if hl else INKE))
        if dim: c.drawRRect(r, P(CREAM, 0.55))
        if cross > 0:
            c.drawLine(x - 150, y - 200, x - 150 + 300 * cl(cross * 2), y - 200 + 400 * cl(cross * 2), S(ACC[0], 12))
            if cross > 0.5: c.drawLine(x + 150, y - 200, x + 150 - 300 * cl(cross * 2 - 1), y - 200 + 400 * cl(cross * 2 - 1), S(ACC[0], 12))
    pop(c, k, x, y, d)


def bars(c, vals, k, x0=150, base=1320, h=420, labels=('ONLINE', 'PRINT', 'PRINT+ONLINE'), hl=2, dark=False):
    tc = CREAM_T if dark else INKE
    c.drawLine(x0 - 20, base, x0 + 800, base, S(tc, 4))
    for i, v in enumerate(vals):
        if v is None: continue
        x = x0 + i * 270; kk = eo(cl(k * 1.4 - i * 0.15)); hh = max(4, h * v / 100 * kk)
        r = skia.Rect.MakeXYWH(x, base - hh, 200, hh); c.drawRect(r, P(ACC[0] if i == hl else ((70, 66, 62) if dark else (205, 198, 186))))
        if i != hl: hatch_rect(c, r, 0.4 if not dark else 0.2)
        c.drawRect(r, S(tc, 3))
        f = anton(76); s_ = '%d%%' % round(v * kk); c.drawString(s_, x + 100 - f.measureText(s_) / 2, base - hh - 22, f, P(tc))
        g = font(26, 'SemiBold', False); c.drawString(labels[i], x + 100 - g.measureText(labels[i]) / 2, base + 44, g, P(tc, 0.85))


def duck(c, x, y, s=1.0, col=None):
    col = col or (196, 150, 98)
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-230, 120, 460, 40), P(INKE, 0.18))
    bodyp = skia.Path(); bodyp.moveTo(-220, 40); bodyp.cubicTo(-200, -40, 80, -60, 160, -10); bodyp.cubicTo(200, 20, 190, 90, 150, 110)
    bodyp.cubicTo(60, 140, -160, 140, -210, 100); bodyp.cubicTo(-240, 80, -236, 60, -220, 40); bodyp.close()
    c.drawPath(bodyp, P(col))
    c.save(); c.clipPath(bodyp, doAntiAlias=True)
    for i in range(-300, 300, 9): c.drawLine(i, 140, i + 120, -60, S(INKE, 1.3, 0.35))
    c.drawPath(skia.Path(), P(INKE)); c.restore()
    c.drawPath(bodyp, S(INKE, 4))
    wing = skia.Path(); wing.moveTo(-140, 30); wing.cubicTo(-80, -10, 40, -6, 90, 30); wing.cubicTo(30, 60, -80, 70, -140, 30); wing.close(); c.drawPath(wing, P((150, 110, 70))); c.drawPath(wing, S(INKE, 3))
    neck = skia.Path(); neck.moveTo(120, -20); neck.cubicTo(110, -90, 130, -150, 190, -150); neck.cubicTo(240, -150, 250, -100, 230, -70); neck.cubicTo(210, -40, 190, -20, 180, 10); neck.close()
    c.drawPath(neck, P((40, 90, 60))); c.drawPath(neck, S(INKE, 4))
    bill = skia.Path(); bill.moveTo(236, -112); bill.cubicTo(270, -112, 300, -104, 306, -94); bill.cubicTo(290, -86, 262, -84, 232, -90); bill.close(); c.drawPath(bill, P((232, 180, 60))); c.drawPath(bill, S(INKE, 3))
    c.drawCircle(205, -118, 8, P(INKE)); c.drawLine(140, -30, 200, -34, S(CREAM, 6))
    c.restore()


def pg(c, *a, **k): page(c, *a, label='N° 02 — ESSAY', **k)


# ------------------------------------------------------------------ scenes
def s_pick(c, t):
    pg(c, False, num=num(1), prog=t / DUR)
    headline(c, [[('WHICH ONE', False)], [('WOULD YOU', False), ('BUY?', True)]], 150, 520, 132, 1.0)
    for i, w in enumerate(('online', 'print for', 'print plus')):
        k = 1.0 if i == 0 else pr(t, ph(w) - 0.15, 0.35)
        card(c, i, XS[i], 1000, k)


def s_you(c, t):
    t0 = SCENES[1][0]; t84 = ph('eighty four')
    pg(c, True, num=num(2), prog=t / DUR)
    headline(c, [[('YOU PICKED', False)], [('THIS ONE,', True), ('RIGHT?', False)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5), dark=True)
    for i in range(3): card(c, i, XS[i], 930, 1.0, hl=(i == 2), dim=(i < 2))
    k = pr(t, t0 + 0.3, 0.6)
    if k > 0:   # hand-drawn ring around the bundle
        p = skia.Path(); p.addOval(skia.Rect.MakeXYWH(XS[2] - 175, 710, 350, 440))
        meas = skia.PathMeasure(p, False); seg = skia.Path(); meas.getSegment(0, meas.getLength() * eo(k), seg, True); c.drawPath(seg, S(CREAM_T, 7))
    if t > t84 - 0.2:
        pop(c, pr(t, t84 - 0.2, 0.4), 300, 1290, lambda: (c.drawString('84%', 150, 1340, anton(130), P(ACC[0])), body(c, 'of students did too', 390, 1320, 38, CREAM_T, 'SemiBold')))


def s_zero(c, t):
    t0 = SCENES[2][0]; tz = ph('zero percent')
    pg(c, False, num=num(3), prog=t / DUR)
    headline(c, [[('NOBODY PICKED', False)], [('THE', False), ('MIDDLE ONE.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5))
    bars(c, [16, 0, 84], pr(t, t0 + 0.2, 0.8), hl=1 if t > tz - 0.2 else 2)
    if t > tz - 0.2:
        k = pr(t, tz - 0.2, 0.4); c.drawCircle(150 + 270 + 100, 1290, 80 * eback(k), S(ACC[0], 8))
    body(c, "Dan Ariely's test, Predictably Irrational", 150, 750, 32, MUTE, 'Medium', a=pr(t, t0 + 0.4, 0.4))


def s_flip(c, t):
    t0 = SCENES[3][0]; tf = ph('choice flipped'); t68 = ph('sixty eight')
    pg(c, True, num=num(4), prog=t / DUR)
    if t < tf + 0.1:
        headline(c, [[('SO HE', False), ('DELETED', True)], [('THE MIDDLE ONE.', False)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5), dark=True)
        for i in range(3):
            if i == 1:
                u = eo(pr(t, ph('took it away') + 0.2, 0.6)); c.save(); c.translate(0, 600 * u); card(c, 1, XS[1], 1000, 1.0, cross=pr(t, ph('took it away') - 0.1, 0.4)); c.restore()
            else: card(c, i, XS[i], 1000, 1.0)
    else:
        headline(c, [[('AND THE CHOICE', False)], [('FLIPPED.', True)]], 150, 520, 120, pr(t, tf, 0.5), dark=True)
        bars(c, [68, None, 32], pr(t, t68 - 0.3, 0.8), hl=0, dark=True, labels=('ONLINE', '', 'PRINT+ONLINE'))


def s_decoy(c, t):
    t0 = SCENES[4][0]; td = ph("it's a decoy"); tu = ph('free upgrade')
    pg(c, False, num=num(5), prog=t / DUR)
    headline(c, [[("IT'S CALLED A", False)], [('DECOY.', True)]], 150, 520, 132, pr(t, td - 0.4, 0.5) if t > td - 0.6 else 0.0)
    if t < td - 0.4: headline(c, [[('THAT USELESS', False)], [('MIDDLE OPTION?', False)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5))
    k = pr(t, td - 0.3, 0.5)
    if k < 1: card(c, 1, 540, 1000, 1.0 - k)
    if k > 0: pop(c, k, 540, 1000, lambda: duck(c, 520, 1020, 1.25))
    if t > tu - 0.5:
        body(c, 'It makes the bundle look', 150, 1290, 40, INKE, 'SemiBold', a=pr(t, tu - 0.5, 0.3))
        body(c, 'like a free upgrade.', 150, 1345, 40, ACC[0], 'Bold', a=pr(t, tu - 0.3, 0.3))


def s_end(c, t):
    t0 = SCENES[5][0]; ts = ph('doing all')
    if t < ts - 0.3:
        pg(c, False, num=num(6), prog=t / DUR)
        headline(c, [[('NEXT TIME YOU SEE', False)], [('THREE', False), ('PRICES...', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5))
        for i in range(3): card(c, i, XS[i], 1000, 1.0, dim=(i != 1))
    else:
        pg(c, False, num=num(7), prog=t / DUR, fill=ACC[0])
        k = pr(t, ts - 0.3, 0.5); f = anton(132)
        for i, s_ in enumerate(('THE ONE NOBODY', 'BUYS IS DOING', 'ALL THE SELLING.')):
            kk = eo(cl(k * 1.6 - i * 0.2)); c.save(); c.translate(0, 40 * (1 - kk))
            c.drawString(s_, 150, 560 + i * 140, f if i < 2 else anton(118), P(CREAM_T if i != 2 else INKE, kk)); c.restore()
        duck(c, 560, 1120, 0.95, (250, 246, 236))


SCENES = [(0.0, s_pick), (ph('you picked') - 0.15, s_you), (ph('now look') - 0.15, s_zero), (ph('so why') - 0.15, s_flip),
          (ph('that useless') - 0.15, s_decoy), (ph('so next time') - 0.15, s_end)]
DARK_S = {1, 3}
SHAKES = [(ph('eighty four'), 8, 0.3), (ph('zero percent'), 10, 0.35), (ph('choice flipped'), 10, 0.35), (ph("it's a decoy"), 10, 0.35), (ph('doing all'), 12, 0.4)]
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
    dark = i in DARK_S or (i == len(SCENES) - 1 and t >= ph('doing all') - 0.3)
    if 0.2 < t < END + 0.1: esubs(c, T, t, dark, 1440)
    return s


def cover(out):
    s = skia.Surface(W, H); c = s.getCanvas()
    page(c, False, label='OOPS, MY BUSINESS', num='N° 02')
    headline(c, [[('THE PRICE', False)], [('NOBODY', False), ('BUYS.', True)]], 150, 540, 160, 1.0, maxw=800)
    for i in range(3): card(c, i, XS[i], 1030, 1.0, cross=1.0 if i == 1 else 0.0)
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
