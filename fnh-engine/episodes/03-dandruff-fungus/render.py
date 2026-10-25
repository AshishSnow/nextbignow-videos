"""FreshNestHub ep03 — 'A fungus is eating your scalp' (Malassezia + dandruff). Fully procedural: NESSA host + 3D yeast, molecules, skin layers.
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


_FOL = {}


def follicle_block():
    if "blk" in _FOL:
        return _FOL["blk"]
    rng = np.random.default_rng(5)
    x0, x1, y0, y1 = 150, 870, 560, 1400
    img = np.zeros((H, W, 3), np.float32); al = np.zeros((H, W), np.float32)
    # top face (skin texture in perspective)
    src = SKIN[600:1100, 300:1300].copy()
    sh_, sw_ = src.shape[:2]
    dst = np.float32([[x0, y0], [x1, y0], [x1 + 70, y0 - 110], [x0 + 70, y0 - 110]])
    Mp = cv2.getPerspectiveTransform(np.float32([[0, sh_], [sw_, sh_], [sw_, 0], [0, 0]]), dst)
    top = cv2.warpPerspective(src, Mp, (W, H))
    tm = cv2.warpPerspective(np.ones((sh_, sw_), np.float32), Mp, (W, H))
    img = img * (1 - tm[..., None]) + top * 1.05 * tm[..., None]; al = np.maximum(al, tm)
    # right side face
    side = np.array([[x1, y0], [x1 + 70, y0 - 110], [x1 + 70, y1 - 110], [x1, y1]], np.int32)
    sm = np.zeros((H, W), np.uint8); cv2.fillPoly(sm, [side], 1); sm = sm.astype(np.float32)
    yy = _yy
    sc = np.where(yy < y0 + 65, 0, np.where(yy < 1150, 1, 2))
    cols = [C((210, 140, 120)), C((205, 112, 118)), C((220, 180, 90))]
    sidec = np.select([(sc == 0)[..., None], (sc == 1)[..., None], (sc == 2)[..., None]], [np.broadcast_to(c, (H, W, 3)) for c in cols]) * 0.62
    img = img * (1 - sm[..., None]) + sidec * sm[..., None]; al = np.maximum(al, sm)
    # front face layers
    fm = np.zeros((H, W), np.float32); fm[y0:y1, x0:x1] = 1
    epi = np.broadcast_to(C((238, 172, 150)), (H, W, 3))
    der = np.broadcast_to(C((236, 128, 136)), (H, W, 3))
    hyp = np.broadcast_to(C((252, 212, 110)), (H, W, 3))
    front = np.select([(yy < y0 + 65)[..., None].repeat(3, 2), (yy < 1150)[..., None].repeat(3, 2)], [epi, der], hyp).astype(np.float32)
    nz = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 3) * 0.05
    front = front * (1 + nz[..., None])
    can = (np.clip(front, 0, 1) * 255).astype(np.uint8).copy()
    # basal line + collagen fibres
    cv2.line(can, (x0, y0 + 64), (x1, y0 + 64), (190, 92, 98), 5, cv2.LINE_AA)
    for i in range(170):
        yb = rng.uniform(y0 + 90, 1140); xb = rng.uniform(x0 - 40, x1)
        pts = [(int(xb + j * 14), int(yb + 7 * math.sin(j * 0.7 + i))) for j in range(rng.integers(6, 14))]
        cv2.polylines(can, [np.array(pts, np.int32)], False, (250, 170, 172), 2, cv2.LINE_AA)
    # fat lobules
    for i in range(70):
        cx_, cy_ = rng.uniform(x0, x1), rng.uniform(1165, y1 - 10); r = rng.uniform(24, 44)
        cv2.circle(can, (int(cx_), int(cy_)), int(r), (255, 226, 132), -1, cv2.LINE_AA)
        cv2.circle(can, (int(cx_), int(cy_)), int(r), (222, 160, 70), 3, cv2.LINE_AA)
        cv2.circle(can, (int(cx_ - r * 0.3), int(cy_ - r * 0.3)), int(r * 0.28), (255, 246, 210), -1, cv2.LINE_AA)
    can[:, :x0] = 0; can[:, x1:] = 0; can[:y0] = 0; can[y1:] = 0
    # follicle
    def fx(y):
        return 510 + (y - y0) * 0.10
    lum = np.zeros((H, W), np.float32)
    for y in range(y0 - 2, 1185):
        w_ = 52 - (y - y0) / 620 * 16
        cv2.line(can, (int(fx(y) - w_ - 18), y), (int(fx(y) + w_ + 18), y), (255, 196, 196), 1)
        cv2.line(can, (int(fx(y) - w_), y), (int(fx(y) + w_), y), (int(120 - (y - y0) * 0.06), 34, 46), 1)
        lum[y, int(fx(y) - w_ + 4):int(fx(y) + w_ - 4)] = 1
    cv2.circle(can, (int(fx(1185)), 1200), 62, (196, 70, 92), -1, cv2.LINE_AA)
    cv2.circle(can, (int(fx(1185)), 1200), 62, (120, 30, 50), 4, cv2.LINE_AA)
    cv2.circle(can, (int(fx(1185)) - 18, 1182), 18, (236, 130, 150), -1, cv2.LINE_AA)
    # sebaceous gland (golden lobes) on the right
    gx, gy = int(fx(800)) + 95, 830
    cv2.line(can, (int(fx(760)) + 40, 768), (gx - 30, 805), (236, 170, 60), 18, cv2.LINE_AA)
    for (dx, dy, r) in ((0, 0, 52), (44, -34, 40), (50, 40, 42), (-6, 58, 36), (8, -60, 34)):
        cv2.circle(can, (gx + dx, gy + dy), r, (232, 150, 30), -1, cv2.LINE_AA)
        cv2.circle(can, (gx + dx, gy + dy), r - 6, (255, 204, 70), -1, cv2.LINE_AA)
        cv2.circle(can, (gx + dx - r // 3, gy + dy - r // 3), r // 3, (255, 240, 180), -1, cv2.LINE_AA)
    frontf = can.astype(np.float32) / 255
    # front lighting: brighter top-left, darker bottom
    lit = np.clip(1.08 - 0.22 * (yy - y0) / (y1 - y0) - 0.06 * (_xx - x0) / (x1 - x0), 0.7, 1.1)[..., None]
    img = img * (1 - fm[..., None]) + frontf * lit * fm[..., None]; al = np.maximum(al, fm)
    cv2.line(img, (x0, y0), (x1, y0), (1, 0.92, 0.88), 3, cv2.LINE_AA)
    # follicle opening on the top face + hair shaft
    cv2.ellipse(img, (int(fx(y0)) + 32, y0 - 52), (46, 18), 0, 0, 360, (0.25, 0.08, 0.08), -1, cv2.LINE_AA)
    pts = [(int(fx(y) - 14), y) for y in range(1150, y0 - 50, -20)] + [(int(fx(y0) + 30 - (i ** 1.3) * 3), y0 - 52 - i * 22) for i in range(1, 11)]
    cv2.polylines(img, [np.array(pts, np.int32)], False, (0.30, 0.17, 0.10), 16, cv2.LINE_AA)
    cv2.polylines(img, [np.array(pts, np.int32) - [4, 0]], False, (0.52, 0.34, 0.22), 4, cv2.LINE_AA)
    al[:y0 - 300] = al[:y0 - 300]
    hm = np.zeros((H, W), np.uint8); cv2.polylines(hm, [np.array(pts, np.int32)], False, 1, 16, cv2.LINE_AA)
    al = np.maximum(al, hm.astype(np.float32))
    _FOL["blk"] = (img.astype(np.float32), al, lum, fx, (gx, gy))
    return _FOL["blk"]




# ================= ep03 assets: yeast, scalp forest, molecules, skin layers =================
YCOL = (1.0, 0.93, 0.74)       # cream yeast
_YS = {}


def yeast_img(r, mouth=0.0, face=True, expr="happy", col=YCOL, bud=True):
    """3D shaded Malassezia yeast cell (round + small bud). returns PIL RGBA centred on the main cell"""
    r = int(max(6, r)); mq = round(mouth * 4) / 4
    key = (r, mq, face, expr, col, bud)
    if key in _YS:
        return _YS[key]
    if len(_YS) > 400:
        _YS.clear()
    k = 2
    R = r * k
    n = int(R * 3.2)
    can = np.zeros((n, n, 3), np.float32); al = np.zeros((n, n), np.float32)
    c = n / 2
    if bud:
        stamp(can, al, sphere(R * 0.46, tuple(min(1, v * 1.02) for v in col), rim=0.5, spec=0.6), c + R * 0.78, c - R * 0.74)
        # neck
        stamp(can, al, sphere(R * 0.30, col, rim=0.4, spec=0.2), c + R * 0.55, c - R * 0.52)
    stamp(can, al, sphere(R, col, rim=0.55, spec=0.75), c, c)
    rgb = can
    rng = np.random.default_rng(r)
    # cell-wall speckles / texture
    for i in range(int(18 + r * 0.25)):
        a = rng.uniform(0, 6.28); d = rng.uniform(0, 0.85) * R
        x, y = c + math.cos(a) * d, c + math.sin(a) * d
        rr = rng.uniform(0.03, 0.08) * R
        cv2.circle(rgb, (int(x), int(y)), max(1, int(rr)), (col[0] * 0.86, col[1] * 0.80, col[2] * 0.70), -1, cv2.LINE_AA)
    # inner vacuole hint
    cv2.ellipse(rgb, (int(c + R * 0.18), int(c + R * 0.22)), (int(R * 0.30), int(R * 0.22)), 20, 0, 360,
                (col[0] * 0.93, col[1] * 0.88, col[2] * 0.80), -1, cv2.LINE_AA)
    rgb *= al[..., None] > 0
    im = Image.fromarray((np.dstack([np.clip(rgb, 0, 1), al]) * 255).astype(np.uint8), "RGBA")
    if face:
        d = ImageDraw.Draw(im)
        ex, ey, er = R * 0.30, c - R * 0.12, R * 0.17
        for s in (-1, 1):
            if expr == "sad":
                d.arc([c + s * ex - er, ey - er * 0.4, c + s * ex + er, ey + er * 1.2], 200, 340, fill=(20, 14, 18, 255), width=max(2, int(R * 0.05)))
            d.ellipse([c + s * ex - er, ey - er * 1.15, c + s * ex + er, ey + er * 1.15], fill=(255, 255, 255, 255), outline=(20, 14, 18, 255),
                      width=max(2, int(R * 0.035)))
            pr = er * 0.55
            d.ellipse([c + s * ex - pr + er * 0.15, ey - pr + er * 0.1, c + s * ex + pr + er * 0.15, ey + pr + er * 0.1], fill=(20, 14, 18, 255))
            d.ellipse([c + s * ex - pr * 0.2, ey - pr * 0.6, c + s * ex + pr * 0.25, ey - pr * 0.15], fill=(255, 255, 255, 255))
        my = c + R * 0.32
        if expr == "sad":
            d.arc([c - R * 0.22, my, c + R * 0.22, my + R * 0.26], 200, 340, fill=(20, 14, 18, 255), width=max(2, int(R * 0.06)))
        elif mq > 0.05:
            h = R * (0.08 + 0.30 * mq)
            d.ellipse([c - R * 0.24, my - h * 0.4, c + R * 0.24, my + h], fill=(120, 20, 40, 255), outline=(20, 14, 18, 255), width=max(2, int(R * 0.04)))
            d.ellipse([c - R * 0.12, my + h * 0.35, c + R * 0.12, my + h * 0.95], fill=(240, 90, 110, 255))
        else:
            d.arc([c - R * 0.26, my - R * 0.18, c + R * 0.26, my + R * 0.2], 20, 160, fill=(20, 14, 18, 255), width=max(2, int(R * 0.06)))
        # cheeks
        for s in (-1, 1):
            d.ellipse([c + s * R * 0.50 - R * 0.09, my - R * 0.08, c + s * R * 0.50 + R * 0.09, my + R * 0.02], fill=(255, 150, 160, 150))
    # soft drop shadow
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sa = Image.fromarray((al * 110).astype(np.uint8))
    sh.putalpha(sa)
    sh = sh.filter(ImageFilter.GaussianBlur(R * 0.08))
    base = Image.new("RGBA", im.size, (0, 0, 0, 0))
    base.alpha_composite(sh, (int(R * 0.06), int(R * 0.12)))
    base.alpha_composite(im)
    out = base.resize((n // k, n // k), Image.LANCZOS)
    _YS[key] = out
    return out


def yeast(f, x, y, r, t=0.0, mouth=0.0, face=True, expr="happy", op=1.0, rot=0.0, bob=True, phase=0.0):
    sq = 1.0 + (0.035 * math.sin(t * 5 + phase) if bob else 0)
    im = yeast_img(r * sq, mouth, face, expr)
    put(f, im, x, y + (6 * math.sin(t * 3 + phase) if bob else 0), op=op, rot=rot)


def chew(t, rate=7.0):
    return 0.5 + 0.5 * math.sin(t * rate)


def flake(f, x, y, s, rot=0.0, seed=0, op=1.0, col=(0.97, 0.96, 0.92)):
    r = np.random.default_rng(seed)
    nv = 7
    pts = []
    for i in range(nv):
        a = i / nv * 2 * math.pi + rot
        d = s * r.uniform(0.55, 1.0)
        pts.append((x + math.cos(a) * d, y + math.sin(a) * d * 0.75))
    p = np.array(pts, np.int32)
    if op >= 0.99:
        cv2.fillPoly(f, [p + 3], (0.25, 0.22, 0.25), cv2.LINE_AA) if s > 14 else None
        cv2.fillPoly(f, [p], col, cv2.LINE_AA)
        cv2.polylines(f, [p], True, (0.80, 0.78, 0.74), max(1, int(s * 0.08)), cv2.LINE_AA)
    else:
        x0, y0 = int(max(0, x - s - 6)), int(max(0, y - s - 6)); x1, y1 = int(min(W, x + s + 6)), int(min(H, y + s + 6))
        if x1 <= x0 or y1 <= y0:
            return
        m = np.zeros((y1 - y0, x1 - x0), np.float32)
        cv2.fillPoly(m, [p - [x0, y0]], 1.0, cv2.LINE_AA)
        m = m[..., None] * op
        f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * (1 - m) + np.array(col, np.float32) * m


# ---- scalp forest (macro of scalp skin with hair shafts, oil and yeast) ----
SCALP, SPORES = gen_skin(1400, 2300, 17, "warm")
_SF = {}


def scalp_static(ox=150, oy=180):
    key = (ox, oy)
    if key in _SF:
        return _SF[key]
    base = skin_view(ox, oy, 1.0, SCALP).copy()
    base = base * np.array([1.02, 0.95, 0.92], np.float32)
    rng = np.random.default_rng(9)
    P = [p for p in SPORES if ox + 40 < p[0] < ox + W - 40 and oy + 200 < p[1] < oy + H - 120]
    rng.shuffle(P)
    hairs = []
    k = 2
    im = Image.new("RGBA", (W * k, H * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    shad = Image.new("RGBA", (W * k, H * k), (0, 0, 0, 0))
    ds = ImageDraw.Draw(shad)
    chosen = []
    for p in P:
        x, y = p[0] - ox, p[1] - oy
        if all((x - a) ** 2 + (y - b) ** 2 > 210 ** 2 for a, b in chosen):
            chosen.append((x, y))
        if len(chosen) >= 9:
            break
    for j, (x, y) in enumerate(chosen):
        ang = -math.pi / 2 - 0.55 + rng.uniform(-0.25, 0.25)
        L = rng.uniform(1300, 1900); wd = rng.uniform(26, 34); bend = rng.uniform(-0.25, 0.25)
        pts = []
        for i in range(30):
            u = i / 29
            a = ang + bend * u
            pts.append((x + math.cos(a) * L * u, y + math.sin(a) * L * u))
        hairs.append(pts)
        ds.line([((px + 18) * k, (py + 26) * k) for px, py in pts], fill=(40, 10, 0, 110), width=int(wd * k))
        # follicle opening
        d.ellipse([(x - wd * 0.95) * k, (y - wd * 0.55) * k, (x + wd * 0.95) * k, (y + wd * 0.55) * k], fill=(110, 46, 36, 255))
    im.alpha_composite(shad.filter(ImageFilter.GaussianBlur(14 * k)))
    d = ImageDraw.Draw(im)
    for pts in hairs:
        wd = 30
        d.line([(px * k, py * k) for px, py in pts], fill=(46, 26, 16, 255), width=int(wd * k), joint="curve")
        d.line([((px - 7) * k, py * k) for px, py in pts], fill=(98, 60, 36, 255), width=int(wd * 0.35 * k), joint="curve")
        d.line([((px - 10) * k, py * k) for px, py in pts], fill=(170, 120, 80, 200), width=int(4 * k), joint="curve")
        # cuticle scales
        for i in range(2, 29):
            px, py = pts[i]
            d.arc([(px - wd / 2) * k, (py - 10) * k, (px + wd / 2) * k, (py + 10) * k], 200, 340, fill=(70, 40, 24, 200), width=2 * k)
    im = im.resize((W, H), Image.LANCZOS)
    rgb, a = to_np(im)
    base = base * (1 - a[..., None]) + rgb * a[..., None]
    # oil sheen droplets near hair bases
    drops = []
    for (x, y) in chosen:
        for i in range(3):
            drops.append((x + rng.uniform(-90, 90), y + rng.uniform(20, 110), rng.uniform(9, 20)))
    for (x, y, r_) in drops:
        spr = sphere(r_, (1.0, 0.80, 0.25), rim=0.3, spec=1.0)
        n_ = spr[1].shape[0]
        over(base, spr[0], spr[1] * 0.85, x - n_ / 2, y - n_ / 2)
    # static flakes stuck to scalp
    for i in range(16):
        x, y = rng.uniform(80, 1000), rng.uniform(300, 1700)
        flake(base, x, y, rng.uniform(14, 34), rng.uniform(0, 6), seed=i, op=0.8)
    _SF[key] = (base.astype(np.float32), chosen)
    return _SF[key]


def scalp_scene(t, munch=True, big=None, ox=150, oy=180):
    base, roots = scalp_static(ox, oy)
    f = base.copy()
    # colony of small yeast around the hair roots
    rng = np.random.default_rng(3)
    for j, (x, y) in enumerate(roots):
        for i in range(5):
            a = rng.uniform(0, 6.28); d = rng.uniform(40, 120)
            yeast(f, x + math.cos(a) * d, y + 40 + math.sin(a) * d * 0.6, rng.uniform(16, 28), t, face=False, phase=i + j, bob=True)
    if big:
        for (x, y, r, ph) in big:
            yeast(f, x, y, r, t, mouth=chew(t + ph, 9) if munch else 0, face=True, phase=ph)
    return f


# ---- molecules ----
GOLD = (1.0, 0.78, 0.18)
HEADC = (1.0, 0.36, 0.52)
OXY = (0.95, 0.15, 0.20)


def ball(f, x, y, r, col, op=1.0):
    spr = sphere(r, col, rim=0.45, spec=0.8)
    n_ = spr[1].shape[0]
    over(f, spr[0], spr[1], x - n_ / 2, y - n_ / 2, op)


def chain_pts(x, y, ang, n=9, step=34, kink=None, kink_ang=0.55):
    pts = []
    a = ang
    for i in range(n):
        if kink is not None and i == kink:
            a += kink_ang
        zz = (i % 2) * 2 - 1
        px = x + math.cos(a) * step * i - math.sin(a) * 9 * zz
        py = y + math.sin(a) * step * i + math.cos(a) * 9 * zz
        pts.append((px, py))
    return pts


def draw_chain(f, pts, r=17, col=GOLD, op=1.0, head=True):
    for i in range(len(pts) - 1):
        cv2.line(f, (int(pts[i][0]), int(pts[i][1])), (int(pts[i + 1][0]), int(pts[i + 1][1])), (0.55, 0.38, 0.05), 7, cv2.LINE_AA)
    for i, (px, py) in enumerate(reversed(pts)):
        ball(f, px, py, r, col, op)
    if head:
        ball(f, pts[0][0], pts[0][1], r * 1.25, OXY, op)


def fatty(f, x, y, ang, kinked=False, sc=1.0, op=1.0):
    pts = chain_pts(x, y, ang, 9, 34 * sc, kink=4 if kinked else None)
    draw_chain(f, pts, 17 * sc, GOLD if not kinked else (1.0, 0.62, 0.12), op)
    return pts


def trig(f, x, y, sep=0.0, op=1.0, sc=1.0, jit=0.0, t=0.0):
    """triglyceride: pink 3-ball glycerol head at (x,y) + 3 golden tails to the right; sep separates tails"""
    hs = []
    for i in range(3):
        hy = y + (i - 1) * 80 * sc
        hs.append((x, hy))
    for i, (hx, hy) in enumerate(hs):
        dx = sep * (60 + 40 * i) * sc
        dy = sep * (i - 1) * 90 * sc
        a = sep * (i - 1) * 0.22 + 0.02 * math.sin(t * 3 + i) * jit
        pts = chain_pts(hx + 50 * sc + dx, hy + dy, a, 9, 34 * sc, kink=4 if i == 1 else None, kink_ang=0.5)
        if sep < 0.05:
            cv2.line(f, (int(hx), int(hy)), (int(pts[0][0]), int(pts[0][1])), (0.6, 0.15, 0.25), 8, cv2.LINE_AA)
        draw_chain(f, pts, 17 * sc, GOLD if i != 1 else (1.0, 0.62, 0.12), op, head=sep > 0.05)
    cv2.line(f, (int(hs[0][0] - sep * 120 * sc), int(hs[0][1])), (int(hs[2][0] - sep * 120 * sc), int(hs[2][1])), (0.6, 0.15, 0.25), 9, cv2.LINE_AA)
    for (hx, hy) in hs:
        ball(f, hx - sep * 120 * sc, hy, 26 * sc, HEADC, op)
    return hs


def enzyme_img(r, bite):
    key = ("enz", int(r), round(bite * 4) / 4)
    if key in _TX:
        return _TX[key]
    k = 3
    n = int(r * 2.6) * k
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    can = np.zeros((n, n, 3), np.float32); al = np.zeros((n, n), np.float32)
    stamp(can, al, sphere(r * k, (0.62, 0.30, 1.0), rim=0.5, spec=0.8), n / 2, n / 2)
    im = Image.fromarray((np.dstack([np.clip(can, 0, 1), al]) * 255).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(im)
    op_ = 18 + 34 * key[2]
    d.pieslice([n / 2 - r * k * 1.1, n / 2 - r * k * 1.1, n / 2 + r * k * 1.1, n / 2 + r * k * 1.1], -op_, op_, fill=(0, 0, 0, 0))
    # cut out wedge -> set alpha 0 there
    a = np.array(im)
    yy, xx = np.mgrid[0:n, 0:n]
    ang = np.degrees(np.arctan2(yy - n / 2, xx - n / 2))
    a[(np.abs(ang) < op_) & (np.hypot(xx - n / 2, yy - n / 2) < r * k * 1.2)] = 0
    im = Image.fromarray(a, "RGBA")
    d = ImageDraw.Draw(im)
    d.ellipse([n / 2 - r * k * 0.15, n / 2 - r * k * 0.62, n / 2 + r * k * 0.15, n / 2 - r * k * 0.32], fill=(20, 10, 30, 255))
    im = im.resize((n // k, n // k), Image.LANCZOS)
    _TX[key] = im
    return im


def oil_world(t, seed=5):
    f = grad((255, 196, 40), (150, 52, 0), cx=0.5, cy=0.42)
    rng = np.random.default_rng(seed)
    for i in range(22):
        x, y = rng.uniform(60, 1020), rng.uniform(260, 1660)
        r = rng.uniform(18, 70)
        y2 = y - ((t * rng.uniform(10, 30)) % 200)
        disc(f, x, y2, r, (255, 232, 140), op=0.22)
        disc(f, x - r * 0.3, y2 - r * 0.3, r * 0.25, (255, 255, 230), op=0.25)
    return f


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


def globe(t, flakes_on=True, head_expr="worried", head_t=None):
    """opening set: a big snow globe holding Nessa's head, dandruff flakes swirling like snow"""
    f = grad((255, 70, 160), (60, 10, 120), cx=0.5, cy=0.42)
    sparkles(f, t, 3, n=30, op=1.0, size=8)
    gx, gy, gr = 540, 820, 360
    # base
    bp = np.array([(gx - 300, gy + gr - 60), (gx + 300, gy + gr - 60), (gx + 250, gy + gr + 170), (gx - 250, gy + gr + 170)], np.int32)
    cv2.fillPoly(f, [bp + [10, 16]], (0.10, 0.02, 0.10), cv2.LINE_AA)
    cv2.fillPoly(f, [bp], C((255, 196, 40)).tolist(), cv2.LINE_AA)
    cv2.rectangle(f, (gx - 270, gy + gr + 20), (gx + 270, gy + gr + 46), C((255, 236, 140)).tolist(), -1, cv2.LINE_AA)
    cv2.polylines(f, [bp], True, (0.45, 0.25, 0.0), 6, cv2.LINE_AA)
    # glass interior: Nessa's head + dark sweater shoulders inside the globe
    d = np.sqrt((_xx - gx) ** 2 + (_yy - gy) ** 2)
    inside = np.clip(gr - d + 0.5, 0, 1)[..., None]
    inner = grad((120, 220, 255), (30, 90, 200), cx=0.5, cy=0.40)
    cv2.ellipse(inner, (gx, gy + gr + 40), (260, 200), 0, 180, 360, (0.10, 0.10, 0.22), -1, cv2.LINE_AA)
    put_head(inner, gx, gy + 20, head_expr, t if head_t is None else head_t, 2.3, mouth(t), look=(0, -1))
    f = f * (1 - inside) + inner * inside
    if flakes_on:
        rng = np.random.default_rng(11)
        for i in range(46):
            a0 = rng.uniform(0, 6.28); rr = rng.uniform(40, gr - 30); sp = rng.uniform(0.5, 1.4)
            a = a0 + t * sp * 0.8
            x, y = gx + math.cos(a) * rr * 0.9, gy + math.sin(a) * rr * 0.75 + 40 * math.sin(t * 2 + i)
            if (x - gx) ** 2 + (y - gy) ** 2 < (gr - 20) ** 2:
                flake(f, x, y, rng.uniform(6, 13), a, seed=i)
    # glass rim + glare
    rim = np.exp(-((d - gr) / 8) ** 2)[..., None]
    f = f * (1 - rim * 0.9) + rim * 0.9
    gl = (np.exp(-((d - gr * 0.84) / (gr * 0.05)) ** 2) * np.clip(-(_xx - gx + _yy - gy) / (gr * 1.1), 0, 1))[..., None] * 0.5
    f = np.clip(f + gl, 0, 1)
    return f


