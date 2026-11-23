# ================= anim_props_lib60.py (ep 60, 23 Nov): "Does spicy food give you stomach ulcers?" — sets ACC to CHILLI RED (your anim_props6 overrides it)
# (the chilli, the curry, the hot words, the sore). The germ is the story's second colour: a sickly OLIVE (only on H. pylori).
# NEW CRAFT (ep 60) = STEAM FROM HOT FOOD (effects animation): food_steam(...) = soft ribbons that rise from a hot dish as a WAVE travelling up
# a simple centreline (Clip Studio Tips 'animated hot steam': steam = 'a wave, float up from the cup', keep the line simple, fade the top with a soft
# brush, grey + an Add/glow blend instead of flat white, denser core / softer edge); each ribbon WIDENS and SLOWS as it climbs, sways more near
# the top, breaks into separate wisps high up, fades in at the base and out at the top; ribbons restart on staggered, uneven cycles so it never
# pulses; a lighten (screen) blend so it glows on dark sets, plus an optional faint ink stroke for white boards. (Moved into anim_fx.py.)
# NEW PLACE: set_lab(t, dim) + lab_front(f, top_y) = a 1982 hospital LAB at night (pale green tiles, a fluorescent tube, shelves of bottles, a night
# window, a wall calendar 1982); a bench top drawn after the people.
# Props: pylori(f, ...) = the H. pylori germ buddy (an olive S-shaped rod with whipping tails at one end; live tails), curry_el (steel katori of red
# curry with chillies), red_chilli_el (ink chilli with a face), scope_view (the round microscope view: pink stomach cells + wriggling spiral germs),
# sore(f, ...) = an ulcer crater on the board stomach lining, broth_glass (a glass of murky olive germ broth). =================
ACC = (214, 52, 40); ACC_S = (150, 26, 20); ACC_L = (246, 150, 130); ACC_XL = (252, 222, 214)      # chilli red
GERM = (150, 168, 70); GERM_S = (98, 116, 36); GERM_L = (206, 218, 140)
TILE = (206, 226, 214); TILE_S = (170, 196, 182)
STEEL = (200, 206, 214); STEEL_S = (142, 150, 162)
CURRY = (200, 60, 30); CURRY_S = (150, 34, 16); OIL = (236, 120, 40)
GREEN_CH = (70, 150, 60)
PINKC = (240, 180, 176); PINKC_S = (214, 130, 128)
RED = (176, 40, 44); OKG = (40, 140, 80); GOLD = (232, 176, 40)
COAT = (246, 248, 250)
SRC_HARV = "Source: Harvard Health (2026); University Hospitals (2025)"
SRC_STING = "Source: Live Science; Harvard Health"
SRC_NOBEL = "Source: Nobel Prize press release (2005)"
SRC_BMJ = "Source: BMJ (2005); Nobel Prize press release"
SRC_UH = "Source: University Hospitals (2025)"
SC3 = 3


