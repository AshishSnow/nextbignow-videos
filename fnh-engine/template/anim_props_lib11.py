# ================= reusable prop library from ep 11 (mint feels cold): mint leaf, gum stick, menthol key-molecule, COLD alarm
# (calarm, jumpy), ice block, ice cube, frost creep, snow, cold breath, icicles, ice-water glass, thermo_c (°C ticks + alarm trigger line),
# airmeter, ice_floor, nerve_icon_el, think_el (thought bubble); extra stage schemes ice / deepice / mintg =================
SCHEMES["ice"] = ((70, 150, 220), (170, 226, 255), (80, 160, 225), (0.25, 0.5, 0.8))
SCHEMES["deepice"] = ((8, 30, 80), (30, 100, 180), (10, 36, 90), (0.1, 0.3, 0.6))
SCHEMES["mintg"] = ((10, 120, 96), (90, 214, 170), (12, 120, 96), (0.05, 0.42, 0.33))
ICE = (200, 240, 255); ICE_D = (90, 170, 230); MINTL = (60, 200, 120); MINTL_D = (16, 120, 70); MENT = (200, 246, 255); MENT_D = (70, 170, 220)
COLDB = (60, 150, 255); COLDB_D = (20, 70, 190)


# ---------------- mint leaf (pointed oval, serrated look, veins) ----------------
def mint_leaf_el(face=False, mood="n", rot=0):
    def mk():
        w, h, sc = 300, 420, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        pts = []
        for i in range(41):
            a = i / 40 * 2 * math.pi; r_ = 1 + (0.05 if i % 2 else 0)        # small teeth on the edge
            x = 150 + 118 * math.sin(a) * r_; y = 220 - 190 * math.cos(a) * r_ * (1 if math.cos(a) > 0 else 0.85)
            pts.append((x * sc, y * sc))
        body = lambda m: m.polygon(pts, fill=255)
        _outline(im, body, 13)
        shape_grad(im, body, (110, 230, 140), MINTL_D)
        bm = Image.new("L", im.size, 0); body(ImageDraw.Draw(bm))
        def veins(q):
            q.line(S(150, 40, 150, 400), fill=(24, 110, 60, 220), width=7 * sc)
            for k in range(5):
                y0 = 110 + k * 55
                q.line(S(150, y0, 150 - 80 + k * 6, y0 - 50), fill=(24, 110, 60, 180), width=4 * sc)
                q.line(S(150, y0, 150 + 80 - k * 6, y0 - 50), fill=(24, 110, 60, 180), width=4 * sc)
        _masked(im, bm, veins)
        _masked(im, bm, lambda q: q.ellipse(S(70, 90, 140, 170), fill=(255, 255, 255, 70)))
        d.line(S(150, 400, 150, 418), fill=INK + (255,), width=9 * sc)
        if face:
            _eyes(d, S, sc, [(118, 200), (182, 200)], 18, (0, 0), sly=(mood == "sly"), happy=(mood == "happy"))
            d.arc(S(126, 222, 174, 262), 20, 160, fill=INK + (255,), width=5 * sc)
        return _done(im, w, h)
    return gcache(("mleaf", face, mood), mk)


# ---------------- gum stick (generic, mint wrapper peeled back) ----------------
def gum_el():
    def mk():
        w, h, sc = 420, 140, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        stick = lambda m: m.rounded_rectangle(S(20, 30, 400, 110), 18 * sc, fill=255)
        _outline(im, stick, 11)
        shape_grad(im, stick, (250, 252, 248), (210, 220, 214))
        wr = lambda m: m.rounded_rectangle(S(170, 26, 404, 114), 14 * sc, fill=255)
        _outline(im, wr, 9)
        shape_grad(im, wr, (120, 230, 180), (20, 150, 110))
        for k in range(3): d.line(S(200 + k * 60, 40, 230 + k * 60, 100), fill=(255, 255, 255, 120), width=6 * sc)
        d.polygon(S(170, 26, 140, 10, 150, 60, 170, 70), fill=(150, 240, 200, 255), outline=INK + (255,))
        return _done(im, w, h)
    return gcache("gum", mk)


