"""Mamba Mentality. INFOGRAPHIC paper look, no mascot, no likeness, no team logos/uniforms (name as plain text only)."""
import sys, os, math, subprocess
sys.path.insert(0, '/home/claude/studio')
from info_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ORANGE = (214, 110, 50)


def ball(c, x, y, r=110, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawCircle(0, 0, r, P(ORANGE)); c.drawCircle(0, 0, r, S(INK, 6))
    c.drawLine(-r, 0, r, 0, S(INK, 4)); c.drawLine(0, -r, 0, r, S(INK, 4))
    for sx in (-1, 1):
        p = skia.Path(); p.moveTo(sx * r * 0.45, -r * 0.9); p.cubicTo(sx * r * 0.05, -r * 0.3, sx * r * 0.05, r * 0.3, sx * r * 0.45, r * 0.9); c.drawPath(p, S(INK, 4))
    c.restore()


def soccer(c, x, y, r=70):
    c.drawCircle(x, y, r, P(WHITE)); c.drawCircle(x, y, r, S(INK, 5))
    pts = [(x + r * 0.35 * math.cos(a), y + r * 0.35 * math.sin(a)) for a in [i * 2 * math.pi / 5 - math.pi / 2 for i in range(5)]]
    shape(c, path(pts), INK, 2)
    for px, py in pts: c.drawLine(px, py, x + (px - x) * 2.6, y + (py - y) * 2.6, S(INK, 3))


def scoreboard(c, x, y, w, h, top, big, k=1.0, col=None):
    col = col or RED
    shape(c, rr(x, y, w, h, 20), NAVY, 5); shape(c, rr(x + 20, y + 20, w - 40, h - 40, 12), (30, 28, 26), 3)
    text(c, top, x + w / 2, y + 80, 40, YEL, 'Bold')
    text(c, big, x + w / 2, y + h - 50, 150, col, 'Black', a=k)


def hoop(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-150, -200, 300, 190, 10), WHITE, 5); shape(c, rr(-55, -120, 110, 80, 6), WHITE, 4)
    c.drawLine(0, -10, 0, 260, S(INK, 10))
    c.drawOval(skia.Rect.MakeXYWH(-80, -20, 160, 30), S(RED, 7))
    for i in range(6): c.drawLine(-72 + i * 29, -2, -50 + i * 20, 90, S(INK, 2.5))
    c.restore()


def notebook(c, x, y, k, t):
    shape(c, rr(x - 260, y - 170, 520, 340, 14), WHITE, 5)
    for i in range(6): c.drawLine(x - 230, y - 110 + i * 52, x + 230, y - 110 + i * 52, S(BLUE, 2, 0.5))
    c.drawLine(x - 190, y - 170, x - 190, y + 170, S(RED, 2, 0.7))
    s = 'I can do this.'; f = font(78, 'Medium', italic=True); tw = f.measureText(s)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x - tw / 2 - 10, y - 90, (tw + 20) * cl(k), 200)); c.drawString(s, x - tw / 2, y + 30, f, P(RED)); c.restore()


def trophy(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-60, -110); p.lineTo(60, -110); p.cubicTo(60, -20, 30, 10, 0, 14); p.cubicTo(-30, 10, -60, -20, -60, -110); p.close(); shape(c, p, YEL, 4)
    for sx in (-1, 1): c.drawArc(skia.Rect.MakeXYWH(sx * 60 - 30, -100, 60, 60), 90 if sx > 0 else -90, 180 * sx, False, S(INK, 5))
    shape(c, skia.Rect.MakeXYWH(-10, 14, 20, 40), YEL, 3); shape(c, rr(-50, 54, 100, 26, 4), NAVY, 3)
    c.restore()


