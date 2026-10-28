# ================= cinematic texture layer (exec'd after anim_base.py) =================
# Owner, 27 Oct: wants the "texture" of top story channels — real-looking light, depth, atmosphere, film look, big 3D words
# tucked behind the hero object. This file gives every shot that look without rewriting shot code:
#   CINE=1 (default): stage(scheme, ...) returns a lit world with depth (sky/skyline/studio/desk) in the scheme's colours,
#   the big colour circle becomes a glowing light disc, and finish() becomes a film grade (tone curve, split tone, bloom,
#   halation, chromatic fringe, grain, vignette). CINE=0 restores the flat look.
# New helpers for shot code: world(kind, t), text3d_el(text, ...), light_rays(f, ...), bokeh(f, ...), dof(f, sigma), light_wrap(...)
import os as _os
CINE = _os.environ.get("CINE", "1") != "0"
_rng = np.random.default_rng
from gfx import GRAIN


def _noise(h, w, scale, seed, octaves=4):
    """smooth value noise 0..1 (cached by caller)"""
    r = _rng(seed); acc = np.zeros((h, w), np.float32); amp = 1.0; tot = 0.0; s = scale
    for _ in range(octaves):
        g = r.random((max(2, int(h / s)), max(2, int(w / s)))).astype(np.float32)
        acc += cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC) * amp; tot += amp; amp *= 0.5; s /= 2
    acc /= tot; return np.clip((acc - acc.min()) / (np.ptp(acc) + 1e-6), 0, 1)


def _mix(a, b, k): return a * (1 - k) + b * k


def _c(c): return np.array(c, np.float32) / 255.0


# palettes per scheme: (sky top, sky horizon, sun/glow, far city, ground near, ground far)
_PAL = {
    "orange": ((176, 34, 40), (255, 128, 30), (255, 206, 110), (150, 50, 50), (96, 30, 12), (226, 104, 30)),
    "yellow": ((255, 136, 0), (255, 214, 60), (255, 244, 170), (214, 110, 30), (150, 80, 10), (250, 170, 30)),
    "purple": ((14, 8, 46), (96, 40, 170), (255, 170, 230), (40, 20, 90), (18, 10, 40), (70, 30, 120)),
    "red": ((60, 6, 16), (210, 40, 46), (255, 170, 120), (90, 16, 26), (40, 6, 10), (150, 30, 34)),
    "teal": ((0, 40, 60), (0, 150, 160), (170, 255, 240), (0, 70, 84), (0, 30, 36), (0, 110, 110)),
    "emerald": ((2, 24, 22), (16, 110, 80), (190, 255, 210), (6, 50, 40), (2, 20, 16), (14, 80, 56)),
    "sky": ((20, 90, 230), (110, 190, 255), (255, 248, 220), (70, 120, 200), (30, 110, 60), (90, 180, 90)),
    "pink": ((120, 20, 80), (255, 130, 180), (255, 230, 240), (150, 50, 110), (80, 16, 50), (220, 90, 150)),
    "cream": ((196, 170, 140), (246, 232, 206), (255, 246, 222), (170, 146, 120), (110, 62, 30), (176, 112, 60)),
}
HORIZON = 1180   # where the far city meets the ground (props usually stand around y 1100-1450)


