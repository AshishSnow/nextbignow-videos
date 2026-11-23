"""Yue Yuen in the INFOGRAPHIC look (no mascot). usage: still t... | nframes | range f0 f1 | cover out.png"""
import sys, os, math, subprocess
sys.path.insert(0, '/home/claude/studio')
from info_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
BRANDS = [('NIKE', 'nike', RED, BLUE), ('ADIDAS', 'adidas', BLUE, YEL), ('NEW BALANCE', 'new balance', (150, 156, 168), RED), ('PUMA', 'puma', YEL, NAVY)]


def callout(c, x, y, w, head, body, k, icon=None):
    if k <= 0: return
    def d():
        card(c, x, y, w, 150, WHITE, 26)
        text(c, head, x + w / 2 + (30 if icon else 0), y + 62, 36, INK, 'Bold', maxw=w - 120 if icon else w - 40)
        text(c, body, x + w / 2 + (30 if icon else 0), y + 112, 28, GREY, 'Medium', maxw=w - 120 if icon else w - 40, disp=False)
        if icon: icon(x + 62, y + 75)
    pop(c, k, x + w / 2, y + 75, d)


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    th = ph('yue yuen'); te = ph('every one')
    title(c, t + 1.0, ['The sneaker maker', "you've never heard of"])
    sky_card(c, 70, 500, 940, 830, 5)
    pos = [(300, 760), (780, 760), (300, 1040), (780, 1040)]
    for i, (n, kk, col, acc) in enumerate(BRANDS):
        k = 1.0 if i == 0 else pr(t, ph(kk) - 0.15, 0.35)
        x, y = pos[i]
        if k > 0:
            pop(c, k, x, y, lambda x=x, y=y, col=col, acc=acc, n=n: (sneaker(c, x, y, 0.62, col, acc, -0.03 * (x - 540)), chip(c, n, x, y + 105, WHITE, 28)))
        if t > te: check(c, x + 150, y - 70, 26, True, pr(t, te - 0.1 + i * 0.12, 0.3))
    if t > th - 0.25:
        def badge():
            c.drawCircle(540, 900, 112, P(YEL)); c.drawCircle(540, 900, 112, S(INK, 5))
            factory(c, 540, 950, 0.3, t); text(c, 'YUE YUEN', 540, 1000, 26, INK, 'Black', maxw=170)
        pop(c, pr(t, th - 0.25, 0.45), 540, 900, badge)
    if t > te - 0.2:
        for i, (x, y) in enumerate(pos): arrow(c, 540 + (-90 if x < 540 else 90), 900 + (-40 if y < 900 else 40), x + (130 if x < 540 else -130), y + (-10 if y < 900 else -10), pr(t, te - 0.2 + i * 0.1, 0.3), RED, 6)


def s_who(c, t):
    t0 = SCENES[1][0]; tl = ph('listed in'); tf = ph('factory company')
    title(c, t - t0, ['Who really makes', 'your sneakers?'])
    sky_card(c, 70, 500, 940, 830, 8)
    factory(c, 540, 1240, 1.15, t)
    conveyor(c, 120, 1180, 300, t, 1.0, 3, 0.2)
    callout(c, 600, 540, 380, 'Yue Yuen', 'footwear maker', pr(t, tf - 0.3, 0.4))
    callout(c, 100, 540, 400, 'Listed in', 'Hong Kong', pr(t, tl - 0.2, 0.4), lambda x, y: pin(c, x, y + 8, 0.9))


def s_volume(c, t):
    t0 = SCENES[2][0]; tn = ph('two hundred'); te = ph('eight pairs')
    title(c, t - t0, ['Shoes shipped', 'in 2025'])
    card(c, 70, 500, 940, 830, CARD_SKY)
    conveyor(c, 110, 700, 860, t, 2.2 if t > te else 1.0, 6, 0.34)
    if t > tn - 0.3:
        def big():
            card(c, 150, 820, 780, 240, YEL, 30)
            text(c, '252.2 million', 540, 950, 110, INK, 'Black'); text(c, 'PAIRS OF SHOES', 540, 1020, 40, INK, 'Bold')
        pop(c, pr(t, tn - 0.3, 0.45), 540, 940, big)
    if t > te - 0.3:
        def sec():
            card(c, 220, 1110, 640, 170, WHITE, 30); stopwatch(c, 330, 1205, 56, t)
            text(c, '8 pairs', 600, 1190, 64, RED, 'Black'); text(c, 'every second', 600, 1245, 36, INK, 'SemiBold')
        pop(c, pr(t, te - 0.3, 0.4), 540, 1195, sec)


def s_price(c, t):
    t0 = SCENES[3][0]; ta = ph('twenty one')
    title(c, t - t0, ['What it gets', 'per pair'])
    sky_card(c, 70, 500, 940, 830, 11)
    sneaker(c, 540, 860, 1.25, RED, BLUE, -0.06)
    if t > ta - 0.3: pop(c, pr(t, ta - 0.3, 0.4), 770, 1080, lambda: pricetag(c, 700, 1080, '$21', -8, 1.05))
    callout(c, 110, 1060, 420, 'On average', 'Yue Yuen, 2025', pr(t, ph('on average') - 0.2, 0.4))


