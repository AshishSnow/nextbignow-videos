"""Cinematic set + post kit for the v3 look: layered atmospheric landscapes, haze, depth of field, grass,
fireflies, light rays, bloom, colour grade, vignette and film grain. Built for the hero.py character."""
import math
import numpy as np
import skia
from toon import *
from gfx import SCREEN, PLUS, glow_disc
from ed import img_from

MUL = skia.BlendMode.kMultiply
FULLR = R.MakeWH(W, H)


def vgrad(c, stops, y0=0, y1=H, rect=None):
    cols = [argb(col) if len(col) == 3 else argb(col[:3], col[3]) for _, col in stops]
    pos = [p for p, _ in stops]
    c.drawRect(rect or FULLR, paint(shader=lin(0, y0, 0, y1, cols, pos)))


def blurred(c, sigma, fn, alpha=1.0, bounds=None):
    """Draw fn() into a layer and blur it (depth of field). bounds (local rect) keeps the layer small."""
    if sigma <= 0.3 and alpha >= 1:
        fn(); return
    p = skia.Paint()
    if sigma > 0.3:
        p.setImageFilter(skia.ImageFilters.Blur(sigma, sigma, skia.TileMode.kDecal, None))
    if alpha < 1: p.setAlphaf(alpha)
    c.saveLayer(bounds, p); fn(); c.restore()


# ------------------------------------------------------------------ landscape layers
def ridge_path(y, amp, seed, freq=1.0, rough=0.35, x0=-200, x1=W + 200, bottom=H + 400, step=12):
    p = skia.Path(); p.moveTo(x0, bottom)
    ph = [hsh(seed, k) * 6.283 for k in range(6)]
    for i in range(int((x1 - x0) / step) + 1):
        x = x0 + i * step; u = x / W * freq
        v = (math.sin(u * 2.1 + ph[0]) * 0.55 + math.sin(u * 4.7 + ph[1]) * 0.25 + math.sin(u * 9.3 + ph[2]) * 0.12 * (1 + rough)
             + math.sin(u * 21 + ph[3]) * 0.05 * rough * 2)
        p.lineTo(x, y - v * amp)
    p.lineTo(x1, bottom); p.close()
    return p


def fill_layer(c, path, top_col, bot_col, y0, y1, edge=None, edge_a=0.0, edge_w=3):
    c.drawPath(path, paint(shader=lin(0, y0, 0, y1, [argb(top_col), argb(bot_col)])))
    if edge and edge_a > 0:
        c.save(); c.clipPath(path, doAntiAlias=True)
        c.drawPath(path, paint(edge, edge_a, stroke=edge_w * 2, blur=edge_w * 0.6, blend=PLUS))
        c.restore()


def tree_path(y, seed, h=150, spacing=70, x0=-120, x1=W + 120, jitter=0.5, round_=True):
    """Rounded-canopy tree line silhouette (crowns + trunks), base at y."""
    parts = skia.Path()
    x = x0; k = 0
    while x < x1:
        r = h * (0.32 + 0.22 * hsh(k, seed))
        cy = y - h * (0.55 + 0.35 * hsh(k, seed + 1))
        parts.addOval(R.MakeXYWH(x - r * 0.9, cy - r * 1.25, r * 1.8, r * 2.5))
        parts.addRect(R.MakeXYWH(x - r * 0.10, cy, r * 0.2, y - cy + 4))
        x += spacing * (0.6 + jitter * hsh(k, seed + 2)); k += 1
    parts.addRect(R.MakeXYWH(x0, y - h * 0.25, x1 - x0, H))
    parts.setFillType(skia.PathFillType.kWinding)
    return skia.Op(parts, parts, skia.PathOp.kUnion_PathOp) or parts


def haze(c, y_mid, h, col, a):
    c.drawRect(R.MakeXYWH(-50, y_mid - h, W + 100, 2 * h),
               paint(shader=lin(0, y_mid - h, 0, y_mid + h, [argb(col, 0), argb(col, a), argb(col, 0)], [0, 0.5, 1])))


def sun_glow(c, x, y, r, col, a=0.8):
    c.drawCircle(x, y, r, paint(shader=rad(x, y, r, [argb(col, a), argb(col, a * 0.35), argb(col, 0)], [0, 0.35, 1]), blend=SCREEN))


