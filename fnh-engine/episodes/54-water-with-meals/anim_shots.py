# ================= shots: FreshNestHub 54 — "Does drinking water while you eat water down your stomach acid?" (Chubby INK; 35-50 s rule; ONE takeaway) =================
# COLOUR SCRIPT: hot noon DHABA (ochre, sun through the open side) for the story; white board + blue ink for the explanation; ONE accent = ACID LIME (the stomach
# acid, the sensor bells, the acid tap). Water keeps its clear blue only on water. The 'weak acid' moment goes pale; 'back to normal' snaps back to lime.
# Story: THAT UNCLE snatches Chubby's glass mid-sip (water flies, splash on the table = frame 0) -> the question. The answer: stomach acid is MADE WITH WATER;
# food + water stretch the stomach, sensor cells notice, send GASTRIN, the acid tap opens; water it down? same alarm, more acid, back to normal (a thermostat).
# Mayo Clinic: water doesn't thin your digestive juices. Safe tip: sip, don't chug a whole bottle (bloated). Send line = the uncle with the glass; 'then
# pour yourself one' = the pour (the run's liquid-FX craft), and the tail rebuilds the snatch (loop).
END = round(LINES["c3"]["end"] + 1.33, 3)            # 0.1 s air + 0.6 s logo + 0.63 s loop tail
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "really") - 0.12, "punch"),
    ("S1", T("i2", "Every") - 0.12, "whip"), ("S1b", T("i2", "who") - 0.1, "cut"),
    ("S2", T("a1", "Funny") - 0.12, "erase"),
    ("S3", T("b1", "When") - 0.12, "erase"), ("S3b", T("b1", "tiny") - 0.1, "punch"),
    ("S4", T("b2", "They") - 0.1, "erase"),
    ("S5", T("b3", "Water") - 0.12, "erase"),
    ("S6", T("c1", "That's") - 0.12, "whip"),
    ("S7", T("c2", "Just") - 0.12, "cut"), ("S7b", T("c2", "Chugging") - 0.1, "punch"),
    ("S8", T("c3", "Send") - 0.1, "whip"), ("S8b", T("c3", "Then") - 0.1, "cut"),
    ("S10", LINES["c3"]["end"] + 0.1, "punch"), ("S11", LINES["c3"]["end"] + 0.7, "cut"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
MORPH = {}
_write_on0 = write_on


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
    """phone-size hand lettering (ep 27: the kit default reads too small)."""
    _write_on0(f, text, x, y, t, t0, int(size * 1.3), col, cps, op)


def st_(sid): return SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, PAPER, 22), 540, y, op=clamp((t - t0) / 0.2))


def kw(f, text, x, y, t, t0, mode="pop", size=130, col=None, **k):
    kin_word(f, text, x, y, t, t0, mode, size, col or ACC_S, stroke=2, stroke_col=INKC, **k)


def el_at(f, el, x, y, s=1.0, t=None, t0=None, rot=0.0, op=1.0):
    k = 1.0 if t0 is None else (snap(t, t0, 4) if t >= t0 else 0.0)
    if k > 0.01: rot_comp(f, scale_el(el, s), x, y, rot, k, op, 0.0)


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look, turn=clamp(look[0]) * 0.5)


def hook_band(f, y0=228, y1=700, a=0.72):
    m = np.zeros((H, 1), np.float32); m[y0:y1] = a
    m = cv2.GaussianBlur(np.repeat(m, 4, 1), (1, 61), 0)[:, :1, None]
    f[:] = f * (1 - m) + np.array(C(PAPER), np.float32) * m


def hook_words(f, t, t0=-1.0, op=1.0):
    """the hook question as moving words (on screen at frame 0)."""
    kw(f, "DO YOU KNOW IF", 540, 300, t, t0, "pop", 70, col=INKC, op=op)
    kw(f, "WATER WITH FOOD", 540, 425, t, t0, "pop", 84, col=WAT_S, op=op)
    kw(f, "= WEAK ACID?", 540, 590, t, t0, "shake", 132, col=ACC_S, amp=0.35, op=op)


def hand_xy(x, y, s, arm, side, lean=0.0):
    """where chub()'s hand ends up for arm angles (a1, a2) on side -1 (screen-left, la) / +1 (screen-right, ra)."""
    a1, a2 = arm; bcx = x + 40 * s * math.sin(math.radians(lean)); bcy = y - 222 * s
    sx, sy = bcx + side * 118 * s, bcy - 46 * s
    ex, ey = sx + side * math.sin(math.radians(a1)) * 76 * s, sy + math.cos(math.radians(a1)) * 76 * s
    return ex + side * math.sin(math.radians(a2)) * 70 * s, ey + math.cos(math.radians(a2)) * 70 * s


def lerp2(a, b, k): return tuple(a[i] + (b[i] - a[i]) * k for i in range(len(a)))


CX, CY, CS = 330, 1790, 1.75            # Chubby at the dhaba table (table top 1330)
UX, UY, US = 790, 1780, 1.68           # the uncle, standing on the right


