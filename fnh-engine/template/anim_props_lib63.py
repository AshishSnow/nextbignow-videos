# ================= anim_props_lib63.py (ep 63) (ep 63, 26 Nov): "Can going out with wet hair give you a cold?" — ACCENT = WET TEAL (the water on his
# hair, the towel, the 'wet' words). The cold virus keeps its lib44 olive; blood vessels = red; germ fighters = mint. Everything else = ink palette.
# NEW PLACE: set_door(t, blur, dim) + door_front(f) = a winter MORNING FRONT DOOR inside an Indian flat: warm peach hallway wall, shoe rack + key hooks +
#   a wall calendar on the left, the front door open on the right onto a foggy cold blue morning (balcony rail, far blocks, a bare tree); the cold
#   light from the door is the key light (a cool spill on the floor). Chubby stands in the doorway, mom inside with a towel.
# NEW ACTING (ep 63): wet_hair(f, x, y, s, t, k) = water drips that swell + let go + fall from his hair rim, a wet sheen + flattened strands;
#   towel_head(f, x, y, s, k) = the towel thrown over his head (the end gag).
# NEW PROPS (ink): towel_el (striped teal towel, fringe), footbowl_el (steel basin of ice water with two bare feet), wbc_el (a mint germ-fighter
#   buddy with a shield), icon_row (an icon array: n little people, the sick ones red-nosed = '3 in 10'), nose_board (profile head + nose
#   passage + the blood vessel that SQUEEZES, fighters riding it, the sleeping virus that wakes + grows), sink_el (a hall wash basin + tap).
ACC = (30, 150, 172); ACC_S = (14, 92, 112); ACC_L = (150, 214, 226); ACC_XL = (214, 240, 244)
WATER = (170, 214, 236); WATER_S = (70, 140, 180); WATER_H = (246, 252, 255)
BLOOD = (200, 52, 56); BLOOD_S = (130, 26, 34)
FIGHT = (150, 222, 190); FIGHT_S = (52, 140, 104)
RED = (176, 40, 44); OKG = (40, 140, 80)
COAT = (246, 248, 250)
TOWEL = (40, 160, 178); TOWEL_S = (20, 106, 124); TOWEL_B = (250, 236, 206)
SRC_MAYO = "Source: Mayo Clinic; Cleveland Clinic"
SRC_UH = "Source: University Hospitals; Mayo Clinic"
SRC_CDF = "Source: Johnson & Eccles, Cardiff University (Family Practice, 2005)"
SC3 = 3
DOOR_FLOOR = 1390


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


