# ================= base: timeline, sets, typography, square-face mascot, props =================
import sys, json, math, re
import numpy as np, cv2, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{R}/lib")
from gfx import W, H, WHITE, F_BLACK, F_XB, F_BOLD, F_SEMI, clamp, eo, eio, eback, font, comp, add_grain

FPS = 24
F_LIL = f"{R}/fonts/lilita/package/files/lilita-one-latin-400-normal.woff"
F_ANTON = f"{R}/fonts/anton/package/files/anton-latin-400-normal.woff"
F_PF = f"{R}/fonts/playfair/package/files/playfair-display-latin-700-normal.woff"
F_PFI = f"{R}/fonts/playfair/package/files/playfair-display-latin-700-italic.woff"
F_PF9 = f"{R}/fonts/playfair/package/files/playfair-display-latin-900-normal.woff"
INK = (22, 22, 28); CREAM = (250, 246, 236); ORANGE = (255, 92, 40); RED_ = (232, 28, 36); YEL_ = (255, 199, 30)
GRN_ = (22, 170, 76); NAVY_ = (28, 52, 140); GOLD = (214, 172, 72); SKIN = (253, 249, 241)
LUMA = np.array([0.2126, 0.7152, 0.0722], np.float32)
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_rr = ((_xx - W / 2) / (W / 2)) ** 2 * 0.7 + ((_yy - H * 0.5) / (H / 2)) ** 2
C = lambda c: tuple(v / 255 for v in c)

# ---------------- timeline ----------------
AL = json.load(open(f"{B}/work/align.json"))
WORDS = AL["words"]; LINES = AL["lines"]
END = round(AL["dur"] + 1.5, 3)


def _n(w): return re.sub(r"[^a-z0-9]", "", w.lower())


def T(lid, w, nth=0):
    hits = [x["t"] for x in WORDS if x["line"] == lid and _n(x["w"]) == _n(w)]
    return hits[nth]