# ---- S0: HOOK at frame 0 = MID-ACCIDENT: the uncle has just yanked the glass from Chubby's lips; water flies out in an arc, splashes the table ----
TS0 = -0.18                             # the snatch started before frame 0


def scene0(f, t, words=True):
    u = t - TS0
    k = eio(clamp(u / 0.55))                                                      # the uncle's arm: from Chubby's mouth up and away
    arm = lerp2((-40, -110), (150, 175), k)
    tilt = 70 * (1 - k) + 8 * math.sin(t * 3) * k
    uncle(f, UX, UY, US, t, la=(60, 100) if k > 0.6 else (30, 20), ra=arm, hand_r="grip", hand_l="point" if k > 0.6 else "open",
          mouth=2 if k > 0.6 else "o", expr="angry", brow="sus", look=(-1, 0), turn=-0.5, lean=-6 * (1 - k),
          hold=_rot_el(scale_el(steel_glass_el(0.4), 0.55), tilt), hold_off=(-10, -40), hold_front=True)
    jolt = take(t, TS0 + 0.15)
    chub(f, CX, CY + jolt["dy"], CS, t=t, la=(26, 14), ra=(150, -128), hand_r="pinch", mouth="o" if u < 1.2 else "jaw", expr="wow", brow="up",
         look=(1, -0.4), turn=0.4, lean=jolt["lean"], squash=jolt["squash"])
    fly_drops2(f, CX + 150, CY - 640, 520, -620, t, TS0 + 0.12, n=9, r=12, seed=3, floor=DHA_TOP + 10)        # water thrown out of the glass
    fly_drops2(f, CX + 100, CY - 600, -260, -380, t, TS0 + 0.16, n=6, r=9, seed=8, floor=DHA_TOP + 10)        # ...and onto Chubby
    for j, (dx, dy) in enumerate(((-30, -30), (40, -10), (10, 40))):                                         # drips on his face
        yy = CY - 640 + dy + 60 * clamp((t - TS0 - 0.4 - 0.2 * j) / 1.5)
        cv2.circle(f, (int(CX + dx), int(yy)), 8, C(WAT), -1, cv2.LINE_AA); cv2.circle(f, (int(CX + dx), int(yy)), 8, C(WAT_S), 2, cv2.LINE_AA)
    dhaba_front(f)
    el_at(f, thali_el("full"), 300, 1300, 0.62)
    splash_crown(f, 600, DHA_TOP + 18, t, TS0 + 0.32, r=70, seed=1)
    splash_crown(f, 470, DHA_TOP + 26, t, TS0 + 0.52, r=40, seed=4)


def shot_S0(t, n):
    f = set_dhaba(t)
    scene0(f, t)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="golden")


# ---- S0b: '...really waters down your stomach acid?' dripping close-up + a thought bubble: water pouring into a stomach of lime acid ----
def thought_stomach(f, cx, cy, t, t0, r=190):
    cv2.circle(f, (cx, cy), r, C(PAPER), -1, cv2.LINE_AA); cv2.circle(f, (cx, cy), r, C(INKC), 6, cv2.LINE_AA)
    for j, (dx, dy, rr) in enumerate(((-150, 210, 26), (-200, 270, 16))):
        cv2.circle(f, (cx + dx, cy + dy), rr, C(PAPER), -1, cv2.LINE_AA); cv2.circle(f, (cx + dx, cy + dy), rr, C(INKC), 5, cv2.LINE_AA)
    pale = clamp((t - t0) / 2.0)
    col = _mix(ACID, (226, 236, 196), pale * 0.7)
    cv2.ellipse(f, (cx, cy + 50), (130, 70), 0, 0, 180, C(col), -1, cv2.LINE_AA)
    cv2.ellipse(f, (cx, cy + 50), (130, 18), 0, 0, 360, C(col), -1, cv2.LINE_AA)
    cv2.ellipse(f, (cx, cy + 50), (130, 70), 0, 0, 180, C(ACID_S), 4, cv2.LINE_AA)
    pour_stream(f, cx - 40, cy - 150, cx + 10, cy + 50, t, w=24, head=ramp(t, t0, 0.35), seed=2)
    write_on(f, "acid", cx + 70, cy + 150, t, t0 + 0.6, 30, ACID_S)


def shot_S0b(t, n):
    f = set_dhaba(t, 9); f = dof(f, 3); t0 = st_("S0b")
    chub_head_only(f, 330, 1270, 3.4, t, mouth="o", expr="wow", brow="up", look=(0.6, 0.4) if t < t0 + 0.8 else (0.4, -0.5), turn=0.2)
    for j in range(3):                                                                                        # water still dripping off his face
        yy = 1000 + 40 * j + ((t - t0) * (90 + 30 * j)) % 260
        cv2.ellipse(f, (int(250 + 120 * j), int(yy)), (11, 15), 0, 0, 360, C(WAT), -1, cv2.LINE_AA); cv2.ellipse(f, (int(250 + 120 * j), int(yy)), (11, 15), 0, 0, 360, C(WAT_S), 2, cv2.LINE_AA)
    thought_stomach(f, 730, 900, t, T("i1", "waters") - 0.1)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="golden")


