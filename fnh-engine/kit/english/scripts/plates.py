"""BODY FILES look — clean white-paper medical explainer kit (owner-approved direction, 26 Oct 2026).
White page, black + red editorial headlines, mono FIG labels, dark X-ray / MRI plates, colour textbook diagrams,
draw-on leader-line labels, stamps and badges. No mascot. All text centred at x=540, width <= 840.

Everything returns PIL RGBA images or works on float RGB frames (H x W x 3, 0..1)."""
import math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
CX = 540
MAXW = 840
FD = "/home/claude/reel-kit/assets/fonts_plate"
ANTON = f"{FD}/Anton-Regular.ttf"
MONO = f"{FD}/PlexMono-Bold.ttf"
MONOM = f"{FD}/PlexMono-Medium.ttf"
IB = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
IXB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
ISB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
INK = (18, 18, 22)
RED = (226, 36, 40)
GREY = (118, 122, 132)
LGREY = (226, 228, 233)
BLUE = (36, 110, 230)
GREEN = (20, 158, 88)
GOLD = (244, 180, 40)
PINK = (232, 108, 132)
IVORY = (244, 230, 204)
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def eo(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def eio(x):
    x = clamp(x); return 3 * x * x - 2 * x * x * x


def eback(x, s=1.6):
    x = clamp(x); x -= 1; return 1 + x * x * ((s + 1) * x + s)


def appear(t, t0, d=0.25):
    return eo((t - t0) / d) if t >= t0 else 0.0


def popk(t, t0, d=0.32):
    return eback((t - t0) / d) if t >= t0 else 0.0


def C(c):
    return np.array(c[:3], np.float32) / 255.0


def paper():
    return np.ones((H, W, 3), np.float32)


# ---------------- compositing ----------------
def to_np(im):
    a = np.asarray(im, np.float32) / 255.0
    return a[..., :3], a[..., 3]


def over(f, rgb, a, x, y, op=1.0):
    h, w = a.shape
    x, y = int(round(x)), int(round(y))
    xa, ya, xb, yb = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if xb <= xa or yb <= ya or op <= 0:
        return
    aa = a[ya - y:yb - y, xa - x:xb - x][..., None] * op
    f[ya:yb, xa:xb] = f[ya:yb, xa:xb] * (1 - aa) + rgb[ya - y:yb - y, xa - x:xb - x] * aa


def put(f, im, cx, cy, op=1.0, sc=1.0, rot=0.0):
    if op <= 0.003 or sc <= 0.01:
        return
    if abs(sc - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
    if abs(rot) > 0.05:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    rgb, a = to_np(im)
    over(f, rgb, a, cx - im.width / 2, cy - im.height / 2, op)


# ---------------- text ----------------
_F, _T = {}, {}


def font(fp, size):
    k = (fp, size)
    if k not in _F:
        _F[k] = ImageFont.truetype(fp, size)
    return _F[k]


def text_img(text, fp, size, fill=INK, track=0):
    key = ("t", text, fp, size, fill, track)
    if key in _T:
        return _T[key]
    fnt = font(fp, size)
    if track:
        widths = [fnt.getlength(ch) + track for ch in text]
        tw = int(sum(widths)) + 4
    else:
        tw = int(fnt.getlength(text)) + 4
    asc, desc = fnt.getmetrics()
    im = Image.new("RGBA", (tw + 8, asc + desc + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if track:
        x = 4
        for ch, wch in zip(text, widths):
            d.text((x, 4), ch, font=fnt, fill=fill + (255,))
            x += wch
    else:
        d.text((4, 4), text, font=fnt, fill=fill + (255,))
    _T[key] = im
    return im


def rich(parts, fp, size, gap=0):
    """one line from [(text, colour), ...]"""
    key = ("r", tuple(parts), fp, size, gap)
    if key in _T:
        return _T[key]
    ims = [text_img(t, fp, size, c) for t, c in parts]
    w = sum(i.width for i in ims) - 8 * (len(ims) - 1) + gap * (len(ims) - 1)
    h = max(i.height for i in ims)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    x = 0
    for i in ims:
        out.alpha_composite(i, (x, 0)); x += i.width - 8 + gap
    _T[key] = out
    return out


def fit(im, maxw=MAXW):
    return min(1.0, maxw / max(1, im.width))


def headline(f, t, t0, rows, y, size=118, lead=None, lead_size=46, out=None, line_gap=0.92):
    """editorial headline: optional small lead line + 1-2 rows of Anton parts [(text, colour)]"""
    if t < t0 or (out is not None and t > out + 0.25):
        return
    o = 1.0 if out is None else clamp(1 - (t - out) / 0.25)
    yy = y
    if lead:
        k = appear(t, t0, 0.25)
        li = text_img(lead, ISB, lead_size, (70, 74, 84))
        put(f, li, CX, yy + 14 * (1 - k), op=k * o, sc=fit(li))
        yy += lead_size * 1.25
    for i, parts in enumerate(rows):
        im = rich(parts, ANTON, size)
        k = appear(t, t0 + 0.08 + 0.1 * i, 0.32)
        put(f, im, CX, yy + im.height / 2 + 26 * (1 - k), op=k * o, sc=fit(im))
        yy += size * line_gap + 6


def mono(f, text, cx, cy, size=28, fill=GREY, op=1.0, track=2):
    im = text_img(text, MONO, size, fill, track)
    put(f, im, cx, cy, op=op, sc=fit(im))


def header(f, op=1.0, series="FRESHNESTHUB  ·  BODY FILES"):
    mono(f, series, CX, 298, 24, GREY, op=op, track=3)
    f[324:327, CX - 46:CX + 46] = f[324:327, CX - 46:CX + 46] * (1 - op) + C(RED) * op


def fig_label(f, text, cy, op=1.0):
    mono(f, text, CX, cy, 26, (92, 96, 106), op=op, track=2)


# ---------------- plates ----------------
_P = {}


def _shadow(im, r=26, a=90, dy=18):
    w, h = im.size
    pad = r * 2
    out = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    m = im.split()[3].point(lambda v: a if v > 0 else 0)
    sh.paste((20, 24, 40, 255), (pad, pad + dy), m)
    sh.putalpha(sh.split()[3].filter(ImageFilter.GaussianBlur(r)))
    out.alpha_composite(sh)
    out.alpha_composite(im, (pad, pad))
    return out


def plate_dark(w, h, label_l="", label_r=""):
    key = ("pd", w, h, label_l, label_r)
    if key in _P:
        return _P[key]
    k = 2
    im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
    yy, xx = np.mgrid[0:h * k, 0:w * k].astype(np.float32)
    d = np.sqrt(((xx / (w * k) - 0.5) * 1.1) ** 2 + ((yy / (h * k) - 0.45)) ** 2)
    g = np.clip(1 - d * 1.4, 0, 1)[..., None]
    col = (np.array([10, 18, 34]) * (1 - g) + np.array([26, 44, 74]) * g).astype(np.uint8)
    base = Image.fromarray(np.dstack([col, np.full(col.shape[:2], 255, np.uint8)]), "RGBA")
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * k - 1, h * k - 1], 30 * k, fill=255)
    im.paste(base, (0, 0), m)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([10 * k, 10 * k, (w - 10) * k, (h - 10) * k], 22 * k, outline=(120, 150, 190, 90), width=2 * k)
    for (x0, y0, sx, sy) in ((26, 26, 1, 1), (w - 26, 26, -1, 1), (26, h - 26, 1, -1), (w - 26, h - 26, -1, -1)):
        dr.line([(x0 * k, y0 * k), ((x0 + 30 * sx) * k, y0 * k)], fill=(170, 200, 235, 160), width=3 * k)
        dr.line([(x0 * k, y0 * k), (x0 * k, (y0 + 30 * sy) * k)], fill=(170, 200, 235, 160), width=3 * k)
    fm = font(MONO, 20 * k)
    if label_l:
        dr.text((40 * k, 40 * k), label_l, font=fm, fill=(170, 200, 235, 200))
    if label_r:
        tw = fm.getlength(label_r)
        dr.text(((w - 40) * k - tw, 40 * k), label_r, font=fm, fill=(170, 200, 235, 200))
    im = im.resize((w, h), Image.LANCZOS)
    _P[key] = _shadow(im, 24, 110, 16)
    return _P[key]


def plate_light(w, h, border=True):
    key = ("pl", w, h, border)
    if key in _P:
        return _P[key]
    k = 2
    im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([0, 0, w * k - 1, h * k - 1], 26 * k, fill=(255, 255, 255, 255),
                         outline=(205, 208, 216, 255) if border else None, width=2 * k)
    im = im.resize((w, h), Image.LANCZOS)
    _P[key] = _shadow(im, 22, 60, 12)
    return _P[key]


def stamp(text, col=RED, size=96, rot=-8):
    key = ("st", text, col, size, rot)
    if key in _P:
        return _P[key]
    fnt = font(ANTON, size)
    tw = int(fnt.getlength(text))
    asc, desc = fnt.getmetrics()
    w, h = tw + 70, asc + desc + 40
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 6, w - 7, h - 7], 14, outline=col + (255,), width=8)
    d.text((35, 14), text, font=fnt, fill=col + (255,))
    rng = np.random.default_rng(len(text))
    a = np.asarray(im).copy()
    holes = rng.random(a.shape[:2]) < 0.06
    a[..., 3] = np.where(holes, (a[..., 3] * 0.35).astype(np.uint8), a[..., 3])
    im = Image.fromarray(a).rotate(rot, resample=Image.BICUBIC, expand=True)
    _P[key] = im
    return im


