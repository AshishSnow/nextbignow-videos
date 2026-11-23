"""Purple Cow (Seth Godin) in the ESSAY look: cream/dark alternating slides, accent purple, ends on full-purple slide.
No book cover art (title as plain text), no likeness of Godin."""
import sys, os, math, subprocess
sys.path.insert(0, '/home/claude/studio')
from essay_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC[0] = (138, 66, 214)
NS = 9


def num(i): return '%02d / %02d' % (i, NS)


def cow_front(c, x, y, s=1.0, col=None, t=0.0):
    col = col or acc()
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-170, 300, 340, 40), P(INKE, 0.18))
    for lx in (-80, -30, 30, 80):
        shape(c, rr(lx - 18, 150, 36, 170, 10), col, 4); c.drawRect(skia.Rect.MakeXYWH(lx - 18, 300, 36, 20), P(INKE))
    bodyp = skia.Path(); bodyp.addOval(skia.Rect.MakeXYWH(-140, -20, 280, 240)); shape(c, bodyp, col, 5)
    for sx in (-1, 1):
        ear = skia.Path(); ear.addOval(skia.Rect.MakeXYWH(sx * 130 - 50, -150, 100, 50)); shape(c, ear, col, 4)
        h = skia.Path(); h.moveTo(sx * 60, -170); h.cubicTo(sx * 110, -200, sx * 140, -250, sx * 120, -290); c.drawPath(h, S(INKE, 9)); c.drawPath(h, S((238, 232, 220), 5))
    head = skia.Path(); head.moveTo(-90, -190); head.cubicTo(-100, -100, -80, 20, 0, 40); head.cubicTo(80, 20, 100, -100, 90, -190); head.cubicTo(40, -220, -40, -220, -90, -190); head.close()
    shape(c, head, col, 5)
    c.save(); c.clipPath(head, doAntiAlias=True)
    for i in range(-200, 200, 10): c.drawLine(i, -220, i + 60, 60, S(INKE, 1.2, 0.25))
    c.restore()
    shape(c, rr(-62, -20, 124, 70, 34), tuple(min(255, v + 40) for v in col), 4)
    for sx in (-1, 1):
        c.drawOval(skia.Rect.MakeXYWH(sx * 26 - 9, 2, 18, 22), P(INKE))
        blink = 0.1 if (t % 3.2) < 0.12 else 1.0
        c.drawOval(skia.Rect.MakeXYWH(sx * 44 - 12, -120, 24, 24 * blink), P(INKE))
    c.restore()


def car(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, rr(-160, -60, 320, 70, 20), (210, 70, 60), 4)
    shape(c, path([(-90, -60), (-60, -115), (70, -115), (110, -60)]), (210, 70, 60), 4)
    for wx in (-55, 30): shape(c, rr(wx, -105, 60, 40, 6), (200, 220, 235), 3)
    for wx in (-95, 95):
        c.drawCircle(wx, 12, 30, P(INKE)); c.save(); c.translate(wx, 12); c.rotate(-t * 600)
        c.drawLine(-18, 0, 18, 0, S(CREAM, 3)); c.restore()
    c.restore()


def book(c, x, y, s=1.0, rot=-6):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect.MakeXYWH(-150 + 14, -210 + 16, 300, 420), P((0, 0, 0), 0.35))
    shape(c, skia.Rect.MakeXYWH(-150, -210, 300, 420), acc(), 4); c.drawRect(skia.Rect.MakeXYWH(-150, -210, 22, 420), P(INKE, 0.25))
    f = anton(78);
    for i, s_ in enumerate(('PURPLE', 'COW')): c.drawString(s_, -f.measureText(s_) / 2 + 10, -60 + i * 84, f, P(CREAM_T))
    g = font(24, 'SemiBold', False); s_ = 'SETH GODIN · 2003'; c.drawString(s_, -g.measureText(s_) / 2 + 10, 170, g, P(CREAM_T, 0.9))
    c.restore()


def store(c, x, y, s=1.0, col=None, label='SHOP'):
    col = col or (205, 200, 190)
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, skia.Rect.MakeXYWH(-80, -150, 160, 150), col, 3)
    for i in range(5): c.drawRect(skia.Rect.MakeXYWH(-80 + i * 32, -150, 32, 34), P(INKE if i % 2 else (240, 236, 226), 0.85))
    c.drawRect(skia.Rect.MakeXYWH(-80, -150, 160, 34), S(INKE, 3))
    shape(c, skia.Rect.MakeXYWH(-25, -80, 50, 80), (120, 110, 100), 3); shape(c, skia.Rect.MakeXYWH(-70, -96, 36, 40), (210, 225, 235), 2)
    c.restore()


def shape(c, sh, fill, ow=4):
    if isinstance(sh, skia.Rect): c.drawRect(sh, P(fill)); c.drawRect(sh, S(INKE, ow))
    elif isinstance(sh, skia.RRect): c.drawRRect(sh, P(fill)); c.drawRRect(sh, S(INKE, ow))
    else: c.drawPath(sh, P(fill)); c.drawPath(sh, S(INKE, ow))