# ---- S1: 'Every family has that one uncle' : THE UNCLE close, glass held high out of reach, finger wag ----
def shot_S1(t, n):
    f = set_dhaba(t, 8); f = dof(f, 2)
    wag = 12 * math.sin(t * 13)
    uncle(f, 600, 2000, 2.0, t, la=(120 + wag, 150), ra=(150, 175), hand_l="point", hand_r="grip", mouth=1, expr="smirk", brow="sus",
          look=(-0.4, 0), turn=-0.2, lean=wag * 0.12, hold=_rot_el(scale_el(steel_glass_el(0.5), 0.55), 6 * math.sin(t * 2)), hold_off=(-10, -40), hold_front=True)
    kw(f, "THAT ONE UNCLE", 540, 350, t, T("i2", "uncle") - 0.2, "pop", 108, col=INKC)
    return finish(f, n, look="golden")


# ---- S1b: '...who grabs your glass the second you sit down to eat.' wide: the glass vanishes in a flash; 0.5 SEC; NO WATER WITH FOOD! ----
def shot_S1b(t, n):
    f = set_dhaba(t); tg = T("i2", "grabs") - 0.08; tsit = T("i2", "sit") - 0.1
    g = ramp(t, tg, 0.16)
    arm = lerp2((30, 20), (-50, -120), g) if t < tg + 0.3 else lerp2((-50, -120), (150, 175), ramp(t, tg + 0.3, 0.18))
    holding = t > tg + 0.16
    uncle(f, UX, UY, US, t, la=(120, 150) if t > tsit else (30, 20), ra=arm, hand_r="grip", hand_l="point", mouth=2 if t > tsit else 0,
          expr="angry" if t > tsit else "smirk", brow="sus", look=(-1, 0), turn=-0.5,
          **(dict(hold=_rot_el(scale_el(steel_glass_el(0.7), 0.55), 0), hold_off=(-10, -40), hold_front=True) if holding else {}))
    chub(f, CX, CY, CS, t=t, la=(26, 14), ra=(70, 60) if not holding else (100, 140), hand_r="open", mouth="o" if holding else 0,
         expr="wow" if holding else "happy", brow="up", look=(1, -0.2) if holding else (0.3, 0.5), turn=0.3)
    if holding and t < tg + 0.5:
        for j in range(4):                                                                                    # whoosh lines where it was
            cv2.line(f, (int(560 + 40 * j), int(1180 + 18 * j)), (int(700 + 40 * j), int(1100 + 18 * j)), C(INKC), 5, cv2.LINE_AA)
    dhaba_front(f)
    el_at(f, thali_el("full"), 300, 1300, 0.62)
    if not holding: el_at(f, steel_glass_el(0.7), 560, 1250, 0.55)
    if t > T("i2", "second") - 0.1: el_at(f, vstamp_el("0.5 SEC", INKC, 70), 300, 340, 1.0, t, T("i2", "second") - 0.1, rot=-5)
    if t > tsit: kw(f, "NO WATER WITH FOOD!", 540, 500, t, tsit, "shake", 74, col=RED, amp=0.4)
    return finish(f, n, look="golden")


# ---- BOARD stomach (shared by S2-S5) ----
STOM = [(500, 560), (488, 620), (420, 600), (346, 650), (310, 760), (318, 900), (360, 1030), (450, 1120), (580, 1160), (720, 1140), (830, 1080),
        (900, 1010), (960, 985), (1000, 990), (1000, 930), (950, 925), (880, 945), (790, 990), (680, 1000), (590, 960), (548, 880), (560, 760),
        (590, 650), (590, 560)]


def _stom_pts(sw=0.0, cx=600, cy=900, dy=0):
    return [(cx + (x - cx) * (1 + sw), cy + dy + (y - cy) * (1 + sw * 0.8)) for x, y in STOM]


def stomach_board(f, t, k=1.0, level=0.45, col=None, sw=0.0, pipe=True, seed=540, dy=0, pipe_y0=300):
    """the board stomach: a J-shaped outline that draws itself, a food pipe in from the top, an acid pool (filled up to `level`)."""
    P = _stom_pts(sw, dy=dy)
    if level > 0 and k >= 0.999:
        ys = [p[1] for p in P]; y0, y1 = min(ys), max(ys); ly = y1 - (y1 - y0) * level
        m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [np.int32(P)], 255, cv2.LINE_AA); m[: int(ly)] = 0
        a = (m.astype(np.float32) / 255 * 0.9)[..., None]
        f[:] = f * (1 - a) + np.array(C(col or ACID), np.float32) * a
        for j in range(5):                                                                     # acid bubbles
            bx = 380 + 90 * j; by = ly + 30 + ((t * 40 + j * 37) % max(10, (y1 - ly - 50)))
            cv2.circle(f, (int(bx), int(by)), 7, C(ACID_S), 2, cv2.LINE_AA)
    draw_on(f, P, k, BP_INK, 8, seed=seed, tip=k < 1, closed=True)
    if pipe:
        draw_on(f, [(500, pipe_y0), (508, 450 + dy * 0.5), (500, 560 + dy)], k, BP_INK, 8, seed=seed + 1, tip=False)
        draw_on(f, [(590, pipe_y0), (598, 450 + dy * 0.5), (590, 560 + dy)], k, BP_INK, 8, seed=seed + 2, tip=False)
    return P


