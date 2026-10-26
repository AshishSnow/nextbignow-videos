# ================= FreshNestHub props: rocket sled, dials, eye, tooth, scale, seat belt, desert, FNH logo =================
TIE = (16, 190, 130)            # FreshNestHub mascot wears a mint tie (OopsMyBusiness = orange)
MINTG = (16, 190, 130); STEEL = (176, 186, 204); NAVY2 = (30, 52, 120); SAND = (238, 178, 104)
RED2 = (214, 36, 44); BLOOD = (196, 18, 30)


def _pil_from_el(el, w, h):
    pm, a = el
    return Image.fromarray((np.dstack([np.clip(pm / np.maximum(a[..., None], 1e-4), 0, 1), a]) * 255).astype(np.uint8), "RGBA").resize((int(w), int(h)), Image.LANCZOS)


def add_patch(f, x0, y0, rgb, a, mode="over"):
    """composite a float patch (rgb straight colour, a alpha) at integer top-left (x0, y0), clipped to the frame."""
    h, w = a.shape; X0, Y0 = max(0, x0), max(0, y0); X1, Y1 = min(W, x0 + w), min(H, y0 + h)
    if X1 <= X0 or Y1 <= Y0: return
    pr = rgb[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]; pa = a[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0, None]
    if mode == "add": f[Y0:Y1, X0:X1] += pr * pa
    else: f[Y0:Y1, X0:X1] = f[Y0:Y1, X0:X1] * (1 - pa) + pr * pa


# ---------------- helmet (drawn over head_el; same centre) ----------------
def helmet_el():
    def mk():
        w, h, sc = 260, 270, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.pieslice(S(28, 2, 232, 178), 180, 360, fill=255), (255, 255, 255), (196, 204, 222))
        d.arc(S(28, 2, 232, 178), 180, 360, fill=INK + (255,), width=6 * sc)
        d.rounded_rectangle(S(118, 6, 142, 84), 10 * sc, fill=RED2 + (255,))
        _ov(im, lambda q: q.arc(S(52, 18, 170, 140), 200, 255, fill=(255, 255, 255, 230), width=9 * sc))
        d.rounded_rectangle(S(22, 76, 238, 96), 10 * sc, fill=RED2 + (255,), outline=INK + (255,), width=4 * sc)
        d.line(S(70, 46, 190, 46), fill=(40, 40, 50, 255), width=8 * sc)
        for cx in (98, 162):
            d.ellipse(S(cx - 21, 26, cx + 21, 68), fill=(36, 70, 96, 255), outline=INK + (255,), width=5 * sc)
            d.ellipse(S(cx - 12, 34, cx - 2, 46), fill=(170, 230, 255, 230))
        for x0, x1 in ((40, 46), (220, 214)): d.line(S(x0, 96, x1, 200), fill=(50, 50, 60, 255), width=5 * sc)
        return _done(im, w, h)
    return gcache("helmet", mk)


def rider_head(f, x, y, s, t, mouth=None, expr="n", brow="n", look=(0, 0), op=1.0, blink=None):
    m = talk(t) if mouth is None else mouth
    bl = blink_at(t, 2) if blink is None else blink
    comp(f, scale_el(head_el(m, bl, brow, look[0], look[1], expr), s), x, y, op=op)
    comp(f, scale_el(helmet_el(), s), x, y, op=op)


