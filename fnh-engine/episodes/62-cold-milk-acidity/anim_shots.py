# ================= shots: FreshNestHub 62 — "Does cold milk cure acidity?" (Chubby INK; 35-50 s rule; ONE takeaway) =================
# COLOUR SCRIPT: the night BEDROOM (indigo wall, one warm bedside lamp) = the burn and the home fix; Chubby's chest flames are the only hot colour.
# The white BOARD (blue ink + burn orange) for every explanation: the stomach with its acid pool, milk calming it, the CLOCK WIPE ('a little later'),
# the protein sensor + the acid tap, the 1976 test, the valve. A warm 1970s room (sepia) for the doctors. Back to the bedroom for the send line + loop.
# ONE accent = BURN ORANGE. Milk = cream + frost blue.
# Story: frame 0 = Chubby sitting up in bed at night, gulping cold milk, little flames licking up from his chest -> the question. Mom swears by it
# (she holds up the glass). For a few minutes: the flames shrink, a relieved exhale. Board: milk isn't acidic -> the burn calms. CLOCK WIPE: a
# little later the stomach notices the protein (a sensor rings) -> the acid tap opens -> MORE acid -> bedroom: the burn comes back (a take).
# 1976: doctors tested whole, low-fat and skim milk -> all three raised acid. Board: fat loosens the valve, acid sneaks up the pipe -> a burp puff.
# Tip: more than twice a week -> a doctor, not milk. Send line = whoever keeps cold milk by the bed; the tail rebuilds frame 0.
END = round(LINES["c2"]["end"] + 0.9, 3)               # 0.05 s air + 0.4 s logo + 0.45 s loop tail
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "really") - 0.12, "punch"),
    ("S1", T("i2", "Your") - 0.12, "whip"), ("S1b", T("i2", "for") - 0.1, "cut"),
    ("S2", T("i3", "Milk") - 0.1, "erase"),
    ("S3", T("a1", "But") - 0.1, "clock"), ("S3b", T("a1", "makes") - 0.1, "cut"), ("S3c", T("a1", "digest") - 0.1, "punch"),
    ("S4", T("a2", "Doctors") - 0.12, "flash"), ("S4b", T("a2", "Whole") - 0.1, "erase"), ("S4c", T("a2", "All") - 0.1, "punch"),
    ("S5", T("b1", "And") - 0.1, "erase"), ("S5b", T("b1", "keeps") - 0.1, "cut"),
    ("S6", T("c1", "If") - 0.1, "whip"), ("S6b", T("c1", "that's") - 0.1, "cut"),
    ("S7", T("c2", "Send") - 0.1, "whip"), ("S7b", T("c2", "by") - 0.1, "punch"),
    ("S8", LINES["c2"]["end"] + 0.05, "punch"), ("S9", round(LINES["c2"]["end"] + 0.45, 3), "cut"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
MORPH = {}
CLOCK = {"S3": (540, 1000)}
CLOCK_D = 0.6
_write_on0 = write_on


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
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


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None, blink=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look,
                   turn=clamp(look[0]) * 0.5, blink=blink)


def hook_band(f, y0=228, y1=700, a=0.72, col=None):
    if a <= 0: return
    m = np.zeros((H, 1), np.float32); m[y0:y1] = a
    m = cv2.GaussianBlur(np.repeat(m, 4, 1), (1, 61), 0)[:, :1, None]
    f[:] = f * (1 - m) + np.array(C(col or PAPER), np.float32) * m


def hook_words(f, t, t0=-1.0, op=1.0):
    kw(f, "DO YOU KNOW IF", 540, 300, t, t0, "pop", 70, col=INKC, op=op)
    kw(f, "COLD MILK", 540, 425, t, t0, "shiver", 110, col=FROST_S, op=op)
    kw(f, "CURES ACIDITY?", 540, 580, t, t0, "shake", 104, col=ACC_S, amp=0.25, op=op)


def nolean(d): return {k: v for k, v in d.items() if k != "lean"}