def badge(text, col=GREEN, size=40, icon="check"):
    key = ("bd", text, col, size, icon)
    if key in _P:
        return _P[key]
    fnt = font(IXB, size)
    tw = int(fnt.getlength(text))
    h = int(size * 1.7)
    w = tw + h + 44
    k = 2
    im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w * k - 1, h * k - 1], h * k // 2, fill=col + (255,))
    r = h * 0.32
    cx, cy = h * 0.62, h / 2
    d.ellipse([(cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k], fill=(255, 255, 255, 255))
    if icon == "check":
        d.line([((cx - r * 0.5) * k, cy * k), ((cx - r * 0.1) * k, (cy + r * 0.4) * k), ((cx + r * 0.55) * k, (cy - r * 0.45) * k)],
               fill=col + (255,), width=int(4 * k), joint="curve")
    else:
        d.line([((cx - r * 0.45) * k, (cy - r * 0.45) * k), ((cx + r * 0.45) * k, (cy + r * 0.45) * k)], fill=col + (255,), width=int(4 * k))
        d.line([((cx + r * 0.45) * k, (cy - r * 0.45) * k), ((cx - r * 0.45) * k, (cy + r * 0.45) * k)], fill=col + (255,), width=int(4 * k))
    d.text(((h + 18) * k, (h - size * 1.22) / 2 * k), text, font=font(IXB, size * k), fill=(255, 255, 255, 255))
    im = _shadow(im.resize((w, h), Image.LANCZOS), 10, 70, 6)
    _P[key] = im
    return im


# ---------------- draw-on annotations ----------------
def leader(f, ax, ay, tx, ty, text, prog, size=26, col=INK, align="auto", tcol=None):
    """dot at anchor (ax,ay) -> elbow line to (tx,ty) -> mono caps label. prog 0..1 animates the draw-on."""
    if prog <= 0:
        return
    p1 = clamp(prog / 0.6)
    p2 = clamp((prog - 0.45) / 0.55)
    cv2.circle(f, (int(ax), int(ay)), 9, C(col).tolist(), -1, cv2.LINE_AA)
    cv2.circle(f, (int(ax), int(ay)), 15, C(col).tolist(), 2, cv2.LINE_AA)
    right = (tx >= ax) if align == "auto" else (align == "r")
    ex_ = tx - (40 if right else -40)
    segs = [(ax, ay, ex_, ty), (ex_, ty, tx, ty)]
    tot = sum(math.hypot(x1 - x0, y1 - y0) for x0, y0, x1, y1 in segs) or 1
    left = p1 * tot
    for x0, y0, x1, y1 in segs:
        L = math.hypot(x1 - x0, y1 - y0)
        if left <= 0 or L == 0:
            continue
        u = min(1.0, left / L)
        cv2.line(f, (int(x0), int(y0)), (int(x0 + (x1 - x0) * u), int(y0 + (y1 - y0) * u)), C(col).tolist(), 3, cv2.LINE_AA)
        left -= L
    if p2 > 0:
        im = text_img(text, MONO, size, tcol or col, 2)
        x = tx + 10 if right else tx - 10 - im.width
        rgb, a = to_np(im)
        over(f, rgb, a, x, ty - im.height / 2, op=p2)


def arrow(f, x0, y0, x1, y1, prog=1.0, col=INK, w=6, head=24):
    if prog <= 0:
        return
    ex, ey = x0 + (x1 - x0) * prog, y0 + (y1 - y0) * prog
    cv2.line(f, (int(x0), int(y0)), (int(ex), int(ey)), C(col).tolist(), w, cv2.LINE_AA)
    if prog > 0.85:
        a = math.atan2(y1 - y0, x1 - x0)
        for s in (-1, 1):
            q = (int(ex - head * math.cos(a + s * 0.5)), int(ey - head * math.sin(a + s * 0.5)))
            cv2.line(f, (int(ex), int(ey)), q, C(col).tolist(), w, cv2.LINE_AA)


def ring_pulse(f, cx, cy, t, t0, rmax=180, dur=0.5, col=RED, th=6):
    q = (t - t0) / dur
    if 0 <= q <= 1:
        cv2.circle(f, (int(cx), int(cy)), int(20 + rmax * eo(q)), (C(col) * 1).tolist(), max(1, int(th * (1 - q))), cv2.LINE_AA)


# ---------------- X-ray hand ----------------
def _hand_bones(pull=0.0):
    """normalised bone list for a right hand, palm view, wrist at bottom. pull separates the index MCP joint."""
    bones = []
    carp = [(0.43, 0.83), (0.50, 0.835), (0.57, 0.835), (0.62, 0.82), (0.46, 0.885), (0.53, 0.89), (0.59, 0.88), (0.40, 0.87)]
    for (x, y) in carp:
        bones.append(((x, y), (x, y + 0.005), 0.030, 0.030))
    bones.append(((0.47, 0.93), (0.47, 1.05), 0.042, 0.048))   # radius
    bones.append(((0.60, 0.93), (0.61, 1.05), 0.030, 0.034))   # ulna
    fingers = [  # base(mc start), mcp, lengths prox/mid/dist, width
        ((0.455, 0.80), (0.400, 0.535), (0.135, 0.085, 0.060), 0.026),   # index
        ((0.505, 0.80), (0.500, 0.505), (0.150, 0.095, 0.064), 0.027),   # middle
        ((0.560, 0.80), (0.598, 0.530), (0.140, 0.090, 0.062), 0.025),   # ring
        ((0.610, 0.79), (0.690, 0.585), (0.110, 0.070, 0.055), 0.022),   # little
    ]
    joints = {}
    for i, (b0, mcp, ls, w) in enumerate(fingers):
        dx, dy = mcp[0] - b0[0], mcp[1] - b0[1]
        n = math.hypot(dx, dy); ux, uy = dx / n, dy / n
        bones.append((b0, mcp, w * 1.05, w * 1.25))
        g = pull * 0.045 if i == 0 else 0.0
        p = (mcp[0] + ux * (0.022 + g), mcp[1] + uy * (0.022 + g))
        joints[i] = ((mcp[0] + p[0]) / 2, (mcp[1] + p[1]) / 2)
        for j, L in enumerate(ls):
            q = (p[0] + ux * L, p[1] + uy * L)
            bones.append((p, q, w * (1.0 - 0.12 * j), w * (0.9 - 0.15 * j)))
            p = (q[0] + ux * 0.016, q[1] + uy * 0.016)
    # thumb
    t0, t1 = (0.40, 0.81), (0.300, 0.665)
    bones.append((t0, t1, 0.028, 0.030))
    ux, uy = (t1[0] - t0[0]), (t1[1] - t0[1]); n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
    p = (t1[0] + ux * 0.02, t1[1] + uy * 0.02)
    for j, L in enumerate((0.10, 0.07)):
        q = (p[0] + ux * L, p[1] + uy * L)
        bones.append((p, q, 0.026 - 0.004 * j, 0.022 - 0.005 * j)); p = (q[0] + ux * 0.016, q[1] + uy * 0.016)
    return bones, joints


_XR = {}


def xray_hand(w, h, pull=0.0, mirror=False, glow=0.0, tint=(0.80, 0.92, 1.0), wear=0.0):
    """dark plate content (no plate frame): returns RGB float (h,w,3). pull 0..1 opens the index knuckle."""
    key = (w, h, round(pull, 2), mirror, round(glow, 2), tint, round(wear, 2))
    if key in _XR:
        return _XR[key]
    k = 2
    W2, H2 = w * k, h * k
    bones, joints = _hand_bones(pull)
    m = Image.new("L", (W2, H2), 0)
    d = ImageDraw.Draw(m)
    s = min(W2 * 1.4, H2 / 0.98)
    ox, oy = W2 / 2 - 0.50 * s, H2 / 2 - 0.60 * s * 1.05

    def P(p):
        return (ox + p[0] * s, oy + p[1] * s * 1.05)
    for (p0, p1, r0, r1) in bones:
        a, b = P(p0), P(p1)
        R0, R1 = r0 * s * 1.12, r1 * s * 1.12
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        mr = min(R0, R1) * 0.62
        d.polygon([(a[0] + nx * mr, a[1] + ny * mr), (b[0] + nx * mr, b[1] + ny * mr), (b[0] - nx * mr, b[1] - ny * mr),
                   (a[0] - nx * mr, a[1] - ny * mr)], fill=255)
        d.ellipse([a[0] - R0, a[1] - R0, a[0] + R0, a[1] + R0], fill=255)
        d.ellipse([b[0] - R1, b[1] - R1, b[0] + R1, b[1] + R1], fill=255)
    M = np.asarray(m, np.uint8)
    dist = cv2.distanceTransform((M > 127).astype(np.uint8), cv2.DIST_L2, 5)
    inside = (M > 127).astype(np.float32)
    I = inside * (0.40 + 0.55 * np.exp(-dist / (5.0 * k)))
    rng = np.random.default_rng(3)
    tex = cv2.GaussianBlur(rng.standard_normal((H2, W2)).astype(np.float32), (0, 0), 2.2 * k)
    I = I * (1 + 0.10 * tex)
    soft = cv2.GaussianBlur(cv2.dilate(M, np.ones((int(46 * k), int(46 * k)), np.uint8)).astype(np.float32) / 255, (0, 0), 16 * k) * 0.16
    I = np.maximum(I, soft)
    bloom = cv2.GaussianBlur(I, (0, 0), 9 * k) * 0.45
    I = np.clip(I + bloom, 0, 1.2)
    rgb = np.dstack([I * tint[0], I * tint[1], I * tint[2]])
    if glow > 0 or wear > 0:
        jx, jy = P(joints[0])
        dd = np.sqrt((np.arange(W2)[None, :] - jx) ** 2 + (np.arange(H2)[:, None] - jy) ** 2)
        if glow > 0:
            gg = np.exp(-(dd / (34 * k)) ** 2)[..., None] * glow
            rgb = rgb * (1 - gg * 0.4) + np.array([1.0, 0.55, 0.35]) * gg
    rgb = cv2.resize(rgb.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA)
    if mirror:
        rgb = rgb[:, ::-1]
    out = np.clip(rgb, 0, 1)
    if len(_XR) > 400:
        _XR.clear()
    _XR[key] = (out, (joints, s / k, ox / k, oy / k))
    return _XR[key]


def hand_joint_xy(info, i, w, mirror=False):
    joints, s, ox, oy = info
    x, y = ox + joints[i][0] * s, oy + joints[i][1] * s * 1.05
    return (w - x if mirror else x), y


def dark_plate_with(f, img, cx, cy, label_l="", label_r="", op=1.0):
    """frame + content: img is RGB float (h,w,3) that fills the plate interior"""
    h, w = img.shape[:2]
    pl = plate_dark(w, h, label_l, label_r)
    rgb, a = to_np(pl)
    pad = (pl.width - w) // 2
    x0, y0 = cx - pl.width / 2, cy - pl.height / 2
    over(f, rgb, a, x0, y0, op)
    # interior: content, rounded mask
    key = ("mask", w, h)
    if key not in _P:
        mk = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mk).rounded_rectangle([12, 12, w - 13, h - 13], 22, fill=255)
        _P[key] = np.asarray(mk, np.float32) / 255
    m = _P[key]
    bg = rgb[pad:pad + h, pad:pad + w]
    comp = np.maximum(bg, img) * m[..., None] + bg * (1 - m[..., None])
    over(f, comp, a[pad:pad + h, pad:pad + w], x0 + pad, y0 + pad, op)
    # re-draw the frame's corner marks/labels on top
    over(f, rgb[pad:pad + h, pad:pad + w], (a[pad:pad + h, pad:pad + w] * (rgb[pad:pad + h, pad:pad + w].mean(2) > 0.5)), x0 + pad, y0 + pad, op)
    return x0 + pad, y0 + pad


