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


# ------------------------------------------------------------------ scenes
def s_mountain(c, t):
    th = ph('and a lot')
    sky_bg(c, t)
    board(c, 70, 250, 940, 200)
    neon_text(c, '$850 BILLION', 540, 340, 72, (255, 70, 90))
    neon_text(c, 'OF RETURNS THIS YEAR', 540, 425, 62, (30, 160, 255))
    rows = [(9, 1340), (8, 1250), (7, 1160), (6, 1070), (5, 980), (4, 890), (3, 800)]
    k = pr(t, 0.1, 2.2)
    n = 0
    for ri, (cnt, y) in enumerate(rows):
        for j in range(cnt):
            n += 1; kk = pr(k, n * 0.02, 0.15)
            if kk <= 0: continue
            x = 540 + (j - (cnt - 1) / 2) * 110
            box(c, x, y - 300 * (1 - eo(kk)), 104, 86, rot=((n * 37) % 10 - 5))
    kh = pr(t, 0.6, 1.8)
    person(c, lerp(160, 470, eio(kh)), lerp(1700, 1460, eio(kh)), 0.5, (255, 140, 40), (36, 44, 90), mood='shock', look=(0.6, -0.6), sweat=2, t=t,
           arm_r=(40, -200), arm_l=(-40, -200), blink=blinking(t))
    box(c, lerp(160, 470, eio(kh)), lerp(1700, 1460, eio(kh)) - 500, 120, 96)
    if t > th - 0.3:
        kk = pr(t, th - 0.3, 0.4)
        def shelf():
            board(c, 640, 1430, 380, 260, (255, 255, 255))
            for i in range(3): c.drawRect(skia.Rect.MakeXYWH(660, 1500 + i * 70, 340, 12), P((150, 150, 170)))
            neon_text(c, '?', 830, 1640, 130, (255, 70, 90))
        pop(c, kk, 830, 1560, shelf)


def s_stats(c, t):
    t16 = ph('sixteen percent'); t19 = ph('nineteen percent')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(230, 245, 255), (200, 228, 252)]))
    c.drawRect(skia.Rect.MakeXYWH(0, 1300, W, 620), LG((0, 1300), (0, H), [(255, 220, 170), (230, 180, 120)]))
    def d(cc):
        ctext(cc, 'NATIONAL RETAIL FEDERATION', 410, 70, 38, (255, 255, 255)); ctext(cc, '2025 RETURNS REPORT', 410, 112, 26, (200, 200, 230), 'Montserrat-ExtraBold.ttf')
        k = pr(t, t16 - 0.3, 0.4)
        if k > 0: neon_text(cc, '16%', 410, 300, 170, (255, 200, 40), cl(k * 2))
        ctext(cc, 'OF EVERYTHING BOUGHT COMES BACK', 410, 370, 30, (255, 255, 255), a=k)
    screen(c, 130, 300, 820, 420, d, (40, 170, 255))
    for i in range(6):
        kk = pr(t, t16 - 0.2 + i * 0.08, 0.3)
        if kk <= 0: continue
        x = 170 + i * 150; y = 1100
        back = (i == 4)
        u = pr(t, t16 + 0.7, 0.9) if back else 0
        bx, by = x + 200 * eio(u) * -1, y - 260 * math.sin(math.pi * min(1, u)) + 0
        pop(c, kk, bx, by, lambda: box(c, bx, by, 120, 100, rot=-30 * u, label='BACK' if back and u > 0.3 else None))
    person(c, 540, 1800, 0.62, (255, 140, 40), (36, 44, 90), mood='shock' if t > t16 + 0.8 else 'happy', look=(-0.4, -0.7), t=t, arm_r=(40, 220), arm_l=(-40, 220), blink=blinking(t))
    if t > t19 - 0.4:
        k = pr(t, t19 - 0.4, 0.4)
        def ph_():
            r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-170, -300, 340, 600), 40, 40)
            c.save(); c.translate(820, 1150); c.rotate(8); inked(c, r, P((30, 30, 40)), 8)
            c.drawRoundRect(skia.Rect.MakeXYWH(-150, -270, 300, 540), 26, 26, LG((0, -270), (0, 270), [(255, 255, 255), (220, 235, 255)]))
            ctext(c, 'ONLINE', 0, -150, 50, (30, 160, 255)); neon_text(c, '19%', 0, 40, 130, (255, 70, 90)); ctext(c, 'RETURNED', 0, 140, 40, (60, 60, 80))
            c.restore()
        pop(c, k, 820, 1150, ph_)


