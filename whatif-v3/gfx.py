"""Drawing toolkit for the Q-Day video (Skia)."""
import skia, math, os
import numpy as np

FONTDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fonts')
NAVY = (10, 16, 34)
CYAN = (46, 230, 255)
RED = (255, 59, 92)
AMBER = (255, 181, 71)
WHITE = (255, 255, 255)
MUTED = (138, 155, 196)
DIM = (70, 84, 120)
ICE = (190, 245, 255)
GOLD = (255, 200, 90)

_TF = {
    'sgb': 'SpaceGrotesk-Bold.ttf', 'sgm': 'SpaceGrotesk-Medium.ttf',
    'jbb': 'JetBrainsMono-Bold.ttf', 'jbm': 'JetBrainsMono-Medium.ttf',
    'ins': 'Inter-SemiBold.ttf', 'inr': 'Inter-Regular.ttf',
}
_tfc, _fc = {}, {}

def font(key, size):
    k = (key, round(size, 1))
    if k not in _fc:
        if key not in _tfc:
            _tfc[key] = skia.Typeface.MakeFromFile(os.path.join(FONTDIR, _TF[key]))
        f = skia.Font(_tfc[key], size)
        f.setEdging(skia.Font.Edging.kAntiAlias)
        f.setSubpixel(True)
        _fc[k] = f
    return _fc[k]

# ------------------------------------------------------------------ math
def cl(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x

def pr(t, t0, d):
    if d <= 0:
        return 1.0 if t >= t0 else 0.0
    return cl((t - t0) / d)

def eo(x):
    return 1 - (1 - x) ** 3

def eo5(x):
    return 1 - (1 - x) ** 5

def ei(x):
    return x ** 3

def eio(x):
    return x * x * (3 - 2 * x)

def eback(x, s=1.7):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    x = x - 1
    return x * x * ((s + 1) * x + s) + 1

def lerp(a, b, x):
    return a + (b - a) * x

def mix(c1, c2, x):
    return tuple(int(lerp(a, b, x)) for a, b in zip(c1, c2))

def fade(t, t0, t1, fi=0.3, fo=0.3):
    return min(pr(t, t0, fi), 1 - pr(t, t1 - fo, fo))

def hsh(i, k=0):
    """deterministic pseudo random in [0,1)"""
    x = math.sin(i * 12.9898 + k * 78.233) * 43758.5453
    return x - math.floor(x)

# ------------------------------------------------------------------ paint
def C(rgb, a=1.0):
    return skia.Color4f(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, cl(a))

def argb(rgb, a=1.0):
    return skia.ColorSetARGB(int(255 * cl(a)), int(rgb[0]), int(rgb[1]), int(rgb[2]))

def paint(rgb=WHITE, a=1.0, stroke=0, blur=0, blend=None, shader=None, cap=True):
    p = skia.Paint()
    p.setAntiAlias(True)
    p.setColor4f(C(rgb, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        if cap:
            p.setStrokeCap(skia.Paint.kRound_Cap)
            p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if blend is not None:
        p.setBlendMode(blend)
    if shader is not None:
        p.setShader(shader)
    return p

PLUS = skia.BlendMode.kPlus
SCREEN = skia.BlendMode.kScreen

def lin(x0, y0, x1, y1, cols, pos=None):
    return skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], cols, pos)

def rad(cx, cy, r, cols, pos=None):
    return skia.GradientShader.MakeRadial(skia.Point(cx, cy), r, cols, pos)

def glow_disc(c, cx, cy, r, rgb, a):
    if a <= 0.003: return
    c.drawCircle(cx, cy, r, paint(shader=rad(cx, cy, r, [argb(rgb, a), argb(rgb, a * 0.35), argb(rgb, 0)], [0, 0.45, 1]), blend=PLUS))

# ------------------------------------------------------------------ text
def tw(s, key, size, sp=0.0):
    f = font(key, size)
    if not sp:
        return f.measureText(s)
    return sum(f.measureText(ch) for ch in s) + sp * (len(s) - 1)

def text(c, s, x, y, key='sgb', size=40, rgb=WHITE, a=1.0, align='c', sp=0.0, glow=0.0, glow_rgb=None,
         shadow=0.0, blend=None):
    if a <= 0.003 or not s:
        return 0
    f = font(key, size)
    w = tw(s, key, size, sp)
    x0 = x - w / 2 if align == 'c' else (x - w if align == 'r' else x)

    def draw(p, dx=0, dy=0):
        if not sp:
            c.drawString(s, x0 + dx, y + dy, f, p)
        else:
            xx = x0 + dx
            for ch in s:
                c.drawString(ch, xx, y + dy, f, p)
                xx += f.measureText(ch) + sp
    if shadow:
        draw(paint((0, 0, 0), a * shadow, blur=size * 0.12), 0, size * 0.05)
    if glow:
        draw(paint(glow_rgb or rgb, a * glow, blur=size * 0.22, blend=PLUS))
    draw(paint(rgb, a, blend=blend))
    return w

def wrap(s, key, size, maxw):
    words = s.split()
    lines, cur = [], ''
    for wd in words:
        trial = (cur + ' ' + wd).strip()
        if tw(trial, key, size) <= maxw:
            cur = trial
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines

# ------------------------------------------------------------------ shapes
def rrect(c, x, y, w, h, r, p):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), p)