def cloud_streaks(c, t, seed, y0, y1, col, a=0.6, n=7, drift=6.0, lit=None):
    for i in range(n):
        u = hsh(i, seed)
        y = lerp(y0, y1, hsh(i, seed + 1))
        w = 300 + 520 * hsh(i, seed + 2); h = 18 + 40 * hsh(i, seed + 3)
        x = (u * (W + 900) + t * drift * (0.6 + hsh(i, seed + 4))) % (W + 900) - 450
        c.drawOval(R.MakeXYWH(x - w / 2, y - h / 2, w, h), paint(col, a * (0.5 + 0.5 * hsh(i, seed + 5)), blur=h * 0.45))
        if lit:
            c.drawOval(R.MakeXYWH(x - w * 0.42, y + h * 0.05, w * 0.84, h * 0.45), paint(lit, a * 0.7, blur=h * 0.25, blend=SCREEN))


def stars(c, seed, y1, n=80, a=0.8, t=0.0):
    for i in range(n):
        x = hsh(i, seed) * W; y = hsh(i, seed + 1) * y1
        k = (1 - y / y1) ** 1.5
        tw_ = 0.6 + 0.4 * math.sin(t * (1 + 3 * hsh(i, seed + 3)) + i)
        c.drawCircle(x, y, 1.2 + 1.6 * hsh(i, seed + 2), paint((255, 250, 240), a * k * tw_))


def god_rays(c, src, t, col, a=0.18, n=7, spread=70, length=2600, seed=3):
    sx, sy = src
    for i in range(n):
        ang = math.radians(90 + (hsh(i, seed) - 0.5) * spread + math.sin(t * 0.3 + i) * 1.5)
        w = math.radians(1.5 + 4 * hsh(i, seed + 1))
        p = skia.Path(); p.moveTo(sx, sy)
        p.lineTo(sx + math.cos(ang - w) * length, sy + math.sin(ang - w) * length)
        p.lineTo(sx + math.cos(ang + w) * length, sy + math.sin(ang + w) * length); p.close()
        aa = a * (0.4 + 0.6 * hsh(i, seed + 2)) * (0.75 + 0.25 * math.sin(t * 0.7 + i * 1.7))
        c.drawPath(p, paint(shader=rad(sx, sy, length, [argb(col, aa), argb(col, aa * 0.4), argb(col, 0)], [0, 0.4, 1]), blur=10, blend=SCREEN))


def fireflies(c, t, n, seed, box, col=(255, 220, 120), size=4.0, a=1.0, drift=18):
    x0, y0, x1, y1 = box
    for i in range(n):
        ph = hsh(i, seed) * 6.283
        x = lerp(x0, x1, hsh(i, seed + 1)) + math.sin(t * 0.6 + ph) * drift + math.sin(t * 1.7 + ph * 2) * drift * 0.3
        y = lerp(y0, y1, hsh(i, seed + 2)) + math.cos(t * 0.5 + ph) * drift * 0.7
        k = max(0.0, math.sin(t * (1.2 + hsh(i, seed + 3)) + ph)) ** 2
        r = size * (0.6 + 0.8 * hsh(i, seed + 4))
        if k * a > 0.02:
            glow_disc(c, x, y, r * 6, col, 0.55 * k * a)
            c.drawCircle(x, y, r * 0.6, paint((255, 255, 230), k * a))


def dust(c, t, n, seed, box, col=(255, 230, 190), a=0.5, size=2.5, wind=(20, -6), blur=0):
    x0, y0, x1, y1 = box
    for i in range(n):
        ph = hsh(i, seed) * 6.283
        x = x0 + ((hsh(i, seed + 1) * (x1 - x0) + t * wind[0] * (0.5 + hsh(i, seed + 5))) % (x1 - x0))
        y = y0 + ((hsh(i, seed + 2) * (y1 - y0) + t * wind[1] * (0.5 + hsh(i, seed + 6)) + math.sin(t + ph) * 8) % (y1 - y0))
        tw_ = 0.5 + 0.5 * math.sin(t * 2 + ph)
        c.drawCircle(x, y, size * (0.5 + hsh(i, seed + 3)), paint(col, a * tw_, blur=blur, blend=SCREEN))