# ---------------- CRAFT: steam from hot food ----------------
def food_steam(f, x, y, t, w=120, h=420, n=4, s=1.0, seed=0, amt=1.0, col=(255, 250, 244), ink=None, period=2.6, sway=1.0):
    """STEAM rising off hot food at (x, y) (the food surface). n ribbons; each one is a wave travelling up a simple centreline: it fades in at the
    base, widens + slows + sways more as it climbs, breaks into separate wisps in its upper half and fades out at the top. Every ribbon has its
    own (uneven) cycle so the steam never pulses together. Lighten blend (glows on dark sets); ink > 0 adds a faint warm-ink curl stroke so
    it still reads on white paper."""
    if amt <= 0.01: return
    if ink is None:                                                     # auto: on a light background the glow alone vanishes -> add the ink curl
        yy0, yy1 = int(max(0, y - h)), int(max(1, y)); xx0, xx1 = int(max(0, x - w)), int(min(W, x + w))
        ink = 0.55 if float(f[yy0:yy1:8, xx0:xx1:8].mean()) > 0.62 else 0.0
    x0, x1 = int(max(0, x - w - 140 * s)), int(min(W, x + w + 140 * s)); y0, y1 = int(max(0, y - h * 1.05)), int(min(H, y + 20))
    if x1 <= x0 or y1 <= y0: return
    L = np.zeros((y1 - y0, x1 - x0), np.float32); Li = np.zeros_like(L)
    rng = np.random.default_rng(seed)
    for i in range(n):
        per = period * rng.uniform(0.8, 1.25); off = rng.uniform(0, per); bx = x + rng.uniform(-w / 2, w / 2); ph0 = rng.uniform(0, 6.28)
        life = ((t + off) % per) / per                                  # 0..1 over this ribbon's cycle
        head = min(1.0, life * 1.6)                                     # how far up the ribbon has reached
        tail = max(0.0, life * 1.6 - 0.75)                              # the bottom lets go late in the cycle (the ribbon detaches + rises)
        m = 26; pts = []
        for j in range(m + 1):
            v = tail + (head - tail) * j / m
            amp = (6 + 46 * v * v) * s * sway
            wav = math.sin(v * 7.5 - t * (2.6 - 1.2 * v) + ph0)       # the wave travels up, slower near the top
            pts.append((bx - x0 + amp * wav + 18 * s * v * math.sin(t * 0.7 + ph0), y - y0 - v * h, v))
        for j in range(m):
            v = pts[j][2]
            if v > 0.5 and math.sin(v * 19 + t * 1.6 + ph0 * 3) > 0.45: continue            # breaks into separate wisps higher up
            a = min(1.0, v / 0.12) * (1 - v) ** 1.4                                          # fade in at the base, out at the top
            wd = max(2, int((10 + 34 * v) * s))                                              # widens as it climbs
            p0, p1 = (int(pts[j][0]), int(pts[j][1])), (int(pts[j + 1][0]), int(pts[j + 1][1]))
            cv2.line(L, p0, p1, float(a), wd, cv2.LINE_AA)
            if ink > 0 and v < 0.8: cv2.line(Li, p0, p1, float(a), max(1, int(3 * s)), cv2.LINE_AA)
    L = cv2.GaussianBlur(L, (0, 0), 7 * s) * (0.55 + 0.35 * (ink > 0)) * amt
    roi = f[y0:y1, x0:x1]
    c = np.array(C(col), np.float32)
    roi[:] = 1 - (1 - roi) * (1 - L[..., None] * c)                                          # lighten / screen
    if ink > 0:
        Li = cv2.GaussianBlur(Li, (0, 0), 0.8) * ink * amt
        roi[:] = roi * (1 - Li[..., None]) + np.array(C((150, 136, 128)), np.float32) * Li[..., None]


# ---------------- the germ: H. pylori ----------------
def _pyl_pts(L=220, A=30, wdt=34, n=18):
    cl = [(-L / 2 + L * u, A * math.sin(2 * math.pi * u)) for u in np.linspace(0, 1, n)]
    top, bot = [], []
    for i, (px, py) in enumerate(cl):
        u = i / (n - 1); dydx = A * 2 * math.pi / L * math.cos(2 * math.pi * u)
        nx, ny = -dydx, 1.0; nl = math.hypot(nx, ny); nx, ny = nx / nl, ny / nl
        r = wdt * (0.55 + 0.45 * math.sin(math.pi * min(1, u * 1.15 + 0.05)) ** 0.4)
        top.append((px + nx * r, py - ny * r)); bot.append((px - nx * r, py + ny * r))
    return cl, top + bot[::-1]


