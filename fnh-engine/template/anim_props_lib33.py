# ================= anim_props_lib33.py (ep 33, 11 Nov): WHICH FOODS HAVE MORE VITAMIN C THAN AN ORANGE? ONE accent: VITAMIN-C ORANGE (= vitamin C only:
# the bar, the mg numbers, the vitamin C buddies, the titles). The foods keep their natural colours (orange, lemon yellow, papaya, red capsicum, green guava,
# green chilli). Props: food_el(kind, mood, look, cut, medal, crown) = the six athletes as ink characters with faces; legs(f, ...) = their little ink legs;
# jump_xy(...) = a high-jump arc with anticipation + squash; crown_el, medal_ink_el, whistle_el, clip_el (clipboard), vitc_el(mood, look, k) (a vitamin C
# buddy; k = how faded / broken), scale_ink_el(text) (kitchen scale), bag_el(kind) (market bag), set_stadium(t, dim, wave) = NEW PLACE: an athletics stadium
# in daylight (stands with a crowd that can do a wave, floodlights, track + infield) softened toward paper; hj_rig(...) = the high-jump uprights with a
# mg scale, the bar and the landing mat; board_row(...) = a leaderboard row for the recap card.
ACC = (244, 146, 30); ACC_S = (190, 96, 14); ACC_L = (252, 206, 150); ACC_XL = (254, 234, 206)
ORA = (246, 150, 40); ORA_S = (206, 104, 20); ORA_L = (252, 196, 120)
LEM = (250, 218, 70); LEM_S = (214, 172, 30)
PAP = (246, 126, 70); PAP_S = (206, 84, 40); PAP_SKIN = (170, 196, 80)
CAP = (218, 52, 40); CAP_S = (160, 28, 24); CAP_H = (246, 120, 100)
GUA = (150, 196, 90); GUA_S = (104, 150, 56); GUA_IN = (244, 140, 150)
CHI = (70, 160, 64); CHI_S = (40, 112, 40)
LEAF = (96, 160, 70); LEAF_S = (60, 116, 44)
STEM = (120, 86, 52)
GOLD = (246, 196, 60); GOLD_S = (196, 140, 30); SILV = (214, 218, 224)
MAT = (70, 120, 200); MAT_S = (44, 82, 150)
TRACK = (200, 96, 74); TRACK_S = (170, 74, 56)
MILK = (252, 248, 238)
SRC_USDA = "Source: USDA FoodData Central (per 100 g, raw)"
SRC_NIH = "Source: NIH Office of Dietary Supplements"
PX_MG = 3.6                                                                 # high-jump scale: px per mg of vitamin C


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


def _leaf(d, x, y, ang, L=34, seed=0):
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = []
    for i in range(9):
        u = i / 8; w = 13 * math.sin(math.pi * u)
        pts.append((x + ca * L * u - sa * w, y + sa * L * u + ca * w))
    for i in range(8, -1, -1):
        u = i / 8; w = 13 * math.sin(math.pi * u)
        pts.append((x + ca * L * u + sa * w, y + sa * L * u - ca * w))
    _ink_poly(d, pts, LEAF, seed, INK_W - 1, amp=0.8)