# ---------------- NEW PLACE: the winter-morning FRONT DOOR ----------------
def set_door(t=0.0, blur=4, dim=0.0, fog_t=True):
    def mk():
        f = _vgrad((236, 216, 192), (220, 196, 168), 0, DOOR_FLOOR)
        cv2.rectangle(f, (0, DOOR_FLOOR - 70), (W, DOOR_FLOOR), C((196, 168, 140)), -1, cv2.LINE_AA)              # skirting
        # the open front door: frame x 600..1000, y 360..floor; outside = a foggy cold morning
        x0, y0, x1 = 600, 360, 1000
        out = _vgrad((168, 192, 220), (214, 224, 234), y0, DOOR_FLOOR)
        f[y0:DOOR_FLOOR, x0:x1] = out[y0:DOOR_FLOOR, x0:x1]
        for (bx, bw, bh, c) in ((620, 120, 520, (150, 170, 196)), (760, 90, 640, (160, 178, 202)), (870, 130, 460, (146, 166, 192))):  # far blocks in fog
            cv2.rectangle(f, (bx, DOOR_FLOOR - 260 - bh), (bx + bw, DOOR_FLOOR - 260), C(c), -1, cv2.LINE_AA)
            for wy in range(DOOR_FLOOR - 240 - bh, DOOR_FLOOR - 280, 60):
                for wx in range(bx + 14, bx + bw - 20, 34): cv2.rectangle(f, (wx, wy), (wx + 16, wy + 24), C((186, 200, 220)), -1)
        pts = [(980, DOOR_FLOOR - 200), (930, 900), (900, 760), (870, 640)]                                      # a bare winter tree
        for a, b in zip(pts[:-1], pts[1:]): cv2.line(f, a, b, C((110, 112, 128)), 16, cv2.LINE_AA)
        for (a, b) in (((930, 900), (840, 820)), ((900, 760), (960, 660)), ((870, 640), (820, 560)), ((870, 640), (900, 540))):
            cv2.line(f, a, b, C((118, 120, 136)), 8, cv2.LINE_AA)
        for k_ in range(3):                                                                                        # fog bands
            yy = 820 + 170 * k_
            band = np.zeros((H, W), np.float32); cv2.ellipse(band, (800, yy), (260, 60), 0, 0, 360, 1.0, -1)
            band = cv2.GaussianBlur(band, (0, 0), 30)[..., None] * 0.35
            f[:] = f * (1 - band) + np.array([0.93, 0.95, 0.97], np.float32) * band
        cv2.rectangle(f, (x0, DOOR_FLOOR - 230), (x1, DOOR_FLOOR - 218), C((90, 96, 110)), -1)                       # balcony rail
        for rx in range(x0 + 20, x1, 46): cv2.line(f, (rx, DOOR_FLOOR - 218), (rx, DOOR_FLOOR), C((90, 96, 110)), 6, cv2.LINE_AA)
        cv2.rectangle(f, (x0 - 34, y0 - 34), (x1 + 34, DOOR_FLOOR), C((150, 104, 66)), 30, cv2.LINE_AA)            # door frame (wood)
        cv2.rectangle(f, (x0 - 50, y0 - 50), (x1 + 50, DOOR_FLOOR), C(INKC), 5, cv2.LINE_AA)
        cv2.fillPoly(f, [np.int32([(x1 + 34, y0 - 20), (W, y0 - 70), (W, DOOR_FLOOR + 40), (x1 + 34, DOOR_FLOOR)])], C((164, 112, 70)), cv2.LINE_AA)  # door leaf open in
        cv2.circle(f, (1050, 900), 12, C((214, 180, 90)), -1, cv2.LINE_AA)
        # left wall: key hooks, a calendar, a shoe rack
        cv2.rectangle(f, (90, 980), (300, 1000), C((150, 104, 66)), -1, cv2.LINE_AA)
        for kx in (120, 170, 220, 270): cv2.line(f, (kx, 1000), (kx, 1030), C((120, 100, 80)), 5, cv2.LINE_AA)
        cv2.rectangle(f, (120, 720), (300, 930), C((252, 248, 238)), -1, cv2.LINE_AA); cv2.rectangle(f, (120, 720), (300, 770), C((200, 70, 60)), -1)
        for gy in range(790, 920, 32):
            for gx in range(135, 290, 32): cv2.rectangle(f, (gx, gy), (gx + 20, gy + 18), C((214, 206, 190)), -1)
        cv2.rectangle(f, (40, 1160), (420, DOOR_FLOOR - 70), C((140, 96, 60)), -1, cv2.LINE_AA)                    # shoe rack
        for sy in (1230, 1300): cv2.line(f, (40, sy), (420, sy), C((110, 74, 44)), 8, cv2.LINE_AA)
        for i_, (sx, c) in enumerate(((80, (60, 70, 90)), (170, (200, 60, 60)), (260, (240, 240, 240)), (340, (80, 120, 90)))):
            cv2.ellipse(f, (sx, 1216), (34, 14), 0, 180, 360, C(c), -1, cv2.LINE_AA); cv2.ellipse(f, (sx + 10, 1286), (34, 14), 0, 180, 360, C(c), -1, cv2.LINE_AA)
        cv2.rectangle(f, (0, DOOR_FLOOR), (W, H), C((204, 178, 150)), -1)                                          # floor tiles
        for xx in range(-200, W + 200, 160): cv2.line(f, (xx, DOOR_FLOOR), (int(540 + (xx - 540) * 1.9), H), C((180, 152, 124)), 3, cv2.LINE_AA)
        for yy in (1450, 1560, 1720): cv2.line(f, (0, yy), (W, yy), C((180, 152, 124)), 3, cv2.LINE_AA)
        cv2.ellipse(f, (800, DOOR_FLOOR + 50), (250, 40), 0, 0, 360, C((160, 80, 70)), -1, cv2.LINE_AA)              # doormat
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("door63", blur), mk).copy()
    glow(f, 800, 900, 520, (210, 228, 250), 0.22)                                                                  # the cold morning light from the door
    cool = np.zeros((H, W), np.float32)
    cv2.fillPoly(cool, [np.int32([(600, DOOR_FLOOR), (1000, DOOR_FLOOR), (1080, H), (380, H)])], 1.0)
    cool = cv2.GaussianBlur(cool, (0, 0), 40)[..., None] * 0.18
    f[:] = f * (1 - cool) + np.array([0.86, 0.92, 1.0], np.float32) * cool
    if fog_t:
        for k_ in range(2):
            xx = 640 + ((t * 30 + 200 * k_) % 360)
            glow(f, xx, 1000 + 160 * k_, 120, (236, 242, 248), 0.08)
    if dim > 0: f *= (1 - 0.6 * dim)
    return inkify(f)


