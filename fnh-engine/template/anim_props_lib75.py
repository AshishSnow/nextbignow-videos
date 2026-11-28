# ================= anim_props_lib75.py (= ep 75 anim_props6.py; lib75 sets ACC to berry magenta: your anim_props6 overrides it) (ep 75, 28 Nov): "Do sweets give you worms?" — ACCENT = BERRY MAGENTA (the worm eggs, the route map, the
# question words, the chips). The laddoos keep their brown (they are the innocent suspect); everything else = the ink palette.
# NEW PLACE: set_yard(t, blur, ground_y, dim) + yard_front(f, top_y, t) = a village BACKYARD at noon (lime-washed brick wall, a green hand-pump, a banana
#   plant, a clothesline with a kurta that sways, a neem tree shadow; bare SOIL ground with pebbles) + a soil mound + spinach rows drawn AFTER the people.
# NEW PROPS (ink): egg_el(mood, look, ready) (a worm egg: cream oval shell, a curled baby worm visible inside, ready 0..1 = it wriggles + the shell glows),
#   worm(f, x, y, s, t, ...) (a live pale-pink cartoon roundworm made of a travelling sine; thin=True = a hookworm larva), tin_el(open_k) (the steel laddoo
#   dabba), poop_el() (a small cartoon swirl, flies optional), chappal_el(), foot_el(mud) (a bare foot from the side), mud_on(f, ...) (mud splats).
# NEW CRAFT (ep 75) = THE EYELINE MATCH + THE INSERT SHOT (StudioBinder 'eyeline match' + 'insert shot'; Wikipedia 'Eyeline match'): shot A = Chubby
#   looks OFF-SCREEN (down at his hands / his feet) and HOLDS the look ~8 frames; cut on the look to shot B = what he sees, framed from his eye position
#   (POV: the hands come up from the bottom edge, the same light + colour as A), a slow push-in carries attention to the detail (the eggs); then a
#   REACTION beat. Inserts = short purposeful close-ups of the one detail the line names (the eggs on the fingertips, the larva at the heel, the foot
#   sliding into a chappal), cut in MID-ACTION. Helpers: look_to(), pov_insert(), insert_push() (copied into anim_fx.py).
ACC = (204, 54, 128); ACC_S = (142, 28, 88); ACC_L = (242, 176, 210); ACC_XL = (252, 224, 238)
EGG = (250, 240, 214); EGG_S = (214, 196, 160)
WORM = (240, 170, 170); WORM_S = (196, 112, 118)
SOIL = (150, 108, 72); SOIL_S = (112, 78, 50); SOIL_L = (186, 146, 104)
STEEL = (210, 216, 222); STEEL_S = (150, 158, 170); STEEL_H = (246, 248, 252)
RED = (176, 40, 44); OKG = (40, 140, 80)
PUMP = (70, 140, 100)
SRC_MYTH = "Source: Kokilaben Dhirubhai Ambani Hospital"
SRC_WHO = "Source: WHO, soil-transmitted worm infections"
SRC_CDC = "Source: CDC; WHO"
SC3 = 3
YARD_GROUND = 1330


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


# ---------------- props ----------------
def egg_el(mood="n", look=(0, 0), ready=0.0, seed=751):
    """a WORM EGG buddy: a cream oval shell with a bumpy rim, a curled baby worm seen through it; ready 0..1 = the worm gets bigger + the shell blushes."""
    rk = round(clamp(ready) * 4) / 4
    def mk():
        w, h = 220, 260; im, d, S = _cv(w, h)
        P = _arcpts(110, 130, 86, 108, 0, 360, 30)[:-1]
        _ink_poly(d, P, tuple(int(EGG[i] * (1 - 0.25 * rk) + ACC_XL[i] * 0.25 * rk) for i in range(3)), seed, INK_W, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(120, 40, 260, 260), fill=c), EGG_S, 110)
        # the curled baby worm inside (a spiral ribbon)
        r0 = 34 + 14 * rk
        sp = [(110 + (r0 - 3.2 * a_) * math.cos(a_ * 1.0), 150 + (r0 - 3.2 * a_) * 0.8 * math.sin(a_ * 1.0)) for a_ in np.linspace(0, 8, 40)]
        d.line([(x * SC3, y * SC3) for x, y in sp], fill=ACC_L + (255,), width=int((12 + 4 * rk) * SC3), joint="curve")
        d.line([(x * SC3, y * SC3) for x, y in sp], fill=ACC + (120,), width=int(3 * SC3), joint="curve")
        for a_ in np.linspace(0, 2 * math.pi, 14, endpoint=False):           # bumpy shell texture dots
            x, y = 110 + 74 * math.cos(a_), 130 + 94 * math.sin(a_)
            d.ellipse(S(x - 4, y - 4, x + 4, y + 4), fill=EGG_S + (255,))
        if mood: _face(d, S, 110, 92, 1.15, mood, look)
        return _done(im, w, h)
    return gcache(("egg75", mood, tuple(look), rk, seed), mk)


