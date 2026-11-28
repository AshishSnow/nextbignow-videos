# ================= shots: FreshNestHub 75 — "Do sweets give you worms?" (Chubby INK; 35-50 s rule; ONE takeaway) =================
# COLOUR SCRIPT: the sunny DINING CORNER (mint + warm sun, the steel laddoo tin = the belief) for the myth + the send line; the white BOARD (blue ink +
# berry magenta) for every explanation (the laddoo that makes no worm, the tiny egg in a magnifier, the person -> poop, the three rides, the route map);
# the noon BACKYARD (lime wall, hand-pump, bare soil) = where the worm eggs really live, and where the fix happens (the pump, the chappals).
# ONE accent = BERRY MAGENTA (the eggs + the route).
# NEW CRAFT = THE EYELINE MATCH + THE INSERT: S4 Chubby lifts his muddy hands and LOOKS DOWN at them (held 8 frames) -> S4b = what he sees, from his eyes
# (POV insert: the hands rise from the bottom edge, same noon light, slow push-in to the eggs hitching a ride); S5 he looks down at his bare feet -> S5b the
# foot insert where a larva wriggles to the heel (he jerks it up = the reaction); the opening insert (the hand pulling a laddoo out of the tin, cut in
# mid-action) and the chappal insert at the end are the same tool.
END = round(LINES["c2"]["end"] + 0.9, 3)     # 0.05 s air + 0.4 s logo + 0.45 s loop tail
LOOK_T = T("a3", "hitch") + 0.25              # S4: the look down starts here; the cut comes 8 frames after it settles
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "sweets") - 0.45, "cut"), ("S0c", T("i1", "gives") - 0.05, "cut"),
    ("S1", T("i2", "Nope.") - 0.1, "punch"), ("S1b", T("i2", "No") - 0.1, "erase"),
    ("S2", T("a1", "Worms") - 0.1, "whip"), ("S2b", T("a1", "those") - 0.1, "erase"),
    ("S3", T("a2", "If") - 0.1, "flash"), ("S3b", T("a2", "where") - 0.1, "erase"),
    ("S4", T("a3", "Then") - 0.1, "cut"), ("S4b", round(LOOK_T + 0.28 + 8 / 24, 3), "cut"), ("S4c", T("a3", "on", 1) - 0.1, "erase"),
    ("S5", T("a4", "And") - 0.1, "whip"), ("S5b", T("a4", "It") - 0.1, "cut"),
    ("S6", T("a5", "So") - 0.1, "punch"), ("S6b", T("a5", "Sugar") - 0.1, "cut"),
    ("S7", T("c1", "Wash") - 0.1, "flash"), ("S7b", T("c1", "wash", 1) - 0.1, "cut"), ("S7c", T("c1", "and") - 0.05, "cut"),
    ("S8", T("c2", "Send") - 0.1, "whip"), ("S8b", T("c2", "hides") - 0.15, "cut"),
    ("S9", LINES["c2"]["end"] + 0.05, "punch"), ("S10", round(LINES["c2"]["end"] + 0.45, 3), "cut"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
MORPH = {}
CLOCK = {}
CLOCK_D = 0.6
ACTION = {}
_write_on0 = write_on


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
    _write_on0(f, text, x, y, t, t0, int(size * 1.3), col, cps, op)


def st_(sid): return SHOT[sid]["start"]


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def hand_xy(x, y, s, arm, side, lean=0.0):
    a1, a2 = arm; bcx = x + 40 * s * math.sin(math.radians(lean)); bcy = y - 222 * s
    sx, sy = bcx + side * 118 * s, bcy - 46 * s
    ex, ey = sx + side * math.sin(math.radians(a1)) * 76 * s, sy + math.cos(math.radians(a1)) * 76 * s
    return ex + side * math.sin(math.radians(a2)) * 70 * s, ey + math.cos(math.radians(a2)) * 70 * s


_IK = {}


def arm_to(x, y, s, side, tx, ty):
    """brute-force 2-bone reach: arm angles (upper, fore) that put chub's hand closest to (tx, ty) (cached)."""
    key = (int(x), int(y), round(s, 2), side, int(tx) // 4, int(ty) // 4)
    if key not in _IK:
        best = None
        for a1 in range(-40, 181, 6):
            for a2 in range(-40, 181, 6):
                hx, hy = hand_xy(x, y, s, (a1, a2), side); d_ = (hx - tx) ** 2 + (hy - ty) ** 2
                if best is None or d_ < best[0]: best = (d_, (a1, a2))
        _IK[key] = best[1]
    return _IK[key]


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
    kw(f, "TOO MANY SWEETS", 540, 430, t, t0, "pop", 94, col=ACC_S, op=op)
    kw(f, "= WORMS?", 540, 590, t, t0, "shake", 130, col=RED, amp=0.25, op=op)


# ---- the cast in the DINING CORNER ----
CX, CY, CS = 320, 1880, 1.85          # Chubby
NX, NY, NS_ = 800, 1870, 1.8          # naani
TIN = (575, 1232)                      # the laddoo tin on the table


def wag(t, amp=16, rate=11): return amp * math.sin(t * rate)


def naani_yell(f, t, x=NX, y=NY, s=NS_, yell=1.0, hide=0.0):
    """naani wagging a finger at Chubby (screen-left arm), mouth open mid-yell; hide 0..1 = she tucks the tin behind her back (the send line)."""
    la = (70 + wag(t) * yell, 38 + wag(t + 0.1) * yell) if hide < 0.5 else (30, 20)
    ra = (24, 12) if hide <= 0 else (24 + 40 * hide, -20 * hide)
    nani(f, x, y, s, t, la=la, ra=ra, hand_l="point" if hide < 0.5 else "open", mouth=("o" if int(t * 8) % 2 else 3) if yell > 0.3 else talk(t),
         expr="angry" if yell > 0.3 and hide < 0.5 else "smirk", brow="sus" if yell > 0.3 else "up", look=(-1, 0.1), turn=-0.4, lean=-4 * yell)


def chub_tin(f, t, reach=1.0, freeze=None, expr="happy", mouth=None, look=(0.6, 0.4)):
    """Chubby with his hand in the laddoo tin; freeze = a take time (he's caught)."""
    tk = take(t, freeze, 0.9) if (freeze is not None and t > freeze - 0.1) else dict(dy=0, squash=0, lean=0)
    tx, ty = TIN[0] - 20, TIN[1] - 80 + 30 * (1 - reach)
    ra = arm_to(CX, CY, CS, 1, tx, ty)
    caught = freeze is not None and t > freeze
    chub(f, CX, CY + tk.get("dy", 0), CS, t=t, la=(30, 16), ra=ra, hand_r="grip", mouth=mouth if mouth is not None else (munch(t) if not caught else "o"),
         expr=tk.get("expr", "wow") if caught else expr, brow=tk.get("brow", "up") if caught else "n", look=(1, -0.1) if caught else look,
         lean=tk.get("lean", 0) + 3, squash=tk.get("squash", 0), turn=0.4)
    return ra


def scene0(f, t):
    """frame 0: Chubby, mouth full, hand deep in naani's steel laddoo tin; naani already mid-yell with a wagging finger; Chubby freezes at 0.9 s."""
    naani_yell(f, t)
    reach = 1.0 - 0.6 * ramp(t, 0.15, 0.4)
    el_at(f, tin_el(1.0), TIN[0], TIN[1], 0.62)
    ra = chub_tin(f, t, reach=reach, freeze=0.9)
    hx, hy = hand_xy(CX, CY, CS, ra, 1, 3)
    el_at(f, laddoo_el(), hx + 10, hy - 6, 0.36); grip_hand(f, hx, hy, CS)
    dining_front(f, DIN_TOP)
    el_at(f, laddoo_el(), 700, 1300, 0.3); el_at(f, laddoo_el(), 740, 1310, 0.28)


def shot_S0(t, n):
    f = set_dining(t, top_y=DIN_TOP)
    scene0(f, t)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="warm")


# ---- S0b: INSERT (cut mid-action) — the hand pulls a laddoo out of the tin, close; crumbs fall ----
def shot_S0b(t, n):
    t0 = st_("S0b")
    f = set_dining(t, top_y=DIN_TOP); f = dof(f, 7)
    k = ramp(t, t0, 0.7)
    el_at(f, tin_el(1.0), 560, 1500, 1.6)
    el_at(f, laddoo_el(), 540, 1360 - 360 * k, 0.95)
    big_hand(f, 540, 1000 - 360 * k, 1.5, rot=180, side=1, curl=(0.55, 0.6, 0.65, 0.7), thumb=30)
    fly_drops2(f, 540, 1330 - 360 * k + 60, 60, -80, t, t0 + 0.3, n=6, r=6, col=(214, 150, 60), rim=(150, 96, 40), floor=1600)
    hook_band(f); hook_words(f, t)
    f = insert_push(f, t, t0, SHOT["S0b"]["end"] - t0, 1.0, 1.06, 540, 1300)
    return finish(f, n, look="warm")


# ---- S0c: naani's close-up yell (reaction); Chubby frozen in the corner with a laddoo at his lips ----
def shot_S0c(t, n):
    f = set_dining(t, top_y=DIN_TOP); f = dof(f, 6)
    nani(f, 640, 2260, 2.5, t, la=(70 + wag(t, 22), 38), hand_l="point", mouth="o" if int(t * 8) % 2 else 3, expr="angry", brow="sus", look=(-1, 0), turn=-0.5, lean=-6)
    peek(f, t, 200, 1330, 0.7, expr="wow", look=(0.8, -0.2), mouth="o")
    el_at(f, laddoo_el(), 250, 1420, 0.4)
    hook_band(f); hook_words(f, t)
    if t > T("i1", "worms?") - 0.1: kw(f, "WORMS!", 540, 820, t, T("i1", "worms?") - 0.1, "sneak", 120, col=RED)
    return finish(f, n, look="warm")


# ---- S1: 'Nope. That's a myth.' board: a laddoo + a worm drawn beside it, NOPE, a MYTH stamp ----
def shot_S1(t, n):
    f = board_bg(); t0 = st_("S1"); tm = T("i2", "myth.") - 0.1
    el_at(f, laddoo_el("n", (1, 0)), 360, 1000, 1.5, t, t0 + 0.02)
    draw_arrow_on(f, (510, 1000), (650, 1000), ramp(t, t0 + 0.15, 0.25), BP_INK, 8, 26)
    if t > t0 + 0.2: worm(f, 900, 980, 1.4, t, 240, 18, ang=0, mood="happy", op=clamp((t - t0 - 0.2) / 0.2))
    if t > tm:
        draw_on(f, [(640, 840), (960, 1140)], ramp(t, tm, 0.2), RED, 20, seed=11, tip=False)
        draw_on(f, [(960, 840), (640, 1140)], ramp(t, tm + 0.1, 0.2), RED, 20, seed=12, tip=False)
        el_at(f, vstamp_el("MYTH", RED, 80), 540, 1290, 1.0, t, tm, rot=-8)
    kw(f, "NOPE.", 540, 400, t, t0 + 0.08, "shake", 170, col=RED, amp=0.3)
    peek(f, t, 160, 1380, 0.6, expr="sus", look=(0.8, -0.4))
    src(f, SRC_MYTH, t, t0 + 0.6, y=1470)
    return finish(f, n, look="fresh")


# ---- S1b: '...No amount of laddoos can make a worm.' a laddoo pile that keeps growing; the worm counter stays at 0 ----
def shot_S1b(t, n):
    f = board_bg(); t0 = st_("S1b"); tw = T("i2", "worm.") - 0.1
    k = ramp(t, t0, 1.3)
    nn = int(1 + 14 * k); i = 0
    for row in range(5):
        for c in range(5 - row):
            if i >= nn: break
            el_at(f, laddoo_el(), 540 + (c - (4 - row) / 2) * 120, 1260 - row * 100, 0.62); i += 1
    write_on(f, f"{count_up(t, t0, 50, 1.3)} laddoos", 540, 760, t, t0, 44, BP_INK, cps=60)
    kw(f, "NO AMOUNT OF LADDOOS", 540, 320, t, t0 + 0.05, "pop", 80, col=BP_INK)
    if t > tw:
        kw(f, "= 0 WORMS", 540, 460, t, tw, "drop", 120, col=ACC_S, t1=tw + 0.7)
    return finish(f, n, look="fresh")


# ---- S2: 'Worms start as tiny eggs,' a speck on the board -> a magnifier inset -> the egg buddy (define on sight) ----
def shot_S2(t, n):
    f = board_bg(); t0 = st_("S2"); te = T("a1", "eggs,") - 0.15
    worm(f, 300, 1150, 1.0, t, 200, 14, ang=10)
    write_on(f, "worm", 230, 1250, t, t0 + 0.1, 40, BP_INK, cps=40)
    cv2.circle(f, (760, 1100), 7, C(ACC_S), -1, cv2.LINE_AA)
    if t > te:
        k = snap(t, te, 5)
        def draw(g):
            g[:] = np.array(C(ACC_XL), np.float32); el_at(g, egg_el("n", (-0.6, 0.2)), 700, 960, 1.35)
        inset(f, 700, 960, 230, draw, k, ring=WHITE)
        draw_on(f, [(760, 1100), (720, 1190)], ramp(t, te, 0.2), BP_INK, 5, seed=3, tip=False)
        write_on(f, "a worm egg", 700, 1260, t, te + 0.2, 42, ACC_S, cps=40)
    kw(f, "WORMS START AS", 540, 320, t, t0 + 0.05, "pop", 86, col=BP_INK)
    if t > te: kw(f, "TINY EGGS", 540, 450, t, te, "pop", 120, col=ACC_S)
    return finish(f, n, look="fresh")


# ---- S2b: '...those eggs come out in an infected person's poop.' person (with worms inside) -> arrow -> a tiny poop with eggs ----
def shot_S2b(t, n):
    f = board_bg(); t0 = st_("S2b"); ti = T("a1", "infected") - 0.1; tp = T("a1", "poop.") - 0.1
    person_icon(f, 280, 1060, 4.6, 0.0, t)
    if t > ti:
        worm(f, 320, 1090, 0.6, t, 140, 9, ang=20, mood=None)
        write_on(f, "infected person", 280, 1250, t, ti, 40, BP_INK, cps=40)
    draw_arrow_on(f, (420, 1040), (600, 1040), ramp(t, ti + 0.2, 0.3), BP_INK, 8, 26)
    if t > tp - 0.15:
        el_at(f, poop_el(), 780, 1060, 1.1, t, tp - 0.15)
        for j, (ex, ey) in enumerate(((730, 1050), (800, 1020), (840, 1080))):
            el_at(f, egg_el("happy" if j == 1 else "n"), ex, ey, 0.25, t, tp + 0.1 + 0.08 * j)
        write_on(f, "poop", 780, 1220, t, tp, 44, BP_INK, cps=40)
    kw(f, "THE EGGS COME OUT IN", 540, 320, t, t0 + 0.05, "pop", 80, col=BP_INK)
    if t > tp: kw(f, "POOP", 540, 450, t, tp, "shake", 130, col=ACC_S, amp=0.2)
    src(f, SRC_WHO, t, t0 + 0.3, y=1470)
    return finish(f, n, look="fresh")


# ---- S3: 'If there's no toilet, they end up in the soil, where they wait about three weeks to get ready.' THE BACKYARD (new place) ----
YX, YY, YS = 300, 1700, 1.5


def week_marks(f, t, t0s, x=540, y=1080):
    for i in range(3):
        bx = x - 150 + 150 * i
        cv2.rectangle(f, (bx - 58, y - 46), (bx + 58, y + 46), C((252, 250, 244)), -1); cv2.rectangle(f, (bx - 58, y - 46), (bx + 58, y + 46), C(INKC), 4)
        cv2.rectangle(f, (bx - 58, y - 46), (bx + 58, y - 22), C(ACC), -1)
        comp(f, ed_el(f"WK {i + 1}", "", lead_col=INKC, lead_size=34), bx, y + 10)
        if t > t0s[i]: draw_on(f, [(bx - 34, y + 6), (bx - 6, y + 34), (bx + 40, y - 24)], ramp(t, t0s[i], 0.15), OKG, 9, seed=40 + i, tip=False)


def shot_S3(t, n):
    f = set_yard(t); t0 = st_("S3"); ts = T("a2", "soil,") - 0.1; t3 = T("a2", "three") - 0.1; tr = T("a2", "ready.") - 0.1
    lk = look_to(YX, YY - 650, 740, 1120)
    chub(f, YX, YY, YS, t=t, la=(30, 16), ra=(100, 70), hand_r="grip", hold=scale_el(magnifier_ink_el(), 0.7), hold_off=(20, -10), hold_front=True,
         mouth=talk(t), expr="sus", brow="sus", look=lk, lean=6, turn=0.5)
    yard_front(f, 1480, t)
    if t > ts:
        k = snap(t, ts, 5)
        def draw(g):
            g[:] = np.array(C(SOIL_L), np.float32); soil_patch(g, 740, 1160, 600, 200, 7, eggs=3, t=t, egg_s=0.5)
        inset(f, 740, 1120, 200, draw, k, ring=WHITE)
    hook_band(f, 250, 640, 0.75)
    kw(f, "NO TOILET?", 540, 320, t, t0 + 0.05, "pop", 96, col=INKC)
    if t > ts: kw(f, "EGGS IN THE SOIL", 540, 460, t, ts, "pop", 100, col=ACC_S)
    src(f, SRC_WHO, t, t0 + 0.3, y=1462)
    return finish(f, n, look="golden")


# ---- S3b: '...where they wait about three weeks to get ready.' board: three week boxes tick; the eggs in the soil ripen + wriggle ----
def shot_S3b(t, n):
    f = board_bg(); t0 = st_("S3b"); t3 = T("a2", "three") - 0.1; tr = T("a2", "ready.") - 0.1
    soil_patch(f, 540, 1200, 760, 260, 9, eggs=4, t=t, ready=ramp(t, t3, 1.1), egg_s=0.62)
    write_on(f, "soil", 180, 1400, t, t0 + 0.1, 40, BP_INK, cps=40)
    week_marks(f, t, [t3 + 0.05, t3 + 0.3, t3 + 0.55], 540, 790)
    kw(f, "THEY WAIT", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > t3: kw(f, "ABOUT 3 WEEKS", 540, 450, t, t3, "pop", 104, col=ACC_S)
    if t > tr: kw(f, "READY!", 540, 610, t, tr, "shake", 90, col=RED, amp=0.3)
    peek(f, t, 900, 1400, 0.55, expr="gross" if t > tr else "sus", look=(-0.7, -0.3))
    src(f, SRC_WHO, t, t0 + 0.3, y=1478)
    return finish(f, n, look="fresh")


# ---- S4: 'Then they hitch a ride...' Chubby playing in the mud; he lifts his hands and LOOKS DOWN at them (eyeline A) ----
def shot_S4(t, n):
    f = set_yard(t); t0 = st_("S4")
    lift = ramp(t, LOOK_T - 0.2, 0.3)
    dig = (1 - lift) * math.sin(t * 9)
    la = (14 + 30 * lift + 8 * dig, -10 + 120 * lift); ra = (14 + 30 * lift - 8 * dig, -10 + 120 * lift)
    lk = (0.0, 0.9 * ramp(t, LOOK_T, 0.15))                      # eyes lead, then hold the look on the hands
    chub(f, 540, 1760, 1.6, t=t, la=la, ra=ra, mouth=3 if lift < 0.5 else "o", expr="happy" if lift < 0.5 else "sus", brow="up" if lift < 0.5 else "sus",
         look=lk, lean=0, hair=(0, 4 * dig))
    for sd in (-1, 1):
        hx, hy = hand_xy(540, 1760, 1.6, la if sd < 0 else ra, sd)
        mud_on(f, hx, hy, 1.0, seed=3 + sd, n=6, r=20)
    yard_front(f, 1500, t, spinach=False)
    if lift < 0.5: fly_drops2(f, 540, 1520, 0, -380, t, t0 + 0.05, n=8, r=10, col=SOIL, rim=SOIL_S, floor=1560)
    hook_band(f, 250, 600, 0.75)
    kw(f, "THEN THEY HITCH A RIDE", 540, 320, t, t0 + 0.05, "sneak", 80, col=INKC)
    return finish(f, n, look="golden")


# ---- S4b: EYELINE B / POV INSERT — his own muddy hands from his eyes; eggs riding on the fingertips; slow push-in ----
def shot_S4b(t, n):
    f = set_yard(t, blur=9); t0 = st_("S4b"); th = T("a3", "hands,") - 0.1
    f = dof(f, 5)
    rise = ramp(t, t0, 0.3)
    ys = 1900 - 300 * rise
    tl = big_hand(f, 330, ys, 1.9, rot=-12, side=-1, curl=(0.2, 0.15, 0.25, 0.35), thumb=40)
    tr = big_hand(f, 750, ys, 1.9, rot=12, side=1, curl=(0.15, 0.2, 0.3, 0.3), thumb=40)
    for j, hh in enumerate((tl, tr)):
        for i, (px, py) in enumerate(hh["tips"]):
            mud_on(f, px, py + 60, 0.7, seed=10 * j + i, n=3, r=14)
        mud_on(f, hh["wrist"][0], hh["wrist"][1] - 120, 1.1, seed=50 + j, n=8, r=24)
    if t > th:
        for j, (hh, i) in enumerate(((tl, 1), (tr, 2), (tr, 0))):
            px, py = hh["tips"][i]; tt = th + 0.15 * j
            if t > tt:
                el_at(f, egg_el("happy", (0, -0.5)), px, py - 50 + 6 * math.sin(t * 9 + j), 0.55, t, tt, rot=8 * math.sin(t * 5 + j))
    hook_band(f, 250, 600, 0.75)
    kw(f, "THEN THEY HITCH A RIDE", 540, 320, t, -1, "pop", 80, col=INKC)
    if t > th: kw(f, "ON DIRTY HANDS", 540, 460, t, th, "pop", 100, col=ACC_S)
    f = pov_insert(f, 1.0)
    f = insert_push(f, t, t0, SHOT["S4b"]["end"] - t0, 1.0, 1.08, 540, 1250)
    return finish(f, n, look="golden")


# ---- S4c: '...on unwashed veggies, or in dirty water.' board: the three rides in a row; an egg hops onto each ----
def shot_S4c(t, n):
    f = board_bg(); t0 = st_("S4c"); tv = T("a3", "veggies,") - 0.15; tw = T("a3", "water.") - 0.2
    items = ((None, "hands", t0 + 0.02, 200), (lettuce_el(), "veggies", tv, 540), (glass2_el((200, 170, 120), 0.7), "water", tw, 880))
    for el, lab, tt, x in items:
        if t > tt:
            if el is None:
                big_hand(f, x, 1150, 0.95, rot=0, side=1, curl=(0.2, 0.15, 0.25, 0.35), thumb=40); mud_on(f, x, 970, 0.9, seed=4, n=6, r=16)
            else: el_at(f, el, x, 1030, 1.25 if x == 540 else 1.15, t, tt)
            hop = ramp(t, tt + 0.1, 0.35)
            el_at(f, egg_el("happy"), x - 70 + 70 * hop, 800 + 40 * hop - 160 * math.sin(math.pi * hop), 0.42)
            write_on(f, lab, x, 1300, t, tt + 0.05, 46, BP_INK, cps=50)
    kw(f, "THEY RIDE ON", 540, 300, t, t0 + 0.02, "pop", 70, col=BP_INK)
    kw(f, "HANDS, VEGGIES, WATER", 540, 420, t, t0 + 0.05, "pop", 68, col=ACC_S)
    src(f, SRC_WHO, t, t0 + 0.3, y=1470)
    return finish(f, n, look="fresh")


# ---- S5: 'And one kind doesn't even need your mouth.' the yard: Chubby covers his mouth, then LOOKS DOWN at his feet (eyeline A) ----
def shot_S5(t, n):
    f = set_yard(t); t0 = st_("S5"); tm = T("a4", "mouth.") - 0.1; tl = T("a4", "mouth.") + 0.25
    cover = ramp(t, tm - 0.25, 0.2)
    lk = (0.0, -0.2) if t < tl else (0.15, 0.95)
    chub(f, 540, 1760, 1.6, t=t, la=(30, 16), ra=(148 * cover + 20 * (1 - cover), -130 * cover + 10 * (1 - cover)), mouth=0 if cover > 0.5 else talk(t),
         expr="sus" if t < tl else "wow", brow="sus" if t < tl else "up", look=lk, lean=0 if t < tl else 4)
    yard_front(f, 1520, t, spinach=False)
    hook_band(f, 250, 600, 0.75)
    kw(f, "ONE KIND DOESN'T", 540, 320, t, t0 + 0.05, "pop", 84, col=INKC)
    if t > tm: kw(f, "NEED YOUR MOUTH", 540, 460, t, tm, "pop", 96, col=ACC_S)
    return finish(f, n, look="golden")


# ---- S5b: EYELINE B / INSERT — his bare foot on the soil; a thin larva wriggles out of the soil to the heel; the foot jerks up ----
def shot_S5b(t, n):
    f = set_yard(t, blur=9); t0 = st_("S5b"); tb = T("a4", "bare") - 0.1; tj = T("a4", "feet.") + 0.25
    f = dof(f, 5)
    up = 140 * ramp(t, tj, 0.12) if t > tj else 0.0
    el_at(f, foot_el(0.5), 560, 1290 - up, 1.45)
    lx = 140 + 260 * ramp(t, t0, max(0.2, tb - t0 + 0.4))
    worm(f, lx, 1430 - 30 * ramp(t, tb, 0.4), 1.6, t, 150, 10, phase_sp=11, ang=-12, thin=True)
    hook_band(f, 250, 600, 0.75)
    kw(f, "IT GETS IN THROUGH", 540, 320, t, t0 + 0.02, "pop", 80, col=INKC)
    if t > tb: kw(f, "BARE FEET", 540, 460, t, tb, "shake", 120, col=RED, amp=0.25)
    if t > tj: kw(f, "!", 760, 1050, t, tj, "pop", 140, col=RED)
    src(f, "Source: CDC; WHO (hookworm)", t, t0 + 0.2, y=1478)
    f = pov_insert(f, 0.8)
    f = insert_push(f, t, t0, SHOT["S5b"]["end"] - t0, 1.0, 1.06, 560, 1350)
    return finish(f, n, look="golden")


# ---- S6: 'So the real route is soil. Hands. Mouth. Sugar isn't even on the map.' the ROUTE MAP; the laddoo is left off it ----
STATIONS = ((215, 980, "SOIL"), (540, 980, "HANDS"), (865, 980, "MOUTH"))


def shot_S6(t, n, titles=True):
    f = board_bg(); t0 = st_("S6"); ts = [T("a5", "soil.") - 0.1, T("a5", "Hands.") - 0.1, T("a5", "Mouth.") - 0.1]
    tsg = T("a5", "Sugar") - 0.1; tm = T("a5", "map.") - 0.15
    for i, (x, y, lab) in enumerate(STATIONS):
        lit = t > ts[i]
        cv2.circle(f, (x, y), 126, C(ACC_XL if lit else (240, 242, 248)), -1, cv2.LINE_AA)
        cv2.circle(f, (x, y), 126, C(ACC if lit else BP_INK), 9, cv2.LINE_AA)
        if i == 0: soil_patch(f, x, y + 30, 210, 100, 3)
        elif i == 1:
            big_hand(f, x, y + 100, 0.7, side=1, curl=(0.2, 0.15, 0.25, 0.35), thumb=40); mud_on(f, x, y - 20, 0.5, seed=8, n=5, r=14)
        else: chub_head_only(f, x, y + 14, 1.1, t, mouth="o" if lit else 0, expr="wow" if lit else "n")
        if lit: kw(f, lab, x, y + 200, t, ts[i], "pop", 66, col=ACC_S)
        if i < 2: draw_arrow_on(f, (x + 128, y), (STATIONS[i + 1][0] - 128, y), ramp(t, ts[i] + 0.1, 0.25), ACC, 9, 26)
        if lit and i < 2:
            hop = clamp((t - ts[i]) / 0.5)
            if hop < 1: el_at(f, egg_el("happy"), x + (STATIONS[i + 1][0] - x) * hop, y - 150 - 90 * math.sin(math.pi * hop), 0.26)
    if t > tsg:
        k = ramp(t, tsg, 0.5)
        lx = 540; ly = 1430 - 80 * k
        el_at(f, laddoo_el("sad" if t > tm else "n", (0, -1)), lx, ly, 0.95)
        if t > tm:
            draw_on(f, [(lx - 100, ly - 100), (lx + 100, ly + 100)], ramp(t, tm, 0.18), RED, 16, seed=6, tip=False)
            draw_on(f, [(lx + 100, ly - 100), (lx - 100, ly + 100)], ramp(t, tm + 0.08, 0.18), RED, 16, seed=7, tip=False)
    if titles: s6_titles(f, t, t0, tm)
    return finish(f, n, look="fresh")


def s6_titles(f, t, t0, tm):
    kw(f, "THE REAL ROUTE", 540, 320, t, t0 + 0.05, "pop", 96, col=BP_INK)
    if t > tm: kw(f, "SUGAR? NOT ON THE MAP", 540, 450, t, tm, "drop", 80, col=RED, t1=tm + 1.2)


def shot_S6b(t, n):
    """the laddoo walks up to the map and gets crossed out: a crash zoom onto it (punchline), then the camera holds."""
    f = shot_S6(t, n, titles=False).astype(np.float32)
    f = crash_zoom(f, t, st_("S6b") + 0.05, 1.12, 540, 1120)
    s6_titles(f, t, st_("S6"), T("a5", "map.") - 0.15)
    return f


# ---- S7: 'Wash your hands before you eat,' the yard hand-pump: water pours, soap foam on Chubby's hands ----
def shot_S7(t, n):
    f = set_yard(t); t0 = st_("S7")
    rub = math.sin(t * 14)
    la = arm_to(520, 1760, 1.55, -1, 500 + 12 * rub, 1440); ra = arm_to(520, 1760, 1.55, 1, 560 - 12 * rub, 1440)
    chub(f, 520, 1760, 1.55, t=t, la=la, ra=ra, mouth=talk(t), expr="happy", brow="up", look=(0.2, 0.7), lean=0, turn=0.2)
    hx1, hy1 = hand_xy(520, 1760, 1.55, la, -1); hx2, hy2 = hand_xy(520, 1760, 1.55, ra, 1)
    mx, my = (hx1 + hx2) / 2, (hy1 + hy2) / 2
    pour_stream(f, 830, 1072, mx + 40, my, t, w=22, col=(170, 214, 246), rim=(90, 150, 210), head=ramp(t, t0, 0.2))
    soap_foam(f, mx, my, t, n=14, rad=70, k=ramp(t, t0 + 0.2, 0.5))
    yard_front(f, 1520, t, spinach=False)
    hook_band(f, 250, 600, 0.75)
    kw(f, "WASH YOUR HANDS", 540, 320, t, t0 + 0.05, "pop", 100, col=ACC_S)
    kw(f, "BEFORE YOU EAT", 540, 460, t, T("c1", "before") - 0.1, "pop", 84, col=INKC)
    return finish(f, n, look="golden")


# ---- S7b: INSERT (mid-action) — spinach under the pump; the eggs wash off and tumble away ----
def shot_S7b(t, n):
    f = set_yard(t, blur=9); t0 = st_("S7b"); f = dof(f, 4)
    pour_stream(f, 520, 700, 540, 1130, t, w=36, col=(170, 214, 246), rim=(90, 150, 210))
    el_at(f, lettuce_el(), 540, 1200, 1.7)
    for j in range(3):
        k = ramp(t, t0 + 0.15 + 0.12 * j, 0.6)
        el_at(f, egg_el("wow"), 470 + 70 * j + 80 * k * (j - 1), 1130 + 420 * k * k, 0.3, rot=200 * k)
    splash_crown(f, 540, 1150, t, t0 + 0.05, 90, (200, 230, 250), (90, 150, 210), seed=3)
    hook_band(f, 250, 600, 0.75)
    kw(f, "WASH THE VEGGIES", 540, 390, t, t0 + 0.02, "pop", 100, col=ACC_S)
    return finish(f, n, look="golden")


# ---- S7c: INSERT — a bare foot slides into a chappal; a tick ----
def shot_S7c(t, n):
    f = set_yard(t, blur=9); t0 = st_("S7c"); tc = T("c1", "chuppuls") - 0.1
    f = dof(f, 4)
    el_at(f, _rot_el(chappal_el(), 90), 600, 1390, 1.6)
    slide = ramp(t, t0 + 0.1, 0.45)
    el_at(f, foot_el(0.0), 120 + 440 * slide, 1230 + 60 * slide, 1.1)
    if t > tc:
        draw_on(f, [(760, 1080), (810, 1130), (900, 1010)], ramp(t, tc + 0.2, 0.2), OKG, 16, seed=70, tip=False)
    hook_band(f, 250, 600, 0.75)
    kw(f, "WEAR CHAPPALS", 540, 340, t, tc - 0.1, "pop", 110, col=ACC_S)
    kw(f, "OUTSIDE", 540, 480, t, T("c1", "outside.") - 0.1, "pop", 90, col=INKC)
    src(f, SRC_CDC, t, t0 + 0.2, y=1478)
    return finish(f, n, look="golden")


# ---- S8: 'Send this to the naani who hides the laddoo tin...' naani tucks the tin behind her back; Chubby points + laughs ----
def shot_S8(t, n):
    f = set_dining(t, top_y=DIN_TOP); t0 = st_("S8"); th = T("c2", "hides") - 0.15
    naani_yell(f, t, yell=0.0, hide=0.01)
    el_at(f, tin_el(0.0), NX + 60, 1240, 0.6)
    chub(f, CX, CY, CS, t=t, **nolean(POSE["point"]), mouth=3 if t > th + 0.3 else talk(t), expr="happy", brow="up", look=(1, 0), lean=4, turn=0.5)
    dining_front(f, DIN_TOP)
    hook_band(f, 250, 640, 0.8)
    ui_word(f, "send this to the naani who", "[HIDES THE TIN]", 430, t, t0 + 0.05, col=INKC, acc=ACC_S, size=104, lead_col=INKC)
    return finish(f, n, look="warm")


# ---- S8b: INSERT (mid-action) — naani slides the tin behind her back; Chubby laughs in the corner ----
def shot_S8b(t, n):
    f = set_dining(t, top_y=DIN_TOP); t0 = st_("S8b"); f = dof(f, 6)
    k = ramp(t, t0, 0.45)
    el_at(f, tin_el(0.0), 760 + 260 * k, 1450 - 40 * k, 1.1, rot=-10 * k)
    nani(f, 560, 2300, 2.4, t, la=(24, 12), ra=(40 + 60 * (1 - k), 20), mouth="smirk" if False else 3, expr="smirk", brow="up", look=(1, -0.2), turn=0.5, lean=4)
    peek(f, t, 180, 1360, 0.7, expr="happy", look=(0.8, -0.2), mouth=3)
    hook_band(f, 250, 640, 0.8)
    ui_word(f, "send this to the naani who", "[HIDES THE TIN]", 430, t, -1, col=INKC, acc=ACC_S, size=104, lead_col=INKC)
    if t > T("c2", "worms!") - 0.1: kw(f, "TO SAVE YOU FROM WORMS!", 540, 610, t, T("c2", "worms!") - 0.1, "sneak", 62, col=RED)
    return finish(f, n, look="warm")


# ---- S9: the logo beat ----
def shot_S9(t, n):
    t0 = st_("S9"); f = set_dining(t, top_y=DIN_TOP); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.2) * 0.95)
    comp(f, ed_el("follow for more food + health facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.1) / 0.2))
    return finish(f, n, look="warm")


# ---- S10: the LOOP TAIL ----
def shot_S10(t, n):
    f = set_dining(t - END, top_y=DIN_TOP)
    scene0(f, t - END)
    hook_band(f)
    return finish(f, n, look="warm")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(0.9, 0.3, 12), (T("i1", "worms?") - 0.1, 0.3, 10), (T("i2", "Nope.") - 0.05, 0.35, 14), (T("i2", "myth.") - 0.1, 0.3, 12),
           (T("i2", "worm.") - 0.1, 0.25, 8), (T("a1", "eggs,") - 0.15, 0.25, 8), (T("a1", "poop.") - 0.1, 0.3, 10), (T("a2", "soil,") - 0.1, 0.25, 8),
           (T("a3", "hands,") - 0.1, 0.25, 8), (T("a4", "bare") - 0.1, 0.3, 12), (T("a4", "feet.") + 0.25, 0.25, 10), (T("a5", "map.") - 0.15, 0.35, 14),
           (T("c1", "chuppuls") - 0.1, 0.25, 8), (T("c2", "hides") - 0.15, 0.3, 10)]


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