# ---------------- menthol: the "key molecule" (six-sided ring head = menthol's ring, key shaft + teeth) ----------------
def menthol_el(mood="sly", look=(0, 0)):
    def mk():
        w, h, sc = 380, 220, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        cx, cy, R0 = 105, 110, 86
        hexp = [((cx + R0 * math.cos(math.radians(30 + 60 * i))) * sc, (cy + R0 * math.sin(math.radians(30 + 60 * i))) * sc) for i in range(6)]
        def allm(m):
            m.polygon(hexp, fill=255); m.rounded_rectangle(S(170, 92, 370, 128), 10 * sc, fill=255)
            for tx in (300, 342): m.rectangle(S(tx - 12, 120, tx + 12, 168), fill=255)
            m.ellipse(S(256, 38, 296, 78), fill=255); m.line(S(276, 70, 276, 100), fill=255, width=14 * sc)   # side group (the -OH)
        _outline(im, allm, 13)
        shape_grad(im, allm, (240, 252, 255), MENT_D)
        hm = Image.new("L", im.size, 0); ImageDraw.Draw(hm).polygon(hexp, fill=255)
        _masked(im, hm, lambda q: q.polygon(S(cx - 46, cy - 60, cx + 10, cy - 70, cx - 20, cy - 30), fill=(255, 255, 255, 160)))
        # snowflake sparkle on the shaft
        for a in (0, 60, 120):
            r = math.radians(a); d.line(S(220 - 14 * math.cos(r), 110 - 14 * math.sin(r), 220 + 14 * math.cos(r), 110 + 14 * math.sin(r)), fill=(255, 255, 255, 255), width=3 * sc)
        _eyes(d, S, sc, [(cx - 26, cy - 4), (cx + 26, cy - 4)], 17, look, sly=(mood == "sly"), happy=(mood == "happy"))
        if mood == "happy": d.chord(S(cx - 22, cy + 18, cx + 22, cy + 46), 0, 180, fill=(40, 20, 60, 255))
        else: d.arc(S(cx - 22, cy + 6, cx + 22, cy + 40), 20, 150, fill=INK + (255,), width=5 * sc)
        return _done(im, w, h)
    return gcache(("menthol", mood, look), mk)


def menthol(f, x, y, s, t, mood="sly", rot=0.0, op=1.0, look=(0, 0), wig=True):
    rot_comp(f, scale_el(menthol_el(mood, look), s), x, y + (6 * math.sin(t * 6) if wig else 0), rot + (5 * math.sin(t * 4.5) if wig else 0), 1.0, op, 0.25)


# ---------------- COLD alarm (TRPM8, drawn simply): icy-blue siren dome with a snowflake + keyhole ----------------
def _flake(d, S, sc, cx, cy, r, col=(255, 255, 255, 255), wd=4):
    for a in range(0, 180, 60):
        ra = math.radians(a); dx, dy = r * math.cos(ra), r * math.sin(ra)
        d.line(S(cx - dx, cy - dy, cx + dx, cy + dy), fill=col, width=wd * sc)
        for sg in (-1, 1):
            bx, by = cx + sg * dx * 0.6, cy + sg * dy * 0.6
            for b in (-40, 40):
                rb = ra + math.radians(b) + (math.pi if sg < 0 else 0)
                d.line(S(bx, by, bx + 0.3 * r * math.cos(rb), by + 0.3 * r * math.sin(rb)), fill=col, width=max(1, wd - 1) * sc)


