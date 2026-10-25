"""Shared drawing helpers: text elements, compositing, cards, easing."""
import math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FD = "/usr/share/fonts/opentype/inter/"
F_BLACK = FD + "InterDisplay-Black.otf"
F_XB = FD + "InterDisplay-ExtraBold.otf"
F_BOLD = FD + "InterDisplay-Bold.otf"
F_SEMI = FD + "InterDisplay-SemiBold.otf"
AMBER = (255, 196, 61)
WHITE = (255, 255, 255)
INK = (18, 15, 12)
GREY = (150, 146, 140)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def eo(x):  # ease out cubic
    x = clamp(x); return 1 - (1 - x) ** 3


def eio(x):
    x = clamp(x); return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def eback(x, s=1.70158):
    x = clamp(x); c3 = s + 1
    return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2


def win(t, t0, d):  # 0..1 progress
    return clamp((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)


_fonts = {}


def font(path, size):
    k = (path, int(size))
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(path, int(size))
    return _fonts[k]


def run_w(text, f, tr):
    if tr == 0:
        return f.getlength(text)
    return sum(f.getlength(c) for c in text) + tr * (len(text) - 1)


_cache = {}


def text_el(lines, align="center", line_h=1.12, shadow=0.8, pad=34, key=None):
    """lines: [(runs, font_path, size, tracking)], runs: [(text, rgb, alpha)] -> (premult rgb, alpha)"""
    k = key or repr((lines, align, line_h, shadow, pad))
    if k in _cache:
        return _cache[k]
    mets = []
    for runs, fp, size, tr in lines:
        f = font(fp, size)
        sp = f.getlength(" ") + tr
        ws = [run_w(t, f, tr) for t, _, _ in runs]
        mets.append((f, sp, ws, sum(ws) + sp * (len(runs) - 1), size))
    tw = int(max(m[3] for m in mets)) + 2 * pad
    th = int(sum(m[4] * line_h for m in mets)) + 2 * pad
    rgb = np.zeros((th, tw, 3), np.float32)
    alpha = np.zeros((th, tw), np.float32)
    y = pad
    for (runs, fp, size, tr), (f, sp, ws, lw, _) in zip(lines, mets):
        x = pad + ((tw - 2 * pad - lw) / 2 if align == "center" else (tw - 2 * pad - lw if align == "right" else 0))
        cap = f.getbbox("H")
        ty = y + (size * line_h - (cap[3] - cap[1])) / 2 - cap[1]
        for (text, col, a), w in zip(runs, ws):
            m = Image.new("L", (tw, th), 0)
            d = ImageDraw.Draw(m)
            if tr == 0:
                d.text((x, ty), text, font=f, fill=255)
            else:
                cx = x
                for c in text:
                    d.text((cx, ty), c, font=f, fill=255)
                    cx += f.getlength(c) + tr
            mk = np.asarray(m, np.float32) / 255 * a
            rgb += mk[..., None] * (np.array(col, np.float32) / 255)
            alpha = np.maximum(alpha, mk)
            x += w + sp
        y += size * line_h
    if shadow:
        aimg = Image.fromarray((np.clip(alpha, 0, 1) * 255).astype(np.uint8))
        s1 = np.asarray(aimg.filter(ImageFilter.GaussianBlur(14)), np.float32) / 255
        s2 = np.asarray(aimg.filter(ImageFilter.GaussianBlur(3)), np.float32) / 255
        s1 = np.roll(s1, 6, axis=0); s2 = np.roll(s2, 2, axis=0)
        sh = np.clip(s1 * 0.85 * shadow + s2 * 0.5 * shadow, 0, 1)
        alpha = alpha + sh * (1 - alpha)
    el = (rgb, alpha)
    _cache[k] = el
    return el


def T(text, fp=F_BLACK, size=80, col=WHITE, a=1.0, tr=0, shadow=0.8, pad=34):
    return text_el([([(text, col, a)], fp, size, tr)], shadow=shadow, pad=pad)


def comp(frame, el, cx, cy, scale=1.0, op=1.0, anchor="c"):
    """anchor: c (center), l (left-middle), r (right-middle)"""
    if op <= 0.003 or el is None:
        return
    pm, a = el
    if abs(scale - 1) > 1e-3:
        h0, w0 = a.shape
        sz = (max(1, int(w0 * scale)), max(1, int(h0 * scale)))
        pm = cv2.resize(pm, sz, interpolation=cv2.INTER_LINEAR)
        a = cv2.resize(a, sz, interpolation=cv2.INTER_LINEAR)
    h, w = a.shape
    if anchor == "c":
        x0 = cx - w / 2
    elif anchor == "l":
        x0 = cx
    else:
        x0 = cx - w
    x0 = int(round(x0)); y0 = int(round(cy - h / 2))
    fx0, fy0, fx1, fy1 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if fx1 <= fx0 or fy1 <= fy0:
        return
    pa = a[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0] * op
    pp = pm[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0] * op
    reg = frame[fy0:fy1, fx0:fx1]
    frame[fy0:fy1, fx0:fx1] = reg * (1 - pa[..., None]) + pp


_masks = {}


def rrect_mask(w, h, r, sc=3):
    k = (w, h, r)
    if k not in _masks:
        m = Image.new("L", (w * sc, h * sc), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, w * sc - 1, h * sc - 1], r * sc, fill=255)
        b = Image.new("L", (w * sc, h * sc), 0)
        ImageDraw.Draw(b).rounded_rectangle([0, 0, w * sc - 1, h * sc - 1], r * sc, outline=255, width=2 * sc)
        _masks[k] = (np.asarray(m.resize((w, h), Image.LANCZOS), np.float32) / 255,
                     np.asarray(b.resize((w, h), Image.LANCZOS), np.float32) / 255)
    return _masks[k]