# ---------------- ACTING: wet hair ----------------
DRIP_PTS = [(-30, -118, 1.25, 0.3), (24, -120, 1.1, 0.75), (-96, -30, 1.15, 0.0), (-70, -92, 1.4, 0.4), (88, -40, 1.05, 0.7), (64, -98, 1.55, 0.15), (-112, 30, 1.3, 0.55), (110, 22, 1.2, 0.85)]


def head_c(x, y, s, t=None, lean=0.0, squash=0.0):
    """Chubby INK's head centre for chub(f, x, y, s, t=..., lean=...) (nose_xy minus the nose offset)."""
    bob = 3.0 * math.sin(t * 2.4) if t is not None else 0.0
    sq = 1 + 0.12 * squash; lr = math.radians(lean)
    return x + 54 * s * math.sin(lr), y - 222 * s / sq - 214 * s / sq + 1.5 * bob * s


def wet_hair(f, x, y, s, t, k=1.0, lean=0.0, squash=0.0, floor=None):
    """WET HAIR on Chubby INK: a cool sheen over the scribble hair (two glossy arcs), little flattened wet strands at the rim, and drips that SWELL
    (slow in), LET GO (snap) and FALL with gravity from 6 rim points at uneven periods (no two drops in sync). k 0..1 = how wet."""
    if k <= 0.02: return
    hx, hy = head_c(x, y, s, t, lean, squash)
    for a0, a1, rr in ((200, 250, 92), (275, 320, 96)):
        cv2.ellipse(f, (int(hx), int(hy - 26 * s)), (int(rr * s), int((rr - 14) * s)), 0, a0, a1, C(WATER_H), max(2, int(9 * s * k)), cv2.LINE_AA)
    for j, (dx, dy, per, off) in enumerate(DRIP_PTS):
        ox, oy = hx + dx * s, hy + dy * s + 4 * s
        u = ((t + off * per) / per) % 1.0
        if u < 0.6:
            r = (4 + 11 * eio(u / 0.6)) * s * k; L = r * 1.3
            cv2.ellipse(f, (int(ox), int(oy + L * 0.5)), (int(max(1, r * 0.8)), int(max(1, r * 1.1))), 0, 0, 360, C(WATER), -1, cv2.LINE_AA)
            cv2.ellipse(f, (int(ox), int(oy + L * 0.5)), (int(max(1, r * 0.8)), int(max(1, r * 1.1))), 0, 0, 360, C(WATER_S), max(1, int(2.5 * s)), cv2.LINE_AA)
        else:
            q = (u - 0.6) / 0.4; r = 13 * s * k
            yy = oy + 14 * s + 1900 * q * q * s / 1.5
            if floor is not None and yy > floor: continue
            if yy < H:
                cv2.ellipse(f, (int(ox), int(yy)), (int(r * 0.75), int(r * 1.15)), 0, 0, 360, C(WATER), -1, cv2.LINE_AA)
                cv2.ellipse(f, (int(ox), int(yy)), (int(r * 0.75), int(r * 1.15)), 0, 0, 360, C(WATER_S), max(1, int(2.5 * s)), cv2.LINE_AA)
                cv2.circle(f, (int(ox - r * 0.25), int(yy - r * 0.4)), max(1, int(r * 0.25)), C(WATER_H), -1, cv2.LINE_AA)


