# ================= anim_props_lib34.py (ep 34, 12 Nov): "Why does spicy food make your nose run?" — CHILLI-RED accent, ink props, NEW PLACE the CHAAT
# STALL at dusk, Chubby's RUNNY NOSE kit (a mucus drip with anticipation + follow-through, flushed cheeks), the LOOP SEAM helper. =================
ACC = (214, 58, 44); ACC_S = (158, 32, 26); ACC_L = (246, 168, 148); ACC_XL = (252, 224, 214)       # chilli red = heat / capsaicin / alarm only
MUC = (196, 230, 180); MUC_S = (96, 150, 110); MUC_H = (250, 255, 252)                                # mucus: pale, clear, a little green
PURI = (232, 176, 92); PURI_S = (190, 128, 52); PURI_D = (150, 92, 36)
PANI = (120, 176, 96); PANI_S = (76, 130, 60)
TISS = (252, 252, 248); TISS_S = (214, 214, 206)
STEELC = (196, 204, 212); STEEL_S = (140, 150, 162)
BRASS = (226, 182, 82); BRASS_S = (176, 130, 40)
MILK = (252, 248, 238)
SRC_CC = "Source: Cleveland Clinic; UCLA Health"
SC3 = 3


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


def golgappa_el(bite=False, pani=True, mood=None, look=(0, 0), seed=341):
    """a pani puri: a round golden puri (puffed ball), a hole broken in the top with green pani + chickpeas; bite = a bite out of the side."""
    def mk():
        w, h = 220, 220; im, d, S = _cv(w, h); cx, cy = 110, 120
        P = _arcpts(cx, cy, 90, 82, 0, 360, 28)[:-1]
        if bite:
            P = [p for p in P if not (p[0] > cx + 40 and p[1] > cy - 10)] ; P.insert(len(P) // 2, (cx + 40, cy + 20))
        _ink_poly(d, P, PURI, seed, INK_W, amp=1.4)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(cx - 20, cy - 30, cx + 140, cy + 130), fill=c), PURI_S, 120)
        rng = np.random.default_rng(seed)
        for k in range(14):
            x, y = cx + rng.uniform(-70, 70), cy + rng.uniform(-60, 64)
            if (x - cx) ** 2 / 80 ** 2 + (y - cy) ** 2 / 72 ** 2 < 1: d.ellipse(S(x - 4, y - 3, x + 4, y + 3), fill=PURI_D + (120,))
        H_ = _arcpts(cx - 4, cy - 46, 44, 22, 0, 360, 18)[:-1]                          # the broken hole on top
        _ink_poly(d, H_, PANI if pani else PURI_D, seed + 1, INK_W - 1, amp=1.6)
        if pani:
            for (x, y) in ((cx - 22, cy - 50), (cx + 6, cy - 44), (cx + 20, cy - 54)): _ink_ell(d, x, y, 9, 8, (226, 196, 130), seed + 3, 2)
        _hatch_in(im, (cx - 90, cy - 80, cx + 90, cy + 90), lambda q, S_: q.ellipse(S_(cx + 10, cy - 20, cx + 120, cy + 110), fill=255))
        if mood: _face(d, S, cx, cy + 18, 1.2, mood, look)
        return _done(im, w, h)
    return gcache(("golg34", bite, pani, mood, tuple(look), seed), mk)


def puri_stack_el(seed=342):
    """a steel plate with a pyramid of puris (the stall's stock)."""
    def mk():
        w, h = 360, 220; im, d, S = _cv(w, h)
        _ink_ell(d, 180, 180, 170, 28, STEELC, seed, INK_W - 1)
        for i, (x, y) in enumerate(((90, 150), (150, 154), (210, 154), (270, 150), (120, 108), (180, 104), (240, 108), (150, 62), (210, 62))):
            _ink_ell(d, x, y, 38, 34, PURI, seed + i, INK_W - 1, amp=1.2)
            d.ellipse(S(x + 4, y - 4, x + 34, y + 30), fill=PURI_S + (90,))
        return _done(im, w, h)
    return gcache(("puris34", seed), mk)


