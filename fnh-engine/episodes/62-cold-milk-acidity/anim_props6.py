# ================= anim_props6.py = lib62 (ep 62, 25 Nov): "Does cold milk cure acidity?" — ACCENT = BURN ORANGE (the heartburn flames, the acid,
# the hot words). Milk keeps its own cream white + a cold frost blue on the glass; everything else stays in the ink palette.
# NEW CRAFT (ep 62) = THE CLOCK WIPE (editing: a transition that SAYS 'time passed'): clock_wipe(prev, cur, p, cx, cy) lives in anim_fx (template);
#   this file adds the clock icon that rides on the wipe centre (clock_icon) so the pivot reads as a clock even on a white board.
# NEW PLACE: set_bedroom(t, dim, lamp) + bed_front(f, top_y, t, glass) = a night bedroom (indigo wall, moon window + curtain, wooden headboard,
#   bedside table + a warm lamp) - Chubby sits up in bed behind the quilt; the bedside table carries the glass of cold milk (the send line).
# NEW ACTING (ep 62): heartburn(f, x, y, s, t, k) = little ink flames licking up from his chest (k = how bad), hand-on-chest wince, the relief
#   exhale, the comeback take, a burp puff (burp_puff).
# NEW PROPS (ink): milk_glass_el(level, frost) (a cold tumbler: condensation beads + frost rim), carton_el(label, col) (a generic milk carton, no
#   brand), acid_pool (the stomach's acid as a hatched orange pool with flames on its surface), board_pipe (food pipe + the VALVE flaps + acid that
#   climbs), clock_icon, week_strip (a 7-day row where burn marks pop), meter_el (an ACID meter for the 1976 test).
ACC = (236, 96, 40); ACC_S = (170, 52, 20); ACC_L = (250, 170, 120); ACC_XL = (254, 226, 206)
FLAME_Y = (255, 210, 80)
MILK = (252, 249, 240); MILK_S = (222, 216, 202)
FROST = (206, 228, 248); FROST_S = (150, 190, 228)
RED = (176, 40, 44); OKG = (40, 140, 80)
COAT = (246, 248, 250)
NIGHT = (58, 56, 96)
SRC_TEMP = "Source: Prevention (Dr J. Koufman); GI Consultants San Antonio"
SRC_1976 = "Source: Ippoliti et al., Annals of Internal Medicine (1976)"
SRC_FAT = "Source: Healthline (medically reviewed); Bon Secours"
SRC_WEEK = "Source: Bon Secours Health System"
SC3 = 3


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


# ---------------- props ----------------
def milk_glass_el(level=0.8, frost=1.0, mood=None, look=(0, 0), seed=621):
    """a tumbler of COLD milk: cream milk, a pale frost band at the rim, condensation beads on the glass (cold you can see)."""
    lv = round(clamp(level) * 10) / 10; fr = round(clamp(frost) * 4) / 4
    def mk():
        w, h = 200, 300; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        yl = 270 - 230 * lv
        if lv > 0.02:
            d.polygon(S(34, yl, 166, yl, 158, 270, 42, 270), fill=MILK + (255,))
            d.polygon(S(110, yl, 166, yl, 158, 270, 116, 270), fill=MILK_S + (150,))
            d.line(_P([(36, yl), (164, yl)]), fill=INKC + (190,), width=3 * SC3)
        if fr > 0:
            d.polygon(S(26, 22, 174, 22, 170, 70, 30, 70), fill=FROST + (int(110 * fr),))
        _ink_poly(d, [(24, 20), (176, 20), (160, 280), (40, 280)], None, seed, INK_W, amp=0.9)
        d.line(_P([(50, 50), (58, 240)]), fill=(255, 255, 255, 220), width=7 * SC3)
        for i in range(int(14 * fr)):                                                         # condensation beads
            x = rng.uniform(46, 154); y = rng.uniform(60, 262); r = rng.uniform(3.5, 7)
            d.ellipse(S(x - r, y - r, x + r, y + r), fill=FROST + (220,), outline=FROST_S + (255,), width=2 * SC3)
            d.ellipse(S(x - r * 0.5, y - r * 0.6, x - r * 0.1, y - r * 0.2), fill=(255, 255, 255, 255))
        if mood: _face(d, S, 100, 190, 1.35, mood, look)
        return _done(im, w, h)
    return gcache(("mglass62", lv, fr, mood, tuple(look), seed), mk)