def towel_el(seed=631, w=200, h=300):
    def mk():
        im, d, S = _cv(w, h)
        P = [(14, 10), (w - 14, 10), (w - 8, h - 30), (12, h - 30)]
        _ink_poly(d, P, TOWEL, seed)
        for yy in (60, 84, h - 80):
            d.rectangle(S(18, yy, w - 14, yy + 12), fill=TOWEL_B + (255,))
        _hatch_in(im, (100, 10, w - 8, h - 30), lambda q, S_: q.polygon(S_(100, 10, w - 14, 10, w - 8, h - 30, 100, h - 30), fill=255))
        for fx in range(20, w - 10, 16):
            d.line(_P([(fx, h - 30), (fx + 2, h - 10)]), fill=INKC + (255,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("towel63", seed, w, h), mk)


def towel_head(f, x, y, s, k=1.0, t=0.0, lean=0.0):
    """the towel thrown over his head: k 0..1 = falling onto it (a soft cap over the hair + two flaps hanging past the ears, fringe at the ends)."""
    if k <= 0.01: return
    hx, hy = head_c(x, y, s, t, lean)
    dy = -300 * s * (1 - k); cy = hy - 30 * s + dy
    cap = [(hx + (150 + 8 * math.sin(a * 9)) * s * math.cos(a), cy + 10 * s - (112 + 10 * math.sin(a * 7)) * s * math.sin(a)) for a in np.linspace(0, math.pi, 40)]
    flapR = [(hx + 150 * s, cy), (hx + 158 * s, cy + 120 * s), (hx + 98 * s, cy + 126 * s), (hx + 104 * s, cy + 10 * s)]
    flapL = [(hx - 150 * s, cy), (hx - 104 * s, cy + 10 * s), (hx - 98 * s, cy + 126 * s), (hx - 158 * s, cy + 120 * s)]
    for P in (flapL, flapR):
        P = np.int32(P); cv2.fillPoly(f, [P], C(TOWEL_S), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), max(3, int(5 * s)), cv2.LINE_AA)
        for j in range(5):
            fx = P[2][0] + (P[3][0] - P[2][0]) * j / 4; fy = P[2][1] + (P[3][1] - P[2][1]) * j / 4
            cv2.line(f, (int(fx), int(fy)), (int(fx), int(fy + 16 * s)), C(INKC), max(2, int(3 * s)), cv2.LINE_AA)
    P = np.int32(cap)
    cv2.fillPoly(f, [P], C(TOWEL), cv2.LINE_AA)
    for fx in (-60, 10, 70):
        cv2.ellipse(f, (int(hx + fx * s), int(cy - 20 * s)), (int(26 * s), int(70 * s)), 0, 200, 300, C(TOWEL_S), max(2, int(5 * s)), cv2.LINE_AA)
    cv2.polylines(f, [P], True, C(INKC), max(3, int(6 * s)), cv2.LINE_AA)


def footbowl_el(ice=True, seed=632):
    """a steel basin of ICE WATER seen from the front, two bare feet + shins going into it, ice cubes bobbing."""
    def mk():
        w, h = 420, 300; im, d, S = _cv(w, h)
        for sx in (150, 270):                                                                   # shins (behind the rim)
            _ink_poly(d, [(sx - 30, 0), (sx + 30, 0), (sx + 30, 150), (sx - 30, 150)], INK_SKIN, seed + sx)
        _ink_poly(d, [(20, 120), (400, 120), (360, 290), (60, 290)], (206, 212, 220), seed)    # basin
        d.polygon(S(30, 130, 390, 130, 382, 160, 38, 160), fill=WATER + (255,))
        if ice:
            for (ix, iy) in ((90, 118), (200, 112), (320, 120)):
                _ink_poly(d, [(ix - 22, iy - 18), (ix + 22, iy - 22), (ix + 26, iy + 16), (ix - 20, iy + 20)], (236, 246, 252), seed + ix)
        _hatch_in(im, (230, 160, 360, 290), lambda q, S_: q.polygon(S_(230, 160, 380, 160, 360, 290, 230, 290), fill=255))
        d.line(_P([(40, 200), (380, 200)]), fill=(150, 158, 168, 255), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("footbowl63", ice, seed), mk)