# ================= shots =================
def shot_H1(t, n):
    dv0 = E["t_eating"] - 0.05
    p = eio((t - dv0) / 0.6)
    big = [(520, 1000, 120, 0.0), (300, 720, 70, 1.5), (780, 640, 80, 2.7)]
    if p >= 0.999:
        f = scalp_scene(t, True, big)
        f = zoom_at(f, 1.0 + 0.03 * (t - dv0), 540, 900)
    else:
        out = globe(t)
        if p > 0:
            z = 1 + 6.0 * p ** 1.7
            out = zoom_at(out, z, 540, 640)
            inner = scalp_scene(t, True, big)
            r = 1300 * p ** 1.3
            m = np.clip(r - np.sqrt((_xx - 540) ** 2 + (_yy - 900) ** 2) + 0.5, 0, 1)[..., None]
            f = out * (1 - m) + inner * m
        else:
            f = out
    if t < E["t_scalp"] - 0.1:
        k = appear(t, 0.08, 0.3)
        put(f, small("do you know", 64), CX, 330, op=k)
    tier(f, t, E["t_scalp"] - 0.08, "a fungus is eating", "YOUR SCALP", 1270, size=170, lo_size=58, gap=135, fill=(255, 236, 80))
    if t > E["t_right0"] - 0.08:
        k = popk(t, E["t_right0"] - 0.08)
        put(f, pill("RIGHT NOW", 46, bg=(220, 20, 70), acc=(255, 255, 255)), CX, 1420, op=clamp(k * 3), sc=0.6 + 0.4 * k)
    return f


