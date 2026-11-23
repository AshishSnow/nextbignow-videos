"""CASE STUDY (red): Huy Fong Foods sriracha — no ads, one farm. ESSAY look.
No trade dress: generic squeeze bottle with WHITE cap and plain 'HOT SAUCE' label (no rooster, no green cap); names as plain text."""
import sys, os, math, subprocess
sys.path.insert(0, '/home/claude/studio')
from essay_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (214, 52, 44)
NS = 8
SAUCE = (196, 40, 30)


def num(i): return '%02d / %02d' % (i, NS)
def pg(c, *a, **k): page(c, *a, label='CASE STUDY — N° 01', **k)


def shape(c, sh, fill, ow=4):
    if isinstance(sh, skia.Rect): c.drawRect(sh, P(fill)); c.drawRect(sh, S(INKE, ow))
    elif isinstance(sh, skia.RRect): c.drawRRect(sh, P(fill)); c.drawRRect(sh, S(INKE, ow))
    else: c.drawPath(sh, P(fill)); c.drawPath(sh, S(INKE, ow))


def hatch(c, clip, a=0.35, step=9, ang=1):
    c.save(); c.clipPath(clip, doAntiAlias=True); b = clip.getBounds()
    for i in range(int(b.left()) - 500, int(b.right()) + 500, step): c.drawLine(i, b.bottom(), i + 250 * ang, b.top(), S(INKE, 1.3, a))
    c.restore()


def bottle(c, x, y, s=1.0, rot=0.0, level=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-120, 250, 240, 30), P(INKE, 0.18))
    body = skia.Path(); body.moveTo(-80, -120); body.cubicTo(-110, -60, -110, 220, -90, 260); body.lineTo(90, 260); body.cubicTo(110, 220, 110, -60, 80, -120); body.close()
    c.drawPath(body, P((246, 240, 230)))
    c.save(); c.clipPath(body, doAntiAlias=True); top = 260 - 380 * level
    c.drawRect(skia.Rect.MakeXYWH(-120, top, 240, 400), P(SAUCE)); c.restore()
    hatch(c, body, 0.22, 10)
    c.drawPath(body, S(INKE, 4))
    shape(c, rr(-50, -190, 100, 76, 10), (246, 244, 238), 4)
    shape(c, path([(-20, -190), (20, -190), (8, -250), (-8, -250)]), (246, 244, 238), 4)
    shape(c, rr(-70, 20, 140, 120, 8), (246, 240, 230), 3)
    f = anton(34); s1 = 'HOT'; s2 = 'SAUCE'; c.drawString(s1, -f.measureText(s1) / 2, 70, f, P(INKE)); c.drawString(s2, -f.measureText(s2) / 2, 112, f, P(INKE))
    c.drawLine(-40, -90, -46, 220, S(WHITE, 8, 0.5))
    c.restore()


def chili(c, x, y, s=1.0, rot=0.0, a=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.moveTo(-60, -10); p.cubicTo(-30, -30, 40, -20, 70, 30); p.cubicTo(76, 40, 64, 44, 56, 36); p.cubicTo(20, 10, -30, 16, -60, 12); p.close()
    c.drawPath(p, P(SAUCE, a)); c.drawPath(p, S(INKE, 3, a))
    st = skia.Path(); st.moveTo(-60, 0); st.cubicTo(-74, -6, -80, -22, -76, -34); c.drawPath(st, S((60, 110, 60), 6, a)); c.restore()


def ship(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y + 6 * math.sin(t * 2)); c.scale(s, s)
    hull = path([(-260, -20), (260, -20), (210, 70), (-230, 70)]); shape(c, hull, (70, 66, 62)); hatch(c, hull, 0.3)
    shape(c, skia.Rect.MakeXYWH(-180, -90, 120, 70), (236, 230, 216)); shape(c, skia.Rect.MakeXYWH(-40, -70, 240, 50), (180, 70, 50))
    shape(c, skia.Rect.MakeXYWH(-150, -150, 30, 60), (60, 56, 52))
    for i in range(4): c.drawRect(skia.Rect.MakeXYWH(-30 + i * 55, -62, 40, 34), S(INKE, 2))
    c.restore()
    for i in range(6):
        wx = x - 330 + i * 120; c.drawArc(skia.Rect.MakeXYWH(wx, y + 64 * s, 120, 30), 180, 180, False, S(INKE, 3, 0.6))


def barn(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, skia.Rect.MakeXYWH(-150, -140, 300, 200), (178, 60, 46)); hatch(c, skia.Path.Rect(skia.Rect.MakeXYWH(-150, -140, 300, 200)), 0.25)
    shape(c, path([(-170, -140), (0, -250), (170, -140)]), (120, 44, 36))
    shape(c, skia.Rect.MakeXYWH(-50, -40, 100, 100), (236, 230, 216)); c.drawLine(-50, -40, 50, 60, S(INKE, 4)); c.drawLine(50, -40, -50, 60, S(INKE, 4))
    c.restore()
    for r in range(2):
        for i in range(5): chili(c, x - 260 + i * 130, y + 110 + r * 60, 0.5, 0.3 * ((i + r) % 2))


def gavel(c, x, y, s=1.0, k=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-150, 120, 300, 50, 10), (120, 84, 60))
    c.save(); c.rotate(-30 + 30 * eo(k))
    shape(c, rr(-20, -40, 260, 34, 10), (150, 104, 70)); shape(c, rr(-110, -100, 110, 150, 18), (120, 84, 60))
    c.restore(); c.restore()


