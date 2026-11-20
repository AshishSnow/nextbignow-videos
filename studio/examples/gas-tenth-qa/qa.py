"""OMB 'Q&A burst' look, modelled on FreshNestHub's current bright Shorts (owner 19 Nov: 'create video on FreshNestHub style'):
full-bleed sunburst background (colour changes every beat) + halftone dots + sparkles, a big two-line outlined headline at the top
(white line + yellow line), ONE polaroid photo-card (here: a drawn comic picture inside the card), flat icons, starburst badges,
small label tags with a red dot, logo top-left, small white subtitle pill. Beats: QUESTION -> WHY? -> BUT... -> STRAIGHT ANSWER."""
import os, math, random
import numpy as np
import skia
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from neon import font, C, P, S, LG, RG, path, inked, INK, sparkle, cloud, person, coin, car

W, H = 1080, 1920
LOGO = '/home/claude/nextbignow-videos/studio/brand/logo/final_black_yellow/omb_icon_512.png'
_logo = None

BG = {'red': ((245, 95, 95), (225, 70, 75)), 'purple': ((110, 90, 180), (85, 65, 150)), 'lilac': ((180, 140, 230), (150, 110, 210)),
      'orange': ((255, 170, 70), (245, 140, 40)), 'green': ((110, 205, 130), (80, 180, 105)), 'blue': ((120, 200, 240), (85, 170, 225)),
      'teal': ((70, 200, 190), (40, 170, 165))}


def sunburst(c, name, t, cx=540, cy=900):
    a, b = BG[name]
    c.drawRect(skia.Rect.MakeWH(W, H), P(a))
    rot = t * 4
    for i in range(24):
        ang = math.radians(i * 15 + rot)
        p = path([(cx, cy), (cx + 2600 * math.cos(ang - 0.11), cy + 2600 * math.sin(ang - 0.11)), (cx + 2600 * math.cos(ang + 0.11), cy + 2600 * math.sin(ang + 0.11))])
        if i % 2 == 0: c.drawPath(p, P(b))
    c.drawCircle(cx, cy, 700, P((255, 255, 255), 0.18, 160))
    for y in range(0, H, 22):
        for x in range((y // 22) % 2 * 11, W, 22):
            d = math.hypot(x - cx, y - cy) / 1400
            c.drawCircle(x, y, 2.2 + 1.5 * d, P((0, 0, 0), 0.07))
    rnd = random.Random(hash(name) % 99)
    for k in range(10):
        x, y = rnd.uniform(60, 1020), rnd.uniform(300, 1300); ph = (t * rnd.uniform(0.4, 0.8) + rnd.random()) % 1
        sparkle(c, x, y, rnd.uniform(10, 18), max(0.0, math.sin(ph * math.pi)) ** 2)


def logo(c):
    global _logo
    if _logo is None:
        from PIL import Image
        im = Image.open(LOGO).convert('RGBA').resize((84, 84)); _logo = skia.Image.fromarray(np.ascontiguousarray(np.array(im)), colorType=skia.kRGBA_8888_ColorType)
    c.drawImage(_logo, 70, 258, skia.SamplingOptions(skia.FilterMode.kLinear))
    f = font('Montserrat-Black.ttf', 26); c.drawString('OOPSMYBUSINESS', 166, 310, f, S(INK, 6)); c.drawString('OOPSMYBUSINESS', 166, 310, f, P((255, 255, 255)))


def headline(c, l1, l2=None, k=1.0, y=420, s1=88, s2=104):
    if k <= 0: return
    sc = 0.6 + 0.4 * min(1, k * 1.4) + 0.06 * math.sin(min(1, k) * math.pi)
    c.save(); c.translate(540, y); c.scale(sc, sc)
    for txt, size, col, dy in ((l1, s1, (255, 255, 255), 0), (l2, s2, (255, 214, 40), s1 * 1.2)):
        if not txt: continue
        f = font('Montserrat-Black.ttf', size); tw = f.measureText(txt)
        while tw > 930: size *= 0.94; f = font('Montserrat-Black.ttf', size); tw = f.measureText(txt)
        c.drawString(txt, -tw / 2 + 8, dy + 10, f, P(INK, 0.9)); c.drawString(txt, -tw / 2, dy, f, S(INK, size * 0.2)); c.drawString(txt, -tw / 2, dy, f, P(col))
    c.restore()


def polaroid(c, cx, cy, w, h, rot, k, draw):
    if k <= 0: return
    s = 0.7 + 0.3 * min(1, k * 1.3) + 0.08 * math.sin(min(1, k) * math.pi)
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    r = skia.Rect.MakeXYWH(-w / 2 - 22, -h / 2 - 22, w + 44, h + 44)
    c.drawRect(r.makeOffset(14, 18), P(INK, 0.35, 10)); inked(c, r, P((255, 255, 255)), 6)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h)); c.translate(-w / 2, -h / 2); draw(c, w, h); c.restore()
    c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), S(INK, 4))
    c.restore()