def food_el(kind="orange", mood="n", look=(0, 0), cut=None, medal=False, crown=False, seed=None):
    """the six athletes: orange / lemon / papaya / capsicum / guava / chilli, each a flat ink fruit with ONE outline, a shadow side + hatching and a 3-stroke
    face. cut=True shows the inside (orange segments, papaya seeds, guava pink). medal = a gold medal on a ribbon, crown = a little gold crown on top.
    Every element is 300 x 340 with the body centred at (150, 200); feet go at y ~ 300 (legs are drawn by the shot)."""
    if cut is None: cut = kind == "papaya"                                  # a papaya always shows its cut face (whole, it reads as a guava)
    sd = seed or {"orange": 331, "lemon": 332, "papaya": 333, "capsicum": 334, "guava": 335, "chilli": 336}[kind]
    def mk():
        w, h = 300, 340; im, d, S = _cv(w, h)
        cx, cy = 150, 200
        if kind == "orange":
            P = _arcpts(cx, cy, 96, 92, 0, 360, 30)[:-1]
            _ink_poly(d, P, ORA, sd, INK_W, amp=1.2)
            _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(cx - 40, cy - 60, cx + 150, cy + 130), fill=c), ORA_S, 110)
            rng = np.random.default_rng(sd)
            for k in range(26):
                a = rng.uniform(0, 2 * math.pi); r = rng.uniform(0, 80); x, y = cx + r * math.cos(a), cy + r * math.sin(a) * 0.95
                d.ellipse(S(x - 2, y - 2, x + 2, y + 2), fill=ORA_S + (140,))
            if cut:
                d.ellipse(S(cx - 70, cy - 66, cx + 70, cy + 66), fill=(255, 238, 200, 255), outline=INKC + (255,), width=3 * SC3)
                for i in range(8):
                    a0 = i * 45 + 4; a1 = a0 + 37
                    pts = [(cx, cy)] + _arcpts(cx, cy, 60, 57, a0, a1, 6)
                    d.polygon(_P(pts), fill=ORA_L + (255,))
            d.line(_P([(cx, cy - 92), (cx + 4, cy - 112)]), fill=STEM + (255,), width=6 * SC3)
            _leaf(d, cx + 4, cy - 108, -20, 40, sd)
            fy = cy + 6
        elif kind == "lemon":
            P = []
            for i in range(32):
                a = 2 * math.pi * i / 32; r = 1.0 + 0.22 * abs(math.cos(a)) ** 6
                P.append((cx + 108 * r * math.cos(a), cy + 76 * math.sin(a)))
            _ink_poly(d, P, LEM, sd, INK_W, amp=1.2)
            _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(cx - 30, cy - 20, cx + 160, cy + 120), fill=c), LEM_S, 110)
            if cut:
                d.ellipse(S(cx - 60, cy - 50, cx + 60, cy + 50), fill=(255, 248, 200, 255), outline=INKC + (255,), width=3 * SC3)
                for i in range(8):
                    a = math.radians(i * 45); d.line(_P([(cx, cy), (cx + 52 * math.cos(a), cy + 44 * math.sin(a))]), fill=LEM_S + (255,), width=3 * SC3)
            _leaf(d, cx + 96, cy - 50, -50, 34, sd)
            fy = cy + 4
        elif kind == "papaya":
            P = []
            for i in range(34):
                a = 2 * math.pi * i / 34; c_, s_ = math.cos(a), math.sin(a)
                rx = 88 * (1 + 0.18 * s_); P.append((cx + rx * c_, cy + 10 + 118 * s_))
            _ink_poly(d, P, PAP_SKIN if not cut else PAP, sd, INK_W, amp=1.2)
            if cut:
                Q = [(cx + (x - cx) * 0.84, cy + 10 + (y - cy - 10) * 0.88) for x, y in P]
                d.polygon(_P(Q), fill=PAP + (255,))
                d.ellipse(S(cx - 36, cy - 20, cx + 36, cy + 90), fill=(250, 170, 110, 255))
                rng = np.random.default_rng(sd)
                for k in range(22):
                    x, y = cx + rng.uniform(-26, 26), cy + rng.uniform(-6, 80)
                    d.ellipse(S(x - 6, y - 6, x + 6, y + 6), fill=(40, 30, 26, 255))
                _ink_poly(d, P, None, sd, INK_W, amp=1.2)
            _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(cx - 20, cy - 60, cx + 170, cy + 200), fill=c), PAP_S if cut else LEAF_S, 90)
            d.line(_P([(cx, cy - 106), (cx + 2, cy - 124)]), fill=STEM + (255,), width=7 * SC3)
            fy = cy - 46 if cut else cy + 10
        elif kind == "capsicum":
            P = []
            for i in range(40):
                a = 2 * math.pi * i / 40; c_, s_ = math.cos(a), math.sin(a)
                lob = 1 + 0.05 * math.cos(4 * a + 0.4) + (0.10 * (s_ > 0.2) * abs(math.cos(3 * a)) - 0.05 * (s_ > 0.2))
                sh = 1.08 if s_ < 0 else 1.0 - 0.18 * s_                                  # broad shoulders on top, narrower lobed bottom
                P.append((cx + 100 * lob * c_ * sh, cy + 8 + 116 * lob * s_ * (1.0 if s_ > 0 else 0.84)))
            _ink_poly(d, P, CAP, sd, INK_W, amp=1.2)
            _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(cx - 10, cy - 70, cx + 170, cy + 160), fill=c), CAP_S, 120)
            for xx in (cx - 40, cx + 42):
                d.line(_P(_wob([(xx, cy - 70), (xx + (xx - cx) * 0.2, cy + 10), (xx + (xx - cx) * 0.1, cy + 96)], 1.0, sd)), fill=CAP_S + (200,), width=4 * SC3, joint="curve")
            d.ellipse(S(cx - 54, cy - 72, cx - 24, cy - 40), fill=CAP_H + (200,))
            _ink_poly(d, [(cx - 30, cy - 92), (cx + 30, cy - 92), (cx + 18, cy - 108), (cx - 18, cy - 108)], LEAF, sd + 1, INK_W - 1, amp=0.8)
            _ink_poly(d, [(cx - 6, cy - 106), (cx + 6, cy - 106), (cx + 12, cy - 136), (cx + 2, cy - 138)], LEAF_S, sd + 2, INK_W - 1, amp=0.6)
            fy = cy + 8
        elif kind == "guava":
            P = []
            for i in range(34):
                a = 2 * math.pi * i / 34; c_, s_ = math.cos(a), math.sin(a)
                r = 1 + 0.1 * s_; P.append((cx + 94 * r * c_, cy + 14 + 98 * s_ * (1.0 if s_ > 0 else 1.06)))
            _ink_poly(d, P, GUA, sd, INK_W, amp=1.2)
            _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(cx - 10, cy - 60, cx + 170, cy + 170), fill=c), GUA_S, 120)
            rng = np.random.default_rng(sd)
            for k in range(18):
                x, y = cx + rng.uniform(-70, 70), cy + 14 + rng.uniform(-70, 70)
                if (x - cx) ** 2 / 80 ** 2 + (y - cy - 14) ** 2 / 84 ** 2 < 1: d.ellipse(S(x - 2, y - 2, x + 2, y + 2), fill=GUA_S + (150,))
            if cut:                                                         # a wedge cut out of the lower right shows the pink inside
                W_ = [(cx + 20, cy + 30), (cx + 92, cy + 20), (cx + 70, cy + 92)]
                d.polygon(_P(W_), fill=GUA_IN + (255,)); d.line(_P(W_ + [W_[0]]), fill=INKC + (255,), width=3 * SC3)
                for k in range(5):
                    x, y = cx + 50 + rng.uniform(-14, 14), cy + 50 + rng.uniform(-10, 14); d.ellipse(S(x - 3, y - 3, x + 3, y + 3), fill=(250, 230, 200, 255))
            for i in range(5):                                              # the little crown at the blossom end (bottom)
                a = math.radians(-90 + 180 + (i - 2) * 22)
                d.line(_P([(cx, cy + 108), (cx + 14 * math.cos(a + math.pi), cy + 108 + 12 * math.sin(a + math.pi) * -1)]), fill=INKC + (255,), width=3 * SC3)
            d.line(_P([(cx - 4, cy - 82), (cx - 8, cy - 104)]), fill=STEM + (255,), width=6 * SC3)
            _leaf(d, cx - 8, cy - 100, -150, 36, sd)
            fy = cy + 8
        else:                                                               # green chilli: a long curved pod standing up
            P = []
            N = 22
            spine = [(cx + 28 * math.sin(math.pi * u * 0.9) - 10, cy - 100 + 230 * u) for u in np.linspace(0, 1, N)]
            for i, (x, y) in enumerate(spine):
                u = i / (N - 1); wd = 36 * (1 - u ** 2.2) + 4; P.append((x - wd, y))
            for i in range(N - 1, -1, -1):
                x, y = spine[i]; u = i / (N - 1); wd = 36 * (1 - u ** 2.2) + 4; P.append((x + wd, y))
            _ink_poly(d, P, CHI, sd, INK_W, amp=1.0)
            _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.rectangle(S_(cx + 4, cy - 120, cx + 120, cy + 160), fill=c), CHI_S, 120)
            d.line(_P(_wob([(cx - 26, cy - 80), (cx - 14, cy + 20)], 0.6, sd)), fill=(170, 230, 150, 200), width=5 * SC3)
            _ink_poly(d, [(cx - 44, cy - 100), (cx + 24, cy - 100), (cx + 10, cy - 116), (cx - 30, cy - 116)], LEAF_S, sd + 1, INK_W - 1, amp=0.6)
            d.line(_P([(cx - 10, cy - 114), (cx - 30, cy - 150)]), fill=LEAF_S + (255,), width=8 * SC3)
            fy = cy - 34
        _hatch_in(im, (cx - 110, cy - 110, cx + 110, cy + 130), lambda q, S_: q.ellipse(S_(cx + 20, cy - 40, cx + 140, cy + 140), fill=255))
        if mood: _face(d, S, cx - (6 if kind == "chilli" else 0), fy, 1.5 if kind != "chilli" else 1.2, mood, look)
        if medal:
            d.line(_P([(cx - 40, cy - 70), (cx, cy + 40), (cx + 40, cy - 70)]), fill=(60, 110, 200, 255), width=8 * SC3)
            _ink_ell(d, cx, cy + 60, 30, 30, GOLD, sd + 5, INK_W - 1)
            d.ellipse(S(cx - 16, cy + 44, cx + 16, cy + 76), outline=GOLD_S + (255,), width=3 * SC3)
        if crown:
            top = cy - (100 if kind != "chilli" else 160)
            C_ = [(cx - 50, top), (cx - 56, top - 52), (cx - 26, top - 24), (cx, top - 62), (cx + 26, top - 24), (cx + 56, top - 52), (cx + 50, top)]
            _ink_poly(d, C_, GOLD, sd + 7, INK_W - 1, amp=0.7)
            for x in (cx - 56, cx, cx + 56): d.ellipse(S(x - 7, top - 60 - 6 + (8 if x != cx else 0), x + 7, top - 60 + 8 + (8 if x != cx else 0)), fill=(226, 70, 80, 255))
        return _done(im, w, h)
    return gcache(("food33", kind, mood, tuple(look), cut, medal, crown, sd), mk)