# ---------------- rocket sled (side view, nose to the right). two layers so the rider sits between ----------------
def sled_el(layer="back"):
    def mk():
        w, h, sc = 780, 320, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        if layer == "back":
            _ov(im, lambda q: q.rounded_rectangle(S(60, 268, 720, 300), 14 * sc, fill=(0, 0, 0, 70)))
            # slippers on the rail
            for x0 in (130, 520): shape_grad(im, lambda m, x0=x0: m.rounded_rectangle(S(x0, 238, x0 + 110, 288), 10 * sc, fill=255), (90, 96, 110), (40, 44, 54))
            # chassis beam + truss
            shape_grad(im, lambda m: m.rounded_rectangle(S(70, 196, 720, 246), 12 * sc, fill=255), (214, 222, 236), (130, 140, 160))
            for i in range(9):
                x = 100 + i * 68; d.line(S(x, 200, x + 34, 242), fill=(110, 118, 136, 255), width=5 * sc); d.line(S(x + 34, 242, x + 68, 200), fill=(110, 118, 136, 255), width=5 * sc)
            # seat back
            shape_grad(im, lambda m: m.rounded_rectangle(S(452, 40, 506, 214), 22 * sc, fill=255), (70, 90, 140), (30, 40, 80))
            # rocket pack
            shape_grad(im, lambda m: m.rounded_rectangle(S(46, 70, 350, 210), 26 * sc, fill=255), (240, 70, 70), (150, 14, 24))
            _ov(im, lambda q: q.rounded_rectangle(S(64, 82, 334, 104), 10 * sc, fill=(255, 255, 255, 70)))
            d.rounded_rectangle(S(46, 150, 350, 172), 0, fill=(255, 255, 255, 255))
            d.text((198 * sc, 161 * sc), "SONIC WIND", font=font(F_BLACK, 20 * sc), fill=RED2 + (255,), anchor="mm")
            for i in range(5): d.ellipse(S(80 + i * 56, 118, 92 + i * 56, 130), fill=(120, 10, 18, 255))
            # three visible nozzles (of nine)
            for yc in (92, 140, 188):
                shape_grad(im, lambda m, yc=yc: m.polygon(S(48, yc - 16, 48, yc + 16, 8, yc + 26, 8, yc - 26), fill=255), (110, 116, 130), (50, 54, 64))
                d.ellipse(S(2, yc - 26, 16, yc + 26), fill=(30, 30, 36, 255))
        else:
            # cockpit side panel + nose
            shape_grad(im, lambda m: m.polygon(S(420, 130, 640, 138, 770, 214, 420, 214), fill=255), (255, 255, 255), (186, 196, 214))
            d.polygon(S(420, 186, 724, 186, 742, 198, 420, 198), fill=RED2 + (255,))
            _ov(im, lambda q: q.line(S(430, 142, 630, 148), fill=(255, 255, 255, 220), width=5 * sc))
            d.line(S(420, 130, 640, 138), fill=(90, 98, 116, 255), width=4 * sc); d.line(S(640, 138, 770, 214), fill=(90, 98, 116, 255), width=4 * sc)
            d.ellipse(S(560, 158, 576, 174), fill=(90, 98, 116, 255))
        return _done(im, w, h)
    return gcache(("sled", layer), mk)


def flame_jet(f, x, y, L, th, t, seed=0, op=1.0):
    """rocket exhaust pointing LEFT from nozzle mouth (x, y)."""
    if L < 4 or op <= 0.01: return
    L = int(L * (0.9 + 0.12 * math.sin(t * 53 + seed * 2.1) + 0.06 * math.sin(t * 91 + seed)))
    pw, ph = L + 60, int(th * 3.2) + 40
    rgb = np.zeros((ph, pw, 3), np.float32); a = np.zeros((ph, pw), np.float32)
    cx = pw - 20; cy = ph // 2
    for frac, wid, col in ((1.0, 1.0, (255, 70, 20)), (0.78, 0.66, (255, 150, 30)), (0.5, 0.36, (255, 236, 150))):
        ll = int(L * frac); tw_ = max(2, int(th * wid))
        pts = np.array([[cx, cy - tw_], [cx - ll * 0.35, cy - tw_ * 1.15], [cx - ll, cy + int(4 * math.sin(t * 40 + seed))], [cx - ll * 0.35, cy + tw_ * 1.15], [cx, cy + tw_]], np.int32)
        cv2.fillPoly(rgb, [pts], C(col), cv2.LINE_AA); cv2.fillPoly(a, [pts], 1.0, cv2.LINE_AA)
    a = cv2.GaussianBlur(a, (0, 0), 2.2); rgb = cv2.GaussianBlur(rgb, (0, 0), 2.2) / np.maximum(a[..., None], 1e-3)
    add_patch(f, int(x - cx), int(y - cy), np.clip(rgb, 0, 1), np.clip(a * op, 0, 1))
    glow(f, x - L * 0.4, y, 60 + L * 0.3, (255, 140, 40), 0.18 * op)


def sled(f, x, y, s=1.0, t=0.0, fire=0.0, expr="n", mouth=None, brow="n", look=(0, 0), straps=True, op=1.0):
    """(x, y) = sled canvas centre.  fire 0..1 = exhaust length."""
    if fire > 0.01:
        for i, yc in enumerate((92, 140, 188)):
            flame_jet(f, x + (2 - 390) * s, y + (yc - 160) * s, (260 + 120 * fire) * s * fire, 20 * s, t, i, op)
    comp(f, scale_el(sled_el("back"), s), x, y, op=op)
    hx, hy = x + (479 - 390) * s, y + (62 - 160) * s
    rider_head(f, hx, hy, 0.62 * s, t, mouth, expr, brow, look, op)
    k = clamp(float(straps))
    if k > 0.01:
        for dx in (-26, 26):
            p0 = (hx + dx * s, hy + 56 * s); p1 = (hx + dx * 0.4 * s, hy + 110 * s)
            q = (p0[0] + (p1[0] - p0[0]) * k, p0[1] + (p1[1] - p0[1]) * k)
            cv2.line(f, (int(p0[0]), int(p0[1])), (int(q[0]), int(q[1])), C(YEL_), max(2, int(9 * s)), cv2.LINE_AA)
    comp(f, scale_el(sled_el("front"), s), x, y, op=op)