# ------------------------------------------------------------------ grass
class Grass:
    """Perspective grass field between horizon_y and bottom. Blades are batched per depth band."""
    def __init__(self, horizon_y, bottom=H + 40, n=1400, seed=7, x0=-100, x1=W + 100, h_near=150, h_far=10,
                 cols=((58, 92, 50), (96, 140, 62)), tip=(222, 196, 120), bands=6, clump=7):
        self.hy, self.by, self.tip = horizon_y, bottom, tip
        self.bands = [[] for _ in range(bands)]
        rng = np.random.default_rng(seed)
        nc = max(1, n // clump)
        for ci in range(nc):
            d0 = rng.random() ** 1.5
            cx = rng.uniform(x0, x1)
            for j in range(clump):
                d = min(1.0, max(0.0, d0 + rng.normal(0, 0.004)))
                y = lerp(horizon_y, bottom, d)
                x = cx + rng.normal(0, lerp(4, 26, d))
                hgt = lerp(h_far, h_near, d) * rng.uniform(0.55, 1.25)
                lean = rng.normal(0, 0.32)
                w = lerp(2.2, 13.0, d) * rng.uniform(0.7, 1.3)
                col = mix(cols[0], cols[1], rng.random())
                b = min(bands - 1, int(d * bands))
                self.bands[b].append((x, y, hgt, lean, w, col, rng.random() * 6.283))
        for b in self.bands: b.sort(key=lambda q: q[1])
        self.cols = cols

    def draw(self, c, t, wind=1.0, light=(255, 210, 150), shade_k=0.0, band_range=None, gust=0.0):
        rng_ = band_range or range(len(self.bands))
        for bi in rng_:
            band = self.bands[bi]
            if not band: continue
            depth = (bi + 0.5) / len(self.bands)
            dk = mix((0, 0, 0), (0, 0, 0), 0)
            body = skia.Path(); tips = skia.Path()
            for (x, y, h, ln, w, col, ph) in band:
                sway = (math.sin(t * 1.6 + x * 0.008 + ph * 0.3) * 0.18 + gust * (0.5 + 0.5 * math.sin(t * 6 + ph))) * wind
                a = ln + sway
                tx, ty = x + math.sin(a) * h, y - math.cos(a) * h
                mx, my = x + math.sin(a * 0.5) * h * 0.55, y - math.cos(a * 0.5) * h * 0.55
                body.moveTo(x - w / 2, y); body.quadTo(mx - w * 0.3, my, tx, ty); body.quadTo(mx + w * 0.3, my, x + w / 2, y); body.close()
                tips.moveTo(mx, my); tips.quadTo((mx + tx) / 2, (my + ty) / 2, tx, ty)
            top = mix(self.cols[1], light, 0.25)
            ylo = band[0][1] - 160; yhi = band[-1][1]
            c.drawPath(body, paint(shader=lin(0, ylo, 0, yhi + 10, [argb(top), argb(mix(self.cols[0], (0, 0, 0), 0.35 * (1 - depth) + 0.1))])))
            c.drawPath(tips, paint(self.tip, 0.10 + 0.12 * depth, stroke=max(1.0, depth * 2.5), blend=SCREEN))


# ------------------------------------------------------------------ captions (v3 style)
YEL = (255, 214, 10)


def fit_size(parts, key, size, maxw):
    f = font(key, size)
    w = sum(f.measureText(p[0]) for p in parts)
    return size * min(1.0, maxw / max(1, w))


def caption(c, t, t0, parts, y, size=140, key='ant', t1=None, maxw=840, pop=True, stroke_k=0.12, x=W / 2):
    """parts = [('WHAT IF ', WHITE), ('CLOSER?', YEL)] -> bold condensed caption, black stroke + soft shadow."""
    if t < t0 or (t1 is not None and t > t1 + 0.15): return
    u = t - t0
    a = cl(u / 0.08)
    if t1 is not None and t > t1: a *= cl(1 - (t - t1) / 0.15)
    sc = 1.0 + (0.28 * (1 - eback(cl(u / 0.22))) if pop else 0)
    size = fit_size(parts, key, size, maxw)
    f = font(key, size)
    widths = [f.measureText(p[0]) for p in parts]
    tw_ = sum(widths)
    c.save(); c.translate(x, y); c.scale(sc, sc)
    xx = -tw_ / 2
    sw = size * stroke_k
    # shadow
    for (s, col), w_ in zip(parts, widths):
        blob = skia.TextBlob(s, f)
        c.drawTextBlob(blob, xx + size * 0.03, size * 0.06, paint((0, 0, 0), 0.55 * a, blur=size * 0.06))
        xx += w_
    xx = -tw_ / 2
    for (s, col), w_ in zip(parts, widths):
        blob = skia.TextBlob(s, f)
        pp = stroke((0, 0, 0), sw, a); c.drawTextBlob(blob, xx, 0, pp)
        xx += w_
    xx = -tw_ / 2
    for (s, col), w_ in zip(parts, widths):
        blob = skia.TextBlob(s, f)
        c.drawTextBlob(blob, xx, 0, paint(col, a))
        xx += w_
    c.restore()


def pill(c, t, t0, text, x, y, col=(226, 40, 52), size=46, t1=None, txt=(255, 255, 255)):
    if t < t0 or (t1 is not None and t > t1 + 0.2): return
    a = cl((t - t0) / 0.12)
    if t1 is not None and t > t1: a *= cl(1 - (t - t1) / 0.2)
    k = eback(cl((t - t0) / 0.25))
    f = font('ant', size); w = f.measureText(text) + size * 0.9; h = size * 1.35
    c.save(); c.translate(x, y); c.scale(k, k)
    c.drawRoundRect(R.MakeXYWH(-w / 2 + 3, -h / 2 + 6, w, h), h / 2, h / 2, paint((0, 0, 0), 0.4 * a, blur=6))
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2, paint(shader=lin(0, -h / 2, 0, h / 2, [argb(mix(col, (255, 255, 255), 0.18), a), argb(col, a)])))
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2, stroke((255, 255, 255), 3, 0.85 * a))
    c.drawString(text, -f.measureText(text) / 2, size * 0.36, f, paint(txt, a))
    c.restore()