def legs(f, x, y, s, phase=0.0, tuck=0.0, run=0.0):
    """little ink legs + round shoes under a food athlete. (x, y) = where the body's bottom meets the legs; tuck 0..1 folds them (mid-jump);
    run = stride amount (0 = standing)."""
    L = 70 * s
    for sg in (-1, 1):
        sw = run * math.sin(phase * 2 * math.pi + (0 if sg > 0 else math.pi))
        hx = x + sg * 26 * s
        kx = hx + (sw * 30 - tuck * sg * 6) * s; ky = y + L * (0.5 - 0.25 * tuck)
        fx = hx + (sw * 46 + tuck * 30) * s; fy = y + L * (1 - 0.55 * tuck) - max(0, sw) * 12 * s
        cv2.polylines(f, [np.array([(hx, y), (kx, ky), (fx, fy)], np.int32)], False, C(INKC), max(2, int(7 * s)), cv2.LINE_AA)
        cv2.ellipse(f, (int(fx + 10 * s), int(fy)), (int(18 * s), int(11 * s)), 0, 0, 360, C(MILK), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(fx + 10 * s), int(fy)), (int(18 * s), int(11 * s)), 0, 0, 360, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)


def athlete(f, kind, x, y, s, t, mood="n", look=(0, 0), run=0.0, tuck=0.0, rot=0.0, sq=1.0, op=1.0, **k):
    """a food athlete standing with its feet at (x, y): legs + body (+ bob when running)."""
    el = food_el(kind, mood, look, **k)
    hip = y - 70 * s
    if tuck < 0.99: legs(f, x, hip, s, t * 2.2, tuck, run)
    body_y = hip - 128 * s * sq
    rot_comp(f, scale_el(el, s), x, body_y + 10 * math.sin(t * 13) * run * s, rot, 1.0, op, 0.0)