def matka_el(seed=343):
    """a clay pot of pani (matka) with a ladle."""
    def mk():
        w, h = 220, 240; im, d, S = _cv(w, h)
        P = _arcpts(110, 150, 90, 78, 0, 360, 26)[:-1]
        _ink_poly(d, P, (196, 108, 64), seed, INK_W)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(130, 80, 260, 260), fill=c), (150, 70, 40), 120)
        _ink_poly(d, [(60, 80), (160, 80), (150, 64), (70, 64)], (214, 124, 76), seed + 1, INK_W - 1)
        _ink_ell(d, 110, 74, 52, 12, PANI, seed + 2, INK_W - 2)
        d.line(_P([(150, 70), (196, 10)]), fill=STEEL_S + (255,), width=7 * SC3)
        d.line(_P([(40, 150), (180, 150)]), fill=(240, 220, 190, 200), width=4 * SC3)
        return _done(im, w, h)
    return gcache(("matka34", seed), mk)


def tissue_box_el(seed=344):
    """a tissue box (mint, the channel colour) with a tissue standing out of the slot."""
    def mk():
        w, h = 260, 260; im, d, S = _cv(w, h)
        B_ = [(30, 120), (230, 120), (230, 240), (30, 240)]
        _ink_poly(d, B_, INK_MINT, seed, INK_W, amp=0.8)
        _ink_poly(d, [(30, 120), (230, 120), (210, 96), (50, 96)], _mix(INK_MINT, (255, 255, 255), 0.35), seed + 1, INK_W - 1, amp=0.6)
        _shade(im, lambda q, S_: q.polygon(_P(B_), fill=255), lambda q, S_, c: q.rectangle(S_(160, 110, 240, 250), fill=c), INK_MINT_S, 110)
        _ink_ell(d, 130, 108, 50, 8, (60, 90, 80), seed + 2, 2)
        T_ = [(100, 108), (84, 50), (112, 20), (150, 30), (176, 60), (160, 108)]
        _ink_poly(d, T_, TISS, seed + 3, INK_W - 1, amp=2.0)
        d.line(_P([(120, 40), (130, 96)]), fill=TISS_S + (255,), width=2 * SC3)
        return _done(im, w, h)
    return gcache(("tbox34", seed), mk)


def tissue_el(seed=345, crumpled=False):
    def mk():
        w, h = 160, 160; im, d, S = _cv(w, h)
        if crumpled:
            P = [(40 + 40 * math.cos(a) * (0.8 + 0.25 * math.sin(5 * a)), 80 + 40 * math.sin(a) * (0.8 + 0.25 * math.cos(4 * a))) for a in np.linspace(0, 2 * math.pi, 22)[:-1]]
            P = [(x + 40, y) for x, y in P]
        else:
            P = [(20, 30), (140, 22), (146, 130), (24, 140)]
        _ink_poly(d, P, TISS, seed, INK_W - 1, amp=2.4)
        for k in range(3): d.line(_P(_wob([(50 + 20 * k, 40), (60 + 20 * k, 120)], 2, seed + k)), fill=TISS_S + (255,), width=2 * SC3)
        return _done(im, w, h)
    return gcache(("tiss34", seed, crumpled), mk)


def caps_el(mood="happy", look=(0, 0), k=1.0, seed=346):
    """CAPSAICIN as a buddy: a little red flame with a 3-stroke face (the hot molecule from the chilli). k = flame height (it flares)."""
    k = round(clamp(k, 0.6, 1.4) * 5) / 5
    def mk():
        w, h = 200, 260; im, d, S = _cv(w, h); cx, by = 100, 230
        def flame(sc_, col, sd):
            P = []
            for a in np.linspace(0, 1, 15):                                               # left side up to the tip, then down the right
                P.append((cx - 70 * sc_ * math.sin(math.pi * (1 - a) ** 0.8) - 6 * math.sin(a * 9), by - 200 * sc_ * k * a))
            P = P + [(cx + 70 * sc_ * math.sin(math.pi * (1 - a) ** 0.8) + 8 * math.sin(a * 7), by - 200 * sc_ * k * a) for a in np.linspace(1, 0, 15)]
            P = [(x + (24 * sc_ * (1 - (by - y) / (200 * sc_ * k + 1e-3))) * 0, y) for x, y in P]
            _ink_poly(d, P, col, sd, INK_W if sc_ > 0.8 else 0, amp=1.0)
        flame(1.0, ACC, seed); flame(0.62, (250, 150, 80), seed + 1); flame(0.3, (255, 226, 140), seed + 2)
        if mood: _face(d, S, cx, by - 70, 1.25, mood, look)
        return _done(im, w, h)
    return gcache(("caps34", mood, tuple(look), k, seed), mk)