def pylori_el(mood="sly", look=(0, 0), seed=601):
    """the H. pylori buddy body (no tails): an olive S-shaped rod with one wobbly ink outline, a shadow side + hatching, a 3-stroke face near
    the front (right) end. 320 x 180, body centre at (160, 90)."""
    def mk():
        w, h = 320, 180; im, d, S = _cv(w, h)
        cl, P = _pyl_pts()
        P = [(160 + px, 90 + py) for px, py in P]
        _ink_poly(d, P, GERM, seed, INK_W, amp=1.0)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.polygon(_P([(160 + px, 90 + py + 18) for px, py in _pyl_pts()[1]]), fill=c), GERM_S, 110)
        for k in range(6):                                                    # little spots
            u = 0.15 + 0.12 * k; px = -110 + 220 * u; py = 30 * math.sin(2 * math.pi * u)
            d.ellipse(S(160 + px - 4, 90 + py - 4, 160 + px + 4, 90 + py + 4), fill=GERM_S + (200,))
        m_ = {"sly": "n", "evil": "angry"}.get(mood, mood)
        _face(d, S, 160 + 70, 90 + 30 * math.sin(2 * math.pi * 0.82) - 2, 1.15, m_, look)
        if mood in ("sly", "evil"):                                           # a sly grin
            d.line([tuple(q * SC3 for q in p) for p in _arcpts(160 + 70, 90 + 30 * math.sin(2 * math.pi * 0.82) + 10, 14, 7, 10, 170, 8)], fill=INKC + (255,), width=4 * SC3)
        return _done(im, w, h)
    return gcache(("pylori60", mood, look, seed), mk)


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


def pylori(f, x, y, s, t, rot=0.0, mood="sly", look=(0, 0), ph=0.0, swim=1.0, op=1.0):
    """the germ with LIVE whipping tails (flagella) out of its back (left) end: each tail is a wave travelling out, slightly different speeds."""
    a = math.radians(rot); ca, sa = math.cos(a), math.sin(a)
    ex, ey = -112 * s, 0.0
    bx, by = x + ex * ca + ey * sa, y - ex * sa + ey * ca
    for k in range(4):
        pts = []
        ang0 = math.radians(180 + (k - 1.5) * 16)
        for j in range(14):
            u = j / 13; L = 120 * s * u
            wv = 14 * s * u * math.sin(u * 9 - t * (11 + k * 1.3) * swim + ph + k)
            lx, ly = L * math.cos(ang0) - wv * math.sin(ang0), -(L * math.sin(ang0)) + wv * math.cos(ang0)
            pts.append((bx + lx * ca + ly * sa, by - lx * sa + ly * ca))
        cv2.polylines(f, [np.int32(pts)], False, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    rot_comp(f, scale_el(pylori_el(mood, look), s), x, y, rot, 1.0, op, 0.0)


# ---------------- food ----------------
def red_chilli_el(mood=None, look=(0, 0), seed=602):
    """a red chilli lying on its side: curved pod, green cap + stem, a shine, an optional 3-stroke face. 320 x 140, centre (160, 70)."""
    def mk():
        w, h = 320, 140; im, d, S = _cv(w, h)
        top = [(70, 50), (120, 38), (180, 40), (240, 54), (282, 78), (300, 104)]
        bot = [(296, 108), (262, 96), (210, 86), (150, 90), (100, 96), (66, 90)]
        P = top + bot
        _ink_poly(d, P, ACC, seed, INK_W, amp=1.0)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.polygon(_P([(60, 80), (300, 92), (300, 120), (60, 120)]), fill=c), ACC_S, 110)
        d.line([tuple(q * SC3 for q in p) for p in ((112, 50), (176, 47), (226, 58))], fill=(255, 220, 210, 230), width=6 * SC3)
        _ink_poly(d, [(50, 44), (78, 40), (84, 66), (78, 94), (50, 96), (44, 70)], GREEN_CH, seed + 1, INK_W - 1, amp=0.8)
        d.line([tuple(q * SC3 for q in p) for p in ((48, 70), (26, 62), (12, 44))], fill=GREEN_CH + (255,), width=8 * SC3)
        d.line([tuple(q * SC3 for q in p) for p in ((48, 70), (26, 62), (12, 44))], fill=INKC + (255,), width=2 * SC3)
        if mood: _face(d, S, 170, 66, 1.1, mood, look)
        return _done(im, w, h)
    return gcache(("rchilli60", mood, look, seed), mk)


