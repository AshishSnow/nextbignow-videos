"""Returns Short (built on gift-card renderer), DAY COMIC look (from car-dealer render_neon.py) (owner approved 18 Nov 13:21). 10 drawn scenes, text lives in the world (neon, screens, notes),
camera push + drift, blinking/sweating characters, coin bursts, shake on reveals. One render pass writes BOTH cuts:
ig = full frame + subs at y 1442;  yt = frame scaled 0.85 into YouTube's safe box over a blurred copy, subs at y 1320.
usage: python3 render_neon.py still t1 t2 ... | range f0 f1 (writes out/ig_f0.mp4 + out/yt_f0.mp4)"""
import sys, os, math, re, json, random, subprocess
import numpy as np
import skia
from neon import *
import neon as N

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, 'comic', 'cd')
FPS = 30
AL = [x for x in json.load(open(os.path.join(D, 'align.json'))) if x[0] not in ('<s>', '</s>', '<sil>')]
TOK = [(w.lower().strip("'"), a, b) for w, a, b in AL]


def ph(text_, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z0-9']+", text_.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j] for j in range(len(q))): return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text_)


END = TOK[-1][2] + 0.5
DUR = END + 1.2


def cl(x): return max(0.0, min(1.0, x))
def pr(t, t0, d): return cl((t - t0) / d)
def eo(x): return 1 - (1 - x) ** 3
def eio(x): return 3 * x * x - 2 * x * x * x
def eback(x, s=1.70158): x -= 1; return x * x * ((s + 1) * x + s) + 1


def pop(c, k, x, y, fn):
    if k <= 0: return
    s = eback(cl(k), 2.0); c.save(); c.translate(x, y); c.scale(s, s); c.translate(-x, -y); fn(); c.restore()


def blinking(t, seed=0): return ((t + seed * 1.7) % 3.3) < 0.12


# ------------------------------------------------------------------ extra props
def screen(c, x, y, w, h, draw, glowc=(80, 200, 255), on=1.0):
    c.drawRoundRect(skia.Rect.MakeXYWH(x - 30, y - 30, w + 60, h + 60), 30, 30, P(glowc, 0.35 * on, 50))
    fr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 16, y - 16, w + 32, h + 32), 22, 22); inked(c, fr, P((20, 18, 30)), 7)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, w, h))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), LG((x, y), (x, y + h), [(14, 20, 40), (30, 20, 60)]))
    c.translate(x, y); draw(c); c.restore()
    for i in range(0, int(h), 6): c.drawRect(skia.Rect.MakeXYWH(x, y + i, w, 2), P((0, 0, 0), 0.12))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h * 0.3), P((255, 255, 255), 0.04))


def ctext(c, s, x, y, size, rgb, fn='Montserrat-Black.ttf', a=1.0):
    f = font(fn, size); c.drawString(s, x - f.measureText(s) / 2, y, f, P(rgb, a))


def bar(c, x, base, w, h, rgb, lab, val, k):
    hh = h * eo(cl(k))
    if k <= 0: return
    c.drawRoundRect(skia.Rect.MakeXYWH(x, base - hh, w, hh), 14, 14, P(rgb, 0.4, 18))
    c.drawRoundRect(skia.Rect.MakeXYWH(x, base - hh, w, hh), 14, 14, LG((x, base - hh), (x, base), [tuple(min(255, v + 60) for v in rgb), rgb]))
    ctext(c, val, x + w / 2, base - hh - 24, 84, rgb, a=cl(k * 2))
    ctext(c, lab, x + w / 2, base + 56, 34, (220, 220, 240), 'Montserrat-ExtraBold.ttf')


def paper(c, x, y, rot, label, k, t):
    if k <= 0: return
    c.save(); c.translate(x, y + 8 * math.sin(t * 2 + x)); c.rotate(rot + 4 * math.sin(t * 1.3 + y)); s = eback(cl(k), 2); c.scale(s, s)
    r = skia.Rect.MakeXYWH(-150, -95, 300, 190); c.drawRect(r.makeOffset(10, 12), P((0, 0, 0), 0.4, 8)); inked(c, r, P((252, 248, 236)), 6)
    ctext(c, label, 0, -30, 40, (40, 30, 60));
    for i in range(3): c.drawLine(-110, 10 + i * 26, 110 - i * 30, 10 + i * 26, S((170, 170, 190), 6))
    c.drawLine(-110, 80, 0, 80, S((40, 30, 60), 4)); c.restore()


def door_glow(c, x, y, w, h, k_open):
    c.drawPath(path([(x, y + h), (x + w, y + h), (x + w + 420 * k_open, 1920), (x - 420 * k_open, 1920)]), LG((0, y + h), (0, 1920), [(255, 200, 80, 0.45 * k_open), (255, 200, 80, 0.0)]))
    c.drawRect(skia.Rect.MakeXYWH(x - 26, y - 26, w + 52, h + 26), P((70, 40, 30))); c.drawRect(skia.Rect.MakeXYWH(x - 26, y - 26, w + 52, h + 26), S(INK, 7))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), RG(x + w / 2, y + h / 2, h, [(255, 250, 200), (255, 190, 60)]))
    c.drawCircle(x + w / 2, y + h / 2, 300, P((255, 210, 90), 0.4 * k_open, 80))
    dw = w * (1 - 0.8 * eio(k_open))
    dp = path([(x, y), (x + dw, y + 30 * k_open), (x + dw, y + h - 30 * k_open), (x, y + h)]); inked(c, dp, LG((x, 0), (x + dw, 0), [(120, 40, 60), (80, 20, 40)]), 6)
    c.drawCircle(x + dw - 26, y + h / 2, 12, P((255, 210, 90))); c.drawCircle(x + dw - 26, y + h / 2, 12, S(INK, 4))


def small_car(c, x, y, s, col, t):
    N.car(c, x, y, 760 * s, body=col, t=t, refl=False)