def hand_xy(x, y, s, arm, side, lean=0.0):
    a1, a2 = arm; bcx = x + 40 * s * math.sin(math.radians(lean)); bcy = y - 222 * s
    sx, sy = bcx + side * 118 * s, bcy - 46 * s
    ex, ey = sx + side * math.sin(math.radians(a1)) * 76 * s, sy + math.cos(math.radians(a1)) * 76 * s
    return ex + side * math.sin(math.radians(a2)) * 70 * s, ey + math.cos(math.radians(a2)) * 70 * s


def glasses(f, x, y, s, lean=0.0, turn=0.0):
    hx = x + lean * 2 * s + turn * 14 * s; hy = y - 420 * s - 6 * s
    for sg in (-1, 1):
        cv2.circle(f, (int(hx + sg * 34 * s), int(hy)), int(26 * s), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.line(f, (int(hx - 8 * s), int(hy)), (int(hx + 8 * s), int(hy)), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)


def doc(f, x, y, s, t, **k):
    """a doctor: white coat (shirt) + round glasses + a stethoscope."""
    k.setdefault("mouth", talk(t))
    chub(f, x, y, s, t=t, shirt=COAT, **k)
    glasses(f, x, y, s, k.get("lean", 0.0), k.get("turn", 0.0))
    hx_ = x - 2 * s; cy_ = y - 320 * s
    cv2.ellipse(f, (int(hx_), int(cy_ - 26 * s)), (int(46 * s), int(40 * s)), 0, 0, 180, C((70, 76, 90)), max(3, int(6 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx_ + 30 * s), int(cy_ + 26 * s)), int(11 * s), C((180, 186, 196)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx_ + 30 * s), int(cy_ + 26 * s)), int(11 * s), C(INKC), max(2, int(3 * s)), cv2.LINE_AA)


# ---- Chubby IN BED: sitting up behind the quilt; the chest point for the heartburn flames ----
BX, BY, BS = 440, 1700, 1.6


def chest_xy(x=BX, y=BY, s=BS, lean=0.0): return x + 40 * s * math.sin(math.radians(lean)) - 10 * s, y - 300 * s


def bed_chub(f, t, sip=0.0, x=BX, y=BY, s=BS, level=0.7, burn=0.0, expr="n", brow="n", look=(0.3, -0.2), mouth=None, lean=0.0, la=(26, 14),
             hand_l="open", squash=0.0, hair=(0, 0), dy=0.0, blink=None, ra=None, hold=True, gulp_t=None):
    """Chubby sitting up in bed. sip 1 = the cold glass tipped at his mouth (gulping), 0 = held at the chest, hold=False = no glass.
    burn 0..1 = heartburn flames from his chest (drawn AFTER him)."""
    gb = 0.0
    if gulp_t is not None and sip > 0.5: gb = 6 * max(0.0, math.sin((t - gulp_t) * 2 * math.pi / 0.55))
    kw_ = dict(la=la, hand_l=hand_l, mouth=(mouth if mouth is not None else (0 if sip > 0.5 else talk(t))), expr=expr, brow=brow, look=look,
               turn=0.3, lean=lean, squash=squash + 0.02 * gb / 6, hair=hair)
    if blink is not None: kw_["blink"] = blink
    if hold:
        rr = ra or (150 - 70 * (1 - sip), -128 + 150 * (1 - sip))
        gl = _rot_el(scale_el(milk_glass_el(level, 1.0), 0.6), 32 * sip)
        chub(f, x, y - gb + dy, s, t=t, ra=rr, hold=gl, hold_off=(-26 * sip - 6 * (1 - sip), 44 * sip - 24 * (1 - sip)), hold_front=True, hand_r="grip", **kw_)
    else:
        chub(f, x, y - gb + dy, s, t=t, ra=ra or (26, 14), **kw_)
    if burn > 0.01:
        cx, cy = chest_xy(x, y + dy, s, lean)
        heartburn(f, cx, cy, s * 0.85, t, burn, n=5, spread=58)