# ------------------------------------------------------------------ scenes  (dark flag per scene for subtitles)
def s_pick(c, t):
    page(c, False, num=num(1), prog=t / DUR)
    headline(c, [[('PICK ANY COW', False)], [('IN', False), ('3 SECONDS.', True)]], 150, 520, 132, 1.0)
    herd(c, 7, (3, 1), t)
    k = eo(pr(t, ph('three seconds') - 0.1, 0.5))
    if k > 0:
        p = skia.Path(); p.moveTo(820, 640); p.cubicTo(860, 760, 760, 860, 560 + 0 * k, 960);
        meas = skia.PathMeasure(p, False); seg = skia.Path(); meas.getSegment(0, meas.getLength() * k, seg, True); c.drawPath(seg, S(acc(), 6))


def s_count(c, t):
    t0 = SCENES[1][0]
    page(c, True, num=num(2), prog=t / DUR)
    f = anton(260); xs = [150, 470, 790]; words = ['three', 'two', 'one']
    for i, (x, w) in enumerate(zip(xs, words)):
        tt = ph(w, t0); k = eo(pr(t, tt - 0.1, 0.3))
        if k > 0:
            c.save(); c.translate(0, 40 * (1 - k)); c.drawString(str(3 - i), x, 980, f, P(CREAM_T, k)); c.restore()
            if i < 2:
                for j in range(3): c.drawRect(skia.Rect.MakeXYWH(x + 150 + j * 44, 950, 30, 30), P(acc(), k))
    th = ph('you picked')
    body(c, 'Go with your gut.', 150, 1110, 64, CREAM_T, 'Bold', a=pr(t, t0 + 0.3, 0.4))
    if t > th - 0.2:
        a = pr(t, th - 0.2, 0.4)
        body(c, '(You picked the', 150, 1190, 44, MUTE, 'Regular', a=a)
        body(c, 'purple one, right?)', 150, 1248, 44, acc(), 'SemiBold', a=a)


def s_eyes(c, t):
    t0 = SCENES[2][0]
    page(c, False, num=num(3), prog=t / DUR)
    headline(c, [[('NOT THE BIGGEST.', None)], [('NOT THE STRONGEST.', None)]], 150, 500, 96, pr(t, t0 + 0.1, 0.6))
    pc = herd(c, 7, (3, 1), t, fade=0.55 * pr(t, t0, 0.6), y0=860, y1=1300, n_rows=5)
    if pc:
        px, py = pc[0], pc[1]
        for i, (ex, ey) in enumerate(((150, 900), (930, 940), (120, 1240), (960, 1260), (540, 1340))):
            k = pr(t, t0 + 0.2 + i * 0.12, 0.35); eye(c, ex, ey, 34, k); dotted(c, ex, ey, px + (ex - px) * 0.25, py + (ey - py) * 0.25, pr(t, t0 + 0.4 + i * 0.12, 0.4))
        c.drawCircle(px, py, 105, S(acc(), 6, pr(t, ph('just different') - 0.2, 0.3)))
    if t > ph('just different') - 0.2:
        k = pr(t, ph('just different') - 0.2, 0.4)
        headline(c, [[("JUST", False), ('DIFFERENT.', True)]], 150, 760, 120, k)


def s_book(c, t):
    t0 = SCENES[3][0]; tb = ph('purple cow')
    page(c, True, num=num(4), prog=t / DUR)
    headline(c, [[('A WHOLE BOOK', False)], [('ON ONE', False), ('IDEA.', True)]], 150, 520, 120, pr(t, t0 + 0.1, 0.6), dark=True)
    k = pr(t, tb - 0.4, 0.5)
    if k > 0: pop(c, k, 540, 1000, lambda: book(c, 540, 1000, 1.0))
    body(c, 'Seth Godin, marketer', 150, 1300, 36, MUTE, 'Medium', a=pr(t, ph('seth godin') - 0.1, 0.4))


def s_trip(c, t):
    t0 = SCENES[4][0]; ts = ph('every cow')
    page(c, False, num=num(5), prog=t / DUR)
    fade = pr(t, ts - 0.2, 0.8)
    if fade < 0.5: headline(c, [[('A ROAD TRIP', False)], [('THROUGH', False), ('FRANCE.', True)]], 150, 520, 120, pr(t, t0 + 0.1, 0.6))
    else: headline(c, [[('EVERY COW LOOKS', False)], [('THE', False), ('SAME.', True)]], 150, 520, 120, pr(t, ts - 0.2 + 0.4, 0.6))
    c.drawRect(skia.Rect.MakeXYWH(0, 1180, W, 70), P((200, 192, 180))); c.drawLine(0, 1215, W, 1215, S(CREAM, 5))
    off = (t * 220) % 260
    for r in range(2):
        for i in range(6):
            x = (i * 260 - off + r * 130) % (W + 260) - 130
            cow(c, x, 840 + r * 170, 0.5 + 0.1 * r, i % 2 == 0, None, True, 1.0 - 0.75 * fade)
    car(c, 540, 1205, 1.0, t)


