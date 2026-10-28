# ================= anim_cine.py — cinematic light + colour + environment sets (owner request 27 Oct 23:08) =================
# Goal: natural colour, depth and light so flat cartoon shots look "3D" and cinematic (warm key light, cool shadows,
# soft bloom, haze, light beams, out-of-focus backgrounds, lit interiors). Loaded after anim_fx.py. Overrides finish().
CINE_LOOK = "warm"          # default grade for every frame (set per shot via finish(f, n, look=...))


def grade(f, look="warm"):
    """colour grade: cool shadows + warm highlights, gentle S-curve, a touch more saturation (film-like, not neon)."""
    if look in (None, "none"): return f
    P = {"warm": ((-0.020, 0.004, 0.030), (0.045, 0.018, -0.030), 1.07, 1.06),
         "cool": ((0.000, 0.012, 0.040), (0.010, 0.010, 0.000), 1.06, 1.02),
         "night": ((-0.010, 0.000, 0.050), (0.030, 0.010, -0.020), 1.10, 0.95),
         "golden": ((-0.025, 0.000, 0.035), (0.070, 0.030, -0.050), 1.08, 1.08),
         "fresh": ((0.000, 0.006, 0.015), (0.020, 0.012, -0.005), 1.04, 1.08)}[look]
    sh, hi, con, sat = P
    f = np.ascontiguousarray(f, np.float32)
    lum = cv2.transform(f, _LM)                                            # same maths as numpy, ~2x faster with cv2
    a = 1.0 - lum; a = cv2.multiply(a, a); b = cv2.multiply(lum, lum)
    ch = cv2.split(f)
    x = cv2.merge([cv2.scaleAdd(a, sh[c], cv2.scaleAdd(b, hi[c], ch[c])) for c in range(3)])
    x = cv2.addWeighted(x, con, x, 0, 0.5 * (1 - con))
    l2 = cv2.transform(x, _LM)
    x = cv2.addWeighted(x, sat, cv2.merge([l2, l2, l2]), 1 - sat, 0)
    return np.clip(x, 0, 1, out=x)


_LM = LUMA.reshape(1, 3)
_VIG = {}


def _vig3(v):
    if v not in _VIG:
        m = (1 - v * np.clip(_rr - 0.3, 0, 1.4)).astype(np.float32); _VIG[v] = cv2.merge([m, m, m])
    return _VIG[v]