def calarm_el(ring=False, key_in=False):
    def mk():
        w, h, sc = 220, 240, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(20, 170, 200, 232), 16 * sc, fill=INK + (255,))
        shape_grad(im, lambda m: m.rounded_rectangle(S(28, 176, 192, 224), 12 * sc, fill=255), (150, 160, 180), (70, 80, 100))
        d.chord(S(34, 30, 186, 250), 180, 360, fill=INK + (255,))
        shape_grad(im, lambda m: m.chord(S(42, 38, 178, 242), 180, 360, fill=255), (235, 252, 255) if ring else (120, 190, 255), (90, 200, 255) if ring else COLDB_D)
        _ov(im, lambda q: q.ellipse(S(62, 60, 100, 108), fill=(255, 255, 255, 150)))
        _flake(d, S, sc, 150, 92, 16, (255, 255, 255, 230), 3)
        kc = (10, 20, 50, 255)
        d.ellipse(S(94, 98, 126, 130), fill=kc); d.polygon(S(100, 120, 120, 120, 128, 160, 92, 160), fill=kc)
        if key_in: d.rounded_rectangle(S(100, 104, 120, 156), 6 * sc, fill=MENT + (255,), outline=INK + (255,), width=3 * sc)
        return _done(im, w, h)
    return gcache(("calarm", ring, key_in), mk)


def calarm(f, x, y, s, t, ring=0.0, key_in=False, jumpy=0.0):
    """cold alarm at (x, y); ring 0..1 = icy glow + shake + sound arcs; jumpy 0..1 = nervous jitter + twitch lines."""
    sh = 6 * ring * math.sin(t * 60) + 4 * jumpy * math.sin(t * 37) * (1 if (t * 3) % 1 < 0.5 else -0.3)
    if ring > 0.05: glow(f, x, y - 30 * s, 170 * s, (120, 210, 255), 0.6 * ring)
    rot_comp(f, scale_el(calarm_el(ring > 0.3, key_in), s), x + sh, y - 3 * jumpy * abs(math.sin(t * 23)), 4 * ring * math.sin(t * 47) + 3 * jumpy * math.sin(t * 31), 1.0, 1.0, 0.2)
    if jumpy > 0.05:
        for sg in (-1, 1):
            for j in range(2):
                a = math.radians(-60 - 25 * j) if sg > 0 else math.radians(-120 + 25 * j)
                r0, r1 = 120 * s, (150 + 12 * math.sin(t * 20 + j)) * s
                cv2.line(f, (int(x + r0 * math.cos(a)), int(y - 40 * s + r0 * math.sin(a))), (int(x + r1 * math.cos(a)), int(y - 40 * s + r1 * math.sin(a))), C(INK), max(2, int(7 * s)), cv2.LINE_AA)
    if ring > 0.3:
        for j in range(3):
            ph = (t * 2.6 + j / 3) % 1.0; r_ = (90 + 140 * ph) * s; op = (1 - ph) * ring
            ov = f.copy()
            for sg in (-1, 1):
                cv2.ellipse(ov, (int(x), int(y - 40 * s)), (int(r_), int(r_)), 0, (200 if sg < 0 else -20), (250 if sg < 0 else 30), C((200, 245, 255)), int(9 * s), cv2.LINE_AA)
            f[:] = f * (1 - op) + ov * op


# ---------------- ice: block that encases a character, cubes, frost creeping in, snow, cold breath, icicles ----------------
def ice_block(f, x0, y0, x1, y1, k, t=0.0):
    """translucent ice slab over a region, growing up from the bottom (k 0..1), with shine streaks + cracks."""
    if k <= 0.01: return
    top = int(y1 - (y1 - y0) * eo(clamp(k)))
    g = f[top:int(y1), int(x0):int(x1)]
    g[:] = g * 0.42 + np.array(C((190, 235, 255)), np.float32) * 0.58
    cv2.rectangle(f, (int(x0), top), (int(x1), int(y1)), C((240, 252, 255)), 10, cv2.LINE_AA)
    cv2.rectangle(f, (int(x0), top), (int(x1), int(y1)), C(ICE_D), 4, cv2.LINE_AA)
    for i, (a, b) in enumerate(((0.12, 0.28), (0.2, 0.34), (0.72, 0.8))):
        xa = x0 + (x1 - x0) * a; xb = x0 + (x1 - x0) * b
        if top < y0 + 60 + i * 30:
            ov = f.copy(); cv2.line(ov, (int(xa), int(y0 + 60 + i * 30)), (int(xb), int(y0 + 220 + i * 30)), C(WHITE), 16 - 4 * i, cv2.LINE_AA)
            f[:] = f * 0.6 + ov * 0.4