def sled_rear_el(lit=0):
    """rear face of the rocket pack: 3 x 3 nozzles, first `lit` glowing."""
    def mk():
        w, h, sc = 520, 470, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(18, 30, 512, 462), 50 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(6, 10, 500, 446), 50 * sc, fill=255), (240, 70, 70), (150, 14, 24))
        d.rounded_rectangle(S(6, 10, 500, 446), 50 * sc, outline=(110, 8, 16, 255), width=6 * sc)
        for i in range(9):
            r_, c_ = divmod(i, 3); cx, cy = 106 + c_ * 147, 92 + r_ * 136
            d.ellipse(S(cx - 58, cy - 58, cx + 58, cy + 58), fill=(70, 74, 86, 255))
            d.ellipse(S(cx - 46, cy - 46, cx + 46, cy + 46), fill=(26, 26, 32, 255))
            if i < lit:
                d.ellipse(S(cx - 40, cy - 40, cx + 40, cy + 40), fill=(255, 120, 30, 255))
                d.ellipse(S(cx - 26, cy - 26, cx + 26, cy + 26), fill=(255, 220, 120, 255))
                d.ellipse(S(cx - 12, cy - 12, cx + 12, cy + 12), fill=(255, 255, 235, 255))
        return _done(im, w, h)
    return gcache(("srear", lit), mk)


# ---------------- desert scenery ----------------
def mesa_el(seed=0, col=(206, 96, 52)):
    def mk():
        w, h, sc = 900, 260, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        rng = np.random.default_rng(seed); x = 0; pts = [(0, 260)]
        while x < 900:
            top = rng.uniform(60, 170); wdt = rng.uniform(120, 260)
            pts += [(x + 30, top), (x + wdt - 30, top), (x + wdt, rng.uniform(190, 240))]; x += wdt
        pts += [(900, 260)]
        d.polygon([(px * sc, py * sc) for px, py in pts], fill=tuple(col) + (255,))
        return _done(im, w, h)
    return gcache(("mesa", seed, col), mk)


def cactus_el(h_=1.0):
    def mk():
        w, h, sc = 200, 320, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        g0, g1 = (70, 170, 80), (30, 110, 50)
        shape_grad(im, lambda m: m.rounded_rectangle(S(80, 20, 124, 320), 22 * sc, fill=255), g0, g1)
        shape_grad(im, lambda m: (m.rounded_rectangle(S(20, 90, 56, 200), 18 * sc, fill=255), m.rounded_rectangle(S(20, 170, 100, 204), 17 * sc, fill=255)), g0, g1)
        shape_grad(im, lambda m: (m.rounded_rectangle(S(146, 60, 182, 170), 18 * sc, fill=255), m.rounded_rectangle(S(104, 140, 182, 174), 17 * sc, fill=255)), g0, g1)
        _ov(im, lambda q: q.line(S(94, 40, 94, 300), fill=(255, 255, 255, 60), width=5 * sc))
        return _done(im, w, h)
    return gcache(("cactus", h_), mk)