def poly(pts, close=False):
    p = skia.Path()
    if not pts:
        return p
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    return p

def partial(pts, frac):
    """first frac (0..1) of a polyline by length"""
    if frac >= 1: return pts
    if frac <= 0 or len(pts) < 2: return pts[:1]
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(seg); target = total * frac; acc = 0
    out = [pts[0]]
    for i, L in enumerate(seg):
        if acc + L >= target:
            k = (target - acc) / L if L else 0
            out.append((lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k)))
            return out
        out.append(pts[i + 1]); acc += L
    return out

def glow_path(c, path, rgb, a, width, glow=1.0, core=True):
    if a <= 0.003: return
    if glow > 0:
        c.drawPath(path, paint(rgb, a * 0.55 * glow, stroke=width * 3.2, blur=width * 2.2, blend=PLUS))
    c.drawPath(path, paint(rgb, a, stroke=width))
    if core:
        c.drawPath(path, paint(mix(rgb, WHITE, 0.6), a * 0.8, stroke=max(1.0, width * 0.35)))

def arrow(c, x0, y0, x1, y1, rgb, a, width=6, head=22, glow=0.8, frac=1.0):
    if a <= 0.003 or frac <= 0: return
    x1p, y1p = lerp(x0, x1, frac), lerp(y0, y1, frac)
    ang = math.atan2(y1 - y0, x1 - x0)
    tipx, tipy = x1p, y1p
    shaft_end = (tipx - math.cos(ang) * head * 0.8, tipy - math.sin(ang) * head * 0.8)
    glow_path(c, poly([(x0, y0), shaft_end]), rgb, a, width, glow, core=False)
    hp = poly([(tipx, tipy),
               (tipx - math.cos(ang - 0.45) * head, tipy - math.sin(ang - 0.45) * head),
               (tipx - math.cos(ang + 0.45) * head, tipy - math.sin(ang + 0.45) * head)], True)
    c.drawPath(hp, paint(rgb, a * 0.5 * glow, blur=8, blend=PLUS))
    c.drawPath(hp, paint(rgb, a))

def pill(c, cx, cy, w, h, rgb, a, fill=0.12, stroke=2.0, glow=0.0):
    if a <= 0.003: return
    x, y = cx - w / 2, cy - h / 2
    rrect(c, x, y, w, h, h / 2, paint(rgb, a * fill))
    if glow:
        rrect(c, x, y, w, h, h / 2, paint(rgb, a * glow, stroke=stroke * 3, blur=10, blend=PLUS))
    rrect(c, x, y, w, h, h / 2, paint(rgb, a * 0.9, stroke=stroke))

# ------------------------------------------------------------------ padlock
def _crack_pts(cx, cy, s, seed=4):
    pts = []
    n = 11
    for i in range(n + 1):
        x = cx - 0.82 * s + 1.64 * s * i / n
        y = cy + 0.1 * s + (hsh(i, seed) - 0.5) * 0.42 * s + 0.12 * s * math.sin(i * 1.7)
        pts.append((x, y))
    return pts

