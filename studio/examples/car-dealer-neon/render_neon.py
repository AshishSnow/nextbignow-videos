"""Car dealer Short, NEON STORY look (owner approved 18 Nov 13:21). 10 drawn scenes, text lives in the world (neon, screens, notes),
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


# ------------------------------------------------------------------ scenes (each: fn(c, t) draws 1080x1920)
def s_showroom(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, 1100), [(18, 12, 34), (38, 22, 66)]))
    wx, wy, ww, wh = 60, 470, 960, 560
    skyline(c, wx, wy, ww, wh, t)
    for i in range(1, 4): c.drawRect(skia.Rect.MakeXYWH(wx + i * ww / 4 - 7, wy, 14, wh), P((24, 16, 44)))
    c.drawRect(skia.Rect.MakeXYWH(wx, wy + wh * 0.38, ww, 12), P((24, 16, 44)))
    c.drawRect(skia.Rect.MakeXYWH(wx - 11, wy - 11, ww + 22, wh + 22), S(INK, 6))
    fl = 1.0 if (t % 3.1) > 0.12 else 0.35
    c.drawRoundRect(skia.Rect.MakeXYWH(70, 250, 940, 200), 30, 30, P((10, 6, 20), 0.75))
    neon_text(c, 'YOUR DEALER BARELY', 540, 335, 70, (255, 60, 200), fl)
    neon_text(c, 'PROFITS ON THE CAR', 540, 420, 70, (80, 220, 255), 1.0)
    fy = wy + wh + 10
    c.drawRect(skia.Rect.MakeXYWH(0, fy, W, H - fy), LG((0, fy), (0, H), [(60, 30, 90), (24, 14, 40)]))
    for i in range(-8, 9): c.drawLine(540 + i * 40, fy, 540 + i * 260, H, S((255, 150, 255), 2, 0.12))
    for yy in [fy + 40, fy + 110, fy + 210, fy + 350, fy + 540, fy + 800]: c.drawLine(0, yy, W, yy, S((255, 150, 255), 2, 0.10))
    for sx in (360, 720): light_cone(c, sx, 0, 60, 520, fy + 240, (255, 210, 255), 0.13)
    lamp(c, 120, 1200, 0.9)
    inked(c, skia.Rect.MakeXYWH(20, 1200, 360, 40), LG((0, 1200), (0, 1240), [(120, 70, 50), (70, 40, 30)]), 6)
    c.drawRect(skia.Rect.MakeXYWH(40, 1240, 320, 200), P((60, 34, 26))); c.drawRect(skia.Rect.MakeXYWH(40, 1240, 320, 200), S(INK, 6))
    person(c, 250, 1460, 0.56, (70, 140, 255), (235, 235, 245), pants=(50, 50, 70), mood='worried', look=(0.6, 0.8), sweat=3, t=t,
           arm_r=(10, 250), arm_l=(70, 255), tie=(230, 40, 60), shirt=(250, 250, 255), blink=blinking(t, 1))
    coin(c, 330, 1192, 18)
    off = -1500 * eio(pr(t, ph('after you drive') - 0.1, 1.4)) ** 2
    car(c, 560 + off, 1460, 800, t=t)
    person(c, 880 + off, 1800, 0.74, (255, 140, 40), (36, 44, 90), mood='happy', look=(-0.5, -0.4), t=t,
           arm_r=(150, -170 + 12 * math.sin(t * 5)), arm_l=(-30, 230), prop=(1, keys), blink=blinking(t))
    c.drawRect(skia.Rect.MakeWH(W, H), P((255, 40, 180), 0.05))


def s_price(c, t):
    t0 = ph('say you buy'); t5 = ph('five percent')
    c.drawRect(skia.Rect.MakeWH(W, H), RG(540, 800, 1300, [(70, 30, 110), (20, 10, 36)]))
    for sx in (300, 540, 780): light_cone(c, sx, 0, 40, 380, 1500, (255, 220, 255), 0.10)
    c.drawRect(skia.Rect.MakeXYWH(0, 1300, W, 620), LG((0, 1300), (0, H), [(70, 34, 100), (20, 10, 34)]))
    c.drawOval(skia.Rect.MakeXYWH(140, 1340, 800, 160), P((255, 120, 220), 0.25, 40))
    car(c, 540, 1380, 900, t=t)
    # hanging price tag (string from the ceiling)
    sw = 6 * math.sin(t * 1.7)
    c.save(); c.translate(540, 260); c.rotate(sw)
    c.drawLine(0, 0, 0, 240, S((230, 230, 240), 4))
    tg = path([(-260, 300), (-200, 240), (260, 240), (260, 520), (-200, 520), (-260, 460)]); c.drawPath(tg.makeTransform(skia.Matrix.Translate(10, 14)) if hasattr(tg, 'makeTransform') else tg, P((0, 0, 0), 0.4, 10))
    inked(c, tg, LG((0, 240), (0, 520), [(255, 255, 255), (230, 225, 240)]), 7)
    c.drawCircle(-200, 380, 18, P((60, 30, 90))); c.drawCircle(-200, 380, 18, S(INK, 5))
    k30 = pr(t, t0 + 0.3, 0.4)
    ctext(c, '$30,000', 40, 420, 120, (30, 20, 50), 'Anton.ttf', a=k30)
    ctext(c, 'NEW CAR', 40, 488, 40, (120, 100, 150), 'Montserrat-ExtraBold.ttf', a=k30)
    c.restore()
    # wall screen: what the dealer keeps
    if t > t5 - 0.4:
        k = pr(t, t5 - 0.4, 0.4)
        def d(cc):
            ctext(cc, 'DEALER KEEPS', 300, 90, 46, (200, 200, 230), 'Montserrat-ExtraBold.ttf')
            neon_text(cc, '~5%', 300, 250, 150, (255, 70, 90))
            ctext(cc, 'KERRIGAN ADVISORS TO CNBC, AUG 2026', 300, 320, 20, (150, 150, 180), 'Montserrat-ExtraBold.ttf')
        pop(c, k, 540, 950, lambda: screen(c, 240, 780, 600, 350, d, (255, 70, 90)))


def s_office(c, t):
    t15 = ph('fifteen hundred'); tb = ph('pay its bills')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(16, 12, 30), (34, 20, 50)]))
    wr = skia.Rect.MakeXYWH(560, 360, 440, 520); c.save(); c.clipRect(wr); skyline(c, 560, 360, 440, 520, t, 9); c.restore(); c.drawRect(wr, S((30, 20, 50), 18)); c.drawRect(wr, S(INK, 6))
    for i in range(5):
        r = skia.Rect.MakeXYWH(60 + i * 90, 420, 70, 300); inked(c, r, P([(150, 60, 70), (60, 90, 150), (90, 150, 90), (160, 120, 50), (100, 60, 140)][i]), 5)
    inked(c, skia.Rect.MakeXYWH(40, 720, 460, 24), P((70, 40, 30)), 5)
    lamp(c, 210, 1150, 1.2)
    inked(c, skia.Rect.MakeXYWH(30, 1150, 1020, 50), LG((0, 1150), (0, 1200), [(130, 80, 55), (80, 45, 30)]), 7)
    c.drawRect(skia.Rect.MakeXYWH(60, 1200, 960, 700), P((60, 34, 26))); c.drawRect(skia.Rect.MakeXYWH(60, 1200, 960, 700), S(INK, 7))
    person(c, 560, 1560, 0.8, (70, 140, 255), (235, 235, 245), pants=(50, 50, 70), mood='worried', look=(-0.4, 0.9), sweat=3, t=t,
           arm_r=(-40, 260), arm_l=(40, 260), tie=(230, 40, 60), shirt=(250, 250, 255), blink=blinking(t, 2))
    inked(c, skia.Rect.MakeXYWH(30, 1150, 1020, 50), LG((0, 1150), (0, 1200), [(130, 80, 55), (80, 45, 30)]), 7)
    k = pr(t, t15 - 0.4, 0.8)
    for i in range(int(7 * k)): coin(c, 380, 1135 - i * 14, 30)
    if t > t15 - 0.2: sticky(c, 390, 980, 0.8, -6, '$1,500', size=56)
    for i in range(14):
        kb = pr(t, tb - 0.7 + i * 0.09, 0.5)
        if kb <= 0: continue
        x = 720 + (i * 53) % 260; y = -200 + (1140 - (i // 4) * 40 + 200) * eo(kb)
        c.save(); c.translate(x, y); c.rotate((i * 37) % 30 - 15)
        r = skia.Rect.MakeXYWH(-70, -45, 140, 90); inked(c, r, P((255, 252, 240)), 5); ctext(c, 'BILL', 0, 12, 36, (220, 40, 60), 'Anton.ttf'); c.restore()


def s_hall(c, t):
    tf = ph('the finance office'); tl = ph('your loan'); tw = ph('extended warranties'); tp = ph('protection plans')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(20, 12, 40), (40, 20, 60)]))
    c.drawPath(path([(0, 0), (300, 500), (300, 1300), (0, 1920)]), P((30, 18, 54))); c.drawPath(path([(1080, 0), (780, 500), (780, 1300), (1080, 1920)]), P((30, 18, 54)))
    c.drawPath(path([(0, 1920), (300, 1300), (780, 1300), (1080, 1920)]), LG((0, 1300), (0, 1920), [(60, 30, 80), (20, 10, 30)]))
    for i in range(5): c.drawLine(300 + i * 120, 1300, -400 + i * 470, 1920, S((255, 150, 255), 2, 0.1))
    for sx in (200, 880): c.drawCircle(sx, 600, 40, P((255, 60, 200), 0.6, 30))
    k = pr(t, tf - 0.6, 1.2)
    door_glow(c, 380, 720, 320, 580, k)
    neon_text(c, 'FINANCE', 540, 650, 84, (255, 200, 60), 1.0 if (t % 2.2) > 0.1 else 0.4)
    person(c, 230, 1800, 0.72, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.9, -0.3), t=t,
           arm_r=(60, 200), arm_l=(-40, 220), prop=(1, keys), blink=blinking(t))
    paper(c, 780, 1050, -8, 'LOAN', pr(t, tl - 0.3, 0.4), t)
    paper(c, 560, 1450, 6, 'WARRANTY', pr(t, tw - 0.3, 0.4), t)
    paper(c, 840, 1420, -4, 'PROTECTION', pr(t, tp - 0.3, 0.4), t)


def s_fin(c, t):
    t4 = ph('four percent'); t23 = ph('twenty three percent')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(40, 26, 14), (70, 40, 20)]))
    c.drawCircle(540, 900, 900, P((255, 190, 80), 0.25, 120))
    def d(cc):
        ctext(cc, 'ASBURY AUTOMOTIVE', 410, 70, 42, (255, 255, 255))
        ctext(cc, 'FINANCE OFFICE, JAN-JUN 2026', 410, 115, 28, (200, 200, 230), 'Montserrat-ExtraBold.ttf')
        bar(cc, 130, 470, 200, 46, (255, 90, 110), 'OF SALES', '4%', pr(t, t4 - 0.3, 0.6))
        bar(cc, 490, 470, 200, 250, (255, 210, 60), 'OF PROFIT', '23%', pr(t, t23 - 0.3, 0.7))
        cc.drawRect(skia.Rect.MakeXYWH(90, 470, 640, 6), P((220, 220, 240)))
    screen(c, 130, 300, 820, 560, d, (255, 200, 80))
    inked(c, skia.Rect.MakeXYWH(40, 1300, 1000, 50), LG((0, 1300), (0, 1350), [(140, 90, 50), (90, 50, 30)]), 7)
    c.drawRect(skia.Rect.MakeXYWH(70, 1350, 940, 600), P((70, 40, 24))); c.drawRect(skia.Rect.MakeXYWH(70, 1350, 940, 600), S(INK, 7))
    person(c, 760, 1700, 0.68, (60, 200, 120), (40, 40, 60), pants=(30, 30, 46), mood='happy', look=(-0.6, 0.2), t=t,
           arm_r=(-60, 230), arm_l=(-160, 220), tie=(255, 200, 60), shirt=(250, 250, 255), blink=blinking(t, 3))
    inked(c, skia.Rect.MakeXYWH(40, 1300, 1000, 50), LG((0, 1300), (0, 1350), [(140, 90, 50), (90, 50, 30)]), 7)
    sc = skia.Path(); sc.moveTo(160, 1290); sc.cubicTo(200, 1500, 120, 1650, 300, 1900); sc.lineTo(420, 1900); sc.cubicTo(250, 1650, 330, 1500, 290, 1290); sc.close()
    inked(c, sc, P((252, 248, 236)), 5)
    for i in range(10): c.drawLine(200 + i * 4, 1330 + i * 55, 260 + i * 6, 1330 + i * 55, S((170, 170, 190), 5))
    for i in range(6): coin(c, 900 - i * 34, 1288 - (i % 2) * 6, 24)


def s_bay(c, t):
    t5 = ph('five percent on the car'); t50 = ph('fifty percent')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, 1100), [(8, 20, 34), (20, 40, 70)]))
    for i in range(7): c.drawRect(skia.Rect.MakeXYWH(i * 160, 520, 150, 500), P((14, 30, 52))); c.drawRect(skia.Rect.MakeXYWH(i * 160, 520, 150, 500), S((40, 90, 130), 4))
    c.drawRoundRect(skia.Rect.MakeXYWH(60, 250, 960, 220), 30, 30, P((4, 10, 18), 0.8))
    if t < t5 - 0.2:
        neon_text(c, 'THE SERVICE BAY', 540, 395, 84, (40, 230, 255), 1.0 if (t % 2.3) > 0.1 else 0.3)
    else:
        k5 = pr(t, t5 - 0.2, 0.3); k50 = pr(t, t50 - 0.1, 0.25)
        neon_text(c, '5% CAR', 300, 400, 80, (255, 70, 90), k5 * (1 - 0.6 * k50))
        if k50 > 0:
            neon_text(c, '50%', 760, 420, 150, (80, 255, 140), k50 * (1.0 if (t % 1.9) > 0.06 else 0.5))
            neon_text(c, 'SERVICE', 760, 300, 46, (80, 255, 140), k50)
    fy = 1020
    c.drawRect(skia.Rect.MakeXYWH(0, fy, W, H - fy), LG((0, fy), (0, H), [(40, 60, 80), (14, 20, 30)]))
    for i in range(-8, 9): c.drawLine(540 + i * 40, fy, 540 + i * 260, H, S((120, 220, 255), 2, 0.1))
    for sx in (300, 780): light_cone(c, sx, 0, 50, 460, fy + 200, (190, 240, 255), 0.13)
    lift = 60 * eo(pr(t, ph('stop two'), 1.5))
    for px in (330, 760):
        c.drawRect(skia.Rect.MakeXYWH(px - 22, 760, 44, 420), LG((px - 22, 0), (px + 22, 0), [(255, 200, 40), (200, 140, 0)])); c.drawRect(skia.Rect.MakeXYWH(px - 22, 760, 44, 420), S(INK, 6))
    c.drawRect(skia.Rect.MakeXYWH(230, 1060 - lift, 620, 26), P((90, 100, 120))); c.drawRect(skia.Rect.MakeXYWH(230, 1060 - lift, 620, 26), S(INK, 6))
    car(c, 545, 990 - lift, 700, t=t, refl=False)
    for i in range(4):
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(40, 1300 - i * 62, 190, 60), 28, 28); inked(c, r, LG((0, 0), (190, 0), [(30, 30, 36), (70, 70, 80), (30, 30, 36)]), 6)
    for dx in (900, 990):
        d = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(dx - 50, 1180, 100, 150), 12, 12); inked(c, d, LG((dx - 50, 0), (dx + 50, 0), [(20, 90, 160), (60, 160, 230), (20, 90, 160)]), 6)
    rx, ry = 560, 1560
    kr = pr(t, t50 - 0.1, 0.3)
    c.drawCircle(rx, ry - 140, 300, P((255, 200, 60), 0.15 + 0.3 * kr, 70))
    reg = path([(rx - 170, ry), (rx + 170, ry), (rx + 140, ry - 170), (rx - 140, ry - 170)]); inked(c, reg, LG((0, ry - 170), (0, ry), [(255, 210, 90), (200, 120, 20)]), 7)
    scr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(rx - 80, ry - 260, 160, 80), 10, 10); inked(c, scr, P((20, 30, 30)), 6)
    ctext(c, '$$$', rx, ry - 202, 52, (80, 255, 140), 'Anton.ttf')
    drw = skia.Rect.MakeXYWH(rx - 190, ry + 40 * kr - 40, 380, 60); inked(c, drw, P((170, 100, 20)), 7)
    if kr > 0:
        rnd = random.Random(2); tt = t - (t50 - 0.1)
        for k in range(46):
            d0 = rnd.random() * 1.2; ang = rnd.uniform(-1.1, 1.1); v = rnd.uniform(600, 1000)
            ph_ = ((tt - d0) % 1.6) / 1.6 if tt > d0 else -1
            if ph_ < 0: continue
            x = rx + math.sin(ang) * v * ph_; y = ry - 20 - (math.cos(ang) * v * ph_ * 1.6 - 1300 * ph_ * ph_)
            coin(c, x, y, rnd.uniform(16, 26))
    person(c, 920, 1760, 0.58, (70, 140, 255), (110, 120, 140), pants=(80, 90, 110), mood='happy', look=(-0.8, -0.2), t=t, arm_r=(-60, 150), arm_l=(-80, 120), blink=blinking(t, 4))
    person(c, 170, 1800, 0.66, (255, 140, 40), (36, 44, 90), mood='worried' if t > t50 else 'neutral', look=(0.8, -0.3), sweat=2 if t > t50 else 0, t=t,
           arm_r=(40, 220), arm_l=(-40, 220), blink=blinking(t))


def s_board(c, t):
    tb = ph('sixty four billion')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(10, 16, 40), (40, 20, 70)]))
    def d(cc):
        k = pr(t, tb - 0.5, 0.4)
        neon_text(cc, '$164 BILLION', 420, 215, 100, (80, 255, 140), cl(k * 2))
        ctext(cc, "AMERICA'S CAR DEALERS MADE", 420, 80, 34, (210, 210, 240), 'Montserrat-ExtraBold.ttf')
        ctext(cc, 'DEALER SERVICE + PARTS, 2025', 420, 300, 34, (210, 210, 240), 'Montserrat-ExtraBold.ttf')
        ctext(cc, 'NADA DATA 2025', 420, 350, 24, (150, 150, 190), 'Montserrat-ExtraBold.ttf')
    screen(c, 120, 300, 840, 400, d, (80, 255, 140))
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, 770), LG((0, 1150), (0, H), [(50, 40, 80), (16, 12, 28)]))
    for i in range(-8, 9): c.drawLine(540 + i * 40, 1150, 540 + i * 260, H, S((160, 160, 255), 2, 0.1))
    for row, (y, s, n) in enumerate([(1080, 0.24, 6), (1260, 0.32, 5), (1500, 0.42, 4)]):
        for i in range(n):
            x = (i + 0.5) * W / n + 60 * math.sin(t * 0.8 + row) - (t * 60 * (row + 1)) % (W / n)
            small_car(c, x, y + 100 * s, s, [(232, 38, 60), (40, 120, 230), (250, 190, 40), (60, 190, 120), (200, 80, 200)][(i + row) % 5], t)
    c.drawCircle(540, 1000, 500, P((80, 255, 140), 0.08, 90))


def s_street(c, t):
    t42 = ph('forty two percent'); t20 = ph('up from twenty')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, 1200), [(40, 20, 90), (200, 70, 140), (255, 160, 110)], [0, 0.6, 1]))
    c.drawCircle(540, 1080, 170, P((255, 220, 150)))
    rnd = random.Random(6); x = -20
    while x < W:
        bw = rnd.randint(70, 140); bh = rnd.uniform(150, 420); c.drawRect(skia.Rect.MakeXYWH(x, 1180 - bh, bw, bh), P((60, 26, 90))); x += bw + 6
    building(c, 30, 900, 470, 420, (90, 90, 150), 'DEALER', (200, 120, 255), t, True)
    building(c, 640, 1000, 400, 320, (170, 90, 60), 'QUICK OIL', (255, 170, 60), t, False)
    c.drawRect(skia.Rect.MakeXYWH(0, 1320, W, 600), LG((0, 1320), (0, H), [(50, 40, 70), (20, 16, 30)]))
    for i in range(8): c.drawRect(skia.Rect.MakeXYWH(i * 150 - (t * 120) % 150, 1590, 80, 14), P((255, 220, 120), 0.8))
    for i in range(3):
        kk = ((t * 0.28 + i * 0.33) % 1.0)
        x = 120 + 700 * eio(kk); y = 1480 - 90 * kk
        small_car(c, x, y, 0.36 - 0.08 * kk, [(232, 38, 60), (40, 120, 230), (250, 190, 40)][i], t)
    def d(cc):
        ctext(cc, 'DRIVERS WHOSE MAIN SERVICE', 360, 52, 30, (255, 255, 255)); ctext(cc, 'PLACE IS A CHAIN SHOP', 360, 92, 30, (255, 255, 255))
        bar(cc, 90, 390, 190, 71, (180, 160, 255), '2020', '20%', pr(t, t20 - 0.2, 0.5))
        bar(cc, 440, 390, 190, 150, (255, 170, 60), '2025', '42%', pr(t, t42 - 0.2, 0.6))
        ctext(cc, 'DUCKER CARLISLE 2026, VIA CNBC', 360, 465, 20, (170, 170, 200), 'Montserrat-ExtraBold.ttf')
    pop(c, pr(t, t42 - 0.5, 0.4), 540, 520, lambda: screen(c, 180, 290, 720, 480, d, (255, 170, 60)))
    c.drawLine(380, 790, 380, 900, S(INK, 16)); c.drawLine(700, 790, 700, 1000, S(INK, 16))


def s_desk(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(22, 14, 44), (50, 26, 70)]))
    c.drawRoundRect(skia.Rect.MakeXYWH(140, 270, 800, 180), 30, 30, P((10, 6, 20), 0.75))
    neon_text(c, 'THE CAR GETS YOU IN', 540, 340, 58, (255, 60, 200), 1.0)
    neon_text(c, 'SERVICE PAYS THE BILLS', 540, 420, 58, (80, 255, 140), pr(t, ph('the oil changes') - 0.2, 0.3))
    c.drawRect(skia.Rect.MakeXYWH(0, 1010, W, 910), LG((0, 1010), (0, H), [(60, 30, 90), (24, 14, 40)]))
    car(c, 540, 960, 640, t=t, refl=False)
    person(c, 790, 1560, 0.66, (70, 140, 255), (235, 235, 245), mood='happy', look=(-0.7, 0), t=t, arm_r=(-120, 140), arm_l=(-60, 220),
           tie=(40, 200, 255), shirt=(250, 250, 255), blink=blinking(t, 5))
    inked(c, skia.Rect.MakeXYWH(470, 1380, 560, 50), LG((0, 1300), (0, 1350), [(120, 70, 140), (80, 40, 100)]), 6)
    c.drawRect(skia.Rect.MakeXYWH(490, 1430, 520, 560), P((70, 36, 90))); c.drawRect(skia.Rect.MakeXYWH(490, 1430, 520, 560), S(INK, 6))
    person(c, 250, 1800, 0.74, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.7, -0.2), t=t, arm_r=(200, -60), arm_l=(-30, 230), prop=(1, keys), blink=blinking(t))


def s_doors(c, t):
    tw = ph('where do you'); td = ph('dealer or'); ts = ph('down the street')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (W, 0), [(60, 20, 110), (40, 16, 60), (120, 50, 20)]))
    c.drawRoundRect(skia.Rect.MakeXYWH(90, 260, 900, 190), 30, 30, P((10, 6, 20), 0.75))
    neon_text(c, 'WHERE DO YOU GET', 540, 340, 62, (255, 255, 255), pr(t, tw - 0.3, 0.3))
    neon_text(c, 'YOURS SERVICED?', 540, 425, 62, (255, 220, 80), pr(t, tw, 0.3))
    for (x, col, lab, k) in ((70, (170, 110, 255), 'DEALER', pr(t, td - 0.3, 0.3)), (590, (255, 160, 60), 'LOCAL SHOP', pr(t, ts - 0.5, 0.3))):
        g = skia.Rect.MakeXYWH(x, 640, 420, 560)
        c.drawRect(g.makeOutset(30, 30), P(col, 0.25 + 0.35 * k, 60))
        inked(c, g, LG((0, 640), (0, 1200), [tuple(min(255, v + 40) for v in col), tuple(int(v * 0.5) for v in col)]), 8)
        for j in range(8): c.drawLine(x, 640 + j * 70, x + 420, 640 + j * 70, S(INK, 4, 0.5))
        neon_text(c, lab, x + 210, 600, 56, col, max(0.35, k))
    c.drawRect(skia.Rect.MakeXYWH(0, 1200, W, 720), LG((0, 1200), (0, H), [(50, 30, 70), (20, 14, 30)]))
    look = (-0.9, -0.3) if (t % 2.4) < 1.2 else (0.9, -0.3)
    person(c, 540, 1800, 0.8, (255, 140, 40), (36, 44, 90), mood='worried', look=look, sweat=2, t=t, arm_r=(-10, -300), arm_l=(-40, 230), blink=blinking(t))


SCENES = [
    (0.0, s_showroom), (ph('say you buy') - 0.15, s_price), (ph("that's around") - 0.15, s_office), (ph("so where's the money") - 0.15, s_hall),
    (ph('at asbury') - 0.15, s_fin), (ph('stop two') - 0.15, s_bay), (ph('last year') - 0.15, s_board), (ph('but drivers') - 0.15, s_street),
    (ph('so the car gets') - 0.15, s_desk), (ph('where do you') - 0.15, s_doors)]
SHAKES = [(ph('five percent'), 8, 0.3), (ph('twenty three percent'), 10, 0.3), (ph('fifty percent'), 18, 0.45), (ph('sixty four billion'), 10, 0.35), (ph('forty two percent'), 8, 0.3)]
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
    vignette(c); grain(c, int(t * FPS) % 11, 0.05)
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


def both(t):
    """returns (ig_rgba, yt_rgba) numpy frames."""
    base = frame(t).makeImageSnapshot()
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