def building(c, x, y, w, h, col, sign, sign_col, t, glass=True):
    c.drawRect(skia.Rect.MakeXYWH(x + 14, y + 14, w, h), P((0, 0, 0), 0.4, 10))
    inked(c, skia.Rect.MakeXYWH(x, y, w, h), LG((x, y), (x, y + h), [tuple(min(255, v + 30) for v in col), col]), 7)
    if glass:
        for i in range(3):
            r = skia.Rect.MakeXYWH(x + 30 + i * (w - 60) / 3, y + h * 0.35, (w - 60) / 3 - 14, h * 0.6); inked(c, r, LG((0, r.top()), (0, r.bottom()), [(140, 120, 220), (60, 40, 120)]), 5)
            c.drawRect(skia.Rect.MakeXYWH(r.left() + 10, r.top() + 10, 14, r.height() - 20), P((255, 255, 255), 0.2))
    else:
        r = skia.Rect.MakeXYWH(x + 30, y + h * 0.35, w - 60, h * 0.6); inked(c, r, P((255, 200, 120)), 5)
        for j in range(5): c.drawLine(x + 30, y + h * 0.35 + j * h * 0.12, x + w - 30, y + h * 0.35 + j * h * 0.12, S((200, 140, 60), 4))
        c.drawCircle(x + w / 2, y + h * 0.65, w * 0.6, P((255, 180, 80), 0.25, 60))
    neon_text(c, sign, x + w / 2, y + h * 0.24, min(64, (w - 40) / max(1, len(sign)) * 1.6), sign_col, 1.0 if (t % 2.7) > 0.08 else 0.4)


# ------------------------------------------------------------------ gift card props
CARDCOLS = [(255, 80, 110), (40, 170, 255), (255, 190, 30), (60, 200, 120), (170, 100, 255), (255, 130, 40)]


def giftcard(c, x, y, w, rot, col, label='', a=1.0, dust=0.0, sparkle_=True, t=0.0):
    h = w * 0.63
    c.save(); c.translate(x, y); c.rotate(rot)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), w * 0.07, w * 0.07)
    c.drawRRect(r.makeOffset(w * 0.03, w * 0.04) if hasattr(r, 'makeOffset') else r, P(INK, 0.3 * a, 6))
    c.drawRRect(r, LG((-w / 2, -h / 2), (w / 2, h / 2), [tuple(min(255, v + 60) for v in col) + (a,), col + (a,), tuple(int(v * 0.75) for v in col) + (a,)]))
    c.save(); c.clipRRect(r, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h * 0.18, w, h * 0.16), P((255, 255, 255), 0.85 * a))
    c.drawRect(skia.Rect.MakeXYWH(w * 0.05, -h / 2, w * 0.1, h), P((255, 255, 255), 0.85 * a))
    c.drawPath(path([(-w / 2, -h / 2), (-w * 0.1, -h / 2), (-w * 0.45, h / 2), (-w / 2, h / 2)]), P((255, 255, 255), 0.18 * a))
    c.restore()
    bw = skia.Path(); bw.addCircle(w * 0.1 - w * 0.07, -h * 0.1, w * 0.07); bw.addCircle(w * 0.1 + w * 0.07, -h * 0.1, w * 0.07)
    c.drawPath(bw, P((255, 255, 255), a)); c.drawPath(bw, S(INK, max(2, w * 0.012), a))
    if label: ctext(c, label, -w * 0.2, h * 0.36, w * 0.17, (255, 255, 255), 'Anton.ttf', a=a)
    c.drawRRect(r, S(INK, max(3, w * 0.018), a))
    if dust > 0:
        c.save(); c.clipRRect(r, doAntiAlias=True); c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), P((150, 140, 120), 0.45 * dust))
        rnd = random.Random(int(w)); [c.drawCircle(rnd.uniform(-w / 2, w / 2), rnd.uniform(-h / 2, h / 2), rnd.uniform(1, 4), P((90, 80, 70), 0.6 * dust)) for _ in range(60)]
        c.restore()
        web = skia.Path(); cx, cy = w / 2, -h / 2
        for k in range(5): a_ = math.radians(90 + k * 22); web.moveTo(cx, cy); web.lineTo(cx + math.cos(a_) * w * 0.35, cy + math.sin(a_) * w * 0.35)
        for rr in (0.12, 0.22, 0.32):
            for k in range(4):
                a1, a2 = math.radians(90 + k * 22), math.radians(90 + (k + 1) * 22)
                web.moveTo(cx + math.cos(a1) * w * rr, cy + math.sin(a1) * w * rr); web.quadTo(cx + math.cos((a1 + a2) / 2) * w * rr * 0.85, cy + math.sin((a1 + a2) / 2) * w * rr * 0.85, cx + math.cos(a2) * w * rr, cy + math.sin(a2) * w * rr)
        c.drawPath(web, S((255, 255, 255), 2.5, 0.9 * dust))
    c.restore()
    if sparkle_ and dust <= 0: sparkle(c, x + w * 0.38, y - h * 0.4, w * 0.08, max(0.0, math.sin(t * 3 + x)) * a)


def cup(c, x, y, s=1.0, steam=0.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    body = path([(-55, -120), (55, -120), (42, 40), (-42, 40)]); inked(c, body, LG((-55, 0), (55, 0), [(255, 255, 255), (230, 235, 240)]), 6)
    sl = path([(-50, -70), (50, -70), (46, -20), (-46, -20)]); inked(c, sl, P((190, 130, 80)), 5)
    lid = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-64, -146, 128, 30), 10, 10); inked(c, lid, P((250, 250, 252)), 6)
    if steam > 0:
        for k in range(3):
            p = skia.Path(); x0 = -20 + k * 20; p.moveTo(x0, -160)
            for j in range(1, 6): p.lineTo(x0 + 10 * math.sin(t * 4 + j + k), -160 - j * 18)
            c.drawPath(p, S((255, 255, 255), 6, 0.7 * steam))
    c.restore()