STY = ["guy", "girl", "nessa", "bald", "girl2"]


def shot_NM(t, n):
    s = SHOT["NM"]["start"]
    f = big_set((40, 210, 190), (0, 50, 110), (255, 206, 0), 540, 800, 280, 21, t)
    k = popk(t, s + 0.05, 0.45)
    if k > 0.02:
        yeast(f, 540, 800, 200 * k, t, mouth=0.0, face=True, phase=0.3)
    tier(f, t, E["t_called"] - 0.05, "a yeast called", "MALASSEZIA", 430, size=150, lo_size=56, gap=118, fill=(255, 236, 80))
    if t > E["t_yeast"] - 0.1:
        put(f, pill("a tiny fungus", 40, acc=(0, 220, 170)), CX, 1110, op=appear(t, E["t_yeast"] - 0.1), sc=0.9)
    # crowd of adults, each with yeast on the head
    if t > E["t_most"] - 0.25:
        for i, x in enumerate((180, 360, 540, 720, 880)):
            q = popk(t, E["t_most"] - 0.25 + i * 0.06, 0.3)
            if q < 0.02:
                continue
            st = STY[i]
            put_char(f, x, 1440, "cheer" if (st == "nessa" and t > E["t_adults"]) else "stand", "wow" if t > E["t_adults"] else "smile", t + i, 0.38,
                     style=st, sc=q, shadow=False)
            if t > E["t_adults"] - 0.1 + i * 0.05:
                qq = popk(t, E["t_adults"] - 0.1 + i * 0.05, 0.3)
                for jj, (dx, dy) in enumerate(((-14, -175), (12, -182), (0, -192))):
                    yeast(f, x + dx, 1440 + dy * q, 9 * qq + 0.1, t, face=False, phase=jj + i)
    return f