def wbc_el(mood="angry", look=(0, 0), seed=633, sh=True):
    """a GERM FIGHTER (a white blood cell as a mint buddy with a little round shield)."""
    def mk():
        w, h = 130, 120; im, d, S = _cv(w, h)
        _ink_ell(d, 58, 62, 44, 42, FIGHT, seed, INK_W - 1, n=24, amp=2.4)
        _shade(im, lambda q, S_: q.ellipse(S_(14, 20, 102, 104), fill=255), lambda q, S_, c: q.ellipse(S_(56, 34, 120, 120), fill=c), FIGHT_S, 90)
        _face(d, S, 56, 62, 0.85, mood, look)
        if sh:
            _ink_ell(d, 106, 78, 20, 24, (246, 236, 196), seed + 1, INK_W - 2, n=18, amp=1.0)
            d.line(_P([(106, 60), (106, 96)]), fill=INKC + (255,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("wbc63", mood, look, seed, sh), mk)


def person_icon(f, x, y, s=1.0, sick=0.0, t=0.0, col=None):
    """an icon-array person (head + shoulders). sick 0..1 = red nose + tissue-pink cheeks + a tiny 'achoo' wobble."""
    wob = 4 * s * math.sin(t * 30) * sick
    c = col or ((214, 206, 196) if sick < 0.5 else (250, 216, 200))
    cv2.ellipse(f, (int(x + wob), int(y + 40 * s)), (int(38 * s), int(30 * s)), 0, 180, 360, C(c), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x + wob), int(y + 40 * s)), (int(38 * s), int(30 * s)), 0, 180, 360, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(x + wob), int(y)), int(22 * s), C(c), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x + wob), int(y)), int(22 * s), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    if sick > 0.5:
        cv2.circle(f, (int(x + wob), int(y + 4 * s)), int(7 * s), C(RED), -1, cv2.LINE_AA)
        for dx in (-12, 12): cv2.circle(f, (int(x + wob + dx * s), int(y - 6 * s)), max(1, int(3 * s)), C(INKC), -1, cv2.LINE_AA)


def icon_row(f, x0, y, n, lit, t, t0s, gap=78, s=1.0):
    """a row of n people; the first len(t0s) of them in `lit` turn sick at their own time (an icon array: '3 in 10')."""
    for i in range(n):
        sk = 0.0
        if i in lit:
            j = lit.index(i)
            if j < len(t0s) and t > t0s[j]: sk = 1.0
        person_icon(f, x0 + i * gap, y, s, sk, t)


# board nose (from ep 34 board_head): profile, back of head, the nose passage, + a BLOOD VESSEL above the passage that squeezes
PROFILE = [(470, 470), (560, 500), (612, 560), (630, 640), (650, 700), (700, 790), (740, 860), (706, 880), (660, 884), (668, 930), (650, 960),
           (672, 1000), (650, 1040), (620, 1090), (560, 1130), (470, 1150), (470, 1240)]
BACK = [(470, 470), (380, 470), (290, 520), (230, 620), (210, 760), (230, 900), (280, 1010), (330, 1080), (330, 1240)]
CAVITY = [(690, 866), (640, 836), (560, 790), (500, 770), (470, 800), (520, 840), (600, 870), (660, 882)]
VESSEL = [(300, 700), (380, 720), (450, 742), (520, 760), (590, 784), (650, 812), (700, 846)]


def _poly_at(P, u):
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(P[:-1], P[1:])]; L = sum(seg); d = clamp(u) * L
    for (a, b), sl in zip(zip(P[:-1], P[1:]), seg):
        if d <= sl: q = d / max(1e-6, sl); return a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q
        d -= sl
    return P[-1]