def carton_el(label="WHOLE", col=None, seed=622, mood=None):
    """a generic milk carton (gable top, coloured band, a plain word label; no brand, no logo)."""
    col = col or (70, 120, 200)
    def mk():
        w, h = 220, 360; im, d, S = _cv(w, h)
        body = [(30, 110), (190, 110), (190, 340), (30, 340)]
        _ink_poly(d, body, (250, 248, 242), seed, INK_W, amp=0.8)
        _shade(im, lambda q, S_: q.polygon(_P(body), fill=255), lambda q, S_, c: q.rectangle(S_(140, 100, 220, 350), fill=c), MILK_S, 140)
        top = [(30, 110), (60, 40), (160, 40), (190, 110)]
        _ink_poly(d, top, _mix(col, (255, 255, 255), 0.55), seed + 1, INK_W, amp=0.8)
        _ink_poly(d, [(60, 40), (60, 18), (160, 18), (160, 40)], _mix(col, (255, 255, 255), 0.3), seed + 2, INK_W - 2, amp=0.5)
        d.rectangle(S(34, 190, 186, 262), fill=tuple(col) + (255,))
        fn = font(F_BLACK, int((44 if len(label) <= 5 else 34) * SC3))
        d.text((110 * SC3, 226 * SC3), label, font=fn, fill=(255, 255, 255, 255), anchor="mm")
        for i in range(3):                                                                    # a little milk drop icon
            pass
        d.ellipse(S(94, 128, 126, 170), fill=MILK + (255,), outline=INKC + (255,), width=3 * SC3)
        if mood: _face(d, S, 110, 296, 1.2, mood, (0, 0))
        return _done(im, w, h)
    return gcache(("carton62", label, col, seed, mood), mk)