def shot_FT(t, n):
    s = SHOT["FT"]["start"]
    f = big_set((255, 150, 60), (190, 30, 60), (255, 230, 90), 540, 860, 300, 31, t)
    sad = t > E["t_fat"] - 0.1
    yeast(f, 400, 900, 175, t, face=True, expr="sad" if sad else "happy", phase=0.5)
    # oil drop icon with a big X
    k = popk(t, s + 0.15, 0.35)
    if k > 0.02:
        cx_, cy_ = 760, 640
        sz = 85 * k
        pts = np.array([(cx_, cy_ - sz * 1.5)] + [(cx_ + math.cos(a) * sz, cy_ + math.sin(a) * sz) for a in np.linspace(-0.3, math.pi + 0.3, 24)],
                       np.int32)
        cv2.fillPoly(f, [pts + [6, 10]], (0.3, 0.1, 0.0), cv2.LINE_AA)
        cv2.fillPoly(f, [pts], (1.0, 0.80, 0.18), cv2.LINE_AA)
        cv2.polylines(f, [pts], True, (0.45, 0.25, 0.0), 6, cv2.LINE_AA)
        disc(f, cx_ - sz * 0.35, cy_ - sz * 0.1, sz * 0.18, (255, 250, 220), op=0.85)
    if t > E["t_fat"] - 0.1:
        q = eo((t - E["t_fat"] + 0.1) / 0.25)
        cx_, cy_ = 760, 640
        for s_ in (-1, 1):
            cv2.line(f, (int(cx_ - 110 * q), int(cy_ - 110 * q * s_)), (int(cx_ + 110 * q), int(cy_ + 110 * q * s_)), (0.1, 0.0, 0.0), 40, cv2.LINE_AA)
            cv2.line(f, (int(cx_ - 110 * q), int(cy_ - 110 * q * s_)), (int(cx_ + 110 * q), int(cy_ + 110 * q * s_)), (0.95, 0.1, 0.15), 28, cv2.LINE_AA)
    put(f, small("it can't make its own fat", 60), CX, 380, op=appear(t, E["t_cant"] - 0.2))
    put_char(f, 790, 1450, "shrug" if sad else "think", "worried" if sad else "think", t, 0.62, m=mouth(t) * 0, look=(-1, 0))
    return f