def worm(f, x, y, s, t, length=260, amp=16, phase_sp=7.0, ang=0.0, thin=False, mood="n", look=(0, 0), op=1.0):
    """a live cartoon worm: a body of overlapping discs along a travelling sine (head at (x, y) moving toward ang deg); thin = hookworm larva."""
    r = (6 if thin else 15) * s; n = 18
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = []
    for i in range(n):
        u = i / (n - 1); L = u * length * s
        off = amp * s * math.sin(u * 2.4 * math.pi - t * phase_sp) * (0.3 + 0.7 * u)
        pts.append((x - ca * L - sa * off, y - sa * L + ca * off))
    g = f if op >= 0.999 else f.copy()
    P = np.int32(pts)
    cv2.polylines(g, [P], False, C(INKC), int(2 * r + 6 * s + 2), cv2.LINE_AA)
    cv2.polylines(g, [P], False, C(WORM), int(2 * r), cv2.LINE_AA)
    for i in range(2, n - 1, 2):                                             # ring segments
        cv2.circle(g, (int(pts[i][0]), int(pts[i][1])), int(r * 0.55), C(WORM_S), max(1, int(2 * s)), cv2.LINE_AA)
    if not thin:
        hx, hy = pts[0]; ex = -sa * 6 * s; ey = ca * 6 * s
        for sg in (-1, 1):
            cv2.circle(g, (int(hx + sg * ex + ca * 3 * s + look[0] * 2 * s), int(hy + sg * ey + sa * 3 * s + look[1] * 2 * s)), max(2, int(3.4 * s)), C(INKC), -1, cv2.LINE_AA)
        if mood == "happy":
            cv2.ellipse(g, (int(hx + ca * 9 * s), int(hy + sa * 9 * s)), (int(6 * s), int(4 * s)), ang, 0, 180, C(INKC), max(1, int(2 * s)), cv2.LINE_AA)
    if g is not f: f[:] = f * (1 - op) + g * op
    return pts[0]


def tin_el(open_k=0.0, seed=752):
    """the steel LADDOO DABBA: a round steel tin seen from the front, laddoos peeking out; open_k lifts + tilts the lid."""
    ok = round(clamp(open_k) * 4) / 4
    def mk():
        w, h = 420, 400; im, d, S = _cv(w, h)
        if ok > 0:
            for j, (lx, ly) in enumerate(((150, 186), (210, 176), (270, 186), (180, 160), (240, 156))):
                _ink_ell(d, lx, ly, 34, 32, (214, 150, 60), seed + 10 + j, 3)
                for k in range(5):
                    a_ = k * 1.3 + j; d.ellipse(S(lx + 18 * math.cos(a_) - 3, ly + 16 * math.sin(a_) - 3, lx + 18 * math.cos(a_) + 3, ly + 16 * math.sin(a_) + 3), fill=(250, 210, 120, 255))
        body = [(70, 190), (350, 190), (340, 370), (80, 370)]
        _ink_poly(d, body, STEEL, seed, INK_W, amp=0.8)
        _shade(im, lambda q, S_: q.polygon(_P(body), fill=255), lambda q, S_, c: q.rectangle(S_(260, 180, 360, 380), fill=c), STEEL_S, 120)
        d.line(S(100, 230, 100, 350), fill=STEEL_H + (255,), width=10 * SC3)
        for yy in (240, 330): d.line(S(76, yy, 344, yy), fill=STEEL_S + (255,), width=3 * SC3)
        # the lid
        ang = -24 * ok; cx, cy = 210 - 60 * ok, 180 - 120 * ok
        lid = [(cx + (px - 210) * math.cos(math.radians(ang)) - (py - 180) * math.sin(math.radians(ang)),
                cy + (px - 210) * math.sin(math.radians(ang)) + (py - 180) * math.cos(math.radians(ang))) for px, py in ((60, 160), (360, 160), (360, 196), (60, 196))]
        _ink_poly(d, lid, STEEL_H, seed + 1, INK_W, amp=0.8)
        kn = (cx + 0 * math.cos(math.radians(ang)) + 30 * math.sin(math.radians(ang)), cy - 30 * math.cos(math.radians(ang)))
        _ink_ell(d, kn[0], kn[1] + 4, 26, 14, STEEL, seed + 2, 3)
        return _done(im, w, h)
    return gcache(("tin75", ok, seed), mk)