def desert(f, t, speed=0.0, track_y=1260, mesa=True, scroll=0.0, water_from=None):
    """ground band + rail; speed in px/s for parallax; scroll = absolute offset alternative."""
    off = scroll if scroll else speed * t
    if mesa:
        mm = mesa_el(3, (190, 80, 44)); ox = -((off * 0.08) % 900)
        for k in range(3): comp(f, mm, ox + 450 + k * 900, track_y - 120, op=0.9)
    gy = track_y + 18
    f[gy:H] = f[gy:H] * 0.55 + np.array(C(SAND), np.float32) * 0.45
    f[gy:gy + 10] *= 0.85
    # sleepers (ties) scroll fast
    sp = 90; o = off % sp
    for k in range(-1, W // sp + 2):
        x = int(k * sp - o); cv2.rectangle(f, (x, gy + 6), (x + 34, gy + 26), C((120, 80, 50)), -1, cv2.LINE_AA)
    cv2.line(f, (0, track_y + 12), (W, track_y + 12), C((90, 96, 110)), 12, cv2.LINE_AA)
    cv2.line(f, (0, track_y + 7), (W, track_y + 7), C((200, 206, 220)), 3, cv2.LINE_AA)
    if water_from is not None and water_from < W:
        x0 = int(max(0, water_from))
        f[gy - 2:gy + 30, x0:W] = f[gy - 2:gy + 30, x0:W] * 0.3 + np.array(C((70, 160, 240)), np.float32) * 0.7
        cv2.line(f, (x0, gy - 2), (W, gy - 2), C((200, 236, 255)), 4, cv2.LINE_AA)
    # near cacti
    cc = cactus_el(); cs = 0.55
    for k in range(4):
        x = (k * 460 + 120 - off * 1.4) % (4 * 460) - 200
        comp(f, scale_el(cc, cs), x, gy + 120 - 320 * cs / 2 + 60, op=1.0)


def speed_lines(f, t, amt, y0=700, y1=1250, n=16, seed=0):
    if amt <= 0.01: return
    rng = np.random.default_rng(seed)
    for i in range(n):
        y = int(rng.uniform(y0, y1)); L = rng.uniform(140, 420) * amt; sp = rng.uniform(1800, 3200)
        x = W - ((t * sp + rng.uniform(0, 2000)) % (W + 600))
        ov = f[max(0, y - 3):y + 4].copy()
        cv2.line(f, (int(x), y), (int(x + L), y), (1, 1, 1), 4, cv2.LINE_AA)
        f[max(0, y - 3):y + 4] = ov * (1 - 0.55 * amt) + f[max(0, y - 3):y + 4] * 0.55 * amt


# ---------------- gauges ----------------
DIALS = {"mph": dict(mx=700, major=100, minor=50, red=(600, 700), unit="MPH"),
         "g": dict(mx=50, major=10, minor=5, red=(18, 50), unit="G")}


def _ang(v, mx): return math.radians(225 - 270 * clamp(v / mx))


def dial_el(kind):
    def mk():
        cfg = DIALS[kind]; w = h = 560; sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        cx = cy = 280; R_ = 250
        _ov(im, lambda q: q.ellipse(S(cx - R_ + 10, cy - R_ + 18, cx + R_ + 10, cy + R_ + 18), fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.ellipse(S(cx - R_, cy - R_, cx + R_, cy + R_), fill=255), (70, 74, 90), (24, 24, 30))
        shape_grad(im, lambda m: m.ellipse(S(cx - R_ + 22, cy - R_ + 22, cx + R_ - 22, cy + R_ - 22), fill=255), (255, 255, 255), (228, 232, 242))
        r0, r1 = cfg["red"]; rr = R_ - 46
        a0 = 225 - 270 * r0 / cfg["mx"]; a1 = 225 - 270 * r1 / cfg["mx"]
        d.arc(S(cx - rr, cy - rr, cx + rr, cy + rr), -a0, -a1, fill=RED2 + (255,), width=26 * sc)
        fnn = font(F_BLACK, 34 * sc)
        v = 0
        while v <= cfg["mx"] + 1e-6:
            a = _ang(v, cfg["mx"]); big = abs(v / cfg["major"] - round(v / cfg["major"])) < 1e-6
            r_a, r_b = R_ - 30, R_ - (70 if big else 52)
            d.line(S(cx + r_a * math.cos(a), cy - r_a * math.sin(a), cx + r_b * math.cos(a), cy - r_b * math.sin(a)), fill=INK + (255,), width=(7 if big else 4) * sc)
            if big:
                rl = R_ - 104; d.text(((cx + rl * math.cos(a)) * sc, (cy - rl * math.sin(a)) * sc), str(int(v)), font=fnn, fill=INK + (255,), anchor="mm")
            v += cfg["minor"]
        d.text((cx * sc, (cy + 86) * sc), cfg["unit"], font=font(F_BLACK, 40 * sc), fill=(120, 126, 140, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("dial", kind), mk)


def readout_el(text, col=WHITE, bg=INK, size=64):
    def mk():
        fn = font(F_BLACK, size * 2); tw = fn.getlength(text) / 2; w, h = int(tw + 60), int(size * 1.45); sc = 2
        im, d = _canvas(w, h); d.rounded_rectangle([0, 0, w * sc - 1, h * sc - 1], 16 * sc, fill=tuple(bg) + (255,))
        d.text((w, h), text, font=fn, fill=tuple(col) + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("readout", text, col, bg, size), mk)


def dial(f, x, y, s, kind, v, txt=None, shake=0.0, mark=None, t=0.0):
    comp(f, scale_el(dial_el(kind), s), x, y)
    cfg = DIALS[kind]; cx, cy = x, y
    if mark is not None:
        a = _ang(mark, cfg["mx"]); r_ = 220 * s
        cv2.line(f, (int(cx + 150 * s * math.cos(a)), int(cy - 150 * s * math.sin(a))), (int(cx + r_ * math.cos(a)), int(cy - r_ * math.sin(a))), C(INK), max(2, int(10 * s)), cv2.LINE_AA)
    a = _ang(v, cfg["mx"]) + (math.radians(2.5) * math.sin(t * 70) * shake)
    L = 200 * s; tip = (cx + L * math.cos(a), cy - L * math.sin(a))
    nrm = (math.sin(a), math.cos(a)); bw = 13 * s
    pts = np.array([[cx + nrm[0] * bw - 30 * s * math.cos(a), cy + nrm[1] * bw + 30 * s * math.sin(a)], [tip[0], tip[1]],
                    [cx - nrm[0] * bw - 30 * s * math.cos(a), cy - nrm[1] * bw + 30 * s * math.sin(a)]], np.int32)
    cv2.fillPoly(f, [pts], C(RED2), cv2.LINE_AA)
    cv2.circle(f, (int(cx), int(cy)), int(30 * s), C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(cx), int(cy)), int(12 * s), C((200, 206, 220)), -1, cv2.LINE_AA)
    if txt: comp(f, scale_el(readout_el(txt, YEL_ if kind == "mph" else WHITE, INK, 60), s), cx, cy + 170 * s)


def stopwatch_el(text, col=INK):
    def mk():
        w, h, sc = 420, 500, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.ellipse(S(20, 106, 412, 498), fill=(0, 0, 0, 70)))
        d.rounded_rectangle(S(170, 20, 250, 70), 14 * sc, fill=(90, 96, 110, 255)); d.rounded_rectangle(S(150, 0, 270, 34), 14 * sc, fill=RED2 + (255,))
        d.rounded_rectangle(S(320, 86, 370, 130), 12 * sc, fill=(90, 96, 110, 255))
        shape_grad(im, lambda m: m.ellipse(S(10, 80, 410, 480), fill=255), (226, 232, 244), (130, 140, 160))
        shape_grad(im, lambda m: m.ellipse(S(40, 110, 380, 450), fill=255), (255, 255, 255), (232, 236, 246))
        for i in range(12):
            a = i * math.pi / 6; d.line(S(210 + 150 * math.cos(a), 280 + 150 * math.sin(a), 210 + 166 * math.cos(a), 280 + 166 * math.sin(a)), fill=INK + (255,), width=5 * sc)
        d.text((210 * sc, 286 * sc), text, font=font(F_BLACK, 104 * sc), fill=tuple(col) + (255,), anchor="mm")
        d.text((210 * sc, 374 * sc), "SECONDS", font=font(F_BLACK, 26 * sc), fill=(120, 126, 140, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("sw", text, col), mk)


# ---------------- water-brake splash ----------------
def splash(f, x, y, t, t0, s=1.0, n=70, seed=4, dur=1.6):
    q = t - t0
    if q < 0 or q > dur: return
    rng = np.random.default_rng(seed)
    fade = clamp((dur - q) / 0.5)
    # big spray sheets
    for side in (1, -1):
        k = eo(clamp(q / 0.35)); hgt = 520 * s * k * (1 - 0.35 * clamp((q - 0.5) / 1.0))
        wd = 260 * s * (0.6 + 0.4 * k)
        pts = np.array([[x, y], [x + side * wd * 0.25, y - hgt], [x + side * wd, y - hgt * 0.75], [x + side * wd * 0.9, y]], np.int32)
        ov = f.copy(); cv2.fillPoly(ov, [pts], C((190, 228, 255)), cv2.LINE_AA)
        f[:] = f * (1 - 0.5 * fade) + ov * 0.5 * fade
    for i in range(n):
        ang = rng.uniform(math.radians(20), math.radians(160)); sp = rng.uniform(600, 1500) * s; r_ = rng.uniform(6, 16) * s
        px = x + math.cos(ang) * sp * q; py = y - math.sin(ang) * sp * q + 1400 * s * q * q
        if py > y + 40: continue
        col = (235, 248, 255) if i % 3 else (110, 190, 250)
        cv2.circle(f, (int(px), int(py)), max(1, int(r_ * (0.6 + 0.4 * fade))), C(col), -1, cv2.LINE_AA)


# ---------------- the eye ----------------
def _eye_vessels(seed=11):
    rng = np.random.default_rng(seed); segs = []
    starts = [(60, 240), (700, 240), (220, 120), (540, 120), (230, 360), (530, 360), (120, 200), (640, 290), (380, 70), (390, 410)]
    for sx, sy in starts:
        for b in range(3):
            x, y = sx + rng.uniform(-12, 12), sy + rng.uniform(-12, 12)
            ang = math.atan2(240 - y, 380 - x) + rng.uniform(-0.7, 0.7); wdt = rng.uniform(3.5, 6.0)
            for k in range(9):
                nx, ny = x + math.cos(ang) * rng.uniform(14, 26), y + math.sin(ang) * rng.uniform(14, 26)
                if math.hypot(nx - 380, ny - 240) < 140: break
                segs.append((x, y, nx, ny, wdt)); x, y = nx, ny; ang += rng.uniform(-0.6, 0.6); wdt *= 0.88
    return segs


_EYE_SEGS = _eye_vessels()


def eye_el(vess=0.0, blood=0.0, pupil=1.0):
    vess = round(clamp(vess) * 20) / 20; blood = round(clamp(blood) * 10) / 10; pupil = round(pupil * 10) / 10
    def mk():
        w, h, sc = 780, 500, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        def almond(m, pad=0):
            top = [(20 + i * 7.4, 250 - math.sin(math.pi * i / 100) * (215 + pad)) for i in range(101)]
            bot = [(760 - i * 7.4, 250 + math.sin(math.pi * i / 100) * (190 + pad)) for i in range(101)]
            m.polygon([(px * sc, py * sc) for px, py in top + bot], fill=255)
        # skin socket
        shape_grad(im, lambda m: m.ellipse(S(0, 0, 780, 500), fill=255), (255, 236, 222), (236, 196, 176))
        shape_grad(im, lambda m: almond(m, 10), (120, 70, 60), (90, 50, 44))
        shape_grad(im, almond, (255, 255, 255), (226, 222, 230))
        # vessels + blood on a sclera-only layer
        ly = Image.new("RGBA", im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(ly)
        nseg = int(len(_EYE_SEGS) * vess)
        for (x0, y0, x1, y1, wd) in _EYE_SEGS[:nseg]: dl.line(S(x0, y0, x1, y1), fill=BLOOD + (230,), width=max(2, int(wd * sc)))
        if blood > 0:
            bl = Image.new("RGBA", im.size, BLOOD + (int(225 * blood),)); ly.alpha_composite(bl)
        mk_ = Image.new("L", im.size, 0); almond(ImageDraw.Draw(mk_))
        im.paste(ly, (0, 0), Image.fromarray(np.minimum(np.asarray(mk_), np.asarray(ly.getchannel("A"))), "L"))
        # iris + pupil
        shape_grad(im, lambda m: m.ellipse(S(250, 110, 510, 370), fill=255), (90, 170, 220), (30, 80, 140))
        d.ellipse(S(250, 110, 510, 370), outline=(20, 50, 90, 255), width=8 * sc)
        for i in range(24):
            a = i * math.pi / 12; d.line(S(380 + 64 * math.cos(a), 240 + 64 * math.sin(a), 380 + 118 * math.cos(a), 240 + 118 * math.sin(a)), fill=(150, 210, 240, 120), width=3 * sc)
        pr = 58 * pupil; d.ellipse(S(380 - pr, 240 - pr, 380 + pr, 240 + pr), fill=(12, 12, 16, 255))
        d.ellipse(S(410, 160, 450, 200), fill=(255, 255, 255, 240)); d.ellipse(S(330, 270, 348, 288), fill=(255, 255, 255, 200))
        # lid line + lashes
        top = [(20 + i * 7.4, 250 - math.sin(math.pi * i / 100) * 215) for i in range(101)]
        d.line([(px * sc, py * sc) for px, py in top], fill=INK + (255,), width=12 * sc, joint="curve")
        for i in range(14, 90, 9):
            px, py = top[i]; a = math.atan2(py - 250, px - 390)
            d.line(S(px, py, px + 34 * math.cos(a), py + 30 * math.sin(a) - 6), fill=INK + (255,), width=7 * sc)
        bot = [(20 + i * 7.4, 250 + math.sin(math.pi * i / 100) * 190) for i in range(101)]
        d.line([(px * sc, py * sc) for px, py in bot], fill=(120, 70, 60, 255), width=6 * sc, joint="curve")
        return _done(im, w, h)
    return gcache(("eye", vess, blood, pupil), mk)


# ---------------- tooth + forceps ----------------
def molar_el():
    def mk():
        w, h, sc = 300, 380, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        def shp(m):
            m.rounded_rectangle(S(30, 40, 270, 210), 70 * sc, fill=255)
            m.ellipse(S(30, 10, 150, 110), fill=255); m.ellipse(S(150, 10, 270, 110), fill=255)
            m.polygon(S(50, 180, 140, 190, 110, 360, 76, 360), fill=255); m.polygon(S(160, 190, 250, 180, 224, 360, 190, 360), fill=255)
        shape_grad(im, shp, (255, 255, 255), (214, 214, 226))
        _ov(im, lambda q: q.arc(S(54, 30, 140, 100), 200, 300, fill=(255, 255, 255, 255), width=10 * sc))
        _ov(im, lambda q: q.line(S(150, 40, 150, 90), fill=(190, 190, 205, 255), width=5 * sc))
        return _done(im, w, h)
    return gcache("molar", mk)


def gum_el():
    def mk():
        w, h, sc = 520, 220, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 30, 520, 220), 90 * sc, fill=255), (250, 130, 150), (200, 70, 96))
        d.ellipse(S(180, 10, 340, 90), fill=(150, 30, 50, 255))
        for x in (60, 410):
            shape_grad(im, lambda m, x=x: m.rounded_rectangle(S(x, -40, x + 60, 70), 24 * sc, fill=255), (255, 255, 255), (214, 214, 226))
        return _done(im, w, h)
    return gcache("gum", mk)