def shot_SB(t, n):
    s, e = SHOT["SB"]["start"], SHOT["SB"]["end"]
    f = grad((255, 210, 70), (232, 90, 40), cx=0.5, cy=0.40)
    img, al, lum, fx, (gx, gy) = follicle_block()
    sh = cv2.GaussianBlur(al, (0, 0), 22)
    f *= (1 - 0.35 * np.roll(np.roll(sh, 26, 0), 18, 1))[..., None]
    f = f * (1 - al[..., None]) + img * al[..., None]
    # oil flowing from the gland up the follicle onto the surface
    for i in range(12):
        q = ((t - s) * 0.6 + i / 12) % 1.0
        if q < 0.3:
            u = q / 0.3
            x, y = lerp(gx - 30, fx(770) + 10, u), lerp(812, 770, u)
        elif q < 0.8:
            u = (q - 0.3) / 0.5
            y = lerp(770, 560, u); x = fx(y) + 14 * math.sin(i + y * 0.05)
        else:
            u = (q - 0.8) / 0.2
            x, y = fx(560) + 32 + (i % 3 - 1) * 160 * u, 508 - 10 * u
        disc(f, x, y, 11, (255, 214, 70), op=0.95)
        disc(f, x - 3, y - 3, 4, (255, 250, 220), op=0.9)
    # yeast on the surface, feeding
    for j, (x, y, r) in enumerate(((370, 500, 46), (560, 470, 40), (760, 490, 50))):
        yeast(f, x, y, r, t, mouth=chew(t + j, 10), face=True, phase=j)
    if t > E["t_oil"] - 0.2:
        k2 = appear(t, E["t_oil"] - 0.2, 0.3)
        arrow_on = k2
    else:
        k2 = 0
    f = zoom_at(f, 0.78 + 0.03 * eio((t - s) / (e - s)), 540, 925, 540, 1090)
    if k2 > 0:
        put(f, pill("oil gland", 44, bg=(150, 80, 0), acc=(255, 230, 90)), CX, 615, op=k2)
        zz = 0.78 + 0.03 * eio((t - s) / (e - s))
        arrow_to(f, 640, 640, 540 + (gx + 40 - 540) * zz, 1090 + (gy - 925) * zz, op=k2)
    tier(f, t, E["t_sebum"] - 0.08, "your scalp's natural oil", "SEBUM", 470, size=170, lo_size=54, gap=128, fill=(255, 226, 60))
    return f


ENZ_TARGETS = [(390, 650), (390, 730), (390, 810)]


def molecule_scene(t, sep=0.0, enz=0.0, bite=0.0, yeast_xy=(330, 1300), tri_xy=(240, 760)):
    f = oil_world(t)
    hs = trig(f, tri_xy[0], tri_xy[1], sep=sep, jit=1.0, t=t, sc=1.35)
    return f, hs


def shot_EN(t, n):
    s = SHOT["EN"]["start"]
    f, hs = molecule_scene(t)
    step_pill(f, t, s + 0.1, 1, "CHOP THE OIL", (255, 64, 140))
    put(f, pill("oil molecule", 40, bg=(120, 50, 0), acc=(255, 230, 90)), CX, 470, op=appear(t, s + 0.3))
    # yeast at the bottom launching enzymes
    yx, yy = 250, 1290
    yeast(f, yx, yy, 150, t, mouth=0.6 if t > E["t_sends"] else 0.0, face=True)
    if t > E["t_sends"] - 0.1:
        for i in range(3):
            q = eio((t - E["t_sends"] + 0.1 - i * 0.12) / 0.75)
            if q <= 0:
                continue
            tx_, ty_ = hs[i][0] + 34, hs[i][1]
            x = lerp(yx + 40, tx_ + 46, q); y = lerp(yy - 80, ty_, q) - 120 * math.sin(math.pi * q)
            put(f, enzyme_img(46, chew(t + i, 12)), x, y, rot=180)
    if t > E["t_enzymes"] - 0.1:
        put(f, pill("enzymes", 44, bg=(80, 20, 140), acc=(200, 140, 255)), CX, 1080, op=appear(t, E["t_enzymes"] - 0.1))
    put_head(f, 820, 1360, "wow", t, 0.85, mouth(t), look=(-1, -1))
    return f


def shot_CH(t, n):
    s, e = SHOT["CH"]["start"], SHOT["CH"]["end"]
    tc = E["t_chop"] - 0.04
    sep = eo((t - tc) / 0.7) if t > tc else 0.0
    f, hs = molecule_scene(t, sep=sep)
    step_pill(f, t, s - 1.0, 1, "CHOP THE OIL", (255, 64, 140))
    for i in range(3):
        tx_, ty_ = hs[i][0] + 34, hs[i][1]
        if t < tc + 0.25:
            put(f, enzyme_img(46, 1.0 if t > tc - 0.1 else chew(t + i, 14)), tx_ + 56 - sep * 60, ty_, rot=180)
        if tc - 0.02 < t < tc + 0.3:
            q = (t - tc + 0.02) / 0.32
            disc(f, tx_ + 20, ty_, 30 + 80 * q, (255, 255, 255), op=(1 - q) * 0.8)
            for a in range(8):
                aa = a / 8 * 2 * math.pi
                cv2.line(f, (int(tx_ + 20 + math.cos(aa) * 40 * (1 + q)), int(ty_ + math.sin(aa) * 40 * (1 + q))),
                         (int(tx_ + 20 + math.cos(aa) * 70 * (1 + q)), int(ty_ + math.sin(aa) * 70 * (1 + q))), (1, 1, 1), 5, cv2.LINE_AA)
    if t > E["t_fatty"] - 0.15:
        k = popk(t, E["t_fatty"] - 0.15)
        put(f, pill("FATTY ACIDS", 50, bg=(150, 70, 0), acc=(255, 230, 90)), CX, 1250, op=clamp(k * 3), sc=0.6 + 0.4 * k)
    put_head(f, 830, 1440, "shock" if t > tc else "wow", t, 0.85, mouth(t), look=(-1, -1))
    return f