def bedroom(f, t, glass_on_table=False, lamp=1.0, **k):
    bed_chub(f, t, **k)
    bed_front(f, BED_TOP, t, glass=glass_on_table)


# ---- S0: HOOK at frame 0: night bedroom, Chubby sitting up in bed mid-gulp of COLD milk, flames licking up his chest ----
def scene0(f, t):
    bedroom(f, t, sip=1.0, level=0.55, burn=0.9, expr="sad", brow="sad", look=(0.2, -0.5), gulp_t=0.0)


def shot_S0(t, n):
    f = set_bedroom(t)
    scene0(f, t)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="night")


# ---- S0b: '...really cure acidity?' close-up: wincing, a hand on his chest, the flames lick at his chin ----
def shot_S0b(t, n):
    f = set_bedroom(t); f = dof(f, 5); t0 = st_("S0b")
    chub(f, 560, 2240, 2.6, t=t, la=(30, -60), hand_l="open", ra=(24, 12), mouth="ve", expr="gross", brow="sad", look=(0, -0.2), lean=-3)
    heartburn(f, 540, 1540, 1.25, t, 1.0, n=5, spread=70)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="night")


# ---- S1: 'Your mom swears by it,' mom close holding up a glass of cold milk, nodding ----
def shot_S1(t, n):
    f = set_bedroom(t); f = dof(f, 6); t0 = st_("S1"); ts = T("i2", "swears") - 0.1
    nod = 6 * math.sin(max(0.0, t - ts) * 9) if t > ts else 0.0
    mom58(f, 560, 2150, 2.3, t, la=(24, 12), ra=(150, -150), hand_r="grip", mouth=talk(t), expr="happy", brow="up", look=(0, 0.1), lean=nod)
    hx, hy = hand_xy(560, 2150, 2.3, (150, -150), 1, nod)
    el_at(f, milk_glass_el(0.85, 1.0), hx - 6, hy - 120, 0.95)
    grip_hand(f, hx, hy - 40, 2.3 * 0.9)
    hook_band(f, 250, 560, 0.75)
    kw(f, "MOM SWEARS", 540, 320, t, t0 + 0.05, "pop", 110, col=INKC)
    if t > ts: kw(f, "BY IT", 540, 460, t, ts + 0.1, "pop", 110, col=FROST_S)
    return finish(f, n, look="warm")


# ---- S1b: '...and for a few minutes, it kind of works.' a gulp, then the flames shrink + a relieved exhale; a clock ticks in the corner ----
def shot_S1b(t, n):
    f = set_bedroom(t); t0 = st_("S1b"); tw = T("i2", "works.") - 0.1
    calm = ramp(t, t0 + 0.4, 1.0)
    sip = 1.0 - snap(t, t0 + 0.7, 5) if t > t0 + 0.7 else 1.0
    happy = t > t0 + 0.9
    bedroom(f, t, sip=sip, level=0.45, burn=0.9 * (1 - calm) + 0.08, expr="happy" if happy else "sad", brow="up" if happy else "sad",
            mouth="o" if happy and t < tw else (0 if sip > 0.5 else talk(t)), look=(0, -0.2), blink=happy and t < tw - 0.3, gulp_t=t0)
    if happy: kin_word(f, "AHHH", 600, 800, t, t0 + 0.9, "breathe", 90, col=FROST_S, stroke=2, stroke_col=INKC)
    clock_icon(f, 900, 760, 70, t, spin=(t - t0) * 0.5)
    hook_band(f, 250, 600, 0.75)
    kw(f, "FOR A FEW MINUTES...", 540, 320, t, t0 + 0.05, "pop", 74, col=INKC)
    if t > tw: kw(f, "IT KIND OF WORKS", 540, 460, t, tw, "pop", 84, col=OKG)
    return finish(f, n, look="night")


# ---- the BOARD stomach (shared by S2 / S3 / S3b / S5): stomach + pipe; acid pool with flames ----
SDY = 180