def s_drop(c, t):
    t0 = ph('you print'); te = ph("that's where")
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(255, 245, 230), (255, 225, 200)]))
    board(c, 220, 260, 640, 150); neon_text(c, 'RETURNS', 540, 365, 96, (255, 70, 90))
    person(c, 560, 1330, 0.6, (70, 140, 255), (255, 255, 255), mood='happy', look=(-0.6, 0.2), t=t, arm_r=(-60, 200), arm_l=(-60, 220), tie=(40, 170, 255), shirt=(250, 250, 255), blink=blinking(t, 2))
    door = skia.Rect.MakeXYWH(700, 560, 300, 620); inked(c, door, LG((0, 560), (0, 1180), [(120, 130, 150), (80, 90, 110)]), 7)
    c.drawRect(skia.Rect.MakeXYWH(720, 580, 260, 160), P((180, 220, 255))); c.drawRect(skia.Rect.MakeXYWH(720, 580, 260, 160), S(INK, 5))
    inked(c, skia.Rect.MakeXYWH(20, 1180, 1040, 50), LG((0, 1180), (0, 1230), [(255, 255, 255), (220, 225, 235)]), 7)
    c.drawRect(skia.Rect.MakeXYWH(40, 1230, 1000, 700), LG((0, 1230), (0, H), [(40, 170, 255), (30, 120, 210)])); c.drawRect(skia.Rect.MakeXYWH(40, 1230, 1000, 700), S(INK, 7))
    kd = pr(t, t0 + 0.3, 0.6); ks = pr(t, te - 0.3, 1.4)
    bx = lerp(300, 460, eio(kd)) + 400 * eio(ks); by = 1110 - 30 * math.sin(math.pi * kd)
    box(c, bx, by, 170, 140, rot=-8 + 16 * kd, label='RETURN')
    if t > te: sticky(c, 520, 900, 0.9, -6, '$$$', size=70, col=(255, 236, 90), tc=(220, 30, 40))
    kw = pr(t, te + 1.0, 1.4)
    person(c, lerp(260, -200, eio(kw)), 1800, 0.74, (255, 140, 40), (36, 44, 90), mood='happy', look=(-0.6, -0.2), t=t, arm_r=(80, 150) if kd < 1 else (40, 220), arm_l=(-30, 230), blink=blinking(t))


def s_warehouse(c, t):
    ts = ph('ship it back'); to = ph('open it'); tc = ph('check it'); tr = ph('repack it'); t66 = ph('sixty six percent')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(225, 240, 255), (190, 220, 245)]))
    for i in range(6): c.drawRect(skia.Rect.MakeXYWH(i * 190, 260, 100, 700), P((255, 255, 255), 0.35))
    for k_, (lab, tt, x, col) in enumerate((('SHIP', ts, 200, (255, 70, 90)), ('OPEN', to, 420, (30, 160, 255)), ('CHECK', tc, 650, (40, 190, 110)), ('REPACK', tr, 880, (255, 160, 30)))):
        kk = pr(t, tt - 0.2, 0.3)
        pop(c, kk, x, 620, lambda: (board(c, x - 105, 560, 210, 100), neon_text(c, lab, x, 635, 48, col)))
    belt = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(30, 1060, 1020, 70), 35, 35); inked(c, belt, P((70, 75, 90)), 7)
    for i in range(14): c.drawCircle(70 + i * 72, 1095, 22, P((150, 155, 170))); c.drawCircle(70 + i * 72, 1095, 22, S(INK, 4))
    for i in range(6):
        x = (i * 210 + t * 160) % 1260 - 110
        box(c, x, 990, 150, 120, open_=1.0 if 320 < x < 760 else 0.0)
    for i, x in enumerate((200, 650)):
        person(c, x, 1600 if i == 0 else 1600, 0.5, (70, 140, 255) if i == 0 else (60, 200, 120), (255, 160, 30), mood='worried', sweat=1, t=t, arm_r=(20, -160), arm_l=(-20, -160), blink=blinking(t, i))
    if t > t66 - 0.5:
        k = pr(t, t66 - 0.5, 0.4); kb = pr(t, t66 - 0.1, 0.3)
        c.drawRect(skia.Rect.MakeWH(W, H), P((255, 255, 255), 0.5 * k))
        def tagd():
            c.save(); c.translate(520, 1100); c.rotate(-6); c.scale(0.85, 0.85)
            tg = path([(-330, -60), (-260, -200), (330, -200), (330, 200), (-260, 200), (-330, 60)]); inked(c, tg, LG((0, -200), (0, 200), [(255, 255, 255), (230, 230, 240)]), 8)
            c.drawCircle(-250, 0, 24, P((200, 200, 210))); c.drawCircle(-250, 0, 24, S(INK, 5))
            ctext(c, "ITEM'S PRICE", 20, -90, 52, (60, 60, 80))
            if kb > 0:
                c.drawLine(-200, -150, lerp(-200, 300, eo(kb)), lerp(-150, 170, eo(kb)), S((255, 70, 90), 14, 0.85))
            neon_text(c, 'UP TO 66%', 20, 90, 110, (255, 70, 90), cl(kb * 2))
            c.restore()
        pop(c, k, 540, 1100, tagd)
        if kb > 0.5: ctext(c, 'TO PROCESS A RETURN (OPTORO, VIA CNBC)', 540, 1360, 26, (40, 40, 60), 'Montserrat-ExtraBold.ttf')