def shot_ET(t, n):
    s, e = SHOT["ET"]["start"], SHOT["ET"]["end"]
    f = oil_world(t, 8)
    step_pill(f, t, s + 0.05, 2, "EAT SOME", (0, 220, 170))
    yx, yy = 540, 1150
    te = E["t_eats"] - 0.1
    open_ = t > te - 0.2 and t < E["t_them"] + 0.35
    fa = [(250, 560, 0.25, False, 0), (700, 520, 2.6, True, 1), (300, 820, -0.1, True, 2), (720, 800, 3.3, False, 3)]
    for (x, y, a, kinked, i) in fa:
        if not kinked:
            q = eio((t - te - i * 0.12) / 0.55) if t > te else 0
            if q >= 0.999:
                continue
            xx, yy2 = lerp(x, yx, q), lerp(y, yy - 40, q)
            sc_ = 1 - 0.85 * q
            fatty(f, xx, yy2, a + q * 2, False, sc_ * 1.0, op=1.0)
        else:
            dx = 40 * math.sin(t * 2 + i)
            push = eo((t - E["t_leaves"]) / 0.6) if t > E["t_leaves"] else 0
            fatty(f, x + dx + (x - 540) * 0.25 * push, y - 80 * push, a + 0.1 * math.sin(t * 2 + i), True, 1.0)
    full = t > E["t_leaves"] - 0.1
    yeast(f, yx, yy, 180 * (1 + 0.06 * full), t, mouth=(0.6 + 0.4 * chew(t, 14)) if open_ else 0.0, face=True)
    if t > E["t_rest"] - 0.12:
        k = popk(t, E["t_rest"] - 0.12)
        put(f, pill("left behind", 46, bg=(18, 16, 40), acc=(255, 160, 40)), CX, 1420, op=clamp(k * 3), sc=0.6 + 0.4 * k)
    return f


def shot_OL(t, n):
    s, e = SHOT["OL"]["start"], SHOT["OL"]["end"]
    f = grad((90, 40, 200), (20, 6, 70), cx=0.5, cy=0.40)
    sparkles(f, t, 51, n=20, op=0.6)
    y0 = 930
    draw_layers(f, t, y0=y0, y1=1480, red=0.0)
    step_pill(f, t, E["t_soaks"] - 0.2, 3, "SOAKS IN", (255, 160, 40))
    # kinked fatty acids hovering, then sinking into the skin
    ts = E["t_soaks"] - 0.1
    for i, (x, a) in enumerate(((300, 1.1), (520, 1.4), (760, 1.9))):
        q = eio((t - ts - i * 0.15) / 1.0) if t > ts else 0
        y = lerp(680 + 30 * math.sin(t * 2 + i), y0 + 120, q)
        op = 1.0 - 0.75 * clamp((y - y0 + 60) / 200)
        fatty(f, x, y, a + 0.15 * math.sin(t * 2 + i), True, 0.9, op=op)
    tier(f, t, E["t_oleic"] - 0.1, "one leftover", "OLEIC ACID", 560, size=160, lo_size=56, gap=125, fill=(255, 176, 60))
    if t > E["t_skin"] - 0.15:
        put(f, pill("into your skin", 42, bg=(18, 16, 40), acc=(255, 120, 140)), CX, 1300, op=appear(t, E["t_skin"] - 0.15))
    return f


def shot_RX(t, n):
    s, e = SHOT["RX"]["start"], SHOT["RX"]["end"]
    tb = E["t_gets"] - 0.2
    if t < tb:
        f = grad((255, 120, 80), (150, 20, 40), cx=0.5, cy=0.40)
        y0 = 760
        red = eo((t - E["t_reacts"] + 0.15) / 0.6) if t > E["t_reacts"] - 0.15 else 0
        draw_layers(f, t, y0=y0, y1=1470, red=red)
        for i in range(3):
            fatty(f, 260 + i * 240, y0 + 150 + 20 * i, 1.2 + i * 0.4, True, 0.55, op=0.6)
        if red > 0:
            for i in range(7):
                x = 180 + i * 120
                q = ((t - E["t_reacts"]) * 1.3 + i * 0.17) % 1
                cv2.line(f, (x, int(y0 - 40 - 140 * q)), (x + 18, int(y0 - 80 - 140 * q)), (1.0, 0.95, 0.6), 7, cv2.LINE_AA)
                cv2.line(f, (x + 18, int(y0 - 80 - 140 * q)), (x - 4, int(y0 - 120 - 140 * q)), (1.0, 0.95, 0.6), 7, cv2.LINE_AA)
        put(f, small("in some people…", 60), CX, 380, op=appear(t, s + 0.1))
        if red > 0:
            put(f, pill("the scalp reacts", 46, bg=(140, 0, 30), acc=(255, 230, 90)), CX, 520, op=clamp(red * 2))
        return f
    # B: Nessa itching
    f = big_set((255, 90, 70), (120, 10, 50), (255, 206, 0), 540, 900, 330, 61, t)
    sc = 1.15
    jig = 8 * math.sin(t * 40)
    put_char(f, 540 + jig, 1470, "cover", "gross" if t > E["t_itchy"] - 0.1 else "worried", t, sc)
    hx, hy = 540, 1470 - 400 * sc
    for i in range(6):
        a = -math.pi / 2 + (i - 2.5) * 0.45
        q = ((t * 3 + i * 0.2) % 1)
        r0 = 110 + 40 * q
        cv2.line(f, (int(hx + math.cos(a) * r0), int(hy + math.sin(a) * r0)), (int(hx + math.cos(a) * (r0 + 50)), int(hy + math.sin(a) * (r0 + 50))),
                 (1.0, 1.0, 1.0), 8, cv2.LINE_AA)
    rng = np.random.default_rng(4)
    for i in range(14):
        q = ((t - tb) * 0.9 + rng.uniform(0, 1)) % 1
        flake(f, hx + rng.uniform(-200, 200), hy + 40 + q * 600, rng.uniform(7, 13), t * 2 + i, seed=i)
    if t > E["t_irritated"] - 0.1:
        k = popk(t, E["t_irritated"] - 0.1)
        put(f, pill("irritated", 48, bg=(140, 0, 30), acc=(255, 230, 90)), CX, 380, op=clamp(k * 3), sc=0.6 + 0.4 * k)
    if t > E["t_itchy"] - 0.1:
        k = popk(t, E["t_itchy"] - 0.1)
        put(f, pill("itchy", 48, bg=(140, 0, 30), acc=(255, 230, 90)), CX, 490, op=clamp(k * 3), sc=0.6 + 0.4 * k)
    return f


def shoulders_scene(t, t0):
    f = grad((150, 80, 255), (40, 10, 110), cx=0.5, cy=0.40)
    sparkles(f, t, 71, n=16, op=0.6)
    disc(f, 540, 820, 330, (255, 206, 0), glow=0.4)
    # dark sweater shoulders
    cv2.ellipse(f, (540, 1560), (470, 400), 0, 180, 360, (0.08, 0.08, 0.16), -1, cv2.LINE_AA)
    cv2.ellipse(f, (540, 1560), (470, 400), 0, 180, 360, (0.25, 0.25, 0.4), 6, cv2.LINE_AA)
    cv2.rectangle(f, (490, 1050), (590, 1180), (1, 1, 1), -1)
    cv2.line(f, (490, 1050), (490, 1170), (0.06, 0.06, 0.08), 7, cv2.LINE_AA)
    cv2.line(f, (590, 1050), (590, 1170), (0.06, 0.06, 0.08), 7, cv2.LINE_AA)
    put_head(f, 540, 900, "gross" if t > E["t_flakes"] - 0.1 else "worried", t, 2.0, mouth(t), look=(1, 1))
    rng = np.random.default_rng(5)
    # flakes resting on the shoulders (accumulate)
    for i in range(46):
        x = rng.uniform(140, 940)
        ys = 1560 - 400 * math.sqrt(max(0, 1 - ((x - 540) / 470) ** 2)) + rng.uniform(10, 60)
        tl = t0 + rng.uniform(0, 1.6)
        if t > tl:
            flake(f, x, ys, rng.uniform(6, 12), i, seed=i)
    for i in range(24):
        q = ((t - t0) * 0.7 + rng.uniform(0, 1)) % 1
        flake(f, rng.uniform(250, 830), 700 + q * 700, rng.uniform(6, 12), t * 2 + i, seed=50 + i)
    return f