def s_split(c, t):
    t0 = SCENES[4][0]; td = ph('the design'); ta = ph('the ads'); tb = ph('does the building')
    title(c, t - t0, ['Who does', 'what?'])
    card(c, 70, 500, 940, 830, WHITE)
    text(c, 'Quick-glance guide', 540, 600, 50, INK, 'Bold'); rule(c, 120, 960, 640)
    text(c, 'Job', 230, 715, 38, GREY, 'SemiBold'); text(c, 'Brand', 590, 715, 38, INK, 'Bold'); text(c, 'Yue Yuen', 850, 715, 38, INK, 'Bold')
    rows = [('Design', td, (True, False)), ('Ads', ta, (True, False)), ('Building', tb, (False, True))]
    for i, (lab, tt, marks) in enumerate(rows):
        y = 840 + i * 150; c.drawLine(120, y - 75, 960, y - 75, S(INK, 2, 0.25))
        text(c, lab, 230, y + 14, 44, INK, 'SemiBold')
        k = pr(t, tt - 0.25, 0.35)
        check(c, 590, y, 36, marks[0], k); check(c, 850, y, 36, marks[1], k)
    sneaker(c, 540, 1270, 0.42, RED, BLUE)


def s_war(c, t):
    t0 = SCENES[5][0]; ts = ph('same maker'); tw = ph('sneaker war'); tb = ph('both sides')
    title(c, t - t0, ['Rivals on the shelf'] if t < ts else ['Rivals on the shelf.', 'Same maker behind.'])
    sky_card(c, 70, 500, 940, 830, 14)
    rk = eo(pr(t, ts - 0.2, 0.7))
    if rk > 0:
        c.save(); c.translate(0, 380 * (1 - rk)); factory(c, 540, 1120, 0.9, t); c.restore()
    bump = math.sin(t * 10) * 12 if t > tw else 0
    sneaker(c, 290 + bump, 1040, 0.72, RED, BLUE, 0.05); chip(c, 'NIKE', 290 + bump, 1150, WHITE, 30)
    sneaker(c, 790 - bump, 1040, 0.72, BLUE, YEL, -0.05, flip=True); chip(c, 'ADIDAS', 790 - bump, 1150, WHITE, 30)
    if t < ts + 0.2: vs_badge(c, 540, 980)
    if rk > 0.9:
        arrow(c, 470, 860, 330, 970, pr(t, ts + 0.4, 0.3), RED, 6, -0.2); arrow(c, 610, 860, 750, 970, pr(t, ts + 0.5, 0.3), RED, 6, 0.2)
    if t > tb - 0.2:
        pop(c, pr(t, tb - 0.2, 0.4), 540, 610, lambda: (card(c, 150, 545, 780, 120, YEL, 30), text(c, 'Both buy from one maker', 540, 625, 50, INK, 'Black')))


SCENES = [(0.0, s_hook), (ph('so who really') - 0.15, s_who), (ph('last year') - 0.15, s_volume), (ph('how much') - 0.15, s_price),
          (ph('the brands do') - 0.15, s_split), (ph('rivals on') - 0.15, s_war)]
SHAKES = [(ph('yue yuen'), 8, 0.3), (ph('two hundred'), 12, 0.4), (ph('twenty one'), 7, 0.3), (ph('same maker'), 10, 0.4), (ph('both sides'), 8, 0.35)]
TR = 0.32


def page(c, t):
    paper(c)


def draw_scene(c, i, t): page(c, t); SCENES[i][1](c, t)


def frame(t):
    s = skia.Surface(W, H); c = s.getCanvas(); sx = sy = 0.0
    for (ts, a, d) in SHAKES:
        if ts <= t < ts + d: k = 1 - (t - ts) / d; sx += a * k * math.sin(t * 90); sy += a * k * math.cos(t * 77)
    c.save(); c.translate(sx, sy)
    i = max(j for j, (t0, _) in enumerate(SCENES) if t >= t0)
    draw_scene(c, i, t)
    if i > 0 and t < SCENES[i][0] + TR:   # slide the old page out to the left
        k = eio((t - SCENES[i][0]) / TR); c.save(); c.translate(-W * k, 0); draw_scene(c, i - 1, t); c.restore()
        c.drawRect(skia.Rect.MakeXYWH(W * (1 - k) - 5, 0, 10, H), P(INK, 0.15))
    c.restore()
    if 0.2 < t < END + 0.1: subs(c, T, t, 1440)
    return s


def cover(out):
    s = skia.Surface(W, H); c = s.getCanvas(); page(c, 0)
    chip(c, 'oops, my business', 540, 300, YEL, 32)
    text(c, 'Who makes', 540, 460, 136, INK, 'Black'); f = font(130, 'Medium', italic=True); s_ = 'your sneakers?'; c.drawString(s_, 540 - f.measureText(s_) / 2, 600, f, P(RED))
    sky_card(c, 70, 680, 940, 760, 5)
    factory(c, 540, 1240, 0.95, 0.4)
    sneaker(c, 280, 1270, 0.55, RED, BLUE, 0.05); sneaker(c, 800, 1270, 0.55, BLUE, YEL, -0.05, flip=True)
    c.drawCircle(540, 860, 80, P(YEL)); c.drawCircle(540, 860, 80, S(INK, 5)); text(c, '?', 540, 900, 110, INK, 'Black')
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
        enc = lambda name: subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
                                             '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', os.path.join(out, name)], stdin=subprocess.PIPE)
        pi = enc('ig_%05d.mp4' % f0)
        for fi in range(f0, f1):
            pi.stdin.write(np.ascontiguousarray(to_np(frame(fi / FPS).makeImageSnapshot())).tobytes())
        pi.stdin.close(); pi.wait()
