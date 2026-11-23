"""Rolex is owned by a charitable foundation. INFOGRAPHIC paper look, no mascot.
No trade dress: generic gold dress watch (no crown, no fluted bezel, no magnifier, no bracelet pattern); names as plain text."""
import sys, os, math, subprocess
sys.path.insert(0, '/home/claude/studio')
from info_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
GOLD2 = (232, 190, 90)


def watch(c, x, y, s=1.0, t=0.0, heart=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for sy in (-1, 1):   # plain leather strap
        shape(c, rr(-62, sy * 130 - (90 if sy < 0 else 0), 124, 90, 14), (110, 70, 50), 4)
    c.drawCircle(0, 0, 150, P(YEL)); c.drawCircle(0, 0, 150, S(INK, 6)); c.drawCircle(0, 0, 124, P(WHITE)); c.drawCircle(0, 0, 124, S(INK, 4))
    shape(c, rr(146, -18, 24, 36, 6), YEL, 3)
    for i in range(12):
        a = i * math.pi / 6; r0 = 100 if i % 3 else 92
        c.drawLine(r0 * math.sin(a), -r0 * math.cos(a), 112 * math.sin(a), -112 * math.cos(a), S(INK, 5 if i % 3 == 0 else 3))
    ah = t * 0.3; am = t * 2.0
    c.drawLine(0, 0, 55 * math.sin(ah + 1.0), -55 * math.cos(ah + 1.0), S(INK, 8)); c.drawLine(0, 0, 88 * math.sin(am), -88 * math.cos(am), S(INK, 5))
    c.drawCircle(0, 0, 9, P(RED))
    if heart > 0:
        k = eback(cl(heart)); c.save(); c.translate(0, 40); c.scale(k * 0.9, k * 0.9)
        p = skia.Path(); p.moveTo(0, 30); p.cubicTo(-60, -10, -40, -60, 0, -30); p.cubicTo(40, -60, 60, -10, 0, 30); p.close(); shape(c, p, RED, 3); c.restore()
    c.restore()


def ticker(c, x, y, w, k, t):
    card(c, x, y, w, 170, NAVY, 20)
    text(c, 'STOCK', x + w / 2, y + 60, 38, WHITE, 'Bold')
    p = skia.Path(); p.moveTo(x + 30, y + 130)
    for i in range(1, 9): p.lineTo(x + 30 + i * (w - 60) / 8, y + 130 - 50 * math.sin(i * 1.3 + t) * 0.5 - i * 4)
    c.drawPath(p, S(YEL, 5))


def frame_portrait(c, x, y, w, h):
    shape(c, rr(x, y, w, h, 10), YEL, 5); shape(c, rr(x + 18, y + 18, w - 36, h - 36, 6), WHITE, 3)
    for i, (px, sc) in enumerate(((0.3, 1.0), (0.55, 0.9), (0.75, 0.7))):
        cx = x + w * px; cy = y + h * 0.48
        c.drawCircle(cx, cy - 30 * sc, 22 * sc, P(BLUE)); c.drawCircle(cx, cy - 30 * sc, 22 * sc, S(INK, 3))
        shape(c, rr(cx - 28 * sc, cy - 4 * sc, 56 * sc, 70 * sc, 18 * sc), BLUE, 3)
    text(c, 'FAMILY', x + w / 2, y + h - 34, 30, INK, 'Bold')


def building(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, path([(-140, -160), (0, -240), (140, -160)]), WHITE, 5)
    shape(c, skia.Rect.MakeXYWH(-130, -160, 260, 160), WHITE, 5)
    for i in range(4): shape(c, rr(-105 + i * 60, -130, 36, 110, 4), CARD_SKY, 3)
    p = skia.Path(); p.moveTo(0, -178); p.cubicTo(-16, -196, -12, -212, 0, -204); p.cubicTo(12, -212, 16, -196, 0, -178); p.close(); shape(c, p, RED, 2)
    c.restore()


def scroll(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-90, -110, 180, 220, 10), WHITE, 4)
    for i in range(5): c.drawLine(-60, -70 + i * 30, 60 - (30 if i == 4 else 0), -70 + i * 30, S(INK, 3, 0.6))
    c.drawCircle(40, 80, 22, P(RED)); c.drawCircle(40, 80, 22, S(INK, 3)); c.restore()