def ice_cube_el():
    def mk():
        w, h, sc = 160, 160, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        cube = lambda m: m.rounded_rectangle(S(14, 14, 146, 146), 22 * sc, fill=255)
        _outline(im, cube, 9, ICE_D)
        shape_grad(im, cube, (245, 253, 255), (150, 210, 245))
        _ov(im, lambda q: q.rounded_rectangle(S(30, 26, 90, 50), 10 * sc, fill=(255, 255, 255, 200)))
        _ov(im, lambda q: q.line(S(40, 120, 120, 60), fill=(255, 255, 255, 120), width=6 * sc))
        return _done(im, w, h)
    return gcache("icecube", mk)


def frost(f, amt, seed=7):
    """frost creeping in from the frame edges (amt 0..1): icy tint + crystal strokes, never covering the centre."""
    if amt <= 0.01: return
    edge = np.minimum.reduce([_xx, W - _xx, _yy, H - _yy]) / 420.0
    m = np.clip(1.0 - edge / max(0.05, amt), 0, 1) ** 1.5
    f[:] = f * (1 - 0.6 * m[..., None]) + np.array(C((225, 245, 255)), np.float32) * 0.6 * m[..., None]
    rng = np.random.default_rng(seed)
    ov = f.copy()
    for i in range(int(60 * amt)):
        side = rng.integers(4); u = rng.uniform(0, 1)
        x, y = [(u * W, 0), (u * W, H), (0, u * H), (W, u * H)][side]
        L = rng.uniform(60, 260) * amt; a = [math.pi / 2, -math.pi / 2, 0, math.pi][side] + rng.uniform(-0.6, 0.6)
        ex, ey = x + L * math.cos(a), y + L * math.sin(a)
        cv2.line(ov, (int(x), int(y)), (int(ex), int(ey)), C(WHITE), 3, cv2.LINE_AA)
        for b in (-0.7, 0.7):
            mx, my = x + 0.6 * L * math.cos(a), y + 0.6 * L * math.sin(a)
            cv2.line(ov, (int(mx), int(my)), (int(mx + 0.3 * L * math.cos(a + b)), int(my + 0.3 * L * math.sin(a + b))), C(WHITE), 2, cv2.LINE_AA)
    f[:] = f * 0.4 + ov * 0.6


def snow(f, t, amt=1.0, n=46, seed=5, y0=0, y1=H):
    if amt <= 0.01: return
    rng = np.random.default_rng(seed)
    for i in range(n):
        x0 = rng.uniform(0, W); sp = rng.uniform(90, 220); r = rng.uniform(5, 12); ph = rng.uniform(0, 1)
        y = y0 + ((t * sp + ph * (y1 - y0)) % (y1 - y0)); x = x0 + 30 * math.sin(t * 1.3 + i)
        cv2.circle(f, (int(x), int(y)), max(2, int(r * amt)), C(WHITE), -1, cv2.LINE_AA)


def breath(f, x, y, t, t0, dir_=1, s=1.0, dur=1.2):
    """cold breath: a soft white vapour cloud puffing out of a mouth."""
    q = t - t0
    if q < 0 or q > dur: return
    k = q / dur
    for i in range(5):
        px = x + dir_ * (40 + 160 * eo(k) * (0.5 + 0.12 * i)) * s; py = y - 30 * k * s + 16 * math.sin(i * 1.7) * s
        r = (26 + 40 * k + 6 * i) * s
        ov = f.copy(); cv2.circle(ov, (int(px), int(py)), int(r), C(WHITE), -1, cv2.LINE_AA)
        a = 0.55 * (1 - k); f[:] = f * (1 - a) + ov * a


