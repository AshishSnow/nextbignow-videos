"""FreshNestHub — 'Your red lipstick might be made of bugs' (carmine / cochineal). Fully procedural: NESSA host + 3D cochineal + designed sets.
Usage: render.py OUT.mp4 [frame,frame,...]   (GUIDES=1 draws IG/Shorts safe-zone overlay on test frames)"""
import os, sys, json, math, subprocess
import numpy as np, cv2, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, "/home/claude/reel-kit/english/scripts")
from nessa import nessa, head, floor_shadow
from mites_assets import sphere

B = "/home/claude/reel-kit/english"
OUT = sys.argv[1]
ONLY = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else None
TL = json.load(open(f"{B}/work/timeline.json"))
EV, LN, END, LEAD = TL["events"], TL["lines"], TL["END"], TL["LEAD"]
SHOTS = TL["shots"]; SHOT = {s["id"]: s for s in SHOTS}
W, H, FPS = 1080, 1920, 30
N = int(round(END * FPS))
CX = 540          # TRUE screen centre for all text (user rule). Keep text <= MAXW wide so it stays clear of the right-side buttons.
MAXW = 840
E = EV
ANTON = "/home/claude/reel-kit/assets/fonts_plate/Anton-Regular.ttf"
IB = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
IXB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
ISB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
GUIDES = os.environ.get("GUIDES")
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)


# ---------------- basics ----------------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def eo(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def eio(x):
    x = clamp(x); return 3 * x * x - 2 * x * x * x


def eback(x, s=1.7):
    x = clamp(x); x -= 1; return 1 + x * x * ((s + 1) * x + s)


def popk(t, t0, d=0.32):
    return eback((t - t0) / d) if t >= t0 else 0.0


def appear(t, t0, d=0.25):
    return eo((t - t0) / d) if t >= t0 else 0.0


def lerp(a, b, u):
    return a + (b - a) * u


def C(c):
    return np.array(c[:3], np.float32) / 255.0


_GR = {}


def grad(c0, c1, cx=0.5, cy=0.42, k=1.0):
    key = (c0, c1, cx, cy, k)
    if key not in _GR:
        d = np.sqrt(((_xx / W - cx) * 1.0) ** 2 + ((_yy / H - cy) * H / W * 0.62) ** 2)
        d = np.clip(d / (0.95 * k), 0, 1)[..., None] ** 1.25
        _GR[key] = (C(c0) * (1 - d) + C(c1) * d).astype(np.float32)
    return _GR[key].copy()


def disc(f, cx, cy, r, col, op=1.0, glow=0.0, ring=None):
    if r <= 1:
        return
    pad = int(r * 0.6) + 8 if glow else 4
    x0, x1, y0, y1 = int(max(0, cx - r - pad)), int(min(W, cx + r + pad)), int(max(0, cy - r - pad)), int(min(H, cy + r + pad))
    if x1 <= x0 or y1 <= y0:
        return
    d = np.sqrt((_xx[y0:y1, x0:x1] - cx) ** 2 + (_yy[y0:y1, x0:x1] - cy) ** 2)
    if glow:
        g = np.exp(-np.clip(d - r, 0, None) / (r * 0.18)) * (d > r) * glow * op
        f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * (1 - g[..., None]) + C(col) * g[..., None]
    a = np.clip(r - d + 0.5, 0, 1) * op
    cc = C(col)
    # subtle top-light gradient for a 3D feel
    sh = 1.06 - 0.14 * np.clip((_yy[y0:y1, x0:x1] - (cy - r)) / (2 * r), 0, 1)
    f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * (1 - a[..., None]) + np.clip(cc * sh[..., None], 0, 1) * a[..., None]
    if ring:
        rc, rw = ring
        ra = np.clip(rw / 2 - np.abs(d - r + rw / 2) + 0.5, 0, 1) * op
        f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * (1 - ra[..., None]) + C(rc) * ra[..., None]


def to_np(im):
    a = np.asarray(im, np.float32) / 255.0
    return a[..., :3], a[..., 3]


def over(f, rgb, a, x, y, op=1.0):
    """composite rgb/alpha arrays with top-left at (x,y)"""
    h, w = a.shape
    x, y = int(round(x)), int(round(y))
    xa, ya, xb, yb = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if xb <= xa or yb <= ya:
        return
    aa = a[ya - y:yb - y, xa - x:xb - x][..., None] * op
    f[ya:yb, xa:xb] = f[ya:yb, xa:xb] * (1 - aa) + rgb[ya - y:yb - y, xa - x:xb - x] * aa


