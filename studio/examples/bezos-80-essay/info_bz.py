"""FOUNDER MINDSET (orange) N° 01: Bezos's regret minimization framework. ESSAY look. No likeness, no logos."""
import sys, os, math, subprocess
sys.path.insert(0, '/home/claude/studio')
from essay_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (232, 130, 20)
NS = 9
LABEL = 'FOUNDER MINDSET — N° 01'
WOOD = (176, 128, 84)
SAND = (226, 186, 110)
LEAF = (86, 130, 80)


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


def hourglass(c, x, y, s=1.0, u=0.5, rot=0.0, a=1.0):
    """u = share of sand already fallen (0..1)"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    shape(c, rr(-150, -250, 300, 36, 10), WOOD, 4, a); shape(c, rr(-150, 214, 300, 36, 10), WOOD, 4, a)
    for px in (-130, 130): shape(c, skia.Rect.MakeXYWH(px - 10, -214, 20, 428), WOOD, 3, a)
    glass = skia.Path(); glass.moveTo(-100, -214); glass.cubicTo(-100, -80, -14, -30, -14, 0); glass.cubicTo(-14, 30, -100, 80, -100, 214)
    glass.lineTo(100, 214); glass.cubicTo(100, 80, 14, 30, 14, 0); glass.cubicTo(14, -30, 100, -80, 100, -214); glass.close()
    c.drawPath(glass, P((246, 242, 232), a))
    c.save(); c.clipPath(glass, doAntiAlias=True)
    top_h = 170 * (1 - u); c.drawRect(skia.Rect.MakeXYWH(-120, -20 - top_h, 240, top_h), P(SAND, a))
    bot_h = 170 * u; c.drawPath(path([(-120, 214), (0, 214 - bot_h - 30 * u), (120, 214)]), P(SAND, a)); c.drawRect(skia.Rect.MakeXYWH(-120, 214 - bot_h * 0.6, 240, bot_h * 0.6), P(SAND, a))
    if 0.02 < u < 0.98: c.drawLine(0, 0, 0, 214 - bot_h, S(SAND, 5, a))
    c.restore()
    hatch(c, glass, 0.12 * a, 12); c.drawPath(glass, S(INKE, 4, a))
    c.drawLine(-60, -180, -40, -90, S(WHITE, 6, 0.6 * a))
    c.restore()


def briefcase(c, x, y, s=1.0, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-60, -150, 120, 50, 16), (90, 60, 40), 5, a); c.drawRRect(rr(-36, -130, 72, 30, 8), P(CREAM, a))
    b = rr(-180, -110, 360, 220, 20); shape(c, b, (120, 80, 52), 5, a); hatch(c, skia.Path.RRect(b), 0.2 * a, 10)
    c.drawLine(-180, -20, 180, -20, S(INKE, 4, a)); shape(c, rr(-24, -36, 48, 34, 6), GOLDC, 3, a)
    c.restore()


GOLDC = (222, 176, 60)


def envelope(c, x, y, s=1.0, rot=0.0, a=1.0, txt='BONUS'):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    e = skia.Rect.MakeXYWH(-130, -80, 260, 160); shape(c, e, (246, 240, 230), 4, a)
    c.drawPath(path([(-130, -80), (0, 10), (130, -80)]), S(INKE, 4, a))
    f = anton(46); c.drawString(txt, -f.measureText(txt) / 2, 60, f, P(ACC[0], a))
    c.restore()


def tree(c, x, y, s=1.0, sway=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, skia.Rect.MakeXYWH(-14, -20, 28, 120), WOOD, 3)
    c.rotate(sway)
    for (dx, dy, r) in ((0, -120, 90), (-60, -70, 64), (60, -70, 64)):
        c.drawCircle(dx, dy, r, P(LEAF)); c.drawCircle(dx, dy, r, S(INKE, 4))
    cl_ = skia.Path(); cl_.addCircle(0, -120, 90); hatch(c, cl_, 0.3, 9)
    c.restore()


def chair(c, x, y, s=1.0, rock=0.0, a=1.0):
    c.save(); c.translate(x, y); c.rotate(rock); c.scale(s, s)
    c.drawArc(skia.Rect.MakeXYWH(-200, 40, 400, 120), 20, 140, False, S(INKE, 8, a))
    for lx in (-110, 110): c.drawLine(lx, 120, lx * 0.9, -10, S(WOOD, 14, a)); c.drawLine(lx, 120, lx * 0.9, -10, S(INKE, 3, a))
    shape(c, rr(-130, -30, 260, 30, 8), WOOD, 4, a)
    shape(c, rr(-120, -300, 240, 280, 16), WOOD, 4, a)
    for i in range(4): c.drawLine(-80 + i * 53, -270, -80 + i * 53, -50, S(INKE, 3, 0.6 * a))
    c.restore()


def scale_(c, x, y, s=1.0, tilt=0.0, lt='', rt=''):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, path([(-60, 200), (60, 200), (14, 0), (-14, 0)]), WOOD, 4)
    c.save(); c.rotate(tilt)
    shape(c, rr(-260, -14, 520, 22, 8), WOOD, 4)
    for sx, t_ in ((-240, lt), (240, rt)):
        c.save(); c.translate(sx, 0); c.rotate(-tilt)
        c.drawLine(-60, 120, 0, 0, S(INKE, 3)); c.drawLine(60, 120, 0, 0, S(INKE, 3))
        shape(c, path([(-90, 120), (90, 120), (60, 160), (-60, 160)]), (236, 226, 206), 4)
        f = font(30, 'Bold', False); c.drawString(t_, -f.measureText(t_) / 2, 106, f, P(INKE)); c.restore()
    c.restore(); c.restore()


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    pg(c, False, num=num(1), prog=t / DUR)
    headline(c, [[('HE PICTURED', False)], [('HIMSELF', False), ('AT 80.', True)]], 150, 520, 128, 1.0)
    hourglass(c, 540, 1070, 1.05, cl(0.15 + t / 6), 0.03 * math.sin(t * 1.6))


def s_trick(c, t):
    t0 = SCENES[1][0]
    pg(c, True, num=num(2), prog=t / DUR)
    headline(c, [[('ONE QUESTION.', False)], [('HARD CALL', False), ('MADE EASY.', True)]], 150, 520, 112, pr(t, t0 + 0.05, 0.5), dark=True)
    k = pr(t, ph('easy') - 0.2, 0.5)
    c.save(); c.translate(540, 1060); c.scale(eback(k) if k > 0 else 0.001, eback(k) if k > 0 else 0.001)
    c.drawCircle(0, 0, 170, P(ACC[0])); c.drawCircle(0, 0, 170, S(CREAM_T, 6)); f = anton(260); c.drawString('?', -f.measureText('?') / 2, 92, f, P(CREAM_T)); c.restore()


def s_job(c, t):
    t0 = SCENES[2][0]; tb = ph('bonus')
    pg(c, False, num=num(3), prog=t / DUR)
    headline(c, [[('GREAT JOB.', False)], [('MIDYEAR', False), ('BONUS.', True)]], 150, 520, 128, pr(t, t0 + 0.05, 0.5))
    briefcase(c, 360, 1060, 1.0)
    k = pr(t, tb - 0.3, 0.5)
    envelope(c, 760 + 120 * eo(pr(t, tb + 0.3, 0.8)), 960 - 40 * eo(k), 0.9, 8 + 20 * eo(pr(t, tb + 0.3, 0.8)), a=k * (1 - 0.6 * pr(t, tb + 0.3, 0.8)))
    if t > tb + 0.2:
        kk = pr(t, tb + 0.2, 0.3); c.drawLine(640, 880, 640 + 260 * kk, 880 + 180 * kk, S(ACC[0], 12))


def s_walk(c, t):
    t0 = SCENES[3][0]; td = ph('two more')
    pg(c, True, num=num(4), prog=t / DUR)
    headline(c, [[('A TWO-HOUR', False)], [('WALK IN', False), ('THE PARK.', True)]], 150, 520, 116, pr(t, t0 + 0.05, 0.5), dark=True)
    p = skia.Path(); p.moveTo(140, 1330); p.cubicTo(400, 1250, 300, 1050, 560, 1000); p.cubicTo(800, 960, 760, 850, 940, 820)
    c.drawPath(p, S((120, 110, 98), 50)); c.drawPath(p, S(CREAM_T, 3, 0.4))
    for (x, y, s_) in ((220, 1100, 0.8), (820, 1150, 0.9), (420, 880, 0.6), (930, 980, 0.6)): tree(c, x, y, s_, 2 * math.sin(t * 1.5 + x))
    m = skia.PathMeasure(p, False); L = m.getLength(); k = pr(t, t0 + 0.2, 4.0)
    for i in range(int(14 * k)):
        pos, tan = m.getPosTan(L * i / 14)
        c.drawOval(skia.Rect.MakeXYWH(pos.x() - 7 + (8 if i % 2 else -8), pos.y() - 10, 14, 20), P(CREAM_T, 0.9))
    if t > td - 0.3:
        kk = pr(t, td - 0.3, 0.4); c.save(); c.translate(720, 1260); c.rotate(-6); c.scale(eback(kk), eback(kk))
        r = rr(-220, -55, 440, 110, 14); c.drawRRect(r, P(ACC[0])); f = anton(70); s_ = 'THINK 48 HRS'
        c.drawString(s_, -f.measureText(s_) / 2, 26, f, P(CREAM_T)); c.restore()


def s_how(c, t):
    t0 = SCENES[4][0]
    pg(c, False, num=num(5), prog=t / DUR)
    headline(c, [[('SO HOW DID', False)], [('HE', False), ('DECIDE?', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    scale_(c, 540, 1000, 1.0, 8 * math.sin(t * 2.5), 'STAY', 'LEAP')


def s_frame(c, t):
    t0 = SCENES[5][0]
    pg(c, True, num=num(6), prog=t / DUR)
    body(c, 'HIS NAME FOR IT', 150, 520, 32, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    headline(c, [[('REGRET', True)], [('MINIMIZATION', False)], [('FRAMEWORK.', False)]], 150, 680, 128, pr(t, t0 + 0.1, 0.6), dark=True)
    k = pr(t, t0 + 0.6, 0.6)
    for i in range(3):
        c.drawRect(skia.Rect.MakeXYWH(150 + i * 260, 1120, 220 * eo(k), 14), P(ACC[0] if i == 0 else CREAM_T, 0.9))


def s_eighty(c, t):
    t0 = SCENES[6][0]; tr = ph('which choice')
    pg(c, False, num=num(7), prog=t / DUR)
    headline(c, [[('AGE 80.', False)], [('LOOKING', False), ('BACK.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    chair(c, 330, 1180, 0.75, 0.06 * math.sin(t * 2.2))
    hourglass(c, 790, 1090, 0.6, 0.95)
    if t > tr - 0.3:
        kk = pr(t, tr - 0.3, 0.4); c.save(); c.translate(560, 820); c.rotate(-5); c.scale(eback(kk), eback(kk))
        r = rr(-250, -50, 500, 100, 14); c.drawRRect(r, P(CREAM)); c.drawRRect(r, S(ACC[0], 7)); f = anton(60); s_ = 'WHAT WOULD I REGRET?'
        c.drawString(s_, -f.measureText(s_) / 2, 22, f, P(ACC[0])); c.restore()


def s_quote(c, t):
    t0 = SCENES[7][0]; tq = ph('in his words')
    pg(c, True, num=num(8), prog=t / DUR)
    if t < tq - 0.2:
        headline(c, [[('FAILING?', False)], [('NOT THE', False), ('SCARY PART.', True)]], 150, 520, 120, pr(t, t0 + 0.05, 0.5), dark=True)
    else:
        k = pr(t, tq - 0.2, 0.5)
        c.drawRect(skia.Rect.MakeXYWH(150, 520, 70, 70), P(ACC[0], k)); c.drawRect(skia.Rect.MakeXYWH(240, 520, 70, 70), P(ACC[0], k))
        f = font(78, 'Bold', False)
        for i, s_ in enumerate(('"The one thing', 'I might regret is', 'not ever having', 'tried."')):
            kk = eo(cl(k * 1.5 - i * 0.18)); c.drawString(s_, 150, 720 + i * 100, f, P(CREAM_T, kk))
        c.drawLine(150, 1150, 200, 1150, S(ACC[0], 4)); body(c, 'JEFF BEZOS, ACADEMY OF ACHIEVEMENT', 220, 1162, 28, MUTE, 'SemiBold', a=k)


def s_end(c, t):
    t0 = SCENES[8][0]; ts = ph('safe') + 0.35
    if t < ts - 0.3:
        pg(c, False, num=num(9), prog=t / DUR)
        headline(c, [[("DON'T ASK", False)], [("WHAT'S", False), ('SAFE.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
        hourglass(c, 540, 1080, 0.9, 0.5, 0.03 * math.sin(t * 2))
    else:
        page(c, False, label=LABEL, num=num(9), prog=t / DUR, fill=ACC[0])
        k = pr(t, ts - 0.3, 0.5); f = anton(124)
        for i, s_ in enumerate(('ASK WHAT', '80-YEAR-OLD YOU', 'WOULD REGRET.')):
            kk = eo(cl(k * 1.6 - i * 0.2)); c.save(); c.translate(0, 40 * (1 - kk)); c.drawString(s_, 150, 580 + i * 136, f, P(CREAM_T if i < 2 else INKE, kk)); c.restore()
        hourglass(c, 540, 1130, 0.7, cl((t - ts) / 3), 0.0)


SCENES = [(0.0, s_hook), (ph('and that one') - 0.15, s_trick), (ph('he had a') - 0.15, s_job), (ph('his boss') - 0.15, s_walk),
          (ph('so how did') - 0.15, s_how), (ph('he called') - 0.15, s_frame), (ph('picture yourself') - 0.15, s_eighty),
          (ph('for him') - 0.15, s_quote), (ph('so next time') - 0.15, s_end)]
DARK_S = {1, 3, 5, 7}
SHAKES = [(ph('easy'), 8, 0.3), (ph('bonus'), 8, 0.3), (ph('regret minimization'), 10, 0.35), (ph('in his words'), 6, 0.25), (ph('safe') + 0.35, 12, 0.4)]
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
    dark = i in DARK_S or (i == len(SCENES) - 1 and t >= ph('safe') + 0.05)
    if 0.2 < t < END + 0.1: esubs(c, T, t, dark, 1440)
    return s


def cover(out):
    s = skia.Surface(W, H); c = s.getCanvas()
    page(c, False, label='FOUNDER MINDSET', num='N° 01')
    headline(c, [[('THE AGE-80', False)], [('TEST.', True)]], 150, 540, 170, 1.0, maxw=820)
    hourglass(c, 540, 1150, 1.0, 0.6)
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