def padlock(c, cx, cy, s, rgb=CYAN, a=1.0, crack=0.0, open_=0.0, glow=1.0, fill_a=0.10, body_rgb=None,
            width=None, keyhole=True, flicker=1.0):
    """cx, cy = centre of the body"""
    if a <= 0.003: return
    width = width or max(2.0, s * 0.075)
    a *= flicker
    bw, bh = 1.7 * s, 1.3 * s
    bx, by = cx - bw / 2, cy - bh / 2
    body = skia.Path(); body.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(bx, by, bw, bh), 0.2 * s, 0.2 * s))
    # shackle
    r = 0.52 * s
    lift = 0.38 * s * eo(open_)
    sh = skia.Path()
    top = by - 0.55 * s - lift
    sh.moveTo(cx - r, by + 0.02 * s - lift * 0.15)
    sh.lineTo(cx - r, top)
    sh.arcTo(skia.Rect.MakeXYWH(cx - r, top - r, 2 * r, 2 * r), 180, 180, False)
    sh.lineTo(cx + r, by + 0.02 * s - lift)
    brgb = body_rgb or rgb
    c.drawPath(body, paint(shader=lin(0, by, 0, by + bh, [argb(brgb, fill_a * 1.6 * a), argb(brgb, fill_a * 0.5 * a)])))
    glow_path(c, sh, rgb, a, width * 1.15, glow)
    glow_path(c, body, brgb, a, width, glow)
    if keyhole:
        kx, ky = cx, cy + 0.02 * s
        kh = skia.Path()
        kh.addCircle(kx, ky - 0.06 * s, 0.13 * s)
        kh.moveTo(kx - 0.06 * s, ky)
        kh.lineTo(kx - 0.1 * s, ky + 0.28 * s)
        kh.lineTo(kx + 0.1 * s, ky + 0.28 * s)
        kh.lineTo(kx + 0.06 * s, ky)
        kh.close()
        c.drawPath(kh, paint(brgb, a * 0.85))
        c.drawPath(kh, paint(brgb, a * 0.4 * glow, blur=10, blend=PLUS))
    if crack > 0:
        pts = partial(_crack_pts(cx, cy, s), eo(crack))
        p = poly(pts)
        c.drawPath(p, paint(RED, a * 0.9, stroke=width * 2.6, blur=width * 2.5, blend=PLUS))
        c.drawPath(p, paint((255, 235, 240), a, stroke=width * 0.55))
        # branches
        full = _crack_pts(cx, cy, s)
        for i in (3, 6, 8):
            if eo(crack) * 11 > i:
                x, y = full[i]
                d = 1 if i % 2 else -1
                br = [(x, y), (x + 0.1 * s, y + d * 0.18 * s), (x + 0.06 * s, y + d * 0.32 * s)]
                c.drawPath(poly(br), paint((255, 220, 230), a * 0.9, stroke=width * 0.4))
                c.drawPath(poly(br), paint(RED, a * 0.6, stroke=width * 1.5, blur=6, blend=PLUS))

def mini_lock(c, cx, cy, s, rgb, a):
    if a <= 0.01: return
    w = max(1.5, s * 0.16)
    rrect(c, cx - 0.8 * s, cy - 0.45 * s, 1.6 * s, 1.15 * s, 0.22 * s, paint(rgb, a * 0.8))
    p = skia.Path()
    p.moveTo(cx - 0.45 * s, cy - 0.4 * s); p.lineTo(cx - 0.45 * s, cy - 0.7 * s)
    p.arcTo(skia.Rect.MakeXYWH(cx - 0.45 * s, cy - 1.15 * s, 0.9 * s, 0.9 * s), 180, 180, False)
    p.lineTo(cx + 0.45 * s, cy - 0.4 * s)
    c.drawPath(p, paint(rgb, a, stroke=w))

# ------------------------------------------------------------------ icons (line style)
def icon_bank(c, cx, cy, s, rgb, a):
    w = s * 0.07
    pp = paint(rgb, a, stroke=w)
    c.drawPath(poly([(cx - s * 0.62, cy - s * 0.25), (cx, cy - s * 0.62), (cx + s * 0.62, cy - s * 0.25)], True), pp)
    for i in range(4):
        x = cx - s * 0.42 + i * s * 0.28
        c.drawLine(x, cy - s * 0.12, x, cy + s * 0.38, pp)
    c.drawLine(cx - s * 0.66, cy + s * 0.52, cx + s * 0.66, cy + s * 0.52, pp)

def icon_mail(c, cx, cy, s, rgb, a):
    w = s * 0.07
    pp = paint(rgb, a, stroke=w)
    rrect(c, cx - s * 0.62, cy - s * 0.42, s * 1.24, s * 0.84, s * 0.1, pp)
    c.drawPath(poly([(cx - s * 0.58, cy - s * 0.36), (cx, cy + s * 0.08), (cx + s * 0.58, cy - s * 0.36)]), pp)