def board_gut(f, t, k=1.0, level=0.45, burn=1.0, milk=0.0, valve=0.0, acid_up=0.0):
    P = board_stomach(f, t, k=k, dy=SDY)
    if k < 0.999: return P, 1200
    sy = acid_pool(f, P, level, t, burn=0.0)
    if milk > 0.01:                                                                             # a cream milk layer on top of the acid
        mh = 46 * milk
        m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [np.int32(P)], 255, cv2.LINE_AA)
        yy = np.arange(H)[:, None]; xx = np.arange(W)[None, :]
        surf = sy + 8 * np.sin(xx / 46 + t * 3.0)
        band = (m > 0) & (yy >= surf - mh) & (yy < surf + 10)
        a = band.astype(np.float32)[..., None] * 0.92
        f[:] = f * (1 - a) + np.array(C(MILK), np.float32) * a
    if burn > 0.02:
        xs = [p[0] for p in P]; x0, x1 = min(xs) + 60, max(xs) - 160
        for i in range(4):
            px = x0 + (i + 0.5) * (x1 - x0) / 4
            heartburn(f, px, sy - (46 * milk if milk > 0.01 else 0) + 8, 0.9, t, burn, seed=i * 3, n=3, spread=34)
    draw_on(f, [(540 + (x - 600) + 0, 860 + (y - 860) + SDY) for x, y in STOM], 1.0, BP_INK, 8, seed=600, tip=False, closed=True)
    board_pipe(f, t, k=1.0, open_=valve, acid_up=acid_up, y_top=560, y_val=560 + SDY)
    return P, sy


# ---- S2: 'Milk isn't acidic, so it calms the burn for a bit.' milk pours down the pipe onto the burning acid; the flames shrink ----
def shot_S2(t, n):
    f = board_bg(); t0 = st_("S2"); tc = T("i3", "calms") - 0.1
    kk = ramp(t, t0, 0.5)
    pour = ramp(t, t0 + 0.45, 0.3) * (1 - ramp(t, tc + 0.6, 0.3))
    milk = ramp(t, t0 + 0.7, 1.2)
    calm = ramp(t, tc, 0.8)
    P, sy = board_gut(f, t, k=kk, burn=1.0 - 0.85 * calm, milk=milk)
    if pour > 0.01 and kk >= 1: pour_stream(f, 545, 560, 545, sy - 40, t, w=26, col=MILK, rim=MILK_S, head=pour, seed=2)
    el_at(f, milk_glass_el(0.6, 1.0), 610, 500, 0.5, t, t0 + 0.1, rot=140)
    if t > T("i3", "acidic,") - 0.1: label_at(f, "MILK: NOT ACIDIC", 820, 700, t, T("i3", "acidic,") - 0.1, 600, 640, size=30)
    peek(f, t, 190, 1380, 0.8, expr="happy", look=(0.5, -0.3))
    kw(f, "MILK ISN'T ACIDIC", 540, 320, t, t0 + 0.05, "pop", 80, col=BP_INK)
    if t > tc: kw(f, "CALMS THE BURN", 540, 450, t, tc, "pop", 92, col=OKG)
    if t > T("i3", "bit.") - 0.1: write_on(f, "...for a bit", 800, 1420, t, T("i3", "bit.") - 0.1, 40, BP_INK, cps=26)
    src(f, SRC_TEMP, t, t0 + 0.4, y=1490)
    return finish(f, n, look="fresh")


def protein62_el(mood="n", look=(0, 0), seed=627):
    """a milk PROTEIN bead (cream, with a face) - the thing the stomach 'notices'."""
    def mk():
        w, h = 110, 110; im, d, S = _cv(w, h)
        _ink_ell(d, 55, 56, 40, 38, (246, 232, 196), seed, INK_W - 1, n=24, amp=2.0)
        _shade(im, lambda q, S_: q.ellipse(S_(15, 18, 95, 94), fill=255), lambda q, S_, c: q.ellipse(S_(50, 30, 110, 110), fill=c), (214, 190, 140), 110)
        d.ellipse(S(30, 30, 44, 42), fill=(255, 255, 255, 210))
        _face(d, S, 55, 58, 0.85, mood, look)
        return _done(im, w, h)
    return gcache(("protein62", mood, look, seed), mk)