def curry_el(level=1.0, seed=603):
    """a steel katori of red curry seen from the front-top: steel body with a rim, a red curry surface with oil specks and two chillies. 360 x 220,
    the curry surface centre at (180, 70) (steam goes there)."""
    def mk():
        w, h = 360, 220; im, d, S = _cv(w, h)
        _ink_poly(d, [(20, 70), (340, 70), (312, 190), (48, 190)], STEEL, seed, INK_W, amp=0.6)
        _shade(im, lambda q, S_: q.polygon(_P([(20, 70), (340, 70), (312, 190), (48, 190)]), fill=255),
               lambda q, S_, c: q.polygon(_P([(220, 70), (340, 70), (312, 190), (200, 190)]), fill=c), STEEL_S, 120)
        d.line([tuple(q * SC3 for q in p) for p in ((70, 100), (84, 176))], fill=(255, 255, 255, 220), width=8 * SC3)
        _ink_ell(d, 180, 70, 160, 36, STEEL, seed + 1, INK_W, amp=0.6)
        if level > 0:
            _ink_ell(d, 180, 72, 140, 26, CURRY, seed + 2, 3, amp=0.6)
            rng = np.random.default_rng(seed)
            for k in range(12):
                xx, yy = 180 + rng.uniform(-110, 110), 72 + rng.uniform(-14, 14)
                d.ellipse(S(xx - 5, yy - 3, xx + 5, yy + 3), fill=OIL + (230,))
            d.line([tuple(q * SC3 for q in p) for p in ((96, 66), (130, 74), (168, 70))], fill=GREEN_CH + (255,), width=10 * SC3)
            d.line([tuple(q * SC3 for q in p) for p in ((200, 76), (238, 64), (262, 70))], fill=ACC_S + (255,), width=10 * SC3)
        return _done(im, w, h)
    return gcache(("curry60", round(level, 1), seed), mk)


def broth_glass(level=0.75):
    """a glass of murky olive germ broth (the self-experiment): lib24 glass2_el in germ colour."""
    return glass2_el(col=GERM_L, level=level, seed=604)


# ---------------- the board stomach + an ulcer on its lining ----------------
STOM = [(500, 560), (488, 620), (420, 600), (346, 650), (310, 760), (318, 900), (360, 1030), (450, 1120), (580, 1160), (720, 1140), (830, 1080),
        (900, 1010), (960, 985), (1000, 990), (1000, 930), (950, 925), (880, 945), (790, 990), (680, 1000), (590, 960), (548, 880), (560, 760),
        (590, 650), (590, 560)]


def board_stomach(f, t, k=1.0, dx=0, dy=0, sc=1.0, seed=600, lining=1.0, col=None):
    """the J-shaped board stomach (from ep 54) + a pale pink lining that floods in once drawn."""
    P = [(540 + (x - 600) * sc + dx, 860 + (y - 860) * sc + dy) for x, y in STOM]
    if k >= 0.999 and lining > 0:
        m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [np.int32(P)], 255, cv2.LINE_AA)
        a = (m.astype(np.float32) / 255 * 0.55 * lining)[..., None]
        f[:] = f * (1 - a) + np.array(C(col or PINKC), np.float32) * a
    draw_on(f, P, k, BP_INK, 8, seed=seed, tip=k < 1, closed=True)
    return P