def cash(c, x, y, rot, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    r = skia.Rect.MakeXYWH(-90, -45, 180, 90); inked(c, r, LG((0, -45), (0, 45), [(170, 230, 160), (110, 190, 110)]), 5)
    c.drawOval(skia.Rect.MakeXYWH(-30, -30, 60, 60), S((60, 130, 60), 4)); ctext(c, '$', 0, 16, 44, (40, 110, 40), 'Anton.ttf')
    c.restore()


def register(c, rx, ry, k_open=0.0, sticky_txt=None, t=0.0):
    reg = path([(rx - 170, ry), (rx + 170, ry), (rx + 140, ry - 170), (rx - 140, ry - 170)]); inked(c, reg, LG((0, ry - 170), (0, ry), [(120, 210, 255), (40, 140, 220)]), 7)
    scr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(rx - 80, ry - 260, 160, 80), 10, 10); inked(c, scr, P((20, 40, 50)), 6)
    ctext(c, 'PAID', rx, ry - 205, 44, (80, 255, 140), 'Anton.ttf')
    for i in range(3):
        for j in range(4): c.drawRoundRect(skia.Rect.MakeXYWH(rx - 110 + j * 58, ry - 150 + i * 44, 44, 32), 6, 6, P((255, 255, 255), 0.85))
    inked(c, skia.Rect.MakeXYWH(rx - 190, ry + 50 * k_open - 10, 380, 60), P((30, 110, 190)), 7)
    if sticky_txt: sticky(c, rx + 10, ry - 420, 1.15, -6, sticky_txt, size=40)


def kitchen_bg(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(255, 250, 240), (240, 232, 215)]))
    wr = skia.Rect.MakeXYWH(560, 470, 440, 400); skyline(c, 560, 470, 440, 400, t, 3); c.drawRect(wr, S((255, 255, 255), 18)); c.drawRect(wr.makeOutset(9, 9), S(INK, 6))
    c.drawLine(780, 470, 780, 870, S((255, 255, 255), 12))
    for i in range(3):
        r = skia.Rect.MakeXYWH(60 + i * 160, 470, 150, 300); inked(c, r, LG((0, 470), (0, 770), [(120, 220, 210), (70, 190, 180)]), 6)
        c.drawRoundRect(skia.Rect.MakeXYWH(60 + i * 160 + 110, 600, 14, 50), 7, 7, P(INK))
    inked(c, skia.Rect.MakeXYWH(20, 1040, 1040, 40), LG((0, 1040), (0, 1080), [(255, 255, 255), (220, 225, 235)]), 6)
    c.drawRect(skia.Rect.MakeXYWH(40, 1080, 1000, 840), LG((0, 1080), (0, H), [(120, 220, 210), (60, 170, 165)])); c.drawRect(skia.Rect.MakeXYWH(40, 1080, 1000, 840), S(INK, 6))
    for i in range(1, 3): c.drawLine(40 + i * 333, 1080, 40 + i * 333, 1920, S(INK, 5))
    c.drawRoundRect(skia.Rect.MakeXYWH(140, 1160, 140, 18), 9, 9, P(INK)); c.drawRoundRect(skia.Rect.MakeXYWH(800, 1160, 140, 18), 9, 9, P(INK))


def drawer(c, x, y, w, k_open, cards_k, t, dust=0.0):
    d = 140 * eo(k_open)
    inner = path([(x - w / 2, y), (x + w / 2, y), (x + w / 2 - 30, y - d), (x - w / 2 + 30, y - d)]); inked(c, inner, P((150, 90, 50)), 6)
    rnd = random.Random(5)
    for i in range(9):
        kk = pr(cards_k, i * 0.07, 0.5)
        if kk <= 0: continue
        cx = x - w * 0.36 + i * w * 0.09 + rnd.uniform(-10, 10); cy = y - d * 0.5 - 140 * eo(kk) + rnd.uniform(-20, 20)
        giftcard(c, cx, cy, 170, rnd.uniform(-35, 35), CARDCOLS[i % 6], '', 1.0, dust * (1 if i == 4 else 0.6), t=t)
    front = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2 - 10, y, w + 20, 170), 16, 16); inked(c, front, LG((0, y), (0, y + 170), [(130, 230, 220), (70, 190, 180)]), 7)
    c.drawRoundRect(skia.Rect.MakeXYWH(x - 90, y + 70, 180, 24), 12, 12, P(INK))


def people(c, x0, y, n, s, hl, k, t, grey=None, hold=True):
    for i in range(n):
        kk = pr(k, i * 0.05, 0.3)
        if kk <= 0: continue
        x = x0 + i * 170 * s
        g = (grey is not None and i == grey)
        hc = (170, 170, 180) if g else [(255, 140, 40), (70, 140, 255), (60, 200, 120), (255, 90, 120), (170, 110, 255)][i % 5]
        jc = (150, 150, 160) if g else [(36, 44, 90), (200, 60, 70), (40, 120, 90), (90, 60, 140), (230, 160, 40)][i % 5]
        pop(c, kk, x, y, lambda: person(c, x, y, 0.28 * s, hc, jc, mood='neutral' if g else 'happy', t=t, blink=blinking(t, i)))
        if hold and i < hl:
            giftcard(c, x + 50 * s, y - 120 * s, 70 * s, -15, CARDCOLS[i % 6], '', kk, (0.8 if g else 0), sparkle_=False)


def lerp(a, b, u): return a + (b - a) * u


BOXC = [(214, 160, 100), (200, 145, 85), (226, 175, 115)]