def icicles(f, x, y, w, k=1.0, n=6, s=1.0):
    if k <= 0.01: return
    for i in range(n):
        px = x - w / 2 + (i + 0.5) * w / n; L = (30 + 26 * ((i * 7) % 3)) * s * k
        P = np.array([[px - 12 * s, y], [px + 12 * s, y], [px, y + L]], np.int32)
        cv2.fillPoly(f, [P], C(ICE), cv2.LINE_AA); cv2.polylines(f, [P], True, C(ICE_D), max(2, int(3 * s)), cv2.LINE_AA)


def ice_glass_el(level=0.8, ice=True):
    def mk():
        w, h, sc = 180, 300, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        glass = lambda m: m.polygon(S(14, 10, 166, 10, 146, 290, 34, 290), fill=255)
        _outline(im, glass, 11)
        shape_grad(im, glass, (236, 246, 255), (200, 220, 240))
        y0 = 290 - 270 * level
        gm = Image.new("L", im.size, 0); glass(ImageDraw.Draw(gm))
        _masked(im, gm, lambda q: q.rectangle(S(0, y0, 180, 300), fill=(150, 210, 255, 255)))
        _masked(im, gm, lambda q: q.rectangle(S(0, (y0 + 290) / 2, 180, 300), fill=(90, 160, 240, 150)))
        if ice:
            for (cx, cy, a) in ((62, y0 + 20, 10), (112, y0 + 34, -14), (86, y0 + 74, 6)):
                P = [((cx + 26 * math.cos(math.radians(a + 45 + 90 * i))) * sc, (cy + 26 * math.sin(math.radians(a + 45 + 90 * i))) * sc) for i in range(4)]
                _masked(im, gm, lambda q, P=P: q.polygon(P, fill=(240, 252, 255, 235), outline=(110, 180, 230, 255)))
        _masked(im, gm, lambda q: q.line(S(36, 30, 48, 270), fill=(255, 255, 255, 150), width=10 * sc))
        return _done(im, w, h)
    return gcache(("iceglass", level, ice), mk)


# ---------------- thermometer with °C ticks + an alarm "trigger line" ----------------
def thermo_c(f, x, y, k, h_=560, col=(60, 150, 255), trig=None, trig_col=COLDB, labels=((0, "0"), (0.5, "25"), (1.0, "50")), trig_lab=None):
    """thermometer (bulb at (x, y)); k 0..1 fill; trig = 0..1 level of the alarm trigger line (alarm rings below it)."""
    thermo(f, x, y, k, h_, col)
    for v, lab in labels:
        yy = y - 20 - (h_ - 40) * v
        cv2.line(f, (int(x - 46), int(yy)), (int(x - 30), int(yy)), C(INK), 5, cv2.LINE_AA)
        comp(f, chip(lab + "°C", INK, WHITE, 24), x - 110, yy)
    if trig is not None:
        yy = y - 20 - (h_ - 40) * trig
        for xx in range(int(x - 60), int(x + 260), 26): cv2.line(f, (xx, int(yy)), (xx + 14, int(yy)), C(trig_col), 7, cv2.LINE_AA)
        if trig_lab: comp(f, chip(trig_lab, trig_col, WHITE, 26), x + 170, yy - 34)