# ---- S2: 'Funny thing is, your stomach acid is made with water in the first place.' ----
def shot_S2(t, n):
    f = board_bg(); t0 = st_("S2"); tw = T("a1", "made") - 0.1
    k = ramp(t, t0, 0.6)
    stomach_board(f, t, k, level=0.45 * ramp(t, t0 + 0.5, 0.5))
    write_on(f, "stomach acid", 600, 1290, t, T("a1", "acid") - 0.2, 46, ACID_S)
    if t > tw:                                                                             # the RECIPE: acid = WATER + acid
        el_at(f, wdrop_el("happy", (0.3, 0.2)), 330, 420, 0.9, t, tw)
        kw(f, "+", 470, 430, t, tw + 0.15, "pop", 110, col=INKC)
        el_at(f, acid_drop_el(0.9, "n"), 610, 420, 1.0, t, tw + 0.25)
        draw_arrow_on(f, (360, 520), (520, 760), ramp(t, tw + 0.3, 0.3), WAT_S, 7, 26, bend=0.2)
        kw(f, "MADE WITH WATER", 540, 1440, t, T("a1", "water") - 0.1, "breathe", 92, col=WAT_S)
    peek(f, t, 900, 330, 0.42, expr="wow" if t > tw else "smirk", look=(-0.7, 0.3))
    src(f, SRC_MAYO54, t, tw + 0.6, y=1560)
    return finish(f, n, look="fresh")


# ---- S3: 'When food and water stretch your stomach,' food + a water stream pour in; the stomach swells; STRETCH arrows ----
def shot_S3(t, n):
    f = board_bg(); t0 = st_("S3"); tst = T("b1", "stretch") - 0.1
    sw = 0.16 * ramp(t, tst, 0.7)
    stomach_board(f, t, 1.0, level=0.45 + 0.15 * ramp(t, t0, 1.6), sw=sw)
    pour_stream(f, 545, 300, 560, 900, t, w=30, head=ramp(t, T("b1", "water") - 0.1, 0.35), seed=5)
    for j in range(3):                                                                     # food bits falling in (roti pieces)
        v = clamp((t - t0 - 0.1 - 0.25 * j) / 0.7)
        if 0 < v < 1: el_at(f, roti_el(j % 2), 520 + 25 * j, 300 + 560 * v * v, 0.3, rot=90 * v + 40 * j)
    if t > tst:
        ka = ramp(t, tst, 0.3)
        for (a, b) in (((330, 980), (200, 1000)), ((880, 900), (1010, 880)), ((650, 1230), (650, 1350)), ((800, 760), (900, 680))):
            draw_arrow_on(f, a, b, ka, RED, 9, 30)
        kw(f, "STRETCH", 540, 1440, t, tst, "breathe", 120, col=RED)
    write_on(f, "food + water", 300, 360, t, t0 + 0.1, 42, BP_INK)
    return finish(f, n, look="fresh")


# ---- S3b: '...tiny sensor cells notice.' ZOOM INTO THE WALL: three sensor buddies on the stomach wall, dials swing, bells RING on 'notice' ----
def shot_S3b(t, n):
    f = board_bg(); t0 = st_("S3b"); tn = T("b1", "notice.") - 0.1
    z = 1 + 0.08 * ramp(t, t0, 1.5)
    cv2.rectangle(f, (0, 1130), (W, 1330), C((244, 190, 200)), -1)                                         # the wall, magnified
    for x in range(0, W, 90): cv2.ellipse(f, (x + 45, 1130), (45, 22), 0, 180, 360, C((244, 190, 200)), -1, cv2.LINE_AA)
    for x in range(0, W, 90): cv2.ellipse(f, (x + 45, 1130), (45, 22), 0, 180, 360, C(BP_INK), 5, cv2.LINE_AA)
    draw_arrow_on(f, (900, 520), (820, 1080), 1.0, RED, 8, 28)
    write_on(f, "stretch", 900, 470, t, t0, 40, RED)
    ring = t > tn
    for j, x in enumerate((260, 540, 820)):
        nd = 0.2 + 0.6 * ramp(t, t0 + 0.2 * j, 0.9)
        el_at(f, checker_el("wow" if ring else "n", (0.2, -0.3), needle=nd, ring=ring and int(t * 10 + j) % 2 == 0), x, 1000 + 8 * math.sin(t * 6 + j), 1.0 * z, t, t0 + 0.1 * j)
    kw(f, "SENSOR CELLS", 540, 360, t, t0 + 0.1, "pop", 104, col=INKC)
    if ring: kw(f, "NOTICED!", 540, 520, t, tn, "shake", 110, col=ACC_S, amp=0.4)
    return finish(f, n, look="fresh")


