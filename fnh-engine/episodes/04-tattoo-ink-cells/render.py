"""FreshNestHub ep04 — 'Your tattoo is being eaten by your own cells' (macrophages hold tattoo ink). Fully procedural: NESSA host + 3D macrophages, ink, skin layers.
Usage: render_mites.py OUT.mp4 [frame,frame,...]   (GUIDES=1 draws IG/Shorts safe-zone overlay on test frames)"""
import os, sys, json, math, subprocess
import numpy as np, cv2, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, "/home/claude/reel-kit/english/scripts")
from nessa import nessa, head, floor_shadow
from mites_assets import gen_skin, draw_mite, stamp, sphere, comp_mites, radius

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


# ---------------- skin world ----------------
SKIN, PORES = gen_skin(1400, 2300, 3, "warm")
SKIN2, PORES2 = gen_skin(1400, 2300, 11, "warm")


def tint(img, mode):
    if mode == "day":
        out = img
    elif mode == "night":
        lum = (img * np.array([0.3, 0.55, 0.15], np.float32)).sum(2, keepdims=True)
        out = img * np.array([0.42, 0.48, 0.95], np.float32) * 0.62 + lum * np.array([0.10, 0.16, 0.42], np.float32)
    elif mode == "party":
        lum = (img * np.array([0.3, 0.55, 0.15], np.float32)).sum(2, keepdims=True)
        out = img * np.array([0.72, 0.38, 0.95], np.float32) * 0.62 + lum * np.array([0.22, 0.05, 0.38], np.float32)
    elif mode == "red":
        out = img * np.array([1.08, 0.72, 0.68], np.float32)
    else:
        out = img
    return out