# ------------------------------------------------------------------ post
def _mat_mul(a, b):
    A = np.eye(5); A[:4, :] = np.array(a).reshape(4, 5)
    B = np.eye(5); B[:4, :] = np.array(b).reshape(4, 5)
    return list((A @ B)[:4, :].reshape(-1))


def grade_matrix(sat=1.2, contrast=1.12, gain=(1.03, 1.0, 0.96), lift=(-0.004, 0.006, 0.02), exposure=1.0):
    lr, lg, lb = 0.2126, 0.7152, 0.0722
    s = sat
    S = [lr * (1 - s) + s, lg * (1 - s), lb * (1 - s), 0, 0,
         lr * (1 - s), lg * (1 - s) + s, lb * (1 - s), 0, 0,
         lr * (1 - s), lg * (1 - s), lb * (1 - s) + s, 0, 0,
         0, 0, 0, 1, 0]
    k = contrast; o = 0.5 * (1 - k)
    C = [k, 0, 0, 0, o, 0, k, 0, 0, o, 0, 0, k, 0, o, 0, 0, 0, 1, 0]
    G = [gain[0] * exposure, 0, 0, 0, lift[0], 0, gain[1] * exposure, 0, 0, lift[1], 0, 0, gain[2] * exposure, 0, lift[2], 0, 0, 0, 1, 0]
    return _mat_mul(G, _mat_mul(C, S))