def jump_xy(t, t0, x0, x1, ground, peak, dur=1.1, anti=0.18):
    """a high-jump: anticipation crouch (anti s), then an arc from x0 to x1 that peaks at y = peak, then the landing squash.
    returns dict(x, y, sq, tuck, rot, phase) with phase 'wait' | 'anti' | 'air' | 'land'."""
    u = t - t0
    if u < 0: return dict(x=x0, y=ground, sq=1.0, tuck=0.0, rot=0.0, phase="wait")
    if u < anti: k = u / anti; return dict(x=x0, y=ground, sq=1 - 0.22 * math.sin(math.pi * k * 0.5), tuck=0.0, rot=-6 * k, phase="anti")
    q = (u - anti) / dur
    if q < 1:
        x = x0 + (x1 - x0) * q
        y = ground - (ground - peak) * 4 * q * (1 - q)
        return dict(x=x, y=y, sq=1.12 - 0.12 * math.sin(math.pi * q), tuck=math.sin(math.pi * q), rot=-20 + 40 * q, phase="air")
    v = u - anti - dur
    return dict(x=x1, y=ground, sq=1 - 0.25 * math.exp(-v * 9) * math.cos(v * 20), tuck=0.0, rot=0.0, phase="land")


def crown_el():
    def mk():
        w, h = 160, 110; im, d, S = _cv(w, h)
        C_ = [(20, 96), (12, 26), (48, 60), (80, 14), (112, 60), (148, 26), (140, 96)]
        _ink_poly(d, C_, GOLD, 371, INK_W, amp=0.7)
        _shade(im, lambda q, S_: q.polygon(_P(C_), fill=255), lambda q, S_, c: q.rectangle(S_(90, 0, 160, 110), fill=c), GOLD_S, 110)
        for x, y in ((12, 22), (80, 10), (148, 22)): d.ellipse(S(x - 9, y - 9, x + 9, y + 9), fill=(226, 70, 80, 255), outline=INKC + (255,), width=2 * SC3)
        return _done(im, w, h)
    return gcache(("crown33",), mk)


