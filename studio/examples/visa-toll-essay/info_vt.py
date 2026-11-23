"""MONEY EXPLAINED (blue) N° 01: how Visa makes money. ESSAY look. Generic blank card, generic banks, toll road. No logos, no card art."""
import sys, os, math, subprocess
sys.path.insert(0, '/home/claude/studio')
from essay_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (36, 98, 214)
NS = 9
LABEL = 'MONEY EXPLAINED — N° 01'
GOLD = (222, 176, 60)
STONE = (220, 210, 192)
ROAD = (70, 66, 62)


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


def card(c, x, y, s=1.0, rot=0.0, sx=1.0, col=None):
    col = col or ACC[0]
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * sx, s)
    c.drawRRect(rr(-170, -100, 340, 210, 22), P(INKE, 0.18))
    body_ = rr(-180, -115, 360, 220, 22); shape(c, body_, col, 5)
    c.save(); c.clipRRect(body_, doAntiAlias=True)
    for i in range(-400, 400, 14): c.drawLine(i, 120, i + 160, -120, S(WHITE, 1.4, 0.18))
    c.restore()
    shape(c, rr(-140, -50, 64, 48, 8), GOLD, 3)
    c.drawLine(-140, -26, -76, -26, S(INKE, 2)); c.drawLine(-108, -50, -108, -2, S(INKE, 2))
    for i in range(4): c.drawRect(skia.Rect.MakeXYWH(-140 + i * 72, 30, 56, 14), P(CREAM_T, 0.85))
    c.drawRect(skia.Rect.MakeXYWH(-140, 64, 120, 10), P(CREAM_T, 0.6))
    c.restore()


def bank(c, x, y, s=1.0, a=1.0, lbl=None):
    c.save(); c.translate(x, y); c.scale(s, s)
    roof = path([(-170, -150), (0, -240), (170, -150)]); shape(c, roof, STONE, 4, a); hatch(c, roof, 0.25 * a, 8)
    shape(c, skia.Rect.MakeXYWH(-170, -150, 340, 30), STONE, 4, a)
    for i in range(4):
        col = skia.Rect.MakeXYWH(-140 + i * 80, -120, 40, 200); shape(c, col, (238, 230, 214), 3, a); hatch(c, skia.Path.Rect(skia.Rect.MakeXYWH(-140 + i * 80 + 26, -120, 14, 200)), 0.3 * a, 6)
    shape(c, skia.Rect.MakeXYWH(-190, 80, 380, 34), STONE, 4, a)
    c.restore()
    if lbl:
        f = font(30, 'Bold', False); c.drawString(lbl, x - f.measureText(lbl) / 2, y + 160 * s, f, P(INKE, a))


def coin(c, x, y, r=34, a=1.0, sym='$'):
    c.drawCircle(x, y, r, P(GOLD, a)); c.drawCircle(x, y, r, S(INKE, 3, a)); c.drawCircle(x, y, r * 0.72, S(INKE, 2, 0.5 * a))
    f = anton(int(r * 1.1)); c.drawString(sym, x - f.measureText(sym) / 2, y + r * 0.38, f, P(INKE, a))


def road(c, y, t, dark=False, k=1.0, booth=True):
    c.drawRect(skia.Rect.MakeXYWH(0, y - 70, W, 140), P(ROAD)); c.drawRect(skia.Rect.MakeXYWH(0, y - 70, W, 140), S(INKE, 4))
    off = (t * 220) % 120
    for i in range(-1, 11): c.drawRect(skia.Rect.MakeXYWH(i * 120 + off, y - 6, 60, 12), P(CREAM_T, 0.8))
    if booth:
        bx = 540; shape(c, skia.Rect.MakeXYWH(bx - 70, y - 300, 140, 200), (238, 230, 214)); shape(c, path([(bx - 95, y - 300), (bx, y - 360), (bx + 95, y - 300)]), ACC[0])
        shape(c, skia.Rect.MakeXYWH(bx - 44, y - 270, 88, 70), (180, 200, 210), 3)
        ang = -70 * (0.5 + 0.5 * math.sin(t * 2.4))
        c.save(); c.translate(bx + 70, y - 120); c.rotate(ang); c.drawRect(skia.Rect.MakeXYWH(0, -8, 240, 16), P(CREAM_T)); c.drawRect(skia.Rect.MakeXYWH(0, -8, 240, 16), S(INKE, 3))
        for i in range(4): c.drawRect(skia.Rect.MakeXYWH(20 + i * 56, -8, 26, 16), P(ACC[0]))
        c.restore()


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    pg(c, False, num=num(1), prog=t / DUR)
    tp = ph('twenty billion')
    headline(c, [[('LENT YOU:', False), ('$0.', True)]], 150, 520, 124, 1.0)
    k = pr(t, tp - 0.3, 0.5)
    if k > 0: headline(c, [[('PROFIT:', False), ('$20B+.', True)]], 150, 680, 124, k)
    card(c, 540, 1080, 1.25, -6 + 3 * math.sin(t * 2))
    for i in range(5):
        u = (t * 0.5 + i / 5) % 1; coin(c, 200 + i * 170, 860 + 300 * u, 30, (1 - u) * k)


