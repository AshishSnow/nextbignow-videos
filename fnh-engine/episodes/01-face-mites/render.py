"""FreshNestHub — 'Tiny bugs live inside your face' (Demodex). Fully procedural: NESSA host + 3D mites + designed sets.
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


# ================= scene builders =================
_BED = {}


def bedroom(t, mode="night"):
    """bedroom set (bg + moon/sun + bed without blanket). returns frame"""
    if mode == "night":
        f = grad((44, 56, 160), (6, 8, 34), cx=0.62, cy=0.28)
        sparkles(f, t, 7, n=40, col=(255, 250, 220), area=(60, 260, 1020, 900), op=0.9, size=6)
        disc(f, 730, 560, 215, (255, 238, 175), glow=0.55)
        for (dx, dy, r) in ((-60, -40, 38), (50, 30, 28), (-10, 90, 22), (80, -70, 18)):
            disc(f, 730 + dx, 560 + dy, r, (236, 212, 150), op=0.8)
    else:
        f = grad((255, 222, 120), (255, 120, 60), cx=0.64, cy=0.26)
        disc(f, 730, 540, 220, (255, 196, 40), glow=0.7)
        for i in range(12):
            a = i / 12 * 2 * math.pi + t * 0.4
            x0, y0 = 730 + math.cos(a) * 250, 540 + math.sin(a) * 250
            x1, y1 = 730 + math.cos(a) * 310, 540 + math.sin(a) * 310
            cv2.line(f, (int(x0), int(y0)), (int(x1), int(y1)), (1.0, 0.86, 0.3), 14, cv2.LINE_AA)
    key = mode
    if key not in _BED:
        im = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        k = 2
        wood, wood_d = (150, 88, 48, 255), (104, 58, 30, 255)
        # floor shadow
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([80 * k, 1360 * k, 1000 * k, 1440 * k], fill=(0, 0, 0, 110))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)))
        d.rounded_rectangle([92 * k, 930 * k, 190 * k, 1370 * k], 40 * k, fill=wood, outline=(40, 20, 10, 255), width=5 * k)
        d.rounded_rectangle([108 * k, 950 * k, 128 * k, 1340 * k], 10 * k, fill=(190, 122, 74, 255))
        d.rounded_rectangle([890 * k, 1080 * k, 962 * k, 1370 * k], 30 * k, fill=wood, outline=(40, 20, 10, 255), width=5 * k)
        d.rectangle([150 * k, 1290 * k, 930 * k, 1350 * k], fill=wood_d, outline=(40, 20, 10, 255), width=5 * k)
        d.rounded_rectangle([140 * k, 1196 * k, 940 * k, 1300 * k], 26 * k, fill=(232, 238, 252, 255), outline=(40, 30, 60, 255), width=5 * k)
        # pillow
        d.ellipse([150 * k, 1108 * k, 440 * k, 1226 * k], fill=(255, 255, 255, 255), outline=(60, 60, 90, 255), width=5 * k)
        d.ellipse([190 * k, 1128 * k, 400 * k, 1170 * k], fill=(240, 242, 255, 255))
        im = im.resize((W, H), Image.LANCZOS)
        _BED[key] = to_np(im)
    rgb, a = _BED[key]
    over(f, rgb, a, 0, 0)
    return f


_BL = {}


def blanket(f, mode="night", top=1118, left=360, hump=True):
    key = (mode, top, left, hump)
    if key not in _BL:
        k = 2
        im = Image.new("RGBA", (W * k, H * k), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        col = (96, 84, 230, 255) if mode == "night" else (0, 178, 140, 255)
        dark = tuple(int(c * 0.72) for c in col[:3]) + (255,)
        pts = [(left, 1300), (left - 10, top + 40)]
        for i in range(31):
            u = i / 30
            x = left + 20 + u * (950 - left - 20)
            y = top + (0 if not hump else -38 * math.sin(math.pi * clamp((u - 0.05) / 0.55)) + 14 * u)
            pts.append((x, y))
        pts += [(958, 1300)]
        d.polygon([(x * k, y * k) for x, y in pts], fill=col, outline=(30, 24, 70, 255), width=5 * k)
        d.line([((left + 5) * k, (top + 42) * k), (950 * k, (top + 42 + 10) * k)], fill=(255, 255, 255, 120), width=10 * k)
        for i in range(6):
            x = left + 70 + i * 95
            d.ellipse([(x - 10) * k, (top + 95) * k, (x + 10) * k, (top + 115) * k], fill=(255, 255, 255, 90))
        d.line([(left * k, 1296 * k), (958 * k, 1296 * k)], fill=dark, width=8 * k)
        _BL[key] = to_np(im.resize((W, H), Image.LANCZOS))
    rgb, a = _BL[key]
    over(f, rgb, a, 0, 0)


def zzz(f, t, t0, x, y):
    if t < t0:
        return
    for i in range(3):
        q = ((t - t0) * 0.8 + i / 3) % 1.0
        op = math.sin(math.pi * q) * clamp((t - t0) / 0.3)
        put(f, big("z", 46 + 18 * i, (255, 255, 255), 5), x + 70 * q + 26 * i, y - 170 * q - 30 * i, op=op, rot=12)


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


# ================= shots =================
def shot_H1(t, n):
    s0 = 0.0
    dv0 = E["t_tiny"] - 0.12
    p = eio((t - dv0) / 0.62)
    # skin world (inside the mirror)
    ox, oy = 160 + t * 6, 200 + t * 10
    pore = pore_near(ox + 520, oy + 880)
    px, py = pore[0] - ox, pore[1] - oy
    inner = skin_view(ox, oy, 1.0 + 0.05 * t)
    zc = 1.0 + 0.05 * t
    px, py = W / 2 + (px - W / 2) * zc, H / 2 + (py - H / 2) * zc
    vis = 0.18 + 0.42 * eo((t - 0.05) / 1.7) + 0.24 * popk(t, E["t_inside"] - 0.05, 0.4)
    mite(inner, 0, 0, math.pi * 0.80, 470, t, vis=min(0.92, vis), emerge=(px, py), wig=1.0)
    if t > E["t_right"] - 0.1:
        p2 = pore_near(ox + 790, oy + 470)
        q2 = (p2[0] - ox - W / 2) * zc + W / 2, (p2[1] - oy - H / 2) * zc + H / 2
        mite(inner, 0, 0, -0.55, 380, t, vis=min(0.6, 0.6 * popk(t, E["t_right"] - 0.08, 0.35)), emerge=q2, phase=1.3)
    if p >= 0.999:
        f = inner
    else:
        out = grad((255, 60, 170), (70, 8, 110), cx=0.5, cy=0.45)
        sparkles(out, t, 3, n=30, op=1.0, size=8)
        mx, my, rx, ry = 510, 800, 300, 380
        # mirror handle + frame
        cv2.rectangle(out, (mx - 36, my + ry - 10), (mx + 36, my + ry + 260), C((0, 150, 100)).tolist(), -1, cv2.LINE_AA)
        cv2.rectangle(out, (mx - 20, my + ry - 10), (mx - 6, my + ry + 250), C((80, 230, 170)).tolist(), -1, cv2.LINE_AA)
        disc(out, mx, my + ry + 262, 38, (0, 150, 100))
        ell = ((_xx - mx) / (rx + 34)) ** 2 + ((_yy - my) / (ry + 34)) ** 2
        fm = np.clip((1 - ell) * 60, 0, 1)[..., None]
        shade = np.clip(0.75 + 0.35 * (-(_yy - my) / ry), 0.5, 1.15)[..., None]
        out = out * (1 - fm) + C((0, 178, 120)) * shade * fm
        # Nessa peeking, shocked
        put_head(out, 220, 1330, "shock", t, 1.55, mouth(t), look=(1, -1))
        z = 1 + 5.5 * p ** 1.6
        out = zoom_at(out, z, mx, my)
        rxz, ryz = rx * z, ry * z
        el = ((_xx - mx) / rxz) ** 2 + ((_yy - my) / ryz) ** 2
        m = np.clip((1 - el) * rxz / 2.2, 0, 1)[..., None]
        f = out * (1 - m) + inner * m
        # glass glare on the mirror
        if p < 0.6:
            g = np.exp(-((_xx - mx + _yy - my + 0.25 * rxz) / (0.09 * rxz)) ** 2)[..., None] * m * 0.22 * (1 - p / 0.6)
            f = f + g
    tier(f, t, E["t_inside"] - 0.06, "there are tiny bugs living", "IN YOUR FACE", 1340, size=150, gap=122)
    return f


def shot_NM(t, n):
    s = SHOT["NM"]["start"]
    f = grad((44, 100, 255), (8, 14, 76), cy=0.46)
    disc(f, 510, 900, 360, (255, 206, 0), glow=0.45)
    sparkles(f, t, 21, n=18, op=0.8)
    tier(f, t, E["t_called"] - 0.05, "they're called", "DEMODEX", 700, size=230, lo_size=58, gap=170)
    k = eo((t - s) / 0.42)
    hx = lerp(1250, 160, k)
    mite(f, hx, 960, math.pi + 0.06, 790, t, walk=1.8, wig=0.55, shadow=0.6)
    if t > E["t_mites"]:
        put(f, pill("about 0.3 mm long", 46, acc=(255, 206, 0)), 510, 1290, op=appear(t, E["t_mites"]), sc=0.85 + 0.15 * popk(t, E["t_mites"]))
    return f


STY = ["guy", "girl", "bald", "girl2", "guy2", "mom", "guy", "girl2", "bald", "girl", "guy2", "nessa", "guy", "girl", "mom", "girl2", "guy2",
       "bald", "girl", "guy"]


def shot_EV(t, n):
    s = SHOT["EV"]["start"]
    f = grad((0, 214, 176), (0, 56, 86), cy=0.55)
    disc(f, 510, 1000, 330, (255, 206, 0), glow=0.4)
    tier(f, t, E["t_every"] - 0.08, "almost", "EVERY ADULT", 400, size=140, lo_size=56, gap=110)
    cols = [130, 320, 510, 700, 890]
    rows = [690, 910, 1130, 1350]
    i = 0
    for r_, fy in enumerate(rows):
        for c_, fx in enumerate(cols):
            st = STY[i]
            idx = r_ * 5 + c_
            t0 = s + 0.02 * idx
            sc = popk(t, t0, 0.3)
            if sc <= 0.02:
                i += 1; continue
            is_n = st == "nessa"
            ex = "smile"
            if t > E["t_every"] + 0.05 * idx:
                ex = "wow"
            if is_n and t > E["t_them"] - 0.05:
                ex = "shock"
            pose = "shock" if is_n and t > E["t_them"] - 0.05 else "stand"
            put_char(f, fx, fy, pose, ex, t + idx * 0.3, 0.36, style=st, sc=sc, shadow=False)
            tm = E["t_every"] - 0.1 + 0.035 * idx
            if t > tm:
                q = popk(t, tm, 0.3)
                mite(f, fx - 40 * q + 6 * math.sin(t * 3 + idx), fy - 134, math.pi + 0.25, 80 * q, t, wig=0.8, walk=2.0, shadow=0.5, phase=idx)
            i += 1
    return f


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


def shot_DY(t, n):
    s, e = SHOT["DY"]["start"], SHOT["DY"]["end"]
    f = grad((255, 200, 50), (232, 80, 30), cx=0.5, cy=0.40)
    img, al, lum, fx, (gx, gy) = follicle_block()
    # soft drop shadow of the block
    sh = cv2.GaussianBlur(al, (0, 0), 22)
    f *= (1 - 0.35 * np.roll(np.roll(sh, 26, 0), 18, 1))[..., None]
    f = f * (1 - al[..., None]) + img * al[..., None]
    # oil droplets flowing from gland into the follicle and up
    for i in range(9):
        q = ((t - s) * 0.55 + i / 9) % 1.0
        if q < 0.3:
            u = q / 0.3
            x, y = lerp(gx - 30, fx(770) + 10, u), lerp(812, 770, u)
        else:
            u = (q - 0.3) / 0.7
            y = lerp(770, 575, u); x = fx(y) + 14 * math.sin(i + y * 0.05)
        disc(f, x, y, 9, (255, 214, 70), op=0.95)
        disc(f, x - 3, y - 3, 3, (255, 250, 220), op=0.9)
    # mites head-down inside the follicle
    for j, (yh, L, ph) in enumerate(((760, 170, 0.0), (900, 160, 1.7), (1040, 150, 3.1))):
        mite(f, fx(yh) - 2, yh, math.pi / 2 + 0.06, L, t, wig=0.45, walk=0.6, shadow=0.2, phase=ph, clipmask=lum)
    # sun (all day)
    k = appear(t, s + 0.05)
    if k > 0:
        cxs, cys = 190, 360
        for i in range(10):
            a = i / 10 * 2 * math.pi + t * 0.8
            cv2.line(f, (int(cxs + math.cos(a) * 74 * k), int(cys + math.sin(a) * 74 * k)),
                     (int(cxs + math.cos(a) * 104 * k), int(cys + math.sin(a) * 104 * k)), (1.0, 0.95, 0.5), 12, cv2.LINE_AA)
        disc(f, cxs, cys, 62 * k, (255, 236, 60), glow=0.6)
        put(f, pill("ALL DAY", 40, bg=(120, 30, 10)), cxs, cys + 140, op=k)
    if t > E["t_headdown"] - 0.05:
        k2 = appear(t, E["t_headdown"] - 0.05, 0.3)
        put(f, pill("head-down", 44, acc=(255, 206, 0)), 300, 1000, op=k2)
        arrow_to(f, 440, 985, fx(880) - 30, 900, op=k2)
    if t > E["t_eating"] - 0.05:
        k3 = appear(t, E["t_eating"] - 0.05, 0.3)
        put(f, pill("face oil", 44, bg=(150, 80, 0), acc=(255, 230, 90)), 790, 1000, op=k3)
        arrow_to(f, 760, 965, gx + 52, gy + 40, op=k3)
    z = 1.0 + 0.08 * eio((t - s) / (e - s))
    return zoom_at(f, z, 520, 860)


def night_skin(t, ox, oy, mode="night", z=1.0):
    return tint(skin_view(ox, oy, z, SKIN2), mode)


def shot_NT(t, n):
    s, e = SHOT["NT"]["start"], SHOT["NT"]["end"]
    f = bedroom(t, "night")
    put_head(f, 300, 1120, "sleep", t, 1.15, 0, tilt=-72)
    blanket(f, "night")
    zzz(f, t, E["t_while"] - 0.2, 400, 1010)
    z = 1.0 + 0.22 * eio((t - s) / (e - s))
    f = zoom_at(f, z, 330, 1120, 330 + (510 - 330) * 0.3 * eio((t - s) / (e - s)), 1120 - 160 * eio((t - s) / (e - s)))
    t0 = E["t_crawl"] - 0.25
    if t > t0:
        r = 360 * eo((t - t0) / 0.45)
        inner = night_skin(t, 140, 300)
        p1 = pore_near(140 + 420, 300 + 760, PORES2); p2 = pore_near(140 + 640, 300 + 900, PORES2)
        v = 0.12 + 0.6 * eo((t - t0) / 1.1)
        mite(inner, 0, 0, math.pi * 0.85, 300, t, vis=v, emerge=(p1[0] - 140, p1[1] - 300), shadow=0.5)
        mite(inner, 0, 0, -0.35, 280, t, vis=max(0.1, v - 0.08), emerge=(p2[0] - 140, p2[1] - 300), shadow=0.5, phase=2)
        f = lens(f, inner, 510, 820, r, ring=(190, 200, 255))
    return f


def shot_MT(t, n):
    s = SHOT["MT"]["start"]
    tb = E["t_on"] - 0.06
    A = None
    if t < tb + 0.22:
        A = night_skin(t, 140, 300)
        k = eio((t - s) / max(0.2, E["t_mate"] - s))
        mite(A, lerp(250, 440, k), 830, 0.10, 300, t, walk=1.4, shadow=0.5)
        mite(A, lerp(780, 590, k), 845, math.pi - 0.10, 290, t, walk=1.4, shadow=0.5, phase=1.5)
        if t > E["t_mate"] - 0.05:
            hk = popk(t, E["t_mate"] - 0.05, 0.36)
            put(A, heart(190), 515, 700 - 30 * hk, op=clamp(hk * 3), sc=0.5 + 0.5 * hk)
            for i in range(6):
                q = (t - E["t_mate"]) * 0.9 + i / 6
                if q > 0:
                    put(A, heart(46, (255, 120, 190)), 515 + 180 * math.sin(i * 2.1) * min(1, q * 2), 700 - 260 * (q % 1), op=0.9 * (1 - q % 1))
            fl = clamp(1 - (t - E["t_mate"]) / 0.25) * 0.45
            if fl > 0:
                A = A * (1 - fl) + C((255, 90, 180)) * fl
        tier(A, t, E["t_mate"] - 0.08, "they crawl out to", "MATE", 1290, size=240, fill=(255, 96, 180), lo_size=56, gap=170)
        if t < tb:
            return A
    # B: Nessa sleeping close-up, mites on her cheek
    Bf = grad((44, 56, 160), (6, 8, 34), cx=0.5, cy=0.40)
    sparkles(Bf, t, 9, n=30, col=(255, 250, 220), op=0.7)
    cv2.ellipse(Bf, (510, 860), (470, 330), 0, 0, 360, (0.10, 0.10, 0.22), -1, cv2.LINE_AA)
    cv2.ellipse(Bf, (510, 850), (456, 316), 0, 0, 360, (0.93, 0.94, 1.0), -1, cv2.LINE_AA)
    cv2.ellipse(Bf, (490, 800), (380, 220), 0, 0, 360, (1.0, 1.0, 1.0), -1, cv2.LINE_AA)
    awake = t > E["t_face"] - 0.04
    put_head(Bf, 510, 820, "shock" if awake else "sleep", t, 2.7, 0.6 if awake else 0)
    for j, (dx, dy, a) in enumerate(((-120, 70, 0.3), (-80, 110, math.pi - 0.3))):
        mite(Bf, 510 + dx, 820 + dy, a, 70, t, walk=1.6, eyes=True, shadow=0.3, phase=j)
    put(Bf, heart(40), 410, 850 - 20 * math.sin(t * 6), op=0.9)
    pts = np.array([(40, 1120)] + [(int(x), int(1080 + 30 * math.sin(x / 160))) for x in range(40, 1041, 40)] + [(1040, 1500), (40, 1500)], np.int32)
    cv2.fillPoly(Bf, [pts], C((96, 84, 230)).tolist(), cv2.LINE_AA)
    cv2.polylines(Bf, [pts[:-2]], False, (0.12, 0.09, 0.28), 8, cv2.LINE_AA)
    for i in range(6):
        disc(Bf, 140 + i * 160, 1230 + 30 * (i % 2), 16, (255, 255, 255), op=0.35)
    if t < tb + 0.22:
        q = eio((t - tb) / 0.22)
        sc = 1 - 0.88 * q
        small_ = cv2.resize(A, (int(W * sc), int(H * sc)), interpolation=cv2.INTER_AREA)
        cx_, cy_ = lerp(W / 2, 410, q), lerp(H / 2, 880, q)
        x0, y0 = int(cx_ - small_.shape[1] / 2), int(cy_ - small_.shape[0] / 2)
        rr = lerp(1200, 70, q)
        m = np.zeros((H, W), np.float32)
        cv2.circle(m, (int(cx_), int(cy_)), int(rr), 1.0, -1, cv2.LINE_AA)
        big_ = np.zeros_like(Bf)
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + small_.shape[1]), min(H, y0 + small_.shape[0])
        big_[ya:yb, xa:xb] = small_[ya - y0:yb - y0, xa - x0:xb - x0]
        Bf = Bf * (1 - m[..., None]) + big_ * m[..., None]
    return Bf


def disco_ball(f, x, y, r, t):
    disc(f, x, y, r, (150, 160, 190))
    for i in range(-6, 7):
        for j in range(-6, 7):
            u, v = i / 6.5, j / 6.5
            if u * u + v * v > 0.92:
                continue
            br = 0.55 + 0.45 * math.sin(i * 1.7 + j * 2.3 + t * 9)
            cx_, cy_ = x + u * r, y + v * r
            s_ = r / 7.5 * math.sqrt(max(0.1, 1 - u * u - v * v)) ** 0.5
            cv2.rectangle(f, (int(cx_ - s_), int(cy_ - s_)), (int(cx_ + s_), int(cy_ + s_)), (0.55 + 0.45 * br, 0.6 + 0.4 * br, 0.75 + 0.25 * br), -1)
    disc(f, x - r * 0.35, y - r * 0.35, r * 0.18, (255, 255, 255), op=0.8)
    cv2.line(f, (int(x), 0), (int(x), int(y - r)), (0.8, 0.8, 0.85), 4, cv2.LINE_AA)


def shot_PT(t, n):
    s, e = SHOT["PT"]["start"], SHOT["PT"]["end"]
    tp = E["t_party"] - 0.08
    party = t > tp
    f = night_skin(t, 200 + (t - s) * 8, 340, "party" if party else "night")
    # melatonin glow rising from the skin
    rng = np.random.default_rng(12)
    for i in range(34):
        x0 = rng.uniform(80, 1000); sp = rng.uniform(90, 170); ph = rng.uniform(0, 1)
        q = ((t - s) * sp / 900 + ph) % 1.0
        y = 1500 - q * 1250
        x = x0 + 30 * math.sin(t * 2 + i)
        col = (255, 226, 120) if i % 2 else (210, 170, 255)
        disc(f, x, y, 10 + 6 * (i % 3), col, op=0.75 * math.sin(math.pi * q) * clamp((t - s) / 0.4), glow=0.8)
    beat = (t - tp) * 2.0
    if party:
        fl = (1 - (beat % 1)) ** 3 * 0.22
        col = (255, 60, 200) if int(beat) % 2 == 0 else (40, 230, 255)
        f = f * (1 - fl) + C(col) * fl
    for j, (x, y, a, L) in enumerate(((290, 1020, -0.4, 240), (530, 1200, 0.2, 230), (760, 990, math.pi + 0.4, 240))):
        bob = math.sin(t * 12.5 + j) * 18 if party else 0
        aa = a + (math.sin(t * 9 + j * 2) * 0.35 if party else 0)
        mite(f, x, y + bob, aa, L, t, walk=2.4 if party else 0.8, eyes=party, wig=1.6 if party else 0.6, phase=j, shadow=0.5)
    if party:
        k = eo((t - tp) / 0.4)
        by = lerp(-160, 430, k)
        # beams
        ov = np.zeros_like(f)
        for i, col in enumerate(((255, 70, 200), (70, 220, 255), (255, 230, 70))):
            a = math.sin(t * 2.2 + i * 2.1) * 0.6 + math.pi / 2
            p1 = (510 + math.cos(a - 0.12) * 1800, by + math.sin(a - 0.12) * 1800)
            p2 = (510 + math.cos(a + 0.12) * 1800, by + math.sin(a + 0.12) * 1800)
            cv2.fillPoly(ov, [np.array([(510, by), p1, p2], np.int32)], C(col).tolist(), cv2.LINE_AA)
        f = np.clip(f + cv2.GaussianBlur(ov, (0, 0), 14) * 0.28 * k, 0, 1)
        disco_ball(f, 510, by, 110, t)
        rng2 = np.random.default_rng(3)
        for i in range(60):
            x0 = rng2.uniform(60, 1020); sp = rng2.uniform(250, 520); ph = rng2.uniform(0, 1)
            y = ((t - tp) * sp + ph * 1900) % 1900
            col = [(255, 70, 200), (70, 220, 255), (255, 230, 70), (120, 255, 140)][i % 4]
            cv2.rectangle(f, (int(x0 + 20 * math.sin(t * 4 + i)), int(y)), (int(x0 + 20 * math.sin(t * 4 + i)) + 12, int(y) + 7), C(col).tolist(), -1)
    else:
        tier(f, t, E["t_hormone"] - 0.1, "the sleep hormone", "MELATONIN", 470, size=150, fill=(255, 230, 120), lo_size=54, gap=120,
             out=tp - 0.25)
    return f


def alarm_clock(f, x, y, t, ring):
    rot = math.sin(t * 60) * 9 if ring else 0
    im = _TX.get("clock")
    if im is None:
        k = 3
        im = Image.new("RGBA", (220 * k, 240 * k), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for s_ in (-1, 1):
            d.ellipse([(110 + s_ * 62 - 34) * k, 14 * k, (110 + s_ * 62 + 34) * k, 72 * k], fill=(255, 210, 40, 255), outline=(30, 20, 10, 255), width=5 * k)
        d.line([(60 * k, 214 * k), (40 * k, 236 * k)], fill=(30, 20, 10, 255), width=10 * k)
        d.line([(160 * k, 214 * k), (180 * k, 236 * k)], fill=(30, 20, 10, 255), width=10 * k)
        d.ellipse([20 * k, 40 * k, 200 * k, 220 * k], fill=(232, 40, 50, 255), outline=(30, 20, 10, 255), width=6 * k)
        d.ellipse([42 * k, 62 * k, 178 * k, 198 * k], fill=(255, 255, 255, 255), outline=(30, 20, 10, 255), width=4 * k)
        d.line([(110 * k, 130 * k), (110 * k, 84 * k)], fill=(20, 20, 20, 255), width=7 * k)
        d.line([(110 * k, 130 * k), (146 * k, 130 * k)], fill=(20, 20, 20, 255), width=7 * k)
        im = im.resize((220, 240), Image.LANCZOS)
        _TX["clock"] = im
    put(f, im, x, y, rot=rot)
    if ring:
        for s_ in (-1, 1):
            for i in range(3):
                a = -math.pi / 2 + s_ * (0.5 + i * 0.3)
                r0 = 130 + 10 * math.sin(t * 30)
                cv2.line(f, (int(x + math.cos(a) * r0), int(y - 20 + math.sin(a) * r0)), (int(x + math.cos(a) * (r0 + 40)), int(y - 20 + math.sin(a) * (r0 + 40))),
                         (0.1, 0.1, 0.1), 7, cv2.LINE_AA)


def shot_WK(t, n):
    s = SHOT["WK"]["start"]
    td = E["t_dive"] - 0.12
    if t < td:
        f = bedroom(t, "morning")
        cv2.line(f, (200, 760), (450, 760), (0.45, 0.25, 0.12), 14, cv2.LINE_AA)
        alarm_clock(f, 330, 640, t, ring=t < E["t_wake"] + 0.35)
        if t < E["t_wake"] - 0.06:
            put_head(f, 300, 1120, "sleep", t, 1.15, 0, tilt=-72)
            blanket(f, "morning")
        else:
            k = popk(t, E["t_wake"] - 0.06, 0.3)
            put_char(f, 330, 1370 + 200 * (1 - k), "stretch", "laugh", t, 1.0, shadow=False, clip_y=1215)
            blanket(f, "morning", top=1190, left=250, hump=False)
        return f
    # mites dive back into their pores
    f = skin_view(170, 360, 1.0, SKIN2) * 1.04
    specs = ((300, 760, -0.5), (620, 640, -2.4), (420, 1080, 0.6), (760, 1000, math.pi - 0.5))
    for j, (x, y, a) in enumerate(specs):
        p = pore_near(170 + x, 360 + y, PORES2)
        t0 = E["t_dive"] - 0.05 + j * 0.13
        v = 0.85 * (1 - eio((t - t0) / 0.32))
        if v > 0.03:
            mite(f, 0, 0, a, 260, t, vis=v, emerge=(p[0] - 170, p[1] - 360), walk=2.0, phase=j)
        if 0 < t - t0 < 0.45:
            for k_ in range(3):
                ang = a + math.pi
                ox_, oy_ = p[0] - 170 + math.cos(ang) * (60 + k_ * 26), p[1] - 360 + math.sin(ang) * (60 + k_ * 26)
                cv2.line(f, (int(ox_ - math.sin(ang) * (k_ - 1) * 24), int(oy_ + math.cos(ang) * (k_ - 1) * 24)),
                         (int(ox_ + math.cos(ang) * 70 - math.sin(ang) * (k_ - 1) * 24), int(oy_ + math.sin(ang) * 70 + math.cos(ang) * (k_ - 1) * 24)),
                         (1, 1, 1), 6, cv2.LINE_AA)
    return f


_BABY = {}


def baby_el():
    if "b" in _BABY:
        return _BABY["b"]
    k = 3
    im = Image.new("RGBA", (260 * k, 180 * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([40 * k, 70 * k, 230 * k, 165 * k], fill=(150, 205, 255, 255), outline=(14, 14, 18, 255), width=6 * k)
    d.arc([60 * k, 80 * k, 210 * k, 150 * k], 200, 330, fill=(255, 255, 255, 200), width=5 * k)
    d.ellipse([20 * k, 30 * k, 120 * k, 130 * k], fill=(255, 255, 255, 255), outline=(14, 14, 18, 255), width=6 * k)
    d.arc([48 * k, 70 * k, 66 * k, 86 * k], 20, 160, fill=(14, 14, 18, 255), width=4 * k)
    d.arc([78 * k, 70 * k, 96 * k, 86 * k], 20, 160, fill=(14, 14, 18, 255), width=4 * k)
    d.arc([60 * k, 88 * k, 84 * k, 104 * k], 20, 160, fill=(14, 14, 18, 255), width=4 * k)
    d.ellipse([40 * k, 90 * k, 54 * k, 98 * k], fill=(255, 178, 196, 255)); d.ellipse([90 * k, 90 * k, 104 * k, 98 * k], fill=(255, 178, 196, 255))
    d.arc([62 * k, 18 * k, 90 * k, 46 * k], 180, 400, fill=(14, 14, 18, 255), width=5 * k)
    im = im.resize((260, 180), Image.LANCZOS)
    _BABY["b"] = im
    return im


def shot_MO(t, n):
    s = SHOT["MO"]["start"]
    f = grad((255, 120, 150), (140, 20, 80), cy=0.46)
    disc(f, 510, 860, 340, (255, 206, 0), glow=0.45)
    sparkles(f, t, 31, n=16, op=0.7)
    if t > E["t_got"] - 0.15:
        put(f, small("you got them from your", 56), CX, 500 + 20 * (1 - appear(t, E["t_got"] - 0.15)), op=appear(t, E["t_got"] - 0.15))
    tier(f, t, E["t_mom"] - 0.08, None, "MOM", 750, size=380)
    mx, my = 380, 1380
    shock = t > E["t_mom"] - 0.05
    put_char(f, mx, my, "cradle", "wow" if shock else "smile", t, 1.12, style="mom")
    bx, by = mx - 4, my - 236 * 1.12
    put(f, baby_el(), bx, by)
    # mite hops from mom's cheek to baby
    t0, t1 = E["t_got"] - 0.15, E["t_from"] + 0.15
    a0 = (mx + 34, my - 448 * 1.12 + 40); a1 = (bx - 50, by - 24)
    if t > t0:
        u = eio((t - t0) / (t1 - t0))
        hx = lerp(a0[0], a1[0], u); hy = lerp(a0[1], a1[1], u) - 150 * math.sin(math.pi * u)
        for i in range(12):
            uu = i / 12 * u
            dx_ = lerp(a0[0], a1[0], uu); dy_ = lerp(a0[1], a1[1], uu) - 150 * math.sin(math.pi * uu)
            disc(f, dx_, dy_, 4, (255, 255, 255), op=0.8)
        disc(f, hx - 30, hy + 10, 60, (255, 255, 255), op=0.25, glow=0.0)
        mite(f, hx + 40, hy - 10, math.pi * 0.85, 100, t, walk=2.2, eyes=True, shadow=0.35)
    nexp = "shock" if shock else "wow"
    put_char(f, 800, my, "shock" if shock else "think", nexp, t, 0.78, m=mouth(t) * 0.0)
    return f


def shot_IT(t, n):
    s = SHOT["IT"]["start"]
    f = skin_view(120, 300, 1.0 + 0.04 * (t - s), SKIN2)
    rng = np.random.default_rng(8)
    specs = []
    for i in range(15):
        x, y = rng.uniform(130, 950), rng.uniform(380, 1450)
        specs.append((x, y, rng.uniform(0, 6.28), rng.uniform(170, 240), s + 0.05 + i * (E["t_red"] - s - 0.2) / 15))
    if t > E["t_red"] - 0.05:
        k = eio((t - E["t_red"] + 0.05) / 0.6)
        d = np.sqrt((_xx - 510) ** 2 + (_yy - 900) ** 2)
        m = np.clip((k * 1500 - d) / 300, 0, 1)[..., None]
        red = f * np.array([1.12, 0.62, 0.6], np.float32) + np.array([0.08, 0, 0], np.float32)
        f = f * (1 - m) + red * m
        for i in range(10):
            bx_, by_ = rng.uniform(150, 930), rng.uniform(400, 1400)
            disc(f, bx_, by_, 70 * k, (226, 80, 80), op=0.28 * float(m[int(by_), int(bx_), 0]))
    for i, (x, y, a, L, t0) in enumerate(specs):
        if t > t0:
            p = pore_near(120 + x, 300 + y, PORES2)
            v = 0.15 + 0.65 * eo((t - t0) / 0.5)
            mite(f, 0, 0, a, L * popk(t, t0, 0.3) if t - t0 < 0.3 else L, t, vis=v, emerge=(p[0] - 120, p[1] - 300), walk=1.5, phase=i, shadow=0.45)
    if t > E["t_itchy"] - 0.05:
        q = eo((t - E["t_itchy"] + 0.05) / 0.35)
        for k_ in range(3):
            x0, y0 = 300 + k_ * 70, 640 + k_ * 30
            x1, y1 = x0 + 380 * q, y0 + 380 * q
            cv2.line(f, (x0, y0), (int(x1), int(y1)), (0.95, 0.35, 0.35), 26, cv2.LINE_AA)
            cv2.line(f, (x0, y0), (int(x1), int(y1)), (1.0, 0.82, 0.82), 9, cv2.LINE_AA)
    tier(f, t, E["t_red"] - 0.06, "too many of them?", "RED & ITCHY", 1310, size=160, fill=(255, 84, 70), lo_size=56, gap=130)
    if t < E["t_red"] - 0.06:
        put(f, small("too many of them?", 56), CX, 1180, op=appear(t, E["t_many"] - 0.25))
    put_char(f, 840, 600, "cover" if t > E["t_itchy"] - 0.1 else "shock", "gross" if t > E["t_red"] else "wow", t, 0.5, shadow=False)
    return f


_EYE = {}


def eye_layer():
    if "e" in _EYE:
        return _EYE["e"]
    k = 2
    im = Image.new("RGBA", (W * k, H * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(4)

    def lid(x):
        u = (x - 510) / 470
        return 880 + 120 * (1 - u * u)
    # lid crease
    pts = [(x * k, (lid(x) - 230 + 40 * ((x - 510) / 470) ** 2) * k) for x in range(40, 1041, 20)]
    d.line(pts, fill=(150, 70, 60, 200), width=10 * k, joint="curve")
    # lashes
    for x in range(70, 1011, 13):
        y0 = lid(x)
        u = (x - 510) / 470
        L = 300 + 90 * (1 - abs(u)) + rng.uniform(-40, 40)
        ang = math.pi / 2 + u * 0.75 + rng.uniform(-0.08, 0.08)
        bend = 0.9 + rng.uniform(-0.2, 0.2)
        lp = []
        for i in range(16):
            v = i / 15
            a = ang + bend * v * v * (1 if u >= 0 else -1) * 0.8
            lp.append((x + math.cos(a) * L * v, y0 + math.sin(a) * L * v))
        for i in range(15):
            w = max(1, int((12 * (1 - i / 15) + 1.5) * k))
            d.line([(lp[i][0] * k, lp[i][1] * k), (lp[i + 1][0] * k, lp[i + 1][1] * k)], fill=(26, 16, 14, 255), width=w)
        d.line([(lp[1][0] * k - 2, lp[1][1] * k), (lp[6][0] * k - 2, lp[6][1] * k)], fill=(110, 80, 70, 160), width=2 * k)
    # lid margin
    pts = [(x * k, lid(x) * k) for x in range(30, 1051, 10)]
    d.line(pts, fill=(120, 40, 40, 255), width=12 * k, joint="curve")
    im = im.resize((W, H), Image.LANCZOS)
    _EYE["e"] = (to_np(im), lid)
    return _EYE["e"]


def shot_LS(t, n):
    s = SHOT["LS"]["start"]
    f = skin_view(160, 380, 1.25, SKIN2)
    (rgb, a), lid = eye_layer()
    # lower area (lid shadow) darker below the lash line
    m = np.clip((_yy - (880 + 120 * (1 - ((_xx - 510) / 470) ** 2))) / 60, 0, 1)[..., None]
    f = f * (1 - 0.35 * m)
    over(f, rgb, a, 0, 0)
    for j, (x, ang) in enumerate(((250, -1.25), (440, -1.6), (620, -1.5), (800, -1.9))):
        mite(f, x, lid(x) - 10 + 8 * math.sin(t * 3 + j), ang, 200, t, walk=1.4, phase=j, shadow=0.5, vis=1.0)
    if t > E["t_love"] - 0.1:
        for j, x in enumerate((250, 440, 620, 800)):
            hk = popk(t, E["t_love"] - 0.1 + j * 0.07, 0.32)
            put(f, heart(80), x, lid(x) - 240 - 30 * math.sin(t * 4 + j), op=clamp(hk * 3), sc=0.4 + 0.6 * hk)
    z = 1.0 + 0.06 * (t - s)
    return zoom_at(f, z, 510, 950)


_CARD = {}


def tip_card(done):
    key = done
    if key in _CARD:
        return _CARD[key]
    k = 2
    w, h = 840, 210
    im = Image.new("RGBA", ((w + 80) * k, (h + 90) * k), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([46 * k, 60 * k, (46 + w) * k, (60 + h) * k], 34 * k, fill=(0, 0, 0, 140))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14 * k)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40 * k, 40 * k, (40 + w) * k, (40 + h) * k], 34 * k, fill=(255, 255, 255, 255))
    d.rounded_rectangle([40 * k, 40 * k, (40 + w) * k, (40 + h * 0.45) * k], 34 * k, fill=(246, 250, 255, 255))
    d.rounded_rectangle([40 * k, 40 * k, 64 * k, (40 + h) * k], 12 * k, fill=(0, 178, 114, 255))
    bx, by = 100, 40 + h / 2
    d.rounded_rectangle([(bx - 38) * k, (by - 38) * k, (bx + 38) * k, (by + 38) * k], 14 * k, fill=(0, 178, 114, 255) if done else (255, 255, 255, 255),
                        outline=(0, 140, 90, 255), width=6 * k)
    if done:
        d.line([((bx - 20) * k, by * k), ((bx - 4) * k, (by + 18) * k), ((bx + 24) * k, (by - 20) * k)], fill=(255, 255, 255, 255), width=10 * k,
               joint="curve")
    f1 = ImageFont.truetype(IB, 50 * k); f2 = ImageFont.truetype(ISB, 36 * k)
    d.text((160 * k, (40 + 38) * k), "Remove eye makeup", font=f1, fill=(16, 20, 34, 255))
    d.text((160 * k, (40 + 112) * k), "before bed, every night", font=f2, fill=(70, 80, 100, 255))
    im = im.resize((im.width // k, im.height // k), Image.LANCZOS)
    _CARD[key] = im
    return im


_PROD = {}


def products():
    if "p" in _PROD:
        return _PROD["p"]
    k = 3
    im = Image.new("RGBA", (300 * k, 420 * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([60 * k, 110 * k, 190 * k, 380 * k], 30 * k, fill=(255, 150, 190, 235), outline=(20, 14, 20, 255), width=6 * k)
    d.rounded_rectangle([74 * k, 130 * k, 100 * k, 360 * k], 12 * k, fill=(255, 220, 236, 200))
    d.rectangle([100 * k, 66 * k, 150 * k, 112 * k], fill=(255, 255, 255, 255), outline=(20, 14, 20, 255), width=5 * k)
    d.rectangle([118 * k, 30 * k, 132 * k, 68 * k], fill=(255, 255, 255, 255), outline=(20, 14, 20, 255), width=4 * k)
    d.rectangle([132 * k, 30 * k, 176 * k, 44 * k], fill=(255, 255, 255, 255), outline=(20, 14, 20, 255), width=4 * k)
    d.rounded_rectangle([86 * k, 210 * k, 166 * k, 290 * k], 12 * k, fill=(255, 255, 255, 230))
    d.ellipse([110 * k, 232 * k, 142 * k, 268 * k], fill=(0, 178, 114, 255))
    for i in range(3):
        y = 330 + i * 26
        d.ellipse([170 * k, (y - 20) * k, 290 * k, (y + 18) * k], fill=(255, 255, 255, 255), outline=(170, 170, 190, 255), width=4 * k)
    im = im.resize((300, 420), Image.LANCZOS)
    _PROD["p"] = im
    return im


def shot_MK(t, n):
    s = SHOT["MK"]["start"]
    f = grad((0, 214, 160), (0, 64, 92), cy=0.50)
    disc(f, 510, 980, 330, (255, 206, 0), glow=0.45)
    sparkles(f, t, 41, n=18, op=0.8)
    put_char(f, 420, 1420, "wipe", "sleepsmile", t, 1.12, m=0)
    put(f, products(), 800, 1240, op=appear(t, s + 0.1), sc=0.9 + 0.1 * popk(t, s + 0.1))
    sparkles(f, t, 43, n=6, area=(430, 820, 560, 920), op=1, size=10)
    k = popk(t, E["t_always"] - 0.1, 0.38)
    if k > 0:
        put(f, tip_card(t > E["t_off"] - 0.02), 520, 470, op=clamp(k * 3), sc=0.7 + 0.3 * k, rot=2.0 * (1 - k) + 1.5)
        put(f, pill("SKIN TIP", 36, bg=(0, 150, 100), acc=(255, 230, 90)), 250, 345, op=clamp(k * 3))
    return f


def shot_LP(t, n):
    s, e = SHOT["LP"]["start"], SHOT["LP"]["end"]
    f = bedroom(t, "night")
    scared = t > E["t_alone"] - 0.05
    put_head(f, 300, 1120, "shock" if scared else "nervous", t, 1.15, 0, look=(1, 0), tilt=-60)
    blanket(f, "night", top=1150)
    if t > E["t_not"] - 0.1:
        for j, (x, y, a) in enumerate(((420, 1120, math.pi + 0.5), (470, 1180, math.pi - 0.1), (395, 1205, math.pi + 0.9))):
            q = popk(t, E["t_not"] - 0.1 + j * 0.18, 0.3)
            if q > 0.02:
                mite(f, x, y, a, 96 * q, t, walk=1.6, eyes=True, shadow=0.4, phase=j)
    u = eio((t - s) / (e - s))
    z = 1.0 + 0.55 * u + 2.2 * clamp((t - (e - 0.3)) / 0.3) ** 2
    f = zoom_at(f, z, 360, 1150, 510, lerp(1150, 900, u))
    if t > e - 0.18:
        q = clamp((t - (e - 0.18)) / 0.18)
        f = f * (1 - q * 0.85) + C((255, 60, 170)) * q * 0.85
    return f


RENDER = {k: globals()[f"shot_{k}"] for k in SHOT}


def rs(sid, t, n):
    s = SHOT[sid]
    tt = min(max(t, s["start"]), s["end"] - 1e-3)
    return RENDER[sid](tt, n)


# ---------------- camera ----------------
PUNCH = [(E["t_inside"], 0.08, 0.3), (E["t_right"], 0.05, 0.3), (E["t_demodex"], 0.06, 0.3), (E["t_every"], 0.05, 0.3), (E["t_mate"], 0.10, 0.35),
         (E["t_face"], 0.09, 0.35), (E["t_party"], 0.07, 0.3), (E["t_wake"], 0.06, 0.3), (E["t_mom"], 0.10, 0.35), (E["t_red"], 0.05, 0.3),
         (E["t_itchy"], 0.06, 0.3), (E["t_love"], 0.05, 0.3), (E["t_off"], 0.04, 0.3), (E["t_alone"], 0.06, 0.3), (E["t_headdown"], 0.03, 0.3)]
SHAKE = [(E["t_inside"], 14, 0.35), (E["t_mate"], 22, 0.45), (E["t_face"], 18, 0.4), (E["t_mom"], 24, 0.5), (E["t_itchy"], 14, 0.5),
         (E["t_party"], 10, 0.3), (SHOT["WK"]["start"] + 0.1, 7, 0.9), (E["t_alone"], 10, 0.35)]


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