def bell_el(ring=0.0, lit=False, seed=347):
    """a round fire-alarm bell on a wall plate; lit = it glows (alarm on)."""
    def mk():
        w, h = 240, 240; im, d, S = _cv(w, h)
        _ink_poly(d, [(40, 40), (200, 40), (200, 200), (40, 200)], (230, 222, 206), seed, INK_W - 1, amp=0.6)
        _ink_ell(d, 120, 120, 78, 78, ACC if lit else _mix(ACC, (120, 110, 104), 0.55), seed + 1, INK_W)
        _shade(im, lambda q, S_: q.ellipse(S_(42, 42, 198, 198), fill=255), lambda q, S_, c: q.ellipse(S_(110, 100, 230, 230), fill=c), ACC_S, 120)
        d.ellipse(S(80, 70, 110, 96), fill=(255, 255, 255, 150))
        _ink_ell(d, 120, 120, 16, 16, (90, 84, 80), seed + 2, 2)
        return _done(im, w, h)
    return gcache(("bell34", lit, seed), mk)


def tap_el(open_k=0.0, seed=348):
    """a brass tap (faucet) seen from the side; open_k turns the handle."""
    ok = round(clamp(open_k) * 4) / 4
    def mk():
        w, h = 300, 240; im, d, S = _cv(w, h)
        _ink_poly(d, [(20, 70), (60, 70), (60, 130), (20, 130)], BRASS_S, seed, INK_W - 1)              # wall flange
        _ink_poly(d, [(60, 84), (200, 84), (226, 104), (236, 150), (206, 150), (198, 116), (60, 116)], BRASS, seed + 1, INK_W)
        _shade(im, lambda q, S_: q.polygon(_P([(60, 84), (200, 84), (226, 104), (236, 150), (206, 150), (198, 116), (60, 116)]), fill=255),
               lambda q, S_, c: q.rectangle(S_(60, 104, 240, 160), fill=c), BRASS_S, 110)
        a = math.radians(-90 + 80 * ok)                                                  # the handle turns
        hx, hy = 130, 84
        d.line(_P([(hx, hy), (hx + 60 * math.cos(a), hy + 60 * math.sin(a))]), fill=INKC + (255,), width=14 * SC3)
        d.line(_P([(hx, hy), (hx + 60 * math.cos(a), hy + 60 * math.sin(a))]), fill=ACC + (255,), width=8 * SC3)
        _ink_ell(d, hx + 64 * math.cos(a), hy + 64 * math.sin(a), 14, 14, ACC, seed + 2, INK_W - 1)
        return _done(im, w, h)
    return gcache(("tap34", ok, seed), mk)