def shot_FL(t, n):
    s, e = SHOT["FL"]["start"], SHOT["FL"]["end"]
    tb = E["t_and3"] - 0.12
    if t < tb:
        A = grad((0, 200, 230), (0, 50, 120), cx=0.5, cy=0.40)
        sparkles(A, t, 81, n=14, op=0.6)
        lift = eio((t - E["t_shed"] + 0.15) / 1.0) if t > E["t_shed"] - 0.15 else 0
        draw_layers(A, t, y0=860, y1=1480, red=0.35, lift=lift)
        put(A, small("dead skin cells", 60), CX, 380, op=appear(t, s + 0.1))
        if t > E["t_clumps"] - 0.15:
            put(A, pill("shed in clumps", 46, bg=(18, 16, 40), acc=(255, 255, 255)), CX, 470, op=appear(t, E["t_clumps"] - 0.15))
        if t > tb - 0.08:
            A = A + (1 - A) * clamp((t - tb + 0.08) / 0.08) * 0.85
        return A
    f = shoulders_scene(t, tb)
    tier(f, t, E["t_flakes"] - 0.08, "and those are your", "FLAKES", 450, size=210, lo_size=58, gap=150)
    if t < tb + 0.2:
        f = f + (1 - f) * (1 - (t - tb) / 0.2) ** 2 * 0.85
    return f


def shot_WT(t, n):
    s, e = SHOT["WT"]["start"], SHOT["WT"]["end"]
    f = big_set((60, 140, 255), (20, 20, 100), (255, 206, 0), 540, 900, 320, 91, t)
    why = t > E["t_so2"] - 0.1
    put(f, small("but wait…", 66), CX, 360, op=appear(t, s + 0.05) * (1 - clamp((t - E["t_so2"] + 0.1) / 0.2)))
    for side, (x, st) in enumerate(((300, "nessa"), (780, "girl2"))):
        flaky = side == 0
        expr = ("gross" if flaky else "laugh") if why else "think"
        pose = ("cover" if flaky else "hips") if why else "stand"
        put_char(f, x, 1430, pose, expr, t + side, 0.82, style=st, m=mouth(t) if side == 0 and False else 0)
        hx, hy = x, 1430 - 400 * 0.82
        # yeast on both heads
        if t > E["t_most2"] - 0.15:
            q = popk(t, E["t_most2"] - 0.15 + side * 0.1, 0.3)
            for j, dx in enumerate((-30, 10, 40)):
                yeast(f, hx + dx, hy - 64 - 4 * j, 16 * q + 0.1, t, face=False, phase=j + side)
        if why and flaky:
            rng = np.random.default_rng(6)
            for i in range(12):
                q = ((t - E["t_so2"]) * 0.8 + rng.uniform(0, 1)) % 1
                flake(f, hx + rng.uniform(-120, 120), hy + 20 + q * 380, rng.uniform(6, 11), t * 2 + i, seed=i)
        if why and not flaky:
            sparkles(f, t, 93, n=8, area=(hx - 140, hy - 140, hx + 140, hy + 120), op=1, size=9)
    if t > E["t_yeast2"] - 0.2 and not why:
        put(f, pill("both have the yeast", 44, bg=(18, 16, 40), acc=(255, 230, 90)), CX, 600, op=appear(t, E["t_yeast2"] - 0.2))
    if why:
        k = popk(t, E["t_why"] - 0.1, 0.4)
        put(f, big("?", 330, (255, 236, 80), 12), CX, 760 + 10 * math.sin(t * 4), op=clamp(k * 3), sc=0.4 + 0.6 * k, rot=6 * math.sin(t * 3))
        put(f, small("why don't we all get flakes?", 54), CX, 380, op=appear(t, E["t_why"] - 0.15))
    return f


def shot_SN(t, n):
    s, e = SHOT["SN"]["start"], SHOT["SN"]["end"]
    f = big_set((0, 200, 150), (0, 60, 90), (255, 230, 90), 540, 1000, 300, 101, t)
    put(f, pill("scientists think", 44, bg=(18, 16, 40), acc=(0, 230, 170)), CX, 330, op=appear(t, s + 0.1))
    # two mini scalp samples: sensitive (reacts) vs tough (calm)
    ts = E["t_sensitive"] - 0.1
    for side, x in enumerate((320, 760)):
        sens = side == 0
        k = popk(t, s + 0.15 + side * 0.12, 0.35)
        if k < 0.02:
            continue
        w_, h_ = 330 * k, 230 * k
        y = 760
        cv2.rectangle(f, (int(x - w_ / 2 + 10), int(y - h_ / 2 + 14)), (int(x + w_ / 2 + 10), int(y + h_ / 2 + 14)), (0.05, 0.1, 0.12), -1, cv2.LINE_AA)
        cv2.rectangle(f, (int(x - w_ / 2), int(y - h_ / 2)), (int(x + w_ / 2), int(y + h_ / 2)), (0.94, 0.53, 0.56), -1, cv2.LINE_AA)
        cv2.rectangle(f, (int(x - w_ / 2), int(y - h_ / 2)), (int(x + w_ / 2), int(y - h_ / 2 + 70 * k)), (1.0, 0.80, 0.72), -1, cv2.LINE_AA)
        for i in range(4):
            cv2.rectangle(f, (int(x - w_ / 2 + i * w_ / 4), int(y - h_ / 2)), (int(x - w_ / 2 + (i + 1) * w_ / 4) - 3, int(y - h_ / 2 + 18 * k)),
                          (0.96, 0.86, 0.74), -1, cv2.LINE_AA)
        fatty(f, x - 90, y - h_ / 2 - 60, 0.3 + 0.1 * math.sin(t * 2 + side), True, 0.45 * k)
        if t > ts and sens:
            r_ = eo((t - ts) / 0.5)
            reg = np.zeros((H, W), np.float32)
            cv2.rectangle(reg, (int(x - w_ / 2), int(y - h_ / 2)), (int(x + w_ / 2), int(y + h_ / 2)), 1.0, -1)
            mm = (reg * r_ * 0.55 * (0.85 + 0.15 * math.sin(t * 9)))[..., None]
            f = f * (1 - mm) + np.array([0.95, 0.08, 0.12], np.float32) * mm
        if t > ts + 0.15 and not sens:
            q = popk(t, ts + 0.15)
            # shield
            sh_ = np.array([(x, y - 180), (x + 70, y - 155), (x + 62, y - 80), (x, y - 40), (x - 62, y - 80), (x - 70, y - 155)], np.int32)
            cv2.fillPoly(f, [sh_], (0.2, 0.85, 0.6), cv2.LINE_AA)
            cv2.polylines(f, [sh_], True, (1, 1, 1), 6, cv2.LINE_AA)
    if t > ts:
        put(f, pill("sensitive scalps react more", 44, bg=(140, 0, 30), acc=(255, 230, 90)), CX, 1010, op=appear(t, ts))
    put_char(f, 540, 1480, "think" if t < ts else "point", "think" if t < ts else "talk", t, 0.7, m=mouth(t), look=(0, -1))
    return f


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