def box(c, x, y, w, h=None, rot=0.0, col=None, tape=True, label=None, open_=0.0):
    h = h or w * 0.75; col = col or BOXC[int(abs(x * 7 + y)) % 3]
    c.save(); c.translate(x, y); c.rotate(rot)
    top = h * 0.22
    c.drawRect(skia.Rect.MakeXYWH(-w / 2 + 8, -h / 2 + 10, w, h), P(INK, 0.25, 5))
    inked(c, skia.Rect.MakeXYWH(-w / 2, -h / 2 + top, w, h - top), LG((0, -h / 2), (0, h / 2), [col, tuple(int(v * 0.85) for v in col)]), max(3, w * 0.025))
    lid = path([(-w / 2, -h / 2 + top), (w / 2, -h / 2 + top), (w / 2 - w * 0.08, -h / 2), (-w / 2 + w * 0.08, -h / 2)])
    if open_ > 0:
        for sx in (-1, 1):
            fl = path([(0, -h / 2 + top), (sx * w / 2, -h / 2 + top), (sx * (w / 2 + w * 0.25 * open_), -h / 2 + top - h * 0.5 * open_), (sx * w * 0.1, -h / 2 + top - h * 0.45 * open_)])
            inked(c, fl, P(tuple(min(255, v + 20) for v in col)), max(3, w * 0.02))
        c.drawRect(skia.Rect.MakeXYWH(-w / 2 + 6, -h / 2 + top, w - 12, h * 0.12), P(INK, 0.5))
    else:
        inked(c, lid, P(tuple(min(255, v + 25) for v in col)), max(3, w * 0.022))
        if tape: c.drawRect(skia.Rect.MakeXYWH(-w * 0.08, -h / 2, w * 0.16, h * 0.55), P((240, 225, 170), 0.9))
    if label: ctext(c, label, 0, h * 0.28, w * 0.2, (60, 40, 20), 'Anton.ttf')
    c.restore()


def pallet(c, x, y, w):
    for i in range(3): inked(c, skia.Rect.MakeXYWH(x - w / 2 + i * (w - 40) / 2, y + 22, 40, 30), P((170, 120, 70)), 4)
    inked(c, skia.Rect.MakeXYWH(x - w / 2, y, w, 24), P((200, 150, 90)), 5)
    inked(c, skia.Rect.MakeXYWH(x - w / 2, y + 50, w, 18), P((190, 140, 80)), 4)


def tv(c, x, y, w, t=0.0, a=1.0):
    h = w * 0.6
    c.save(); c.translate(x, y)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 18, 18); inked(c, r, P((30, 30, 40)), 7)
    sc = skia.Rect.MakeXYWH(-w / 2 + 16, -h / 2 + 16, w - 32, h - 32)
    c.drawRect(sc, LG((0, -h / 2), (0, h / 2), [(60, 200, 255), (120, 90, 255), (255, 120, 200)]))
    c.drawPath(path([(-w / 2 + 16, -h / 2 + 16), (-w * 0.05, -h / 2 + 16), (-w * 0.3, h / 2 - 16), (-w / 2 + 16, h / 2 - 16)]), P((255, 255, 255), 0.25))
    c.drawLine(-w * 0.15, h / 2, -w * 0.25, h / 2 + 60, S(INK, 12)); c.drawLine(w * 0.15, h / 2, w * 0.25, h / 2 + 60, S(INK, 12))
    c.restore()


def sky_bg(c, t, ground=(150, 220, 160)):
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(20, 130, 235), (110, 200, 255), (230, 245, 255)], [0, 0.5, 1]))
    c.drawCircle(880, 300, 90, P((255, 255, 230))); c.drawCircle(880, 300, 200, P((255, 255, 220), 0.5, 70))
    cloud(c, 80 + 20 * math.sin(t * 0.3), 560, 0.6); cloud(c, 700 - 15 * math.sin(t * 0.25), 680, 0.5)
    c.drawRect(skia.Rect.MakeXYWH(0, 1350, W, 570), LG((0, 1350), (0, H), [ground, tuple(int(v * 0.8) for v in ground)]))


# ------------------------------------------------------------------ grocery props
def milk(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    inked(c, path([(-50, -60), (50, -60), (50, 110), (-50, 110)]), LG((-50, 0), (50, 0), [(255, 255, 255), (225, 235, 245)]), 6)
    inked(c, path([(-50, -60), (0, -110), (50, -60)]), P((80, 160, 255)), 6)
    c.drawRect(skia.Rect.MakeXYWH(-50, -10, 100, 50), P((80, 160, 255))); ctext(c, 'MILK', 0, 28, 30, (255, 255, 255), 'Anton.ttf')
    c.restore()


def bread(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-80, -40, 160, 80), 40, 40)); inked(c, p, LG((0, -40), (0, 40), [(240, 180, 100), (200, 130, 60)]), 6)
    for i in range(3): c.drawLine(-40 + i * 40, -30, -30 + i * 40, 30, S((170, 100, 40), 5))
    c.restore()


def apple(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 0, 38, RG(-12, -12, 50, [(255, 120, 120), (220, 40, 50), (160, 20, 30)])); c.drawCircle(0, 0, 38, S(INK, 5))
    c.drawLine(0, -36, 6, -54, S((110, 70, 30), 6)); c.drawOval(skia.Rect.MakeXYWH(6, -58, 26, 14), P((60, 180, 80))); c.restore()