# ---------------- knuckle joint diagram (colour textbook / MRI) ----------------
_J = {}


def joint_img(gap=0.0, fluid=1.0, cav=0.0, cap=1.0, bones=1.0, mode="color", size=760):
    """sagittal section of a knuckle (MCP) joint. gap in px (0..60), cav 0..1 bubble size, cap = capsule draw-on 0..1.
    mode 'color' -> RGBA on transparent; 'mri' -> RGB float grayscale MRI look."""
    key = (round(gap), round(fluid, 2), round(cav, 2), round(cap, 2), round(bones, 2), mode, size)
    if key in _J:
        return _J[key]
    k = 2
    S = size * k
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32) / k
    cx = size / 2
    g = gap
    hy = 470.0
    head = (np.abs(xx - cx) <= 100) & (yy >= hy) | (((xx - cx) ** 2 + (yy - hy) ** 2) <= 122 ** 2)
    head &= yy >= hy - 122
    phal_rect = (np.abs(xx - cx) <= 92) & (yy <= 360 - g)
    flare = (((xx - cx) / 118) ** 2 + ((yy - (368 - g)) / 50) ** 2) <= 1
    socket = ((xx - cx) ** 2 + (yy - (hy - g)) ** 2) <= 131 ** 2
    phal = (phal_rect | flare) & ~socket
    cart_h = head & ((((xx - cx) ** 2 + (yy - hy) ** 2) >= 106 ** 2) & (yy < hy + 10))
    cart_p = phal & (((xx - cx) ** 2 + (yy - (hy - g)) ** 2) <= 146 ** 2)
    capsule = (((xx - cx) / (190 + 0)) ** 2 + ((yy - (hy - 95 - g / 2)) / (160 + g / 2)) ** 2) <= 1
    cap_edge = capsule & ~((((xx - cx) / 178) ** 2 + ((yy - (hy - 95 - g / 2)) / (148 + g / 2)) ** 2) <= 1)
    fluid_m = capsule & ~head & ~phal
    cyc = (hy - 122 + (hy - g - 131)) / 2
    bub_r = max(0.0, cav) * 1.0
    bub = (((xx - cx) / (70 * bub_r + 1e-3)) ** 2 + ((yy - cyc) / ((g / 2 + 10) * bub_r + 1e-3)) ** 2) <= 1 if bub_r > 0.02 else np.zeros_like(head)
    rng = np.random.default_rng(7)
    tex = cv2.GaussianBlur(rng.standard_normal((S, S)).astype(np.float32), (0, 0), 3 * k)
    tex2 = cv2.GaussianBlur(rng.standard_normal((S, S)).astype(np.float32), (0, 0), 1.2 * k)
    bonem = (head | phal).astype(np.float32)
    dist = cv2.distanceTransform((bonem > 0).astype(np.uint8), cv2.DIST_L2, 5) / k
    if mode == "mri":
        I = np.zeros((S, S), np.float32) + 0.06
        I = np.where(capsule, 0.22, I)
        I = np.where(fluid_m, 0.88 * fluid + 0.22 * (1 - fluid), I)
        marrow = 0.50 + 0.10 * tex
        cort = dist < 9
        I = np.where(bonem > 0, np.where(cort, 0.10, marrow), I)
        I = np.where(cart_h | cart_p, 0.62, I)
        I = np.where(bub, 0.02, I)
        I = cv2.GaussianBlur(I, (0, 0), 1.6 * k) + 0.035 * tex2
        I = cv2.resize(I, (size, size), interpolation=cv2.INTER_AREA)
        out = np.clip(np.dstack([I, I, I * 1.02]), 0, 1).astype(np.float32)
        _J[key] = out
        return out
    rgba = np.zeros((S, S, 4), np.float32)

    def paint(mask, col, a=1.0):
        m = mask.astype(np.float32)[..., None] * a
        rgba[..., :3] = rgba[..., :3] * (1 - m) + np.array(col[:3], np.float32) / 255 * m
        rgba[..., 3:] = rgba[..., 3:] * (1 - m) + m
    # capsule fill + fluid
    paint(capsule, (255, 214, 222), 0.55 * cap)
    paint(fluid_m, (250, 208, 96), 0.75 * fluid * cap)
    # bones (trabecular ivory)
    if bones > 0:
        trab = np.clip((tex2 - 0.9) * 0.6, 0, 1) * 0.22 + np.clip(tex * 0.08, -0.05, 0.05)
        bcol = np.array(IVORY, np.float32) / 255 * (1 - trab[..., None]) * (0.93 + 0.07 * tex[..., None])
        edge = np.clip(1 - dist / 10, 0, 1)[..., None]
        bcol = bcol * (1 - edge * 0.25) + np.array([0.62, 0.50, 0.36]) * edge * 0.25
        m = bonem[..., None] * bones
        rgba[..., :3] = rgba[..., :3] * (1 - m) + bcol * m
        rgba[..., 3:] = np.maximum(rgba[..., 3:], m)
        paint(cart_h | cart_p, (150, 200, 240), bones)
        outl = (dist > 0) & (dist < 2.2)
        paint(outl, (120, 92, 66), bones)
    # capsule outline draw-on (angle sweep)
    if cap > 0:
        ang = (np.degrees(np.arctan2(yy - (hy - 95 - g / 2), xx - cx)) + 270) % 360
        paint(cap_edge & (ang <= 360 * cap), PINK, 1.0)
    if bub_r > 0.02:
        paint(bub, (255, 255, 255), 0.97)
        be = bub & ~((((xx - cx) / (70 * bub_r - 4 + 1e-3)) ** 2 + ((yy - cyc) / max(1, (g / 2 + 10) * bub_r - 3)) ** 2) <= 1)
        paint(be, (120, 170, 220), 1.0)
        hl = (((xx - (cx - 30 * bub_r)) / (14 * bub_r + 1e-3)) ** 2 + ((yy - (cyc - (g / 2) * 0.3 * bub_r)) / (5 * bub_r + 1e-3)) ** 2) <= 1
        paint(hl & bub, (255, 255, 255), 1.0)
    im = Image.fromarray((np.clip(rgba, 0, 1) * 255).astype(np.uint8), "RGBA").resize((size, size), Image.LANCZOS)
    if len(_J) > 300:
        _J.clear()
    _J[key] = im
    return im