def burst(c, x, y, r, txt, k, col=(255, 214, 40), tc=INK, rot=-8, size=None):
    if k <= 0: return
    s = min(1.15, k * 1.6) if k < 0.7 else 1.0 + 0.05 * math.sin(k * 20)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); n = 14
    for i in range(n * 2):
        a = math.pi * i / n; rr = r if i % 2 == 0 else r * 0.74
        (p.moveTo if i == 0 else p.lineTo)(rr * math.cos(a), rr * math.sin(a))
    p.close(); c.drawPath(p.makeOffset(8, 10) if hasattr(p, 'makeOffset') else p, P(INK, 0.4)); inked(c, p, P(col), 7)
    size = size or (r * 0.42 if '\n' not in txt else r * 0.3); f = font('Montserrat-Black.ttf', size)
    lines = txt.split('\n')
    for i, ln in enumerate(lines):
        tw = f.measureText(ln); yy = (i - (len(lines) - 1) / 2) * size * 1.05 + size * 0.36
        c.drawString(ln, -tw / 2, yy, f, P(tc))
    c.restore()


def label(c, txt, x, y, k, rot=-2, size=34, bg=(255, 255, 255), dot=True):
    if k <= 0: return
    f = font('Montserrat-ExtraBold.ttf', size); tw = f.measureText(txt); w = tw + (64 if dot else 36); h = size * 1.6
    c.save(); c.translate(x, y); c.rotate(rot); s = min(1, k * 1.5); c.scale(s, s)
    r = skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h); c.drawRect(r.makeOffset(6, 8), P(INK, 0.5)); inked(c, r, P(bg), 4)
    if dot: c.drawCircle(-w / 2 + 24, 0, 8, P((235, 50, 60)))
    c.drawString(txt, -w / 2 + (44 if dot else 18), size * 0.36, f, P(INK)); c.restore()


def subpill(c, words, t, y=1442):
    """words = [(word, a, b)] of the current chunk; active word highlighted yellow like FNH."""
    f = font('Montserrat-ExtraBold.ttf', 36); sp = f.measureText(' ')
    tw = sum(f.measureText(w) for w, a, b in words) + sp * (len(words) - 1) + 40
    x = 540 - tw / 2
    r = skia.Rect.MakeXYWH(x, y - 40, tw, 58); c.drawRect(r.makeOffset(6, 7), P(INK, 0.6)); inked(c, r, P((255, 255, 255)), 4)
    c.drawCircle(x + 20, y - 11, 7, P((235, 50, 60)))
    xx = x + 36
    for w, a, b in words:
        on = a - 0.03 <= t <= b + 0.08; ww = f.measureText(w)
        if on: c.drawRect(skia.Rect.MakeXYWH(xx - 4, y - 34, ww + 8, 46), P((255, 214, 40)))
        c.drawString(w, xx, y, f, P(INK)); xx += ww + sp