def poop_el(seed=753):
    """a small cartoon poop swirl (kept tiny + friendly on the board)."""
    def mk():
        w, h = 220, 200; im, d, S = _cv(w, h)
        for (cx, cy, rx, ry) in ((110, 160, 86, 32), (110, 122, 64, 28), (112, 88, 42, 22)):
            _ink_ell(d, cx, cy, rx, ry, (140, 94, 56), seed + cy, INK_W - 1)
        _ink_poly(d, [(104, 70), (118, 40), (124, 70)], (140, 94, 56), seed + 9, INK_W - 1)
        _shade(im, lambda q, S_: q.ellipse(S_(24, 60, 196, 192), fill=255), lambda q, S_, c: q.rectangle(S_(130, 50, 220, 200), fill=c), (100, 64, 36), 110)
        return _done(im, w, h)
    return gcache(("poop75", seed), mk)


def chappal_el(seed=754, col=(60, 120, 200)):
    """a rubber chappal (flip-flop) from above: cream sole, blue V strap."""
    def mk():
        w, h = 200, 420; im, d, S = _cv(w, h)
        sole = _arcpts(100, 120, 78, 104, 180, 360, 14) + [(178, 300), (164, 380)] + _arcpts(100, 370, 64, 44, 0, 180, 10) + [(36, 380), (22, 300)]
        _ink_poly(d, sole, (246, 240, 226), seed, INK_W, amp=1.0)
        _ink_poly(d, [(40, 310), (100, 120), (160, 310)], None, seed + 1, 22, closed=False, amp=0.6, col=col)
        _ink_ell(d, 100, 120, 12, 12, col, seed + 2, 3)
        return _done(im, w, h)
    return gcache(("chappal75", seed, col), mk)


def foot_el(mud=0.0, seed=755, chappal=0.0):
    """a bare foot from the side (toes right): skin, ink outline, toes, a muddy sole when mud > 0."""
    mk_ = round(clamp(mud) * 2) / 2
    def mk():
        w, h = 560, 300; im, d, S = _cv(w, h)
        P = [(40, 60), (120, 40), (180, 70), (260, 140), (400, 170), (470, 176), (520, 196), (526, 230), (500, 250), (200, 256), (80, 250), (36, 210), (26, 130)]
        _ink_poly(d, P, INK_SKIN, seed, INK_W, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.rectangle(S_(0, 226, 560, 300), fill=c), (214, 150, 120), 130)
        for j, (tx, ty, r) in enumerate(((452, 178, 22), (486, 188, 18), (512, 204, 15))):
            _ink_ell(d, tx, ty, r, r * 0.8, INK_SKIN, seed + 20 + j, 3)
            d.ellipse(S(tx - r * 0.5, ty - r * 0.6, tx + r * 0.3, ty - r * 0.1), fill=(255, 244, 236, 255))
        d.arc(S(60, 120, 120, 180), 200, 330, fill=INKC + (180,), width=3 * SC3)
        if mk_ > 0:
            rng = np.random.default_rng(seed)
            for _ in range(int(14 * mk_)):
                x = rng.uniform(60, 500); r = rng.uniform(10, 24)
                d.ellipse(S(x - r, 236 - r * 0.5, x + r, 252 + r * 0.4), fill=SOIL + (255,))
        return _done(im, w, h)
    return gcache(("foot75", mk_, seed), mk)