def card(frame, x0, y0, x1, y1, op, r=34, dark=0.40):
    if op <= 0.003:
        return
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    y0c, y1c = max(0, y0), min(H, y1)
    if y1c <= y0c:
        return
    m, b = rrect_mask(x1 - x0, y1 - y0, r)
    m = m[y0c - y0:y1c - y0]; b = b[y0c - y0:y1c - y0]
    reg = frame[y0c:y1c, x0:x1]
    blur = cv2.GaussianBlur(reg, (0, 0), 22)
    tint = blur * dark + np.array([0.03, 0.025, 0.02], np.float32)
    mm = (m * op)[..., None]
    out = reg * (1 - mm) + tint * mm
    bb = (b * 0.2 * op)[..., None]
    frame[y0c:y1c, x0:x1] = out * (1 - bb) + bb


def fill_rrect(frame, x0, y0, x1, y1, col, op=1.0, r=20):
    x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
    if x1 - x0 < 2 or y1 - y0 < 2 or op <= 0:
        return
    r = min(r, (x1 - x0) // 2, (y1 - y0) // 2)
    m, _ = rrect_mask(x1 - x0, y1 - y0, max(1, r))
    fx0, fy0, fx1, fy1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if fx1 <= fx0 or fy1 <= fy0:
        return
    m = m[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0] * op
    c = np.array(col, np.float32) / 255 if max(col) > 1 else np.array(col, np.float32)
    reg = frame[fy0:fy1, fx0:fx1]
    frame[fy0:fy1, fx0:fx1] = reg * (1 - m[..., None]) + c * m[..., None]


def pill_el(text, size=40, bg=AMBER, fg=INK, padx=34, h=None, fp=F_BLACK, tr=1, icon=None):
    k = ("pill", text, size, bg, fg, padx, h, fp, tr, icon)
    if k in _cache:
        return _cache[k]
    f = font(fp, size)
    tw = run_w(text, f, tr)
    h = h or int(size * 1.75)
    iw = int(size * 1.1) if icon else 0
    w = int(tw + 2 * padx + iw)
    sc = 3
    im = Image.new("RGBA", (w * sc, h * sc), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w * sc - 1, h * sc - 1], h * sc // 2, fill=tuple(bg) + (255,))
    if icon == "pin":
        px, py, rr = (padx + size * 0.35) * sc, h * sc / 2 - size * 0.12 * sc, size * 0.3 * sc
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=tuple(fg) + (255,))
        d.polygon([(px - rr * .82, py + rr * .5), (px + rr * .82, py + rr * .5), (px, py + rr * 2.1)], fill=tuple(fg) + (255,))
        d.ellipse([px - rr * .4, py - rr * .4, px + rr * .4, py + rr * .4], fill=tuple(bg) + (255,))
    if icon == "send":
        px, py, s = (padx + size * 0.1) * sc, h * sc / 2, size * 0.75 * sc
        d.polygon([(px, py - s * 0.45), (px + s, py), (px, py + s * 0.45), (px + s * 0.22, py)], fill=tuple(fg) + (255,))
    if icon == "dot":
        px, py, rr = (padx + size * 0.25) * sc, h * sc / 2, size * 0.22 * sc
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=AMBER + (255,))
    im = im.resize((w, h), Image.LANCZOS)
    a = np.asarray(im, np.float32) / 255
    pm, al = a[..., :3] * a[..., 3:4], a[..., 3].copy()
    t = text_el([([(text, fg, 1.0)], fp, size, tr)], shadow=0, pad=0)
    th, tww = t[1].shape
    y0 = max(0, (h - th) // 2); x0 = padx + iw
    hh = min(th, h - y0); ww = min(tww, w - x0)
    pm[y0:y0 + hh, x0:x0 + ww] = pm[y0:y0 + hh, x0:x0 + ww] * (1 - t[1][:hh, :ww, None]) + t[0][:hh, :ww]
    el = (pm, al)
    _cache[k] = el
    return el


def ring_el(progress, r=80, stroke=14):
    sc = 3
    size = (2 * r + stroke + 8) * sc
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size / 2; R = r * sc
    bb = [c - R, c - R, c + R, c + R]
    d.ellipse(bb, outline=(255, 255, 255, 60), width=stroke * sc)
    if progress > 0.002:
        ang = 360 * progress
        d.arc(bb, -90, -90 + ang, fill=AMBER + (255,), width=stroke * sc)
        for a_ in (-90, -90 + ang):
            rr = R - stroke * sc / 2
            px = c + rr * math.cos(math.radians(a_)); py = c + rr * math.sin(math.radians(a_))
            h = stroke * sc / 2
            d.ellipse([px - h, py - h, px + h, py + h], fill=AMBER + (255,))
    im = im.resize((size // sc, size // sc), Image.LANCZOS)
    a = np.asarray(im, np.float32) / 255
    return a[..., :3] * a[..., 3:4], a[..., 3]


# ---- graphic background ----
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_g = np.exp(-(((_xx - W / 2) / 700) ** 2 + ((_yy - 520) / 650) ** 2))
_v = 1 - 0.35 * np.clip(((_xx - W / 2) / (W / 2)) ** 2 * 0.6 + ((_yy - H / 2) / (H / 2)) ** 2, 0, 1.5)
BG_BASE = (np.array([0.045, 0.040, 0.036], np.float32)[None, None] +
           _g[..., None] * np.array([0.13, 0.085, 0.03], np.float32)[None, None]) * _v[..., None]
_dots = np.zeros((H, W), np.float32)
for y in range(18, H, 36):
    for x in range(18, W, 36):
        cv2.circle(_dots, (x, y), 1, 1.0, -1, cv2.LINE_AA)
BG_BASE = BG_BASE + _dots[..., None] * 0.035
_rng = np.random.default_rng(11)
GRAIN = [(_rng.standard_normal((H // 2, W // 2)).astype(np.float32) * 0.012) for _ in range(6)]


def graphic_bg(n):
    g = cv2.resize(GRAIN[n % 6], (W, H), interpolation=cv2.INTER_NEAREST)
    return np.clip(BG_BASE + g[..., None], 0, 1).astype(np.float32)


def add_grain(f, n, amt=1.0):
    g = cv2.resize(GRAIN[(n + 3) % 6], (W, H), interpolation=cv2.INTER_NEAREST) * amt
    return f + g[..., None]