def meter_el(v=0.2, label="ACID"):
    """a tall ACID meter (thermometer style): v 0..1, the top third is hot orange."""
    vv = round(clamp(v) * 20) / 20
    def mk():
        w, h = 120, 380; im, d, S = _cv(w, h)
        _ink_poly(d, [(36, 20), (84, 20), (84, 300), (36, 300)], (252, 250, 244), 623, INK_W - 1, amp=0.5)
        top = 296 - 270 * vv
        if vv > 0: d.rectangle(S(42, top, 78, 296), fill=(ACC if vv > 0.55 else ACC_L) + (255,))
        _ink_ell(d, 60, 322, 40, 40, ACC if vv > 0.55 else ACC_L, 624, INK_W - 1, amp=0.5)
        for j in range(6): d.line(S(84, 40 + j * 50, 98, 40 + j * 50), fill=INKC + (255,), width=3 * SC3)
        d.line(S(36, 110, 84, 110), fill=ACC_S + (200,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("meter62", vv, label), mk)


def heartburn(f, x, y, s, t, k=1.0, seed=0, n=5, spread=70):
    """HEARTBURN you can see: n little ink flames licking up from a point on his chest (x, y = the base). k 0..1 = how bad (height + count)."""
    if k <= 0.02: return
    glow(f, x, y - 40 * s * k, 150 * s * (0.5 + k), (255, 140, 60), 0.28 * k)
    m = max(1, int(round(n * min(1.0, 0.4 + k))))
    for i in range(m):
        u = (i - (m - 1) / 2) / max(1, (m - 1) / 2) if m > 1 else 0
        bx = x + u * spread * s
        ph = math.sin(t * 17 + i * 2.3 + seed) * 0.5 + 0.5
        hgt = (70 + 50 * ph) * s * k * (1 - 0.35 * abs(u)); hw = (20 + 6 * ph) * s * (0.6 + 0.4 * k)
        tip = math.sin(t * 9 + i * 1.7 + seed) * 12 * s
        P = [(bx - hw, y)] + [(bx - hw * (1 - a) ** 0.8 + tip * a * a, y - hgt * a) for a in np.linspace(0.15, 1, 7)] + \
            [(bx + hw * (1 - a) ** 0.8 + tip * a * a, y - hgt * a) for a in np.linspace(1, 0.15, 7)] + [(bx + hw, y)]
        cv2.fillPoly(f, [np.int32(P)], C(ACC), cv2.LINE_AA)
        Q = [(bx + (px - bx) * 0.55, y - (y - py) * 0.6) for px, py in P]
        cv2.fillPoly(f, [np.int32(Q)], C(FLAME_Y), cv2.LINE_AA)
        cv2.polylines(f, [np.int32(P)], True, C(ACC_S), max(2, int(3 * s)), cv2.LINE_AA)


def burp_puff(f, x, y, s, t, t0, dur=0.9):
    """a tiny comic burp: a small orange-grey puff with a curl that rises and fades from the mouth."""
    u = (t - t0) / dur
    if not (0 <= u <= 1): return
    for j in range(3):
        r = (18 + 26 * u + 8 * j) * s; px = x + (20 + 40 * u) * s + j * 14 * s; py = y - (30 * u + 18 * j) * s
        a = (1 - u) * 0.8
        lay = f.copy(); cv2.circle(lay, (int(px), int(py)), int(r), C(_mix(ACC_L, (230, 226, 220), 0.4)), -1, cv2.LINE_AA)
        cv2.circle(lay, (int(px), int(py)), int(r), C(INKC), max(2, int(3 * s)), cv2.LINE_AA)
        f[:] = f * (1 - a) + lay * a


def clock_icon(f, x, y, r, t, spin=0.0, op=1.0):
    """an ink wall clock: cream face, 12 ticks, two hands; spin = turns of the minute hand (time passing)."""
    lay = f.copy()
    cv2.circle(lay, (int(x), int(y)), int(r), C((252, 248, 236)), -1, cv2.LINE_AA)
    cv2.circle(lay, (int(x), int(y)), int(r), C(INKC), max(3, int(r * 0.08)), cv2.LINE_AA)
    for j in range(12):
        a = j / 12 * 2 * math.pi; L0 = r * (0.78 if j % 3 else 0.68)
        cv2.line(lay, (int(x + L0 * math.sin(a)), int(y - L0 * math.cos(a))), (int(x + r * 0.88 * math.sin(a)), int(y - r * 0.88 * math.cos(a))), C(INKC),
                 max(2, int(r * 0.04)), cv2.LINE_AA)
    am = spin * 2 * math.pi; ah = am / 12 + 0.9
    cv2.line(lay, (int(x), int(y)), (int(x + r * 0.7 * math.sin(am)), int(y - r * 0.7 * math.cos(am))), C(ACC_S), max(3, int(r * 0.07)), cv2.LINE_AA)
    cv2.line(lay, (int(x), int(y)), (int(x + r * 0.45 * math.sin(ah)), int(y - r * 0.45 * math.cos(ah))), C(INKC), max(4, int(r * 0.09)), cv2.LINE_AA)
    cv2.circle(lay, (int(x), int(y)), max(3, int(r * 0.08)), C(INKC), -1, cv2.LINE_AA)
    f[:] = f * (1 - op) + lay * op


# ---------------- the BOARD stomach with an acid pool + flames, the pipe + valve ----------------
def acid_pool(f, P, level, t, burn=1.0, col=None):
    """fill the bottom of the board stomach polygon P with acid up to `level` (0..1 of its height); flames dance on the surface (burn 0..1)."""
    ys = [p[1] for p in P]; xs = [p[0] for p in P]
    ytop, ybot = min(ys), max(ys); sy = ybot - (ybot - ytop) * 0.62 * level
    m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [np.int32(P)], 255, cv2.LINE_AA)
    xx = np.arange(W); surf = sy + 8 * np.sin(xx / 46 + t * 3.0)
    yy = np.arange(H)[:, None]
    mask = (m > 0) & (yy >= surf[None, :])
    a = mask.astype(np.float32)[..., None] * 0.85
    f[:] = f * (1 - a) + np.array(C(col or ACC_L), np.float32) * a
    for x0 in range(int(min(xs)), int(max(xs)), 26):                                           # hatch inside the pool
        for yv in range(int(sy) + 20, int(ybot), 26):
            if 0 <= yv < H and 0 <= x0 < W and mask[yv, x0]:
                cv2.line(f, (x0, yv), (x0 + 12, yv - 12), C(ACC_S), 2, cv2.LINE_AA)
    pts = [(x, surf[x]) for x in range(int(min(xs)), int(max(xs)), 6) if m[int(min(H - 1, surf[x] + 4)), x] > 0]
    if len(pts) > 2: cv2.polylines(f, [np.int32(pts)], False, C(ACC_S), 5, cv2.LINE_AA)
    if burn > 0.02 and len(pts) > 4:
        xs2 = [p[0] for p in pts]; x0, x1 = min(xs2), max(xs2); n_ = max(2, int((x1 - x0) / 110))
        for i in range(n_):
            px = x0 + (i + 0.5) * (x1 - x0) / n_
            heartburn(f, px, surf[int(px)] + 6, 0.9, t, burn, seed=i * 3, n=3, spread=34)
    return sy