def mic(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    shape(c, rr(-14, 0, 28, 200, 10), NAVY, 4); shape(c, rr(-48, -110, 96, 120, 48), (200, 200, 205), 5)
    for i in range(4): c.drawLine(-38, -80 + i * 24, 38, -80 + i * 24, S(INK, 2, 0.5))
    shape(c, rr(-40, 40, 80, 40, 6), RED, 3); c.restore()


def quote_mark(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for dx in (0, 70): c.drawPath(path([(dx, 0), (dx + 55, 0), (dx + 35, 90), (dx - 10, 90)]), P(RED))
    c.restore()


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tz = ph('zero points'); tq = ph('quitting')
    title(c, t + 1.0, ['Zero points', 'at twelve'])
    card(c, 70, 500, 940, 830, CARD_SKY)
    hoop(c, 300, 760, 0.9)
    ball(c, 190 + 30 * math.sin(t * 2.2), 1180 - abs(math.sin(t * 3.0)) * 150, 76, t)
    k = pr(t, tz - 0.3, 0.4)
    scoreboard(c, 560, 560, 380, 330, 'ALL SUMMER', '0', 1.0 if t < tz - 0.3 else 1.0)
    if k > 0: pop(c, k, 750, 1000, lambda: chip(c, 'NOT ONE POINT', 750, 1000, YEL, 38))
    if t > tq - 0.2: pop(c, pr(t, tq - 0.2, 0.4), 750, 1180, lambda: (soccer(c, 700, 1180, 64), text(c, '?', 820, 1210, 110, RED, 'Black')))


def s_choice(c, t):
    t0 = SCENES[1][0]; to = ph('obsessed'); ti = ph('i can do this'); tg = ph('studied the greats')
    title(c, t - t0, ['So what', 'did he do?'])
    card(c, 70, 500, 940, 830, CARD_SKY)
    notebook(c, 540, 760, pr(t, ti - 0.1, 0.8), t)
    if t > tg - 0.3:
        items = [('The greats', 230, 1100), ('The basics', 540, 1100), ('Over and over', 850, 1100)]
        for i, (lab, x, y) in enumerate(items):
            k = pr(t, tg - 0.2 + i * 0.35, 0.4)
            if k > 0: pop(c, k, x, y, lambda lab=lab, x=x, y=y: (card(c, x - 140, y - 70, 280, 150, WHITE, 24), check(c, x, y - 10, 30, True, 1), text(c, lab, x, y + 50, 32, INK, 'Bold', maxw=250)))


def s_titles(c, t):
    t0 = SCENES[2][0]
    title(c, t - t0, ['Years', 'later'])
    sky_card(c, 70, 500, 940, 830, 91)
    for i in range(5):
        k = pr(t, t0 + 0.3 + i * 0.18, 0.35)
        if k > 0: pop(c, k, 180 + i * 180, 900, lambda i=i: trophy(c, 180 + i * 180, 900, 1.15))
    chip(c, '5 NBA titles', 540, 1150, YEL, 46) if t > t0 + 1.0 else None


def s_twist(c, t):
    t0 = SCENES[3][0]; tl = ph('led two games'); tr = ph('reporters asked')
    title(c, t - t0, ["But here's", 'the twist'])
    card(c, 70, 500, 940, 830, CARD_SKY)
    if t > t0 + 0.2: pop(c, pr(t, t0 + 0.2, 0.45), 540, 740, lambda: scoreboard(c, 260, 560, 560, 330, '2009 FINALS', '2-0', 1.0, YEL))
    if t > tr - 0.3:
        for i, (x, r) in enumerate(((330, -0.4), (540, 0.0), (750, 0.4))):
            k = pr(t, tr - 0.3 + i * 0.12, 0.4)
            if k > 0: pop(c, k, x, 1050, lambda x=x, r=r: mic(c, x, 1060, 0.85, r))
        chip(c, '"Why aren\'t you happy?"', 540, 1250, WHITE, 36)


def s_quote(c, t):
    t0 = SCENES[4][0]; tj = ph("job's not")
    card(c, 70, 330, 940, 1000, (40, 36, 34), 36)
    quote_mark(c, 150, 420, 1.2)
    f = font(66, 'Medium', italic=True)
    lines = ["What's there to be", 'happy about?']
    for i, s in enumerate(lines):
        k = pr(t, t0 + 0.3 + i * 0.2, 0.4)
        c.drawString(s, 150, 680 + i * 86, f, P(WHITE, k))
    if t > tj - 0.1:
        k = eo(pr(t, tj - 0.1, 0.4)); f2 = font(96, 'Bold', italic=True)
        c.drawString("Job's not", 150, 940, f2, P((226, 70, 64), k)); c.drawString('finished.', 150, 1050, f2, P((226, 70, 64), k))
    c.drawLine(150, 1180, 210, 1180, S(RED, 5)); text(c, 'KOBE BRYANT, 2009 FINALS', 240, 1192, 30, (200, 190, 175), 'SemiBold', align='l')


def s_end(c, t):
    t0 = SCENES[5][0]; tn = ph('never satisfied'); tm = ph("that's the mamba")
    title(c, t - t0, ['The Mamba', 'Mentality'] if t > tm - 0.3 else ['Never', 'satisfied'])
    card(c, 70, 500, 940, 830, WHITE)
    text(c, 'Age 12', 290, 640, 44, GREY, 'SemiBold'); text(c, 'Age 30', 790, 640, 44, GREY, 'SemiBold')
    c.drawLine(540, 580, 540, 1000, S(INK, 3, 0.5))
    text(c, '0 points', 290, 800, 80, INK, 'Black')
    if t > tn - 0.2: text(c, 'Job not', 790, 780, 72, RED, 'Black', a=pr(t, tn - 0.2, 0.4)); text(c, 'finished', 790, 870, 72, RED, 'Black', a=pr(t, tn - 0.2, 0.4))
    ball(c, 540, 1160, 110, t * 1.5)


SCENES = [(0.0, s_hook), (ph('so what did') - 0.15, s_choice), (ph('he went on') - 0.15, s_titles), (ph("but here's") - 0.15, s_twist),
          (ph('he said') - 0.15, s_quote), (ph('zero points at') - 0.15, s_end)]
SHAKES = [(ph('zero points'), 14, 0.4), (ph('five nba'), 10, 0.35), (ph("job's not"), 12, 0.4), (ph("that's the mamba"), 10, 0.4)]
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
    text(c, 'Zero points', 540, 460, 130, INK, 'Black'); f = font(120, 'Medium', italic=True); s_ = 'to five titles'; c.drawString(s_, 540 - f.measureText(s_) / 2, 600, f, P(RED))
    card(c, 70, 690, 940, 750, CARD_SKY)
    hoop(c, 330, 950, 0.95); ball(c, 330, 1260, 90, 0.3)
    scoreboard(c, 560, 760, 380, 330, 'AGE 12', '0')
    for i in range(5): trophy(c, 600 + i * 70, 1250, 0.5)
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