# ---- S4: 'They send out a signal called gastrin, and your stomach makes more acid.' sensor -> GASTRIN courier runs -> the ACID TAP opens ----
PATH4 = [(200, 1060), (230, 900), (330, 660), (520, 470), (720, 560)]


def shot_S4(t, n):
    f = board_bg(); t0 = st_("S4"); tg = T("b2", "gastrin,") - 0.15; tm = T("b2", "more") - 0.12
    stomach_board(f, t, 1.0, level=0.42 + 0.22 * ramp(t, tm + 0.2, 1.0), pipe=False)
    for j in range(16):                                                                    # dotted message route
        P, e = _cut_poly(PATH4, j / 15)
        cv2.circle(f, (int(e[0]), int(e[1])), 6, C(BP_GRID2), -1, cv2.LINE_AA)
    el_at(f, checker_el("wow", (0.6, -0.4), needle=0.8, ring=int(t * 10) % 2 == 0), 180, 1240, 0.8)
    v = ramp(t, t0 + 0.1, max(0.4, tm - t0 - 0.3))
    P, e = _cut_poly(PATH4, v)
    hop = 18 * abs(math.sin(t * 12)) if v < 1 else 0
    el_at(f, courier_el("happy", (1, 0)), e[0], e[1] - 60 - hop, 0.8, rot=8 * math.sin(t * 12) if v < 1 else 0)
    if t > tg: write_on(f, "gastrin", e[0], e[1] + 40, t, tg, 40, BP_INK)
    ok = ramp(t, tm, 0.25)
    el_at(f, acid_tap_el(ok), 880, 560, 1.0)
    if ok > 0.3:
        pour_stream(f, 955, 630, 740, 1000, t, w=28, col=ACID, rim=ACID_S, head=ramp(t, tm + 0.08, 0.3), seed=9)
    kw(f, "SIGNAL: GASTRIN", 540, 330, t, tg, "pop", 92, col=BP_INK)
    if t > tm: kw(f, "MORE ACID", 540, 1440, t, tm, "shake", 120, col=ACC_S, amp=0.35)
    return finish(f, n, look="fresh")


# ---- S5: 'Water it down a bit? Same alarm, more acid, and it's back to normal.' THE SOURNESS DIAL (a thermostat) ----
def dial(f, cx, cy, R, v, t):
    """a big half-dial: WEAK (pale, left) .. NORMAL (lime band, right); needle at v 0..1."""
    for j in range(24):
        a0 = 180 + 180 * j / 24; a1 = 180 + 180 * (j + 1) / 24
        col = _mix((226, 236, 196), ACID, j / 23)
        cv2.ellipse(f, (cx, cy), (R, R), 0, a0, a1 + 0.5, C(col), 40, cv2.LINE_AA)
    cv2.ellipse(f, (cx, cy), (R + 22, R + 22), 0, 180, 360, C(BP_INK), 5, cv2.LINE_AA)
    cv2.ellipse(f, (cx, cy), (R - 22, R - 22), 0, 180, 360, C(BP_INK), 5, cv2.LINE_AA)
    write_on(f, "weak", cx - R + 20, cy + 50, t, -9, 34, BP_INK); write_on(f, "normal", cx + R - 30, cy + 50, t, -9, 34, ACID_S)
    a = math.pi + math.pi * (0.1 + 0.8 * v)
    cv2.line(f, (cx, cy), (int(cx + (R - 10) * math.cos(a)), int(cy + (R - 10) * math.sin(a))), C(RED), 12, cv2.LINE_AA)
    cv2.circle(f, (cx, cy), 18, C(INKC), -1, cv2.LINE_AA)


def shot_S5(t, n):
    f = board_bg(); t0 = st_("S5"); tw = T("b3", "Water") - 0.1; ta = T("b3", "alarm,") - 0.12; tm = T("b3", "more") - 0.1; tn = T("b3", "normal.") - 0.12
    weak = ramp(t, tw + 0.2, 0.8); back = ramp(t, tm + 0.1, max(0.3, tn - tm - 0.1))
    v = 0.85 - 0.65 * weak + 0.65 * back
    pale = clamp(weak - back)
    stomach_board(f, t, 1.0, level=0.5 + 0.1 * weak + 0.08 * back, col=_mix(ACID, (226, 236, 196), pale * 0.8), pipe=True, dy=170, pipe_y0=560)
    dial(f, 540, 470, 180, v + 0.02 * math.sin(t * 9) * (1 - back), t)
    if t < tm + 0.4: pour_stream(f, 545, 560, 560, 1060, t, w=26, head=ramp(t, tw, 0.3), tail=ramp(t, tm, 0.4), seed=11)
    if t > ta: el_at(f, checker_el("wow", (0.6, -0.4), needle=0.9, ring=int(t * 10) % 2 == 0), 190, 1250, 0.75, t, ta)
    if t > tm:
        el_at(f, acid_tap_el(1.0), 900, 860, 0.9)
        pour_stream(f, 968, 922, 760, 1150, t, w=24, col=ACID, rim=ACID_S, head=ramp(t, tm, 0.3), seed=12)
    if t < ta: kw(f, "WATERED DOWN?", 540, 1440, t, tw, "pop", 96, col=WAT_S)
    elif t < tn: kw(f, "SAME ALARM", 540, 1440, t, ta, "shake", 100, col=RED, amp=0.35)
    else:
        kw(f, "BACK TO NORMAL", 540, 1440, t, tn, "pop", 100, col=ACC_S)
        draw_on(f, [(780, 520), (810, 550), (860, 480)], ramp(t, tn, 0.2), (40, 140, 80), 12, seed=55, tip=False)
    src(f, SRC_PHYS54, t, t0 + 0.6, y=1560)
    return finish(f, n, look="fresh")