def put(f, im, cx, cy, op=1.0, sc=1.0, rot=0.0, anchor="c"):
    if op <= 0.003 or sc <= 0.01:
        return
    if abs(sc - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
    if abs(rot) > 0.05:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    rgb, a = to_np(im)
    if anchor == "c":
        over(f, rgb, a, cx - im.width / 2, cy - im.height / 2, op)
    elif anchor == "b":
        over(f, rgb, a, cx - im.width / 2, cy - im.height, op)


_TX = {}


def txt(text, fp, size, fill=(255, 255, 255), stroke=0, sfill=(10, 10, 14), shadow=0.55, track=0):
    key = (text, fp, size, fill, stroke, sfill, shadow, track)
    if key in _TX:
        return _TX[key]
    fnt = ImageFont.truetype(fp, size)
    bb = fnt.getbbox(text, stroke_width=stroke)
    w, h = bb[2] - bb[0] + 60, bb[3] - bb[1] + 60
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((30 - bb[0] + 4, 30 - bb[1] + 10), text, font=fnt, fill=(0, 0, 0, int(255 * shadow)), stroke_width=stroke,
                                stroke_fill=(0, 0, 0, int(255 * shadow)))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(im).text((30 - bb[0], 30 - bb[1]), text, font=fnt, fill=fill + (255,) if len(fill) == 3 else fill, stroke_width=stroke,
                            stroke_fill=sfill)
    _TX[key] = im
    return im


def big(text, size=200, fill=(255, 255, 255), stroke=9):
    return txt(text, ANTON, size, fill, stroke, (12, 12, 16), 0.6)


def small(text, size=56, fill=(255, 255, 255)):
    return txt(text, ISB, size, fill, 0, shadow=0.55)


def tier(f, t, t0, lo, hi, y, size=190, fill=(255, 255, 255), lo_size=54, gap=None, out=None):
    """editorial two-tier caption: small lowercase line + huge word"""
    if t < t0 or (out is not None and t > out + 0.2):
        return
    o = 1.0 if out is None else clamp(1 - (t - out) / 0.2)
    if lo:
        k = appear(t, t0, 0.22)
        sm_ = small(lo, lo_size)
        put(f, sm_, CX, y - (gap or size * 0.62) + 20 * (1 - k), op=k * o, sc=min(1.0, MAXW / max(1, sm_.width - 60)))
    s = popk(t, t0 + 0.06, 0.34)
    im = big(hi, size, fill)
    fit = min(1.0, MAXW / max(1, im.width - 60))
    put(f, im, CX, y, op=clamp(s * 3) * o, sc=(0.6 + 0.4 * s) * fit)


def pill(text, size=42, bg=(14, 18, 34), fg=(255, 255, 255), padx=28, pady=14, acc=None):
    key = ("pill", text, size, bg, fg, acc)
    if key in _TX:
        return _TX[key]
    fnt = ImageFont.truetype(IXB, size)
    bb = fnt.getbbox(text)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    dot = 26 if acc else 0
    w, h = tw + 2 * padx + dot, th + 2 * pady
    im = Image.new("RGBA", (w + 40, h + 50), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([20, 30, 20 + w, 30 + h], h // 2, fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 18, 20 + w, 18 + h], h // 2, fill=bg + (240,))
    d.rounded_rectangle([20, 18, 20 + w, 18 + h // 2], h // 2, fill=(255, 255, 255, 22))
    if acc:
        d.ellipse([20 + padx - 4, 18 + h / 2 - 9, 20 + padx + 14, 18 + h / 2 + 9], fill=acc + (255,))
    d.text((20 + padx + dot - bb[0], 18 + pady - bb[1]), text, font=fnt, fill=fg)
    _TX[key] = im
    return im


# ---------------- voice envelope -> mouth ----------------
_vo, _vsr = sf.read(f"{B}/work/vo.wav", dtype="float32")
_hop = _vsr // 100
_nv = len(_vo) // _hop
VDB = 20 * np.log10(np.sqrt((_vo[: _nv * _hop].reshape(_nv, _hop) ** 2).mean(1)) + 1e-9)
VDB = np.convolve(VDB, np.ones(4) / 4, "same")


def mouth(t):
    i = int((t - LEAD) * 100)
    if i < 0 or i >= len(VDB):
        return 0.0
    return clamp((VDB[i] + 42) / 20)


# ---------------- characters (cached) ----------------
_NC = {}


def char(pose="stand", expr="smile", t=0.0, scale=1.0, m=0.0, look=(0, 0), style="nessa", tilt=0.0):
    tq = round(t * 15) / 15
    mq = round(m * 4) / 4
    key = (pose, expr, tq, round(scale, 3), mq, look, style, tilt)
    if key not in _NC:
        if len(_NC) > 900:
            _NC.clear()
        _NC[key] = nessa(pose, expr, t=tq, scale=scale, mouth=mq, look=look, style=style, tilt=tilt)
    return _NC[key]


def put_char(f, x, feet_y, pose="stand", expr="smile", t=0.0, scale=1.0, m=0.0, look=(0, 0), style="nessa", op=1.0, shadow=True, sc=1.0,
             tilt=0.0, clip_y=None):
    im, (ax, ay) = char(pose, expr, t, scale, m, look, style, tilt)
    if shadow:
        sh = floor_shadow(int(170 * scale), int(26 * scale), 110)
        put(f, sh, x, feet_y, op=op)
    if abs(sc - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
        ax, ay = ax * sc, ay * sc
    rgb, a = to_np(im)
    if clip_y is not None:
        cut = int(clip_y - (feet_y - ay))
        if cut < a.shape[0]:
            a = a.copy(); a[max(0, cut):] = 0
    over(f, rgb, a, x - ax, feet_y - ay, op)


_HC = {}


def put_head(f, x, y, expr="smile", t=0.0, scale=1.0, m=0.0, look=(0, 0), tilt=0.0, style="nessa", op=1.0):
    key = (expr, round(t * 15) / 15, round(scale, 3), round(m * 4) / 4, look, round(tilt), style)
    if key not in _HC:
        if len(_HC) > 600:
            _HC.clear()
        _HC[key] = to_np(head(expr, key[1], scale, key[3], look, tilt, style))
    rgb, a = _HC[key]
    over(f, rgb, a, x - a.shape[1] / 2, y - a.shape[0] / 2, op)



def heart(size, col=(255, 70, 140)):
    key = ("heart", size, col)
    if key in _TX:
        return _TX[key]
    s = size * 3
    im = Image.new("RGBA", (s + 60, s + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = []
    for i in range(120):
        a = i / 120 * 2 * math.pi
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((30 + s / 2 + x * s / 34, 30 + s / 2 + y * s / 34))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(x + 6, y + 12) for x, y in pts], fill=(0, 0, 0, 110))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d.polygon(pts, fill=col + (255,))
    d.line(pts + [pts[0]], fill=(255, 255, 255, 255), width=int(s * 0.04))
    d.ellipse([30 + s * 0.22, 30 + s * 0.25, 30 + s * 0.38, 30 + s * 0.36], fill=(255, 255, 255, 170))
    im = im.resize((im.width // 3, im.height // 3), Image.LANCZOS)
    _TX[key] = im
    return im


def sparkles(f, t, seed, n=24, col=(255, 255, 255), area=(60, 250, 960, 1500), op=1.0, size=7):
    r = np.random.default_rng(seed)
    for i in range(n):
        x, y = r.uniform(area[0], area[2]), r.uniform(area[1], area[3])
        ph = r.uniform(0, 6.28); sp = r.uniform(1.5, 3.5)
        a = (0.5 + 0.5 * math.sin(t * sp + ph)) ** 3 * op
        if a < 0.05:
            continue
        s = size * r.uniform(0.6, 1.4)
        disc(f, x, y, s * 0.45, col, op=a)
        f[int(max(0, y - 0.6)):int(y + 1.6), int(max(0, x - s * 2)):int(min(W, x + s * 2))] += 0.35 * a
        f[int(max(0, y - s * 2)):int(min(H, y + s * 2)), int(max(0, x - 0.6)):int(x + 1.6)] += 0.35 * a


def guides(f):
    red = np.array([1.0, 0.1, 0.1], np.float32)
    for (x0, y0, x1, y1) in ((0, 0, W, 250), (0, H - 420, W, H), (W - 120, 0, W, H), (0, 0, 60, H)):
        f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * 0.6 + red * 0.4
    for cy in (1080, 1220, 1360, 1500):
        cv2.circle(f, (1010, cy), 40, (1, 1, 1), 3)
    return f


def zoom_at(f, z, px, py, tx=None, ty=None):
    """scale frame by z around (px,py) and move that point to (tx,ty)"""
    tx = px if tx is None else tx; ty = py if ty is None else ty
    if abs(z - 1) < 1e-3 and tx == px and ty == py:
        return f
    M = np.float32([[z, 0, tx - z * px], [0, z, ty - z * py]])
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

def arrow_to(f, x0, y0, x1, y1, op=1.0, col=(255, 255, 255), w=7):
    if op <= 0:
        return
    pts = []
    for i in range(21):
        u = i / 20 * op
        mx, my = (x0 + x1) / 2 + (y1 - y0) * 0.18, (y0 + y1) / 2 - (x1 - x0) * 0.18
        x = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1
        y = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1
        pts.append((x, y))
    p = np.array(pts, np.int32)
    cv2.polylines(f, [p + 3], False, (0, 0, 0), w + 3, cv2.LINE_AA)
    cv2.polylines(f, [p], False, C(col).tolist(), w, cv2.LINE_AA)
    if op > 0.9:
        a = math.atan2(pts[-1][1] - pts[-3][1], pts[-1][0] - pts[-3][0])
        for s in (-1, 1):
            q = (int(pts[-1][0] - 26 * math.cos(a + s * 0.5)), int(pts[-1][1] - 26 * math.sin(a + s * 0.5)))
            cv2.line(f, (int(pts[-1][0]), int(pts[-1][1])), q, C(col).tolist(), w, cv2.LINE_AA)



def lens(f, inner, cx, cy, r, ring=(255, 255, 255)):
    if r < 2:
        return f
    d = np.sqrt((_xx - cx) ** 2 + (_yy - cy) ** 2)
    m = np.clip(r - d + 0.5, 0, 1)[..., None]
    f = f * (1 - m) + inner * m
    rim = np.exp(-((d - r) / 9) ** 2)[..., None]
    f = f * (1 - rim * 0.95) + C(ring) * rim * 0.95
    gl = (np.exp(-((d - r * 0.82) / (r * 0.05)) ** 2) * np.clip(-(_xx - cx + _yy - cy) / (r * 1.2), 0, 1))[..., None] * 0.35
    return np.clip(f + gl, 0, 1)


# ---------------- characters with flip ----------------
def char(pose="stand", expr="smile", t=0.0, scale=1.0, m=0.0, look=(0, 0), style="nessa", tilt=0.0, flip=False):
    tq = round(t * 15) / 15
    mq = round(m * 4) / 4
    key = (pose, expr, tq, round(scale, 3), mq, look, style, tilt, flip)
    if key not in _NC:
        if len(_NC) > 900:
            _NC.clear()
        im, (ax, ay) = nessa(pose, expr, t=tq, scale=scale, mouth=mq, look=look, style=style, tilt=tilt)
        if flip:
            im = im.transpose(Image.FLIP_LEFT_RIGHT); ax = im.width - ax
        _NC[key] = (im, (ax, ay))
    return _NC[key]


def put_char(f, x, feet_y, pose="stand", expr="smile", t=0.0, scale=1.0, m=0.0, look=(0, 0), style="nessa", op=1.0, shadow=True, sc=1.0,
             tilt=0.0, flip=False):
    im, (ax, ay) = char(pose, expr, t, scale, m, look, style, tilt, flip)
    if shadow:
        put(f, floor_shadow(int(170 * scale), int(26 * scale), 110), x, feet_y, op=op)
    if abs(sc - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
        ax, ay = ax * sc, ay * sc
    rgb, a = to_np(im)
    over(f, rgb, a, x - ax, feet_y - ay, op)


# ================= assets =================
_AS = {}


def _noise(h, w, s, seed):
    r = np.random.default_rng(seed)
    n = r.standard_normal((h // s + 3, w // s + 3)).astype(np.float32)
    n = cv2.resize(n, (w + 3 * s, h + 3 * s), interpolation=cv2.INTER_CUBIC)[:h, :w]
    return n / (np.abs(n).max() + 1e-9)


def cochineal(L, wax=0.85, seed=0, phase=0, dark=0.0, eyes=False):
    """realistic-ish female cochineal scale insect seen from above, head up. L = body length px. returns PIL RGBA"""
    key = ("coch", int(L), round(wax, 2), seed, phase % 4, round(dark, 2), eyes)
    if key in _AS:
        return _AS[key]
    k = 3
    S_ = int(L * 1.5) * k
    c = S_ / 2
    im = Image.new("RGBA", (S_, S_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rx, ry = 0.34 * L * k, 0.5 * L * k
    # legs (under the body)
    lw = max(2, int(0.035 * L * k))
    for i, yy in enumerate((-0.25, 0.0, 0.25)):
        sw = math.sin(phase * math.pi / 2 + i * 1.3) * 0.18
        for s in (-1, 1):
            x0, y0 = c + s * rx * 0.75, c + yy * ry
            x1, y1 = c + s * rx * 1.32, c + (yy + 0.10 + sw * s) * ry
            x2, y2 = c + s * rx * 1.45, c + (yy + 0.32 + sw * s) * ry
            d.line([(x0, y0), (x1, y1), (x2, y2)], fill=(70, 22, 36, 255), width=lw, joint="curve")
    # antennae
    for s in (-1, 1):
        d.line([(c + s * rx * 0.25, c - ry * 0.88), (c + s * rx * 0.55, c - ry * 1.12), (c + s * rx * 0.62, c - ry * 1.22)], fill=(70, 22, 36, 255),
               width=max(2, lw - 1), joint="curve")
    base = np.asarray(im, np.float32) / 255.0
    rgb, al = base[..., :3].copy(), base[..., 3].copy()
    y, x = np.mgrid[0:S_, 0:S_].astype(np.float32)
    nx, ny = (x - c) / rx, (y - c) / ry
    dd = np.sqrt(nx ** 2 + ny ** 2)
    nz = np.sqrt(np.clip(1 - dd ** 2, 0, 1))
    Lv = np.array([-0.45, -0.6, 0.66]); Lv /= np.linalg.norm(Lv)
    diff = np.clip(nx * Lv[0] * 0.8 + ny * Lv[1] * 0.8 + nz * Lv[2], 0, 1)
    body = np.array([0.52, 0.10, 0.22], np.float32) * (1 - dark * 0.5)
    seg = 1 - 0.32 * np.exp(-(((ny * 5.2 + 0.5) % 1.0 - 0.5) / 0.09) ** 2) * (dd < 0.97)
    col = body * (0.45 + 0.75 * diff)[..., None] * seg[..., None]
    # white waxy powder: denser on the back, tufts along ridges
    n1 = _noise(S_, S_, max(2, int(L * k / 22)), seed) * 0.5 + _noise(S_, S_, max(2, int(L * k / 60)), seed + 7) * 0.5
    wm = np.clip((n1 + 0.15 + 0.55 * nz - 0.25) * 2.2, 0, 1) * wax * (0.85 + 0.15 * seg)
    waxc = np.array([0.97, 0.95, 0.98], np.float32) * (0.62 + 0.45 * diff)[..., None]
    col = col * (1 - wm[..., None]) + waxc * wm[..., None]
    sp = np.exp(-((nx + 0.3) ** 2 + (ny + 0.4) ** 2) / 0.03) * 0.35 * (1 - wm * 0.6)
    col = np.clip(col + sp[..., None], 0, 1)
    ba = np.clip((1 - dd) * ry * 0.5 + 0.5, 0, 1)
    rgb = rgb * (1 - ba[..., None]) + col * ba[..., None]
    al = np.maximum(al, ba)
    out = Image.fromarray((np.dstack([rgb, al]) * 255).astype(np.uint8), "RGBA")
    if eyes:
        dr = ImageDraw.Draw(out)
        for s in (-1, 1):
            ex, ey, er = c + s * rx * 0.33, c - ry * 0.72, rx * 0.16
            dr.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(255, 255, 255, 255), outline=(14, 14, 18, 255), width=lw)
            dr.ellipse([ex - er * 0.45, ey - er * 0.3, ex + er * 0.45, ey + er * 0.6], fill=(14, 14, 18, 255))
    out = out.resize((S_ // k, S_ // k), Image.LANCZOS)
    _AS[key] = out
    return out


def bug(f, x, y, L, ang=0.0, t=0.0, op=1.0, wax=0.85, seed=0, walk=0.0, dark=0.0, eyes=False, shadow=True, sc=1.0):
    """ang in degrees (0 = head up). walk = leg cycles per second"""
    if op <= 0.01 or L * sc < 4:
        return
    ph = int(t * walk * 4) if walk else 0
    im = cochineal(max(8, int(L)), wax, seed, ph, dark, eyes)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        r = L * 0.36
        ImageDraw.Draw(sh).ellipse([im.width / 2 - r, im.height / 2 - L * 0.5, im.width / 2 + r, im.height / 2 + L * 0.5], fill=(0, 0, 0, 120))
        sh = sh.filter(ImageFilter.GaussianBlur(max(2, L * 0.06)))
        put(f, sh, x + L * 0.05 * sc, y + L * 0.08 * sc, op=op * 0.8, sc=sc, rot=ang)
    put(f, im, x, y, op=op, sc=sc, rot=ang)


def _cyl(w, h, col, shine=0.9, dark=0.28):
    x = np.linspace(-1, 1, w, dtype=np.float32)
    n = np.sqrt(np.clip(1 - x ** 2, 0, 1))
    sh = dark + (1 - dark) * (0.25 + 0.85 * n) * (1 - 0.25 * x)
    sp = np.exp(-((x + 0.45) / 0.10) ** 2) * shine + np.exp(-((x - 0.72) / 0.06) ** 2) * shine * 0.35
    row = np.clip(C(col)[None] * sh[:, None] + sp[:, None], 0, 1)
    return np.broadcast_to(row[None], (h, w, 3)).copy()


def lipstick(ext, scale=1.0):
    """gold case + red bullet, anchor bottom-centre. ext = bullet height (px at scale 1)"""
    ext = int(round(ext / 4) * 4)
    key = ("lip", ext, round(scale, 2))
    if key in _AS:
        return _AS[key]
    k = 2 * scale
    cw, ch = int(210 * k), int(330 * k)
    sw, sh_ = int(176 * k), int((50 + 0.4 * ext) * k)
    bw, bh = int(150 * k), max(2, int(ext * k))
    slant = int(70 * k)
    Wd, Hd = int(260 * k), ch + sh_ + bh + int(30 * k)
    rgb = np.zeros((Hd, Wd, 3), np.float32); al = np.zeros((Hd, Wd), np.float32)
    cx = Wd // 2
    # bullet
    y_b1 = Hd - ch - sh_ + int(10 * k); y_b0 = y_b1 - bh
    bul = _cyl(bw, bh, (214, 10, 52), 0.75, 0.22)
    xs = np.arange(bw)[None, :]; ys = np.arange(bh)[:, None]
    top = slant * (1 - xs / bw)
    m = (ys >= np.minimum(top, bh - 2)).astype(np.float32)
    rgb[y_b0:y_b1, cx - bw // 2:cx - bw // 2 + bw] = bul; al[y_b0:y_b1, cx - bw // 2:cx - bw // 2 + bw] = m
    # glossy slanted face
    face = (np.abs(ys - top) < 7 * k) & (ys < bh - 2)
    rgb[y_b0:y_b1, cx - bw // 2:cx - bw // 2 + bw][face] = np.clip(rgb[y_b0:y_b1, cx - bw // 2:cx - bw // 2 + bw][face] + 0.35, 0, 1)
    # sleeve
    y_s0 = Hd - ch - sh_
    rgb[y_s0:y_s0 + sh_, cx - sw // 2:cx - sw // 2 + sw] = _cyl(sw, sh_, (236, 190, 70), 0.9, 0.3)
    al[y_s0:y_s0 + sh_, cx - sw // 2:cx - sw // 2 + sw] = 1
    # case
    y_c0 = Hd - ch
    case = _cyl(cw, ch, (250, 196, 60), 1.0, 0.3)
    case[: int(14 * k)] *= 1.15; case[int(14 * k):int(20 * k)] *= 0.55
    case[int(ch * 0.55):int(ch * 0.55) + int(8 * k)] *= 0.6
    rgb[y_c0:, cx - cw // 2:cx - cw // 2 + cw] = np.clip(case, 0, 1); al[y_c0:, cx - cw // 2:cx - cw // 2 + cw] = 1
    # round the case bottom corners
    rr = int(18 * k)
    for (xx, yy) in ((cx - cw // 2, Hd - rr), (cx + cw // 2 - rr, Hd - rr)):
        sub = al[yy:yy + rr, xx:xx + rr]
        gy, gx = np.mgrid[0:rr, 0:rr]
        ox = 0 if xx < cx else rr
        dd = np.sqrt((gx - (rr - 1 if ox == 0 else 0)) ** 2 + gy ** 2)
        sub[dd > rr] = 0
    im = Image.fromarray((np.dstack([rgb, al]) * 255).astype(np.uint8), "RGBA")
    im = im.filter(ImageFilter.SMOOTH)
    im = im.resize((max(1, Wd // 2), max(1, Hd // 2)), Image.LANCZOS)
    _AS[key] = im
    return im


def lip_top(x, bottom, ext, scale=1.0):
    """screen point at the tip of the bullet"""
    return x + 35 * scale, bottom - (330 + 50 + 0.4 * ext + ext - 10 - 8) * scale


def put_lip(f, x, bottom, ext, scale=1.0, op=1.0, rot=0.0):
    im = lipstick(ext, scale)
    sh = floor_shadow(int(170 * scale), int(26 * scale), 120)
    put(f, sh, x, bottom, op=op)
    put(f, im, x, bottom, op=op, anchor="b") if abs(rot) < 0.05 else put(f, im, x, bottom - im.height / 2, op=op, rot=rot)


def bgset(c0, c1, circ=(255, 206, 0), cx=540, cy=900, r=330, cyg=0.45, t=0.0, seed=1, spark=18):
    f = grad(c0, c1, cy=cyg)
    if circ:
        disc(f, cx, cy, r, circ, glow=0.45)
    if spark:
        sparkles(f, t, seed, n=spark, op=0.8)
    return f


def pad_img(w, h, seed=0, colony=0.0):
    key = ("pad", w, h, seed, round(colony, 2))
    if key in _AS:
        return _AS[key]
    k = 2
    W2, H2 = w * k, h * k
    y, x = np.mgrid[0:H2, 0:W2].astype(np.float32)
    nx, ny = (x - W2 / 2) / (W2 / 2), (y - H2 / 2) / (H2 / 2)
    dd = np.sqrt(nx ** 2 + ny ** 2)
    nz = np.sqrt(np.clip(1 - dd ** 2, 0, 1))
    diff = np.clip(-0.4 * nx - 0.5 * ny + 0.75 * nz, 0, 1)
    nse = _noise(H2, W2, 18, seed) * 0.06
    col = np.array([0.30, 0.72, 0.26], np.float32) * (0.5 + 0.65 * diff + nse)[..., None]
    rgb = np.clip(col + (np.exp(-((nx + 0.35) ** 2 + (ny + 0.4) ** 2) / 0.05) * 0.18)[..., None], 0, 1)
    al = np.clip((1 - dd) * W2 * 0.25, 0, 1)
    im = Image.fromarray((np.dstack([rgb, al]) * 255).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(im)
    r = np.random.default_rng(seed)
    # areoles + spines
    for i in range(int(w * h / 2600)):
        a_ = r.uniform(0, 6.28); q = math.sqrt(r.uniform(0, 0.8))
        px, py = W2 / 2 + math.cos(a_) * q * W2 / 2 * 0.9, H2 / 2 + math.sin(a_) * q * H2 / 2 * 0.9
        d.ellipse([px - 5 * k, py - 5 * k, px + 5 * k, py + 5 * k], fill=(232, 220, 150, 255))
        for s in range(3):
            aa = r.uniform(0, 6.28)
            d.line([(px, py), (px + math.cos(aa) * 16 * k, py + math.sin(aa) * 16 * k)], fill=(250, 245, 215, 255), width=2 * k)
    # white waxy colonies of cochineal
    if colony > 0:
        fl = Image.new("RGBA", im.size, (0, 0, 0, 0)); fd = ImageDraw.Draw(fl)
        for i in range(int(colony * w * h / 1800)):
            a_ = r.uniform(0, 6.28); q = math.sqrt(r.uniform(0, 0.7))
            px, py = W2 / 2 + math.cos(a_) * q * W2 / 2, H2 / 2 + math.sin(a_) * q * H2 / 2
            for j in range(5):
                rr = r.uniform(5, 13) * k
                ox, oy = r.normal(0, 9 * k), r.normal(0, 7 * k)
                fd.ellipse([px + ox - rr, py + oy - rr, px + ox + rr, py + oy + rr], fill=(250, 248, 252, 235))
        fl = fl.filter(ImageFilter.GaussianBlur(2 * k))
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.paste((60, 20, 40, 110), (0, 0), fl.split()[3])
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4 * k)), (3 * k, 4 * k))
        im.alpha_composite(fl)
        m = Image.new("L", im.size, 0); ImageDraw.Draw(m).ellipse([2, 2, W2 - 2, H2 - 2], fill=255)
        im.putalpha(Image.fromarray(np.minimum(np.asarray(im.split()[3]), np.asarray(m))))
    im = im.resize((w, h), Image.LANCZOS)
    _AS[key] = im
    return im


def fruit(r):
    key = ("fruit", r)
    if key in _AS:
        return _AS[key]
    spr = sphere(r, (0.78, 0.12, 0.42), rim=0.5, spec=0.5)
    rgb, a = spr
    im = Image.fromarray((np.dstack([rgb, a]) * 255).astype(np.uint8), "RGBA").resize((int(r * 2), int(r * 2.5)), Image.LANCZOS)
    _AS[key] = im
    return im


def cactus(f, cx, base, t, colony=0.6, s=1.0):
    """prickly pear: 3 pads + fruits. returns list of (x,y) pad centres"""
    pads = [((0, -260), 360, 470, 0, 4), ((-170, -610), 260, 330, -24, 5), ((165, -640), 250, 320, 22, 6), ((-10, -880), 190, 240, 4, 7)]
    out = []
    for (dx, dy), w, h, rot, sd in pads:
        im = pad_img(int(w * s), int(h * s), sd, colony)
        put(f, im, cx + dx * s, base + dy * s, rot=rot)
        out.append((cx + dx * s, base + dy * s))
    for (dx, dy) in ((-250, -760), (-120, -780), (100, -800), (260, -790), (-60, -1000), (50, -1005)):
        put(f, fruit(int(24 * s)), cx + dx * s, base + dy * s)
    return out


def mortar_img():
    if "mortar" in _AS:
        return _AS["mortar"]
    w, h = 560, 330
    k = 2
    y, x = np.mgrid[0:h * k, 0:w * k].astype(np.float32)
    nx = (x - w * k / 2) / (w * k / 2)
    ny = y / (h * k)
    inside = (nx ** 2 + ((ny) / 1.0) ** 2 * 0 <= 1)
    prof = np.sqrt(np.clip(1 - nx ** 2, 0, 1))
    m = (ny <= prof * 0.98 + 0.0).astype(np.float32) * (np.abs(nx) <= 1)
    m *= (y >= h * k * 0.0)
    nse = _noise(h * k, w * k, 10, 3) * 0.08
    sh = 0.45 + 0.6 * np.clip(1 - np.abs(nx + 0.3), 0, 1) * (1 - 0.35 * ny)
    rgb = np.array([0.62, 0.60, 0.66], np.float32) * (sh + nse)[..., None]
    im = Image.fromarray((np.dstack([np.clip(rgb, 0, 1), m]) * 255).astype(np.uint8), "RGBA")
    # rim ellipse (opening)
    top = Image.new("RGBA", (w * k, h * k + 80 * k), (0, 0, 0, 0))
    td = ImageDraw.Draw(top)
    td.ellipse([0, 0, w * k, 80 * k], fill=(120, 116, 128, 255))
    td.ellipse([18 * k, 10 * k, w * k - 18 * k, 70 * k], fill=(54, 50, 62, 255))
    top.alpha_composite(im, (0, 40 * k))
    td = ImageDraw.Draw(top)
    td.ellipse([0, 0, w * k, 80 * k], outline=(200, 196, 210, 255), width=4 * k)
    td.ellipse([18 * k, 10 * k, w * k - 18 * k, 70 * k], fill=(54, 50, 62, 255))
    out = top.resize((w, h + 80), Image.LANCZOS)
    _AS["mortar"] = out
    return out


def pestle_img():
    if "pestle" in _AS:
        return _AS["pestle"]
    w, h = 110, 470
    rgb = _cyl(w, h, (170, 166, 180), 0.6, 0.3)
    y = np.arange(h)[:, None]; x = np.linspace(-1, 1, w)[None]
    width = 0.55 + 0.45 * np.clip((y - h * 0.55) / (h * 0.3), 0, 1)
    m = (np.abs(x) <= width).astype(np.float32)
    bot = h - 50
    m[bot:] *= (np.sqrt(np.clip(1 - ((y[bot:] - bot) / 50.0) ** 2, 0, 1)) >= np.abs(x)).astype(np.float32)
    im = Image.fromarray((np.dstack([rgb, m]) * 255).astype(np.uint8), "RGBA").filter(ImageFilter.SMOOTH)
    _AS["pestle"] = im
    return im


def pile_img(n, seed=4, w=360):
    key = ("pile", n, seed, w)
    if key in _AS:
        return _AS[key]
    h = int(w * 0.62)
    im = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    r = np.random.default_rng(seed)
    sp = [cochineal(26, r.uniform(0.6, 0.95), i % 5) for i in range(5)]
    for i in range(n):
        u = (i + 0.5) / n
        rad = w / 2 * math.sqrt(r.uniform(0, 1))
        a_ = r.uniform(math.pi, 2 * math.pi)
        x = (w + 60) / 2 + math.cos(a_) * rad
        ymax = h + 30
        hh = h * (1 - (abs(x - (w + 60) / 2) / (w / 2)) ** 2) * min(1, 0.25 + u)
        y = ymax - r.uniform(0, max(1, hh))
        b = sp[i % 5].rotate(r.uniform(0, 360), expand=True)
        im.alpha_composite(b, (int(x - b.width / 2), int(min(ymax, y) - b.height / 2)))
    _AS[key] = im
    return im


def jar_img():
    if "jar" in _AS:
        return _AS["jar"]
    w, h = 230, 290
    k = 2
    im = Image.new("RGBA", ((w + 40) * k, (h + 80) * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([20 * k, 50 * k, (20 + w) * k, (50 + h) * k], 40 * k, fill=(220, 240, 255, 120), outline=(255, 255, 255, 230), width=5 * k)
    d.rounded_rectangle([30 * k, 110 * k, (10 + w) * k, (40 + h) * k], 32 * k, fill=(206, 0, 48, 255))
    d.ellipse([30 * k, 96 * k, (10 + w) * k, 130 * k], fill=(240, 40, 80, 255))
    d.rounded_rectangle([44 * k, 120 * k, 70 * k, (20 + h) * k], 12 * k, fill=(255, 255, 255, 90))
    d.rounded_rectangle([12 * k, 18 * k, (28 + w) * k, 62 * k], 14 * k, fill=(250, 196, 60, 255), outline=(150, 100, 20, 255), width=4 * k)
    d.rounded_rectangle([22 * k, 24 * k, (18 + w) * k, 34 * k], 6 * k, fill=(255, 236, 160, 255))
    im = im.resize((w + 40, h + 80), Image.LANCZOS)
    _AS["jar"] = im
    return im


def food(kind):
    key = ("food", kind)
    if key in _AS:
        return _AS[key]
    k = 3
    S_ = 240
    im = Image.new("RGBA", (S_ * k, S_ * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    O = (20, 14, 22, 255)
    if kind == "yogurt":
        d.polygon([(40 * k, 80 * k), (200 * k, 80 * k), (180 * k, 225 * k), (60 * k, 225 * k)], fill=(255, 255, 255, 255), outline=O)
        d.line([(40 * k, 80 * k), (200 * k, 80 * k), (180 * k, 225 * k), (60 * k, 225 * k), (40 * k, 80 * k)], fill=O, width=5 * k)
        d.rectangle([55 * k, 130 * k, 186 * k, 175 * k], fill=(255, 110, 160, 255))
        d.ellipse([34 * k, 60 * k, 206 * k, 102 * k], fill=(255, 150, 190, 255), outline=O, width=5 * k)
        d.ellipse([60 * k, 68 * k, 150 * k, 86 * k], fill=(255, 205, 225, 255))
        d.rounded_rectangle([140 * k, 10 * k, 158 * k, 84 * k], 8 * k, fill=(200, 210, 230, 255), outline=O, width=4 * k)
        d.line([(66 * k, 100 * k), (66 * k, 215 * k)], fill=(255, 255, 255, 160), width=8 * k)
    elif kind == "candy":
        d.polygon([(20 * k, 80 * k), (75 * k, 120 * k), (20 * k, 160 * k)], fill=(255, 90, 140, 255), outline=O)
        d.polygon([(220 * k, 80 * k), (165 * k, 120 * k), (220 * k, 160 * k)], fill=(255, 90, 140, 255), outline=O)
        for pts in (((20, 80), (75, 120), (20, 160)), ((220, 80), (165, 120), (220, 160))):
            d.line([(x * k, y * k) for x, y in pts] + [(pts[0][0] * k, pts[0][1] * k)], fill=O, width=5 * k)
        d.ellipse([60 * k, 65 * k, 180 * k, 175 * k], fill=(232, 20, 60, 255), outline=O, width=5 * k)
        for i in range(4):
            d.arc([70 * k, 75 * k, 170 * k, 165 * k], 200 + i * 90, 240 + i * 90, fill=(255, 255, 255, 255), width=10 * k)
        d.ellipse([85 * k, 85 * k, 115 * k, 105 * k], fill=(255, 255, 255, 200))
    else:  # ice cream
        d.polygon([(70 * k, 120 * k), (170 * k, 120 * k), (120 * k, 232 * k)], fill=(232, 168, 80, 255))
        for i in range(-4, 6):
            d.line([((70 + i * 22) * k, 120 * k), ((120 + i * 6) * k, 232 * k)], fill=(180, 110, 40, 255), width=3 * k)
            d.line([((170 - i * 22) * k, 120 * k), ((120 - i * 6) * k, 232 * k)], fill=(180, 110, 40, 255), width=3 * k)
        d.line([(70 * k, 120 * k), (120 * k, 232 * k), (170 * k, 120 * k)], fill=O, width=5 * k)
        d.ellipse([50 * k, 40 * k, 190 * k, 150 * k], fill=(255, 140, 185, 255), outline=O, width=5 * k)
        d.ellipse([58 * k, 108 * k, 182 * k, 140 * k], fill=(255, 140, 185, 255))
        d.ellipse([80 * k, 58 * k, 120 * k, 82 * k], fill=(255, 210, 230, 255))
        d.ellipse([108 * k, 18 * k, 136 * k, 46 * k], fill=(220, 0, 40, 255), outline=O, width=4 * k)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 90), (0, 0), im.split()[3])
    base = Image.new("RGBA", im.size, (0, 0, 0, 0))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8 * k)), (6 * k, 10 * k)); base.alpha_composite(im)
    out = base.resize((S_, S_), Image.LANCZOS)
    _AS[key] = out
    return out


def warn_sign(s=220):
    key = ("warn", s)
    if key in _AS:
        return _AS[key]
    k = 3
    im = Image.new("RGBA", ((s + 40) * k, (s + 40) * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [((s / 2 + 20) * k, 20 * k), ((s + 20) * k, (s * 0.88 + 20) * k), (20 * k, (s * 0.88 + 20) * k)]
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(x + 8 * k, y + 14 * k) for x, y in pts], fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8 * k)))
    d.polygon(pts, fill=(255, 210, 0, 255))
    d.line(pts + [pts[0]], fill=(20, 14, 20, 255), width=12 * k, joint="curve")
    fnt = ImageFont.truetype(ANTON, int(s * 0.55) * k)
    bb = fnt.getbbox("!")
    d.text(((s / 2 + 20) * k - (bb[0] + bb[2]) / 2, (s * 0.58 + 20) * k - (bb[1] + bb[3]) / 2), "!", font=fnt, fill=(20, 14, 20, 255))
    im = im.resize((s + 40, s + 40), Image.LANCZOS)
    _AS[key] = im
    return im


def label_card(hl):
    key = ("label", round(hl, 2))
    if key in _AS:
        return _AS[key]
    k = 2
    w, h = 640, 520
    im = Image.new("RGBA", ((w + 60) * k, (h + 70) * k), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([36 * k, 46 * k, (36 + w) * k, (46 + h) * k], 30 * k, fill=(0, 0, 0, 130))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14 * k)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([30 * k, 30 * k, (30 + w) * k, (30 + h) * k], 30 * k, fill=(255, 255, 255, 255))
    d.rounded_rectangle([30 * k, 30 * k, (30 + w) * k, 120 * k], 30 * k, fill=(30, 36, 60, 255))
    d.rectangle([30 * k, 90 * k, (30 + w) * k, 120 * k], fill=(30, 36, 60, 255))
    f1 = ImageFont.truetype(IB, 44 * k)
    d.text((70 * k, 50 * k), "INGREDIENTS", font=f1, fill=(255, 255, 255, 255))
    r = np.random.default_rng(2)
    y = 160
    rows = []
    for i in range(7):
        x = 70
        while x < w - 40:
            ln = int(r.uniform(60, 170))
            ln = min(ln, w - 10 - x)
            if ln > 30:
                rows.append((x, y, ln))
            x += ln + 22
        y += 52
    for (x, y_, ln) in rows:
        d.rounded_rectangle([x * k, y_ * k, (x + ln) * k, (y_ + 22) * k], 11 * k, fill=(200, 206, 220, 255))
    # the highlighted word on row 4
    f2 = ImageFont.truetype(IB, 40 * k)
    wx, wy = 200, 160 + 3 * 52 - 9
    tb = f2.getbbox("CARMINE")
    d.rectangle([(wx - 14) * k, (wy - 6) * k, (wx + 14) * k + tb[2], (wy + 50) * k], fill=(255, 255, 255, 255))
    if hl > 0:
        d.rounded_rectangle([(wx - 14) * k, (wy - 6) * k, (wx - 14) * k + int((tb[2] + 28 * k) * hl), (wy + 50) * k], 10 * k, fill=(255, 220, 0, 255))
    d.text((wx * k, wy * k), "CARMINE", font=f2, fill=(200, 0, 50, 255))
    im = im.resize((w + 60, h + 70), Image.LANCZOS)
    _AS[key] = im
    return im


def tip_card(done):
    key = ("tip", done)
    if key in _AS:
        return _AS[key]
    k = 2
    w, h = 840, 230
    im = Image.new("RGBA", ((w + 80) * k, (h + 90) * k), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([46 * k, 60 * k, (46 + w) * k, (60 + h) * k], 34 * k, fill=(0, 0, 0, 140))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14 * k)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40 * k, 40 * k, (40 + w) * k, (40 + h) * k], 34 * k, fill=(255, 255, 255, 255))
    d.rounded_rectangle([40 * k, 40 * k, (40 + w) * k, (40 + h * 0.45) * k], 34 * k, fill=(246, 250, 255, 255))
    d.rounded_rectangle([40 * k, 40 * k, 64 * k, (40 + h) * k], 12 * k, fill=(0, 178, 114, 255))
    bx, by = 104, 40 + h / 2
    d.rounded_rectangle([(bx - 38) * k, (by - 38) * k, (bx + 38) * k, (by + 38) * k], 14 * k, fill=(0, 178, 114, 255) if done else (255, 255, 255, 255),
                        outline=(0, 140, 90, 255), width=6 * k)
    if done:
        d.line([((bx - 20) * k, by * k), ((bx - 4) * k, (by + 18) * k), ((bx + 24) * k, (by - 20) * k)], fill=(255, 255, 255, 255), width=10 * k,
               joint="curve")
    f1 = ImageFont.truetype(IB, 54 * k); f2 = ImageFont.truetype(ISB, 34 * k)
    d.text((168 * k, (40 + 36) * k), "Check the label for", font=f1, fill=(16, 20, 34, 255))
    d.text((168 * k, (40 + 122) * k), "carmine, cochineal extract, E120", font=f2, fill=(200, 0, 50, 255))
    im = im.resize((im.width // k, im.height // k), Image.LANCZOS)
    _AS[key] = im
    return im


def powder_burst(f, t, t0, cx, cy, n=60, seed=5, spread=1.0):
    if t < t0:
        return
    q = t - t0
    r = np.random.default_rng(seed)
    for i in range(n):
        a_ = r.uniform(-math.pi * 0.95, -math.pi * 0.05)
        sp = r.uniform(300, 1100) * spread
        x = cx + math.cos(a_) * sp * q
        y = cy + math.sin(a_) * sp * q + 900 * q * q
        op = clamp(1 - q / 0.9)
        if op <= 0:
            continue
        col = (230, 10, 60) if i % 3 else (255, 70, 110)
        disc(f, x, y, r.uniform(5, 15) * (1 + q), col, op=op)


# ================= shots =================
PINK0, PINK1 = (255, 70, 165), (112, 10, 124)


def shot_H1(t, n):
    f = bgset(PINK0, PINK1, (255, 206, 0), 610, 900, 340, t=t, seed=3, spark=24)
    ext = 30 + 270 * eo((t - 0.05) / 0.9)
    lx, lb = 610, 1340
    put_lip(f, lx, lb, ext, 1.0)
    tx, ty = lip_top(lx, lb, ext)
    tb = E["t_bugs0"] - 0.06
    if t > E["t_made"] - 0.2:
        specs = ((-30, 20, -20, 70), (40, 100, 15, 74), (-35, 190, 160, 66), (45, 270, 200, 70), (-45, 350, -170, 62), (30, 430, 30, 64))
        for j, (dx, dy, a_, L) in enumerate(specs):
            t0 = E["t_made"] - 0.2 + j * 0.09
            q = popk(t, t0, 0.3)
            if q > 0.01:
                bug(f, tx - 35 + dx, ty + dy + 8 * math.sin(t * 5 + j), L, a_ + 10 * math.sin(t * 3 + j), t, sc=q, walk=2, seed=j, eyes=False)
    shock = t > tb
    put_char(f, 235, 1490, "shock" if shock else "point", "gross" if shock else "talk", t, 0.88, m=mouth(t), look=(1, -1))
    tier(f, t, 0.05, "do you know what's in your", "RED LIPSTICK?", 450, size=150, out=tb - 0.2)
    tier(f, t, tb, "it might be made of", "BUGS!", 450, size=250, fill=(255, 226, 40))
    return f


def shot_NM(t, n):
    s = SHOT["NM"]["start"]
    f = bgset((40, 110, 255), (10, 16, 80), (255, 206, 0), 560, 1030, 330, t=t, seed=21)
    tier(f, t, E["t_carmine"] - 0.12, "it's called", "CARMINE", 520, size=240, fill=(255, 60, 100), gap=175)
    ti = E["t_carmine"] + 0.3
    if t > ti:
        k = eo((t - ti) / 0.8)
        bug(f, lerp(1250, 590, k), 1040, 330, -90 + 70 * k + 4 * math.sin(t * 6), t, walk=2.5 if k < 0.98 else 0.6, seed=2, eyes=False)
    if t > E["t_cochineal"] - 0.05:
        put(f, pill("cochineal insect", 46, acc=(255, 206, 0)), 590, 1400, op=appear(t, E["t_cochineal"] - 0.05),
            sc=0.85 + 0.15 * popk(t, E["t_cochineal"] - 0.05))
    put_char(f, 190, 1490, "magnify", "wow" if t > ti + 0.3 else "smile", t, 0.62, m=mouth(t))
    return f


def shot_CA(t, n):
    s, e = SHOT["CA"]["start"], SHOT["CA"]["end"]
    f = grad((255, 170, 60), (255, 70, 120), cx=0.5, cy=0.2)
    disc(f, 830, 470, 120, (255, 236, 90), glow=0.7)
    # dunes
    cv2.ellipse(f, (300, 1720), (900, 420), 0, 0, 360, (0.96, 0.62, 0.36), -1, cv2.LINE_AA)
    cv2.ellipse(f, (860, 1760), (700, 400), 0, 0, 360, (0.99, 0.76, 0.44), -1, cv2.LINE_AA)
    sparkles(f, t, 33, n=10, op=0.6, area=(60, 260, 1000, 900))
    k = popk(t, s + 0.02, 0.4)
    sc = 0.92 + 0.08 * k
    pads = cactus(f, 600, 1440, t, colony=0.55, s=sc)
    # bugs walking on the pads
    for j, (px, py) in enumerate(pads[:3]):
        for i in range(2):
            a_ = t * 0.5 + i * 3 + j
            bug(f, px + 60 * math.cos(a_) - 20, py + 70 * math.sin(a_ * 0.8), 34, math.degrees(a_) % 360, t, walk=2, seed=i + j, shadow=False)
    if t > E["t_mostly"] - 0.1:
        put(f, pill("mostly in PERU", 50, bg=(150, 30, 70), acc=(255, 230, 90)), CX, 330, op=appear(t, E["t_mostly"] - 0.1),
            sc=0.85 + 0.15 * popk(t, E["t_mostly"] - 0.1))
    put_char(f, 190, 1500, "magnify", "wow", t, 0.74, m=mouth(t))
    z = 1.0 + 0.06 * eio((t - s) / (e - s))
    return zoom_at(f, z, 600, 1000)


def shot_CR(t, n):
    s, e = SHOT["CR"]["start"], SHOT["CR"]["end"]
    f = grad((120, 50, 200), (24, 6, 60), cy=0.45)
    disc(f, 560, 920, 360, (255, 120, 200), op=0.35, glow=0.6)
    sparkles(f, t, 51, n=20, op=0.6)
    td = E["t_dried"] - 0.12
    dry = eio((t - td) / 0.5) if t > td else 0.0
    put(f, pad_img(620, 760, 9, 0.25), 600, 960, rot=-6)
    specs = ((470, 780, 20), (650, 760, -30), (560, 960, 10), (720, 1060, 160), (450, 1110, -150))
    for j, (x, y, a_) in enumerate(specs):
        L = 120 * (1 - 0.18 * dry)
        bug(f, x, y, L, a_ + 6 * math.sin(t * 2 + j) * (1 - dry), t, walk=0.8 * (1 - dry), seed=j + 10, dark=0.9 * dry, wax=0.85 - 0.4 * dry)
    if t > E["t_females"] - 0.1:
        k = popk(t, E["t_females"] - 0.1, 0.35)
        for j, (x, y, a_) in enumerate(specs[:3]):
            cv2.circle(f, (x, y), int(95 * min(1, k)), (1.0, 0.45, 0.8), 6, cv2.LINE_AA)
        put(f, pill("females only", 46, bg=(160, 20, 110), acc=(255, 160, 220)), CX, 420, op=clamp(k * 3) * clamp(1 - dry * 2.5), sc=0.85 + 0.15 * k)
    if dry > 0:
        # warm drying light + heat shimmer
        f = f * (1 - 0.25 * dry) + C((255, 150, 40)) * 0.25 * dry
        disc(f, 840, 400, 90 * dry, (255, 220, 60), glow=0.8)
        put(f, pill("dried", 46, bg=(170, 80, 0), acc=(255, 220, 60)), CX, 420, op=clamp(dry * 2.5 - 1.2))
    put_char(f, 175, 1500, "whisper", "whisper", t, 0.66, m=mouth(t))
    z = 1.0 + 0.10 * eio((t - s) / (e - s))
    return zoom_at(f, z, 590, 950)


def shot_CS(t, n):
    s = SHOT["CS"]["start"]
    tc = E["t_crushed"] - 0.05
    f = bgset((255, 70, 90), (120, 0, 40), (255, 206, 0), 540, 1000, 360, t=t, seed=61)
    mo = mortar_img()
    mx, my = 560, 1180
    # contents
    hit_ = t > tc
    put(f, mo, mx, my)
    if not hit_:
        r = np.random.default_rng(3)
        for i in range(14):
            bug(f, mx + r.uniform(-170, 170), my - 150 + r.uniform(-14, 14), 46, r.uniform(0, 360), t, dark=0.9, wax=0.45, seed=i % 5, shadow=False)
    else:
        q = eo((t - tc) / 0.3)
        cv2.ellipse(f, (mx, my - 152), (int(220 * q + 30), int(28 * q + 6)), 0, 0, 360, (0.86, 0.02, 0.2), -1, cv2.LINE_AA)
        cv2.ellipse(f, (mx - 40, my - 160), (int(90 * q + 10), int(10 * q + 2)), 0, 0, 360, (1.0, 0.3, 0.45), -1, cv2.LINE_AA)
    # pestle: raised, slams at tc
    if t < tc:
        u = eio((t - s) / max(0.1, tc - s))
        py = lerp(560, 640, u) - 60 * math.sin(math.pi * clamp((t - s) / max(0.1, tc - s - 0.12))) ** 2 * 0
        ang = -18
        py = lerp(560, 760, eio(clamp((t - (tc - 0.18)) / 0.18)))
    else:
        py = 760 + 8 * math.sin((t - tc) * 30) * math.exp(-(t - tc) * 6)
        ang = -18
    put(f, pestle_img(), mx + 90, py, rot=ang)
    powder_burst(f, t, tc, mx, my - 160, n=70)
    if hit_:
        fl = clamp(1 - (t - tc) / 0.25) * 0.55
        f = f * (1 - fl) + C((255, 40, 80)) * fl
    put_head(f, 200, 1350, "shock" if hit_ else "wow", t, 0.95, 0, look=(1, -1))
    return f


def shot_CT(t, n):
    s = SHOT["CT"]["start"]
    f = bgset((255, 226, 70), (255, 110, 20), (255, 255, 255), 540, 1080, 340, t=t, seed=71, spark=12)
    tier(f, t, E["t_seventy"] - 0.08, "it takes about", "70,000", 470, size=250, fill=(226, 0, 70), gap=170)
    if t > E["t_bugs"] - 0.1:
        put(f, small("bugs", 64, (40, 10, 30)), CX, 640, op=appear(t, E["t_bugs"] - 0.1))
    tj = E["t_one"] - 0.1
    k = eo((t - s) / 1.6)
    px = lerp(540, 390, eio((t - tj) / 0.35)) if t > tj else 540
    pile = pile_img(int(30 + 250 * k), 4)
    put(f, pile, px, 1200, anchor="b")
    r = np.random.default_rng(9)
    for i in range(26):
        ph = r.uniform(0, 1); sp = r.uniform(1.4, 2.2)
        q = ((t - s) * sp + ph) % 1.0
        if t - s < ph / sp:
            continue
        bug(f, px + r.uniform(-160, 160), lerp(700, 1120, q ** 2), 30, r.uniform(0, 360) + t * 200, t, shadow=False, seed=i % 5)
    if t > tj:
        q = popk(t, tj, 0.35)
        put(f, jar_img(), 790, 1080, op=clamp(q * 3), sc=0.5 + 0.5 * q)
        arrow_to(f, 560, 1080, 700, 1060, op=clamp((t - tj) / 0.3))
        put(f, pill("= 1 pound of dye", 50, bg=(150, 0, 50), acc=(255, 230, 90)), CX, 1340, op=clamp(q * 3), sc=0.85 + 0.15 * q)
    return f


def shot_WT(t, n):
    s = SHOT["WT"]["start"]
    f = bgset((160, 70, 255), (40, 10, 110), (255, 206, 0), 540, 960, 330, t=t, seed=81)
    pose = "pointup" if t < E["t_not"] - 0.05 else "shrug"
    put_char(f, 380, 1460, pose, "mischief" if t < E["t_not"] - 0.05 else "talk", t, 1.08, m=mouth(t))
    tl = E["t_just"] - 0.15
    if t > tl:
        q = eo((t - tl) / 0.35)
        put_lip(f, lerp(1200, 760, q), 1300, 220, 0.72)
    if t > E["t_lip2"] + 0.05:
        k = popk(t, E["t_lip2"] + 0.05, 0.3)
        put(f, big("+", 300, (255, 230, 60), 12), 760, 700, op=clamp(k * 3), sc=0.5 + 0.5 * k)
    return f


def shot_FD(t, n):
    s = SHOT["FD"]["start"]
    f = bgset((0, 226, 210), (0, 70, 130), None, t=t, seed=91, spark=16)
    for x, tk, kind, col in ((250, E["t_yogurt"], "yogurt", (255, 120, 180)), (540, E["t_candy"], "candy", (255, 206, 0)),
                             (830, E["t_ice"], "ice", (255, 90, 120))):
        t0 = tk - 0.12
        q = popk(t, t0, 0.32)
        disc(f, x, 860, 135 * min(1, q * 1.2), col, glow=0.3)
        if q > 0.01:
            put(f, food(kind), x, 850, sc=(0.4 + 0.6 * q) * 1.1)
            if t > t0 + 0.3:
                u = eo((t - t0 - 0.3) / 0.35)
                bug(f, x + 55, lerp(560, 760, u) - 70 * math.sin(math.pi * u), 44, 160, t, walk=2.5, seed=int(x) % 5, sc=1)
    sh = t > E["t_yogurt"]
    put_char(f, 540, 1480, "shock" if sh else "stand", "gross" if t > E["t_candy"] else "wow", t, 0.82, m=mouth(t))
    return f


def shot_AL(t, n):
    s, e = SHOT["AL"]["start"], SHOT["AL"]["end"]
    f = bgset((255, 120, 70), (130, 20, 40), (255, 220, 120), 470, 980, 320, t=t, seed=101, spark=10)
    worried = t > E["t_cause"] - 0.1
    put_head(f, 460, 980, "worried" if worried else "think", t, 2.3, mouth(t), look=(1, 0) if worried else (0, -1))
    if t > E["t_few"] - 0.1:
        put(f, pill("for a few people", 46, bg=(120, 20, 40), acc=(255, 200, 80)), CX, 450, op=appear(t, E["t_few"] - 0.1))
    if t > E["t_allergic"] - 0.1:
        k = popk(t, E["t_allergic"] - 0.1, 0.35)
        put(f, warn_sign(220), 790, 660, op=clamp(k * 3), sc=0.5 + 0.5 * k, rot=6 * math.sin(t * 5))
        put(f, pill("allergic reactions", 50, bg=(30, 20, 40), acc=(255, 210, 0)), CX, 1360, op=clamp(k * 3), sc=0.85 + 0.15 * k)
    z = 1.0 + 0.06 * eio((t - s) / (e - s))
    return zoom_at(f, z, 540, 900)


def shot_LB(t, n):
    s, e = SHOT["LB"]["start"], SHOT["LB"]["end"]
    f = bgset((120, 255, 210), (0, 140, 140), (255, 255, 255), 540, 820, 380, t=t, seed=111, spark=10)
    hl = clamp((t - E["t_carmine2"] + 0.1) / 0.3)
    card = label_card(hl)
    k = popk(t, s, 0.35)
    put(f, card, CX, 820, sc=0.8 + 0.2 * k)
    # magnifier sweeps to the highlighted word
    u = eio((t - s - 0.1) / 0.9)
    mxx, myy = lerp(760, 495, u), lerp(1000, 855, u)
    inner = zoom_at(f, 1.5, mxx, myy)
    f = lens(f, inner, mxx, myy, 150, ring=(30, 36, 60))
    ang = math.radians(45)
    cv2.line(f, (int(mxx + math.cos(ang) * 158), int(myy + math.sin(ang) * 158)), (int(mxx + math.cos(ang) * 290), int(myy + math.sin(ang) * 290)),
             C((30, 36, 60)).tolist(), 30, cv2.LINE_AA)
    put_char(f, 190, 1500, "point", "talk", t, 0.62, m=mouth(t))
    return f


def shot_TC(t, n):
    s = SHOT["TC"]["start"]
    f = bgset((0, 214, 160), (0, 64, 92), (255, 206, 0), 560, 1050, 320, t=t, seed=121)
    k = popk(t, s + 0.02, 0.38)
    put(f, tip_card(t > E["t_twenty"] - 0.05), CX, 560, op=clamp(k * 3), sc=(0.7 + 0.3 * k) * (MAXW + 40) / 920, rot=1.5 * (1 - k))
    put(f, pill("SKIN TIP", 36, bg=(0, 150, 100), acc=(255, 230, 90)), 300, 410, op=clamp(k * 3))
    put_char(f, 330, 1460, "point", "smile" if t > E["t_twenty"] else "talk", t, 1.0, m=mouth(t))
    put_lip(f, 760, 1340, 200, 0.7)
    if t > E["t_twenty"] - 0.05:
        sparkles(f, t, 123, n=8, area=(640, 900, 880, 1200), op=1, size=10)
    return f


def shot_LP(t, n):
    s, e = SHOT["LP"]["start"], SHOT["LP"]["end"]
    f = bgset(PINK0, PINK1, (255, 206, 0), 640, 960, 320, t=t, seed=131, spark=20)
    ext = 120 + 140 * eo((t - E["t_put"]) / 0.6) if t > E["t_put"] else 120
    put_lip(f, 740, 1340, ext, 0.85)
    put_char(f, 300, 1470, "mirror", "smile", t, 1.0, m=mouth(t))
    z = 1.0 + 0.05 * eio((t - s) / (e - s))
    return zoom_at(f, z, 600, 1000)


def shot_LQ(t, n):
    s, e = SHOT["LQ"]["start"], SHOT["LQ"]["end"]
    f = bgset(PINK0, PINK1, (255, 206, 0), 640, 960, 320, t=t, seed=131, spark=20)
    ext = 260
    put_lip(f, 740, 1340, ext, 0.85)
    tx, ty = lip_top(740, 1340, ext, 0.85)
    tyy = E["t_yourself"] - 0.1
    if t > tyy:
        q = popk(t, tyy, 0.35)
        bug(f, tx - 30, ty + 6, 54, -20 + 15 * math.sin(t * 6), t, sc=q, walk=2, seed=3)
    put_char(f, 300, 1470, "mirror", "nervous" if t > tyy else "whisper", t, 1.0, m=mouth(t), look=(1, -1))
    u = eio((t - s) / (e - s))
    z = 1.0 + 1.3 * u
    f = zoom_at(f, z, tx - 30, ty + 40, lerp(tx - 30, 540, u), lerp(ty + 40, 860, u))
    if t > e - 0.2:
        q = clamp((t - (e - 0.2)) / 0.2)
        f = f * (1 - q * 0.8) + C(PINK0) * q * 0.8
    return f


RENDER = {k: globals()[f"shot_{k}"] for k in SHOT}


def rs(sid, t, n):
    s = SHOT[sid]
    tt = min(max(t, s["start"]), s["end"] - 1e-3)
    return RENDER[sid](tt, n)


# ---------------- camera ----------------
PUNCH = [(E["t_bugs0"], 0.10, 0.35), (E["t_carmine"], 0.06, 0.3), (E["t_cochineal"], 0.05, 0.3), (E["t_peru"], 0.04, 0.3),
         (E["t_females"], 0.03, 0.3), (E["t_crushed"], 0.12, 0.35), (E["t_thousand"], 0.08, 0.3), (E["t_one"], 0.06, 0.3), (E["t_wait"], 0.08, 0.3),
         (E["t_yogurt"], 0.04, 0.25), (E["t_candy"], 0.04, 0.25), (E["t_ice"], 0.04, 0.25), (E["t_allergic"], 0.06, 0.3), (E["t_carmine2"], 0.04, 0.3),
         (E["t_twenty"], 0.05, 0.3), (E["t_yourself"], 0.05, 0.3)]
SHAKE = [(E["t_bugs0"], 22, 0.45), (E["t_carmine"], 10, 0.3), (E["t_crushed"], 28, 0.5), (E["t_thousand"], 16, 0.4), (E["t_wait"], 14, 0.35),
         (E["t_allergic"], 10, 0.35)]


def camera(t):
    z = 1.0
    for t0, a, d in PUNCH:
        if t0 - 0.05 <= t < t0 + d * 4:
            q = t - t0
            z += a * (clamp((q + 0.05) / 0.05) if q < 0 else math.exp(-q / d))
    dx = dy = 0.0
    for t0, a, d in SHAKE:
        if t0 <= t < t0 + d:
            q = (t - t0) / d
            amp = a * (1 - q) ** 2
            dx += amp * math.sin(t * 91); dy += amp * math.cos(t * 77 + 1)
    return z, dx, dy


def zoom_frame(f, z, dx=0.0, dy=0.0):
    if abs(z - 1) < 1e-3 and abs(dx) < 0.3 and abs(dy) < 0.3:
        return f
    M = np.float32([[z, 0, (1 - z) * W / 2 + dx], [0, z, (1 - z) * H / 2 + dy]])
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


# ---------------- transitions ----------------
def whip_trans(A, Bf, q):
    e = eio(q)
    off = int(W * e)
    out = np.empty_like(A)
    out[:, :W - off] = A[:, off:]
    out[:, W - off:] = Bf[:, :off]
    k = int(2 + 80 * math.sin(math.pi * q))
    return cv2.blur(out, (k, 1)) if k > 2 else out


def pop_trans(A, Bf, q, col=(255, 255, 255)):
    R = 1300 * eo(q)
    d = np.sqrt((_xx - W / 2) ** 2 + (_yy - H / 2) ** 2)
    m = np.clip(R - d + 1, 0, 1)[..., None]
    out = A * (1 - m) + Bf * m
    ring = np.exp(-((d - R) / 10) ** 2)[..., None] * (1 - q)
    return out * (1 - ring) + C(col) * ring


def zblur(f, amt):
    if amt < 0.01:
        return f
    acc = f.copy()
    for i in range(1, 5):
        acc += zoom_frame(f, 1 + amt * i / 4)
    return acc / 5


def zoomblur_trans(A, Bf, q):
    if q < 0.5:
        u = q / 0.5
        return zblur(zoom_frame(A, 1 + 0.5 * u * u), 0.25 * u)
    u = (q - 0.5) / 0.5
    return zblur(zoom_frame(Bf, 1 + 0.4 * (1 - u) ** 2), 0.25 * (1 - u))


def dip_trans(A, Bf, q):
    if q < 0.5:
        return A * (1 - eio(q / 0.5) * 0.92)
    return Bf * (0.08 + 0.92 * eio((q - 0.5) / 0.5))


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    f = None
    for cur, nxt in ((SHOTS[i - 1] if i > 0 else None, sh), (sh, nx)):
        if cur is None or nxt is None or f is not None:
            continue
        b, k = nxt["start"], nxt["trans"]
        if k == "whip" and b - 0.13 <= t < b + 0.13:
            f = whip_trans(rs(cur["id"], t, n), rs(nxt["id"], t, n), (t - b + 0.13) / 0.26)
        elif k == "pop" and b - 0.08 <= t < b + 0.26:
            f = pop_trans(rs(cur["id"], t, n), rs(nxt["id"], t, n), (t - b + 0.08) / 0.34)
        elif k == "zoomblur" and b - 0.16 <= t < b + 0.16:
            f = zoomblur_trans(rs(cur["id"], t, n), rs(nxt["id"], t, n), (t - b + 0.16) / 0.32)
        elif k == "dip" and b - 0.2 <= t < b + 0.2:
            f = dip_trans(rs(cur["id"], t, n), rs(nxt["id"], t, n), (t - b + 0.2) / 0.4)
    if f is None:
        f = rs(sh["id"], t, n)
        q = t - sh["start"]
        if sh["trans"] == "flash" and q < 0.3:
            f = f + (1 - f) * (1 - q / 0.3) ** 2
        elif sh["trans"] == "flashp" and q < 0.3:
            w_ = (1 - q / 0.3) ** 2 * 0.85
            f = f * (1 - w_) + C((200, 80, 255)) * w_
        elif sh["trans"] == "punch" and q < 0.3:
            f = zoom_frame(f, 1 + 0.16 * (1 - eo(q / 0.3)))
        if nx is not None and nx["trans"] in ("flash", "flashp") and nx["start"] - t < 0.08:
            f = f + (1 - f) * (1 - (nx["start"] - t) / 0.08) * 0.8
    z, dx, dy = camera(t)
    f = zoom_frame(np.clip(f, 0, 1), z, dx, dy)
    # finish: vibrance + gentle contrast + vignette
    lum = (f * np.array([0.299, 0.587, 0.114], np.float32)).sum(2, keepdims=True)
    f = lum + (f - lum) * 1.14
    f = (f - 0.5) * 1.05 + 0.5
    f = f * VIG
    if GUIDES:
        f = guides(f)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)


VIG = (1 - 0.24 * np.clip(np.sqrt(((_xx - W / 2) / (W * 0.62)) ** 2 + ((_yy - H / 2) / (H * 0.6)) ** 2) - 0.45, 0, 1) ** 1.5)[..., None].astype(np.float32)


def main():
    if ONLY:
        os.makedirs(f"{B}/frames", exist_ok=True)
        for n in ONLY:
            cv2.imwrite(f"{B}/frames/r_{n:04d}.jpg", cv2.cvtColor(compose(n), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
        return
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "medium",
                            "-crf", "16", "-profile:v", "high",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                            "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    a, b = int(os.environ.get("SEG_A", 0)), int(os.environ.get("SEG_B", N))
    for n in range(a, min(b, N)):
        enc.stdin.write(compose(n).tobytes())
        if n % 60 == 0:
            print(f"frame {n}/{N}", flush=True)
    enc.stdin.close(); enc.wait()
    print("done", OUT, N)


if __name__ == "__main__":
    main()