def cart(c, x, y, s=1.0, full=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if full > 0:
        milk(c, -60, -170, 0.9, -8); bread(c, 40, -150, 0.9, 10); apple(c, 110, -130, 1.0); apple(c, -130, -130, 0.9)
    basket = path([(-180, -140), (180, -140), (150, 20), (-150, 20)])
    c.drawPath(basket, P((200, 220, 240), 0.5)); c.drawPath(basket, S(INK, 7))
    for i in range(1, 6): c.drawLine(-180 + i * 60, -140, -150 + i * 50, 20, S(INK, 3))
    for j in range(1, 3): c.drawLine(-175 + j * 8, -140 + j * 53, 175 - j * 8, -140 + j * 53, S(INK, 3))
    c.drawLine(180, -140, 240, -200, S(INK, 9)); c.drawLine(-150, 20, -120, 60, S(INK, 7)); c.drawLine(150, 20, 130, 60, S(INK, 7))
    c.drawLine(-140, 60, 150, 60, S(INK, 7))
    for wx in (-110, 120): c.drawCircle(wx, 80, 22, P(INK)); c.drawCircle(wx, 80, 9, P((200, 200, 210)))
    c.restore()


def phone(c, x, y, s, rot, draw):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-160, -290, 320, 580), 40, 40); c.drawRRect(r.makeOffset(10, 12) if hasattr(r, 'makeOffset') else r, P(INK, 0.3, 6)); inked(c, r, P((30, 30, 40)), 8)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(-140, -260, 280, 520)); c.drawRect(skia.Rect.MakeXYWH(-140, -260, 280, 520), P((255, 255, 255))); c.translate(-140, -260); draw(c); c.restore()
    c.restore()


def moneybag(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    b = skia.Path(); b.moveTo(-30, -70); b.cubicTo(-110, -40, -110, 80, 0, 80); b.cubicTo(110, 80, 110, -40, 30, -70); b.close()
    inked(c, b, LG((0, -70), (0, 80), [(150, 220, 140), (80, 170, 90)]), 6)
    inked(c, path([(-34, -70), (34, -70), (20, -95), (-20, -95)]), P((120, 200, 120)), 5)
    ctext(c, '$', 0, 30, 70, (30, 100, 40), 'Anton.ttf'); c.restore()


def store_inside(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(240, 250, 255), (215, 238, 252)]))
    for row in range(3):
        y = 520 + row * 170
        inked(c, skia.Rect.MakeXYWH(40, y + 120, 1000, 18), P((200, 210, 225)), 4)
        rnd = random.Random(row)
        for i in range(12):
            x = 70 + i * 82; col = [(255, 90, 110), (40, 170, 255), (255, 190, 30), (60, 200, 120), (170, 100, 255)][rnd.randint(0, 4)]
            hh = rnd.randint(70, 110); inked(c, skia.Rect.MakeXYWH(x, y + 120 - hh, 60, hh), P(col), 3)
            c.drawRect(skia.Rect.MakeXYWH(x + 8, y + 120 - hh + 15, 44, 14), P((255, 255, 255), 0.85))
    c.drawRect(skia.Rect.MakeXYWH(0, 1100, W, 820), LG((0, 1100), (0, H), [(230, 235, 245), (190, 200, 215)]))
    for i in range(-6, 7): c.drawLine(540 + i * 60, 1100, 540 + i * 300, H, S((255, 255, 255), 3, 0.6))


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    th = ph('the real money')
    sky_bg(c, t, (170, 180, 195))
    building(c, 110, 760, 860, 560, (255, 245, 230), 'GROCERY', (40, 170, 90), t, True)
    board(c, 70, 250, 940, 200)
    neon_text(c, 'YOUR GROCERY STORE', 540, 340, 66, (40, 170, 90))
    neon_text(c, 'BARELY PROFITS ON FOOD', 540, 425, 60, (255, 70, 90))
    kx = pr(t, 0.0, 1.6)
    cart(c, lerp(-150, 700, eo(kx)), 1600, 1.0, 1.0, t)
    person(c, lerp(-420, 300, eo(kx)), 1700, 0.62, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.7, -0.2), t=t, arm_r=(200, -120), arm_l=(160, -80), blink=blinking(t))
    if t > th - 0.3:
        k = pr(t, th - 0.3, 0.4)
        burst_k = k
        pop(c, k, 760, 1000, lambda: (board(c, 600, 930, 320, 140, (255, 236, 90)), neon_text(c, '???', 760, 1030, 90, (255, 70, 90))))


def s_margin(c, t):
    t2 = ph('two cents'); tc = ph('hundred dollar'); tl = ph('the lights')
    store_inside(c, t)
    inked(c, skia.Rect.MakeXYWH(20, 1250, 1040, 50), LG((0, 1250), (0, 1300), [(255, 255, 255), (220, 225, 235)]), 7)
    c.drawRect(skia.Rect.MakeXYWH(40, 1300, 1000, 650), LG((0, 1300), (0, H), [(60, 200, 120), (40, 160, 95)])); c.drawRect(skia.Rect.MakeXYWH(40, 1300, 1000, 650), S(INK, 7))
    register(c, 300, 1240, 0.0, None, t)
    cart(c, 760, 1690, 0.75, 1.0, t)
    rk = pr(t, tc - 0.4, 1.0)
    if rk > 0:
        rl = 500 * eo(rk); r = skia.Rect.MakeXYWH(440, 1240 - rl, 170, rl); inked(c, r, P((255, 255, 255)), 4)
        for i in range(int(rl / 40)): c.drawLine(460, 1220 - i * 40, 590 - (i % 3) * 30, 1220 - i * 40, S((170, 170, 190), 5))
        if rk > 0.6: ctext(c, '$100', 525, 1240 - rl + 60, 46, (40, 40, 60), 'Anton.ttf')
    if t > t2 - 0.3:
        k = pr(t, t2 - 0.3, 0.4)
        def big():
            coin(c, 800, 900, 140)
            neon_text(c, '2¢', 800, 935, 110, (255, 255, 255))
        pop(c, k, 800, 900, big)
        if t > t2 + 0.5: neon_text(c, 'OF EVERY $1', 800, 1100, 48, (40, 170, 90), pr(t, t2 + 0.5, 0.3))
    if t > tc: sticky(c, 800, 1180, 1.0, 6, '= ~$2', size=60) if t < tl - 0.3 else None
    for i, lab in enumerate(('LIGHTS', 'STAFF', 'FREEZERS')):
        kb = pr(t, tl - 0.3 + i * 0.35, 0.35)
        if kb > 0: bill(c, 650 + i * 140, 1150 - 40 * i, kb, t, -10 + i * 10, lab)