def shelf(c, y, empty=1.0):
    c.drawRect(skia.Rect.MakeXYWH(120, y, 840, 26), P((150, 120, 90))); c.drawRect(skia.Rect.MakeXYWH(120, y, 840, 26), S(INKE, 3))
    for i in range(5):
        if i == 2: bottle(c, 540, y - 150, 0.55)
        else: c.drawRect(skia.Rect.MakeXYWH(150 + i * 165, y - 230, 110, 230), S(INKE, 2, 0.35 * empty))


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    pg(c, False, num=num(1), prog=t / DUR)
    headline(c, [[('$0 ON ADS.', False)], [('STILL', False), ('EVERYWHERE.', True)]], 150, 520, 128, 1.0)
    bottle(c, 540, 1060, 1.0, 0.04 * math.sin(t * 2))
    for i, (x, y) in enumerate(((210, 880), (870, 900))):   # crossed-out ad icons
        c.save(); c.translate(x, y)
        shape(c, rr(-70, -50, 140, 100, 10), (236, 230, 216)); f = font(26, 'Bold', False); s_ = ['TV AD', 'BILLBOARD'][i]; c.drawString(s_, -f.measureText(s_) / 2, 10, f, P(INKE))
        k = pr(t, 0.4 + i * 0.25, 0.3); c.drawLine(-80, -60, -80 + 160 * k, -60 + 120 * k, S(ACC[0], 9)); c.restore()