def s_pallet(c, t):
    t0 = ph('so lots of'); tl = ph('liquidators'); tb = ph('bargain stores')
    sky_bg(c, t, (180, 190, 205))
    kp = pr(t, t0 - 0.1, 1.2)
    if t < tb - 0.4:
        pallet(c, 540, 1320, 700)
        n = 0
        for row in range(4):
            for j in range(4 - (row // 2)):
                n += 1; kk = pr(kp, n * 0.06, 0.25)
                if kk <= 0: continue
                x = 540 + (j - (3 - row // 2) / 2) * 165; y = 1240 - row * 120
                box(c, x, y - 400 * (1 - eo(kk)), 160, 118)
        if kp >= 1: c.drawRoundRect(skia.Rect.MakeXYWH(190, 800, 700, 520), 30, 30, P((220, 240, 255), 0.35)); c.drawRoundRect(skia.Rect.MakeXYWH(190, 800, 700, 520), 30, 30, S((255, 255, 255), 5, 0.9))
        if t > tl - 0.2:
            kg = pr(t, tl - 0.2, 0.3)
            c.save(); c.translate(860, 600); c.rotate(-40 + 40 * eo(kg))
            inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-40, -110, 220, 90), 20, 20), LG((0, -110), (0, -20), [(200, 130, 70), (150, 90, 40)]), 6)
            c.drawLine(70, -30, 70, 200, S(INK, 22)); c.drawLine(70, -30, 70, 200, S((180, 110, 60), 12)); c.restore()
            pop(c, pr(t, tl + 0.1, 0.3), 330, 620, lambda: (board(c, 160, 550, 340, 130, (255, 236, 90)), neon_text(c, 'SOLD!', 330, 645, 80, (255, 70, 90))))
    else:
        building(c, 150, 760, 780, 600, (255, 150, 120), 'BARGAIN STORE', (255, 200, 40), t, False)
        for i in range(6):
            x = 120 + i * 160; kk = pr(t, tb - 0.4 + i * 0.07, 0.3)
            if kk <= 0: continue
            pop(c, kk, x, 1700, lambda: person(c, x, 1700, 0.3, [(255, 140, 40), (70, 140, 255), (60, 200, 120), (255, 90, 120), (170, 110, 255)][i % 5], [(36, 44, 90), (200, 60, 70), (40, 120, 90), (90, 60, 140), (230, 160, 40)][i % 5], mood='happy', t=t, blink=blinking(t, i)))


def s_reveal(c, t):
    tw = ph('the wild part'); t90 = ph('ninety percent')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(255, 240, 220), (245, 215, 180)]))
    pallet(c, 540, 1380, 760)
    for j in range(4): box(c, 260 + j * 185, 1300, 170, 130) if j != 1 else None
    ko = pr(t, t90 - 0.5, 0.5)
    box(c, 445, 1300, 170, 130, open_=ko)
    dim = pr(t, tw - 0.1, 0.4) * (1 - pr(t, t90 - 0.2, 0.25))
    if dim > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((20, 30, 60), 0.4 * dim))
    if t > t90 - 0.2:
        k = pr(t, t90 - 0.2, 0.5)
        c.drawCircle(540, 1000, 420, P((255, 255, 220), 0.6 * k, 90))
        pop(c, k, 540, 1000, lambda: tv(c, 540, 1050 - 120 * eo(k), 520, t))
        for i in range(6): sparkle(c, 540 + 300 * math.cos(i + t), 1000 + 220 * math.sin(i * 2 + t), 30, k * abs(math.sin(t * 3 + i)))
        def q():
            board(c, 80, 270, 920, 300)
            neon_text(c, '"90% OF THE TIME,', 540, 370, 62, (30, 160, 255))
            neon_text(c, "THERE'S NOTHING", 540, 445, 62, (255, 70, 90)); neon_text(c, 'WRONG WITH IT."', 540, 520, 62, (255, 70, 90))
            ctext(c, 'TONY SCIARROTTA, REVERSE LOGISTICS ASSN., TO CNBC', 540, 600, 22, (40, 40, 60), 'Montserrat-ExtraBold.ttf')
        pop(c, pr(t, t90 + 0.1, 0.4), 540, 420, q)