vo, _sr = sf.read(f"{B}/work/vo.wav", dtype="float32")
_hop = _sr // FPS
_env = np.array([np.sqrt(np.mean(vo[i * _hop:(i + 1) * _hop] ** 2)) for i in range(len(vo) // _hop + 2)] + [0.0])
_env = _env / (np.percentile(_env[_env > 1e-4], 92) + 1e-9)


def talk(t, on=True):
    if not on: return 0
    i = int(t * FPS); v = (_env[max(0, i - 1)] * 0.3 + _env[min(len(_env) - 1, i)] * 0.7) if i < len(_env) else 0
    return 0 if v < 0.18 else (1 if v < 0.45 else (2 if v < 0.8 else 3))


_gc = {}


def gcache(key, fn):
    if key not in _gc:
        if len(_gc) > 900: _gc.clear()
        _gc[key] = fn()
    return _gc[key]


def el_from(im):
    a = np.asarray(im, np.float32) / 255
    return (a[..., :3] * a[..., 3:4]).astype(np.float32), a[..., 3].copy()


def scale_el(el, s):
    pm, a = el; h, w = a.shape; nw, nh = max(2, int(w * s)), max(2, int(h * s))
    return cv2.resize(pm, (nw, nh), interpolation=cv2.INTER_AREA), cv2.resize(a, (nw, nh), interpolation=cv2.INTER_AREA)


def rot_comp(f, el, x, y, rot, scale=1.0, op=1.0, shadow=0.0):
    if op <= 0.003: return
    pm, a = el; h, w = a.shape
    D = int(math.hypot(w, h) * scale) + 60
    M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, scale); M[0, 2] += D / 2 - w / 2; M[1, 2] += D / 2 - h / 2
    pm2 = cv2.warpAffine(pm, M, (D, D), flags=cv2.INTER_LINEAR); a2 = cv2.warpAffine(a, M, (D, D), flags=cv2.INTER_LINEAR)
    if shadow:
        comp(f, (np.zeros_like(pm2), cv2.GaussianBlur(a2, (0, 0), 14) * shadow), x + 8, y + 18, op=op)
    comp(f, (pm2, a2), x, y, op=op)


def pop(t, t0, d=0.22):
    k = (t - t0) / d
    return clamp(k * 2.5), (0.85 + 0.15 * eback(k) if k < 1 else 1.0)


def pin(t, t0, d=0.3):
    """0..1 entrance with overshoot, for scale."""
    k = clamp((t - t0) / d); return eback(k) if k < 1 else 1.0


def grad_img(w, h, top, bot):
    g = np.linspace(0, 1, h)[:, None, None]
    arr = (np.array(top, np.float32)[None, None] * (1 - g) + np.array(bot, np.float32)[None, None] * g)
    arr = np.repeat(arr, w, axis=1).astype(np.uint8)
    return Image.fromarray(arr, "RGB").convert("RGBA")


def shape_grad(im, draw_mask, top, bot):
    """paint a vertical gradient through a mask drawn by draw_mask(ImageDraw)."""
    m = Image.new("L", im.size, 0); draw_mask(ImageDraw.Draw(m))
    g = grad_img(im.size[0], im.size[1], top, bot); im.paste(g, (0, 0), m)


# ---------------- sets: seamless cyclorama, spotlight, faint floor perspective, sun circle ----------------
SCHEMES = {
    "cream": ((240, 233, 220), (252, 249, 242), (232, 222, 204), (0.80, 0.76, 0.68)),
    "sky": ((60, 140, 240), (120, 190, 255), (70, 140, 230), (0.2, 0.45, 0.85)),
    "yellow": ((255, 186, 20), (255, 222, 90), (240, 170, 10), (0.85, 0.6, 0.05)),
    "purple": ((26, 10, 70), (86, 36, 190), (20, 8, 56), (0.25, 0.12, 0.6)),
    "teal": ((0, 104, 116), (0, 176, 168), (0, 92, 100), (0.0, 0.4, 0.42)),
    "red": ((150, 8, 18), (228, 32, 40), (170, 12, 22), (0.62, 0.05, 0.08)),
    "emerald": ((4, 46, 36), (12, 104, 76), (4, 40, 30), (0.1, 0.32, 0.24)),
    "orange": ((222, 64, 14), (255, 118, 52), (206, 56, 12), (0.75, 0.22, 0.05)),
    "pink": ((236, 72, 140), (255, 140, 184), (226, 60, 128), (0.8, 0.25, 0.48)),
}


def _stage_base(scheme):
    top, mid, bot, line = SCHEMES[scheme]
    y = (_yy / H)[..., None]
    top, mid, bot = np.array(top) / 255.0, np.array(mid) / 255.0, np.array(bot) / 255.0
    g = np.where(y < 0.55, top + (mid - top) * (y / 0.55), mid + (bot - mid) * ((y - 0.55) / 0.45)).astype(np.float32)
    spot = np.exp(-(((_xx - W / 2) / 620) ** 2 + ((_yy - 760) / 760) ** 2))[..., None]
    g = g * (0.93 + 0.12 * spot)
    ov = np.zeros((H, W), np.float32); vp = (W / 2, 900)
    for x in range(-1400, W + 1500, 170): cv2.line(ov, (int(vp[0]), int(vp[1])), (x, H + 200), 1.0, 2, cv2.LINE_AA)
    for k in range(1, 14): cv2.line(ov, (0, int(900 + 9 * k * k)), (W, int(900 + 9 * k * k)), 1.0, 2, cv2.LINE_AA)
    fade = np.clip((_yy - 900) / 700, 0, 1) * 0.12
    g = g * (1 - (ov * fade)[..., None]) + np.array(line, np.float32) * (ov * fade)[..., None]
    return np.clip(g, 0, 1).astype(np.float32)


def sun_el(col, R=540):
    def mk():
        s = 2 * R + 8; yy, xx = np.mgrid[0:s, 0:s].astype(np.float32); d = np.hypot(xx - s / 2, yy - s / 2)
        a = np.clip(R - d + 0.5, 0, 1)
        shade_ = 1.07 - 0.13 * np.clip(np.hypot(xx - s * 0.38, yy - s * 0.34) / R, 0, 1.6)
        rgb = np.clip((np.array(col, np.float32) / 255)[None, None] * shade_[..., None], 0, 1)
        return (rgb * a[..., None]).astype(np.float32), a.astype(np.float32)
    return gcache(("sun", col, R), mk)


def stage(scheme, sun=None, sx=540, sy=900, R=420):
    f = gcache(("stg", scheme), lambda: _stage_base(scheme)).copy()
    if sun is not None and R > 4:
        s_el = sun_el(sun)
        comp(f, (np.zeros_like(s_el[0]), cv2.GaussianBlur(s_el[1], (0, 0), 26) * 0.2), sx + 10, sy + 30, scale=R / 540)
        comp(f, s_el, sx, sy, scale=R / 540)
    return f


def finish(f, n, vig=0.22, grain=0.45):
    f = f * (1 - vig * np.clip(_rr - 0.3, 0, 1.4))[..., None]
    return np.clip(add_grain(np.clip(f, 0, 1), n, grain), 0, 1)


def cam(f, s=1.0, cx=W / 2, cy=H / 2, dx=0.0, dy=0.0, rot=0.0):
    if abs(s - 1) < 1e-3 and not dx and not dy and not rot: return f
    M = cv2.getRotationMatrix2D((cx, cy), rot, s); M[0, 2] += dx; M[1, 2] += dy
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def contact(f, x, y, w, op=0.32):
    el = gcache("cshadow", lambda: (np.zeros((120, 400, 3), np.float32),
                                    cv2.GaussianBlur(cv2.ellipse(np.zeros((120, 400), np.float32), (200, 60), (150, 26), 0, 0, 360, 1.0, -1), (0, 0), 14)))
    comp(f, scale_el(el, max(0.05, w / 300)), x, y, op=op)


# ---------------- editorial typography ----------------
_MK = re.compile(r"\[(.*?)\]|([^\[]+)")


def _segs(s, base, acc):
    return [(m.group(1), acc) if m.group(1) is not None else (m.group(2), base) for m in _MK.finditer(s)]


def ed_el(lead="", big="", tail="", big_col=INK, acc=RED_, lead_col=INK, big_size=170, lead_size=46, tail_size=44,
          shadow=0.0, maxw=800, fp_big=None, track=-0.03):
    key = ("ed", lead, big, tail, big_col, acc, lead_col, big_size, lead_size, tail_size, shadow, maxw, fp_big, track)
    if key in _gc: return _gc[key]
    fp_big = fp_big or F_BLACK; sc = 2
    while True:
        fb = font(fp_big, big_size * sc)
        bw = sum(sum(fb.getlength(c) + track * big_size * sc for c in s) for s, _ in _segs(big, big_col, acc)) if big else 0
        if bw / sc <= maxw or big_size <= 50: break
        big_size -= 6
    fl = font(F_SEMI, lead_size * sc); ft = font(F_BOLD, tail_size * sc)
    while lead and fl.getlength(lead) / sc > maxw and lead_size > 24:   # long leads ran into the right-hand UI (28 Oct)
        lead_size -= 2; fl = font(F_SEMI, lead_size * sc)
    while tail and ft.getlength(tail) / sc > maxw and tail_size > 22:
        tail_size -= 2; ft = font(F_BOLD, tail_size * sc)
    lw = fl.getlength(lead) if lead else 0; tw = ft.getlength(tail) if tail else 0
    w = int(max(bw, lw, tw) + 120 * sc)
    hl = lead_size * 1.25 * sc if lead else 0; hb = big_size * 1.02 * sc if big else 0; ht = tail_size * 1.3 * sc if tail else 0
    h = int(hl + hb + ht + 80 * sc)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y = 40 * sc
    if lead: d.text((w / 2, y + hl / 2), lead, font=fl, fill=tuple(lead_col) + (255,), anchor="mm"); y += hl
    if big:
        x = (w - bw) / 2
        for s, col in _segs(big, big_col, acc):
            for ch in s:
                d.text((x, y + hb * 0.5), ch, font=fb, fill=tuple(col) + (255,), anchor="lm"); x += fb.getlength(ch) + track * big_size * sc
        y += hb
    if tail: d.text((w / 2, y + ht / 2), tail, font=ft, fill=tuple(lead_col) + (255,), anchor="mm")
    im = im.resize((w // sc, h // sc), Image.LANCZOS)
    if shadow:
        a = im.getchannel("A").filter(ImageFilter.GaussianBlur(9))
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * shadow)))
        base = Image.new("RGBA", im.size, (0, 0, 0, 0)); base.alpha_composite(sh, (0, 6)); base.alpha_composite(im); im = base
    el = el_from(im)
    if len(_gc) < 900: _gc[key] = el
    return el


def rise_el(el, k):
    if k >= 1: return el
    pm, a = el; h = a.shape[0]; dy = int((1 - eo(clamp(k))) * h * 0.85)
    if dy <= 0: return el
    p2 = np.zeros_like(pm); a2 = np.zeros_like(a); p2[dy:] = pm[:h - dy]; a2[dy:] = a[:h - dy]
    return p2, a2


def ed_show(f, el, x, y, t, t0, d=0.36, out=None, scale=1.0):
    if t < t0: return
    k = (t - t0) / d
    op = clamp(k * 4) * (clamp((out - t) / 0.15) if out is not None else 1.0)
    sc_ = scale * (1.0 + 0.025 * math.exp(-max(0, t - t0 - d) * 6)); x, y = safe_xy(el, x, y, scale * 1.025)
    comp(f, rise_el(el, k), x, y, op=op, scale=sc_)


def chip(text, bg=INK, fg=WHITE, size=26, max_w=800):
    def mk():
        sz = size; fn = font(F_BOLD, sz * 2)
        while fn.getlength(text) / 2 + 44 > max_w and sz > 14: sz -= 1; fn = font(F_BOLD, sz * 2)   # long source chips ran edge to edge
        tw = fn.getlength(text) / 2; w, h = int(tw + 44), int(sz * 1.7)
        im = Image.new("RGBA", (w * 2, h * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], h, fill=tuple(bg) + (235,))
        d.text((w, h), text, font=fn, fill=tuple(fg) + (255,), anchor="mm")
        return el_from(im.resize((w, h), Image.LANCZOS))
    el = gcache(("chip", text, bg, fg, size, max_w), mk); _SAFE_IDS[id(el[1])] = el[1]   # (keeps a reference, so the id is never reused) chips/source chips: comp() keeps them in the safe area
    return el


# ---------------- platform-UI safe area for captions (R&D Visuals run, 28 Oct 2026; tools/layout_check.py) ----------------
# Instagram/YouTube draw their UI over these bands (PLAYBOOK §6): top 250, bottom 420, left 60, right 120 px. Caption helpers
# (ed_show/ui_word, say, title3d, hud_rule, hud_choice) nudge a caption back inside when it pokes out by < 220 px; bigger offsets
# are treated as deliberate (slide-ins, off-screen moves) and left alone. SAFE=0 switches this off for A/B.
SAFE = os.environ.get("SAFE", "1") != "0"
SAFE_T, SAFE_B, SAFE_L, SAFE_R = 250, H - 420, 60, W - 120


def safe_xy(el, x, y, scale=1.0, m=10, reach=220):
    if not SAFE or el is None: return x, y
    a = el[1]; cols = np.nonzero(a.max(0) > 0.08)[0]; rows = np.nonzero(a.max(1) > 0.08)[0]
    if not len(cols): return x, y
    h, w = a.shape
    x0, x1 = x + (cols[0] - w / 2) * scale, x + (cols[-1] - w / 2) * scale
    y0, y1 = y + (rows[0] - h / 2) * scale, y + (rows[-1] - h / 2) * scale
    def fix(lo, hi, zlo, zhi):
        if hi - lo > zhi - zlo - 2 * m: return 0.0
        if lo < zlo + m and zlo + m - lo < reach: return zlo + m - lo
        if hi > zhi - m and hi - (zhi - m) < reach: return zhi - m - hi
        return 0.0
    return x + fix(x0, x1, SAFE_L, SAFE_R), y + fix(y0, y1, SAFE_T, SAFE_B)


_SAFE_IDS = {}         # alpha arrays of cached caption elements (chips) that comp() should keep inside the safe area
_comp_raw = comp


def comp(frame, el, cx, cy, scale=1.0, op=1.0, anchor="c"):   # noqa: F811  (gfx.comp + safe area for chips)
    if SAFE and el is not None and anchor == "c" and id(el[1]) in _SAFE_IDS: cx, cy = safe_xy(el, cx, cy, scale)
    return _comp_raw(frame, el, cx, cy, scale=scale, op=op, anchor=anchor)


# ---------------- the square-face mascot ----------------
def head_el(mouth=0, blink=False, brow="n", lx=0, ly=0, expr="n"):
    key = ("head", mouth, blink, brow, lx, ly, expr)
    if key in _gc: return _gc[key]
    sc = 3; w, h = 210, 200
    im = Image.new("RGBA", (w * sc, h * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    S = lambda *v: [x * sc for x in v]
    d.rounded_rectangle(S(22, 20, 188, 182), 40 * sc, fill=INK + (255,))
    d.rounded_rectangle(S(29, 27, 181, 175), 34 * sc, fill=SKIN + (255,))
    sh = Image.new("L", im.size, 0); ds = ImageDraw.Draw(sh)
    ds.rounded_rectangle(S(29, 27, 181, 175), 34 * sc, fill=255)
    grad = np.clip((np.linspace(0, 1, im.size[1])[:, None] * 0.6 + np.linspace(0, 1, im.size[0])[None, :] * 0.4 - 0.55) * 120, 0, 40).astype(np.uint8)
    shade = Image.fromarray(np.minimum(np.asarray(sh), grad), "L")
    im.paste(Image.new("RGBA", im.size, (150, 120, 90, 255)), (0, 0), shade)
    d.ellipse(S(48, 40, 98, 66), fill=(255, 255, 255, 170))
    for cx in (62, 148):
        d.ellipse(S(cx - 16, 118, cx + 16, 134), fill=(255, 150, 150, 120))
    ox, oy = lx * 9, ly * 6
    for cx in (78, 132):
        x = cx + ox; y = 92 + oy
        if blink: d.rounded_rectangle(S(x - 11, y - 2, x + 11, y + 3), 2 * sc, fill=INK + (255,))
        elif expr == "sus": d.rounded_rectangle(S(x - 12, y - 4, x + 12, y + 6), 4 * sc, fill=INK + (255,))
        else:
            r = 15 if expr == "wow" else 11; d.ellipse(S(x - r * 0.8, y - r, x + r * 0.8, y + r), fill=INK + (255,))
            d.ellipse(S(x - 4, y - r + 3, x + 2, y - r + 9), fill=(255, 255, 255, 255))
    for i, cx in enumerate((78, 132)):
        sgn = -1 if i == 0 else 1
        if brow == "up": pts = [(cx - 16, 62), (cx + 16, 58)] if i == 0 else [(cx - 16, 58), (cx + 16, 62)]
        elif brow == "sus": pts = [(cx - 16, 66), (cx + 16, 74)] if i == 0 else [(cx - 16, 74), (cx + 16, 66)]
        elif brow == "sad": pts = [(cx - 16, 74), (cx + 16, 66)] if i == 0 else [(cx - 16, 66), (cx + 16, 74)]
        else: pts = [(cx - 15, 70), (cx + 15, 68)] if i == 0 else [(cx - 15, 68), (cx + 15, 70)]
        d.line([(p[0] * sc, p[1] * sc) for p in pts], fill=INK + (255,), width=7 * sc)
    mx, my = 105, 138
    if expr == "wow" and mouth == 0: mouth = "o"
    if mouth == 0:
        if expr == "sad": d.arc(S(mx - 22, my - 2, mx + 22, my + 22), 200, 340, fill=INK + (255,), width=6 * sc)
        elif expr == "smirk": d.arc(S(mx - 24, my - 16, mx + 22, my + 10), 10, 120, fill=INK + (255,), width=6 * sc)
        elif expr == "sus": d.line(S(mx - 16, my + 2, mx + 16, my - 2), fill=INK + (255,), width=6 * sc)
        else: d.arc(S(mx - 24, my - 18, mx + 24, my + 12), 20, 160, fill=INK + (255,), width=6 * sc)
    elif mouth == "o":
        d.ellipse(S(mx - 12, my - 10, mx + 12, my + 16), fill=INK + (255,))
    else:
        hh = {1: 10, 2: 17, 3: 24}[mouth]; ww = {1: 18, 2: 22, 3: 26}[mouth]
        d.rounded_rectangle(S(mx - ww, my - 6, mx + ww, my - 6 + hh * 1.6), int(hh * 0.8) * sc, fill=(60, 16, 20, 255))
        if mouth >= 2: d.ellipse(S(mx - ww * 0.6, my - 6 + hh * 0.9, mx + ww * 0.6, my - 6 + hh * 1.7), fill=(236, 90, 96, 255))
        d.rectangle(S(mx - ww + 6, my - 6, mx + ww - 6, my - 1), fill=(255, 255, 255, 255))
    el = el_from(im.resize((w, h), Image.LANCZOS))
    _gc[key] = el; return el


def _seg(f, p, q, th, col):
    cv2.line(f, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), col, max(1, int(th)), cv2.LINE_AA)
    cv2.circle(f, (int(q[0]), int(q[1])), max(1, int(th / 2)), col, -1, cv2.LINE_AA)


def guy(f, x, y, s=1.0, la=(18, 8), ra=(18, 8), ll=7, rl=7, lean=0.0, sit=False, mouth=0, blink=False, brow="n", look=(0, 0),
        expr="n", bob=0.0, hold=None, hold_off=(0, 0), face_dir=1, op=1.0, shadow=True):
    """square-face stick mascot. (x, y) = feet baseline (or seat point when sit=True). Angles in degrees from straight
    down, positive = outward. la = screen-left arm (upper, fore), ra = screen-right arm."""
    ink = C(INK); th = 12 * s
    g = f if op >= 0.999 else f.copy()
    if not sit:
        hip = (x, y - 178 * s)
        if shadow: contact(g, x, y + 4 * s, 170 * s, 0.3)
        for side, ang in ((-1, ll), (1, rl)):
            ft = (hip[0] + side * math.sin(math.radians(ang)) * 175 * s, hip[1] + math.cos(math.radians(ang)) * 175 * s)
            _seg(g, hip, ft, th, ink)
            cv2.ellipse(g, (int(ft[0] + side * 10 * s), int(ft[1] + 2 * s)), (int(22 * s), int(10 * s)), 0, 0, 360, ink, -1, cv2.LINE_AA)
    else:
        hip = (x, y)
        for side in (-1, 1):
            kn = (hip[0] + side * 30 * s, hip[1] + 26 * s); ft = (hip[0] + side * 36 * s, hip[1] + 138 * s)
            _seg(g, hip, kn, th, ink); _seg(g, kn, ft, th, ink)
            cv2.ellipse(g, (int(ft[0] + side * 10 * s), int(ft[1] + 2 * s)), (int(22 * s), int(10 * s)), 0, 0, 360, ink, -1, cv2.LINE_AA)
    lr = math.radians(lean)
    neck = (hip[0] + 168 * s * math.sin(lr), hip[1] - 168 * s * math.cos(lr))
    _seg(g, hip, neck, th * 1.05, ink)
    tie = np.array([[neck[0] - 9 * s, neck[1] + 6 * s], [neck[0] + 9 * s, neck[1] + 6 * s], [neck[0] + 5 * s, neck[1] + 20 * s],
                    [neck[0] + 13 * s, neck[1] + 78 * s], [neck[0], neck[1] + 94 * s], [neck[0] - 13 * s, neck[1] + 78 * s],
                    [neck[0] - 5 * s, neck[1] + 20 * s]], np.int32)
    cv2.fillPoly(g, [tie], C(ORANGE), cv2.LINE_AA)
    sh_ = (neck[0] + 22 * s * math.sin(lr), neck[1] + 22 * s * math.cos(lr))
    hands = {}
    for side, (a1, a2) in ((-1, la), (1, ra)):
        e = (sh_[0] + side * math.sin(math.radians(a1)) * 92 * s, sh_[1] + math.cos(math.radians(a1)) * 92 * s)
        hd = (e[0] + side * math.sin(math.radians(a2)) * 84 * s, e[1] + math.cos(math.radians(a2)) * 84 * s)
        _seg(g, sh_, e, th, ink); _seg(g, e, hd, th, ink)
        hands[side] = hd
    if hold is not None:
        hx, hy = hands[1]; comp(g, hold, hx + hold_off[0] * s, hy + hold_off[1] * s)
    for side in (-1, 1):
        hx, hy = hands[side]
        cv2.circle(g, (int(hx), int(hy)), int(15 * s), ink, -1, cv2.LINE_AA)
        cv2.circle(g, (int(hx), int(hy)), int(10 * s), (1, 1, 1), -1, cv2.LINE_AA)
    hel = head_el(mouth, blink, brow, look[0], look[1], expr)
    comp(g, scale_el(hel, s * 1.0), neck[0], neck[1] - 76 * s + bob * s)
    if op < 0.999: f[:] = f * (1 - op) + g * op
    return hands


def blink_at(t, seed=0):
    ph = (t + seed * 1.37) % 3.1
    return ph < 0.09


def walk(t, speed=1.0):
    ph = math.sin(t * 9 * speed)
    return dict(ll=8 + 22 * ph, rl=8 - 22 * ph, la=(18 - 26 * ph, 10), ra=(18 + 26 * ph, 10), bob=-6 * abs(math.cos(t * 9 * speed)))
