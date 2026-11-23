"""Scrub Daddy: the foam 3M left behind. INFOGRAPHIC paper look, no mascot.
No trade dress: a generic BLUE rectangular foam block with a plain slot (not the round yellow smiley), no 3M / Shark Tank logos,
names as plain text only, no likeness of real people."""
import sys, os, math, subprocess
sys.path.insert(0, '/home/claude/studio')
from info_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
FOAM = (120, 160, 205)


def sponge(c, x, y, s=1.0, rot=0.0, slot=0.0, firm=0.5):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * (1.04 - 0.08 * firm), s * (0.96 + 0.08 * firm))
    shape(c, rr(-120, -70, 240, 140, 30), FOAM, 5)
    rnd = random.Random(4)
    for i in range(26): c.drawCircle(rnd.uniform(-100, 100), rnd.uniform(-52, 52), rnd.uniform(3, 7), P(INK, 0.18))
    if slot > 0:
        k = cl(slot); p = skia.Path(); p.moveTo(-60 * k, 10); p.cubicTo(-30 * k, 40 * k, 30 * k, 40 * k, 60 * k, 10)
        p.cubicTo(30 * k, 22 * k, -30 * k, 22 * k, -60 * k, 10); p.close(); shape(c, p, INK, 3)
    c.restore()


def box(c, x, y, s=1.0, lid=0.0, label='SCRAP'):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, path([(-200, -60), (200, -60), (180, 160), (-180, 160)]), (205, 160, 110), 5)
    c.drawLine(-190, 0, 190, 0, S(INK, 2, 0.4))
    a = lid * 1.2
    for sx in (-1, 1):
        c.save(); c.translate(sx * 200, -60); c.rotate(sx * (-a) * 57.3)
        shape(c, path([(0, 0), (-sx * 200, 0), (-sx * 200, -18), (0, -18)]) if lid < 0.05 else path([(0, 0), (-sx * 190, 0), (-sx * 170, -90), (0, -90)]), (190, 145, 98), 4)
        c.restore()
    c.save(); c.rotate(-0.05); shape(c, rr(-110, 30, 220, 70, 6), WHITE, 3); text(c, label, 0, 82, 50, RED, 'Black'); c.restore()
    c.restore()


def cal(c, x, y, yr, k):
    if k <= 0: return
    def d():
        shape(c, rr(x - 75, y - 70, 150, 150, 14), WHITE, 4); c.drawRect(skia.Rect.MakeXYWH(x - 73, y - 68, 146, 40), P(RED))
        for i in (-40, 40): c.drawLine(x + i, y - 84, x + i, y - 56, S(INK, 5))
        text(c, yr, x, y + 48, 54, INK, 'Black')
    pop(c, k, x, y, d)


def snow(c, x, y, r):
    for i in range(3):
        a = i * math.pi / 3; c.drawLine(x - r * math.cos(a), y - r * math.sin(a), x + r * math.cos(a), y + r * math.sin(a), S(BLUE, 6))
    c.drawCircle(x, y, 8, P(WHITE)); c.drawCircle(x, y, 8, S(INK, 2))


def sun(c, x, y, r, t):
    for i in range(10):
        a = i * math.pi / 5 + t * 0.5; c.drawLine(x + r * 1.15 * math.cos(a), y + r * 1.15 * math.sin(a), x + r * 1.5 * math.cos(a), y + r * 1.5 * math.sin(a), S(YEL, 6))
    c.drawCircle(x, y, r, P(YEL)); c.drawCircle(x, y, r, S(INK, 4))


def spoon(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-34, -120, 68, 92), P((210, 212, 218))); c.drawOval(skia.Rect.MakeXYWH(-34, -120, 68, 92), S(INK, 4))
    shape(c, rr(-10, -34, 20, 170, 10), (210, 212, 218), 4); c.restore()