def flower(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawLine(0, 0, 0, 120, S((96, 116, 64), 7))
    for i in range(6):
        a = i * math.pi / 3; c.drawCircle(28 * math.cos(a), 28 * math.sin(a), 22, P(WHITE)); c.drawCircle(28 * math.cos(a), 28 * math.sin(a), 22, S(INK, 3))
    c.drawCircle(0, 0, 18, P(YEL)); c.drawCircle(0, 0, 18, S(INK, 3)); c.restore()


def cap(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, path([(-70, -10), (0, -45), (70, -10), (0, 25)]), NAVY, 4); shape(c, rr(-36, 4, 72, 34, 8), NAVY, 4)
    c.drawLine(60, -6, 60, 40, S(YEL, 5)); c.drawCircle(60, 44, 8, P(YEL)); c.restore()


def palette(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.addOval(skia.Rect.MakeXYWH(-70, -50, 140, 100)); shape(c, p, (226, 196, 150), 4)
    for i, col in enumerate((RED, YEL, BLUE, (96, 116, 64))): c.drawCircle(-38 + i * 24, -18 + (i % 2) * 14, 11, P(col)); c.drawCircle(-38 + i * 24, -18 + (i % 2) * 14, 11, S(INK, 2))
    c.drawCircle(30, 22, 14, P(BG)); c.drawCircle(30, 22, 14, S(INK, 3)); c.restore()


def hands(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, 26); p.cubicTo(-46, -6, -30, -46, 0, -24); p.cubicTo(30, -46, 46, -6, 0, 26); p.close(); shape(c, p, RED, 3)
    shape(c, path([(-80, 60), (-20, 40), (20, 40), (80, 60), (60, 80), (-60, 80)]), (226, 196, 150), 4); c.restore()


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tn = ph("can't buy"); tf = ph('no owning')
    title(c, t + 1.0, ['Who owns', 'Rolex?'])
    sky_card(c, 70, 500, 940, 830, 51)
    watch(c, 540, 860, 1.15, t)
    chip(c, '~CHF 11B sales, 2025 est.', 540, 1150, WHITE, 34)
    if t > tn - 0.2:
        pop(c, pr(t, tn - 0.2, 0.4), 820, 640, lambda: (ticker(c, 700, 560, 250, 1, t), check(c, 935, 570, 34, False, 1)))
    if t > tf - 0.2:
        pop(c, pr(t, tf - 0.2, 0.4), 250, 650, lambda: (frame_portrait(c, 130, 540, 240, 220), check(c, 360, 552, 34, False, 1)))


def s_who(c, t):
    t0 = SCENES[1][0]; tw = ph('lost his wife'); tn = ph('next year'); td = ph('when he died')
    title(c, t - t0, ['The story', 'behind it'])
    card(c, 70, 500, 940, 830, CARD_SKY)
    c.drawLine(150, 1150, 930, 1150, S(INK, 4))
    steps = [(220, '1944', 'His wife dies', pr(t, ph('in nineteen') - 0.1, 0.4), lambda x: flower(c, x, 860, 1.3)),
             (540, '1945', 'Foundation set up', pr(t, tn - 0.2, 0.4), lambda x: building(c, x, 1000, 0.85)),
             (860, '1960', 'Shares left to it', pr(t, td - 0.2, 0.4), lambda x: scroll(c, x, 900, 1.0))]
    for x, yr, lab, k, draw in steps:
        if k <= 0: continue
        def d(x=x, yr=yr, lab=lab, draw=draw):
            draw(x); c.drawCircle(x, 1150, 16, P(RED)); c.drawCircle(x, 1150, 16, S(INK, 3))
            text(c, yr, x, 1215, 52, INK, 'Black'); text(c, lab, x, 1262, 30, GREY, 'Medium', maxw=290)
        pop(c, k, x, 1000, d)
    text(c, 'Hans Wilsdorf, founder', 540, 590, 38, INK, 'SemiBold', a=pr(t, t0 + 0.3, 0.4))


def s_funds(c, t):
    t0 = SCENES[2][0]; ts = ph('scholarships'); ta = ph('the arts'); tp = ph('people in need')
    title(c, t - t0, ['What the', 'foundation funds'])
    card(c, 70, 500, 940, 830, CARD_SKY)
    building(c, 540, 820, 0.95)
    items = [(220, 'Scholarships', ts, lambda x, y: cap(c, x, y, 1.0)), (540, 'The arts', ta, lambda x, y: palette(c, x, y, 1.0)), (860, 'People in need', tp, lambda x, y: hands(c, x, y - 10, 0.95))]
    for x, lab, tt, ic in items:
        k = pr(t, tt - 0.2, 0.4)
        if k > 0:
            pop(c, k, x, 1060, lambda x=x, lab=lab, ic=ic: (card(c, x - 140, 930, 280, 290, WHITE, 26), ic(x, 1040), text(c, lab, x, 1180, 34, INK, 'Bold', maxw=250)))
            arrow(c, 540, 840, x, 920, k, RED, 5, 0.0 if x == 540 else (0.1 if x < 540 else -0.1))


def s_end(c, t):
    t0 = SCENES[3][0]; tb = ph('billionaire'); tc = ph("it's a charity")
    title(c, t - t0, ["Owner? Not a", 'billionaire.'] if t < tc - 0.2 else ['Owner?', 'A charity.'])
    sky_card(c, 70, 500, 940, 830, 61)
    watch(c, 540, 870, 1.15, t, pr(t, tc - 0.1, 0.4))
    if t > tb - 0.2: check(c, 830, 640, 44, False, pr(t, tb - 0.2, 0.3))
    if t > tc - 0.1: check(c, 830, 640, 44, True, pr(t, tc - 0.1, 0.3))


SCENES = [(0.0, s_hook), (ph('so who actually') - 0.15, s_who), (ph('so what does') - 0.15, s_funds), (ph('so the owner') - 0.15, s_end)]
SHAKES = [(ph("can't buy"), 8, 0.3), (ph('all his rolex'), 10, 0.35), (ph("it's a charity"), 12, 0.4)]
TR = 0.32


def page(c, t): paper(c)
def draw_scene(c, i, t): page(c, t); SCENES[i][1](c, t)


def frame(t):
    s = skia.Surface(W, H); c = s.getCanvas(); sx = sy = 0.0
    for (ts, a, d) in SHAKES:
        if ts <= t < ts + d: k = 1 - (t - ts) / d; sx += a * k * math.sin(t * 90); sy += a * k * math.cos(t * 77)
    c.save(); c.translate(sx, sy)
    i = max(j for j, (t0, _) in enumerate(SCENES) if t >= t0)
    draw_scene(c, i, t)
    if i > 0 and t < SCENES[i][0] + TR:
        k = eio((t - SCENES[i][0]) / TR); c.save(); c.translate(-W * k, 0); draw_scene(c, i - 1, t); c.restore()
        c.drawRect(skia.Rect.MakeXYWH(W * (1 - k) - 5, 0, 10, H), P(INK, 0.15))
    c.restore()
    if 0.2 < t < END + 0.1: subs(c, T, t, 1440)
    return s


def cover(out):
    s = skia.Surface(W, H); c = s.getCanvas(); page(c, 0)
    chip(c, 'oops, my business', 540, 300, YEL, 32)
    text(c, 'Who owns', 540, 460, 136, INK, 'Black'); f = font(140, 'Medium', italic=True); s_ = 'Rolex?'; c.drawString(s_, 540 - f.measureText(s_) / 2, 610, f, P(RED))
    sky_card(c, 70, 690, 940, 750, 51)
    watch(c, 540, 1000, 1.25, 0.6)
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