SENS = (380, 1060)


# ---- S3 (after the CLOCK WIPE): 'But then your stomach notices all that protein,' protein beads float in, the sensor rings ----
def shot_S3(t, n):
    f = board_bg(); t0 = st_("S3"); tn = T("a1", "notices") - 0.1; tp = T("a1", "protein,") - 0.1
    P, sy = board_gut(f, t, burn=0.15, milk=1.0 - ramp(t, t0 + 0.6, 1.5) * 0.7)
    for i in range(5):
        k = ramp(t, tn + 0.12 * i, 0.6)
        if k > 0:
            x = 600 + 70 * i + 10 * math.sin(t * 3 + i); y = sy - 30 - 40 * math.sin(i * 1.7) + 6 * math.sin(t * 4 + i)
            el_at(f, protein62_el("happy" if i % 2 else "n", (0, 0.5)), x, y, 0.7 * k)
    ring = t > tp
    el_at(f, checker_el("wow" if ring else "n", (1, 0), needle=0.9 if ring else 0.2, ring=ring), SENS[0], SENS[1], 0.75)
    if t > tp: label_at(f, "PROTEIN SPOTTED!", 330, 1420, t, tp + 0.1, SENS[0], SENS[1] + 110, size=30)
    write_on(f, "a little later...", 540, 320, t, t0 + 0.05, 52, BP_INK, cps=30)
    if t > tn: kw(f, "IT NOTICES THE PROTEIN", 540, 450, t, tn, "pop", 70, col=ACC_S)
    return finish(f, n, look="fresh")


# ---- S3b: '...and makes MORE acid to digest it.' the acid tap opens wide, acid pours, the pool rises, the flames roar back ----
TAP = (840, 660)


def shot_S3b(t, n):
    f = board_bg(); t0 = st_("S3b"); tm = T("a1", "more") - 0.05
    op_ = snap(t, t0 + 0.15, 4) if t > t0 + 0.15 else 0.0
    rise = ramp(t, tm, 1.2)
    P, sy = board_gut(f, t, level=0.45 + 0.35 * rise, burn=0.2 + 0.95 * rise, milk=0.3 * (1 - rise))
    if op_ > 0.3: pour_stream(f, TAP[0] + 62, TAP[1] + 50, TAP[0] + 30, sy - 6, t, w=30, col=ACC_L, rim=ACC_S, head=ramp(t, t0 + 0.2, 0.3), seed=5)
    el_at(f, acid_tap_el(op_), TAP[0], TAP[1], 1.0)
    el_at(f, checker_el("wow", (1, -0.3), needle=1.0, ring=True), SENS[0], SENS[1], 0.75)
    kw(f, "AND MAKES", 540, 320, t, t0 + 0.05, "pop", 84, col=BP_INK)
    if t > tm: kw(f, "MORE ACID!", 540, 470, t, tm, "shake", 140, col=ACC_S, amp=0.5)
    return finish(f, n, look="fresh")


# ---- S3c: '...to digest it.' bedroom: the burn is BACK - a cartoon take, a hand to his chest, the flames burst up ----
def shot_S3c(t, n):
    f = set_bedroom(t); t0 = st_("S3c")
    tk = take(t, t0 + 0.05, 1.0)
    bedroom(f, t, sip=0.0, level=0.3, burn=min(1.2, 0.3 + 1.5 * ramp(t, t0 + 0.1, 0.25)), expr=tk["expr"] if t < t0 + 0.6 else "gross",
            brow=tk["brow"], mouth="jaw" if t < t0 + 0.7 else "ve", look=tk["look"], lean=tk["lean"], squash=tk["squash"], dy=tk["dy"],
            la=(40, -70), hand_l="open")
    hook_band(f, 250, 560, 0.75)
    kw(f, "THE BURN IS BACK", 540, 360, t, t0 + 0.1, "shake", 96, col=ACC_S, amp=0.45)
    return finish(f, n, look="night")