class Post:
    def __init__(self, bloom=0.45, thresh=0.58, grade=None, vig=0.66, grain=0.045, vig_col=(10, 6, 12)):
        self.bloom, self.th, self.vig, self.grain = bloom, thresh, vig, grain
        self.S = skia.Surface(W, H)
        self.q = skia.Surface(W // 4, H // 4)
        k = 1.0 / (1 - thresh)
        self.TH = skia.ColorFilters.Matrix([k, 0, 0, 0, -thresh * k, 0, k, 0, 0, -thresh * k, 0, 0, k, 0, -thresh * k, 0, 0, 0, 1, 0])
        self.GR = skia.ColorFilters.Matrix(grade or grade_matrix())
        self.VIG = paint(shader=rad(W / 2, H * 0.47, max(W, H) * 0.72, [argb((255, 255, 255)), argb((255, 255, 255)), argb(mix(vig_col, (255, 255, 255), 1 - vig))], [0, 0.5, 1]), blend=MUL)
        rng = np.random.default_rng(11)
        self.GN = []
        for i in range(6):
            n = rng.normal(128, 40, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)
            a = np.dstack([n, n, n, np.full_like(n, 255)])
            self.GN.append(img_from(a, False))

    def set_grade(self, m):
        self.GR = skia.ColorFilters.Matrix(m)

    def apply(self, img, t, bloom=None):
        q = self.q.getCanvas(); q.clear(skia.ColorTRANSPARENT)
        p = skia.Paint(); p.setColorFilter(self.TH); p.setImageFilter(skia.ImageFilters.Blur(7, 7, skia.TileMode.kClamp, None))
        q.drawImageRect(img, R.MakeWH(W // 4, H // 4), LINS, p)
        b = self.q.makeImageSnapshot()
        o = self.S.getCanvas()
        pg = skia.Paint(); pg.setColorFilter(self.GR)
        o.drawImage(img, 0, 0, LINS, pg)
        pb = skia.Paint(); pb.setBlendMode(SCREEN); pb.setAlphaf(self.bloom if bloom is None else bloom)
        o.drawImageRect(b, FULLR, LINS, pb)
        o.drawRect(FULLR, self.VIG)
        if self.grain > 0:
            pn = skia.Paint(); pn.setBlendMode(skia.BlendMode.kOverlay); pn.setAlphaf(self.grain)
            o.drawImageRect(self.GN[int(t * 24) % len(self.GN)], FULLR, LINS, pn)
        return self.S.makeImageSnapshot()


# ------------------------------------------------------------------ realistic moon
_MOON = {}


def moon_img(size, seed=5, warm=0.0, light=None):
    key = (size, seed, round(warm, 2), light)
    if key in _MOON: return _MOON[key]
    from ed import _upnoise
    rng = np.random.default_rng(seed)
    n = size
    y, x = np.mgrid[0:n, 0:n].astype(np.float32)
    x = (x + 0.5) / n * 2 - 1; y = (y + 0.5) / n * 2 - 1
    r2 = x * x + y * y; m = r2 < 1; z = np.sqrt(np.clip(1 - r2, 0, 1))
    maria = _upnoise(rng, 5, 5, n, n) * 1.0 + _upnoise(rng, 11, 11, n, n) * 0.45
    maria = np.clip((maria - 0.05) * 3.2, 0, 1)
    fine = _upnoise(rng, 60, 60, n, n) * 0.5 + _upnoise(rng, 160, 160, n, n) * 0.35 + rng.normal(0, 0.05, (n, n))
    alb = 0.97 - 0.30 * maria + fine * 0.07
    # small craters: bright rims + dark floors
    for i in range(45):
        cx, cy = rng.uniform(-0.9, 0.9, 2); rr = rng.uniform(0.006, 0.03)
        d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / rr
        alb += -0.035 * np.exp(-(d / 0.8) ** 2) + np.exp(-((d - 1.0) / 0.35) ** 2) * 0.03
    # bright young crater with faint rays
    cx, cy = 0.22, 0.55
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    ang = np.arctan2(y - cy, x - cx)
    rays = (np.cos(ang * 7 + 1.3) * 0.5 + 0.5) ** 4 * np.exp(-d / 0.5) * 0.07
    alb += rays + np.exp(-(d / 0.03) ** 2) * 0.05
    shade = 0.80 + 0.20 * z
    v = np.clip(alb * shade, 0, 1.15)
    base = np.array([255, 250, 240], np.float32)
    tint = np.array([255, 196, 150], np.float32)
    col = v[..., None] * (base * (1 - warm) + tint * warm)
    # warm lower limb (atmosphere)
    col *= (1 - 0.18 * np.clip(y, 0, 1))[..., None] * np.array([1.0, 0.94, 0.86])[None, None, :] + np.clip(-y, 0, 1)[..., None] * 0.0
    if light is not None:
        Lv = np.array(light, np.float32); Lv /= np.linalg.norm(Lv)
        lam = np.clip(x * Lv[0] + y * Lv[1] + z * Lv[2], 0, 1)
        col *= (0.035 + 0.965 * np.clip(lam * 1.25, 0, 1) ** 0.8)[..., None]
    edge = np.clip((1 - np.sqrt(r2)) * n / 2.0, 0, 1)
    out = np.zeros((n, n, 4), np.float32)
    out[..., :3] = np.clip(col, 0, 255) * edge[..., None]
    out[..., 3] = edge * 255
    out[~m] = 0
    im = img_from(out.astype(np.uint8), False)
    _MOON[key] = im
    return im


def draw_moon(c, cx, cy, r, glow=(255, 226, 200), ga=0.5, warm=0.15, low_haze=(255, 150, 110), lha=0.5, light=None):
    size = 1024 if r > 300 else (640 if r > 120 else 320)
    im = moon_img(size, warm=warm, light=light)
    sun_glow(c, cx, cy, r * 2.4, glow, ga * 0.6)
    sun_glow(c, cx, cy, r * 1.35, glow, ga)
    c.drawImageRect(im, R.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), LINS, skia.Paint())
    if lha > 0:
        c.save(); p = skia.Path(); p.addCircle(cx, cy, r); c.clipPath(p, doAntiAlias=True)
        c.drawRect(R.MakeLTRB(cx - r, cy - r * 0.1, cx + r, cy + r),
                   paint(shader=lin(0, cy - r * 0.1, 0, cy + r, [argb(low_haze, 0), argb(low_haze, lha)]), blend=MUL))
        c.restore()


# ------------------------------------------------------------------ organic tree rows
def crown_row_path(y, seed, h=150, spacing=70, x0=-160, x1=W + 160, conifer=0.15, tall=0.12):
    parts = []
    x = x0; k = 0
    while x < x1:
        r = h * (0.30 + 0.18 * hsh(k, seed))
        if hsh(k, seed + 9) < tall: r *= 1.35
        top = y - h * (0.55 + 0.35 * hsh(k, seed + 1)) * (1.3 if hsh(k, seed + 9) < tall else 1)
        p = skia.Path()
        if hsh(k, seed + 7) < conifer:
            for j in range(4):
                yy = top + j * r * 0.55; ww = r * (0.45 + 0.28 * j)
                p.moveTo(x, yy - r * 0.35); p.lineTo(x + ww, yy + r * 0.45); p.lineTo(x - ww, yy + r * 0.45); p.close()
            p.addRect(R.MakeXYWH(x - r * 0.08, top + r * 1.8, r * 0.16, y - top))
        else:
            nb = 4 + int(hsh(k, seed + 3) * 3)
            for j in range(nb):
                a = (j / nb) * math.pi * 1.1 + math.pi * 0.95
                bx = x + math.cos(a) * r * 0.55 + (hsh(j, k + seed) - 0.5) * r * 0.3
                by = top + r * 0.9 + math.sin(a) * r * 0.6
                br = r * (0.45 + 0.25 * hsh(j + 3, k + seed))
                p.addCircle(bx, by, br)
            p.addCircle(x, top + r * 0.95, r * 0.75)
            for j in range(9):
                a = math.pi * (1.05 + 0.9 * j / 8)
                lr = r * (0.16 + 0.1 * hsh(j + 11, k + seed))
                p.addCircle(x + math.cos(a) * r * 0.86, top + r * 0.95 + math.sin(a) * r * 0.86, lr)
            p.addRect(R.MakeXYWH(x - r * 0.07, top + r, r * 0.14, y - top))
        parts.append(p)
        x += spacing * (0.55 + 0.6 * hsh(k, seed + 2)); k += 1
    base = skia.Path(); base.addRect(R.MakeXYWH(x0, y - h * 0.42, x1 - x0, H))
    out = base
    for p in parts:
        p.setFillType(skia.PathFillType.kWinding)
        out = skia.Op(out, p, skia.PathOp.kUnion_PathOp) or out
    return out


def rim_fill(c, path, top_col, bot_col, y0, y1, rim_col=None, rim_a=0.0, rim_dir=(0, -1), rim_w=4):
    c.drawPath(path, paint(shader=lin(0, y0, 0, y1, [argb(top_col), argb(bot_col)])))
    if rim_col and rim_a > 0:
        q = skia.Path(path); q.offset(-rim_dir[0] * rim_w, -rim_dir[1] * rim_w)
        rp = skia.Op(path, q, skia.PathOp.kDifference_PathOp)
        if rp is not None:
            c.drawPath(rp, paint(rim_col, rim_a, blur=rim_w * 0.9, blend=PLUS))


def ground_tex(c, y0, y1, col_far, col_near, seed=3, blotch=(0, 0, 0), ba=0.22, t=0.0):
    vgrad(c, [(0, col_far), (1, col_near)], y0, y1, rect=R.MakeLTRB(-300, y0, W + 300, y1 + 400))
    for i in range(40):
        u = hsh(i, seed); v = hsh(i, seed + 1) ** 1.3
        y = lerp(y0, y1, v); w = lerp(160, 700, v) * (0.6 + 0.8 * hsh(i, seed + 2)); h = w * lerp(0.08, 0.22, v)
        x = u * (W + 400) - 200
        col = blotch if hsh(i, seed + 3) > 0.35 else (120, 160, 80)
        c.drawOval(R.MakeXYWH(x - w / 2, y - h / 2, w, h), paint(col, ba * (0.5 + 0.5 * hsh(i, seed + 4)), blur=h * 0.4))