def forceps_el(open_=0.0):
    open_ = round(clamp(open_) * 4) / 4
    def mk():
        w, h, sc = 360, 600, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        g0, g1 = (232, 238, 248), (120, 130, 150)
        sp = 30 * open_
        for side in (-1, 1):
            shape_grad(im, lambda m, side=side: m.polygon(S(180 + side * (16 + sp), 0, 180 + side * (46 + sp), 0, 180 + side * 30, 200, 180 + side * 8, 200), fill=255), g0, g1)
            shape_grad(im, lambda m, side=side: m.polygon(S(180 + side * 8, 200, 180 + side * 30, 200, 180 + side * (70 + sp), 590, 180 + side * (36 + sp), 590), fill=255), g0, g1)
        d.ellipse(S(162, 184, 198, 220), fill=(90, 96, 110, 255))
        return _done(im, w, h)
    return gcache(("forceps", open_), mk)


def burst_el(text, col=YEL_, fg=INK, size=64, n=12):
    def mk():
        fn = font(F_BLACK, size * 2); tw = fn.getlength(text) / 2; R1 = max(tw / 2 + 60, size * 1.6); R0 = R1 * 0.78
        w = h = int(2 * R1 + 20); sc = 2; im, d = _canvas(w, h)
        pts = []
        for i in range(2 * n):
            a = i * math.pi / n; r_ = R1 if i % 2 == 0 else R0; pts.append(((w / 2 + r_ * math.cos(a)) * sc, (h / 2 + r_ * math.sin(a) * 0.82) * sc))
        d.polygon(pts, fill=tuple(col) + (255,), outline=INK + (255,), width=6 * sc)
        d.text((w / 2 * sc, h / 2 * sc), text, font=fn, fill=tuple(fg) + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("burst", text, col, fg, size, n), mk)