def sore(f, x, y, r, k=1.0, t=0.0, sting=0.0):
    """an ULCER = a sore crater in the lining: a red ring, a dark hatched pit, sting 0..1 = it flares (glow + heat ticks)."""
    if k <= 0.01: return
    rr = r * eob(min(1.0, k))
    if sting > 0: glow(f, x, y, rr * 2.6, (255, 90, 60), 0.55 * sting)
    cv2.ellipse(f, (int(x), int(y)), (int(rr), int(rr * 0.62)), 0, 0, 360, C(ACC_L), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (int(rr * 0.62), int(rr * 0.38)), 0, 0, 360, C(ACC_S), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (int(rr), int(rr * 0.62)), 0, 0, 360, C(BP_INK), 5, cv2.LINE_AA)
    if sting > 0:
        for j in range(6):
            a = j / 6 * 2 * math.pi + t * 0.5; L0, L1 = rr * 1.2, rr * (1.5 + 0.3 * math.sin(t * 20 + j))
            cv2.line(f, (int(x + L0 * math.cos(a)), int(y + L0 * math.sin(a) * 0.7)), (int(x + L1 * math.cos(a)), int(y + L1 * math.sin(a) * 0.7)),
                     C(ACC), 5, cv2.LINE_AA)


def eob(k): return 1 + 2.70158 * (k - 1) ** 3 + 1.70158 * (k - 1) ** 2


# ---------------- the microscope view ----------------
def scope_view(f, cx, cy, r, t, k=1.0, n=7, seed=605):
    """the round microscope view: pink stomach-lining cells with nuclei, spiral germs wriggling over them, a dark eyepiece ring."""
    if k <= 0.01: return
    rr = int(r * eob(min(1.0, k)))
    lay = f.copy()
    cv2.circle(lay, (int(cx), int(cy)), rr, C((250, 222, 220)), -1, cv2.LINE_AA)
    rng = np.random.default_rng(seed)
    for i in range(22):
        a = rng.uniform(0, 2 * math.pi); d_ = rng.uniform(0, rr * 0.9); px, py = cx + d_ * math.cos(a), cy + d_ * math.sin(a)
        cv2.ellipse(lay, (int(px), int(py)), (int(rr * 0.16), int(rr * 0.12)), rng.uniform(0, 180), 0, 360, C(PINKC_S), 3, cv2.LINE_AA)
        cv2.circle(lay, (int(px), int(py)), int(rr * 0.035), C((170, 100, 130)), -1, cv2.LINE_AA)
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi); d_ = rng.uniform(0, rr * 0.7)
        px = cx + d_ * math.cos(a) + 20 * math.sin(t * 1.3 + i); py = cy + d_ * math.sin(a) + 14 * math.cos(t * 1.1 + i)
        ang = rng.uniform(0, 2 * math.pi) + 0.4 * math.sin(t * 2 + i)
        pts = []
        for j in range(16):
            u = j / 15 - 0.5; L = rr * 0.22
            wv = rr * 0.035 * math.sin(u * 14 + t * 9 + i)
            pts.append((px + u * L * math.cos(ang) - wv * math.sin(ang), py + u * L * math.sin(ang) + wv * math.cos(ang)))
        cv2.polylines(lay, [np.int32(pts)], False, C(GERM_S), max(4, int(rr * 0.04)), cv2.LINE_AA)
    m = np.zeros((H, W), np.float32); cv2.circle(m, (int(cx), int(cy)), rr, 1.0, -1, cv2.LINE_AA)
    f[:] = f * (1 - m[..., None]) + lay * m[..., None]
    cv2.circle(f, (int(cx), int(cy)), rr, C((40, 36, 40)), 22, cv2.LINE_AA)
    cv2.circle(f, (int(cx), int(cy)), rr + 11, C(INKC), 4, cv2.LINE_AA)


# ---------------- NEW PLACE: the 1982 hospital LAB at night ----------------
LAB_TOP = 1330