def mud_on(f, x, y, s, seed=0, n=7, r=22):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        dx, dy = rng.normal(0, 26 * s), rng.normal(0, 18 * s); rr = rng.uniform(0.5, 1.0) * r * s
        cv2.circle(f, (int(x + dx), int(y + dy)), int(rr), C(SOIL), -1, cv2.LINE_AA)
        cv2.circle(f, (int(x + dx - rr * 0.3), int(y + dy - rr * 0.3)), max(1, int(rr * 0.3)), C(SOIL_L), -1, cv2.LINE_AA)


def soil_patch(f, cx, cy, w, h, seed=0, eggs=0, t=0.0, ready=0.0, egg_s=0.32):
    """a board-style soil mound (brown fill, hatching, pebbles); eggs = how many egg buddies sit in it."""
    pts =[(cx - w / 2 + w * i / 12, cy + h / 2 - h * math.sin(math.pi * i / 12) ** 0.6 + 6 * math.sin(i * 2.3 + seed)) for i in range(13)]
    P = np.int32(pts + [(cx + w / 2, cy + h / 2 + 10), (cx - w / 2, cy + h / 2 + 10)])
    cv2.fillPoly(f, [P], C(SOIL), cv2.LINE_AA)
    x0, y0 = int(max(0, cx - w / 2 - 10)), int(max(0, cy - h / 2 - 10)); x1, y1 = int(min(W, cx + w / 2 + 10)), int(min(H, cy + h / 2 + 12))
    m = np.zeros((y1 - y0, x1 - x0), np.uint8); cv2.fillPoly(m, [P - np.int32([x0, y0])], 255)
    sub = f[y0:y1, x0:x1].copy()
    for k in range(-int(w), int(w), 22):
        cv2.line(sub, (int(cx + k - x0), int(cy + h / 2 - y0)), (int(cx + k + 50 - x0), int(cy - h / 2 - y0)), C(SOIL_S), 3, cv2.LINE_AA)
    mm = (m > 0)[..., None]; f[y0:y1, x0:x1] = np.where(mm, sub, f[y0:y1, x0:x1])
    cv2.polylines(f, [P], True, C(INKC), 6, cv2.LINE_AA)
    rng = np.random.default_rng(seed + 5)
    for _ in range(9):
        px, py = rng.uniform(cx - w * 0.4, cx + w * 0.4), rng.uniform(cy, cy + h * 0.4)
        cv2.ellipse(f, (int(px), int(py)), (9, 6), 0, 0, 360, C(SOIL_L), -1, cv2.LINE_AA)
    for j in range(eggs):
        ex = cx - w * 0.3 + w * 0.6 * (j + 0.5) / max(1, eggs); ey = cy + h * 0.12 + 10 * math.sin(j * 2.1)
        wig = 4 * ready * math.sin(t * 14 + j)
        el_at(f, egg_el("n" if ready < 0.5 else "happy", (0, 0), ready), ex, ey, egg_s, rot=wig)