def s_stop(c, t):
    t0 = SCENES[5][0]; w1, w2, w3 = ph("you'd stop"), ph("you'd stare"), ph("you'd tell")
    page(c, False, num=num(6), prog=t / DUR)
    segs = [('YOU', False), ('STOP.', True)]
    headline(c, [segs], 150, 500, 120, pr(t, w1 - 0.1, 0.4))
    headline(c, [[('YOU STARE.', False)]], 150, 630, 120, pr(t, w2 - 0.1, 0.4))
    headline(c, [[('YOU TELL PEOPLE.', False)]], 150, 760, 120, pr(t, w3 - 0.1, 0.4))
    k = eo(pr(t, t0 + 0.1, 0.6))
    for i, (x, fl) in enumerate(((180, False), (900, True))): cow(c, x, 1180, 0.6, fl, None, True, 0.6)
    c.save(); c.translate(0, 60 * (1 - k)); cow_front(c, 540, 1000, 0.75 * k + 0.01, acc(), t); c.restore()


def s_biz(c, t):
    t0 = SCENES[6][0]; ts = ph('same thing'); tf = ph('in the field')
    page(c, True, num=num(7), prog=t / DUR)
    headline(c, [[('NOW LOOK AT', False)], [('YOUR BUSINESS.', True)]], 150, 520, 120, pr(t, t0 + 0.1, 0.6), dark=True)
    for i in range(5):
        k = pr(t, ts - 0.3 + i * 0.1, 0.35)
        if k > 0: pop(c, k, 170 + i * 185, 1000, lambda i=i: store(c, 170 + i * 185, 1060, 1.0))
    if t > tf - 0.4:
        body(c, 'Same stuff. Same way.', 150, 1180, 48, CREAM_T, 'Bold', a=pr(t, tf - 0.4, 0.3))
        body(c, 'One more cow in the field.', 150, 1245, 44, MUTE, 'Medium', a=pr(t, tf - 0.2, 0.3))


def s_end(c, t):
    t0 = SCENES[7][0]; tp = ph('be the purple')
    if t < tp - 0.2:
        page(c, False, num=num(8), prog=t / DUR)
        headline(c, [[("DON'T BE A", False)], [('BETTER COW.', None)]], 150, 520, 132, pr(t, t0 + 0.1, 0.6))
        herd(c, 11, None, t, 0.3, 900, 1320, 4)
    else:
        page(c, False, num=num(9), prog=t / DUR, fill=acc())
        k = pr(t, tp - 0.2, 0.5)
        f = anton(150)
        for i, s_ in enumerate(('BE THE', 'PURPLE', 'ONE.')):
            kk = eo(cl(k * 1.6 - i * 0.2)); c.save(); c.translate(0, 40 * (1 - kk))
            c.drawString(s_, 150, 560 + i * 155, f, P(CREAM_T if i != 1 else INKE, kk)); c.restore()
        cow_front(c, 700, 1080, 0.6, (250, 246, 236), t)


SCENES = [(0.0, s_pick), (ph('three two') - 0.15, s_count), (ph("it's not the biggest") - 0.15, s_eyes), (ph('marketer') - 0.15, s_book),
          (ph('on a road') - 0.15, s_trip), (ph('a purple cow') - 0.15, s_stop), (ph('now look') - 0.15, s_biz), (ph('so stop trying') - 0.15, s_end)]
DARK_S = {1, 3, 6}
SHAKES = [(ph('just different'), 8, 0.3), (ph('purple cow', ph('marketer')), 8, 0.3), (ph("you'd stop"), 10, 0.35), (ph('be the purple'), 12, 0.4)]
TR = 0.3


def draw_scene(c, i, t): SCENES[i][1](c, t)


def frame(t):
    s = skia.Surface(W, H); c = s.getCanvas(); sx = sy = 0.0
    for (ts, a, d) in SHAKES:
        if ts <= t < ts + d: k = 1 - (t - ts) / d; sx += a * k * math.sin(t * 90); sy += a * k * math.cos(t * 77)
    c.save(); c.translate(sx, sy)
    i = max(j for j, (t0, _) in enumerate(SCENES) if t >= t0)
    draw_scene(c, i, t)
    if i > 0 and t < SCENES[i][0] + TR:   # page slides up and away (card swipe)
        k = eio((t - SCENES[i][0]) / TR); c.save(); c.translate(-W * k, 0); draw_scene(c, i - 1, t); c.restore()
    c.restore()
    dark = i in DARK_S or (i == len(SCENES) - 1 and t >= ph('be the purple') - 0.2)
    if 0.2 < t < END + 0.1: esubs(c, T, t, dark, 1440)
    return s


def cover(out):
    s = skia.Surface(W, H); c = s.getCanvas()
    page(c, False, label='OOPS, MY BUSINESS', num='N° 01')
    headline(c, [[('BE THE', False), ('PURPLE', True)], [('COW.', False)]], 150, 540, 170, 1.0, maxw=780)
    body(c, 'The one rule of standing out', 150, 790, 44, INKE, 'SemiBold')
    for x, y, fl in ((170, 1180, False), (920, 1170, True), (120, 1330, False), (960, 1320, True)): cow(c, x, y, 0.62, fl)
    cow_front(c, 540, 1080, 0.85, acc(), 1.0)
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