# ---------------- weight, scale, dossier, seat, wheel ----------------
def weight_el(text="x18"):
    def mk():
        w, h, sc = 420, 400, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(140, 0, 280, 120), outline=(40, 40, 48, 255), width=26 * sc)
        shape_grad(im, lambda m: m.polygon(S(90, 90, 330, 90, 410, 390, 10, 390), fill=255), (80, 84, 96), (24, 24, 30))
        _ov(im, lambda q: q.polygon(S(100, 100, 150, 100, 80, 380, 26, 380), fill=(255, 255, 255, 40)))
        d.text((210 * sc, 260 * sc), text, font=font(F_BLACK, 120 * sc), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("weight", text), mk)


def bscale_el(crack=0.0):
    crack = round(clamp(crack) * 4) / 4
    def mk():
        w, h, sc = 620, 230, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(20, 70, 616, 226), 40 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.polygon(S(70, 30, 550, 30, 610, 190, 10, 190), fill=255), (255, 255, 255), (214, 220, 234))
        shape_grad(im, lambda m: m.rounded_rectangle(S(10, 180, 610, 220), 16 * sc, fill=255), (190, 196, 212), (130, 138, 156))
        d.rounded_rectangle(S(215, 60, 405, 120), 12 * sc, fill=(30, 34, 40, 255))
        if crack > 0:
            rng = np.random.default_rng(2)
            for k in range(int(6 * crack)):
                x, y = 310, 150; a = rng.uniform(0, 2 * math.pi)
                for j in range(5):
                    nx, ny = x + math.cos(a) * rng.uniform(20, 50), y + math.sin(a) * rng.uniform(8, 20)
                    d.line(S(x, y, nx, ny), fill=INK + (255,), width=4 * sc); x, y = nx, ny; a += rng.uniform(-0.6, 0.6)
        return _done(im, w, h)
    return gcache(("scale", crack), mk)