def icon_card(c, cx, cy, s, rgb, a):
    w = s * 0.07
    pp = paint(rgb, a, stroke=w)
    rrect(c, cx - s * 0.66, cy - s * 0.42, s * 1.32, s * 0.84, s * 0.1, pp)
    c.drawLine(cx - s * 0.66, cy - s * 0.18, cx + s * 0.66, cy - s * 0.18, pp)
    rrect(c, cx - s * 0.48, cy + s * 0.02, s * 0.3, s * 0.22, s * 0.04, pp)
    c.drawLine(cx + s * 0.05, cy + s * 0.22, cx + s * 0.45, cy + s * 0.22, pp)

def icon_browser(c, cx, cy, s, rgb, a):
    w = s * 0.06
    pp = paint(rgb, a, stroke=w)
    rrect(c, cx - s * 0.75, cy - s * 0.5, s * 1.5, s * 1.0, s * 0.1, pp)
    c.drawLine(cx - s * 0.75, cy - s * 0.24, cx + s * 0.75, cy - s * 0.24, pp)
    for i in range(3):
        c.drawCircle(cx - s * 0.62 + i * s * 0.12, cy - s * 0.37, s * 0.035, paint(rgb, a))
    rrect(c, cx - s * 0.6, cy - s * 0.08, s * 1.2, s * 0.26, s * 0.13, pp)
    mini_lock(c, cx - s * 0.45, cy + s * 0.07, s * 0.09, rgb, a)
    c.drawLine(cx - s * 0.3, cy + s * 0.05, cx + s * 0.45, cy + s * 0.05, paint(rgb, a * 0.6, stroke=w * 0.8))

def icon_plane(c, cx, cy, s, rgb, a):
    w = s * 0.07
    pp = paint(rgb, a, stroke=w)
    c.drawPath(poly([(cx - s * 0.6, cy - s * 0.05), (cx + s * 0.6, cy - s * 0.5), (cx + s * 0.25, cy + s * 0.55),
                     (cx - s * 0.02, cy + s * 0.12)], True), pp)
    c.drawLine(cx - s * 0.02, cy + s * 0.12, cx + s * 0.6, cy - s * 0.5, pp)

# ------------------------------------------------------------------ coin
def coin(c, cx, cy, r, a=1.0, spin=0.0, glow=0.6):
    if a <= 0.003: return
    sx = max(0.08, abs(math.cos(spin)))
    c.save(); c.translate(cx, cy); c.scale(sx, 1)
    c.drawCircle(0, 0, r * 1.25, paint(GOLD, a * 0.25 * glow, blur=r * 0.35, blend=PLUS))
    c.drawCircle(0, 0, r, paint(shader=rad(-r * 0.3, -r * 0.35, r * 1.6,
                                         [argb((255, 226, 140), a), argb((235, 160, 40), a), argb((150, 90, 20), a)], [0, 0.55, 1])))
    c.drawCircle(0, 0, r * 0.82, paint((255, 236, 170), a * 0.7, stroke=max(1.5, r * 0.05)))
    if sx > 0.3:
        f = r * 1.05
        text(c, 'B', -f * 0.02, f * 0.36, 'sgb', f, (120, 70, 10), a * 0.9)
        for dx in (-0.12, 0.1):
            c.drawLine(dx * r, -r * 0.62, dx * r, -r * 0.42, paint((120, 70, 10), a * 0.9, stroke=r * 0.08, cap=False))
            c.drawLine(dx * r, r * 0.42, dx * r, r * 0.62, paint((120, 70, 10), a * 0.9, stroke=r * 0.08, cap=False))
    c.restore()

# ------------------------------------------------------------------ stamp
def stamp(c, cx, cy, s, rgb, a, angle, scale=1.0):
    if a <= 0.003: return
    c.save(); c.translate(cx, cy); c.rotate(angle); c.scale(scale, scale)
    size = 74
    w = tw(s, 'sgb', size, 4) + 70; h = 126
    rrect(c, -w / 2, -h / 2, w, h, 14, paint(rgb, a * 0.10))
    rrect(c, -w / 2, -h / 2, w, h, 14, paint(rgb, a * 0.5, stroke=14, blur=12, blend=PLUS))
    rrect(c, -w / 2, -h / 2, w, h, 14, paint(rgb, a, stroke=8))
    rrect(c, -w / 2 + 12, -h / 2 + 12, w - 24, h - 24, 8, paint(rgb, a * 0.6, stroke=2.5))
    text(c, s, 0, size * 0.36, 'sgb', size, rgb, a, sp=4, glow=0.5)
    c.restore()