def helmet_el(seed=349):
    """a red firefighter's helmet (ink) to put on Chubby's head."""
    def mk():
        w, h = 300, 200; im, d, S = _cv(w, h)
        _ink_poly(d, [(30, 150), (270, 150), (290, 170), (10, 170)], ACC_S, seed, INK_W)
        P = _arcpts(150, 150, 110, 120, 180, 360, 20)
        _ink_poly(d, P, ACC, seed + 1, INK_W)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.rectangle(S_(160, 20, 280, 160), fill=c), ACC_S, 110)
        _ink_poly(d, [(122, 50), (178, 50), (172, 110), (128, 110)], BRASS, seed + 2, INK_W - 1)
        d.line(_P([(150, 32), (150, 150)]), fill=INKC + (255,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("helm34", seed), mk)


def ext_el(seed=350):
    """a red fire extinguisher with a black hose."""
    def mk():
        w, h = 200, 320; im, d, S = _cv(w, h)
        B_ = [(60, 90), (140, 90), (150, 120), (150, 300), (50, 300), (50, 120)]
        _ink_poly(d, B_, ACC, seed, INK_W)
        _shade(im, lambda q, S_: q.polygon(_P(B_), fill=255), lambda q, S_, c: q.rectangle(S_(110, 80, 160, 310), fill=c), ACC_S, 120)
        _ink_poly(d, [(64, 170), (136, 170), (136, 230), (64, 230)], MILK, seed + 1, 3)
        _ink_poly(d, [(80, 60), (120, 60), (120, 92), (80, 92)], (70, 66, 64), seed + 2, INK_W - 1)
        d.line(_P(_wob([(110, 64), (160, 40), (180, 80), (176, 150)], 1.2, seed)), fill=(50, 46, 44, 255), width=9 * SC3, joint="curve")
        return _done(im, w, h)
    return gcache(("ext34", seed), mk)


def flower_ink_el(seed=351):
    """a pollen flower (the allergy icon): yellow centre, pollen dots."""
    def mk():
        w, h = 220, 260; im, d, S = _cv(w, h)
        d.line(_P(_wob([(110, 130), (104, 250)], 1.2, seed)), fill=LEAF_S + (255,), width=8 * SC3)
        for i in range(6):
            a = 2 * math.pi * i / 6; _ink_ell(d, 110 + 46 * math.cos(a), 100 + 46 * math.sin(a), 34, 26, (246, 170, 196), seed + i, INK_W - 1)
        _ink_ell(d, 110, 100, 30, 30, (250, 210, 70), seed + 9, INK_W - 1)
        rng = np.random.default_rng(seed)
        for k in range(12): x, y = 110 + rng.uniform(-100, 100), 60 + rng.uniform(-50, 40); d.ellipse(S(x - 4, y - 4, x + 4, y + 4), fill=(250, 210, 70, 230))
        return _done(im, w, h)
    return gcache(("flower34", seed), mk)


def bowl_soup_el(seed=352):
    """a bowl of hot tomato soup (ink): red-orange, a spoon, a cream swirl."""
    def mk():
        w, h = 320, 220; im, d, S = _cv(w, h)
        B_ = _arcpts(160, 90, 140, 120, 0, 180, 18)
        _ink_poly(d, B_, MILK, seed, INK_W)
        _shade(im, lambda q, S_: q.polygon(_P(B_), fill=255), lambda q, S_, c: q.rectangle(S_(170, 80, 310, 220), fill=c), TISS_S, 120)
        _ink_ell(d, 160, 92, 140, 30, (222, 96, 54), seed + 1, INK_W - 1)
        d.arc(S(120, 82, 200, 102), 200, 340, fill=(250, 230, 210, 255), width=4 * SC3)
        d.line(_P([(210, 90), (290, 20)]), fill=STEEL_S + (255,), width=10 * SC3)
        return _done(im, w, h)
    return gcache(("soup34", seed), mk)


# ---------------- live: Chubby's nose + the drip ----------------
def nose_xy(x, y, s, t=None, lean=0.0, squash=0.0):
    """where Chubby INK's nose tip is for chub(f, x, y, s, t=..., lean=...) (head centre ~ (x, y - 436 s) + the breathing bob)."""
    bob = 3.0 * math.sin(t * 2.4) if t is not None else 0.0
    sq = 1 + 0.12 * squash; lr = math.radians(lean)
    hx = x + 54 * s * math.sin(lr); hy = y - 222 * s / sq - 214 * s / sq + 1.5 * bob * s
    a = math.radians(-lean * 0.6)
    dx, dy = 8 * s, 41 * s
    return hx + dx * math.cos(a) - dy * math.sin(a), hy + dx * math.sin(a) + dy * math.cos(a)


def drip(f, nx, ny, s, t, t0, period=1.6, amt=1.0, seed=0, side=1):
    """a MUCUS DRIP from a nostril with anticipation + follow-through: it swells (slow in), stretches, the drop lets go (snap), falls with gravity, and the
    stub springs back up (overshoot + settle). amt 0..1 scales it (0 = dry). Loops every `period` s from t0. Returns True on the frame a drop lets go."""
    if amt <= 0.02 or t < t0: return False
    u = ((t - t0) / period + seed * 0.37) % 1.0
    ox = nx + side * 10 * s; oy = ny + 4 * s
    col, sh = MUC, MUC_S
    if u < 0.62:                                                                     # swell + stretch (ease in)
        q = eio(u / 0.62); L = (16 + 46 * q) * s * amt; r = (7 + 9 * q) * s * amt
    elif u < 0.68:                                                                   # the neck thins, it lets go
        q = (u - 0.62) / 0.06; L = (62 + 10 * q) * s * amt; r = 16 * s * amt
    else:                                                                            # stub springs back (follow-through) while the drop falls
        q = (u - 0.68) / 0.32; L = (14 + 10 * math.exp(-6 * q) * math.cos(14 * q)) * s * amt; r = 7 * s * amt
        dy = (60 + 1400 * q * q) * s; dr = 15 * s * amt
        if oy + dy < H:
            cv2.ellipse(f, (int(ox), int(oy + dy)), (int(dr * 0.85), int(dr * 1.25)), 0, 0, 360, C(col), -1, cv2.LINE_AA)
            cv2.ellipse(f, (int(ox), int(oy + dy)), (int(dr * 0.85), int(dr * 1.25)), 0, 0, 360, C(sh), max(2, int(3 * s)), cv2.LINE_AA)
    pts = np.array([(ox - 6 * s * amt, oy), (ox + 6 * s * amt, oy), (ox + r * 0.6, oy + L - r), (ox - r * 0.6, oy + L - r)], np.int32)
    cv2.fillPoly(f, [pts], C(col), cv2.LINE_AA)
    cv2.circle(f, (int(ox), int(oy + L - r)), int(max(2, r)), C(col), -1, cv2.LINE_AA)
    cv2.circle(f, (int(ox), int(oy + L - r)), int(max(2, r)), C(sh), max(2, int(3 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(ox - r * 0.3), int(oy + L - r * 1.3)), int(max(1, r * 0.28)), C(MUC_H), -1, cv2.LINE_AA)
    return 0.62 <= u < 0.62 + 1 / (FPS * period)


def flush(f, x, y, s, k=1.0, t=0.0, lean=0.0):
    """spicy FLUSH: red cheeks + a few heat wiggles above the head + sweat beads (Chubby's head at chub(f, x, y, s))."""
    if k <= 0.02: return
    hx, hy = x + 54 * s * math.sin(math.radians(lean)), y - 436 * s + 4.5 * s * math.sin(t * 2.4)
    for sg in (-1, 1): glow(f, hx + sg * 56 * s, hy + 44 * s, 34 * s, (240, 70, 60), 0.32 * k)
    for j in range(3):                                                               # heat wiggles rising off the head
        xx = hx + (j - 1) * 50 * s; ph = t * 5 + j * 1.7
        P = [(xx + 8 * s * math.sin(ph + v * 6), hy - 110 * s - v * 70 * s) for v in np.linspace(0, 1, 8)]
        cv2.polylines(f, [np.array(P, np.int32)], False, C(_mix(ACC, (255, 255, 255), 0.25)), max(2, int(5 * s * k)), cv2.LINE_AA)


def heat_lines(f, x, y, s, t, k=1.0, n=3, col=None):
    """wavy heat lines rising from (x, y)."""
    for j in range(n):
        xx = x + (j - (n - 1) / 2) * 40 * s; ph = t * 5 + j * 1.9
        P = [(xx + 7 * s * math.sin(ph + v * 6), y - v * 90 * s * k) for v in np.linspace(0, 1, 8)]
        cv2.polylines(f, [np.array(P, np.int32)], False, C(col or ACC), max(2, int(5 * s)), cv2.LINE_AA)


# ---------------- NEW PLACE: THE CHAAT STALL at dusk (a pani-puri cart on a street; string bulbs; far shop lights as bokeh) ----------------
def set_chaat(t=0.0, blur=4, top_y=1300, dim=0.0):
    """CHAAT STALL AT DUSK: violet-orange dusk sky, a blurred street of shopfronts with lit signs (no words), a striped red-cream awning across the top,
    a string of warm bulbs that sway, the cart's steel top at top_y (draw cart_front AFTER Chubby). dim 0..1 = lights down."""
    def mk():
        f = _vgrad((92, 70, 122), (238, 150, 104), 0, 900)
        f[900:] = _vgrad((238, 150, 104), (120, 86, 92), 900, H)[900:]
        rng = np.random.default_rng(7)
        for i in range(7):                                                            # far shopfronts
            x0 = -40 + i * 170; hh = rng.uniform(380, 560); col = [(150, 110, 120), (120, 96, 120), (170, 120, 110)][i % 3]
            cv2.rectangle(f, (x0, int(1220 - hh)), (x0 + 160, 1240), C(col), -1)
            cv2.rectangle(f, (x0 + 20, int(1240 - hh * 0.45)), (x0 + 140, 1210), C((255, 214, 150)), -1)    # a lit shop opening
            cv2.rectangle(f, (x0 + 14, int(1240 - hh * 0.62)), (x0 + 146, int(1240 - hh * 0.5)), C([(90, 170, 150), (230, 120, 90), (240, 200, 90)][i % 3]), -1)  # a sign board (no words)
        cv2.rectangle(f, (0, 1240), (W, top_y), C((96, 80, 86)), -1)                  # the street
        f = _soft(f, blur + 5)
        # the awning (sharp-ish, close to camera)
        for i in range(9):
            col = (214, 58, 44) if i % 2 == 0 else (250, 236, 214)
            pts = np.array([(i * 124 - 10, 250), (i * 124 + 114, 250), (i * 124 + 114, 330), (i * 124 + 52, 360), (i * 124 - 10, 330)], np.int32)
            cv2.fillPoly(f, [pts], C(_mix(col, (240, 226, 210), 0.12)), cv2.LINE_AA)
        cv2.line(f, (0, 250), (W, 250), C(INKC), 6, cv2.LINE_AA)
        f[:250] = f[:250] * 0.0 + np.array(C((150, 44, 36)), np.float32)              # awning roof (above the safe zone line)
        cv2.rectangle(f, (40, 330), (64, top_y), C((120, 92, 70)), -1); cv2.rectangle(f, (1016, 330), (1040, top_y), C((120, 92, 70)), -1)   # poles
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("chaat34", blur, top_y), mk).copy()
    bokeh(f, t, n=16, seed=11, ymin=760, ymax=1220, rmin=14, rmax=44, amt=0.32 * (1 - dim))
    for i in range(8):                                                                # the string of bulbs sways
        x = 80 + i * 130; y = 400 + 30 * math.sin(math.pi * (i + 0.5) / 8) + 4 * math.sin(t * 1.6 + i)
        glow(f, x, y, 60, (255, 210, 140), 0.22 * (1 - 0.6 * dim))
        cv2.circle(f, (int(x), int(y)), 12, C((255, 236, 180)), -1, cv2.LINE_AA)
    xs = [80 + i * 130 for i in range(8)]; ys = [400 + 30 * math.sin(math.pi * (i + 0.5) / 8) + 4 * math.sin(t * 1.6 + i) - 14 for i in range(8)]
    cv2.polylines(f, [np.array(list(zip(xs, ys)), np.int32)], False, C((60, 44, 40)), 3, cv2.LINE_AA)
    glow(f, 540, 1150, 700, (255, 196, 130), 0.14)                                   # warm key light from the stall lamp
    if dim > 0: f *= (1 - 0.5 * dim)
    return inkify(f)


def cart_front(f, top_y=1300, props=True):
    """the pani-puri cart: a steel top edge, a glass case of puris, a wooden body with a painted red band; drawn AFTER Chubby."""
    cv2.rectangle(f, (0, top_y), (W, H), C((176, 120, 72)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y), (W, top_y + 26), C(STEELC), -1, cv2.LINE_AA)
    cv2.line(f, (0, top_y), (W, top_y), C(INKC), 6, cv2.LINE_AA); cv2.line(f, (0, top_y + 26), (W, top_y + 26), C(INKC), 4, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y + 110), (W, top_y + 150), C(ACC), -1, cv2.LINE_AA)
    cv2.line(f, (0, top_y + 110), (W, top_y + 110), C(INKC), 4, cv2.LINE_AA); cv2.line(f, (0, top_y + 150), (W, top_y + 150), C(INKC), 4, cv2.LINE_AA)
    for x in range(60, W, 160): cv2.circle(f, (x, top_y + 130), 8, C((250, 230, 190)), -1, cv2.LINE_AA)
    _hatch_band(f, top_y + 154, H)


def loop_seam(f, first, t, t_end, dur=0.33):
    """LOOP SEAM (ep 34 craft skill): over the last `dur` seconds blend the frame toward the video's first frame, so the replay starts with no jump."""
    q = clamp((t - (t_end - dur)) / dur)
    if q <= 0: return f
    q = eio(q)
    return f * (1 - q) + first * q