# ---- S6: 'That's why the Mayo Clinic says water doesn't thin your digestive juices.' the DOCTOR at the dhaba drinks with his meal; the uncle's jaw drops ----
def doctor(f, x, y, s, t, sip=0.0):
    ra = (150 - 70 * (1 - sip), -128 + 150 * (1 - sip))
    chub(f, x, y, s, t=t, shirt=(246, 248, 250), la=(26, 14), ra=ra, hand_r="grip", hold=_rot_el(scale_el(steel_glass_el(0.7), 0.55), 32 * sip),
         hold_off=(-38 * sip - 6 * (1 - sip), -18 * sip - 24 * (1 - sip)), hold_front=True, mouth=0 if sip > 0.5 else talk(t), expr="happy", brow="up",
         look=(-0.6, 0), turn=-0.4)
    hx_ = x - 2 * s; cy_ = y - 320 * s
    cv2.ellipse(f, (int(hx_), int(cy_ - 40 * s / 1.5)), (int(70 * s / 1.5), int(60 * s / 1.5)), 0, 0, 180, C((70, 76, 90)), 8, cv2.LINE_AA)
    cv2.circle(f, (int(hx_ + 40 * s / 1.5), int(cy_ + 40 * s / 1.5)), int(16 * s / 1.5), C((180, 186, 196)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx_ + 40 * s / 1.5), int(cy_ + 40 * s / 1.5)), int(16 * s / 1.5), C(INKC), 4, cv2.LINE_AA)
    hx2, hy2 = x - 0.4 * 14 * s, y - 420 * s                                                       # head mirror = 'doctor' at a glance
    cv2.line(f, (int(hx2 - 96 * s), int(hy2 - 62 * s)), (int(hx2 + 96 * s), int(hy2 - 62 * s)), C(INKC), max(3, int(8 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(30 * s), C((214, 222, 230)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(30 * s), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(9 * s), C(INKC), -1, cv2.LINE_AA)


def shot_S6(t, n):
    f = set_dhaba(t); t0 = st_("S6"); tth = T("c1", "thin") - 0.12
    uncle(f, 810, 1790, 1.6, t, la=(30, 20), ra=(30, 20), mouth="jaw" if t > tth else 0, expr="wow" if t > tth else "sus", brow="up", look=(-1, 0), turn=-0.5)
    sip = clamp(math.sin((t - t0 - 0.6) * 1.6)) if t > t0 + 0.6 else 0.0
    doctor(f, 400, 1800, 1.75, t, sip=sip)
    dhaba_front(f)
    el_at(f, thali_el("full"), 420, 1300, 0.6)
    hook_band(f, 250, 680)
    kw(f, "MAYO CLINIC:", 540, 320, t, t0 + 0.05, "pop", 80, col=INKC)
    if t > tth - 0.2:
        kw(f, "WATER DOESN'T", 540, 440, t, tth - 0.2, "pop", 80, col=WAT_S)
    if t > tth:
        kw(f, "THIN IT", 540, 580, t, tth, "shake", 124, col=ACC_S, amp=0.3)
        el_at(f, vstamp_el("MYTH", RED, 90), 870, 760, 1.0, t, tth + 0.3, rot=8)
    src(f, SRC_MAYO54, t, t0 + 0.5)
    return finish(f, n, look="golden")


# ---- S7: 'Just sip it.' calm close-up sip ----
def drinker(f, t, x=CX, y=CY, s=CS, sip=1.0, level=0.6, expr="happy", brow="n", look=(0.3, -0.3), mouth=None):
    ra = (150 - 70 * (1 - sip), -128 + 150 * (1 - sip))
    gl = _rot_el(scale_el(steel_glass_el(level), 0.62), 32 * sip)
    chub(f, x, y, s, t=t, la=(26, 14), ra=ra, hold=gl, hold_off=(-38 * sip - 6 * (1 - sip), -18 * sip - 24 * (1 - sip)), hold_front=True, hand_r="grip",
         mouth=(mouth if mouth is not None else (0 if sip > 0.5 else talk(t))), expr=expr, brow=brow, look=look, turn=0.3)


def shot_S7(t, n):
    f = set_dhaba(t, 9); f = dof(f, 2); t0 = st_("S7")
    sip = ramp(t, t0 + 0.1, 0.35)
    drinker(f, t, x=470, y=2150, s=2.3, sip=sip, expr="happy", look=(0.3, -0.4))
    kw(f, "SIP", 540, 420, t, T("c2", "sip") - 0.1, "breathe", 170, col=WAT_S)
    return finish(f, n, look="golden")


# ---- S7b: 'Chugging a whole bottle can leave you feeling bloated.' standing, the big jug tipped over his mouth (the stream pours IN); the belly swells ----
def rot_pt(dx, dy, ang):
    """where an offset (dx, dy) from an element's centre lands after rot_comp / _rot_el by ang degrees (cv2: + = counter-clockwise on screen)."""
    a = math.radians(ang); return dx * math.cos(a) + dy * math.sin(a), -dx * math.sin(a) + dy * math.cos(a)


JUG_SPOUT = (-80, -110); JUG_HANDLE = (110, 20)          # offsets from the centre of jug54_el (240 x 300)


def jug_in_hand(f, hx, hy, s, ang):
    """draw jug54_el so its HANDLE sits in the hand at (hx, hy); returns the spout tip."""
    ox, oy = rot_pt(JUG_HANDLE[0] * s, JUG_HANDLE[1] * s, ang)
    cx, cy = hx - ox, hy - oy
    rot_comp(f, scale_el(jug54_el(), s), cx, cy, ang)
    sx, sy = rot_pt(JUG_SPOUT[0] * s, JUG_SPOUT[1] * s, ang)
    return cx + sx, cy + sy


def floor54(f, y0=1330):
    """the dhaba floor (worn stone slabs) for full-body shots without the table."""
    cv2.rectangle(f, (0, y0), (W, H), C((200, 176, 140)), -1)
    for x in range(-200, W + 200, 180): cv2.line(f, (x, y0), (int(540 + (x - 540) * 2.0), H), C((170, 146, 112)), 4, cv2.LINE_AA)
    for y in (y0 + 70, y0 + 170, y0 + 320): cv2.line(f, (0, y), (W, y), C((170, 146, 112)), 4, cv2.LINE_AA)
    cv2.line(f, (0, y0), (W, y0), C(INKC), 6, cv2.LINE_AA)


def shot_S7b(t, n):
    f = set_dhaba(t); floor54(f); t0 = st_("S7b"); tb = T("c2", "bloated.") - 0.12
    chug = t < tb - 0.15
    bl = ramp(t, t0 + 0.3, max(0.4, tb - t0 - 0.3))
    x, y, s = 520, 1560, 1.35
    hx, hy = x, y - 420 * s
    if chug:
        ra = (178, 178)
        chub(f, x, y, s, t=t, la=(60, 90), ra=ra, hand_l="open", hand_r="grip", mouth="o", expr="gross" if bl > 0.75 else "n",
             brow="up", look=(0.3, -1), turn=0.1, lean=-4, squash=-0.04 * bl)
        gx, gy = hand_xy(x, y, s, ra, 1, -4)
        sp = jug_in_hand(f, gx, gy, 0.9, 60 + 4 * math.sin(t * 8))
        pour_stream(f, sp[0], sp[1], hx + 6 * s, hy + 56 * s, t, w=18, head=ramp(t, t0 + 0.1, 0.2), seed=31, land=False)
        for j in range(3):                                                                          # glug marks at the throat
            r = int((20 + 18 * ((t * 2.2 + j * 0.33) % 1)) * s)
            cv2.ellipse(f, (int(hx + 70 * s), int(hy + 120 * s)), (r, int(r * 0.6)), 0, 200, 340, C(WAT_S), max(2, int(4 * s)), cv2.LINE_AA)
    else:
        chub(f, x, y, s, t=t, la=(40, 70), ra=(30, 60), hand_l="open", hand_r="open", mouth=0, expr="gross", brow="sad", look=(0.2, 0.6), turn=0.0, lean=-8)
        el_at(f, jug54_el(), 860, 1290, 0.8, rot=80)
    bx, by = x + 6, y - 250 * s
    rr = 95 + 70 * bl + (6 * math.sin(t * 20) if not chug else 0)
    cv2.ellipse(f, (int(bx), int(by)), (int(rr), int(rr * 0.95)), 0, 0, 360, C(INK_MINT), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(bx), int(by)), (int(rr), int(rr * 0.95)), 0, 0, 360, C(INKC), 7, cv2.LINE_AA)
    cv2.ellipse(f, (int(bx - rr * 0.35), int(by - rr * 0.4)), (int(rr * 0.25), int(rr * 0.12)), -30, 0, 360, C((236, 250, 240)), -1, cv2.LINE_AA)
    if not chug:
        for j in range(3):                                                                          # slosh marks
            cv2.ellipse(f, (int(bx + rr + 30), int(by - 40 + 40 * j)), (24, 12), 0, 200, 340, C(WAT_S), 5, cv2.LINE_AA)
    kw(f, "A WHOLE BOTTLE?", 540, 340, t, t0 + 0.05, "pop", 92, col=INKC)
    if t > tb: kw(f, "BLOATED", 540, 500, t, tb, "breathe", 140, col=WAT_S)
    src(f, SRC_BLOAT54, t, t0 + 0.6)
    return finish(f, n, look="golden")


# ---- S8: 'Send this to the uncle with the glass.' ----
def shot_S8(t, n):
    f = set_dhaba(t)
    uncle(f, UX, UY, US, t, la=(30, 20), ra=(150, 175), hand_r="grip", mouth=0, expr="sus", brow="sus", look=(-1, 0), turn=-0.5,
          hold=_rot_el(scale_el(steel_glass_el(0.6), 0.55), 4 * math.sin(t * 2)), hold_off=(-10, -40), hold_front=True)
    chub(f, CX, CY, CS, t=t, la=(26, 14), ra=(72, 42), hand_r="point", mouth=talk(t), expr="smirk", brow="up", look=(1, -0.2), turn=0.4)
    dhaba_front(f)
    el_at(f, thali_el("full"), 300, 1300, 0.62)
    hook_band(f, 250, 560)
    ui_word(f, "send this to the uncle with the", "[GLASS]", 420, t, T("c3", "Send") - 0.05, col=INKC, acc=WAT_S, size=130, lead_col=INKC)
    return finish(f, n, look="golden")


# ---- S8b: 'Then pour yourself one.' the POUR close-up: Chubby tips the jug, the stream narrows as it falls, the glass fills with a small landing splash ----
def shot_S8b(t, n):
    f = set_dhaba(t, 9); f = dof(f, 2); t0 = st_("S8b")
    head = ramp(t, t0 + 0.2, 0.25); lvl = clamp((t - t0 - 0.4) / 1.3)
    x, y, s = 760, 1750, 1.9
    la = (172, 170)
    chub(f, x, y, s, t=t, la=la, ra=(26, 14), hand_l="grip", mouth=talk(t), expr="happy", brow="up", look=(-1, 0.6), turn=-0.4)
    dhaba_front(f, 1500)
    gx, gy = 360, 1383
    el_at(f, steel_glass_el(0.15 + 0.7 * lvl), gx, gy, 0.9)
    hx, hy = hand_xy(x, y, s, la, -1)
    sp = jug_in_hand(f, hx, hy, 1.15, 80 * ramp(t, t0, 0.25))
    surf = gy - 95 + 110 * (1 - lvl)
    if t > t0 + 0.2: pour_stream(f, sp[0], sp[1], gx + 6, surf, t, w=30, head=head, seed=21)
    kw(f, "POUR YOURSELF ONE", 540, 380, t, T("c3", "pour") - 0.1, "pop", 92, col=WAT_S)
    return finish(f, n, look="golden")


# ---- S10: the logo beat (0.6 s) ----
def shot_S10(t, n):
    t0 = st_("S10"); f = set_dhaba(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.25) * 0.95)
    comp(f, ed_el("follow for more food facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.12) / 0.2))
    return finish(f, n, look="warm")


# ---- S11: the LOOP TAIL: replays the run-up to frame 0 so the seam lands on the same pose ----
def shot_S11(t, n):
    f = set_dhaba(t)
    scene0(f, t - END)
    hook_band(f)
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i2", "grabs") - 0.08, 0.3, 12), (T("i2", "sit") - 0.1, 0.3, 10), (T("a1", "water") - 0.1, 0.35, 12),
           (T("b1", "stretch") - 0.1, 0.3, 10), (T("b1", "notice.") - 0.1, 0.3, 12), (T("b2", "more") - 0.12, 0.35, 14),
           (T("b3", "alarm,") - 0.12, 0.3, 10), (T("b3", "normal.") - 0.12, 0.3, 10), (T("c1", "thin") - 0.12, 0.35, 14),
           (T("c2", "bloated.") - 0.12, 0.3, 10), (T("c3", "glass.") - 0.1, 0.3, 10)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


_FIRST = {}


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); k = sh["trans"]; dt = t - sh["start"]
    if i > 0:
        if k == "erase" and dt < 0.42:
            f = erase_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42)
        elif k == "morph" and dt < 0.42:
            a, b = MORPH[sh["id"]]; f = morph_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42, a, b)
        elif k == "whip" and dt < 0.22:
            p = 1 - dt / 0.22; M = np.float32([[1, 0, -360 * p * p], [0, 1, 0]])
            f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
        elif k == "flash" and dt < 0.14: f = f + 0.8 * (1 - dt / 0.14) ** 1.5
        elif k == "punch" and dt < 0.16: f = cam(f, 1 + 0.08 * (1 - dt / 0.16)) + 0.12 * (1 - dt / 0.16)
    nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    if nx is not None and nx["trans"] == "whip" and sh["end"] - t < 0.14:
        p = 1 - (sh["end"] - t) / 0.14; M = np.float32([[1, 0, 360 * p * p], [0, 1, 0]])
        f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
    if i == len(SHOTS) - 1:
        if "f0" not in _FIRST: _FIRST["f0"] = rs(SHOTS[0]["id"], 0.0, 0)
        f = loop_seam(f, _FIRST["f0"], t, END, 0.33)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