def nose_board(f, t, k=1.0, sq=0.0, fighters=0.0, vir=0.0, vir_mood="sleep", dx=0, dy=0, sc=1.0):
    """the profile head on the board with the nose passage and ONE red blood vessel feeding it; sq 0..1 = how hard the chill squeezes the vessel
    (its width shrinks, a pinch ring at the squeeze, red cells slow down); fighters 0..1 = germ fighters riding the vessel (with sq most stop at the
    pinch); vir 0..1 = the virus asleep in the passage -> awake + bigger."""
    tr = lambda P: [(540 + (x - 540) * sc + dx, 860 + (y - 860) * sc + dy) for x, y in P]
    draw_on(f, tr(BACK), k, BP_INK, 7, seed=22, tip=False)
    draw_on(f, tr(PROFILE), k, BP_INK, 7, seed=23)
    if k < 0.6: return
    q = clamp((k - 0.6) / 0.4)
    cv2.fillPoly(f, [np.array(tr(CAVITY), np.int32)], C(_mix((255, 255, 255), (236, 214, 208), q)), cv2.LINE_AA)
    draw_on(f, tr(CAVITY), q, BP_INK, 5, seed=24, tip=False, closed=True)
    V = tr(VESSEL)
    w0 = 26 * sc; pinch = (0.45, 0.75)
    for i in range(len(V) - 1):
        u = (i + 0.5) / (len(V) - 1)
        wk = 1 - 0.62 * sq * (1.0 if pinch[0] < u < pinch[1] else 0.55)
        ww = int(max(4, w0 * wk))
        cv2.line(f, (int(V[i][0]), int(V[i][1])), (int(V[i + 1][0]), int(V[i + 1][1])), C(BLOOD), ww, cv2.LINE_AA)
    for i in range(len(V) - 1):
        cv2.line(f, (int(V[i][0]), int(V[i][1] - 15 * sc)), (int(V[i + 1][0]), int(V[i + 1][1] - 15 * sc)), C(BLOOD_S), 2, cv2.LINE_AA)
    sp = 0.35 * (1 - 0.7 * sq)
    for j in range(7):                                                              # red cells flowing (slower when squeezed)
        u = (t * sp + j / 7) % 1.0
        px, py = _poly_at(V, u)
        cv2.circle(f, (int(px), int(py)), int(6 * sc), C((255, 140, 140)), -1, cv2.LINE_AA)
    if sq > 0.05:                                                                   # the squeeze: two ink 'clamp' marks
        for u in (0.5, 0.68):
            px, py = _poly_at(V, u)
            for sg in (-1, 1):
                cv2.line(f, (int(px - 16 * sc), int(py + sg * (34 - 14 * sq) * sc)), (int(px + 16 * sc), int(py + sg * (34 - 14 * sq) * sc)), C(ACC_S), 6, cv2.LINE_AA)
    if fighters > 0.01:
        for j in range(5):
            u = ((t * 0.22 + j / 5) % 1.0)
            if sq > 0.3 and j % 3 != 0: u = min(u, 0.42 + 0.02 * j)                 # most are stuck before the pinch
            px, py = _poly_at(V, u)
            comp(f, scale_el(wbc_el("angry" if sq < 0.3 else "sad", (1, 0)), 0.55 * sc * fighters), px, py - 30 * sc)
    if vir > 0.01:
        cx, cy = tr([(585, 826)])[0]
        g = 0.4 + 0.5 * vir
        comp(f, scale_el(virus_el("sly" if vir > 0.5 else "n", (1, 0), int(t * 8) % 4), g * sc), cx, cy)
        if vir < 0.5:
            write_on(f, "z z", cx + 60 * sc, cy - 70 * sc, 99, 0, 30, BP_INK)
    return V


def sink_el(seed=634):
    """a small hall wash basin with a tap (generic)."""
    def mk():
        w, h = 360, 300; im, d, S = _cv(w, h)
        _ink_poly(d, [(150, 20), (210, 20), (210, 60), (150, 60)], (200, 206, 214), seed)
        _ink_poly(d, [(170, 50), (190, 50), (190, 120), (240, 120), (240, 140), (170, 140)], (200, 206, 214), seed + 1)
        _ink_ell(d, 180, 200, 160, 60, (246, 248, 250), seed + 2, INK_W, n=32)
        _ink_poly(d, [(60, 210), (300, 210), (230, 296), (130, 296)], (236, 238, 242), seed + 3)
        _hatch_in(im, (180, 210, 300, 296), lambda q, S_: q.polygon(S_(180, 210, 300, 210, 230, 296, 180, 296), fill=255))
        return _done(im, w, h)
    return gcache(("sink63", seed), mk)