def whistle_el():
    def mk():
        w, h = 120, 80; im, d, S = _cv(w, h)
        _ink_poly(d, [(10, 30), (60, 30), (60, 18), (84, 18), (84, 34)] + _arcpts(80, 50, 30, 26, -60, 200, 10)[1:] + [(10, 52)], SILV, 372, INK_W - 1, amp=0.6)
        d.ellipse(S(70, 40, 88, 58), fill=INKC + (255,))
        return _done(im, w, h)
    return gcache(("whistle33",), mk)


def vitc_el(mood="happy", look=(0, 0), k=0.0, seed=373):
    """a VITAMIN C buddy: a small accent-orange ball with a 'C' on its belly. k 0..1 = fading/breaking (heat: cracks + paler; 1 = almost gone)."""
    kk = round(clamp(k) * 4) / 4
    def mk():
        w, h = 140, 140; im, d, S = _cv(w, h)
        col = tuple(int(c * (1 - 0.6 * kk) + 252 * 0.6 * kk) for c in ACC)
        _ink_ell(d, 70, 74, 52, 50, col, seed, INK_W - 1, col=tuple(int(c * (1 - 0.5 * kk) + 220 * 0.5 * kk) for c in INKC))
        _shade(im, lambda q, S_: q.ellipse(S_(18, 24, 122, 124), fill=255), lambda q, S_, c: q.ellipse(S_(50, 40, 150, 150), fill=c), ACC_S, int(110 * (1 - kk)))
        fn = font(F_HAND, 40 * SC3)
        d.text((70 * SC3, 106 * SC3), "C", font=fn, fill=(255, 250, 236, int(255 * (1 - 0.5 * kk))), anchor="mm")
        if kk > 0:
            for j in range(int(1 + 3 * kk)):
                x0 = 40 + 20 * j; d.line(_P([(x0, 28), (x0 + 8, 46), (x0 - 4, 58), (x0 + 6, 72)]), fill=INKC + (200,), width=3 * SC3)
        _face(d, S, 70, 56, 0.9, mood, look)
        return _done(im, w, h)
    return gcache(("vitc33", mood, tuple(look), kk, seed), mk)