PIPE_X0, PIPE_X1 = 500, 590


def board_pipe(f, t, k=1.0, open_=0.0, acid_up=0.0, y_top=280, y_val=560, flap=46, seed=626):
    """the food pipe into the board stomach's top: two walls, the VALVE = two flaps at y_val (open_ 0 = shut tight, 1 = loose, hanging open),
    acid_up 0..1 = acid climbing up the pipe above the valve (accent with a wobbly top)."""
    draw_on(f, [(PIPE_X0, y_top), (PIPE_X0, y_val)], k, BP_INK, 8, seed=seed, tip=False)
    draw_on(f, [(PIPE_X1, y_top), (PIPE_X1, y_val)], k, BP_INK, 8, seed=seed + 1, tip=False)
    if acid_up > 0.01:
        top = y_val - (y_val - y_top - 20) * acid_up
        P = [(PIPE_X0 + 4, y_val + 10)] + [(x, top + 7 * math.sin(x / 9 + t * 8)) for x in np.linspace(PIPE_X0 + 4, PIPE_X1 - 4, 10)] + [(PIPE_X1 - 4, y_val + 10)]
        cv2.fillPoly(f, [np.int32(P)], C(ACC_L), cv2.LINE_AA)
        cv2.polylines(f, [np.int32(P[1:-1])], False, C(ACC_S), 4, cv2.LINE_AA)
    a = math.radians(-8 + 78 * clamp(open_))                                                     # flap angle down from horizontal
    for sd, x0 in ((1, PIPE_X0), (-1, PIPE_X1)):
        x1 = x0 + sd * flap * math.cos(a); y1 = y_val + flap * math.sin(a)
        Pf = [(x0, y_val - 9), (x1, y1 - 9), (x1, y1 + 9), (x0, y_val + 9)]
        cv2.fillPoly(f, [np.int32(Pf)], C((236, 150, 150)), cv2.LINE_AA)
        cv2.polylines(f, [np.int32(Pf)], True, C(BP_INK), 5, cv2.LINE_AA)
    return (PIPE_X0 + PIPE_X1) / 2, y_val


def week_strip(f, t, marks, y=1160, x0=120, gap=122, size=100):
    """a 7-day row (M T W T F S S) on the board; marks = {day index: t_pop}: a flame pops into that day's box at t_pop."""
    days = "MTWTFSS"
    for i, dch in enumerate(days):
        x = x0 + i * gap
        cv2.rectangle(f, (int(x - size / 2), int(y - size / 2)), (int(x + size / 2), int(y + size / 2)), C(BP_INK), 5, cv2.LINE_AA)
        comp(f, ed_el(dch, "", lead_col=BP_INK, lead_size=40), x, y - size / 2 - 38)
        if i in marks and t >= marks[i]:
            k = snap(t, marks[i], 4)
            heartburn(f, x, y + 30, 0.55 * k + 0.01, t, 1.0, seed=i, n=3, spread=36)


# ---------------- NEW PLACE: THE BEDROOM at night ----------------
BED_TOP = 1420