JOINT_INFO = dict(hy=470, cx=380)   # in diagram px (size 760) — for placing labels


# ---------------- small icons ----------------
def clock_icon(prog, r=110):
    key = ("clk", round(prog, 2), r)
    if key in _P:
        return _P[key]
    k = 3
    S = (r * 2 + 20) * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = S / 2
    R = r * k
    d.ellipse([c - R, c - R, c + R, c + R], fill=(255, 255, 255, 255), outline=INK + (255,), width=7 * k)
    if prog > 0:
        d.pieslice([c - R + 14 * k, c - R + 14 * k, c + R - 14 * k, c + R - 14 * k], -90, -90 + 360 * prog * 0.5, fill=(255, 220, 220, 255))
    for i in range(12):
        a = i / 12 * 2 * math.pi
        r0 = R - (24 if i % 3 == 0 else 16) * k
        d.line([(c + math.cos(a) * r0, c + math.sin(a) * r0), (c + math.cos(a) * (R - 8 * k), c + math.sin(a) * (R - 8 * k))], fill=INK + (255,),
               width=(5 if i % 3 == 0 else 3) * k)
    a = -math.pi / 2 + 2 * math.pi * prog * 0.5
    d.line([(c, c), (c + math.cos(a) * R * 0.72, c + math.sin(a) * R * 0.72)], fill=RED + (255,), width=7 * k)
    d.line([(c, c), (c, c - R * 0.45)], fill=INK + (255,), width=8 * k)
    d.ellipse([c - 9 * k, c - 9 * k, c + 9 * k, c + 9 * k], fill=INK + (255,))
    im = im.resize((S // k, S // k), Image.LANCZOS)
    _P[key] = im
    return im


def hand_icon(swell=0.0, size=260):
    key = ("hand", round(swell, 2), size)
    if key in _P:
        return _P[key]
    k = 3
    S = size * k
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    u = S / 100
    d.rounded_rectangle([28 * u, 44 * u, 74 * u, 92 * u], 16 * u, fill=255)
    for i, (x, h) in enumerate(((30, 34), (41, 26), (52, 24), (63, 30))):
        d.rounded_rectangle([x * u, h * u, (x + 10) * u, 60 * u], 5 * u, fill=255)
    d.rounded_rectangle([12 * u, 50 * u, 24 * u, 74 * u], 6 * u, fill=255)
    d.polygon([(18 * u, 72 * u), (30 * u, 66 * u), (30 * u, 82 * u)], fill=255)
    M = np.asarray(m, np.float32) / 255
    out = np.zeros((S, S, 4), np.float32)
    if swell > 0:
        halo = cv2.GaussianBlur(cv2.dilate(M, np.ones((int(9 * u), int(9 * u)), np.uint8)), (0, 0), 3 * u) * swell
        out[..., :3] = np.array(RED) / 255
        out[..., 3] = np.clip(halo * 0.55, 0, 1)
    edge = cv2.dilate(M, np.ones((int(2.2 * u), int(2.2 * u)), np.uint8)) - M
    fillc = np.array([255, 232, 214]) / 255
    mm = M[..., None]
    out[..., :3] = out[..., :3] * (1 - mm) + fillc * mm
    out[..., 3] = np.maximum(out[..., 3], M)
    e = np.clip(edge, 0, 1)[..., None]
    out[..., :3] = out[..., :3] * (1 - e) + np.array(INK) / 255 * e
    out[..., 3] = np.maximum(out[..., 3], e[..., 0])
    im = Image.fromarray((out * 255).astype(np.uint8), "RGBA").resize((size, size), Image.LANCZOS)
    _P[key] = im
    return im


def gauge_icon(val=1.0, size=260):
    key = ("gauge", round(val, 2), size)
    if key in _P:
        return _P[key]
    k = 3
    S = size * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c, cy = S / 2, S * 0.62
    R = S * 0.40
    for i in range(40):
        a0 = math.pi + math.pi * i / 40
        col = (int(226 - 200 * i / 40), int(60 + 120 * i / 40), 70, 255)
        d.arc([c - R, cy - R, c + R, cy + R], math.degrees(a0), math.degrees(a0 + math.pi / 40) + 0.5, fill=col, width=int(S * 0.07))
    a = math.pi + math.pi * val
    d.line([(c, cy), (c + math.cos(a) * R * 0.8, cy + math.sin(a) * R * 0.8)], fill=INK + (255,), width=int(S * 0.03))
    d.ellipse([c - S * 0.04, cy - S * 0.04, c + S * 0.04, cy + S * 0.04], fill=INK + (255,))
    im = im.resize((size, size), Image.LANCZOS)
    _P[key] = im
    return im


def tip_card(title, sub, done, w=820, h=230, strip=RED):
    key = ("tip", title, sub, done, w, h, strip)
    if key in _P:
        return _P[key]
    k = 2
    im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w * k - 1, h * k - 1], 30 * k, fill=(255, 255, 255, 255), outline=(210, 213, 220, 255), width=2 * k)
    d.rounded_rectangle([0, 0, 26 * k, h * k - 1], 12 * k, fill=strip + (255,))
    bx, by = 104, h / 2
    d.rounded_rectangle([(bx - 40) * k, (by - 40) * k, (bx + 40) * k, (by + 40) * k], 14 * k, fill=(GREEN if done else (255, 255, 255)) + (255,),
                        outline=GREEN + (255,), width=6 * k)
    if done:
        d.line([((bx - 20) * k, by * k), ((bx - 4) * k, (by + 18) * k), ((bx + 24) * k, (by - 20) * k)], fill=(255, 255, 255, 255), width=10 * k,
               joint="curve")
    d.text((176 * k, (h / 2 - 66) * k), title, font=font(IB, 52 * k), fill=INK + (255,))
    d.text((176 * k, (h / 2 + 8) * k), sub, font=font(ISB, 40 * k), fill=(80, 86, 100, 255))
    im = _shadow(im.resize((w, h), Image.LANCZOS), 18, 70, 12)
    _P[key] = im
    return im


def guides(f):
    red = np.array([1.0, 0.1, 0.1], np.float32)
    for (x0, y0, x1, y1) in ((0, 0, W, 250), (0, H - 420, W, H), (W - 120, 0, W, H), (0, 0, 60, H)):
        f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * 0.6 + red * 0.4
    cv2.line(f, (CX, 0), (CX, H), (0.1, 0.6, 1.0), 1)
    return f