def scale_ink_el(text="100 g"):
    def mk():
        w, h = 360, 230; im, d, S = _cv(w, h)
        _ink_poly(d, [(40, 90), (320, 90), (340, 210), (20, 210)], (236, 238, 240), 374, INK_W)
        _ink_poly(d, [(20, 60), (340, 60), (330, 92), (30, 92)], (206, 210, 216), 375, INK_W - 1)
        d.rounded_rectangle(S(100, 120, 260, 186), 10 * SC3, fill=(40, 60, 52, 255), outline=INKC + (255,), width=3 * SC3)
        d.text((180 * SC3, 154 * SC3), text, font=font(F_HAND, 44 * SC3), fill=(150, 250, 180, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("scale33", text), mk)


def clip_el():
    def mk():
        w, h = 180, 230; im, d, S = _cv(w, h)
        _ink_poly(d, [(14, 20), (166, 20), (166, 222), (14, 222)], (170, 120, 76), 376, INK_W)
        _ink_poly(d, [(28, 40), (152, 40), (152, 208), (28, 208)], MILK, 377, INK_W - 2)
        _ink_poly(d, [(60, 8), (120, 8), (120, 34), (60, 34)], SILV, 378, INK_W - 2)
        for j in range(5): d.line(_P(_wob([(42, 70 + 26 * j), (138 - 14 * (j % 2), 70 + 26 * j)], 0.8, j)), fill=BP_INK + (200,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("clip33",), mk)


def bag_el(kind="guava"):
    """a cloth market bag with three foods poking out (kind = 'guava' mixed veg | 'orange' a bag of oranges)."""
    def mk():
        w, h = 360, 420; im, d, S = _cv(w, h)
        items = [("orange", 110, 120), ("orange", 190, 100), ("orange", 260, 128)] if kind == "orange" else [("guava", 110, 116), ("capsicum", 200, 96), ("papaya", 270, 124)]
        for kd, x, y in items:
            pi = el_pil(food_el(kd, None), 0.55 * SC3)
            im.alpha_composite(pi, (int(x * SC3 - pi.size[0] / 2), int(y * SC3 - pi.size[1] / 2)))
        B_ = [(40, 170), (320, 170), (300, 400), (60, 400)]
        _ink_poly(d, B_, (226, 214, 186), 379, INK_W)
        _shade(im, lambda q, S_: q.polygon(_P(B_), fill=255), lambda q, S_, c: q.rectangle(S_(220, 160, 360, 420), fill=c), (180, 164, 130), 120)
        d.line(_P(_wob([(90, 172), (120, 60), (180, 40), (240, 60), (270, 172)], 1.2, 9)), fill=INKC + (255,), width=6 * SC3, joint="curve")
        return _done(im, w, h)
    return gcache(("bag33", kind), mk)


def el_pil(el, s=1.0):
    """an (premultiplied rgb, alpha) element -> a PIL RGBA image scaled by s (to stack elements inside PIL canvases)."""
    pm, a = scale_el(el, s); rgb = pm / np.maximum(a[..., None], 1e-4)
    return Image.fromarray((np.dstack([np.clip(rgb, 0, 1), a]) * 255).astype(np.uint8), "RGBA")


# ---------------- NEW PLACE: the STADIUM (athletics, daylight) ----------------
def set_stadium(t=0.0, dim=0.0, wave=None, blur=4):
    """an athletics stadium on a bright day: sky, two tiers of stands with a dotted crowd (wave = t0 of a Mexican wave travelling left->right),
    floodlight towers, plain boards, green infield and the red track in perspective (feet of the athletes at y ~ 1440). Paper-softened.
    dim 0..1 = the lights go down (the mystery-contender beat)."""
    def mk():
        f = _vgrad((150, 200, 238), (226, 238, 246), 0, 560)
        f[560:1060] = _vgrad((96, 104, 130), (130, 136, 158), 560, 1060)[560:1060]
        for i, y in enumerate(range(600, 1060, 46)):                       # stand tiers
            cv2.line(f, (0, y), (W, y), C((80, 86, 110)), 4, cv2.LINE_AA)
        f[1060:1140] = _vgrad((240, 236, 226), (226, 220, 206), 1060, 1140)[1060:1140]
        for x in range(0, W, 270): cv2.line(f, (x, 1060), (x, 1140), C((200, 190, 170)), 4)
        f[1140:1330] = _vgrad((126, 186, 100), (106, 168, 84), 1140, 1330)[1140:1330]
        for x in range(-200, W + 200, 160):                                 # mowing stripes
            cv2.fillPoly(f, [np.array([(x, 1140), (x + 80, 1140), (x + 110, 1330), (x + 30, 1330)], np.int32)], C((118, 178, 92)), cv2.LINE_AA)
        f[1330:] = _vgrad(TRACK, TRACK_S, 1330, H)[1330:]
        for j, y in enumerate((1330, 1420, 1540, 1690, 1880)): cv2.line(f, (0, y), (W, y), C((250, 246, 236)), 5 + 2 * j, cv2.LINE_AA)
        for x in (90, 990):                                                 # floodlight towers
            cv2.line(f, (x, 560), (x, 120), C((90, 96, 116)), 14, cv2.LINE_AA)
            cv2.rectangle(f, (x - 70, 80), (x + 70, 160), C((90, 96, 116)), -1, cv2.LINE_AA)
            for i in range(3):
                for j in range(2): cv2.circle(f, (x - 46 + 46 * i, 104 + 32 * j), 13, C((255, 250, 220)), -1, cv2.LINE_AA)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("set_stadium33",), mk).copy()
    rng = np.random.default_rng(33)                                         # the crowd: dots, a Mexican wave lifts them
    cols = [(236, 92, 80), (250, 210, 90), (120, 180, 230), (250, 250, 240), (160, 220, 140), (244, 160, 60)]
    for i in range(420):
        x = rng.uniform(10, W - 10); row = rng.integers(0, 10); y = 620 + row * 46 - 14
        lift = 0.0
        if wave is not None:
            ph = (t - wave) * 900 - x
            if 0 < ph < 260: lift = math.sin(math.pi * ph / 260)
        cv2.circle(f, (int(x), int(y - 16 * lift)), 9, C(cols[i % 6]), -1, cv2.LINE_AA)
        if lift > 0.3: cv2.line(f, (int(x), int(y - 16 * lift)), (int(x), int(y - 16 * lift - 22)), C(cols[i % 6]), 4, cv2.LINE_AA)
    f[560:1060] = cv2.GaussianBlur(f[560:1060], (0, 0), blur)
    f[:560] = cv2.GaussianBlur(f[:560], (0, 0), blur * 0.6)
    for x in (90, 990): glow(f, x, 120, 180, (255, 248, 220), 0.18 * (1 - dim))
    if dim > 0:
        f[:] = f * (1 - 0.68 * dim) + np.array(C((20, 22, 40)), np.float32) * 0.0
    return inkify(f)


def hj_rig(f, x0=170, x1=910, ground=1440, bar=None, t=0.0, labels=True, top=None, mat=True, bar_col=None, wob=0.0, px=None):
    """the high-jump rig: two uprights with a vitamin C scale (tick every 50 mg, labels in mg), the bar at `bar` mg (None = no bar),
    a blue landing mat behind. wob = the bar wobbles after a touch."""
    px = px or PX_MG
    top = top or max(380, ground - 260 * px)
    stp = 10 if px > 5 else 25; lab = 20 if px > 5 else 50
    if mat:
        cv2.rectangle(f, (x0 + 120, ground - 110), (x1 - 120, ground - 20), C(MAT), -1, cv2.LINE_AA)
        cv2.rectangle(f, (x0 + 120, ground - 110), (x1 - 120, ground - 20), C(INKC), 5, cv2.LINE_AA)
        cv2.line(f, (x0 + 120, ground - 80), (x1 - 120, ground - 80), C(MAT_S), 4, cv2.LINE_AA)
    for x in (x0, x1):
        cv2.rectangle(f, (x - 12, int(top)), (x + 12, ground), C((246, 244, 238)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (x - 12, int(top)), (x + 12, ground), C(INKC), 4, cv2.LINE_AA)
        cv2.rectangle(f, (x - 40, ground - 14), (x + 40, ground + 8), C((120, 124, 140)), -1, cv2.LINE_AA)
        for mg in range(0, 251, stp):
            y = int(ground - mg * px)
            if y < top: break
            L = 22 if mg % lab == 0 else 12
            cv2.line(f, (x - 12 - L if x == x0 else x + 12, y), (x - 12 if x == x0 else x + 12 + L, y), C(INKC), 3, cv2.LINE_AA)
    if labels:
        for mg in range(lab, 251, lab):
            y = ground - mg * px
            if y < top + 10: break
            write_on(f, str(mg), x0 - 76, y + 14, 99, 0, 34, INKC, 99)
        write_on(f, "mg", x0 - 76, ground - 20, 99, 0, 30, INKC, 99)
    if bar is not None:
        y = ground - bar * px + wob
        cv2.line(f, (x0 - 6, int(y)), (x1 + 6, int(y - wob * 0.4)), C(INKC), 18, cv2.LINE_AA)
        cv2.line(f, (x0 - 4, int(y)), (x1 + 4, int(y - wob * 0.4)), C(bar_col or ACC), 11, cv2.LINE_AA)
        return y
    return None


def board_row(f, y, kind, name, mg, t, t0, maxw=520, x_ic=150, x_name=250, x_bar=470, hl=False):
    """one leaderboard row: food icon, hand-lettered name, an accent bar that grows to mg (scale 242 -> maxw), the number counting up."""
    if t < t0: return
    k = eo(clamp((t - t0) / 0.5))
    el_at_(f, food_el(kind, "happy" if hl else "n"), x_ic, y - 6, 0.5, t, t0)
    write_on(f, name, x_name, y + 18, t, t0, 46, INKC, 40)
    L = int(maxw * mg / 242 * k)
    if L > 4:
        poly = [(x_bar, y - 36), (x_bar + L, y - 36), (x_bar + L, y + 36), (x_bar, y + 36)]
        cv2.fillPoly(f, [np.array(poly, np.int32)], C(ACC_L if not hl else ACC), cv2.LINE_AA)
        hatch_on(f, poly, 1.0, ACC_S, 14, 45, 3, 0.6)
        cv2.polylines(f, [np.array(poly, np.int32)], True, C(INKC), 4, cv2.LINE_AA)
    v = int(round(mg * k))
    write_on(f, str(v), min(x_bar + L + 70, 990), y + 20, 99, 0, 54, ACC_S if hl else INKC, 99)


def el_at_(f, el, x, y, s, t, t0):
    k = snap(t, t0, 4) if t >= t0 else 0.0
    if k > 0.01: rot_comp(f, scale_el(el, s), x, y, 0.0, k, 1.0, 0.0)