def set_bedroom(t=0.0, blur=4, top_y=BED_TOP, dim=0.0, lamp=1.0):
    """night bedroom: indigo wall softened toward paper, a moon window with a curtain on the left, a wooden headboard behind the bed, a bedside
    table on the right with a warm lamp (its glow pools on the wall). Chubby sits up in bed at x ~ 440 behind bed_front()."""
    def mk():
        f = _vgrad((84, 82, 128), (60, 58, 98), 0, top_y)
        for xx in range(0, W, 90): cv2.line(f, (xx, 0), (xx, top_y), C((76, 74, 118)), 2, cv2.LINE_AA)          # faint wallpaper stripes
        cv2.rectangle(f, (70, 380), (380, 900), C((52, 44, 60)), -1, cv2.LINE_AA)                                   # window
        f[400:880, 90:360] = _vgrad((24, 30, 70), (64, 54, 98), 400, 880)[400:880, 90:360]
        for (x, y) in ((130, 450), (190, 520), (300, 470), (330, 610), (150, 650), (250, 560)): cv2.circle(f, (x, y), 3, C((240, 240, 255)), -1, cv2.LINE_AA)
        cv2.circle(f, (280, 520), 40, C((240, 236, 214)), -1, cv2.LINE_AA)
        cv2.circle(f, (296, 508), 34, C((30, 34, 74)), -1, cv2.LINE_AA)                                             # crescent
        cv2.line(f, (225, 400), (225, 880), C((52, 44, 60)), 10, cv2.LINE_AA); cv2.line(f, (90, 640), (360, 640), C((52, 44, 60)), 10, cv2.LINE_AA)
        cv2.rectangle(f, (20, 340), (120, 1000), C((150, 96, 120)), -1, cv2.LINE_AA)                                # curtain
        for k_ in range(3): cv2.line(f, (40 + 30 * k_, 360), (40 + 30 * k_, 980), C((120, 70, 96)), 5, cv2.LINE_AA)
        cv2.rectangle(f, (120, 980), (780, top_y), C((140, 92, 58)), -1, cv2.LINE_AA)                               # headboard
        cv2.ellipse(f, (450, 990), (330, 90), 0, 180, 360, C((140, 92, 58)), -1, cv2.LINE_AA)
        for xx in range(170, 760, 75): cv2.line(f, (xx, 960), (xx, top_y), C((118, 74, 44)), 4, cv2.LINE_AA)
        cv2.rectangle(f, (800, 1180), (1080, top_y), C((128, 86, 56)), -1, cv2.LINE_AA)                              # bedside table top/back
        cv2.rectangle(f, (870, 1000), (900, 1180), C((90, 70, 60)), -1, cv2.LINE_AA)                                 # lamp stem
        cv2.fillPoly(f, [np.int32([(800, 1010), (970, 1010), (930, 900), (840, 900)])], C((250, 220, 160)), cv2.LINE_AA)  # shade
        cv2.rectangle(f, (0, top_y), (W, H), C((70, 54, 64)), -1)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("bedroom62", blur, top_y), mk).copy()
    if lamp > 0:
        glow(f, 885, 960, 420, (255, 196, 120), 0.32 * lamp)
        glow(f, 885, 1000, 160, (255, 230, 170), 0.25 * lamp)
    if dim > 0: f *= (1 - 0.6 * dim)
    return inkify(f)


def bed_front(f, top_y=BED_TOP, t=0.0, glass=True, level=0.8, table=True):
    """the quilt across the bottom (Chubby sits behind it) + the bedside table front on the right with the cold glass on it."""
    P = [(0, top_y + 30)] + [(x, top_y + 18 * math.sin(x / 140) - 10) for x in range(0, 800, 40)] + [(800, top_y + 10), (800, H), (0, H)]
    cv2.fillPoly(f, [np.int32(P)], C((150, 206, 196)), cv2.LINE_AA)
    cv2.polylines(f, [np.int32(P[:-2])], False, C(INKC), 7, cv2.LINE_AA)
    for xx in range(60, 800, 150):                                                                 # quilt stitches
        for yy in range(top_y + 70, H, 120):
            cv2.line(f, (xx, yy), (xx + 60, yy + 30), C((110, 170, 160)), 4, cv2.LINE_AA)
    _hatch_band(f, top_y + 200, H)
    if table:
        cv2.rectangle(f, (800, top_y - 60), (1080, H), C((150, 104, 66)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (790, top_y - 80), (1080, top_y - 50), C((170, 120, 78)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (790, top_y - 80), (1080, top_y - 50), C(INKC), 5, cv2.LINE_AA)
        cv2.rectangle(f, (820, top_y), (1060, top_y + 120), C(INKC), 5, cv2.LINE_AA)
        cv2.circle(f, (940, top_y + 60), 9, C(INKC), -1, cv2.LINE_AA)
        if glass: comp(f, scale_el(milk_glass_el(level, 1.0), 0.6), 920, top_y - 80 - 84)