# ---------------------------------------------------------------- drawn pictures for the cards
def pic_station(c, w, h, t, price_frac=True):
    c.drawRect(skia.Rect.MakeWH(w, h), LG((0, 0), (0, h), [(40, 150, 240), (150, 215, 255)]))
    cloud(c, 60, 120, 0.4)
    c.drawRect(skia.Rect.MakeXYWH(0, h * 0.78, w, h * 0.22), P((90, 95, 110)))
    pole = skia.Rect.MakeXYWH(w * 0.5 - 14, h * 0.4, 28, h * 0.4); inked(c, pole, P((80, 80, 95)), 4)
    sg = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(w * 0.1, h * 0.08, w * 0.8, h * 0.36), 16, 16); inked(c, sg, P((30, 32, 44)), 6)
    c.drawRect(skia.Rect.MakeXYWH(w * 0.1, h * 0.08, w * 0.8, h * 0.08), P((235, 60, 60)))
    f = font('Montserrat-Black.ttf', h * 0.05); s = 'REGULAR'; c.drawString(s, w / 2 - f.measureText(s) / 2, h * 0.14, f, P((255, 255, 255)))
    f2 = font('Anton.ttf', h * 0.19); s2 = '$2.99'
    tw = f2.measureText(s2); x0 = w / 2 - tw / 2 - (w * 0.06 if price_frac else 0)
    c.drawString(s2, x0, h * 0.37, f2, P((255, 214, 40), 1.0))
    if price_frac:
        f3 = font('Anton.ttf', h * 0.075); fl = 1.0 if (t % 1.4) > 0.15 else 0.4
        c.drawString('9', x0 + tw + 10, h * 0.25, f3, P((255, 214, 40), fl)); c.drawLine(x0 + tw + 8, h * 0.27, x0 + tw + 50, h * 0.27, S((255, 214, 40), 4, fl))
        c.drawString('10', x0 + tw + 4, h * 0.34, f3, P((255, 214, 40), fl))
    pump = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(w * 0.08, h * 0.52, w * 0.2, h * 0.3), 10, 10); inked(c, pump, P((235, 60, 60)), 5)
    c.drawRect(skia.Rect.MakeXYWH(w * 0.11, h * 0.56, w * 0.14, h * 0.07), P((200, 240, 255))); c.drawRect(skia.Rect.MakeXYWH(w * 0.11, h * 0.56, w * 0.14, h * 0.07), S(INK, 3))
    car(c, w * 0.68, h * 0.74, w * 0.5, t=t, refl=False)


def pic_old(c, w, h, t):
    c.drawRect(skia.Rect.MakeWH(w, h), LG((0, 0), (0, h), [(235, 215, 170), (210, 180, 130)]))
    for i in range(0, w, 8): c.drawLine(i, 0, i, h, S((150, 120, 80), 1, 0.15))
    pump = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(w * 0.32, h * 0.2, w * 0.36, h * 0.66), 40, 40); inked(c, pump, P((200, 70, 60)), 6)
    c.drawCircle(w * 0.5, h * 0.18, w * 0.16, P((250, 245, 230))); c.drawCircle(w * 0.5, h * 0.18, w * 0.16, S(INK, 6))
    f = font('Anton.ttf', w * 0.09); s = '1930s'; c.drawString(s, w * 0.5 - f.measureText(s) / 2, h * 0.21, f, P((200, 70, 60)))
    c.drawRect(skia.Rect.MakeXYWH(w * 0.38, h * 0.36, w * 0.24, h * 0.14), P((250, 245, 230))); c.drawRect(skia.Rect.MakeXYWH(w * 0.38, h * 0.36, w * 0.24, h * 0.14), S(INK, 4))
    f2 = font('Anton.ttf', w * 0.08); s2 = 'TAX'; c.drawString(s2, w * 0.5 - f2.measureText(s2) / 2, h * 0.46, f2, P(INK))
    hose = skia.Path(); hose.moveTo(w * 0.68, h * 0.5); hose.cubicTo(w * 0.9, h * 0.55, w * 0.88, h * 0.8, w * 0.75, h * 0.86); c.drawPath(hose, S(INK, 12))
    c.drawRect(skia.Rect.MakeWH(w, h), P((120, 80, 30), 0.15))


def pic_profit(c, w, h, t, k):
    c.drawRect(skia.Rect.MakeWH(w, h), LG((0, 0), (0, h), [(255, 250, 235), (240, 225, 200)]))
    # one gallon jug -> 10-15 cents
    jug = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(w * 0.08, h * 0.2, w * 0.36, h * 0.6), 30, 30); inked(c, jug, LG((0, h * 0.2), (0, h * 0.8), [(255, 220, 90), (240, 170, 30)]), 6)
    f = font('Montserrat-Black.ttf', w * 0.06); s = '1 GALLON'; c.drawString(s, w * 0.26 - f.measureText(s) / 2, h * 0.52, f, P(INK))
    for j in range(int(4 * min(1, k * 2))): coin(c, w * 0.72, h * 0.72 - j * 22, w * 0.1)
    f2 = font('Anton.ttf', w * 0.11); s2 = '10-15¢'; c.drawString(s2, w * 0.72 - f2.measureText(s2) / 2, h * 0.36, f2, P((40, 160, 90)))
    f3 = font('Montserrat-ExtraBold.ttf', w * 0.045); s3 = 'STATION MARGIN'; c.drawString(s3, w * 0.72 - f3.measureText(s3) / 2, h * 0.43, f3, P(INK))