def s_bet(c, t):
    t0 = SCENES[1][0]
    pg(c, True, num=num(2), prog=t / DUR)
    headline(c, [[('ONE BIG BET.', False)], [('ONE', False), ('FARM.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    pop(c, pr(t, t0 + 0.3, 0.5), 540, 1050, lambda: barn(c, 540, 1080, 1.1))


def s_story(c, t):
    t0 = SCENES[2][0]; tn = ph('named it'); tl = ph('his line')
    pg(c, False, num=num(3), prog=t / DUR)
    if t < tl - 0.3:
        headline(c, [[('1980.', True), ("LA'S CHINATOWN.", False)]], 150, 520, 100, pr(t, t0 + 0.05, 0.5))
        body(c, 'David Tran starts Huy Fong Foods', 150, 620, 40, INKE, 'SemiBold', a=pr(t, t0 + 0.4, 0.4))
        k = pr(t, tn - 0.2, 0.5)
        if k > 0:
            pop(c, k, 540, 1000, lambda: ship(c, 540 - 300 * (1 - eo(k)), 1000, 1.2, t))
            chip_ = 'named after this freighter'; body(c, chip_, 150, 1240, 38, ACC[0], 'Bold', a=k)
        else: bottle(c, 540, 1050, 0.9)
    else:
        k = pr(t, tl - 0.3, 0.5)
        c.drawRect(skia.Rect.MakeXYWH(150, 640, 70, 70), P(ACC[0], k)); c.drawRect(skia.Rect.MakeXYWH(240, 640, 70, 70), P(ACC[0], k))
        f = font(76, 'Bold', False)
        for i, s_ in enumerate(('"Rich man\'s sauce', 'at a poor man\'s', 'price."')):
            kk = eo(cl(k * 1.5 - i * 0.2)); c.drawString(s_, 150, 830 + i * 96, f, P(INKE, kk))
        c.drawLine(150, 1120, 200, 1120, S(ACC[0], 4)); body(c, "DAVID TRAN'S MOTTO", 220, 1132, 28, MUTE, 'SemiBold', a=k)


def s_bottles(c, t):
    t0 = SCENES[3][0]; tz = ph('zero ads')
    pg(c, True, num=num(4), prog=t / DUR)
    body(c, 'BY 2012, PER THE COMPANY', 150, 520, 32, MUTE, 'SemiBold', a=pr(t, t0, 0.4))
    k = pr(t, ph('twenty million') - 0.2, 0.6)
    f = anton(190); n = int(20000000 * eo(k)); s_ = '{:,}'.format(n)
    c.drawString(s_, 150, 760, f if f.measureText(s_) < 800 else anton(190 * 780 / f.measureText(s_)), P(CREAM_T, max(0.15, k)))
    headline(c, [[('BOTTLES A', False), ('YEAR.', True)]], 150, 880, 100, k, dark=True)
    for i in range(7):
        if k > i / 7: bottle(c, 190 + i * 118, 1220, 0.36)
    if t > tz - 0.2:
        kk = pr(t, tz - 0.2, 0.35); c.save(); c.translate(820, 560); c.rotate(-10); c.scale(eback(kk), eback(kk))
        r = rr(-150, -60, 300, 120, 14); c.drawRRect(r, S(ACC[0], 8)); f2 = anton(80); c.drawString('ADS: $0', -f2.measureText('ADS: $0') / 2, 28, f2, P(ACC[0])); c.restore()


def s_wrong(c, t):
    t0 = SCENES[4][0]; ty = ph('twenty eight')
    pg(c, False, num=num(5), prog=t / DUR)
    headline(c, [[('SO WHAT WENT', False)], [('WRONG?', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5))
    k = pr(t, ty - 0.2, 0.5)
    if k > 0:
        pop(c, k, 300, 1050, lambda: barn(c, 300, 1050, 0.75))
        bottle(c, 820, 1060, 0.7)
        for i in range(4):
            u = (t * 0.6 + i / 4) % 1; chili(c, 430 + 260 * u, 980 - 40 * math.sin(u * math.pi), 0.6, 0.3)
        body(c, '28 years. One farm.', 150, 1290, 48, INKE, 'Bold', a=k)


def s_court(c, t):
    t0 = SCENES[5][0]; tm = ph('twenty three')
    pg(c, True, num=num(6), prog=t / DUR)
    headline(c, [[('THEN THEY', False), ('SPLIT.', True)]], 150, 520, 132, pr(t, t0 + 0.05, 0.5), dark=True)
    gavel(c, 540, 900, 1.1, pr(t, ph('a court') - 0.1, 0.25))
    if t > tm - 0.3:
        k = pr(t, tm - 0.3, 0.4)
        c.drawString('$23M+', 150, 1300, anton(150), P(ACC[0], k)); body(c, 'court-ordered, paid to the farm', 560, 1270, 34, CREAM_T, 'SemiBold', a=k)


def s_short(c, t):
    t0 = SCENES[6][0]; te = ph('seventy dollars')
    pg(c, False, num=num(7), prog=t / DUR)
    headline(c, [[('THEN CAME THE', False)], [('SHORTAGE.', True)]], 150, 520, 128, pr(t, t0 + 0.05, 0.5))
    shelf(c, 1150)
    for i in range(5): chili(c, 200 + i * 170, 760, 0.7, 0.4, a=0.25)
    if t > te - 0.3:
        k = pr(t, te - 0.3, 0.4); c.save(); c.translate(760, 940); c.rotate(-8); c.scale(eback(k), eback(k))
        shape(c, path([(-30, -60), (190, -60), (190, 60), (-30, 60), (-80, 0)]), (255, 214, 40), 4)
        f = anton(84); c.drawString('$70', 80 - f.measureText('$70') / 2, 30, f, P(INKE)); c.restore()
        body(c, 'one big bottle, on eBay', 560, 1060, 32, INKE, 'SemiBold', a=k)


def s_end(c, t):
    t0 = SCENES[7][0]; ts = ph('one supplier')
    if t < ts - 0.3:
        pg(c, False, num=num(8), prog=t / DUR)
        headline(c, [[('FREE ADS CAN', False)], [('BUILD A', False), ('BRAND.', True)]], 150, 520, 128, pr(t, t0 + 0.05, 0.5))
        bottle(c, 540, 1060, 1.0)
    else:
        page(c, False, label='CASE STUDY — N° 01', num=num(8), prog=t / DUR, fill=ACC[0])
        k = pr(t, ts - 0.3, 0.5); f = anton(140)
        for i, s_ in enumerate(('ONE SUPPLIER', 'CAN SHAKE IT.')):
            kk = eo(cl(k * 1.6 - i * 0.2)); c.save(); c.translate(0, 40 * (1 - kk)); c.drawString(s_, 150, 580 + i * 150, f, P(CREAM_T if i == 0 else INKE, kk)); c.restore()
        bottle(c, 540 + 12 * math.sin(t * 30) * pr(t, ts, 0.2) * (1 - pr(t, ts + 0.6, 0.3)), 1080, 0.95, 0.06 * math.sin(t * 20) * (1 - pr(t, ts + 0.6, 0.3)))


SCENES = [(0.0, s_hook), (ph('but it bet') - 0.15, s_bet), (ph('in nineteen eighty') - 0.15, s_story), (ph('by twenty twelve') - 0.15, s_bottles),
          (ph('so what went') - 0.15, s_wrong), (ph('then they split') - 0.15, s_court), (ph('later a chili') - 0.15, s_short), (ph('free ads') - 0.15, s_end)]
DARK_S = {1, 3, 5}
SHAKES = [(ph('one farm'), 8, 0.3), (ph('zero ads'), 10, 0.35), (ph('a court'), 12, 0.4), (ph('seventy dollars'), 8, 0.3), (ph('one supplier'), 12, 0.4)]
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
    dark = i in DARK_S or (i == len(SCENES) - 1 and t >= ph('one supplier') - 0.3)
    if 0.2 < t < END + 0.1: esubs(c, T, t, dark, 1440)
    return s


def cover(out):
    s = skia.Surface(W, H); c = s.getCanvas()
    page(c, False, label='CASE STUDY', num='N° 01')
    headline(c, [[('$0 ON ADS.', False)], [('ONE', False), ('FARM.', True)]], 150, 540, 160, 1.0, maxw=800)
    barn(c, 300, 1150, 0.7); bottle(c, 780, 1080, 0.95)
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