# ---------------- NEW PLACE: the village BACKYARD at noon ----------------
def set_yard(t=0.0, blur=4, ground_y=YARD_GROUND, dim=0.0):
    """a BACKYARD at noon: lime-washed brick wall, a green hand-pump on the right, a banana plant, a clothesline with a swaying kurta, sky above the wall,
    bare soil ground with pebbles from ground_y. Paper-softened for Chubby INK."""
    def mk():
        f = _vgrad((150, 200, 238), (220, 236, 244), 0, 600)
        f[600:ground_y] = _vgrad((238, 230, 206), (222, 212, 184), 600, ground_y)[600:ground_y]          # the lime-washed wall
        for yy in range(640, ground_y, 46):
            off = 0 if (yy // 46) % 2 else 60
            cv2.line(f, (0, yy), (W, yy), C((206, 194, 164)), 2)
            for xx in range(off, W, 120): cv2.line(f, (xx, yy), (xx, yy + 46), C((206, 194, 164)), 2)
        for (px, py, r) in ((200, 900, 90), (760, 1100, 70)):                                              # peeled plaster patches
            cv2.ellipse(f, (px, py), (r, int(r * 0.6)), 10, 0, 360, C((214, 140, 110)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (0, 588), (W, 616), C((200, 188, 158)), -1); cv2.line(f, (0, 588), (W, 588), C(INKC), 4)
        # a neem tree behind the wall (left)
        for (tx, ty, tr) in ((120, 470, 150), (290, 420, 120), (40, 380, 110)):
            cv2.circle(f, (tx, ty), tr, C((118, 170, 96)), -1, cv2.LINE_AA)
        f = _soft(f, blur + 1)
        # the banana plant (left, in front of the wall)
        cv2.line(f, (150, ground_y), (160, 860), C((120, 160, 80)), 26, cv2.LINE_AA)
        for k, (ang, L) in enumerate(((-130, 300), (-60, 280), (-160, 240), (-20, 260))):
            a = math.radians(ang); ex, ey = 160 + L * math.cos(a), 860 + L * math.sin(a)
            P = np.int32([(160, 860), (160 + L * 0.5 * math.cos(a) - 40 * math.sin(a), 860 + L * 0.5 * math.sin(a) + 40 * math.cos(a)), (ex, ey),
                          (160 + L * 0.5 * math.cos(a) + 30 * math.sin(a), 860 + L * 0.5 * math.sin(a) - 30 * math.cos(a))])
            cv2.fillPoly(f, [P], C((132, 186, 88)), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), 4, cv2.LINE_AA)
            cv2.line(f, (160, 860), (int(ex), int(ey)), C((96, 140, 64)), 3, cv2.LINE_AA)
        # the green hand-pump (right)
        bx = 900
        cv2.rectangle(f, (bx - 30, 980), (bx + 30, ground_y - 10), C(PUMP), -1); cv2.rectangle(f, (bx - 30, 980), (bx + 30, ground_y - 10), C(INKC), 5)
        cv2.rectangle(f, (bx - 50, 950), (bx + 50, 990), C(PUMP), -1); cv2.rectangle(f, (bx - 50, 950), (bx + 50, 990), C(INKC), 5)
        cv2.rectangle(f, (bx - 90, 1040), (bx - 30, 1070), C(PUMP), -1); cv2.rectangle(f, (bx - 90, 1040), (bx - 30, 1070), C(INKC), 4)   # spout
        cv2.line(f, (bx + 40, 960), (bx + 190, 900), C(INKC), 16, cv2.LINE_AA); cv2.line(f, (bx + 40, 960), (bx + 190, 900), C(PUMP), 10, cv2.LINE_AA)
        cv2.rectangle(f, (bx - 140, ground_y - 30), (bx + 60, ground_y + 6), C((190, 190, 186)), -1); cv2.rectangle(f, (bx - 140, ground_y - 30), (bx + 60, ground_y + 6), C(INKC), 4)
        # ground: bare soil
        f[ground_y:] = _vgrad(SOIL_L, SOIL, ground_y, H)[ground_y:]
        rng = np.random.default_rng(75)
        for _ in range(260):
            x = rng.uniform(0, W); y = rng.uniform(ground_y + 10, H); r = rng.uniform(3, 9) * (0.6 + (y - ground_y) / 800)
            cv2.ellipse(f, (int(x), int(y)), (int(r * 1.5), int(r)), 0, 0, 360, C(SOIL_S if rng.uniform() > 0.4 else (204, 170, 130)), -1, cv2.LINE_AA)
        cv2.line(f, (0, ground_y), (W, ground_y), C(INKC), 4)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("yard75", blur, ground_y), mk).copy()
    # the clothesline + a kurta that sways (live)
    cv2.line(f, (0, 700), (W, 660), C(INKC), 3, cv2.LINE_AA)
    sw = 10 * math.sin(t * 1.7)
    kx, ky = 560, 682
    P = np.int32([(kx - 70, ky), (kx + 70, ky - 3), (kx + 80 + sw, ky + 60), (kx + 50 + sw, ky + 62), (kx + 56 + sw * 1.3, ky + 230), (kx - 54 + sw * 1.3, ky + 232), (kx - 48 + sw, ky + 64), (kx - 80 + sw, ky + 62)])
    cv2.fillPoly(f, [P], C((236, 196, 120)), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), 4, cv2.LINE_AA)
    for cxp in (kx - 60, kx + 60): cv2.rectangle(f, (cxp - 5, ky - 12), (cxp + 5, ky + 10), C((214, 90, 70)), -1)
    glow(f, 900, 200, 500, (255, 238, 180), 0.25)
    god_rays(f, 980, 120, t, (255, 236, 176), 0.14, 7, 1700, 1.0, 2.1, 5)
    dust_motes(f, t, 0, 640, W, ground_y, 14, 75, 0.5)
    if dim > 0: f = f * (1 - 0.5 * dim)
    return inkify(f)