def dossier_el():
    def mk():
        w, h, sc = 700, 470, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(14, 20, 700, 470), 30 * sc, fill=(0, 0, 0, 70)))
        d.rounded_rectangle(S(0, 0, 686, 452), 30 * sc, fill=(255, 255, 255, 255))
        d.rounded_rectangle(S(0, 0, 686, 96), 30 * sc, fill=NAVY2 + (255,)); d.rectangle(S(0, 60, 686, 96), fill=NAVY2 + (255,))
        d.text((343 * sc, 50 * sc), "U.S. AIR FORCE  ·  1954", font=font(F_BLACK, 40 * sc), fill=(255, 255, 255, 255), anchor="mm")
        d.rounded_rectangle(S(36, 130, 246, 410), 20 * sc, fill=(214, 234, 255, 255))
        hp = _pil_from_el(head_el(0, False, "n", 0, 0, "smirk"), 190 * sc, 181 * sc); im.alpha_composite(hp, (int(46 * sc), int(210 * sc)))
        hm = _pil_from_el(helmet_el(), 235 * sc, 244 * sc); im.alpha_composite(hm, (int(23 * sc), int(178 * sc)))
        fb = font(F_BLACK, 40 * sc); fs = font(F_BOLD, 30 * sc)
        d.text((276 * sc, 168 * sc), "DR. JOHN", font=fb, fill=INK + (255,), anchor="lm")
        d.text((276 * sc, 214 * sc), "PAUL STAPP", font=fb, fill=INK + (255,), anchor="lm")
        d.text((276 * sc, 272 * sc), "Air Force doctor", font=fs, fill=(90, 96, 110, 255), anchor="lm")
        d.text((276 * sc, 312 * sc), "Crash researcher", font=fs, fill=(90, 96, 110, 255), anchor="lm")
        for i, ln in enumerate((300, 240)): d.rounded_rectangle(S(276, 352 + i * 30, 276 + ln, 366 + i * 30), 7 * sc, fill=(220, 224, 234, 255))
        return _done(im, w, h)
    return gcache("dossier", mk)