def chair(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(4): shape(c, rr(-120, -220 + i * 44, 240, 30, 8), WHITE, 4)
    shape(c, rr(-140, -20, 280, 34, 8), WHITE, 4)
    for lx in (-120, 110): shape(c, skia.Rect.MakeXYWH(lx, 14, 14, 120), WHITE, 3)
    c.restore()


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tb = ph('left one'); ts = ph('called scrap')
    title(c, t + 1.0, ['The foam 3M', 'left behind'])
    sky_card(c, 70, 500, 940, 830, 71)
    lid = eo(pr(t, ts - 0.4, 0.6))
    box(c, 540, 1060, 1.1, lid)
    if lid > 0.3: sponge(c, 540, 1000 - 120 * eo(pr(t, ts - 0.1, 0.5)), 0.85, 0.08 * math.sin(t * 3))
    chip(c, '3M buys his pad business, 2008', 540, 620, WHITE, 32)
    if t > tb - 0.2: check(c, 830, 600, 34, False, pr(t, tb - 0.2, 0.3))


def s_story(c, t):
    t0 = SCENES[1][0]; tm = ph('made a foam'); tn = ph("wouldn't buy"); ty = ph('for years')
    title(c, t - t0, ['What was', 'in the box?'])
    card(c, 70, 500, 940, 830, CARD_SKY)
    c.drawLine(150, 1080, 930, 1080, S(INK, 4))
    cal(c, 220, 680, '2006', pr(t, tm - 0.2, 0.4)); cal(c, 540, 680, '2007', pr(t, tn - 0.3, 0.4)); cal(c, 860, 680, 'years', pr(t, ty - 0.3, 0.4))
    if t > tm - 0.1: pop(c, pr(t, tm - 0.1, 0.4), 220, 920, lambda: (sponge(c, 220, 900, 0.85), text(c, 'Hand scrubber', 220, 1140, 32, INK, 'Bold')))
    if t > tn - 0.2: pop(c, pr(t, tn - 0.2, 0.4), 540, 920, lambda: (check(c, 540, 900, 78, False, 1), text(c, 'Body shops: no', 540, 1140, 32, INK, 'Bold')))
    if t > ty - 0.2: pop(c, pr(t, ty - 0.2, 0.4), 860, 940, lambda: (box(c, 860, 880, 0.62), text(c, 'In the box', 860, 1140, 32, INK, 'Bold')))
    for x, tt in ((220, tm), (540, tn), (860, ty)):
        if t > tt - 0.2: c.drawCircle(x, 1080, 14, P(RED)); c.drawCircle(x, 1080, 14, S(INK, 3))


def s_find(c, t):
    t0 = SCENES[2][0]; tf = ph('made it firm'); tw = ph('warm water')
    title(c, t - t0, ['One fall day,', 'a second look'])
    card(c, 70, 500, 940, 830, CARD_SKY)
    if t < tf - 0.3:
        chair(c, 540, 1050, 1.3); sponge(c, 540 + 60 * math.sin(t * 6), 880, 0.7, 0.2 * math.sin(t * 6))
        chip(c, 'Fall 2011: scrubbing lawn furniture', 540, 1200, WHITE, 30)
    else:
        c.drawLine(540, 540, 540, 1290, S(INK, 3, 0.5))
        snow(c, 300, 650, 56); sponge(c, 300, 900, 0.8, 0, 0, 1.0); text(c, 'Cold water', 300, 1080, 44, INK, 'Bold'); text(c, '= firm', 300, 1140, 44, BLUE, 'Bold')
        k = pr(t, tw - 0.2, 0.4)
        if k > 0: pop(c, k, 780, 880, lambda: (sun(c, 780, 650, 46, t), sponge(c, 780, 900, 0.8, 0, 0, 0.0), text(c, 'Warm water', 780, 1080, 44, INK, 'Bold'), text(c, '= soft', 780, 1140, 44, RED, 'Bold')))


def s_smile(c, t):
    t0 = SCENES[3][0]; tn = ph('scrub daddy')
    title(c, t - t0, ['He gave it', 'a smile'])
    sky_card(c, 70, 500, 940, 830, 77)
    sl = eo(pr(t, ph('a smile') - 0.1, 0.5))
    sponge(c, 540, 860, 1.6, -0.03, sl)
    if t > ph('cleaning spoons') - 0.3:
        u = pr(t, ph('cleaning spoons') - 0.3, 0.6); spoon(c, 540 + 200 * (1 - eo(u)), 830, 1.1, 1.3 - 0.3 * eo(u))
    callout(c, 120, 1090, 420, 'The smile', 'cleans utensils', pr(t, ph('cleaning spoons'), 0.4))
    if t > tn - 0.2: pop(c, pr(t, tn - 0.2, 0.4), 760, 1160, lambda: chip(c, 'Scrub Daddy', 760, 1170, YEL, 40))


def callout(c, x, y, w, head, body, k):
    if k <= 0: return
    pop(c, k, x + w / 2, y + 75, lambda: (card(c, x, y, w, 150, WHITE, 26), text(c, head, x + w / 2, y + 62, 36, INK, 'Bold'), text(c, body, x + w / 2, y + 112, 28, GREY, 'Medium')))


def s_work(c, t):
    t0 = SCENES[4][0]; tt = ph('two hundred thousand'); ts = ph('sales topped')
    title(c, t - t0, ['Did it', 'work?'])
    card(c, 70, 500, 940, 830, WHITE)
    if t > tt - 0.3:
        pop(c, pr(t, tt - 0.3, 0.45), 540, 680, lambda: (card(c, 160, 580, 760, 200, CARD_SKY, 28), text(c, '$200,000', 540, 690, 88, INK, 'Black'), text(c, 'from Lori Greiner on Shark Tank, 2012', 540, 750, 32, GREY, 'Medium')))
    if t > ts - 0.3:
        pop(c, pr(t, ts - 0.3, 0.45), 540, 960, lambda: (card(c, 130, 840, 820, 250, YEL, 30), text(c, '$220M+', 540, 980, 130, INK, 'Black'), text(c, 'sales in 2023, reported', 540, 1050, 38, INK, 'SemiBold')))
    sponge(c, 540, 1200, 0.75, 0.05 * math.sin(t * 3), 1.0)


def s_end(c, t):
    t0 = SCENES[5][0]; tr = ph('real business')
    title(c, t - t0, ['What 3M left behind', 'was the business.'] if t > tr - 0.4 else ['What 3M', 'left behind?'])
    sky_card(c, 70, 500, 940, 830, 81)
    box(c, 540, 1080, 1.0, 1.0)
    k = eo(pr(t, t0 + 0.3, 0.6)); sponge(c, 540, 1000 - 200 * k, 0.9 + 0.2 * k, 0.05 * math.sin(t * 2), 1.0)
    if t > tr - 0.3:
        for i in range(8):
            a = i * math.pi / 4 + t; rr_ = 200 + 20 * math.sin(t * 5 + i)
            c.drawLine(540 + rr_ * math.cos(a) * 0.8, 800 + rr_ * math.sin(a) * 0.6, 540 + (rr_ + 40) * math.cos(a) * 0.8, 800 + (rr_ + 40) * math.sin(a) * 0.6, S(YEL, 6))


SCENES = [(0.0, s_hook), (ph('so what was') - 0.15, s_story), (ph('then one fall') - 0.15, s_find), (ph('he gave it') - 0.15, s_smile),
          (ph('did it work') - 0.15, s_work), (ph('so the thing') - 0.15, s_end)]
SHAKES = [(ph('called scrap'), 8, 0.3), (ph("wouldn't buy"), 8, 0.3), (ph('two hundred thousand'), 8, 0.3), (ph('sales topped'), 12, 0.4), (ph('real business'), 10, 0.4)]
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
    text(c, 'From scrap box', 540, 460, 118, INK, 'Black'); f = font(124, 'Medium', italic=True); s_ = 'to $220M'; c.drawString(s_, 540 - f.measureText(s_) / 2, 600, f, P(RED))
    sky_card(c, 70, 690, 940, 750, 71)
    box(c, 540, 1180, 1.15, 1.0); sponge(c, 540, 930, 1.05, -0.06, 1.0)
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