def set_lab(t=0.0, blur=4, top_y=LAB_TOP, dim=0.0):
    """THE LAB (1982, night): pale green tiled wall, a fluorescent tube that hums (a tiny flicker), a night window with a moon (left), shelves with
    brown + clear bottles and flasks (right), a wall calendar '1982', the bench top at top_y (draw lab_front AFTER the people). Paper-softened."""
    def mk():
        f = _vgrad((222, 236, 226), (196, 216, 204), 0, top_y)
        for yy in range(260, top_y, 64): cv2.line(f, (0, yy), (W, yy), C(TILE_S), 2, cv2.LINE_AA)
        for xx in range(0, W, 64): cv2.line(f, (xx, 260), (xx, top_y), C(TILE_S), 2, cv2.LINE_AA)
        cv2.rectangle(f, (0, 0), (W, 250), C((176, 190, 184)), -1)
        cv2.rectangle(f, (60, 360), (380, 820), C((40, 52, 84)), -1, cv2.LINE_AA)                                    # night window
        cv2.circle(f, (300, 470), 46, C((246, 240, 210)), -1, cv2.LINE_AA)
        for xx in (60, 220, 380): cv2.line(f, (xx, 360), (xx, 820), C((150, 160, 160)), 12, cv2.LINE_AA)
        for yy in (360, 590, 820): cv2.line(f, (60, yy), (380, yy), C((150, 160, 160)), 12, cv2.LINE_AA)
        for k, yy in enumerate((520, 760, 1000)):                                                                    # shelves of bottles
            cv2.rectangle(f, (640, yy), (1040, yy + 16), C((150, 120, 90)), -1)
            for j in range(6):
                bx = 670 + j * 62; hh = 90 + 30 * ((j + k) % 3); cc = (140, 84, 40) if (j + k) % 2 else (210, 226, 230)
                cv2.rectangle(f, (bx, yy - hh), (bx + 40, yy), C(cc), -1, cv2.LINE_AA)
                cv2.rectangle(f, (bx + 12, yy - hh - 16), (bx + 28, yy - hh), C((90, 90, 96)), -1)
                cv2.rectangle(f, (bx, yy - hh), (bx + 40, yy), C(INKC), 3, cv2.LINE_AA)
        cv2.rectangle(f, (440, 880), (590, 1060), C((250, 248, 240)), -1)                                             # calendar
        cv2.rectangle(f, (440, 880), (590, 920), C(ACC), -1)
        cv2.rectangle(f, (440, 880), (590, 1060), C(INKC), 3, cv2.LINE_AA)
        comp(f, ed_el("1982", "", lead_col=INKC, lead_size=46), 515, 990)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("lab60", blur, top_y), mk).copy()
    fl = 1.0 - 0.06 * (math.sin(t * 37) > 0.93)
    cv2.rectangle(f, (300, 268), (780, 292), C((250, 252, 246)), -1, cv2.LINE_AA)                                    # the tube
    glow(f, 540, 300, 420, (230, 255, 240), 0.22 * fl)
    haze(f, 260, 700, (230, 250, 240), 0.12)
    if dim > 0: f = f * (1 - 0.55 * dim)
    return inkify(f)


def lab_front(f, top_y=LAB_TOP):
    """the lab bench: a dark slate worktop with a steel lip, cupboard doors below (drawn AFTER the people)."""
    cv2.rectangle(f, (0, top_y), (W, top_y + 60), C((70, 78, 84)), -1)
    cv2.rectangle(f, (0, top_y + 60), (W, top_y + 72), C(STEEL), -1)
    cv2.line(f, (0, top_y), (W, top_y), C(INKC), 6, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y + 72), (W, H), C((176, 196, 186)), -1)
    for xx in range(0, W, 270):
        cv2.rectangle(f, (xx + 14, top_y + 92), (xx + 256, H - 20), C((150, 172, 160)), 4, cv2.LINE_AA)
        cv2.circle(f, (xx + 236, top_y + 220), 9, C(STEEL_S), -1, cv2.LINE_AA)
    _hatch_band(f, top_y + 76, H)