def bill(c, x, y, k, t, rot, s):
    if k <= 0: return
    sc = min(1, k * 1.5); c.save(); c.translate(x, y); c.rotate(rot + 4 * math.sin(t * 3 + x)); c.scale(sc, sc)
    c.drawRect(skia.Rect.MakeXYWH(-90 + 8, -110 + 8, 180, 220), P(INK, 0.3)); inked(c, skia.Rect.MakeXYWH(-90, -110, 180, 220), P((255, 252, 240)), 6)
    ctext(c, s, 0, -50, 34 if len(s) > 6 else 40, (220, 40, 60), 'Anton.ttf')
    for i in range(4): c.drawLine(-70, -10 + i * 30, 60 - (i % 2) * 40, -10 + i * 30, S((170, 170, 190), 5))
    c.restore()


def s_ads(c, t):
    ts = ph('screen at checkout'); tco = ph('the coupon'); tsp = ph('the sponsored'); ta = ph('those are ads'); tp = ph('brands pay')
    store_inside(c, t)
    if t < ta - 0.2:
        board(c, 120, 260, 840, 150); neon_text(c, "WHERE'S THE MONEY?", 540, 360, 64, (30, 160, 255))
        pop(c, pr(t, ts - 0.3, 0.35), 250, 820, lambda: (tv(c, 250, 820, 360, t), neon_text(c, 'AD', 250, 860, 110, (255, 255, 255))))
        pop(c, pr(t, tco - 0.3, 0.35), 760, 900, lambda: phone(c, 760, 900, 0.75, 6, lambda cc: (cc.drawRect(skia.Rect.MakeXYWH(20, 120, 240, 200), P((255, 236, 90))), ctext(cc, 'COUPON', 140, 200, 44, (220, 40, 60), 'Anton.ttf'), ctext(cc, '$1 OFF', 140, 270, 50, (40, 40, 60), 'Anton.ttf'))))
        def search(cc):
            for i in range(4):
                y = 40 + i * 120; cc.drawRect(skia.Rect.MakeXYWH(20, y, 240, 100), P((240, 245, 250))); cc.drawRect(skia.Rect.MakeXYWH(20, y, 70, 100), P([(255, 90, 110), (40, 170, 255), (255, 190, 30), (60, 200, 120)][i]))
                if i == 0: cc.drawRect(skia.Rect.MakeXYWH(100, y + 10, 150, 30), P((255, 214, 40))); ctext(cc, 'SPONSORED', 175, y + 34, 22, (40, 40, 60))
        pop(c, pr(t, tsp - 0.3, 0.35), 520, 1230, lambda: phone(c, 520, 1230, 0.6, -5, search))
    else:
        board(c, 120, 260, 840, 150); neon_text(c, 'THOSE ARE ADS', 540, 360, 74, (255, 70, 90))
        person(c, 780, 1700, 0.62, (70, 140, 255), (40, 170, 90), mood='happy', look=(-0.7, 0), t=t, arm_r=(-160, 120), arm_l=(-60, 220), tie=(255, 214, 40), shirt=(250, 250, 255), blink=blinking(t, 2))
        for i in range(3):
            kk = pr(t, tp - 0.2 + i * 0.25, 0.4)
            x = 200 + i * 40; y = 1700 - i * 10
            if kk > 0:
                person(c, 200 + i * 160 - 120 * (1 - eo(kk)), 1760, 0.42, [(170, 110, 255), (255, 90, 120), (60, 200, 120)][i], [(90, 60, 140), (200, 60, 70), (40, 120, 90)][i], mood='happy', t=t, arm_r=(120, -40), arm_l=(-30, 230), blink=blinking(t, i + 3))
                u = pr(t, tp + 0.3 + i * 0.25, 0.6)
                moneybag(c, lerp(260 + i * 160, 660, eio(u)), lerp(1480, 1300, eio(u)) - 80 * math.sin(math.pi * u), 0.8, -10 + 20 * u)