# ---- S4: 'Doctors tested this in nineteen seventy-six.' a warm 1970s room: a doctor raises a glass of milk; 1976 snaps in ----
def shot_S4(t, n):
    f = set_room60(t); t0 = st_("S4"); ty = T("a2", "nineteen") - 0.1
    doc(f, 560, 2000, 1.9, t, la=(30, 20), ra=(150, -150), hand_r="grip", expr="sus", brow="sus", look=(0.3, -0.3), turn=0.3)
    hx, hy = hand_xy(560, 2000, 1.9, (150, -150), 1)
    el_at(f, milk_glass_el(0.85, 0.5), hx - 6, hy - 100, 0.8)
    grip_hand(f, hx, hy - 34, 1.9 * 0.9)
    sepia(f, 0.3)
    hook_band(f, 250, 640, 0.78)
    kw(f, "DOCTORS TESTED IT", 540, 320, t, t0 + 0.05, "pop", 84, col=INKC)
    if t > ty: kw(f, "IN 1976", 540, 480, t, ty, "pop", 150, col=ACC_S)
    src(f, SRC_1976, t, t0 + 0.4, y=1462)
    return finish(f, n, look="warm")


# ---- S4b / S4c: board: three cartons (WHOLE / LOW-FAT / SKIM) land on their words, each with an ACID meter that climbs ----
CARTS = [("WHOLE", (70, 120, 200), 220, ("a2", "Whole")), ("LOW-FAT", (60, 150, 110), 540, ("a2", "low-fat,")), ("SKIM", (150, 110, 190), 860, ("a2", "skim."))]


def cartons(f, t, rise=0.0, faces=None):
    for i, (lab, col, x, (lid, wd)) in enumerate(CARTS):
        tl = T(lid, wd) - 0.1
        if t < tl: continue
        k = snap(t, tl, 5)
        el_at(f, meter_el(0.2 + 0.7 * rise), x, 830, 0.9 * k)
        el_at(f, carton_el(lab, col, mood=faces), x, 1220, 0.95 * k)


def shot_S4b(t, n):
    f = board_bg(); t0 = st_("S4b")
    cartons(f, t, rise=0.0)
    kw(f, "WHOLE, LOW-FAT,", 540, 320, t, t0 + 0.05, "pop", 84, col=BP_INK)
    if t > T("a2", "even") - 0.1: kw(f, "EVEN SKIM", 540, 450, t, T("a2", "even") - 0.1, "pop", 96, col=ACC_S)
    src(f, SRC_1976, t, t0 + 0.4, y=1462)
    return finish(f, n, look="fresh")


def shot_S4c(t, n):
    f = board_bg(); t0 = st_("S4c"); tr = T("a2", "raised") - 0.1
    cartons(f, t, rise=ramp(t, tr, 0.6), faces="wow" if t > tr else None)
    kw(f, "ALL OF THEM", 540, 320, t, t0 + 0.05, "pop", 96, col=BP_INK)
    if t > tr: kw(f, "RAISED ACID", 540, 460, t, tr, "shake", 120, col=ACC_S, amp=0.35)
    src(f, SRC_1976, t, t0 + 0.4, y=1462)
    return finish(f, n, look="fresh")


# ---- S5: 'And the fat in full-cream milk loosens the little valve...' board: fat drops drift to the valve, it goes slack, acid climbs ----
def fat_drop(f, x, y, r):
    cv2.circle(f, (int(x), int(y)), int(r), C((252, 226, 140)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), int(r), C(INKC), 4, cv2.LINE_AA)
    cv2.circle(f, (int(x - r * 0.35), int(y - r * 0.35)), max(2, int(r * 0.22)), C((255, 255, 255)), -1, cv2.LINE_AA)