def _skyline(seed, h_lo, h_hi, bw=(40, 120)):
    r = _rng(seed); m = np.zeros((H, W), np.float32); win = np.zeros((H, W), np.float32); x = -40
    while x < W + 40:
        w = int(r.integers(*bw)); h = int(r.integers(h_lo, h_hi)); top = HORIZON - h
        cv2.rectangle(m, (x, top), (x + w, HORIZON + 4), 1.0, -1)
        if r.random() < 0.35: cv2.rectangle(m, (x + w // 3, top - int(r.integers(10, 50))), (x + w // 3 + 6, top), 1.0, -1)
        for yy in range(top + 12, HORIZON - 8, 16):
            for xx in range(x + 6, x + w - 8, 12):
                if r.random() < 0.28: cv2.rectangle(win, (xx, yy), (xx + 4, yy + 6), 1.0, -1)
        x += w + int(r.integers(-6, 14))
    return m, win * m


def _world_base(kind, scheme):
    top, hor, glow, city, gnear, gfar = (_c(v) for v in _PAL.get(scheme, _PAL["orange"]))
    y = (_yy / H)[..., None]
    if kind in ("skyline", "golden", "night"):
        ky = np.clip(_yy / HORIZON, 0, 1)[..., None] ** 1.6
        f = _mix(top, hor, ky).astype(np.float32)
        # clouds (soft, lit from the horizon)
        n = _noise(H, W, 260, 11); cl = np.clip((n - 0.55) * 3.2, 0, 1) * np.clip(1 - _yy / HORIZON, 0, 1) ** 0.6
        f = _mix(f, _mix(hor, glow, 0.5), (cl * 0.55)[..., None])
        # sun glow on the horizon
        g = np.exp(-(((_xx - W * 0.5) / 520) ** 2 + ((_yy - (HORIZON - 120)) / 380) ** 2))[..., None]
        f = f + glow * g * 0.55
        # two skyline layers: far (hazy) and mid
        for seed, (lo, hi), haze, blur in ((3, (120, 330), 0.72, 5), (5, (60, 210), 0.45, 3)):
            m, win = _skyline(seed, lo, hi)
            col = _mix(city, hor, haze)
            f = _mix(f, col, cv2.GaussianBlur(m, (0, 0), blur)[..., None])
            lit = (kind == "night") * 1.0 + 0.35
            f = f + _mix(glow, np.array([1.0, 0.85, 0.5], np.float32), 0.5) * (cv2.GaussianBlur(win, (0, 0), 1.2) * (1 - haze) * lit)[..., None]
        # ground: perspective field, darker near the camera, soft
        kg = np.clip((_yy - HORIZON) / (H - HORIZON), 0, 1)[..., None]
        gr = _mix(gfar, gnear, kg ** 0.8)
        tex = _noise(H, W, 40, 21, 3)[..., None]
        gr = gr * (0.9 + 0.2 * tex)
        f = np.where((_yy >= HORIZON)[..., None], gr, f)
        f = _mix(f, hor, (np.exp(-((_yy - HORIZON) / 60) ** 2) * 0.55)[..., None])   # horizon haze band
    elif kind == "desk":
        # blurred room + window light behind, wooden tabletop in front
        f = _mix(_mix(top, hor, 0.6), glow, (np.exp(-(((_xx - W * 0.72) / 300) ** 2 + ((_yy - 520) / 420) ** 2)) * 0.8)[..., None])
        f = f * (0.75 + 0.3 * y)
        r_ = _rng(31).random((H // 6, 6)).astype(np.float32)
        n = cv2.GaussianBlur(cv2.resize(r_, (W, H), interpolation=cv2.INTER_CUBIC), (0, 0), 3)
        grain_ = np.sin((_yy * 0.11 + n * 9.0 + 2.0 * np.sin(_xx * 0.004)) * 1.0) * 0.5 + 0.5
        wood = _mix(gnear * 1.25, gfar * 1.1, (grain_ * 0.65 + 0.35 * n)[..., None])
        kd = np.clip((_yy - HORIZON) / 120, 0, 1)[..., None]
        f = _mix(f, wood * (0.85 + 0.25 * np.clip((_yy - HORIZON) / (H - HORIZON), 0, 1))[..., None], kd)
    else:  # "studio": seamless backdrop, spotlight, haze, glossy floor
        f = _mix(top, hor, np.clip(_yy / H * 1.25, 0, 1)[..., None])
        spot = np.exp(-(((_xx - W / 2) / 460) ** 2 + ((_yy - 900) / 700) ** 2))[..., None]
        f = f * (0.55 + 0.75 * spot) + glow * spot * 0.12
        haze = _noise(H, W, 300, 41)[..., None]
        f = f + glow * haze * spot * 0.10
        fl = np.clip((_yy - HORIZON) / 500, 0, 1)[..., None]
        f = f * (1 - 0.35 * fl)
    return np.clip(f, 0, 1.2).astype(np.float32)


_SCHEME_KIND = {"orange": "golden", "yellow": "golden", "sky": "skyline", "purple": "night", "teal": "night",
                "emerald": "studio", "red": "studio", "pink": "studio", "cream": "desk"}


def world(kind=None, scheme="orange", t=0.0, drift=6.0):
    """lit background with depth. kind: golden | skyline | night | studio | desk (None = by scheme). Slow parallax drift."""
    kind = kind or _SCHEME_KIND.get(scheme, "studio")
    f = gcache(("world", kind, scheme), lambda: _world_base(kind, scheme))
    if drift:
        M = np.float32([[1.02, 0, -W * 0.01 - drift * math.sin(t * 0.35)], [0, 1.02, -H * 0.01]])
        return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return f.copy()


def glow_disc(f, col, sx, sy, R, op=0.9):
    """the channel's big colour circle, now a lit disc: soft core, bright rim, outer glow — the world shows around it."""
    if R < 4: return
    key = ("gdisc", col, int(R))
    def mk():
        s = int(2 * R * 1.6) // 2 * 2; yy, xx = np.mgrid[0:s, 0:s].astype(np.float32); d = np.hypot(xx - s / 2, yy - s / 2) / R
        a = np.clip((1 - d) * R / 2.5, 0, 1)
        c = _c(col)
        shade_ = 1.04 - 0.30 * np.clip(np.hypot(xx - s * 0.40, yy - s * 0.34) / R, 0, 1.6)
        rim = np.exp(-((d - 0.975) / 0.022) ** 2)
        rgb = c[None, None] * shade_[..., None] + c[None, None] * 0.25 * rim[..., None]
        outer = np.exp(-np.clip(d - 1, 0, None) / 0.12) * (d > 0.98) * 0.32
        alpha = np.clip(a + outer, 0, 1)
        rgb = np.where((d > 1)[..., None], c[None, None] * 1.2, rgb)
        return (np.clip(rgb, 0, 1.4) * alpha[..., None]).astype(np.float32), alpha.astype(np.float32)
    comp(f, gcache(key, mk), sx, sy, op=op)


def light_rays(f, sx, sy, col=(255, 236, 190), strength=0.22, n_rays=28, seed=2):
    """volumetric light rays from a point (screen blend)"""
    def mk():
        ang = np.arctan2(_yy - sy, _xx - sx); r = _rng(seed).random(n_rays)
        pat = np.zeros_like(ang)
        for i, v in enumerate(r): pat += np.exp(-((np.angle(np.exp(1j * (ang - i * 2 * np.pi / n_rays))) / (0.02 + 0.05 * v)) ** 2)) * (0.4 + 0.6 * v)
        fall = np.exp(-np.hypot(_xx - sx, _yy - sy) / 900)
        return cv2.GaussianBlur((pat * fall).astype(np.float32), (0, 0), 6)
    m = gcache(("rays", int(sx), int(sy), n_rays, seed), mk)[..., None] * strength
    f[:] = 1 - (1 - f) * (1 - _c(col) * m)


def bokeh(f, seed=1, count=26, col=(255, 210, 150), y0=0, y1=H, rmin=14, rmax=46, op=0.35, t=0.0):
    """out-of-focus light circles (drifting slowly)"""
    def mk():
        r = _rng(seed); m = np.zeros((H, W), np.float32)
        for _ in range(count):
            cx, cy, rr = int(r.integers(0, W)), int(r.integers(y0, y1)), int(r.integers(rmin, rmax))
            cv2.circle(m, (cx, cy), rr, float(0.4 + 0.6 * r.random()), -1, cv2.LINE_AA)
        return cv2.GaussianBlur(m, (0, 0), 2.5)
    m = gcache(("bokeh", seed, count, y0, y1), mk)
    if t: m = np.roll(m, int(t * 8) % W, axis=1)
    f[:] = 1 - (1 - f) * (1 - _c(col) * (m * op)[..., None])


def dof(f, sigma=6.0):
    """blur a whole layer (use on the background before drawing the hero object)"""
    return cv2.GaussianBlur(f, (0, 0), sigma)


def text3d_el(text, size=230, face=(250, 250, 250), side=(40, 40, 52), depth=22, font_path=None, shadow=0.55, tilt=0.55):
    """big extruded 3D word (for 'BILLION DOLLAR'-style titles tucked behind the hero object). Returns (premult rgb, alpha)."""
    key = ("t3d", text, size, face, side, depth, font_path, shadow)
    def mk():
        fnt = font(font_path or F_ANTON, size)
        bb = ImageDraw.Draw(Image.new("L", (10, 10))).textbbox((0, 0), text, font=fnt)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]; pad = depth * 2 + 60
        Wd, Hd = tw + 2 * pad, th + 2 * pad
        m = Image.new("L", (Wd, Hd), 0); ImageDraw.Draw(m).text((pad - bb[0], pad - bb[1]), text, font=fnt, fill=255)
        m = np.asarray(m, np.float32) / 255
        rgb = np.zeros((Hd, Wd, 3), np.float32); al = np.zeros((Hd, Wd), np.float32)
        # soft cast shadow
        sh = np.roll(np.roll(cv2.GaussianBlur(m, (0, 0), 16), int(depth * 1.4), 0), int(depth * 0.9), 1) * shadow
        al = np.maximum(al, sh)
        sd = _c(side)
        for i in range(depth, 0, -1):   # extrusion, darker further back
            mi = np.roll(np.roll(m, i, 0), int(i * tilt), 1); k = 0.55 + 0.45 * (1 - i / depth)
            rgb = rgb * (1 - mi[..., None]) + (sd * k)[None, None] * mi[..., None]; al = np.maximum(al, mi)
        # face: vertical gradient + top bevel highlight + inner shade
        yy = np.linspace(0, 1, Hd)[:, None, None]
        fc = _c(face)[None, None] * (1.08 - 0.22 * yy)
        er = cv2.erode(m, np.ones((3, 3), np.uint8), iterations=2)
        hl = np.clip(m - np.roll(er, 3, 0), 0, 1) * 0.35
        fc = fc + hl[..., None]
        rgb = rgb * (1 - m[..., None]) + np.clip(fc, 0, 1.2) * m[..., None]; al = np.maximum(al, m)
        return (rgb * 1.0).astype(np.float32) * (al[..., None] > 0), al.astype(np.float32)
    pm, a = gcache(key, mk)
    return pm * 1.0, a


def light_wrap(f, el, x, y, col, strength=0.25):
    """rim light: a thin glow of the background colour around a hero object's edge (sells it as 'in' the scene)"""
    pm, a = el
    edge = np.clip(a - cv2.erode(a, np.ones((5, 5), np.uint8), iterations=2), 0, 1)
    comp(f, ((_c(col)[None, None] * edge[..., None] * strength).astype(np.float32), edge * strength), x, y)


# ---------- film grade ----------
_CA = None


def _ca_maps():
    global _CA
    if _CA is None:
        dx = (_xx - W / 2) / (W / 2); dy = (_yy - H / 2) / (H / 2); r2 = dx * dx + dy * dy
        k = 2.2 * r2 / 2.0
        _CA = [(_xx + dx * k * s, _yy + dy * k * s) for s in (1, -1)]
        _CA = [(a.astype(np.float32), b.astype(np.float32)) for a, b in _CA]
    return _CA


_LUMK = None; _VIGC = {}; _GRC = {}


def _lum(f):
    global _LUMK
    if _LUMK is None: _LUMK = LUMA.reshape(1, 3).astype(np.float32)
    return cv2.transform(f, _LUMK)


def cine_grade(f, n, warmth=0.45, bloom=0.18, grain=0.55, vig=0.32, ca=True, sat=1.16):
    f = np.clip(f, 0, 1.5).astype(np.float32)
    lum = _lum(f)
    # bloom + halation (warm glow around highlights) at quarter resolution
    sm = cv2.resize(f, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    sm = np.clip((_lum(sm) - 0.8) / 0.2, 0, 1)[..., None] * sm
    b1 = cv2.GaussianBlur(sm, (0, 0), 4); b2 = cv2.GaussianBlur(sm, (0, 0), 14)
    bl = cv2.resize((b1 + b2) * (0.6 * bloom) * np.array([1.0, 0.9, 0.8], np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
    f += bl
    # filmic tone curve (soft shoulder, slight S)
    f = f / (1 + 0.25 * f) * 1.25
    f = f + 0.42 * (f - f * f) * (f - 0.5)   # contrast S-curve: deep shadows, rich highlights
    lum = _lum(f)[..., None]
    # split tone: warm highlights, cool-teal shadows; vibrance kept
    a_ = warmth * np.array([0.035, 0.012, -0.03], np.float32); b_ = warmth * np.array([-0.018, 0.004, 0.03], np.float32)
    f += lum * (a_ - b_) + b_
    f = lum + (f - lum) * sat
    if ca:
        (ax, ay), (bx, by) = _ca_maps()
        f = cv2.merge([cv2.remap(f[..., 0], ax, ay, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT), np.ascontiguousarray(f[..., 1]),
                       cv2.remap(f[..., 2], bx, by, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)])
    if vig not in _VIGC: _VIGC[vig] = (1 - vig * np.clip(_rr - 0.25, 0, 1.4)).astype(np.float32)[..., None]
    f *= _VIGC[vig]
    # grain: stronger in the mid-tones, like film
    lum = np.clip(_lum(f), 0, 1)
    gi = (n + 3) % 6
    if gi not in _GRC: _GRC[gi] = cv2.resize(GRAIN[gi], (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32)
    f += (_GRC[gi] * (grain * 1.6) * (0.35 + 2.6 * lum * (1 - lum)))[..., None]
    return np.clip(f, 0, 1)

if CINE:
    _stage_flat, _finish_flat = stage, finish

    def stage(scheme, sun=None, sx=540, sy=900, R=420, t=None, kind=None):   # noqa: F811 — same API as anim_base.stage
        tt = t if t is not None else (globals().get("_CINE_T", 0.0))
        if "set_light" in globals(): set_light("day")          # characters lit for the open studio look
        f = world(kind, scheme, tt)
        if sun is not None and R > 4: glow_disc(f, sun, sx, sy, R)
        return f

    def finish(f, n, vig=0.32, grain=0.55):   # noqa: F811
        globals()["_CINE_T"] = n / FPS
        return cine_grade(f, n, vig=vig, grain=grain)


def title3d(f, text, y, t=0.0, t0=-1.0, size=260, face=(255, 214, 60), side=(120, 40, 10), depth=26, max_w=800, op=1.0):
    """giant 3D word centred at x=540 (safe zone: fits in max_w px), popping in at t0 and floating gently.
    Draw it BEFORE the hero object so the object overlaps it (the 'tucked behind' look)."""
    el = text3d_el(text, size, face=face, side=side, depth=depth)
    a_ = el[1]; cols = np.nonzero(a_.max(0) > 0.08)[0]; Wd = a_.shape[1]
    w = (cols[-1] - cols[0] + 1) if len(cols) else Wd  # visible width INCLUDING extrusion + cast shadow (28 Oct: HOOVER hit the UI)
    s = min(1.0, max_w / max(1, w))
    xc = 540 - ((cols[0] + cols[-1]) / 2 - Wd / 2) * s if len(cols) else 540   # centre the visible mass, not the padded box
    k = clamp((t - t0) / 0.35) if t0 >= 0 else 1.0
    if k <= 0: return
    s *= (0.86 + 0.14 * eback(k)) if k < 1 else 1.0
    _, y = safe_xy(el, xc, y, s)
    comp(f, el, xc, y + 4 * math.sin(t * 1.4), scale=s * (1 + 0.006 * math.sin(t * 0.9)), op=op * min(1.0, k * 2))