def s_big(c, t):
    th = ph('how big'); t64 = ph('six point four'); tm = ph('membership fees')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(30, 150, 240), (150, 215, 255)]))
    c.drawRect(skia.Rect.MakeXYWH(0, 1300, W, 620), LG((0, 1300), (0, H), [(255, 220, 170), (230, 180, 120)]))
    def d(cc):
        k = pr(t, t64 - 0.4, 0.4)
        ctext(cc, "WALMART'S AD BUSINESS", 410, 70, 40, (255, 255, 255))
        if k > 0: neon_text(cc, '~$6.4 BILLION', 410, 250, 104, (80, 230, 140), cl(k * 2))
        ctext(cc, 'FISCAL 2026, PER WALMART RESULTS', 410, 330, 24, (200, 200, 230), 'Montserrat-ExtraBold.ttf')
    screen(c, 130, 300, 820, 380, d, (80, 230, 140))
    dim = pr(t, th - 0.1, 0.4) * (1 - pr(t, t64 - 0.2, 0.25))
    if t > tm - 0.3:
        k = pr(t, tm - 0.3, 0.4)
        def card_():
            giftcard(c, 540, 1010, 560, -5, (40, 120, 220), '', 1.0, sparkle_=True, t=t)
            neon_text(c, 'MEMBERSHIP', 540, 960, 56, (255, 255, 255)); neon_text(c, '$4.3B+', 540, 1090, 100, (255, 214, 40))
        pop(c, k, 540, 1010, card_)
    else:
        rnd = random.Random(2)
        for i in range(int(16 * pr(t, t64, 1.2))):
            moneybag(c, 140 + (i * 197) % 820, 1150 - (i // 5) * 90 + rnd.uniform(-20, 20), 0.75, rnd.uniform(-20, 20))
    person(c, 900, 1800, 0.56, (255, 140, 40), (36, 44, 90), mood='shock', look=(-0.6, -0.7), sweat=2, t=t, arm_r=(40, 220), arm_l=(-40, 220), blink=blinking(t))
    if dim > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((20, 30, 60), 0.4 * dim))


def s_customer(c, t):
    tn = ph("it's not you"); tb = ph("it's the brands")
    store_inside(c, t)
    c.drawRect(skia.Rect.MakeWH(W, H), P((20, 30, 60), 0.25))
    board(c, 100, 260, 880, 150); neon_text(c, 'WHO IS THE REAL CUSTOMER?', 540, 352, 50, (30, 160, 255))
    sp = 1.0 if t < tb - 0.2 else 0.0
    light_cone(c, 280, 420, 60, 420, 1400, (255, 255, 220), 0.35 * sp + 0.05)
    light_cone(c, 780, 420, 60, 460, 1400, (255, 255, 220), 0.05 + 0.4 * (1 - sp))
    cart(c, 300, 1600, 0.7, 1.0, t)
    person(c, 260, 1800, 0.6, (255, 140, 40), (36, 44, 90), mood='happy' if t < tn else 'shock', look=(0.6, -0.4), t=t, arm_r=(100, -40), arm_l=(-30, 230), blink=blinking(t))
    for i in range(3):
        person(c, 660 + i * 150, 1780, 0.42, [(170, 110, 255), (255, 90, 120), (60, 200, 120)][i], [(90, 60, 140), (200, 60, 70), (40, 120, 90)][i], mood='happy', t=t, arm_r=(40, -200), arm_l=(-30, 230), blink=blinking(t, i))
        moneybag(c, 690 + i * 150, 1360, 0.7, 10)
    if t > tn - 0.2: pop(c, pr(t, tn - 0.2, 0.3), 260, 980, lambda: (board(c, 120, 920, 280, 110, (255, 255, 255)), neon_text(c, 'NOT YOU?', 260, 1000, 54, (255, 70, 90))))
    if t > tb - 0.2: pop(c, pr(t, tb - 0.2, 0.3), 810, 980, lambda: (board(c, 620, 920, 380, 110, (255, 236, 90)), neon_text(c, 'THE BRANDS', 810, 1000, 54, (40, 170, 90))))


def s_end(c, t):
    tm = ph('you came in'); ta = ph('your attention'); tq = ph('do you ever')
    sky_bg(c, t)
    if t < tq - 0.3:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'YOU CAME FOR MILK', 540, 355, 70, (30, 160, 255)); neon_text(c, 'THEY CAME FOR YOU', 540, 440, 70, (255, 70, 90), pr(t, ta - 0.6, 0.3))
        pop(c, pr(t, tm, 0.4), 330, 1100, lambda: milk(c, 330, 1100, 2.2, -8))
        if t > ta - 0.4:
            def eye():
                c.drawOval(skia.Rect.MakeXYWH(620, 950, 300, 170), P((255, 255, 255))); c.drawOval(skia.Rect.MakeXYWH(620, 950, 300, 170), S(INK, 8))
                c.drawCircle(770 + 20 * math.sin(t * 2), 1035, 60, P((40, 120, 220))); c.drawCircle(770 + 20 * math.sin(t * 2), 1035, 28, P(INK)); c.drawCircle(755, 1020, 10, P((255, 255, 255)))
            pop(c, pr(t, ta - 0.4, 0.4), 770, 1035, eye)
    else:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'DO YOU TAP THE', 540, 355, 70, (30, 160, 255)); neon_text(c, 'SPONSORED STUFF?', 540, 440, 70, (255, 190, 30))
        for x, lab, col in ((300, 'YES', (40, 190, 110)), (780, 'NO', (255, 70, 90))):
            pop(c, pr(t, tq + 0.3, 0.3), x, 650, lambda: (board(c, x - 130, 590, 260, 120, col), neon_text(c, lab, x, 680, 80, (255, 255, 255))))
    person(c, 540, 1660, 0.66, (255, 140, 40), (36, 44, 90), mood='happy', look=(0, -0.6), t=t, arm_r=(80, -220), arm_l=(-30, 230), blink=blinking(t))


SCENES = [
    (0.0, s_hook), (ph('the food industry') - 0.15, s_margin), (ph("so where's the") - 0.15, s_ads), (ph('how big') - 0.15, s_big),
    (ph("so who's the") - 0.15, s_customer), (ph('you came in') - 0.15, s_end)]
SHAKES = [(ph('two cents'), 10, 0.35), (ph('six point four'), 18, 0.45), (ph('four point three'), 10, 0.35), (ph("it's the brands"), 8, 0.3)]
TR = 0.32


def draw_scene(c, i, t):
    t0 = SCENES[i][0]; t1 = SCENES[i + 1][0] if i + 1 < len(SCENES) else DUR
    u = cl((t - t0) / max(0.1, t1 - t0))
    z = 1.0 + 0.06 * u; dx = 18 * math.sin(t * 0.5 + i); dy = 10 * math.cos(t * 0.4 + i)
    c.save(); c.translate(540 + dx, 960 + dy); c.scale(z, z); c.translate(-540, -960)
    SCENES[i][1](c, t); c.restore()