def shot_S5(t, n):
    f = board_bg(); t0 = st_("S5"); tf = T("b1", "fat") - 0.1; tl = T("b1", "loosens") - 0.1
    loose = ramp(t, tl, 0.5); up = ramp(t, tl + 0.5, 1.2)
    P, sy = board_gut(f, t, level=0.6, burn=0.7, valve=loose, acid_up=0.75 * up)
    for i in range(4):
        k = ramp(t, tf + 0.15 * i, 0.9)
        if k > 0:
            x = 545 + (200 + 60 * i) * (1 - k) * (1 if i % 2 else -1) + (1 if i % 2 else -1) * 26 * k; y = 560 + SDY + 40 + 80 * (1 - k) + 10 * math.sin(t * 3 + i)
            fat_drop(f, x, y, 20)
    if t > T("b1", "valve") - 0.1: label_at(f, "THE VALVE", 830, 640, t, T("b1", "valve") - 0.1, 600, 560 + SDY, size=32)
    kw(f, "FAT LOOSENS", 540, 320, t, tf, "pop", 100, col=(196, 150, 40))
    if t > tl: kw(f, "THE VALVE", 540, 450, t, tl, "drop", 96, col=ACC_S, t1=tl + 0.9)
    src(f, SRC_FAT, t, t0 + 0.4, y=1490)
    return finish(f, n, look="fresh")


# ---- S5b: '...that keeps acid down in your stomach.' bedroom: the flames climb to his throat, a small burp puff, hands on his chest ----
def shot_S5b(t, n):
    f = set_bedroom(t); t0 = st_("S5b"); tb = t0 + 0.6
    hc = hic(t, (tb,), 0.6) if "hic" in globals() else dict(dy=0, squash=0, lean=0)
    bedroom(f, t, sip=0.0, hold=False, level=0.3, burn=0.9, expr="gross" if t > tb else "sad", brow="sad", mouth="o" if tb < t < tb + 0.3 else 0,
            look=(0.2, -0.1), la=(40, -70), ra=(40, -70), lean=hc.get("lean", 0.0), squash=hc.get("squash", 0.0), dy=hc.get("dy", 0.0))
    hx, hy = BX + 30, BY - 420 * BS + 80
    burp_puff(f, hx + 40, hy, 1.4, t, tb, 1.0)
    heartburn(f, BX + 20, BY - 360 * BS, BS * 0.45, t, 0.8, n=3, spread=40, seed=7)
    hook_band(f, 250, 560, 0.75)
    kw(f, "ACID SNEAKS UP", 540, 330, t, t0 + 0.05, "sneak", 96, col=ACC_S)
    return finish(f, n, look="night")