# ---------------- airflow meter (generic gauge on a box) ----------------
def airmeter(f, x, y, s, v, label="AIRFLOW", t=0.0):
    cv2.rectangle(f, (int(x - 150 * s), int(y - 120 * s)), (int(x + 150 * s), int(y + 150 * s)), C(INK), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - 138 * s), int(y - 108 * s)), (int(x + 138 * s), int(y + 138 * s)), C((90, 120, 230)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y + 10 * s)), int(100 * s), C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y + 10 * s)), int(90 * s), C(WHITE), -1, cv2.LINE_AA)
    for i in range(7):
        a = math.radians(210 - 240 * i / 6)
        cv2.line(f, (int(x + 70 * s * math.cos(a)), int(y + 10 * s - 70 * s * math.sin(a))), (int(x + 86 * s * math.cos(a)), int(y + 10 * s - 86 * s * math.sin(a))), C(INK), max(2, int(5 * s)), cv2.LINE_AA)
    a = math.radians(210 - 240 * clamp(v) + 2 * math.sin(t * 9))
    cv2.line(f, (int(x), int(y + 10 * s)), (int(x + 76 * s * math.cos(a)), int(y + 10 * s - 76 * s * math.sin(a))), C(RED_), max(2, int(8 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y + 10 * s)), int(12 * s), C(INK), -1, cv2.LINE_AA)
    comp(f, chip(label, INK, WHITE, int(24 * s + 2)), x, y - 82 * s)


def ice_floor(f, x0, x1, y, th=40):
    cv2.rectangle(f, (int(x0), int(y)), (int(x1), int(y + th)), C(ICE), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x0), int(y)), (int(x1), int(y + th)), C(ICE_D), 5, cv2.LINE_AA)
    for xx in range(int(x0 + 30), int(x1 - 30), 90): cv2.line(f, (xx, int(y + 10)), (xx + 40, int(y + 10)), C(WHITE), 5, cv2.LINE_AA)


def nose_cold(f, x, y, s, t, red=0.0):
    """big side-view cartoon nose (stuffy = red tip) — used for the nose-trick part."""
    col = tuple(int(a + (b - a) * red) for a, b in zip((255, 214, 186), (255, 120, 120)))
    P = np.array([[x - 60 * s, y - 200 * s], [x + 40 * s, y - 40 * s], [x + 110 * s, y + 60 * s], [x + 70 * s, y + 110 * s], [x - 40 * s, y + 110 * s], [x - 80 * s, y]], np.int32)
    cv2.fillPoly(f, [P], C(INK), cv2.LINE_AA)
    P2 = (P - np.array([x, y])) * 0.9 + np.array([x, y]); cv2.fillPoly(f, [P2.astype(np.int32)], C(col), cv2.LINE_AA)
    cv2.ellipse(f, (int(x + 30 * s), int(y + 80 * s)), (int(30 * s), int(14 * s)), 0, 0, 360, C(INK), -1, cv2.LINE_AA)


def nerve_icon_el():
    def mk():
        w, h, sc = 200, 200, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.line(S(100, 190, 90, 120, 100, 60), fill=INK + (255,), width=26 * sc, joint="curve")
        d.line(S(100, 190, 90, 120, 100, 60), fill=NERVE + (255,), width=16 * sc, joint="curve")
        d.ellipse(S(70, 30, 130, 90), fill=INK + (255,)); d.ellipse(S(78, 38, 122, 82), fill=NERVE + (255,))
        return _done(im, w, h)
    return gcache("nerveicon", mk)


def think_el(text, size=40):
    """thought bubble with text (cloud + two small trailing circles at bottom-left)."""
    def mk():
        fn = font(F_BLACK, size * 2); tw = fn.getlength(text) / 2; w, h = int(tw + 120), int(size * 2.6 + 70); sc = 2
        im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def cloud(m):
            m.rounded_rectangle(S(10, 10, w - 10, h - 60), int((h - 70) / 2) * sc, fill=255)
            m.ellipse(S(40, h - 66, 70, h - 36), fill=255); m.ellipse(S(22, h - 34, 38, h - 18), fill=255)
        _outline(im, cloud, 9)
        cm = Image.new("L", im.size, 0); cloud(ImageDraw.Draw(cm))
        im.paste(Image.new("RGBA", im.size, (255, 255, 255, 255)), (0, 0), cm.filter(ImageFilter.MinFilter(9)))
        d.text((w / 2 * sc, (h - 60) / 2 * sc + 5 * sc), text, font=fn, fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("think", text, size), mk)