def seat_el():
    def mk():
        w, h, sc = 520, 640, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        c0, c1 = (70, 74, 90), (30, 32, 40)
        shape_grad(im, lambda m: m.rounded_rectangle(S(170, 0, 350, 110), 40 * sc, fill=255), c0, c1)
        shape_grad(im, lambda m: m.rounded_rectangle(S(80, 90, 440, 520), 80 * sc, fill=255), c0, c1)
        _ov(im, lambda q: q.rounded_rectangle(S(170, 120, 350, 500), 50 * sc, fill=(255, 255, 255, 26)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(40, 470, 480, 620), 60 * sc, fill=255), c0, c1)
        d.rounded_rectangle(S(408, 120, 450, 160), 10 * sc, fill=(150, 156, 170, 255))
        return _done(im, w, h)
    return gcache("seat", mk)


def wheel_el():
    def mk():
        w, h, sc = 520, 300, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(20, 20, 500, 300 + 180), outline=(30, 30, 36, 255), width=40 * sc)
        d.line(S(260, 200, 260, 300), fill=(30, 30, 36, 255), width=40 * sc)
        d.ellipse(S(200, 150, 320, 270), fill=(50, 52, 62, 255))
        return _done(im, w, h)
    return gcache("wheel", mk)


def belt_draw(f, x, y, s, k, clicked=False):
    """3-point seat belt over a seated guy at hip (x, y). k = 0..1 draw-on."""
    if k <= 0: return
    p0 = (x + 120 * s, y - 210 * s); p1 = (x - 70 * s, y + 4 * s)
    q = (p0[0] + (p1[0] - p0[0]) * k, p0[1] + (p1[1] - p0[1]) * k)
    cv2.line(f, (int(p0[0]), int(p0[1])), (int(q[0]), int(q[1])), C((30, 30, 36)), int(30 * s), cv2.LINE_AA)
    cv2.line(f, (int(p0[0]), int(p0[1])), (int(q[0]), int(q[1])), C((70, 74, 90)), int(18 * s), cv2.LINE_AA)
    if k >= 0.999:
        cv2.line(f, (int(x - 110 * s), int(y + 10 * s)), (int(x + 120 * s), int(y + 10 * s)), C((30, 30, 36)), int(30 * s), cv2.LINE_AA)
        cv2.line(f, (int(x - 110 * s), int(y + 10 * s)), (int(x + 120 * s), int(y + 10 * s)), C((70, 74, 90)), int(18 * s), cv2.LINE_AA)
    bx, by = int(q[0]), int(q[1])
    cv2.rectangle(f, (bx - int(30 * s), by - int(18 * s)), (bx + int(30 * s), by + int(18 * s)), C((200, 206, 220)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (bx - int(10 * s), by - int(8 * s)), (bx + int(10 * s), by + int(8 * s)), C(RED2 if clicked else (120, 126, 140)), -1, cv2.LINE_AA)


def bars2(f, base, items, k, t):
    """simple comparison bars: items = [(x, value, col, label)] with height = value*px."""
    for x, hv, col, lab in items:
        hh = max(2, int(hv * clamp(k)))
        f[int(base - hh + 14):int(base), int(x - 95 + 14):int(x + 95 + 14)] *= 0.72
        f[int(base - hh):int(base), int(x - 95):int(x + 95)] = np.array(C(col), np.float32)
        cv2.rectangle(f, (int(x - 95), int(base - hh)), (int(x + 95), int(base)), C(INK), 6, cv2.LINE_AA)
        if k > 0.5: comp(f, chip(lab, INK, WHITE, 30), x, base - hh - 44)


# ---------------- FreshNestHub logo (overrides the OopsMyBusiness one) ----------------
def logo_el():
    def mk():
        w, h, sc = 940, 360, 2; im, d = _canvas(w, h)
        hp = _pil_from_el(head_el(2, False, "up", 0, 0, "n"), 168 * sc, 160 * sc); im.alpha_composite(hp, (int(20 * sc), int(40 * sc)))
        fo = font(F_BLACK, 150 * sc); x = 200 * sc
        for ch in "FRESH": d.text((x, 122 * sc), ch, font=fo, fill=MINTG + (255,), anchor="lm"); x += fo.getlength(ch) - 4 * sc
        d.text((w / 2 * sc + 90 * sc, 270 * sc), "NEST HUB", font=font(F_BLACK, 104 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache("logo_fnh", mk)