# ---- S6: 'If the burn shows up more than twice a week,' board: a week strip; burn marks pop on three days ----
def shot_S6(t, n):
    f = board_bg(); t0 = st_("S6")
    marks = {0: T("c1", "burn") - 0.05, 2: T("c1", "shows") - 0.05, 4: T("c1", "twice") - 0.05}
    week_strip(f, t, marks, y=1020, x0=124, gap=132, size=110)
    peek(f, t, 190, 1350, 0.8, expr="sad", look=(0.6, -0.4))
    kw(f, "BURN MORE THAN", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > T("c1", "twice") - 0.1: kw(f, "2x A WEEK?", 540, 460, t, T("c1", "twice") - 0.1, "shake", 130, col=ACC_S, amp=0.3)
    src(f, SRC_WEEK, t, t0 + 0.4, y=1490)
    return finish(f, n, look="fresh")


# ---- S6b: '...that's a job for a doctor, not for milk.' the doctor points; the milk glass gets a NOT A CURE stamp ----
def shot_S6b(t, n):
    f = board_bg(); t0 = st_("S6b"); td = T("c1", "doctor,") - 0.1; tn = T("c1", "not") - 0.1
    doc(f, 360, 1600, 1.35, t, la=(26, 14), ra=(70, 40), hand_r="point", expr="happy", brow="up", look=(1, 0), turn=0.4)
    el_at(f, milk_glass_el(0.7, 1.0), 800, 1180, 1.0)
    if t > tn: el_at(f, vstamp_el("NOT A CURE", RED, 64), 800, 1230, 1.0, t, tn + 0.1, rot=-10)
    kw(f, "A JOB FOR", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > td: kw(f, "A DOCTOR", 540, 460, t, td, "pop", 130, col=OKG)
    return finish(f, n, look="fresh")


# ---- S7: send line: Chubby in bed points at the glass on the bedside table ----
def shot_S7(t, n):
    f = set_bedroom(t); t0 = st_("S7")
    bedroom(f, t, glass_on_table=True, hold=False, expr="smirk", brow="up", look=(1, 0), ra=(100, 60), la=(26, 14), mouth=talk(t))
    hook_band(f, 250, 640, 0.8)
    ui_word(f, "send this to whoever keeps", "[COLD MILK]", 430, t, t0 + 0.05, col=INKC, acc=ACC_S, size=110, lead_col=INKC)
    return finish(f, n, look="night")


# ---- S7b: '...by the bed for acidity.' push-in on the bedside table: the cold glass sweating under the lamp, Chubby peeking ----
def shot_S7b(t, n):
    f = set_bedroom(t); f = dof(f, 7); t0 = st_("S7b")
    z = 1 + 0.06 * ramp(t, t0, 1.2)
    cv2.rectangle(f, (300, 1300), (1080, H), C((150, 104, 66)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (280, 1270), (1080, 1320), C((170, 120, 78)), -1, cv2.LINE_AA); cv2.rectangle(f, (280, 1270), (1080, 1320), C(INKC), 6, cv2.LINE_AA)
    glow(f, 700, 900, 520, (255, 196, 120), 0.3)
    el_at(f, milk_glass_el(0.8, 1.0), 700, 1130, 1.25)
    peek(f, t, 240, 1250, 0.95, expr="smirk", look=(1, 0), mouth=talk(t))
    hook_band(f, 250, 640, 0.8)
    ui_word(f, "by the bed for", "[ACIDITY]", 430, t, t0 + 0.05, col=INKC, acc=ACC_S, size=120, lead_col=INKC)
    return finish(cam(f, z, 700, 1100), n, look="night")


# ---- S8: the logo beat ----
def shot_S8(t, n):
    t0 = st_("S8"); f = set_bedroom(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.2) * 0.95)
    comp(f, ed_el("follow for more food + health facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.1) / 0.2))
    return finish(f, n, look="warm")


# ---- S9: the LOOP TAIL ----
def shot_S9(t, n):
    f = set_bedroom(t - END)
    scene0(f, t - END)
    hook_band(f)
    return finish(f, n, look="night")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "cure") - 0.1, 0.3, 12), (T("i3", "calms") - 0.1, 0.25, 8), (T("a1", "protein,") - 0.1, 0.25, 8), (T("a1", "more") - 0.05, 0.4, 16),
           (SHOT["S3c"]["start"] + 0.05, 0.35, 14), (T("a2", "nineteen") - 0.1, 0.3, 10), (T("a2", "raised") - 0.1, 0.35, 14),
           (T("b1", "loosens") - 0.1, 0.3, 10), (SHOT["S5b"]["start"] + 0.6, 0.25, 8), (T("c1", "twice") - 0.1, 0.3, 10), (T("c1", "not") - 0.1, 0.3, 10),
           (T("c2", "bed") - 0.1, 0.25, 8)]


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
        elif k == "clock" and dt < CLOCK_D:
            cx, cy = CLOCK.get(sh["id"], (540, 960)); f = clock_wipe(rs(SHOTS[i - 1]["id"], t, n), f, dt / CLOCK_D, cx, cy)
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