def bloom(f, thr=0.80, amt=0.28, radius=18):
    sm = cv2.resize(f, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    br = np.clip((sm - thr) / (1 - thr), 0, 1) ** 1.5
    br = cv2.GaussianBlur(br, (0, 0), radius / 4 + 2)
    return np.clip(f + cv2.resize(br, (W, H), interpolation=cv2.INTER_LINEAR) * amt, 0, 1)


def finish(f, n, vig=0.24, grain=0.40, look=None, bloom_amt=0.26):
    """replaces anim_base.finish: grade + bloom + vignette + grain."""
    f = grade(np.clip(f, 0, 1), look or CINE_LOOK)
    bloom_amt *= clamp((0.80 - float(f[::8, ::8].mean())) / 0.25)      # bright flat stages would wash out -> less bloom
    if bloom_amt > 0.01: f = bloom(f, amt=bloom_amt)
    f = cv2.multiply(f, _vig3(round(vig, 3)))
    return np.clip(add_grain(np.clip(f, 0, 1), n, grain), 0, 1)


def god_rays(f, x, y, t, col=(255, 226, 170), amt=0.35, n=9, length=1700, spread=0.9, ang0=1.15, seed=1):
    """soft volumetric light shafts from a source (window / lamp / sun). ang0 = main direction (radians, 0 = right)."""
    rng = np.random.default_rng(seed); sm = np.zeros((H // 4, W // 4), np.float32)
    for i in range(n):
        a = ang0 + (i / (n - 1) - 0.5) * spread + 0.03 * math.sin(t * 0.6 + i); wd = rng.uniform(0.02, 0.06)
        p = np.array([[x, y], [x + length * math.cos(a - wd), y + length * math.sin(a - wd)], [x + length * math.cos(a + wd), y + length * math.sin(a + wd)]], np.float32) / 4
        cv2.fillPoly(sm, [p.astype(np.int32)], rng.uniform(0.5, 1.0), cv2.LINE_AA)
    sm = cv2.GaussianBlur(sm, (0, 0), 6)
    yy, xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
    sm *= np.clip(1 - np.hypot(xx - x / 4, yy - y / 4) / (length / 4), 0, 1) ** 1.2
    f += cv2.resize(sm, (W, H))[..., None] * np.array(C(col), np.float32) * amt


def haze(f, y0, y1, col=(255, 236, 214), amt=0.35):
    g = np.clip((_yy - y0) / max(1, (y1 - y0)), 0, 1)
    g = np.sin(np.pi * g) * amt
    f[:] = f * (1 - g[..., None]) + np.array(C(col), np.float32) * g[..., None]


def bokeh(f, t, n=14, seed=3, ymin=300, ymax=1300, rmin=18, rmax=60, cols=((255, 214, 150), (255, 240, 210), (255, 170, 120)), amt=0.35):
    """out-of-focus light circles drifting in the background (draw BEFORE the subject)."""
    rng = np.random.default_rng(seed); ov = np.zeros((H // 2, W // 2, 3), np.float32)
    for i in range(n):
        x = (rng.uniform(0, W) + 14 * math.sin(t * 0.3 + i)) / 2; y = (rng.uniform(ymin, ymax) + 10 * math.cos(t * 0.25 + i)) / 2
        r = rng.uniform(rmin, rmax) / 2; c = np.array(C(cols[i % len(cols)]), np.float32) * rng.uniform(0.4, 1.0)
        cv2.circle(ov, (int(x), int(y)), int(r), tuple(float(v) for v in c), -1, cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 2.5)
    f += cv2.resize(ov, (W, H)) * amt


def dust_motes(f, t, x0, y0, x1, y1, n=26, seed=6, amt=0.8):
    rng = np.random.default_rng(seed)
    for i in range(n):
        x = x0 + (rng.uniform(0, 1) * (x1 - x0) + 30 * math.sin(t * 0.5 + i)) % max(1, (x1 - x0))
        y = y0 + (rng.uniform(0, 1) * (y1 - y0) - 12 * t) % max(1, (y1 - y0))
        r = rng.uniform(1.5, 3.5); a = amt * (0.5 + 0.5 * math.sin(t * 2 + i))
        cv2.circle(f, (int(x), int(y)), int(r + 0.5), (a, a * 0.95, a * 0.85), -1, cv2.LINE_AA)


def lamp_glow(f, x, y, r, col=(255, 210, 150), amt=0.55):
    glow(f, x, y, r, col, amt)


def light_leak(f, t, amt=0.18, col=(255, 150, 80)):
    x = W * (0.85 + 0.1 * math.sin(t * 0.4)); y = H * (0.15 + 0.05 * math.cos(t * 0.3))
    glow(f, x, y, 520, col, amt)


def cast_shadow(f, x, y, w, h, skew=0.35, op=0.35):
    """long soft shadow on the floor away from the key light (light from top-left -> shadow to bottom-right)."""
    m = np.zeros((H // 4, W // 4), np.float32)
    pts = np.array([[x - w / 2, y], [x + w / 2, y], [x + w / 2 + h * skew, y + h * 0.18], [x - w / 2 + h * skew, y + h * 0.18]], np.float32) / 4
    cv2.fillPoly(m, [pts.astype(np.int32)], 1.0, cv2.LINE_AA)
    m = cv2.resize(cv2.GaussianBlur(m, (0, 0), 6), (W, H)) * op
    f[:] = f * (1 - m[..., None]) + np.array(C((40, 26, 30)), np.float32) * m[..., None]


# ---------------- environment sets (static parts cached; call each frame) ----------------
def _soft(img, s_): return cv2.GaussianBlur(img, (0, 0), s_) if s_ > 0 else img


def _vgrad(top, bot, y0=0, y1=H):
    g = np.clip((np.arange(H, dtype=np.float32)[:, None, None] - y0) / max(1, y1 - y0), 0, 1)
    return (np.array(C(top), np.float32) * (1 - g) + np.array(C(bot), np.float32) * g) * np.ones((1, W, 1), np.float32)


def _counter_el(counter_y=1330):
    """wooden counter top + cabinet front as a layer (rgb premult, alpha) covering y >= counter_y."""
    def mk():
        h = H - counter_y; rgb = np.zeros((h, W, 3), np.float32)
        rgb[:40] = np.array(C((196, 140, 92)), np.float32)
        g = np.clip((np.arange(h - 40, dtype=np.float32) / max(1, h - 40)), 0, 1)[:, None, None]
        rgb[40:] = np.array(C((150, 100, 66)), np.float32) * (1 - g) + np.array(C((96, 62, 42)), np.float32) * g
        for x in range(0, W, 260): cv2.line(rgb, (x, 40), (x, h), C((80, 52, 36)), 3, cv2.LINE_AA)
        for x in range(130, W, 260): cv2.circle(rgb, (x, 120), 8, C((230, 196, 140)), -1, cv2.LINE_AA)
        cv2.line(rgb, (0, 1), (W, 1), C((240, 196, 140)), 3, cv2.LINE_AA)
        rgb[40:52] *= 0.7                                   # lip shadow under the worktop
        return rgb, np.ones((h, W), np.float32)
    return gcache(("counter_el", counter_y), mk)


def counter_front(f, counter_y=1330):
    """draw the counter again IN FRONT of the character -> he stands behind it (cooking-show framing). Props on the
    worktop go after this call (their base at y ~ counter_y + 10)."""
    comp(f, _counter_el(counter_y), W / 2, counter_y + (H - counter_y) / 2)


def set_kitchen(t=0.0, blur=5, counter_y=1330):
    """warm kitchen: tiled wall, wooden cabinets, window light from the left, pendant lamp, wooden counter in front."""
    def mk():
        f = _vgrad((214, 190, 160), (190, 158, 128), 0, counter_y)
        # subway tiles
        for r_ in range(0, 26):
            y = 560 + r_ * 44
            if y > counter_y: break
            cv2.line(f, (0, y), (W, y), C((176, 148, 120)), 3, cv2.LINE_AA)
            off = 0 if r_ % 2 else 60
            for x in range(-off, W, 120): cv2.line(f, (x, y), (x, y + 44), C((176, 148, 120)), 3, cv2.LINE_AA)
        # upper cabinets
        for x0 in (-40, 300, 640, 980):
            cv2.rectangle(f, (x0, 0), (x0 + 320, 470), C((140, 92, 60)), -1, cv2.LINE_AA)
            cv2.rectangle(f, (x0 + 20, 20), (x0 + 300, 450), C((160, 108, 72)), -1, cv2.LINE_AA)
            cv2.rectangle(f, (x0 + 20, 20), (x0 + 300, 450), C((110, 70, 46)), 4, cv2.LINE_AA)
            cv2.circle(f, (x0 + 280 if x0 % 2 else x0 + 40, 420), 9, C((230, 200, 140)), -1, cv2.LINE_AA)
        f[470:500] = np.array(C((96, 62, 40)), np.float32)
        # window (left) with sky
        cv2.rectangle(f, (40, 560), (360, 1050), C((96, 64, 44)), -1, cv2.LINE_AA)
        f[580:1030, 60:340] = _vgrad((255, 214, 150), (255, 240, 210), 580, 1030)[580:1030, 60:340]
        cv2.line(f, (200, 580), (200, 1030), C((96, 64, 44)), 12, cv2.LINE_AA); cv2.line(f, (60, 805), (340, 805), C((96, 64, 44)), 12, cv2.LINE_AA)
        # shelf with jars
        cv2.rectangle(f, (600, 760), (1010, 780), C((120, 80, 52)), -1, cv2.LINE_AA)
        for i, c in enumerate(((220, 120, 60), (90, 150, 90), (230, 190, 90), (180, 90, 80))):
            x = 640 + i * 95; cv2.rectangle(f, (x, 640), (x + 70, 760), C(c), -1, cv2.LINE_AA)
            cv2.rectangle(f, (x - 4, 622), (x + 74, 646), C((110, 90, 80)), -1, cv2.LINE_AA)
            cv2.line(f, (x + 14, 660), (x + 14, 740), (1, 1, 1), 5, cv2.LINE_AA)
        f = _soft(f, blur)
        comp(f, _counter_el(counter_y), W / 2, counter_y + (H - counter_y) / 2)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("set_kitchen", blur, counter_y), mk).copy()
    god_rays(f, 120, 560, t, (255, 220, 160), 0.16, 7, 1500, 0.55, 0.55, 2)
    lamp_glow(f, 760, 250, 300, (255, 214, 150), 0.28)
    dust_motes(f, t, 60, 600, 700, 1300, 22, 4, 0.45)
    return f


def set_room(t=0.0, blur=6, floor_y=1180):
    """cozy room: bookshelf wall, window glow, wooden floor in perspective, rug; warm lamp."""
    def mk():
        f = _vgrad((92, 64, 52), (130, 90, 66), 0, floor_y)
        rng = np.random.default_rng(7)
        for r_ in range(4):
            y0 = 300 + r_ * 210; cv2.rectangle(f, (40, y0 + 190), (1040, y0 + 210), C((70, 44, 32)), -1, cv2.LINE_AA)
            x = 60
            while x < 1020:
                bw = int(rng.uniform(26, 52)); bh = int(rng.uniform(130, 185))
                c = [(170, 60, 50), (60, 90, 140), (200, 160, 70), (70, 120, 80), (220, 210, 190), (120, 70, 110)][int(rng.integers(0, 6))]
                cv2.rectangle(f, (x, y0 + 190 - bh), (x + bw, y0 + 190), C(c), -1, cv2.LINE_AA)
                cv2.line(f, (x + 6, y0 + 200 - bh), (x + 6, y0 + 180), C(tuple(min(255, v + 40) for v in c)), 3, cv2.LINE_AA)
                x += bw + int(rng.uniform(2, 8))
        f = _soft(f, blur)
        # floor planks in perspective
        vp = (540, 820)
        fl = _vgrad((150, 100, 64), (110, 70, 44), floor_y, H)
        f[floor_y:] = fl[floor_y:]
        for x in range(-1600, W + 1700, 150): cv2.line(f, (int(vp[0] + (x - vp[0]) * 0.18), floor_y), (x, H), C((86, 54, 34)), 3, cv2.LINE_AA)
        for k in range(1, 9): y = int(floor_y + 12 * k * k); cv2.line(f, (0, y), (W, y), C((96, 62, 40)), 2, cv2.LINE_AA)
        cv2.ellipse(f, (540, 1500), (470, 150), 0, 0, 360, C((150, 52, 50)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (540, 1500), (420, 120), 0, 0, 360, C((190, 80, 64)), 6, cv2.LINE_AA)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("set_room", blur, floor_y), mk).copy()
    lamp_glow(f, 900, 300, 380, (255, 200, 130), 0.5)
    bokeh(f, t, 8, 9, 260, 1100, 20, 50, amt=0.18)
    return f


def set_dusk(t=0.0, blur=4, ground_y=1240):
    """outdoor golden hour: warm sky, low sun, layered hills + trees in haze, grassy ground."""
    def mk():
        f = _vgrad((70, 60, 110), (255, 170, 110), 0, 1000)
        f[1000:] = _vgrad((255, 170, 110), (255, 210, 160), 1000, ground_y)[1000:]
        glow(f, 720, 980, 260, (255, 230, 170), 0.8)
        cv2.circle(f, (720, 980), 90, C((255, 238, 200)), -1, cv2.LINE_AA)
        rng = np.random.default_rng(3)
        for layer, (base_y, col, amp) in enumerate(((1060, (190, 110, 120), 50), (1120, (140, 80, 100), 70), (1180, (90, 60, 80), 60))):
            pts = [(0, H)]
            for x in range(0, W + 60, 60): pts.append((x, base_y - amp * (0.5 + 0.5 * math.sin(x / 140 + layer * 2)) - rng.uniform(0, 18)))
            pts.append((W, H)); cv2.fillPoly(f, [np.array(pts, np.int32)], C(col), cv2.LINE_AA)
            haze(f, base_y - 200, base_y + 120, (255, 190, 150), 0.12)
        f = _soft(f, blur)
        f[ground_y:] = _vgrad((96, 120, 60), (40, 70, 36), ground_y, H)[ground_y:]
        for i in range(260):
            x = rng.uniform(0, W); y = rng.uniform(ground_y, H); hgt = rng.uniform(8, 26)
            cv2.line(f, (int(x), int(y)), (int(x + rng.uniform(-5, 5)), int(y - hgt)), C((70, 100, 50) if i % 2 else (120, 150, 70)), 2, cv2.LINE_AA)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("set_dusk", blur, ground_y), mk).copy()
    god_rays(f, 720, 980, t, (255, 210, 160), 0.22, 11, 1600, 2.6, -1.57, 5)
    dust_motes(f, t, 0, 700, W, ground_y, 18, 9, 0.6)
    return f


# ---------------- mood light, rim/wrap light, depth (spotlight(f, x, y, r, amt, feather) is in anim_fx) ----------------
def mood(f, col=(255, 60, 60), amt=0.35, cx=540, cy=900, r=1100):
    """tint the scene toward a colour (danger red, cold blue...) stronger at the edges -> emotional colour beat."""
    k = np.clip(np.hypot(_xx - cx, _yy - cy) / r, 0, 1)[..., None] * amt
    f[:] = f * (1 - k) + f * np.array(C(col), np.float32) * k * 1.2


def dof(f, sigma=6.0):
    return cv2.GaussianBlur(f, (0, 0), sigma)


def _c(c): return np.array(c, np.float32) / 255.0


def text3d_el(text, size=230, face=(250, 250, 250), side=(40, 40, 52), depth=22, font_path=None, shadow=0.55, tilt=0.55):
    """big extruded 3D word (titles tucked BEHIND the hero, like the reference reels). Returns (premult rgb, alpha).
    (adapted from studio/template/scripts/anim_cine.py)"""
    key = ("t3d", text, size, face, side, depth, font_path, shadow)
    def mk():
        fnt = font(font_path or F_ANTON, size)
        bb = ImageDraw.Draw(Image.new("L", (10, 10))).textbbox((0, 0), text, font=fnt)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]; pad = depth * 2 + 60
        Wd, Hd = tw + 2 * pad, th + 2 * pad
        m = Image.new("L", (Wd, Hd), 0); ImageDraw.Draw(m).text((pad - bb[0], pad - bb[1]), text, font=fnt, fill=255)
        m = np.asarray(m, np.float32) / 255
        rgb = np.zeros((Hd, Wd, 3), np.float32); al = np.zeros((Hd, Wd), np.float32)
        sh = np.roll(np.roll(cv2.GaussianBlur(m, (0, 0), 16), int(depth * 1.4), 0), int(depth * 0.9), 1) * shadow
        al = np.maximum(al, sh)
        sd = _c(side)
        for i in range(depth, 0, -1):
            mi = np.roll(np.roll(m, i, 0), int(i * tilt), 1); k = 0.55 + 0.45 * (1 - i / depth)
            rgb = rgb * (1 - mi[..., None]) + (sd * k)[None, None] * mi[..., None]; al = np.maximum(al, mi)
        yy = np.linspace(0, 1, Hd)[:, None, None]
        fc = _c(face)[None, None] * (1.08 - 0.22 * yy)
        er = cv2.erode(m, np.ones((3, 3), np.uint8), iterations=2)
        fc = fc + (np.clip(m - np.roll(er, 3, 0), 0, 1) * 0.35)[..., None]
        rgb = rgb * (1 - m[..., None]) + np.clip(fc, 0, 1.2) * m[..., None]; al = np.maximum(al, m)
        return (rgb * (al[..., None] > 0)).astype(np.float32), al.astype(np.float32)
    return gcache(key, mk)


def title3d(f, text, y, t=0.0, t0=-1.0, size=260, face=(255, 214, 60), side=(120, 40, 10), depth=26, max_w=860, op=1.0, x=540):
    """giant 3D word, pops in at t0 and floats gently. Draw it BEFORE Chubby / the hero prop so they overlap it."""
    el = text3d_el(text, size, face=face, side=side, depth=depth)
    w = el[1].shape[1] - 2 * (depth * 2 + 60)
    sc = min(1.0, max_w / max(1, w))
    k = clamp((t - t0) / 0.35) if t0 >= 0 else 1.0
    if k <= 0: return
    sc *= (0.86 + 0.14 * eback(k)) if k < 1 else 1.0
    comp(f, el, x, y + 4 * math.sin(t * 1.4), scale=sc * (1 + 0.006 * math.sin(t * 0.9)), op=op * min(1.0, k * 2))


def light_wrap(f, el, x, y, col, strength=0.25):
    """rim of background-coloured light around a hero element's edge (sells it as lit BY the scene)."""
    pm, a = el
    edge = np.clip(a - cv2.erode(a, np.ones((5, 5), np.uint8), iterations=2), 0, 1)
    comp(f, ((_c(col)[None, None] * edge[..., None] * strength).astype(np.float32), edge * strength), x, y)


# ================= ep 15 (27-28 Oct): MATERIALS on the Chubby v2 light model + two new lit places =================
BLOOMW = (236, 228, 214)
# ---------------- MATERIALS (ep 15 craft skill): what makes a surface read as glossy, satin, matte or chalky ----------------
# Gloss = a SMALL, SHARP, bright highlight + a crisp mirror image of the light source (window bars with hard edges) + deep
# darks + a bright Fresnel rim; satin = a broader, softer highlight; matte = no reflection, wide soft light wrap, low contrast;
# chalky (bloom) = lifted, desaturated blacks + a powdery speckle and streaks on top (Proko 'What makes materials look
# different'; ctrlpaint 'Studying glossiness'). Same key light (LIGHT3) as Chubby so props and character share one light.
MATS = {"gloss": dict(spec=0.70, shin=70, wrap=0.12, rim=0.40, ao=0.26, refl=0.85, lift=0.0, speck=0.0, squeeze=1.0),
        "satin": dict(spec=0.26, shin=16, wrap=0.30, rim=0.26, ao=0.20, refl=0.0, lift=0.0, speck=0.0, squeeze=1.0),
        "matte": dict(spec=0.02, shin=6, wrap=0.65, rim=0.10, ao=0.12, refl=0.0, lift=0.07, speck=0.0, squeeze=0.72),
        "chalky": dict(spec=0.0, shin=4, wrap=0.75, rim=0.05, ao=0.08, refl=0.0, lift=0.34, speck=0.9, squeeze=0.6)}


def mat_shade(mask, base, shadow, hi=None, kind="gloss", flat=0.95, light=LIGHT3, seed=0, lift_col=BLOOMW):
    """shade a flat mask (supersampled float 0..1) as a material. Returns rgb (h, w, 3)."""
    p = MATS[kind]
    col = _inflate(mask, base, shadow, hi, light=light, flat=flat, spec=p["spec"], shin=p["shin"], wrap=p["wrap"], rim_amt=p["rim"], ao=p["ao"])
    m = (mask > 0.5).astype(np.uint8)
    if m.sum() == 0: return col
    ys, xs = np.nonzero(m); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); bw, bh = max(1, x1 - x0), max(1, y1 - y0)
    if p["squeeze"] < 1:
        mu = col[m > 0].mean(0); col = mu + (col - mu) * p["squeeze"]
    if p["refl"] > 0:                                     # crisp window reflection = the strongest 'gloss' cue
        R = np.zeros(mask.shape, np.float32)
        for off, wd in ((0.16, 0.08), (0.30, 0.035)):
            pts = np.array([[x0 + bw * off, y0], [x0 + bw * (off + wd), y0], [x0 + bw * (off + wd) - bh * 0.45, y1], [x0 + bw * off - bh * 0.45, y1]], np.int32)
            cv2.fillPoly(R, [pts], 1.0, cv2.LINE_AA)
        k = max(3, int(min(bw, bh) * 0.07) | 1)
        inner = cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))).astype(np.float32)
        yy = np.arange(mask.shape[0], dtype=np.float32)[:, None]
        R *= inner * np.clip(1.15 - (yy - y0) / bh, 0, 1) * p["refl"]
        col = col + R[..., None] * (1 - col)
    if p["lift"] > 0:
        l_ = col.mean(2, keepdims=True); col = col * 0.6 + l_ * 0.4
        col = col * (1 - p["lift"]) + _n01(lift_col)[None, None] * p["lift"]
    if p["speck"] > 0:
        rng = np.random.default_rng(seed + 11)
        nz = rng.random((max(2, mask.shape[0] // 6), max(2, mask.shape[1] // 6))).astype(np.float32)
        nz = cv2.resize(nz, (mask.shape[1], mask.shape[0]), interpolation=cv2.INTER_LINEAR)
        streak = cv2.GaussianBlur(rng.random((max(2, mask.shape[0] // 40), max(2, mask.shape[1] // 40))).astype(np.float32), (0, 0), 0.8)
        streak = cv2.resize(streak, (mask.shape[1], mask.shape[0]), interpolation=cv2.INTER_CUBIC)
        a = np.clip((nz - 0.55) * 3, 0, 1) * 0.55 + np.clip((streak - 0.5) * 2.5, 0, 1) * 0.5
        col = col * (1 - (a * p["speck"])[..., None]) + _n01((250, 246, 238))[None, None] * (a * p["speck"])[..., None]
    return np.clip(col, 0, 1)


def mat_put(cv, m, base, shadow, hi=None, kind="gloss", outline=5, flat=0.95, seed=0):
    if outline: cv.outline(m, outline)
    cv.put(mat_shade(m, base, shadow, hi, kind, flat, seed=seed), np.clip(m, 0, 1))


# ---------------- places (ep 15): chocolatier workroom with a marble slab; night kitchen lit by an open fridge ----------------
def _marble_el(y0=1330):
    def mk():
        h = H - y0; rgb = np.zeros((h, W, 3), np.float32)
        g = np.clip(np.arange(h, dtype=np.float32) / h, 0, 1)[:, None, None]
        rgb[:] = np.array(C((236, 232, 226)), np.float32) * (1 - g) + np.array(C((196, 190, 184)), np.float32) * g
        rng = np.random.default_rng(12)
        for i in range(14):                                     # veins
            x = rng.uniform(-100, W); pts = [(x, 0)]
            for k in range(16): x += rng.uniform(-14, 40); pts.append((x, (k + 1) * h / 16))
            cv2.polylines(rgb, [np.array(pts, np.int32)], False, C((200, 194, 196)), int(rng.uniform(2, 4)), cv2.LINE_AA)
        rgb = cv2.GaussianBlur(rgb, (0, 0), 2.2)
        rgb[:14] = np.array(C((250, 248, 244)), np.float32)   # polished front edge catches the light
        rgb[14:22] *= 0.82
        glow_ = np.exp(-((np.arange(W) - 360) / 260.0) ** 2)[None, :, None] * np.exp(-np.arange(h) / 90.0)[:, None, None]
        rgb = np.clip(rgb + glow_ * 0.18, 0, 1)                 # soft reflection of the lamp on the polished stone
        return rgb.astype(np.float32), np.ones((h, W), np.float32)
    return gcache(("marble", y0), mk)


def marble_front(f, y0=1330):
    comp(f, _marble_el(y0), W / 2, y0 + (H - y0) / 2)


def set_chocolatier(t=0.0, blur=6, y0=1330):
    """chocolate-shop workroom: dark walnut wall, shelves of bars in coloured wrappers, copper pots, warm pendant lamps,
    white marble slab in front (draw marble_front AFTER Chubby to stand him behind it)."""
    def mk():
        f = _vgrad((70, 42, 30), (110, 70, 48), 0, y0)
        for k in range(0, W, 90): cv2.line(f, (k, 0), (k, y0), C((60, 36, 26)), 4, cv2.LINE_AA)   # wood panels
        rng = np.random.default_rng(21)
        for r_ in range(3):
            ys = 420 + r_ * 230; cv2.rectangle(f, (30, ys + 120), (1050, ys + 140), C((140, 92, 58)), -1, cv2.LINE_AA)
            x = 50
            while x < 1020:
                bw = int(rng.uniform(60, 90)); bh = int(rng.uniform(90, 118))
                c = [(200, 40, 50), (40, 120, 90), (230, 180, 60), (60, 80, 150), (240, 230, 210), (150, 60, 110)][int(rng.integers(0, 6))]
                cv2.rectangle(f, (x, ys + 120 - bh), (x + bw, ys + 120), C(c), -1, cv2.LINE_AA)
                cv2.rectangle(f, (x + 6, int(ys + 120 - bh * 0.6)), (x + bw - 6, int(ys + 120 - bh * 0.45)), C((255, 230, 170)), -1, cv2.LINE_AA)
                x += bw + int(rng.uniform(8, 20))
        for px in (150, 900):                                    # copper pots on the top shelf
            cv2.ellipse(f, (px, 300), (90, 70), 0, 0, 360, C((200, 110, 60)), -1, cv2.LINE_AA)
            cv2.ellipse(f, (px - 30, 280), (24, 40), 0, 0, 360, C((255, 190, 140)), -1, cv2.LINE_AA)
        f = _soft(f, blur)
        comp(f, _marble_el(y0), W / 2, y0 + (H - y0) / 2)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("set_choco", blur, y0), mk).copy()
    for lx in (300, 780):
        cv2.line(f, (lx, 0), (lx, 150), C((30, 20, 16)), 4, cv2.LINE_AA)
        cv2.ellipse(f, (lx, 170), (60, 34), 0, 180, 360, C((40, 30, 24)), -1, cv2.LINE_AA)
        lamp_glow(f, lx, 200, 260, (255, 200, 130), 0.45)
    bokeh(f, t, 10, 15, 300, 1200, 18, 46, amt=0.16)
    dust_motes(f, t, 100, 400, 980, 1300, 18, 8, 0.35)
    return f


def set_fridge_night(t=0.0, door=1.0, blur=5):
    """dark kitchen at night lit ONLY by an open fridge on the right (cold blue key light, warm practical in the back)."""
    def mk():
        f = _vgrad((14, 18, 36), (26, 32, 54), 0, H)
        for r_ in range(0, 22):
            y = 560 + r_ * 44
            if y > 1330: break
            cv2.line(f, (0, y), (620, y), C((30, 36, 58)), 3, cv2.LINE_AA)
        cv2.rectangle(f, (0, 1330), (W, H), C((20, 22, 36)), -1)
        # fridge body + bright interior
        cv2.rectangle(f, (600, 600), (1060, 1480), C((200, 214, 230)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (630, 630), (1030, 1450), C((214, 238, 255)), -1, cv2.LINE_AA)
        for k, y in enumerate((840, 1040, 1260)):
            cv2.rectangle(f, (630, y), (1030, y + 12), C((170, 200, 230)), -1, cv2.LINE_AA)
        for (x, y, c) in ((690, 800, (240, 120, 90)), (800, 790, (120, 200, 120)), (920, 1000, (250, 220, 120)), (720, 1220, (230, 230, 240)), (930, 1420, (200, 80, 90))):
            cv2.rectangle(f, (x - 40, y - 80), (x + 40, y + 36), C(c), -1, cv2.LINE_AA)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("set_fridge", blur), mk).copy()
    glow(f, 830, 1040, 400, (170, 220, 255), 0.55 * door)
    god_rays(f, 640, 1040, t, (170, 214, 255), 0.25 * door, 9, 1300, 1.3, math.pi, 7)
    haze(f, 700, 1500, (120, 170, 230), 0.10 * door)
    return f


# ================= ep 16 (28 Oct): INSIDE-THE-BODY WORLD — a lit gut tunnel with depth, translucent backlit folds, wet highlights ==========
# Craft skill (ep 16): what makes an inside-the-body scene read as soft, wet, living tissue instead of flat red paint
# (Jensen et al., subsurface scattering, UCSD graphics: translucent things look SOFT, light BLEEDS through thin parts and into
# the shadows, and the effect is strongest when the light is BEHIND the surface; Kurzgesagt house style: rounded forms, few
# bold saturated colours, uncluttered). Recipe used here: (1) BACKLIGHT from deep in the tunnel so every fold's thin rim glows
# orange-pink (light bleeding through), (2) shadows stay warm (deep magenta, never black), (3) small, sharp, cool-white WET
# highlights on the near folds (moist surface = specular), (4) DEPTH: far folds smaller, hazier (fog toward the glow) and
# blurred, near folds big and sharp; floating particles in front = scale + parallax; (5) the peristalsis squeeze is a ring that
# narrows the tunnel and travels toward the camera.
GUT_PAL = dict(deep=(52, 6, 26), wall=(178, 40, 72), wall_d=(96, 14, 42), rim=(255, 150, 120), glow=(255, 176, 140), spec=(255, 244, 236))


def set_gut(t=0.0, squeeze=None, bend=(60, -40), n=9, rot=0.0, pal=None, particles=True, cx=540, cy=900):
    """looking down a living intestine. squeeze = depth 0..1 (0 = at camera, 1 = far) of a travelling peristalsis ring (None = off).
    bend = how far the tunnel curves away (px at the far end). Draw story props/characters AFTER it."""
    P = dict(GUT_PAL, **(pal or {}))
    gx, gy = cx + bend[0], cy + bend[1]
    d = np.clip(np.hypot(_xx - gx, (_yy - gy) * 0.9) / 1000, 0, 1)[..., None]          # tunnel wall: glowing far end -> dark rim
    g_ = (1 - d) ** 7
    f = (np.array(C(P["glow"]), np.float32) * g_ + (np.array(C(P["wall"]), np.float32) * (1 - d) + np.array(C(P["deep"]), np.float32) * d) * (1 - g_)).astype(np.float32)
    far = f.copy(); split = False
    for i in range(n):
        z = 1.0 - i / (n - 1)                                                  # 1 = far .. 0 = near
        ph = (t * 0.35) % 1.0
        zz = 0.10 + 2.6 * (clamp(z - ph / (n - 1), 0, 1)) ** 1.5
        r = 700 / (zz + 0.3)
        sq = 0.42 * math.exp(-((z - squeeze) / 0.08) ** 2) if squeeze is not None else 0.0
        r *= (1 - sq) * (1 + 0.02 * math.sin(t * 2.2 + i))
        x = cx + bend[0] * z ** 1.3 + 14 * math.sin(t * 0.7 + i * 0.6); y = cy + bend[1] * z ** 1.3
        if not split and z < 0.45:                                             # hand-over: blur the far layers (depth of field)
            f[:] = cv2.GaussianBlur(f, (0, 0), 4); split = True
        fog = clamp(z * 0.9)
        wc = tuple(int(a + (b - a) * fog) for a, b in zip(P["wall"], P["glow"]))
        dc = tuple(int(a + (b - a) * fog * 0.8) for a, b in zip(P["wall_d"], P["wall"]))
        th = max(6, int(r * 0.2))                                              # fold thickness
        ax = (r * 1.05, r * 0.92)
        def ring(rx, ry, dy=0.0, a0=0, a1=360):
            aa = np.radians(np.arange(a0, a1 + 1, 4))
            wob = 1 + 0.045 * np.sin(aa * 3 + i * 1.7 + t * 0.8) + 0.03 * np.sin(aa * 5 - i)
            return np.stack([x + rx * wob * np.cos(aa), y + dy + ry * wob * np.sin(aa)], 1).astype(np.int32)
        cv2.polylines(f, [ring(ax[0] + th, ax[1] + th, th * 0.3)], True, C(dc), th, cv2.LINE_AA)          # shadowed back of the fold
        cv2.polylines(f, [ring(ax[0] + th / 2, ax[1] + th / 2)], True, C(wc), max(3, int(th * 0.7)), cv2.LINE_AA)
        rimc = tuple(int(a + (b - a) * (0.25 + 0.6 * sq)) for a, b in zip(P["rim"], (255, 110, 110)))
        cv2.polylines(f, [ring(*ax)], True, C(rimc), max(2, int(th * 0.13)), cv2.LINE_AA)                 # thin edge glows (light bleeds through)
        cv2.polylines(f, [ring(*ax, 0, 190, 350)], False, C(P["glow"]), max(2, int(th * 0.1)), cv2.LINE_AA)
        ax = (int(ax[0]), int(ax[1]))
        if z < 0.6:                                                             # wet highlights on near folds
            for j in range(4):
                a_ = math.radians(200 + 32 * j + 6 * math.sin(t + i))
                hx, hy = x + (ax[0] + th * 0.3) * math.cos(a_), y + (ax[1] + th * 0.3) * math.sin(a_)
                cv2.ellipse(f, (int(hx), int(hy)), (max(2, int(th * 0.28)), max(1, int(th * 0.08))), math.degrees(a_) + 90, 0, 360, C(P["spec"]), -1, cv2.LINE_AA)
        if sq > 0.05:
            cv2.ellipse(f, (int(x), int(y)), (ax[0] + th // 2, ax[1] + th // 2), rot, 0, 360, C((255, 80, 90)), max(3, int(th * 0.9 * sq / 0.42)), cv2.LINE_AA)
    haze(f, 300, 1500, P["glow"], 0.05)
    glow(f, gx, gy, 260, (255, 230, 200), 0.22)
    f *= (0.62 + 0.38 * np.clip((_yy[..., None] - 250) / 650, 0, 1))         # darker top band: the tunnel's far wall in shadow (+ caption room)
    if particles:
        bokeh(f, t, 16, 23, 260, 1700, 10, 46, cols=((255, 200, 170), (255, 150, 150), (255, 230, 210)), amt=0.2)
    return f


def peri_tube(f, x0, x1, y, r0, xs, t=0.0, sq=0.55, wall=46, label=True, cargo=None, cargo_dx=110, pal=None, relax=0.25):
    """SIDE VIEW of a gut segment (horizontal) with a peristalsis squeeze at x = xs: the muscle BEHIND the food contracts
    (narrow, red-hot) and the muscle IN FRONT relaxes (wider). cargo = element pushed just ahead of the squeeze.
    Returns the cargo position."""
    P = dict(GUT_PAL, **(pal or {}))
    xs_ = np.linspace(x0, x1, 120)
    def rad(x):
        g1 = math.exp(-((x - xs) / 70) ** 2); g2 = math.exp(-((x - xs - cargo_dx) / 120) ** 2)
        return r0 * (1 - sq * g1 + relax * g2 + 0.03 * math.sin(x / 40 + t * 3))
    top = [(x, y - rad(x)) for x in xs_]; bot = [(x, y + rad(x)) for x in xs_]
    outer_t = [(x, yy - wall) for x, yy in top]; outer_b = [(x, yy + wall) for x, yy in bot]
    for band_in, band_out in ((top, outer_t), (bot, outer_b)):
        poly = np.array(band_in + band_out[::-1], np.int32)
        cv2.fillPoly(f, [poly], C(OUT3), cv2.LINE_AA)
        inner = np.array([(x, yy + (3 if band_in is top else -3)) for x, yy in band_in] + [(x, yy + (-3 if band_in is top else 3)) for x, yy in band_out[::-1]], np.int32)
        cv2.fillPoly(f, [inner], C(P["wall"]), cv2.LINE_AA)
        for k in range(0, len(xs_), 6):                                        # muscle ring stripes
            x = xs_[k]; g1 = math.exp(-((x - xs) / 70) ** 2)
            col = tuple(int(a + (b - a) * g1) for a, b in zip(P["wall_d"], (255, 70, 70)))
            ya, yb = band_in[k][1], band_out[k][1]
            cv2.line(f, (int(x), int(ya)), (int(x), int(yb)), C(col), 5 + int(4 * g1), cv2.LINE_AA)
        cv2.polylines(f, [np.array(band_in, np.int32)], False, C(P["rim"]), 5, cv2.LINE_AA)       # wet inner lining
    lum = np.array(top + bot[::-1], np.int32)
    ov = f.copy(); cv2.fillPoly(ov, [lum], C((120, 30, 50)), cv2.LINE_AA); f[:] = f * 0.55 + ov * 0.45
    cx_ = xs + cargo_dx
    if cargo is not None and x0 < cx_ < x1: comp(f, cargo, cx_, y)
    if label:
        lx = xs
        if x0 + 60 < lx < x1 - 60:
            comp(f, chip("SQUEEZE", (200, 40, 50), WHITE, 28), lx, y - r0 - wall - 60)
        if x0 + 60 < lx + cargo_dx + 130 < x1 - 40:
            comp(f, chip("RELAX", (60, 130, 200), WHITE, 28), lx + cargo_dx + 130, y + r0 + wall + 62)
    return cx_, y