def skin_view(ox, oy, z=1.0, tex=None):
    """1080x1920 window of the skin texture; top-left (ox,oy) in texture px, zoom z around the window centre"""
    T = SKIN if tex is None else tex
    if abs(z - 1) < 1e-3 and 0 <= ox <= T.shape[1] - W and 0 <= oy <= T.shape[0] - H:
        x0, y0 = int(ox), int(oy)
        return T[y0:y0 + H, x0:x0 + W].copy()
    cx, cy = ox + W / 2, oy + H / 2
    M = np.float32([[z, 0, W / 2 - z * cx], [0, z, H / 2 - z * cy]])
    return cv2.warpAffine(T, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def pore_near(px, py, pores=None):
    P = PORES if pores is None else pores
    d = (P[:, 0] - px) ** 2 + (P[:, 1] - py) ** 2
    return P[int(np.argmin(d))]


def mite(f, x, y, ang, L, t, vis=1.0, wig=1.0, eyes=False, op=1.0, shadow=0.55, walk=1.0, phase=0.0, curl=0.0, clipmask=None, emerge=None):
    """draw one mite into frame f. If emerge=(px,py): mite is positioned so its cut point sits in that pore."""
    pad = int(L * 0.12) + 30
    if emerge is not None:
        # build spine at origin to find the cut point, then shift
        from mites_assets import spine
        pts = spine(0, 0, ang, L, t, wig, curl, phase)
        k = max(1, int(80 * vis)) - 1
        x, y = emerge[0] - pts[k][0], emerge[1] - pts[k][1]
    dx, dy = math.cos(ang), math.sin(ang)
    bx0 = min(x, x - dx * L) - pad; bx1 = max(x, x - dx * L) + pad
    by0 = min(y, y - dy * L) - pad; by1 = max(y, y - dy * L) + pad
    bx0, by0 = int(bx0), int(by0)
    w, h = int(bx1 - bx0), int(by1 - by0)
    if w <= 4 or h <= 4 or bx0 > W or by0 > H or bx0 + w < 0 or by0 + h < 0:
        return None
    can = np.zeros((h, w, 3), np.float32)
    al = np.zeros((h, w), np.float32)
    pts = draw_mite(can, al, x - bx0, y - by0, ang, L, t, vis=vis, wig=wig, eyes=eyes, walk=walk, phase=phase, curl=curl)
    if clipmask is not None:
        al *= clipmask[max(0, by0):max(0, by0) + h, max(0, bx0):max(0, bx0) + w][:al.shape[0], :al.shape[1]] if bx0 >= 0 and by0 >= 0 else 1
    comp_mites(f, can, al, bx0, by0, shadow=shadow, sh_off=(int(L * 0.025) + 4, int(L * 0.04) + 6), blur=max(3, L * 0.02), op=op)
    if emerge is not None and vis < 0.995:
        k = max(1, int(80 * vis)) - 1
        cx_, cy_ = pts[k][0] + bx0, pts[k][1] + by0
        r = radius(pts[k][2], L) * 1.45
        pore_mouth(f, cx_, cy_, r, op)
    return pts


def pore_mouth(f, cx, cy, r, op=1.0):
    x0, x1, y0, y1 = int(max(0, cx - 2 * r)), int(min(W, cx + 2 * r)), int(max(0, cy - 2 * r)), int(min(H, cy + 2 * r))
    if x1 <= x0 or y1 <= y0:
        return
    d = np.sqrt((_xx[y0:y1, x0:x1] - cx) ** 2 + ((_yy[y0:y1, x0:x1] - cy) * 1.1) ** 2) / r
    a = np.clip(1.15 - d, 0, 1) ** 0.7 * 0.92 * op
    f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * (1 - a[..., None]) + np.array([0.18, 0.07, 0.06], np.float32) * a[..., None]
    lip = np.exp(-((d - 1.0) / 0.12) ** 2) * np.clip((_xx[y0:y1, x0:x1] - cx + _yy[y0:y1, x0:x1] - cy) / (2 * r), 0, 1) * 0.5 * op
    f[y0:y1, x0:x1] += lip[..., None] * np.array([1.0, 0.85, 0.75], np.float32) * 0.6


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


def lens(f, inner, cx, cy, r, ring=(255, 255, 255)):
    if r < 2:
        return f
    d = np.sqrt((_xx - cx) ** 2 + (_yy - cy) ** 2)
    m = np.clip(r - d + 0.5, 0, 1)[..., None]
    f = f * (1 - m) + inner * m
    rim = np.exp(-((d - r) / 7) ** 2)[..., None]
    f = f * (1 - rim * 0.95) + C(ring) * rim * 0.95
    sh = np.exp(-np.clip(d - r - 6, 0, None) / 18)[..., None] * (d > r + 6)[..., None] * 0.35
    f = f * (1 - sh)
    gl = (np.exp(-((d - r * 0.82) / (r * 0.05)) ** 2) * np.clip(-(_xx - cx + _yy - cy) / (r * 1.2), 0, 1))[..., None] * 0.35
    return np.clip(f + gl, 0, 1)


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



def chew(t, rate=7.0):
    return 0.5 + 0.5 * math.sin(t * rate)


def ball(f, x, y, r, col, op=1.0):
    spr = sphere(r, col, rim=0.45, spec=0.8)
    n_ = spr[1].shape[0]
    over(f, spr[0], spr[1], x - n_ / 2, y - n_ / 2, op)


# ---- skin layers cross-section ----
_LB = {}
LX0, LX1 = 120, 960


def layers_block(y0=760, y1=1470):
    key = (y0, y1)
    if key in _LB:
        return _LB[key]
    rng = np.random.default_rng(21)
    k = 2
    im = Image.new("RGBA", (W * k, H * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0, x1 = LX0, LX1
    sc_h = 96
    # dermis
    d.rounded_rectangle([x0 * k, (y0 + 290) * k, x1 * k, y1 * k], 30 * k, fill=(240, 134, 142, 255))
    for i in range(140):
        yb = rng.uniform(y0 + 320, y1 - 30); xb = rng.uniform(x0, x1 - 120)
        pts = [((xb + j * 16) * k, (yb + 8 * math.sin(j * 0.8 + i)) * k) for j in range(rng.integers(5, 10))]
        d.line(pts, fill=(255, 180, 182, 255), width=3 * k)
    # blood vessel
    vy = y0 + 470
    pts = [((x0 + 10 + u * (x1 - x0 - 20)) * k, (vy + 40 * math.sin(u * 5)) * k) for u in np.linspace(0, 1, 40)]
    d.line(pts, fill=(150, 20, 40, 255), width=46 * k, joint="curve")
    d.line(pts, fill=(214, 40, 60, 255), width=32 * k, joint="curve")
    d.line([(x, y - 8 * k) for x, y in pts], fill=(255, 120, 130, 255), width=6 * k, joint="curve")
    # living epidermis (round cells)
    d.rectangle([x0 * k, (y0 + sc_h) * k, x1 * k, (y0 + 300) * k], fill=(255, 196, 176, 255))
    for row in range(5):
        yy = y0 + sc_h + 22 + row * 40
        off = 20 if row % 2 else 0
        for xx in range(x0 + 10 + off, x1 - 10, 44):
            d.ellipse([(xx - 20) * k, (yy - 18) * k, (xx + 20) * k, (yy + 18) * k], fill=(255, 214, 196, 255), outline=(220, 140, 130, 255), width=2 * k)
            d.ellipse([(xx - 6) * k, (yy - 6) * k, (xx + 6) * k, (yy + 6) * k], fill=(190, 90, 120, 255))
    # basal line
    d.line([(x0 * k, (y0 + 300) * k), (x1 * k, (y0 + 300) * k)], fill=(200, 80, 100, 255), width=5 * k)
    im = im.resize((W, H), Image.LANCZOS)
    _LB[key] = to_np(im)
    # stratum corneum bricks (drawn per frame so clumps can lift off)
    bricks = []
    for row in range(4):
        yy = y0 + row * 24
        off = 36 if row % 2 else 0
        for xx in range(x0 - off, x1, 72):
            a_, b_ = max(x0, xx), min(x1, xx + 70)
            if b_ - a_ > 10:
                bricks.append((a_, yy, b_, yy + 22, row))
    _LB[key + ("b",)] = bricks
    return _LB[key]


CLUMPS = [(300, 2), (560, 3), (790, 2)]   # (centre x, rows deep)


def in_clump(bx, row, y0):
    for cx_, rows in CLUMPS:
        if abs(bx - cx_) < 110 and row < rows:
            return cx_
    return None


def draw_layers(f, t, y0=760, y1=1470, red=0.0, lift=0.0, oil=1.0, hair=True, x_off=0, sc=1.0):
    rgb, a = layers_block(y0, y1)
    sh = cv2.GaussianBlur(a, (0, 0), 18)
    f *= (1 - 0.35 * np.roll(np.roll(sh, 24, 0), 14, 1))[..., None]
    over(f, rgb, a, 0, 0)
    bricks = _LB[(y0, y1, "b")]
    clumps = {}
    for (bx0, by0, bx1, by1, row) in bricks:
        c_ = in_clump((bx0 + bx1) / 2, row, y0) if lift > 0 else None
        if c_ is not None:
            clumps.setdefault(c_, []).append((bx0, by0, bx1, by1))
            continue
        cv2.rectangle(f, (bx0, by0), (bx1, by1), (0.96, 0.86, 0.74), -1, cv2.LINE_AA)
        cv2.rectangle(f, (bx0, by0), (bx1, by1), (0.74, 0.56, 0.46), 2, cv2.LINE_AA)
    # hair shaft through the layers
    if hair:
        hx = 680
        cv2.line(f, (hx, y0 + 300), (hx + 40, y0 - 520), (0.18, 0.10, 0.06), 30, cv2.LINE_AA)
        cv2.line(f, (hx - 7, y0 + 300), (hx + 33, y0 - 520), (0.40, 0.25, 0.15), 8, cv2.LINE_AA)
        disc(f, hx, y0 + 300, 34, (196, 70, 92))
    # oil film on top
    if oil > 0:
        m = np.zeros((H, W), np.float32)
        cv2.rectangle(m, (LX0, y0 - 16), (LX1, y0 + 2), 1.0, -1)
        m = cv2.GaussianBlur(m, (0, 0), 3)[..., None] * 0.8 * oil
        f[:] = f * (1 - m) + np.array([1.0, 0.80, 0.22], np.float32) * m
    # inflammation
    if red > 0:
        reg = np.zeros((H, W), np.float32)
        cv2.rectangle(reg, (LX0, y0), (LX1, y1), 1.0, -1)
        pulse = 0.85 + 0.15 * math.sin(t * 9)
        fall = np.clip(1 - (_yy - y0) / (y1 - y0) * 0.7, 0, 1)
        mm = (reg * fall * red * 0.55 * pulse)[..., None]
        f[:] = f * (1 - mm) + np.array([0.95, 0.08, 0.12], np.float32) * mm
    # lifting clumps
    for j, (c_, bl) in enumerate(sorted(clumps.items())):
        q = clamp(lift * 1.15 - j * 0.12)
        dy = -250 * eio(q) - 20 * q
        dx = (c_ - 540) * 0.35 * q
        ang = (j - 1) * 0.5 * q
        for (bx0, by0, bx1, by1) in bl:
            ptsr = np.array([(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)], np.float32)
            cx_, cy_ = c_, y0 + 40
            ca, sa = math.cos(ang), math.sin(ang)
            pr = [((px - cx_) * ca - (py - cy_) * sa + cx_ + dx, (px - cx_) * sa + (py - cy_) * ca + cy_ + dy) for px, py in ptsr]
            p = np.array(pr, np.int32)
            cv2.fillPoly(f, [p], (0.98, 0.95, 0.88), cv2.LINE_AA)
            cv2.polylines(f, [p], True, (0.72, 0.62, 0.55), 2, cv2.LINE_AA)
    return f


def big_set(c0, c1, disc_col=(255, 206, 0), dx=540, dy=930, dr=340, seed=1, t=0.0, cy=0.46):
    f = grad(c0, c1, cy=cy)
    disc(f, dx, dy, dr, disc_col, glow=0.45)
    sparkles(f, t, seed, n=18, op=0.8)
    return f


def step_pill(f, t, t0, n, label, col=(255, 64, 140)):
    k = appear(t, t0, 0.25)
    if k > 0:
        put(f, pill(f"STEP {n}   {label}", 44, bg=(18, 16, 40), acc=col[:3]), CX, 320, op=k, sc=0.9 + 0.1 * popk(t, t0))


_CARD = {}


def tip_card2(line1, line2, done, acc=(0, 178, 114)):
    key = (line1, line2, done, acc)
    if key in _CARD:
        return _CARD[key]
    k = 2
    w, h = 820, 200
    im = Image.new("RGBA", ((w + 80) * k, (h + 90) * k), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([46 * k, 60 * k, (46 + w) * k, (60 + h) * k], 34 * k, fill=(0, 0, 0, 140))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14 * k)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40 * k, 40 * k, (40 + w) * k, (40 + h) * k], 34 * k, fill=(255, 255, 255, 255))
    d.rounded_rectangle([40 * k, 40 * k, (40 + w) * k, (40 + h * 0.45) * k], 34 * k, fill=(246, 250, 255, 255))
    d.rounded_rectangle([40 * k, 40 * k, 64 * k, (40 + h) * k], 12 * k, fill=acc + (255,))
    bx, by = 100, 40 + h / 2
    d.rounded_rectangle([(bx - 38) * k, (by - 38) * k, (bx + 38) * k, (by + 38) * k], 14 * k, fill=acc + (255,) if done else (255, 255, 255, 255),
                        outline=tuple(int(c * 0.78) for c in acc) + (255,), width=6 * k)
    if done:
        d.line([((bx - 20) * k, by * k), ((bx - 4) * k, (by + 18) * k), ((bx + 24) * k, (by - 20) * k)], fill=(255, 255, 255, 255), width=10 * k,
               joint="curve")
    f1 = ImageFont.truetype(IB, 48 * k); f2 = ImageFont.truetype(ISB, 34 * k)
    d.text((160 * k, (40 + 36) * k), line1, font=f1, fill=(16, 20, 34, 255))
    d.text((160 * k, (40 + 108) * k), line2, font=f2, fill=(70, 80, 100, 255))
    im = im.resize((im.width // k, im.height // k), Image.LANCZOS)
    _CARD[key] = im
    return im




# ================= ep04 assets: macrophages, ink, inked forearm, needle, mouse, lymph node =================
MPH = (0.82, 0.46, 1.0)        # macrophage lavender-purple
FRESH = (0.30, 0.92, 0.78)     # fresh recruit (mint)
INKC = (0.10, 0.12, 0.30)      # navy-black tattoo ink
_MP = {}


def face_on(im, c, R, expr="happy", mq=0.0):
    d = ImageDraw.Draw(im)
    ex, ey, er = R * 0.30, c - R * 0.14, R * 0.17
    for s in (-1, 1):
        if expr == "sad":
            d.arc([c + s * ex - er, ey - er * 1.5, c + s * ex + er, ey - er * 0.2], 200, 340, fill=(20, 14, 18, 255), width=max(2, int(R * 0.05)))
        d.ellipse([c + s * ex - er, ey - er * 1.15, c + s * ex + er, ey + er * 1.15], fill=(255, 255, 255, 255), outline=(20, 14, 18, 255),
                  width=max(2, int(R * 0.035)))
        pr = er * 0.55
        d.ellipse([c + s * ex - pr + er * 0.15, ey - pr + er * 0.1, c + s * ex + pr + er * 0.15, ey + pr + er * 0.1], fill=(20, 14, 18, 255))
        d.ellipse([c + s * ex - pr * 0.2, ey - pr * 0.6, c + s * ex + pr * 0.25, ey - pr * 0.15], fill=(255, 255, 255, 255))
    my = c + R * 0.30
    if expr == "sad":
        d.arc([c - R * 0.22, my, c + R * 0.22, my + R * 0.26], 200, 340, fill=(20, 14, 18, 255), width=max(2, int(R * 0.06)))
    elif mq > 0.05:
        h = R * (0.08 + 0.34 * mq)
        d.ellipse([c - R * 0.26, my - h * 0.4, c + R * 0.26, my + h], fill=(120, 20, 50, 255), outline=(20, 14, 18, 255), width=max(2, int(R * 0.04)))
        d.ellipse([c - R * 0.13, my + h * 0.35, c + R * 0.13, my + h * 0.95], fill=(240, 90, 120, 255))
    else:
        d.arc([c - R * 0.26, my - R * 0.18, c + R * 0.26, my + R * 0.2], 20, 160, fill=(20, 14, 18, 255), width=max(2, int(R * 0.06)))
    for s in (-1, 1):
        d.ellipse([c + s * R * 0.52 - R * 0.09, my - R * 0.10, c + s * R * 0.52 + R * 0.09, my], fill=(255, 140, 190, 150))


def mph_img(r, ph, ink, face, expr, mq, col, grey=0.0):
    """3D shaded macrophage: wobbly blob with pseudopods, nucleus and swallowed ink granules. PIL RGBA centred."""
    key = (int(r), ph, round(ink, 2), face, expr, mq, col, round(grey, 2))
    if key in _MP:
        return _MP[key]
    if len(_MP) > 500:
        _MP.clear()
    k = 2
    R = r * k
    n = int(R * 3.0)
    c = n / 2
    th = np.linspace(0, 2 * math.pi, 140, endpoint=False)
    p = ph * 2 * math.pi / 16
    rad = R * (1 + 0.09 * np.sin(3 * th + p) + 0.06 * np.sin(5 * th - 1.3 * p + 1) + 0.04 * np.sin(7 * th + 2 * p)
               + 0.22 * np.exp(-((np.angle(np.exp(1j * (th - 0.4 - 0.2 * math.sin(p))))) / 0.22) ** 2)
               + 0.16 * np.exp(-((np.angle(np.exp(1j * (th - 3.6 + 0.2 * math.cos(p))))) / 0.20) ** 2))
    pts = np.stack([c + np.cos(th) * rad, c + np.sin(th) * rad * 0.94], 1).astype(np.int32)
    m = np.zeros((n, n), np.uint8)
    cv2.fillPoly(m, [pts], 255, cv2.LINE_AA)
    al = m.astype(np.float32) / 255
    dist = cv2.distanceTransform((m > 127).astype(np.uint8), cv2.DIST_L2, 5)
    h = np.clip(dist / (R * 0.55), 0, 1)
    hz = np.sqrt(1 - (1 - h) ** 2) * R * 0.5
    hz = cv2.GaussianBlur(hz, (0, 0), R * 0.04)
    gy, gx = np.gradient(hz)
    nrm = np.sqrt(gx ** 2 + gy ** 2 + 1)
    Lv = np.array([-0.45, -0.55, 0.7]); Lv /= np.linalg.norm(Lv)
    diff = np.clip((-gx * Lv[0] - gy * Lv[1] + Lv[2]) / nrm, 0, 1)
    cc = np.array(col, np.float32)
    if grey > 0:
        lum = cc.mean()
        cc = cc * (1 - grey) + np.array([lum, lum, lum * 1.05]) * grey * 0.85
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    spec = np.exp(-(((xx - c) / R + 0.38) ** 2 + ((yy - c) / R + 0.42) ** 2) / 0.03) * 0.55
    rim = np.clip(1 - h, 0, 1) ** 2
    rgb = cc * (0.55 + 0.55 * diff)[..., None] + spec[..., None] + rim[..., None] * np.array([1.0, 0.85, 1.0]) * 0.18
    # nucleus (kidney shaped, darker)
    cv2.ellipse(rgb, (int(c - R * 0.12), int(c + R * 0.30)), (int(R * 0.30), int(R * 0.20)), -15, 0, 360, tuple(float(v) for v in cc * 0.62), -1,
                cv2.LINE_AA)
    cv2.ellipse(rgb, (int(c - R * 0.18), int(c + R * 0.25)), (int(R * 0.12), int(R * 0.06)), -15, 0, 360, tuple(float(v) for v in cc * 0.82), -1,
                cv2.LINE_AA)
    # swallowed ink granules (stay inside the cell)
    rng = np.random.default_rng(int(r) + 7)
    ng = int(round(ink * 34))
    for i in range(ng):
        a = rng.uniform(0, 6.28); dd = math.sqrt(rng.uniform(0, 1)) * R * 0.62
        x, y = c + math.cos(a) * dd, c + math.sin(a) * dd * 0.9
        rr = rng.uniform(0.045, 0.085) * R
        spr = sphere(rr, INKC, rim=0.4, spec=0.5)
        nn = spr[1].shape[0]
        x0, y0 = int(x - nn / 2), int(y - nn / 2)
        if 0 <= x0 and 0 <= y0 and x0 + nn < n and y0 + nn < n:
            aa = spr[1][..., None] * 0.92
            rgb[y0:y0 + nn, x0:x0 + nn] = rgb[y0:y0 + nn, x0:x0 + nn] * (1 - aa) + spr[0] * aa
    rgb = np.clip(rgb, 0, 1) * (al[..., None] > 0)
    # membrane edge
    edge = np.clip(1 - np.abs(dist - 2.5) / 2.5, 0, 1) * al
    rgb = rgb * (1 - edge[..., None] * 0.5) + cc * 0.45 * edge[..., None] * 0.5
    im = Image.fromarray((np.dstack([np.clip(rgb, 0, 1), al]) * 255).astype(np.uint8), "RGBA")
    if face:
        face_on(im, c, R, expr, mq)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(Image.fromarray((al * 110).astype(np.uint8)))
    sh = sh.filter(ImageFilter.GaussianBlur(R * 0.08))
    base = Image.new("RGBA", im.size, (0, 0, 0, 0))
    base.alpha_composite(sh, (int(R * 0.06), int(R * 0.12)))
    base.alpha_composite(im)
    out = base.resize((n // k, n // k), Image.LANCZOS)
    _MP[key] = out
    return out


def mph(f, x, y, r, t, ink=1.0, face=True, expr="happy", mouth=0.0, col=MPH, op=1.0, phase=0.0, grey=0.0, sc=1.0, rot=0.0, wob=1.0):
    ph = int(round(((t * 1.4 * wob + phase) % (2 * math.pi)) / (2 * math.pi) * 16)) % 16
    im = mph_img(max(6, r), ph, clamp(ink), face, expr, round(mouth * 4) / 4 if face else 0, col, grey)
    put(f, im, x, y + 5 * math.sin(t * 2.6 + phase), op=op, sc=sc, rot=rot)


def inkdot(f, x, y, r, op=1.0):
    ball(f, x, y, r, INKC, op)


def star_pts(cx, cy, R, r, rot=-0.15, n=5):
    pts = []
    for i in range(2 * n):
        a = rot - math.pi / 2 + i * math.pi / n
        rr = R if i % 2 == 0 else r
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return np.array(pts, np.float32)


STAR_C, STAR_R = (560, 1000), 205
_ARM = {}


def arm_static(night=False):
    """opening set: hot-pink set, big sunburst disc, a tanned forearm across the frame with a bold star tattoo"""
    if night in _ARM:
        return _ARM[night]
    f = grad((255, 92, 150), (110, 20, 140), cx=0.5, cy=0.45)
    # sunburst rays + disc
    rays = np.zeros((H, W), np.float32)
    for i in range(18):
        a0 = i * math.pi / 9
        pts = np.array([(540, 1000), (540 + math.cos(a0) * 2200, 1000 + math.sin(a0) * 2200),
                        (540 + math.cos(a0 + 0.12) * 2200, 1000 + math.sin(a0 + 0.12) * 2200)], np.int32)
        cv2.fillPoly(rays, [pts], 1.0, cv2.LINE_AA)
    f = f * (1 - rays[..., None] * 0.10) + rays[..., None] * np.array([1.0, 0.85, 0.4], np.float32) * 0.10
    disc(f, 540, 1000, 330, (255, 206, 0), glow=0.45)
    # forearm: thick tilted band with skin texture + cylinder shading
    x0, y0, x1, y1 = -200, 1075, 1300, 900
    m = np.zeros((H, W), np.float32)
    cv2.line(m, (x0, y0), (x1, y1), 1.0, 420, cv2.LINE_AA)
    dx, dy = x1 - x0, y1 - y0
    Ln = math.hypot(dx, dy)
    perp = ((_xx - x0) * (-dy) + (_yy - y0) * dx) / Ln / 210.0      # -1..1 across the arm
    shade = np.clip(1.0 - 0.38 * np.clip(perp, -1, 1) ** 2 - 0.10 * perp, 0.45, 1.1)
    sk = cv2.GaussianBlur(skin_view(150, 0, 1.0), (0, 0), 2.5) * np.array([1.06, 0.94, 0.86], np.float32)
    sk = sk * 0.5 + C((236, 170, 132)) * 0.5
    armc = sk * shade[..., None]
    hl = np.exp(-((perp + 0.45) / 0.16) ** 2)[..., None] * 0.10
    armc = armc + hl
    shm = cv2.GaussianBlur(np.roll(m, 34, 0), (0, 0), 22)
    f = f * (1 - 0.45 * shm[..., None])
    f = f * (1 - m[..., None]) + armc * m[..., None]
    # tattoo: bold outline star with teal fill, multiplied into the skin (ink sits under the skin)
    tm = np.zeros((H, W), np.float32); fm = np.zeros((H, W), np.float32)
    sp = star_pts(STAR_C[0], STAR_C[1], STAR_R, STAR_R * 0.45).astype(np.int32)
    cv2.fillPoly(fm, [sp], 1.0, cv2.LINE_AA)
    cv2.polylines(tm, [sp], True, 1.0, 20, cv2.LINE_AA)
    sp2 = star_pts(STAR_C[0], STAR_C[1], STAR_R * 0.62, STAR_R * 0.28).astype(np.int32)
    cv2.polylines(tm, [sp2], True, 1.0, 8, cv2.LINE_AA)
    fm = cv2.GaussianBlur(fm, (0, 0), 1.2) * m; tm = cv2.GaussianBlur(tm, (0, 0), 1.0) * m
    teal = np.array([0.05, 0.70, 0.80], np.float32)
    f = f * (1 - fm[..., None] * (1 - teal) * 0.85)
    f = f * (1 - tm[..., None] * 0.88) + tm[..., None] * np.array([0.04, 0.05, 0.12], np.float32) * 0.88 * f.mean(2, keepdims=True)
    if night:
        lum = (f * np.array([0.3, 0.55, 0.15], np.float32)).sum(2, keepdims=True)
        f = f * 0.72 + lum * np.array([0.14, 0.10, 0.32], np.float32)
    _ARM[night] = (f.astype(np.float32), m)
    return _ARM[night]


_DM = {}


def dermis_bg(seed=1, c0=(255, 150, 170), c1=(196, 40, 110)):
    """macro of the dermis: pink tissue with wavy collagen fibres"""
    key = (seed, c0, c1)
    if key in _DM:
        return _DM[key].copy()
    f = grad(c0, c1, cx=0.5, cy=0.45)
    rng = np.random.default_rng(seed)
    can = (f * 255).astype(np.uint8).copy()
    for i in range(130):
        yb = rng.uniform(150, 1800); xb = rng.uniform(-100, 1000)
        pts = [(int(xb + j * 26), int(yb + 16 * math.sin(j * 0.5 + i))) for j in range(rng.integers(6, 16))]
        cv2.polylines(can, [np.array(pts, np.int32)], False, (255, 196, 210), int(rng.integers(3, 7)), cv2.LINE_AA)
    f = cv2.GaussianBlur(can.astype(np.float32) / 255, (0, 0), 1.6)
    _DM[key] = f
    return f.copy()




def macro_inner(t, night=False, munch=True):
    """what the lens sees over the tattoo: ink-stuffed macrophages packed in the dermis, munching"""
    f = dermis_bg(3, (255, 160, 190), (150, 30, 120))
    if night:
        lum = (f * np.array([0.3, 0.55, 0.15], np.float32)).sum(2, keepdims=True)
        f = f * 0.72 + lum * np.array([0.14, 0.10, 0.32], np.float32)
    rng = np.random.default_rng(5)
    for i in range(40):
        inkdot(f, rng.uniform(250, 900), rng.uniform(700, 1300), rng.uniform(7, 13))
    for j, (x, y, r) in enumerate(((420, 860, 105), (690, 830, 95), (560, 1080, 120), (330, 1130, 80), (800, 1110, 85))):
        mph(f, x, y, r, t, ink=0.9, face=True, mouth=chew(t + j, 10) if munch else 0, phase=j * 1.3)
    return f


def lens_with_handle(f, inner, cx, cy, r):
    # handle first (behind the rim)
    a = math.radians(48)
    hx0, hy0 = cx + math.cos(a) * (r + 6), cy + math.sin(a) * (r + 6)
    hx1, hy1 = cx + math.cos(a) * (r + 260), cy + math.sin(a) * (r + 260)
    cv2.line(f, (int(hx0 + 8), int(hy0 + 14)), (int(hx1 + 8), int(hy1 + 14)), (0.10, 0.02, 0.10), 62, cv2.LINE_AA)
    cv2.line(f, (int(hx0), int(hy0)), (int(hx1), int(hy1)), (0.12, 0.10, 0.18), 58, cv2.LINE_AA)
    cv2.line(f, (int(hx0 - 10), int(hy0 - 8)), (int(hx1 - 10), int(hy1 - 8)), (0.42, 0.40, 0.55), 10, cv2.LINE_AA)
    f = lens(f, inner, cx, cy, r, ring=(255, 214, 40))
    d = np.sqrt((_xx - cx) ** 2 + (_yy - cy) ** 2)
    rim = np.exp(-((d - r - 10) / 9) ** 2)[..., None]
    return f * (1 - rim * 0.9) + C((255, 190, 0)) * rim * 0.9


def needle(f, x, ytip, op=1.0):
    """tattoo needle: chrome shaft from the top of the frame down to the tip"""
    top = 120
    w = 15
    poly = np.array([(x - w, top), (x + w, top), (x + w, ytip - 70), (x + 2, ytip), (x - 2, ytip), (x - w, ytip - 70)], np.int32)
    cv2.fillPoly(f, [poly + [8, 12]], (0.08, 0.04, 0.12), cv2.LINE_AA)
    cv2.fillPoly(f, [poly], (0.70, 0.74, 0.80), cv2.LINE_AA)
    cv2.line(f, (x - 6, top), (x - 6, int(ytip - 70)), (0.97, 0.98, 1.0), 5, cv2.LINE_AA)
    cv2.line(f, (x + 9, top), (x + 9, int(ytip - 70)), (0.42, 0.45, 0.52), 4, cv2.LINE_AA)
    cv2.polylines(f, [poly], True, (0.15, 0.15, 0.22), 3, cv2.LINE_AA)
    # ink-wet tip
    cv2.fillPoly(f, [np.array([(x - w + 3, ytip - 50), (x + w - 3, ytip - 50), (x + 2, ytip), (x - 2, ytip)], np.int32)], INKC, cv2.LINE_AA)
    # grip tube
    cv2.rectangle(f, (x - 48, 60), (x + 48, 250), (0.10, 0.08, 0.18), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x - 44, 64), (x - 26, 246), (0.38, 0.32, 0.55), -1, cv2.LINE_AA)
    for yy in range(80, 246, 22):
        cv2.line(f, (x - 46, yy), (x + 46, yy), (0.22, 0.18, 0.32), 3, cv2.LINE_AA)


BY0, BY1 = 620, 1300            # skin block (layers) used in the needle / shed shots
NX = 760                        # needle x
_rd = np.random.default_rng(8)
DEP = [(NX + _rd.uniform(-150, 150), 935 + _rd.uniform(0, 105), _rd.uniform(8, 15)) for _ in range(36)]


def deposits(f, k, op=1.0):
    """ink droplets parked in the dermis (k = fraction deposited)"""
    for i, (x, y, r) in enumerate(DEP):
        if i < int(len(DEP) * k):
            inkdot(f, x, y, r, op)


def clock_icon(f, x, y, r, t, spin=1.0):
    disc(f, x + 8, y + 12, r, (40, 10, 60), op=0.5)
    disc(f, x, y, r, (255, 255, 255), ring=((20, 20, 40), 12))
    for i in range(12):
        a = i * math.pi / 6
        cv2.line(f, (int(x + math.cos(a) * r * 0.78), int(y + math.sin(a) * r * 0.78)), (int(x + math.cos(a) * r * 0.9), int(y + math.sin(a) * r * 0.9)),
                 (0.1, 0.1, 0.2), 5, cv2.LINE_AA)
    a1 = -math.pi / 2 + t * 6 * spin; a2 = -math.pi / 2 + t * 0.5 * spin
    cv2.line(f, (int(x), int(y)), (int(x + math.cos(a1) * r * 0.72), int(y + math.sin(a1) * r * 0.72)), (0.95, 0.1, 0.3), 7, cv2.LINE_AA)
    cv2.line(f, (int(x), int(y)), (int(x + math.cos(a2) * r * 0.5), int(y + math.sin(a2) * r * 0.5)), (0.1, 0.1, 0.2), 10, cv2.LINE_AA)
    disc(f, x, y, 12, (20, 20, 40))


def mouse(f, x, y, t, s=1.0):
    """cartoon lab mouse with a green-inked (tattooed) tail"""
    # tail
    pts = [(x + 150 * s + i * 22 * s, y + 70 * s + 60 * s * math.sin(i * 0.35 + t * 2.0) * (i / 18)) for i in range(13)]
    p = np.array(pts, np.int32)
    cv2.polylines(f, [p + [6, 10]], False, (0.15, 0.05, 0.15), int(20 * s), cv2.LINE_AA)
    cv2.polylines(f, [p], False, (1.0, 0.72, 0.78), int(18 * s), cv2.LINE_AA)
    for i in range(3, 12, 3):  # green tattoo bands (the 2018 study used green ink on mouse tails)
        cv2.line(f, (int(pts[i][0]), int(pts[i][1] - 9 * s)), (int(pts[i][0]), int(pts[i][1] + 9 * s)), (0.0, 0.70, 0.30), int(10 * s), cv2.LINE_AA)
    # body
    ball_ = sphere(150 * s, (0.96, 0.95, 0.98), rim=0.4, spec=0.5)
    over(f, ball_[0], ball_[1], x - ball_[1].shape[1] / 2, y - ball_[1].shape[0] / 2)
    cv2.ellipse(f, (int(x + 20 * s), int(y + 60 * s)), (int(150 * s), int(90 * s)), 0, 0, 180, (0.86, 0.85, 0.90), -1, cv2.LINE_AA)
    # head
    hx, hy = x - 140 * s, y - 40 * s
    for ex, ey in ((hx - 40 * s, hy - 95 * s), (hx + 55 * s, hy - 100 * s)):
        disc(f, ex, ey, 52 * s, (245, 240, 248)); disc(f, ex, ey, 32 * s, (255, 160, 190))
    hb = sphere(95 * s, (0.97, 0.96, 0.99), rim=0.4, spec=0.6)
    over(f, hb[0], hb[1], hx - hb[1].shape[1] / 2, hy - hb[1].shape[0] / 2)
    disc(f, hx - 92 * s, hy + 18 * s, 16 * s, (255, 110, 150))
    for ex in (-38, 14):
        disc(f, hx + ex * s, hy - 12 * s, 13 * s, (20, 14, 26)); disc(f, hx + ex * s - 4 * s, hy - 17 * s, 4 * s, (255, 255, 255))
    for dy_ in (-8, 6, 20):
        cv2.line(f, (int(hx - 92 * s), int(hy + 18 * s)), (int(hx - 160 * s), int(hy + 18 * s + dy_ * 1.6 * s)), (0.3, 0.3, 0.35), 3, cv2.LINE_AA)


def bean_mask(cx, cy, a, b, rot=0.0):
    th = np.linspace(0, 2 * math.pi, 120, endpoint=False)
    rr = 1 - 0.26 * np.exp(-((np.angle(np.exp(1j * (th + math.pi / 2)))) / 0.5) ** 2)
    x = np.cos(th) * a * rr; y = np.sin(th) * b * rr
    ca, sa = math.cos(rot), math.sin(rot)
    return np.stack([cx + x * ca - y * sa, cy + x * sa + y * ca], 1).astype(np.int32)


def lymph_curve(u):
    """path from the tattooed skin patch (top-left) to the lymph node (centre)"""
    x = (1 - u) ** 2 * 230 + 2 * (1 - u) * u * 940 + u * u * 560
    y = (1 - u) ** 2 * 640 + 2 * (1 - u) * u * 760 + u * u * 1070
    return x, y


def spill_pos(i, q):
    a = i * 2.39996 + 0.4
    d = 40 + 210 * eo(q) * (0.6 + 0.4 * ((i * 37) % 10) / 10)
    return 540 + math.cos(a) * d, 900 + math.sin(a) * d * 0.85


# ================= shots =================
def shot_H1(t, n):
    base, _ = arm_static()
    f = base.copy()
    sparkles(f, t, 3, n=26, op=0.9, size=8, area=(60, 260, 1020, 700))
    ls = 0.45
    u = eo((t - ls) / 0.7)
    if t > ls:
        cx = lerp(1400, 600, u); cy = lerp(780, 990, u)
        r = 245
        inner = zoom_at(macro_inner(t), 1.0, 560, 990, cx, cy)
        f = lens_with_handle(f, inner, cx, cy, r)
    if t < E["t_eaten0"] - 0.1:
        put(f, small("do you know", 64), CX, 330, op=appear(t, 0.05))
    tier(f, t, E["t_eaten0"] - 0.08, "your tattoo is being", "EATEN", 490, size=200, lo_size=60, gap=150, fill=(255, 236, 80))
    if t > E["t_own"] - 0.12:
        k = popk(t, E["t_own"] - 0.12)
        put(f, pill("by your own cells", 48, bg=(18, 16, 40), acc=(190, 120, 255)), CX, 1420, op=clamp(k * 3), sc=0.6 + 0.4 * k)
    put_char(f, 200, 1480, "shock" if t > E["t_eaten0"] else "stand", "shock" if t > E["t_eaten0"] else "talk", t, 0.5, m=mouth(t), look=(1, -1))
    return f


def shot_AN(t, n):
    s = SHOT["AN"]["start"]
    f = big_set((150, 70, 255), (40, 10, 110), (255, 206, 0), 540, 880, 310, 21, t)
    k = popk(t, s + 0.08, 0.45)
    if k > 0.02:
        mph(f, 560, 880, 210, t, ink=0.85, face=True, mouth=chew(t, 8) * 0.6 if t > E["t_holding"] else 0, sc=k)
    # ink dots drifting into the cell
    if t > E["t_holding"] - 0.3:
        for i in range(8):
            q = ((t - E["t_holding"] + 0.3) * 0.7 + i / 8) % 1.0
            a = i * 0.8 + 0.3
            inkdot(f, 560 + math.cos(a) * 330 * (1 - q), 880 + math.sin(a) * 300 * (1 - q), 14 * (1 - 0.5 * q), op=clamp((1 - q) * 4))
    tier(f, t, E["t_called"] - 0.05, "immune cells called", "MACROPHAGES", 440, size=150, lo_size=56, gap=118, fill=(255, 236, 80))
    if t < E["t_called"] - 0.05:
        put(f, small("tiny immune cells", 60), CX, 380, op=appear(t, E["t_tiny"] - 0.15))
    if t > E["t_holding"] - 0.1:
        put(f, pill("holding your ink right now", 44, acc=(0, 220, 200)), CX, 1210, op=appear(t, E["t_holding"] - 0.1), sc=0.95)
    put_char(f, 860, 1480, "point" if t > E["t_macro"] else "stand", "talk" if mouth(t) > 0.3 else "smile", t, 0.55, m=mouth(t), look=(-1, 0))
    return f


def skin_shot(t, lift=0.0, dep=0.0, glow=0.0):
    f = grad((60, 200, 255), (20, 40, 150), cx=0.5, cy=0.42)
    sparkles(f, t, 41, n=16, op=0.7, area=(60, 260, 1020, 600))
    f = draw_layers(f, t, BY0, BY1, red=0.0, lift=lift, oil=0.0, hair=False)
    if glow > 0:
        for (x, y, r) in DEP:
            disc(f, x, y, r * 2.2, (0, 230, 255), op=0.25 * glow * (0.8 + 0.2 * math.sin(t * 6)))
    deposits(f, dep)
    return f


def shot_ND(t, n):
    s, e = SHOT["ND"]["start"], SHOT["ND"]["end"]
    dep = clamp((t - E["t_pushes"]) / 2.2) if t > E["t_pushes"] else 0.0
    f = skin_shot(t, 0.0, dep)
    tgt = 1010
    if t < E["t_pushes"]:
        ytip = lerp(420, BY0 - 30, eo((t - s) / 0.6))
    else:
        ytip = tgt - 60 + 70 * abs(math.sin((t - E["t_pushes"]) * 7.5))
    needle(f, NX, int(ytip))
    if t < E["t_dermis"] - 0.15:
        step_pill(f, t, s + 0.05, 1, "THE NEEDLE")
    if t > E["t_outer"] - 0.1:
        put(f, pill("outer skin", 40, bg=(18, 16, 40), acc=(255, 214, 180)), CX, 760, op=appear(t, E["t_outer"] - 0.1), sc=0.9)
    tier(f, t, E["t_dermis"] - 0.1, "into the", "DERMIS", 500, size=170, lo_size=56, gap=128, fill=(255, 236, 80))
    put_char(f, 880, 1490, "point", "talk" if mouth(t) > 0.3 else "smile", t, 0.42, m=mouth(t), look=(-1, -1))
    return f


def shot_SD(t, n):
    s, e = SHOT["SD"]["start"], SHOT["SD"]["end"]
    lift = clamp((t - E["t_sheds"] + 0.1) / 1.4) if t > E["t_sheds"] - 0.1 else 0.0
    glow = appear(t, E["t_dermis2"] - 0.1, 0.4)
    f = skin_shot(t, lift, 1.0, glow)
    step_pill(f, t, s + 0.05, 2, "SHEDDING")
    if t > E["t_sheds"] - 0.1:
        k = popk(t, E["t_sheds"] - 0.1)
        put(f, pill("outer skin sheds every day", 46, bg=(18, 16, 40), acc=(255, 214, 180)), CX, 1390,
            op=clamp(k * 3) * (1 - clamp((t - E["t_dermis2"] + 0.2) / 0.15)), sc=0.7 + 0.3 * k)
    if t > E["t_dermis2"] - 0.1:
        k = popk(t, E["t_dermis2"] - 0.1)
        put(f, pill("the dermis stays", 48, bg=(0, 120, 160), acc=(255, 236, 80)), CX, 1390, op=clamp(k * 3), sc=0.7 + 0.3 * k)
    put_char(f, 905, 1295, "shrug" if t > E["t_but1"] else "stand", "wow" if t > E["t_stays"] else "talk", t, 0.42, m=mouth(t), look=(-1, -1))
    return f


VES_Y = 1200


def shot_IV(t, n):
    s, e = SHOT["IV"]["start"], SHOT["IV"]["end"]
    f = dermis_bg(7, (255, 150, 175), (170, 30, 100))
    # blood vessel along the bottom
    pts = [(int(x), int(VES_Y + 26 * math.sin(x * 0.006))) for x in range(-20, 1110, 30)]
    p = np.array(pts, np.int32)
    cv2.polylines(f, [p + [0, 16]], False, (0.35, 0.02, 0.10), 150, cv2.LINE_AA)
    cv2.polylines(f, [p], False, (0.62, 0.05, 0.14), 140, cv2.LINE_AA)
    cv2.polylines(f, [p], False, (0.88, 0.12, 0.22), 110, cv2.LINE_AA)
    cv2.polylines(f, [p - [0, 30]], False, (1.0, 0.45, 0.50), 12, cv2.LINE_AA)
    for i in range(9):  # red blood cells flowing
        x = ((t * 260 + i * 140) % 1250) - 80
        disc(f, x, VES_Y + 26 * math.sin(x * 0.006), 26, (230, 40, 60), ring=((150, 10, 30), 6))
    # ink particles + alarm
    alarm = t > E["t_invader"] - 0.1
    INK = [(300, 760), (520, 690), (740, 780), (420, 900), (650, 940), (820, 640)]
    for i, (x, y) in enumerate(INK):
        if alarm:
            q = ((t - E["t_invader"]) * 1.4 + i * 0.17) % 1
            disc(f, x, y, 40 + 90 * q, (255, 40, 60), op=0.45 * (1 - q))
        inkdot(f, x, y, 30)
    if alarm:
        k = popk(t, E["t_invader"] - 0.1)
        put(f, pill("INVADER!", 74, bg=(220, 20, 60), acc=(255, 236, 80)), CX, 420, op=clamp(k * 3), sc=0.6 + 0.4 * k, rot=3 * math.sin(t * 9))
    else:
        put(f, small("your body treats the ink…", 58), CX, 400, op=appear(t, E["t_body"] - 0.2))
    # macrophages squeeze out of the vessel and crawl up
    if t > E["t_sends"] - 0.2:
        for j, (tx, ty) in enumerate(((330, 880), (560, 820), (780, 860))):
            q = eio((t - E["t_sends"] + 0.2 - j * 0.15) / 1.4)
            if q <= 0:
                continue
            x = lerp(tx + (j - 1) * 30, tx, q); y = lerp(VES_Y + 20, ty + 60, q)
            mph(f, x, y, 105 * (0.5 + 0.5 * q), t, ink=0.0, face=True, expr="happy", mouth=0.6 if q > 0.8 else 0, phase=j)
        put(f, pill("macrophages to the rescue", 42, bg=(18, 16, 40), acc=(190, 120, 255)), CX, 540, op=appear(t, E["t_macro2"] - 0.1), sc=0.92)
    put_head(f, 880, 1400, "wow" if alarm else "talk", t, 0.95, mouth(t), look=(-1, -1))
    return f


def shot_SW(t, n):
    s, e = SHOT["SW"]["start"], SHOT["SW"]["end"]
    f = big_set((255, 120, 60), (170, 20, 90), (255, 220, 60), 540, 900, 330, 51, t)
    ts = E["t_swallow"] - 0.05
    q = eio((t - ts) / 0.9)
    INK = [(860, 760, 34), (900, 920, 30), (830, 1060, 32), (760, 860, 26)]
    held = q > 0.98
    # cell slides right and wraps the ink
    cx = lerp(470, 560, q)
    mphr = 220
    mph(f, cx, 900, mphr, t, ink=0.25 + 0.6 * q, face=True, mouth=(0.9 if 0.2 < q < 0.95 else 0.0) if t < E["t_cant"] else 0.0,
        expr="sad" if E["t_cant"] < t < E["t_so"] else "happy", wob=2.0 if E["t_cant"] < t < E["t_so"] else 1.0)
    if not held:
        for i, (x, y, r) in enumerate(INK):
            x2, y2 = lerp(x, cx + (i - 1.5) * 50, q), lerp(y, 900 + (i % 2) * 50 - 20, q)
            inkdot(f, x2, y2, r * (1 - 0.5 * q), op=clamp((1 - q) * 3))
    put(f, small("they swallow the ink", 60), CX, 380, op=appear(t, ts - 0.1) * (1 - clamp((t - E["t_cant"] + 0.15) / 0.2)))
    if t > E["t_cant"] - 0.12:
        k = popk(t, E["t_cant"] - 0.12)
        put(f, small("but can't break it down", 60), CX, 380, op=clamp(k * 3) * (1 - clamp((t - E["t_so"] + 0.1) / 0.2)))
        # red X over a broken-down icon (pieces) beside the cell
        if t < E["t_so"]:
            xq = eo((t - E["t_cant"]) / 0.25)
            for s_ in (-1, 1):
                cv2.line(f, (int(540 - 120 * xq), int(610 - 120 * xq * s_)), (int(540 + 120 * xq), int(610 + 120 * xq * s_)), (0.1, 0, 0), 42, cv2.LINE_AA)
                cv2.line(f, (int(540 - 120 * xq), int(610 - 120 * xq * s_)), (int(540 + 120 * xq), int(610 + 120 * xq * s_)), (0.95, 0.1, 0.15), 28, cv2.LINE_AA)
    if t > E["t_so"] - 0.1:
        k = popk(t, E["t_so"] - 0.1)
        put(f, small("so they just hold it", 64), CX, 380, op=clamp(k * 3))
        put(f, heart(60), 560, 610 + 8 * math.sin(t * 4), op=clamp(k * 3), sc=0.6 + 0.4 * k)
    hold = t > E["t_hold"] - 0.1
    put_char(f, 200, 1490, "cradle" if hold else ("shrug" if t > E["t_cant"] else "point"), "laugh" if hold else "talk", t, 0.55, m=mouth(t),
             look=(1, -1))
    return f


def star_cells():
    if "sc" in _ARM:
        return _ARM["sc"]
    sp = star_pts(STAR_C[0], STAR_C[1], STAR_R, STAR_R * 0.45)
    out = []
    for yy in range(int(STAR_C[1] - STAR_R), int(STAR_C[1] + STAR_R), 34):
        for xx in range(int(STAR_C[0] - STAR_R), int(STAR_C[0] + STAR_R), 34):
            x = xx + (17 if (yy // 34) % 2 else 0)
            if cv2.pointPolygonTest(sp.reshape(-1, 1, 2), (float(x), float(yy)), True) > 6:
                out.append((x, yy))
    _ARM["sc"] = out
    return out


def shot_SE(t, n):
    s, e = SHOT["SE"]["start"], SHOT["SE"]["end"]
    zo = eio((t - (E["t_tattoo4"] - 0.55)) / 0.9)       # 0 = macro of cells forming the star, 1 = the arm
    base, _ = arm_static()
    if zo < 0.999:
        g = dermis_bg(9, (255, 175, 200), (200, 60, 140))
        cells = star_cells()
        for j, (x, y) in enumerate(cells):
            mph(g, x, y, 17, t, ink=1.0, face=False, phase=j * 0.7, wob=0.5)
        # camera: start zoomed in 3.2x on the star, pull back to 1x while cross-fading to the tattoo on the arm
        z = lerp(1.9, 1.0, zo)
        az = zoom_at(base, z, STAR_C[0], STAR_C[1], 540, lerp(960, STAR_C[1], zo))
        gz = zoom_at(g, z, STAR_C[0], STAR_C[1], 540, lerp(960, STAR_C[1], zo))
        mix_ = clamp((zo - 0.35) / 0.5)
        f = gz * (1 - mix_) + az * mix_
    else:
        f = base.copy()
        sparkles(f, t, 61, n=30, op=1.0, size=9, area=(300, 760, 820, 1240))
    if t < E["t_tattoo4"] - 0.2:
        put(f, small("all those ink-stuffed cells…", 60), CX, 380, op=appear(t, s + 0.1))
    else:
        k = popk(t, E["t_tattoo4"] - 0.2)
        put(f, small("…are the tattoo", 60), CX, 330, op=clamp(k * 3))
        put(f, big("YOU SEE!", 170, (255, 236, 80)), CX, 470, op=clamp(k * 3), sc=0.6 + 0.4 * k)
    if zo > 0.6:
        put_char(f, 200, 1480, "cheer", "laugh", t, 0.5, m=mouth(t), op=clamp((zo - 0.6) / 0.3))
    return f


def shot_WT(t, n):
    s, e = SHOT["WT"]["start"], SHOT["WT"]["end"]
    f = big_set((40, 150, 255), (16, 20, 100), (255, 206, 0), 540, 930, 320, 71, t)
    old = clamp((t - E["t_live"] + 0.2) / 0.8)
    put(f, small("but wait…", 66), CX, 360, op=appear(t, s + 0.05))
    clock_icon(f, 540, 600, 105, t, spin=1.0 + 3 * old)
    mph(f, 540, 980, 190, t, ink=0.9, face=True, expr="sad" if old > 0.3 else "happy", grey=0.55 * old, wob=1.0 - 0.6 * old)
    if t > E["t_these"] - 0.1:
        put(f, pill("these cells don't live forever", 44, bg=(18, 16, 40), acc=(255, 120, 120)), CX, 1250, op=appear(t, E["t_these"] - 0.1), sc=0.92)
    put_char(f, 870, 1490, "think", "worried" if old > 0.2 else "think", t, 0.5, m=mouth(t), look=(-1, -1))
    return f


def shot_DI(t, n):
    s, e = SHOT["DI"]["start"], SHOT["DI"]["end"]
    f = dermis_bg(11, (200, 110, 220), (60, 20, 110))
    sparkles(f, t, 81, n=14, op=0.6, area=(60, 260, 1020, 1400))
    td = E["t_dies"] - 0.05
    if t < td:
        mph(f, 540, 900, 190, t, ink=0.9, face=True, expr="sad", grey=0.55, wob=0.4)
    else:
        q = (t - td)
        if q < 0.25:   # swell then burst
            mph(f, 540, 900, 190 * (1 + 0.25 * q / 0.25), t, ink=0.9, face=True, expr="sad", grey=0.6, op=1 - q / 0.25 * 0.6)
            disc(f, 540, 900, 260 * q / 0.25, (255, 255, 255), op=0.5 * (1 - q / 0.25))
        rng = np.random.default_rng(13)
        for i in range(14):   # membrane fragments
            a = rng.uniform(0, 6.28); sp = rng.uniform(220, 520)
            x, y = 540 + math.cos(a) * sp * eo(q / 1.2), 900 + math.sin(a) * sp * eo(q / 1.2) + 60 * q * q
            disc(f, x, y, rng.uniform(10, 22), (180, 150, 200), op=clamp(1 - q / 2.2))
        qs = clamp((t - E["t_spills"] + 0.3) / 1.6)
        for i in range(16):
            x, y = spill_pos(i, max(qs, clamp(q / 0.6) * 0.25))
            inkdot(f, x, y, 20 + (i % 4) * 3)
    put(f, small("when one dies…", 62), CX, 380, op=appear(t, s + 0.1) * (1 - clamp((t - E["t_spills"] + 0.15) / 0.2)))
    if t > E["t_spills"] - 0.15:
        put(f, small("it spills its ink", 62), CX, 380, op=appear(t, E["t_spills"] - 0.15))
    put_char(f, 870, 1490, "whisper", "whisper", t, 0.5, m=mouth(t), look=(-1, -1))
    return f


def shot_RC(t, n):
    s, e = SHOT["RC"]["start"], SHOT["RC"]["end"]
    f = big_set((0, 210, 170), (0, 70, 120), (255, 214, 0), 540, 900, 320, 91, t)
    tg = E["t_gobbles"] - 0.1
    arr = eo((t - (E["t_fresh"] - 0.25)) / 0.6)
    cx = lerp(-260, 540, arr)
    q = eio((t - tg) / 0.7)
    mph(f, cx, 920, 200, t, ink=0.05 + 0.85 * q, face=True, col=FRESH, mouth=0.9 if 0 < q < 0.95 else (chew(t, 12) * 0.5 if q >= 0.95 else 0.2),
        expr="happy")
    if q < 0.98:
        for i in range(16):
            x, y = spill_pos(i, 1.0)
            x2, y2 = lerp(x, cx + math.cos(i) * 80, q), lerp(y, 920 + math.sin(i) * 70, q)
            inkdot(f, x2, y2, (20 + (i % 4) * 3) * (1 - 0.5 * q), op=clamp((1 - q) * 3))
    if t < tg + 0.1:
        put(f, small("a fresh macrophage…", 62), CX, 380, op=appear(t, s + 0.1))
    tier(f, t, E["t_back"] - 0.12, "catch, release,", "RECAPTURE", 480, size=160, lo_size=56, gap=124, fill=(255, 236, 80))
    put_char(f, 200, 1490, "cheer" if q > 0.5 else "point", "laugh" if q > 0.5 else "talk", t, 0.52, m=mouth(t), look=(1, -1))
    return f


def shot_MC(t, n):
    s, e = SHOT["MC"]["start"], SHOT["MC"]["end"]
    f = big_set((120, 230, 120), (0, 110, 90), (255, 255, 255), 540, 1000, 300, 101, t)
    put(f, small("scientists saw this cycle", 60), CX, 360, op=appear(t, s + 0.1))
    # mini cycle: holding cell -> dying cell -> new cell (rotating arrows)
    cyc = [(380, 610, MPH, 0.0), (700, 610, MPH, 0.55), (540, 760, FRESH, 0.0)]
    hi = int(((t - s) * 1.6) % 3)
    for i, (x, y, col, g) in enumerate(cyc):
        k = popk(t, s + 0.2 + i * 0.15)
        if k > 0.02:
            mph(f, x, y, 48 * (1.15 if i == hi else 1.0), t, ink=0.9, face=False, col=col, grey=g, sc=k, phase=i)
    if t > s + 0.7:
        o = appear(t, s + 0.7)
        arrow_to(f, 440, 580, 640, 580, op=o)
        arrow_to(f, 720, 680, 600, 770, op=o)
        arrow_to(f, 480, 770, 360, 680, op=o)
    mouse(f, 410, 1100, t, 0.8)
    if t > E["t_mice"] - 0.1:
        put(f, pill("green ink on mouse tails", 40, bg=(18, 16, 40), acc=(0, 200, 90)), CX, 1325, op=appear(t, E["t_mice"] - 0.1), sc=0.9)
    if t > E["t_twenty"] - 0.1:
        k = popk(t, E["t_twenty"] - 0.1)
        put(f, pill("2018 MOUSE STUDY", 46, bg=(220, 20, 70), acc=(255, 255, 255)), CX, 1420, op=clamp(k * 3), sc=0.6 + 0.4 * k)
    put_char(f, 880, 1260, "magnify", "wow" if t > E["t_mice"] else "think", t, 0.48, m=mouth(t), look=(-1, 0), shadow=False)
    return f


def shot_LY(t, n):
    s, e = SHOT["LY"]["start"], SHOT["LY"]["end"]
    f = grad((40, 220, 230), (10, 60, 150), cx=0.5, cy=0.45)
    sparkles(f, t, 111, n=18, op=0.8, area=(60, 260, 1020, 1400))
    # tattooed skin patch (source), top-left
    cv2.rectangle(f, (110 + 8, 560 + 12), (370 + 8, 720 + 12), (0.05, 0.1, 0.2), -1, cv2.LINE_AA)
    cv2.rectangle(f, (110, 560), (370, 720), (0.96, 0.74, 0.62), -1, cv2.LINE_AA)
    sp = star_pts(240, 640, 60, 27).astype(np.int32)
    cv2.fillPoly(f, [sp], (0.06, 0.55, 0.62), cv2.LINE_AA); cv2.polylines(f, [sp], True, (0.05, 0.05, 0.12), 6, cv2.LINE_AA)
    # lymph vessel
    P = np.array([lymph_curve(u) for u in np.linspace(0, 1, 60)], np.int32)
    cv2.polylines(f, [P + [6, 10]], False, (0.03, 0.15, 0.25), 58, cv2.LINE_AA)
    cv2.polylines(f, [P], False, (0.80, 0.98, 0.90), 52, cv2.LINE_AA)
    cv2.polylines(f, [P - [6, 6]], False, (1.0, 1.0, 1.0), 8, cv2.LINE_AA)
    # lymph node bean
    nd = bean_mask(560, 1080, 230, 150, -0.15)
    cv2.fillPoly(f, [nd + [10, 16]], (0.03, 0.10, 0.20), cv2.LINE_AA)
    cv2.fillPoly(f, [nd], (0.62, 0.95, 0.55), cv2.LINE_AA)
    cv2.polylines(f, [nd], True, (0.10, 0.40, 0.20), 8, cv2.LINE_AA)
    tint_ = clamp((t - E["t_drift"]) / 1.6)
    rng = np.random.default_rng(15)
    for i in range(int(40 * tint_)):
        a = rng.uniform(0, 6.28); d = math.sqrt(rng.uniform(0, 1))
        inkdot(f, 560 + math.cos(a) * 170 * d, 1080 + math.sin(a) * 100 * d, 9)
    # tiny ink bits drifting along the vessel
    if t > E["t_bits"] - 0.3:
        for i in range(10):
            u = ((t - E["t_bits"] + 0.3) * 0.45 + i / 10) % 1.0
            x, y = lymph_curve(u)
            inkdot(f, x, y, 11)
    if t > E["t_bits"] - 0.15 and t < E["t_lymph"] - 0.1:
        put(f, small("tiny ink bits drift…", 60), CX, 380, op=appear(t, E["t_bits"] - 0.15))
    tier(f, t, E["t_lymph"] - 0.1, "all the way to your", "LYMPH NODES", 440, size=150, lo_size=56, gap=118, fill=(255, 236, 80))
    put_char(f, 860, 1490, "point" if t > E["t_drift"] else "stand", "wow" if t > E["t_lymph"] else "talk", t, 0.5, m=mouth(t), look=(-1, -1))
    return f


def shot_TP(t, n):
    s, e = SHOT["TP"]["start"], SHOT["TP"]["end"]
    f = big_set((0, 214, 160), (0, 64, 92), (255, 206, 0), 540, 1050, 300, 121, t)
    put(f, pill("TATTOO TIP", 40, bg=(0, 150, 100), acc=(255, 230, 90)), CX, 300, op=appear(t, s + 0.05))
    if t > E["t_choose"] - 0.2:
        k1 = popk(t, E["t_choose"] - 0.2, 0.38)
        put(f, tip_card2("Choose a licensed studio", "clean tools, trained artists", t > E["t_studio"] - 0.05), CX, 480, op=clamp(k1 * 3),
            sc=(0.7 + 0.3 * k1) * 0.9, rot=1.5 * (1 - k1))
    if t > E["t_let"] - 0.2:
        k2 = popk(t, E["t_let"] - 0.2, 0.38)
        put(f, tip_card2("Let it heal", "follow your aftercare advice", t > E["t_heal"] + 0.05, (40, 130, 255)), CX, 740, op=clamp(k2 * 3),
            sc=(0.7 + 0.3 * k2) * 0.9, rot=-1.5 * (1 - k2))
    if t < E["t_choose"] - 0.2:
        put(f, small("getting one?", 66), CX, 520, op=appear(t, E["t_getting"] - 0.15))
    mph(f, 760, 1230, 95, t, ink=0.8, face=True, mouth=chew(t, 6) * 0.3, phase=1.0)
    put_char(f, 360, 1480, "point" if t > E["t_choose"] else "hips", "talk" if mouth(t) > 0.3 else "smile", t, 0.75, m=mouth(t))
    return f


def loop_frame(t, lens_u, day=0.0):
    out = None
    for nt, w in ((True, 1.0 - day), (False, day)):
        if w <= 0.001:
            continue
        base, _ = arm_static(night=nt)
        f = base.copy()
        if lens_u > 0.001:
            cx = lerp(1400, 600, lens_u); cy = lerp(780, 990, lens_u)
            inner = zoom_at(macro_inner(t, night=nt), 1.0, 560, 990, cx, cy)
            f = lens_with_handle(f, inner, cx, cy, 245)
        out = f * w if out is None else out + f * w
    return out


def shot_LP(t, n):
    s, e = SHOT["LP"]["start"], SHOT["LP"]["end"]
    f = loop_frame(t, eo((t - s - 0.1) / 0.8))
    put(f, small("that tattoo you love…", 62), CX, 380, op=appear(t, E["t_tattoo9"] - 0.2))
    put_char(f, 200, 1480, "whisper", "whisper", t, 0.5, m=mouth(t), look=(1, -1))
    return f


def shot_LQ(t, n):
    s, e = SHOT["LQ"]["start"], SHOT["LQ"]["end"]
    out = clamp((t - (e - 0.55)) / 0.5)        # lens slides away at the very end -> matches the opening frame
    f = loop_frame(t, 1.0 - eio(out), day=eio(out))
    if out < 0.5:
        put(f, small("is being eaten…", 62), CX, 380, op=appear(t, s + 0.05) * (1 - out * 2))
    if t > E["t_right"] - 0.12:
        k = popk(t, E["t_right"] - 0.12)
        put(f, pill("RIGHT NOW", 46, bg=(220, 20, 70), acc=(255, 255, 255)), CX, 1330, op=clamp(k * 3) * (1 - out), sc=0.6 + 0.4 * k)
    put_char(f, 200, 1480, "whisper", "mischief", t, 0.5, m=mouth(t), look=(1, -1))
    return f


RENDER = {k: globals()[f"shot_{k}"] for k in SHOT}


def rs(sid, t, n):
    s = SHOT[sid]
    tt = min(max(t, s["start"]), s["end"] - 1e-3)
    return RENDER[sid](tt, n)


# ---------------- camera ----------------
PUNCH = [(E["t_eaten0"], 0.07, 0.3), (E["t_own"], 0.04, 0.3), (E["t_macro"], 0.06, 0.3), (E["t_holding"], 0.03, 0.3), (E["t_pushes"], 0.05, 0.3),
         (E["t_dermis"], 0.07, 0.3), (E["t_sheds"], 0.05, 0.3), (E["t_stays"], 0.05, 0.3), (E["t_invader"], 0.08, 0.35), (E["t_macro2"], 0.04, 0.3),
         (E["t_swallow"], 0.06, 0.3), (E["t_cant"], 0.05, 0.3), (E["t_hold"], 0.04, 0.3), (E["t_see"], 0.07, 0.35), (E["t_wait"], 0.06, 0.3),
         (E["t_forever"], 0.04, 0.3), (E["t_dies"], 0.08, 0.35), (E["t_gobbles"], 0.06, 0.3), (E["t_back"], 0.06, 0.3), (E["t_mice"], 0.05, 0.3),
         (E["t_twenty"], 0.04, 0.3), (E["t_lymph"], 0.07, 0.3), (E["t_studio"], 0.04, 0.3), (E["t_heal"], 0.04, 0.3), (E["t_eaten9"], 0.05, 0.3),
         (E["t_now"], 0.05, 0.3)]
SHAKE = [(E["t_eaten0"], 12, 0.35), (E["t_pushes"], 8, 0.3), (E["t_invader"], 18, 0.45), (E["t_dies"], 20, 0.45), (E["t_gobbles"], 12, 0.4),
         (E["t_wait"], 10, 0.35)]


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