def s_landfill(c, t):
    t58 = ph('five point eight')
    sky_bg(c, t, (150, 200, 120))
    hill = skia.Path(); hill.moveTo(0, 1400); hill.cubicTo(200, 1000, 800, 980, 1080, 1380); hill.lineTo(1080, 1920); hill.lineTo(0, 1920); hill.close()
    c.drawPath(hill, LG((0, 1000), (0, 1500), [(170, 150, 120), (130, 110, 90)])); c.drawPath(hill, S(INK, 7))
    rnd = random.Random(3)
    for i in range(26): box(c, rnd.uniform(120, 960), rnd.uniform(1120, 1400), rnd.uniform(60, 110), rot=rnd.uniform(-40, 40))
    tx = lerp(1300, 760, eo(pr(t, ph("what doesn't") - 0.1, 1.0)))
    c.save(); c.translate(tx, 1180)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(0, -60, 200, 160), 20, 20), P((255, 190, 30)), 7)
    c.drawRect(skia.Rect.MakeXYWH(30, -40, 120, 60), P((180, 220, 255))); c.drawRect(skia.Rect.MakeXYWH(30, -40, 120, 60), S(INK, 5))
    tilt = 25 * pr(t, t58 - 0.6, 0.6)
    c.save(); c.translate(-20, 60); c.rotate(-tilt)
    bed = path([(-320, -140), (0, -140), (0, 40), (-300, 40)]); inked(c, bed, P((40, 170, 255)), 7)
    for j in range(3): box(c, -250 + j * 90, -170, 80)
    c.restore()
    for x in (-220, 60): c.drawCircle(x + 40, 110, 46, P(INK)); c.drawCircle(x + 40, 110, 20, P((200, 200, 210)))
    c.restore()
    if t > t58 - 0.4:
        def sg():
            board(c, 90, 280, 900, 260)
            neon_text(c, 'UP TO 5.8 BILLION LBS', 540, 380, 64, (255, 70, 90)); neon_text(c, 'TO LANDFILL A YEAR', 540, 460, 58, (40, 160, 90))
            ctext(c, 'OPTORO ESTIMATE, VIA CNBC', 540, 520, 24, (40, 40, 60), 'Montserrat-ExtraBold.ttf')
        pop(c, pr(t, t58 - 0.4, 0.4), 540, 410, sg)


def s_end(c, t):
    t0 = ph('so that box'); tm = ph('would you buy')
    sky_bg(c, t)
    pallet(c, 540, 1320, 700)
    for row in range(3):
        for j in range(4 - row):
            box(c, 540 + (j - (3 - row) / 2) * 165, 1240 - row * 120, 160, 118, label='RETURN' if (row == 2 and j == 0) else None)
    if t < tm - 0.3:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'YOUR RETURN IS', 540, 355, 70, (30, 160, 255)); neon_text(c, 'ON A PALLET NOW', 540, 440, 70, (255, 190, 30), pr(t, t0 + 0.6, 0.3))
        pop(c, pr(t, t0 + 1.2, 0.3), 840, 820, lambda: sticky(c, 840, 820, 1.0, 8, 'SOLD', size=60))
    else:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'WOULD YOU BUY A', 540, 355, 70, (30, 160, 255)); neon_text(c, 'MYSTERY PALLET?', 540, 440, 70, (255, 190, 30))
        for x, lab, col in ((300, 'YES', (40, 190, 110)), (780, 'NO', (255, 70, 90))):
            pop(c, pr(t, tm + 0.3, 0.3), x, 620, lambda: (board(c, x - 130, 560, 260, 120, col), neon_text(c, lab, x, 650, 80, (255, 255, 255))))
    person(c, 180, 1800, 0.66, (255, 140, 40), (36, 44, 90), mood='shock' if t < tm else 'happy', look=(0.8, -0.4), t=t, arm_r=(120, -60), arm_l=(-30, 230), blink=blinking(t))


SCENES = [
    (0.0, s_mountain), (ph('the national retail') - 0.15, s_stats), (ph('you print') - 0.15, s_drop), (ph('someone has to') - 0.15, s_warehouse),
    (ph('so lots of') - 0.15, s_pallet), (ph("and here's the") - 0.15, s_reveal), (ph("and what doesn't") - 0.15, s_landfill), (ph('so that box') - 0.15, s_end)]
SHAKES = [(ph('sixteen percent'), 8, 0.3), (ph('nineteen percent'), 8, 0.3), (ph('sixty six percent'), 12, 0.35), (ph('ninety percent'), 16, 0.45), (ph('five point eight'), 10, 0.35)]
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