def frame(t):
    s = skia.Surface(W, H); c = s.getCanvas()
    sx = sy = 0.0
    for (ts, a, d) in SHAKES:
        if ts <= t < ts + d:
            k = 1 - (t - ts) / d; sx += a * k * math.sin(t * 90); sy += a * k * math.cos(t * 77)
    c.save(); c.translate(sx, sy)
    i = max(j for j, (t0, _) in enumerate(SCENES) if t >= t0)
    draw_scene(c, i, t)
    if i > 0 and t < SCENES[i][0] + TR:      # whip-in: previous scene slides out under a light streak
        k = eio((t - SCENES[i][0]) / TR)
        c.saveLayer(paint=None); c.translate(-W * k, 0); draw_scene(c, i - 1, t); c.restore()
        c.drawRect(skia.Rect.MakeXYWH(W * (1 - k) - 60, 0, 120, H), P((255, 255, 255), 0.5 * (1 - abs(2 * k - 1)), 30))
    if t > END:
        r = 1500 * eio(pr(t, END, 0.8)); c.drawCircle(540, 900, r, P((10, 6, 20)))
    c.restore()
    rnd = random.Random(i * 7 + 1)
    for k in range(9):
        x, y = rnd.uniform(80, 1000), rnd.uniform(260, 1250); ph_ = (t * rnd.uniform(0.5, 0.9) + rnd.random()) % 1.0
        sparkle(c, x, y, rnd.uniform(16, 34), max(0.0, math.sin(ph_ * math.pi)) ** 2)
    vignette(c, 0.12)
    c.drawRect(skia.Rect.MakeXYWH(14, 14, W - 28, H - 28), S((255, 255, 255), 28)); c.drawRect(skia.Rect.MakeXYWH(28, 28, W - 56, H - 56), S(INK, 8))
    return s


# ------------------------------------------------------------------ subtitles (small glass pill, active word in neon)
SUBW = []
_k = 0
for wd in open(os.path.join(D, 'script.txt')).read().split():
    n = len(re.findall(r"[A-Za-z0-9'%]+", wd))
    if n == 0: continue
    seg = AL[_k:_k + n]; _k += n
    if seg: SUBW.append((wd, seg[0][1], seg[-1][2]))
CH = []
cur = []
for w in SUBW:
    cur.append(w)
    if len(cur) >= 3 or w[0][-1] in '.,?!':
        CH.append(cur); cur = []
if cur: CH.append(cur)


def subs(c, t, y):
    for ch in CH:
        if ch[0][1] - 0.05 <= t <= ch[-1][2] + 0.15:
            f = font('Montserrat-ExtraBold.ttf', 40); sp = f.measureText(' ')
            ws = [w for w, a, b in ch]; tw = sum(f.measureText(w) for w in ws) + sp * (len(ws) - 1)
            x = 540 - tw / 2; r = skia.Rect.MakeXYWH(x - 26, y - 46, tw + 52, 66)
            c.drawRoundRect(r, 33, 33, P((10, 6, 24), 0.72)); c.drawRoundRect(r, 33, 33, S((255, 80, 210), 2.5, 0.8))
            for w, a, b in ch:
                on = a - 0.03 <= t <= b + 0.08
                if on: c.drawString(w, x, y, f, P((255, 80, 210), 0.9, 10))
                c.drawString(w, x, y, f, P((255, 120, 230) if on else (255, 255, 255)))
                x += f.measureText(w) + sp
            return


_sat, _con = 1.25, 1.06
_lr, _lg, _lb = 0.2126, 0.7152, 0.0722
SAT = []
for r_, row in enumerate(((1, 0, 0), (0, 1, 0), (0, 0, 1))):
    cs = [(_lr, _lg, _lb)[k] * (1 - _sat) + row[k] * _sat for k in range(3)]
    SAT += [v * _con for v in cs] + [0, (1 - _con) * 0.5]
SAT += [0, 0, 0, 1, 0]


def both(t):
    """returns (ig_rgba, yt_rgba) numpy frames."""
    raw = frame(t).makeImageSnapshot(); gs = skia.Surface(W, H); gp = skia.Paint(ColorFilter=skia.ColorFilters.Matrix(SAT)); gs.getCanvas().drawImage(raw, 0, 0, skia.SamplingOptions(), gp); base = gs.makeImageSnapshot()
    ig = skia.Surface(W, H); c = ig.getCanvas(); c.drawImage(base, 0, 0)
    if 0.3 < t < END + 0.1: subs(c, t, 1442)
    yt = skia.Surface(W, H); c = yt.getCanvas()
    bp = skia.Paint(); bp.setImageFilter(skia.ImageFilters.Blur(40, 40)); c.drawImage(base, 0, 0, skia.SamplingOptions(), bp)
    c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), 0.35))
    c.save(); c.translate(450 - 450 * 0.85, 250 - 250 * 0.85); c.scale(0.85, 0.85)
    sh = P((0, 0, 0), 0.6, 30); c.drawRect(skia.Rect.MakeWH(W, H), sh); c.drawImage(base, 0, 0); c.restore()
    if 0.3 < t < END + 0.1: subs(c, t, 1320)
    return ig.makeImageSnapshot(), yt.makeImageSnapshot()


def to_np(img): return img.toarray(colorType=skia.kRGBA_8888_ColorType)[:, :, :3]


if __name__ == '__main__':
    out = os.path.join(HERE, 'out'); os.makedirs(out, exist_ok=True)
    if sys.argv[1] == 'still':
        for v in sys.argv[2:]:
            ig, yt = both(float(v)); ig.save(os.path.join(out, 'ig_%06.2f.png' % float(v)), skia.kPNG); yt.save(os.path.join(out, 'yt_%06.2f.png' % float(v)), skia.kPNG)
    elif sys.argv[1] == 'nframes':
        print(int(DUR * FPS))
    elif sys.argv[1] == 'range':
        f0, f1 = int(sys.argv[2]), int(sys.argv[3])
        enc = lambda name: subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
                                             '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', os.path.join(out, name)], stdin=subprocess.PIPE)
        pi, py = enc('ig_%05d.mp4' % f0), enc('yt_%05d.mp4' % f0)
        for fi in range(f0, f1):
            ig, yt = both(fi / FPS)
            pi.stdin.write(np.ascontiguousarray(to_np(ig)).tobytes()); py.stdin.write(np.ascontiguousarray(to_np(yt)).tobytes())
            if fi % 60 == 0: print(fi, flush=True)
        pi.stdin.close(); py.stdin.close(); pi.wait(); py.wait()