def s_where(c, t):
    t0 = SCENES[1][0]
    pg(c, True, num=num(2), prog=t / DUR)
    headline(c, [[('SO WHERE', False)], [('DOES IT', False)], [('COME FROM?', True)]], 150, 520, 124, pr(t, t0 + 0.05, 0.5), dark=True)
    card(c, 540, 1130, 1.0, 0, sx=math.cos(t * 3))


def s_bank(c, t):
    t0 = SCENES[2][0]; tb = ph('your bank does')
    pg(c, False, num=num(3), prog=t / DUR)
    headline(c, [[('NOT FROM VISA.', False)], [('FROM YOUR', False), ('BANK.', True)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5))
    bank(c, 330, 1080, 1.0, 1.0, 'YOUR BANK')
    k = pr(t, tb - 0.2, 0.6)
    card(c, 330 + 410 * eo(k), 1000 - 60 * math.sin(eo(k) * math.pi), 0.8, -10 + 20 * eo(k))


def s_net(c, t):
    t0 = SCENES[3][0]; ts = ph("the store's")
    pg(c, True, num=num(4), prog=t / DUR)
    headline(c, [[('VISA = THE', False)], [('NETWORK', True), ('BETWEEN.', False)]], 150, 520, 116, pr(t, t0 + 0.05, 0.5), dark=True)
    road(c, 1100, t, True, booth=False)
    bank(c, 200, 1010, 0.55, 1.0); body(c, 'YOUR BANK', 110, 1240, 30, CREAM_T, 'Bold')
    k = pr(t, ts - 0.2, 0.4)
    if k > 0: bank(c, 880, 1010, 0.55, k); body(c, "STORE'S BANK", 770, 1240, 30, CREAM_T, 'Bold', a=k)
    for i in range(6):
        u = (t * 0.45 + i / 6) % 1; x = 320 + 440 * u
        c.drawCircle(x, 1100 + (i % 2) * 30 - 15, 12, P(ACC[0])); c.drawCircle(x, 1100 + (i % 2) * 30 - 15, 12, S(CREAM_T, 3))


def s_fees(c, t):
    t0 = SCENES[4][0]; t1 = ph('how much'); t2 = ph('every transaction')
    pg(c, False, num=num(5), prog=t / DUR)
    headline(c, [[('BANKS PAY', False)], [('SMALL', True), ('FEES.', False)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    road(c, 1150, t, False)
    for j, (lbl, ti) in enumerate((('% OF SPENDING', t1), ('PER SWIPE', t2))):
        k = pr(t, ti - 0.2, 0.4)
        if k > 0:
            c.save(); c.translate(260 + j * 560, 800); c.rotate(-6 + 12 * j); c.scale(eback(k), eback(k))
            f = font(36, 'Bold', False); w = f.measureText(lbl)
            r = rr(-w / 2 - 24, -40, w + 48, 70, 12); c.drawRRect(r, P(CREAM)); c.drawRRect(r, S(ACC[0], 6)); c.drawString(lbl, -w / 2, 10, f, P(ACC[0])); c.restore()
    for i in range(4):
        u = ((t - t0) * 0.7 + i / 4) % 1; coin(c, 300 + 240 * u, 900 - 90 * math.sin(u * math.pi) + 30, 22, pr(t, t0 + 0.6, 0.3) * (1 - u * 0.3))


def s_how(c, t):
    t0 = SCENES[5][0]
    pg(c, True, num=num(6), prog=t / DUR)
    headline(c, [[('SMALL FEES', False)], [('MAKE', False), ('$20B?', True)]], 150, 520, 140, pr(t, t0 + 0.05, 0.5), dark=True)
    for i in range(9):
        k = pr(t, t0 + 0.3 + i * 0.08, 0.3); coin(c, 300 + (i % 3) * 240, 1300 - (i // 3) * 76 - 120 * (1 - eo(k)), 44, k)


def s_count(c, t):
    t0 = SCENES[6][0]; tc = ph('two hundred')
    pg(c, False, num=num(7), prog=t / DUR)
    body(c, 'TRANSACTIONS PROCESSED, FY2025 (VISA 10-K)', 150, 520, 30, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    k = pr(t, tc - 0.2, 1.2)
    n = 257.5 * eo(k); s_ = '%.1f' % n
    if k > 0:
        c.drawString(s_, 140, 790, anton(260), P(INKE, k))
        headline(c, [[('BILLION', True), ('SWIPES.', False)]], 150, 930, 120, k)
    else: card(c, 540, 1000, 1.0, -4 + 3 * math.sin(t * 2))
    for r in range(4):
        for q in range(9):
            kk = pr(t, tc + (r * 9 + q) * 0.04, 0.2)
            if kk > 0: card(c, 190 + q * 88, 1080 + r * 70, 0.2, -8 + (q % 3) * 6)


def s_fx(c, t):
    t0 = SCENES[7][0]; te = ph('extra')
    pg(c, True, num=num(8), prog=t / DUR)
    headline(c, [[('PAYING IN', False)], [('ANOTHER', False), ('CURRENCY?', True)]], 150, 520, 104, pr(t, t0 + 0.05, 0.5), dark=True)
    k = pr(t, t0 + 0.3, 0.6)
    coin(c, 300, 960, 90, k, '$'); coin(c, 780, 960, 90, k, '€')
    for j in (0, 1):
        kk = pr(t, t0 + 0.6 + j * 0.3, 0.5); y = 900 + j * 120; d = 1 if j == 0 else -1
        x0, x1 = (420, 660) if j == 0 else (660, 420)
        c.drawLine(x0, y, x0 + (x1 - x0) * eo(kk), y, S(CREAM_T, 6, kk))
        if kk > 0.9: c.drawPath(path([(x1, y), (x1 - 26 * d, y - 18), (x1 - 26 * d, y + 18)]), P(CREAM_T))
    if t > te - 0.2:
        kk = pr(t, te - 0.2, 0.4); c.save(); c.translate(540, 1240); c.rotate(-6); c.scale(eback(kk), eback(kk))
        f = anton(90); s_ = '+ A CONVERSION FEE'; f = anton(64); w = f.measureText(s_)
        c.drawRect(skia.Rect.MakeXYWH(-w / 2 - 24, -60, w + 48, 90), P(ACC[0])); c.drawString(s_, -w / 2, 10, f, P(CREAM_T)); c.restore()


def s_end(c, t):
    t0 = SCENES[8][0]; ts = ph('it just')
    if t < ts - 0.3:
        pg(c, False, num=num(9), prog=t / DUR)
        headline(c, [[('NEVER LENDS', False)], [('YOU A', False), ('DOLLAR.', True)]], 150, 520, 128, pr(t, t0 + 0.05, 0.5))
        card(c, 540, 1060, 1.1, -4)
    else:
        page(c, False, label=LABEL, num=num(9), prog=t / DUR, fill=ACC[0])
        k = pr(t, ts - 0.3, 0.5); f = anton(124)
        for i, s_ in enumerate(('IT CHARGES A TOLL', 'ON THE ROAD YOUR', 'MONEY TRAVELS.')):
            kk = eo(cl(k * 1.6 - i * 0.2)); c.save(); c.translate(0, 40 * (1 - kk)); c.drawString(s_, 150, 580 + i * 136, f, P(CREAM_T if i < 2 else INKE, kk)); c.restore()
        road(c, 1260, t, False)
        for i in range(3):
            u = ((t - ts) * 0.4 + i / 3) % 1; card(c, -100 + 1280 * u, 1240, 0.28, 0)


SCENES = [(0.0, s_hook), (ph('so where') - 0.15, s_where), (ph("visa doesn't") - 0.15, s_bank), (ph('visa runs') - 0.15, s_net),
          (ph('and banks') - 0.15, s_fees), (ph('small fees how') - 0.15, s_how), (ph('processed') - 1.0, s_count),
          (ph('and when') - 0.15, s_fx), (ph('visa never') - 0.15, s_end)]
DARK_S = {1, 3, 5, 7}
SHAKES = [(ph('twenty billion'), 10, 0.35), (ph('your bank does'), 6, 0.25), (ph('two hundred'), 10, 0.35), (ph('it just'), 12, 0.4)]
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
    dark = i in DARK_S or (i == len(SCENES) - 1 and t >= ph('it just') - 0.3)
    if 0.2 < t < END + 0.1: esubs(c, T, t, dark, 1440)
    return s


def cover(out):
    s = skia.Surface(W, H); c = s.getCanvas()
    page(c, False, label='MONEY EXPLAINED', num='N° 01')
    headline(c, [[('NEVER LENDS.', False)], [('STILL MAKES', False)], [('$20B.', True)]], 150, 540, 140, 1.0, maxw=820)
    card(c, 540, 1160, 1.35, -6)
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