def yard_front(f, top_y=1480, t=0.0, spinach=True):
    """a soil mound + spinach rows across the bottom (drawn AFTER the people) = depth; the feet are hidden behind it."""
    pts = [(x, top_y + 18 * math.sin(x / 140.0) + 10 * math.sin(x / 47.0)) for x in range(-20, W + 40, 20)]
    P = np.int32(pts + [(W + 40, H), (-20, H)])
    cv2.fillPoly(f, [P], C(SOIL), cv2.LINE_AA); cv2.polylines(f, [np.int32(pts)], False, C(INKC), 6, cv2.LINE_AA)
    for k in range(-200, W + 200, 26): cv2.line(f, (k, H), (k + 90, int(top_y + 40)), C(SOIL_S), 3, cv2.LINE_AA)
    if spinach:
        for i, x in enumerate(range(60, W, 150)):
            sw = 4 * math.sin(t * 2 + i)
            for j, ang in enumerate((-40, -10, 20, 50)):
                a = math.radians(ang - 90 + sw); L = 70 + 16 * (j % 2)
                ex, ey = x + L * math.cos(a), top_y + 30 + L * math.sin(a)
                cv2.ellipse(f, (int((x + ex) / 2), int((top_y + 30 + ey) / 2)), (int(L / 2), 18), math.degrees(a), 0, 360, C((76, 150, 80)), -1, cv2.LINE_AA)
                cv2.ellipse(f, (int((x + ex) / 2), int((top_y + 30 + ey) / 2)), (int(L / 2), 18), math.degrees(a), 0, 360, C(INKC), 3, cv2.LINE_AA)


# ---------------- the EYELINE MATCH / INSERT helpers (also copied into anim_fx.py) ----------------
def look_to(x0, y0, x1, y1, gain=1.0):
    """the look vector (-1..1) for a character's head at (x0, y0) looking at a point (x1, y1) off- or on-screen."""
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) + 1e-6
    return (clamp(gain * dx / L, -1, 1), clamp(gain * dy / L, -1, 1))


def insert_push(f, t, t0, dur, z0=1.0, z1=1.07, cx=W / 2, cy=H / 2):
    """the slow push-in of an INSERT shot: attention drifts into the detail (ease-out), never a static close-up."""
    k = eo(clamp((t - t0) / max(1e-3, dur)))
    return cam(f, z0 + (z1 - z0) * k, cx, cy)


def pov_insert(f, amt=1.0, blur_edge=7):
    """a POV framing for the 'what he sees' half of an eyeline match: soft focus at the top + bottom edges + a gentle dark oval (his eye's frame)."""
    if amt <= 0: return f
    b = cv2.GaussianBlur(f, (0, 0), blur_edge)
    yy = np.linspace(-1, 1, H, dtype=np.float32)[:, None, None]
    m = np.clip((np.abs(yy) - 0.55) / 0.45, 0, 1) * amt
    f = f * (1 - m) + b * m
    xx = np.linspace(-1, 1, W, dtype=np.float32)[None, :, None]
    v = np.clip((xx ** 2 * 0.9 + yy ** 2 * 0.55 - 0.45) / 0.8, 0, 1) * 0.28 * amt
    return f * (1 - v)
