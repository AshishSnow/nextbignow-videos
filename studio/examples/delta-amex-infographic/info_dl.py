"""Delta x American Express in the INFOGRAPHIC paper look (no mascot). usage: still t... | nframes | range f0 f1 | cover out.png
No real logos / trade dress: generic plane (no livery), plain card with chip, names only as plain text."""
import sys, os, math, subprocess
sys.path.insert(0, '/home/claude/studio')
from info_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR


# ------------------------------------------------------------------ props
def plane(c, x, y, s=1.0, rot=0.0, t=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    wing = path([(-40, 0), (60, 0), (-30, 150), (-90, 150)]); shape(c, wing, BLUE, 4)
    tail = path([(-250, -10), (-200, -10), (-260, -110), (-290, -110)]); shape(c, tail, RED, 4)
    body = skia.Path(); body.moveTo(-280, -20); body.cubicTo(-200, -55, 150, -55, 230, -30); body.cubicTo(290, -15, 290, 20, 230, 30)
    body.cubicTo(150, 50, -200, 45, -280, 20); body.close(); shape(c, body, WHITE, 5)
    for i in range(9): c.drawCircle(-180 + i * 40, -10, 9, P(SKY2)); c.drawCircle(-180 + i * 40, -10, 9, S(INK, 2))
    shape(c, path([(205, -32), (250, -24), (240, -6), (200, -10)]), NAVY, 2.5)
    c.drawLine(-270, 12, 240, 14, S(RED, 5))
    wing2 = path([(-30, -10), (40, -10), (-40, -120), (-80, -120)]); shape(c, wing2, BLUE, 4)
    c.restore()


def ccard(c, x, y, w=340, rot=0.0, label='CO-BRAND CARD', col=None, wings=0.0, t=0.0):
    col = col or NAVY; h = w * 0.63
    c.save(); c.translate(x, y); c.rotate(rot)
    if wings > 0:   # the payoff image: a card with wings
        for sx in (-1, 1):
            fl = math.sin(t * 9) * 12 * wings
            c.save(); c.scale(sx, 1)
            for i in range(4):
                f = path([(w / 2 - 20, -h * 0.25 + i * 18), (w / 2 + 170 * wings - i * 25, -h * 0.55 - fl + i * 30), (w / 2 + 150 * wings - i * 25, -h * 0.4 - fl + i * 34), (w / 2 - 20, -h * 0.05 + i * 18)])
                shape(c, f, WHITE, 3.5)
            c.restore()
    c.drawRRect(rr(-w / 2 + 8, -h / 2 + 10, w, h, w * 0.06), P(INK, 0.15))
    shape(c, rr(-w / 2, -h / 2, w, h, w * 0.06), col, 5)
    shape(c, rr(-w / 2 + w * 0.1, -h / 2 + h * 0.3, w * 0.16, h * 0.22, 6), YEL, 3)
    for i in range(4): c.drawLine(-w / 2 + w * 0.1 + i * w * 0.18, h * 0.22, -w / 2 + w * 0.1 + i * w * 0.18 + w * 0.13, h * 0.22, S(WHITE, 5, 0.8))
    if label: text(c, label, 0, -h / 2 + h * 0.18, w * 0.07, WHITE, 'SemiBold', maxw=w * 0.8)
    c.restore()


def bank(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape(c, path([(-150, -170), (0, -250), (150, -170)]), WHITE, 5)
    shape(c, skia.Rect.MakeXYWH(-140, -170, 280, 26), WHITE, 4)
    for i in range(4): shape(c, skia.Rect.MakeXYWH(-115 + i * 70, -144, 34, 124), WHITE, 4)
    shape(c, skia.Rect.MakeXYWH(-160, -20, 320, 26), WHITE, 4)
    c.restore()


def miles(c, x, y, r=46, label='MILES'):
    c.drawCircle(x, y, r, P(YEL)); c.drawCircle(x, y, r, S(INK, 4)); c.drawCircle(x, y, r * 0.75, S(INK, 2))
    text(c, label, x, y + r * 0.18, r * 0.42, INK, 'Bold', maxw=r * 1.4)


def cash(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    shape(c, rr(-90, -45, 180, 90, 8), (150, 170, 120), 4); c.drawCircle(0, 0, 26, P(WHITE, 0.7)); c.drawCircle(0, 0, 26, S(INK, 2.5))
    text(c, '$', 0, 13, 36, INK, 'Bold'); c.restore()


def bar(c, x, base, w, h, col, lab, val, k):
    if k <= 0: return
    hh = h * eo(k)
    c.drawRRect(rr(x + 8, base - hh + 10, w, hh, 14), P(INK, 0.14)); shape(c, rr(x, base - hh, w, hh, 14), col, 5)
    text(c, val, x + w / 2, base - hh - 26, 64, INK, 'Black', a=cl(k * 2))
    text(c, lab[0], x + w / 2, base + 56, 36, INK, 'SemiBold'); text(c, lab[1], x + w / 2, base + 98, 30, GREY, 'Medium')


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tb = ph('but one'); tc = ph('credit card')
    title(c, t + 1.0, ["The airline's", 'biggest paycheck'])
    sky_card(c, 70, 500, 940, 830, 21)
    fly = 1.0 - eo(pr(t, tb, 0.8)) * 0.25
    plane(c, 540 + 30 * math.sin(t * 1.3) - (1 - fly) * 400, 800 - 10 * math.sin(t * 2), 1.15 * fly, -0.04)
    chip(c, '200M+ customers in 2025', 540, 1150, WHITE, 34)
    if t > tc - 0.3:
        pop(c, pr(t, tc - 0.3, 0.45), 640, 900, lambda: ccard(c, 650, 900, 400, -6))
    if t > ph("didn't come") - 0.1: check(c, 860, 640, 40, False, pr(t, ph("didn't come") - 0.1, 0.3))


def s_how(c, t):
    t0 = SCENES[1][0]; ts = ph('swipe'); tm = ph('you earn'); tp = ph('pays delta')
    title(c, t - t0, ['How an airline makes', 'money from a card'])
    card(c, 70, 500, 940, 830, CARD_SKY)
    # flow: card -> miles -> bank -> plane, with cash flowing back
    k1 = pr(t, t0 + 0.25, 0.4); k2 = pr(t, tm - 0.2, 0.4); k3 = pr(t, ph('american express pays') - 0.2, 0.4); k4 = pr(t, tp - 0.2, 0.4)
    if k1 > 0: pop(c, k1, 270, 720, lambda: (ccard(c, 270 + 30 * math.sin(pr(t, ts - 0.2, 0.4) * math.pi), 700, 310, -8, 'DELTA CARD'), text(c, 'You swipe', 270, 880, 40, INK, 'Bold')))
    if k2 > 0: pop(c, k2, 780, 720, lambda: (miles(c, 730, 700, 70), miles(c, 840, 740, 58), text(c, 'You earn miles', 780, 880, 40, INK, 'Bold')))
    arrow(c, 450, 710, 640, 710, k2, RED, 7)
    if k3 > 0: pop(c, k3, 270, 1080, lambda: (bank(c, 270, 1150, 0.9), text(c, 'American Express', 270, 1230, 38, INK, 'Bold')))
    arrow(c, 740, 810, 400, 960, k3, RED, 7, -0.15)
    if k4 > 0: pop(c, k4, 780, 1080, lambda: (plane(c, 790, 1080, 0.55, -0.05), text(c, 'Delta', 780, 1230, 42, INK, 'Bold')))
    if k4 > 0:
        arrow(c, 430, 1100, 590, 1100, k4, (96, 116, 64), 7)
        for i in range(3):
            u = (t * 0.8 + i / 3) % 1; cash(c, 450 + 140 * u, 1050 - 20 * math.sin(u * math.pi), 0.35)


def s_money(c, t):
    t0 = SCENES[2][0]; te = ph('eight point')
    title(c, t - t0, ['Paid to Delta', 'in 2025'])
    sky_card(c, 70, 500, 940, 830, 33)
    for i in range(7):
        u = (t * 0.35 + i / 7) % 1; cash(c, 140 + i * 130, 560 + 620 * u, 0.55, math.sin(t * 2 + i) * 0.4)
    if t > te - 0.3:
        def big():
            card(c, 130, 780, 820, 260, YEL, 30)
            text(c, '$8.2 billion', 540, 920, 124, INK, 'Black'); text(c, 'from American Express', 540, 990, 40, INK, 'SemiBold')
        pop(c, pr(t, te - 0.3, 0.45), 540, 910, big)
    chip(c, "Delta's 2025 results", 540, 1180, WHITE, 32)


def s_compare(c, t):
    t0 = SCENES[3][0]; tf = ph('five point'); tm = ph('brought in more')
    title(c, t - t0, ['Is that', 'a lot?'])
    card(c, 70, 500, 940, 830, WHITE)
    c.drawLine(150, 1150, 930, 1150, S(INK, 4))
    bar(c, 210, 1150, 260, 520, RED, ('Card deal', 'paid by Amex'), '$8.2B', pr(t, SCENES[3][0] + 0.2, 0.7))
    bar(c, 610, 1150, 260, 520 * 5.8 / 8.2, NAVY, ('Operating profit', 'whole airline'), '$5.8B', pr(t, tf - 0.2, 0.7))
    if t > tm - 0.2: check(c, 520, 700, 44, True, pr(t, tm - 0.2, 0.3))


def s_end(c, t):
    t0 = SCENES[4][0]; tw = ph('with wings')
    title(c, t - t0, ["Delta isn't just", 'an airline'] if t < tw - 0.3 else ['A credit card', 'with wings.'])
    sky_card(c, 70, 500, 940, 830, 41)
    wk = eo(pr(t, tw - 0.4, 0.5))
    ccard(c, 540, 860 - 60 * wk + 14 * math.sin(t * 3) * wk, 420 + 40 * wk, -4 + 4 * wk, 'DELTA CARD', NAVY, wk, t)
    if wk <= 0.01: plane(c, 540, 1130, 0.5, -0.03)


SCENES = [(0.0, s_hook), (ph('so how does') - 0.15, s_how), (ph('last year delta') - 0.15, s_money), (ph('is that a lot') - 0.15, s_compare), (ph("so delta isn't") - 0.15, s_end)]
SHAKES = [(ph('credit card'), 8, 0.3), (ph('eight point'), 12, 0.4), (ph('brought in more'), 8, 0.3), (ph('with wings'), 10, 0.4)]
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
    text(c, "Delta's biggest", 540, 460, 120, INK, 'Black'); f = font(130, 'Medium', italic=True); s_ = 'paycheck?'; c.drawString(s_, 540 - f.measureText(s_) / 2, 600, f, P(RED))
    sky_card(c, 70, 680, 940, 760, 21)
    plane(c, 470, 900, 0.9, -0.05)
    ccard(c, 640, 1170, 440, -6, 'CO-BRAND CARD')
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