def bottle(f, x, y, t):
    im = _TX.get("bottle")
    if im is None:
        k = 3
        im = Image.new("RGBA", (220 * k, 420 * k), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([30 * k, 110 * k, 190 * k, 410 * k], 40 * k, fill=(40, 170, 255, 255), outline=(14, 14, 30, 255), width=6 * k)
        d.rounded_rectangle([46 * k, 130 * k, 76 * k, 390 * k], 14 * k, fill=(160, 220, 255, 200))
        d.rounded_rectangle([70 * k, 50 * k, 150 * k, 114 * k], 14 * k, fill=(255, 255, 255, 255), outline=(14, 14, 30, 255), width=5 * k)
        d.rounded_rectangle([90 * k, 14 * k, 130 * k, 54 * k], 10 * k, fill=(255, 255, 255, 255), outline=(14, 14, 30, 255), width=5 * k)
        d.rounded_rectangle([60 * k, 220 * k, 160 * k, 320 * k], 18 * k, fill=(255, 255, 255, 235))
        for i in range(3):
            d.ellipse([(80 + i * 22) * k, 250 * k, (96 + i * 22) * k, 266 * k], fill=(40, 170, 255, 255))
        d.rectangle([78 * k, 282 * k, 142 * k, 290 * k], fill=(150, 200, 240, 255))
        im = im.resize((220, 420), Image.LANCZOS)
        _TX["bottle"] = im
    put(f, im, x, y, rot=4 * math.sin(t * 3))


def shot_TP(t, n):
    s, e = SHOT["TP"]["start"], SHOT["TP"]["end"]
    f = big_set((0, 214, 160), (0, 64, 92), (255, 206, 0), 540, 1050, 300, 111, t)
    put(f, pill("SCALP TIP", 40, bg=(0, 150, 100), acc=(255, 230, 90)), CX, 300, op=appear(t, s + 0.05))
    k1 = popk(t, s + 0.05, 0.38)
    put(f, tip_card2("Wash regularly", "gently massage, rinse well", t > E["t_regularly"] - 0.05), CX, 470, op=clamp(k1 * 3), sc=0.7 + 0.3 * k1,
        rot=1.5 * (1 - k1))
    if t > E["t_if"] - 0.2:
        k2 = popk(t, E["t_if"] - 0.2, 0.38)
        put(f, tip_card2("Flakes won't quit?", "see a dermatologist", t > E["t_derm"] - 0.05, (40, 130, 255)), CX, 730, op=clamp(k2 * 3),
            sc=0.7 + 0.3 * k2, rot=-1.5 * (1 - k2))
    # bubbles + plain shampoo bottle + Nessa
    rng = np.random.default_rng(7)
    for i in range(14):
        q = ((t - s) * 0.5 + rng.uniform(0, 1)) % 1
        x = rng.uniform(150, 940); y = 1450 - q * 600
        disc(f, x, y, rng.uniform(10, 26), (220, 245, 255), op=0.5 * math.sin(math.pi * q), ring=((255, 255, 255), 3))
    bottle(f, 760, 1260, t)
    derm = t > E["t_see"] - 0.1
    put_char(f, 380, 1470, "point" if derm else "hips", "talk" if mouth(t) > 0.3 else "smile", t, 0.82, m=mouth(t))
    return f


def shot_LP(t, n):
    s, e = SHOT["LP"]["start"], SHOT["LP"]["end"]
    big = [(540, 980, 170, 0.0)]
    f = scalp_scene(t, False, None)
    u = eio((t - s) / (e - s))
    f = zoom_at(f, 1.0 + 0.35 * u, 540, 980)
    # night-ish whisper tint
    lum = (f * np.array([0.3, 0.55, 0.15], np.float32)).sum(2, keepdims=True)
    f = f * 0.75 + lum * np.array([0.15, 0.10, 0.30], np.float32)
    yeast(f, 540, 980, 170 + 20 * u, t, mouth=0.0, face=True, phase=0.0)
    put(f, small("that tiny fungus…", 62), CX, 380, op=appear(t, E["t_tiny"] - 0.2))
    return f


def shot_LQ(t, n):
    s, e = SHOT["LQ"]["start"], SHOT["LQ"]["end"]
    tr = E["t_right"] - 0.15
    f = scalp_scene(t, False, None)
    f = zoom_at(f, 1.35, 540, 980)
    lum = (f * np.array([0.3, 0.55, 0.15], np.float32)).sum(2, keepdims=True)
    f = f * 0.75 + lum * np.array([0.15, 0.10, 0.30], np.float32)
    # dinner: yeast gobbling glowing oil droplets
    for i in range(6):
        q = ((t - s) * 0.9 + i / 6) % 1.0
        a = i * 1.05
        x = 540 + math.cos(a) * 330 * (1 - q); y = 1000 + math.sin(a) * 240 * (1 - q)
        ball(f, x, y, 22 * (1 - 0.6 * q), (1.0, 0.80, 0.22))
    yeast(f, 540, 980, 190, t, mouth=0.4 + 0.6 * chew(t, 13), face=True)
    # napkin bib
    if t > E["t_dinner"] - 0.15:
        put(f, pill("dinner on your head", 46, bg=(18, 16, 40), acc=(255, 200, 40)), CX, 1330, op=appear(t, E["t_dinner"] - 0.15))
    if t > tr:
        # pull back out to the snow globe (loops into the opening)
        q = eio((t - tr) / 0.5)
        G = globe(t, head_expr="worried")
        r = 1300 * (1 - q) ** 1.3
        f = zoom_at(f, 1 + 0.0 * q, 540, 900)
        Gz = zoom_at(G, 1 + 6.0 * (1 - q) ** 1.7, 540, 640)
        m = np.clip(r - np.sqrt((_xx - 540) ** 2 + (_yy - 900) ** 2) + 0.5, 0, 1)[..., None]
        f = Gz * (1 - m) + f * m
    return f



RENDER = {k: globals()[f"shot_{k}"] for k in SHOT}


def rs(sid, t, n):
    s = SHOT[sid]
    tt = min(max(t, s["start"]), s["end"] - 1e-3)
    return RENDER[sid](tt, n)


# ---------------- camera ----------------
PUNCH = [(E["t_scalp"], 0.07, 0.3), (E["t_mala"], 0.06, 0.3), (E["t_adults"], 0.04, 0.3), (E["t_fat"], 0.06, 0.3), (E["t_sebum"], 0.06, 0.3),
         (E["t_enzymes"], 0.04, 0.3), (E["t_chop"], 0.09, 0.35), (E["t_eats"], 0.05, 0.3), (E["t_rest"], 0.04, 0.3), (E["t_oleic"], 0.06, 0.3),
         (E["t_soaks"], 0.04, 0.3), (E["t_reacts"], 0.06, 0.3), (E["t_itchy"], 0.05, 0.3), (E["t_clumps"], 0.05, 0.3), (E["t_flakes"], 0.09, 0.35),
         (E["t_wait"], 0.06, 0.3), (E["t_why"], 0.06, 0.3), (E["t_sensitive"], 0.05, 0.3), (E["t_regularly"], 0.04, 0.3), (E["t_derm"], 0.04, 0.3),
         (E["t_dinner"], 0.05, 0.3), (E["t_now"], 0.05, 0.3)]
SHAKE = [(E["t_scalp"], 12, 0.35), (E["t_chop"], 20, 0.45), (E["t_reacts"], 14, 0.4), (E["t_itchy"], 12, 0.5), (E["t_flakes"], 20, 0.45),
         (E["t_wait"], 12, 0.35), (E["t_why"], 8, 0.3)]


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
