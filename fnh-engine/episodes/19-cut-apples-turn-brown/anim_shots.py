# ================= shots: FreshNestHub 19 — "Why do cut apples turn brown?" (Chubby INK, ep 3 of the ink look) =================
# COLOUR SCRIPT (5-colour ink palette + ONE accent): APPLE RED accent = the apple skin, the 3D ink titles, the chips; the browning = a sepia
# wash in the ink family; MINT = PPO the enzyme machine + every fix; paper = flesh / oxygen / the colourless stage. Places: the new LUNCH
# TABLE (sunny window, checked cloth) for every story moment, paper stages for the cell diagrams, the fridge-night and stove places for
# cold / heat. CRAFT (ep 19): TIMING & SPACING — snappy 4-frame pose changes with long moving holds (anim_fx.keyed / pose_keys /
# moving_hold), a proper cartoon TAKE on every surprise (anim_fx.take: anticipation, 2-frame snap, held extreme, settle), ink 3D titles
# that SNAP in (anim_cine.title_ink); Chubby stands INSIDE the diagram shots (next to the cell room) instead of cutting away.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i2", "Yeah.") - 0.15, "punch"), ("S1", T("i3", "Stick") - 0.2, "whip"),
    ("S2", T("a1", "So,") - 0.2, "flash"), ("S2b", T("a1", "like") - 0.12, "zoom"),
    ("S3", T("a2", "In") - 0.2, "whip"), ("S3b", T("a2", "In", 1) - 0.15, "punch"), ("S3c", T("a2", "a") - 0.12, "zoom"),
    ("S4", T("a3", "In") - 0.2, "whip"), ("S4b", T("a3", "Fine,") - 0.15, "punch"),
    ("S5", T("b1", "Then") - 0.2, "flash"), ("S5b", T("b1", "And") - 0.15, "zoom"),
    ("S6", T("b2", "And") - 0.2, "whip"),
    ("S7", T("b3", "PPO") - 0.2, "whip"), ("S7b", T("b3", "At") - 0.15, "punch"),
    ("S8", T("b4", "Then") - 0.2, "whip"), ("S8b", T("b4", "And") - 0.15, "zoom"),
    ("S9", T("c1", "Same") - 0.2, "flash"), ("S9b", T("c1", "The") - 0.15, "punch"),
    ("S10", T("c2", "Why") - 0.2, "whip"), ("S10b", T("c2", "Scientists") - 0.15, "zoom"),
    ("S11", T("c3", "Quick") - 0.2, "whip"), ("S11b", T("c4", "Nope.") - 0.12, "flash"), ("S11c", T("c4", "It") - 0.15, "punch"),
    ("S12", T("d1", "Okay,") - 0.2, "whip"),
    ("S13", T("d2", "Lemon") - 0.2, "whip"), ("S13b", T("d2", "and") - 0.15, "punch"),
    ("S14", T("d3", "No") - 0.2, "whip"), ("S14b", T("d3", "The") - 0.15, "zoom"),
    ("S15", T("d4", "Cold") - 0.2, "focus"), ("S15b", T("d4", "Heat") - 0.12, "flash"),
    ("S16", T("e1", "Now") - 0.2, "whip"), ("S16b", T("e2", "Black") - 0.2, "punch"), ("S16c", T("e2", "Coffee") - 0.15, "zoom"),
    ("S17", T("e3", "Avocados,") - 0.2, "whip"), ("S17b", T("e3", "That") - 0.15, "punch"),
    ("S18", T("f1", "And") - 0.2, "flash"), ("S18b", T("f1", "Scientists") - 0.15, "zoom"), ("S18c", T("f2", "Approved") - 0.2, "punch"),
    ("S19", T("g1", "Quick") - 0.2, "whip"), ("S20", T("g2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
SRC_U = "Source: UW-Madison (R. Hartel) · Science News Explores"
SRC_I = "Source: University of Illinois Extension · Penn State Extension"
SRC_N = "Source: University of Nebraska-Lincoln · Illinois Extension"
SRC_S = "Source: Scientific American (UMass Amherst) · UW-Madison"
SRC_A = "Source: Medill Reports (USDA, 2015) · Science News Explores"


def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def icap(f, lead, big, t, t0, acc=ACC, size=170, y=470, out=None, tail="", dark=False):
    """ink caption: warm-ink text on paper sets, white with shadow on dark sets."""
    if dark: ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.6, lead_col=WHITE, out=out, tail=tail)
    else: ui_word(f, lead, big, y, t, t0, col=INKC, acc=acc, size=size, shadow=0.0, lead_col=INKC, out=out, tail=tail)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def rays(f, x, y, r, col, amt, t, nr=14):
    if amt <= 0.01: return
    ov = np.zeros((H, W), np.float32); a0 = t * 0.25
    for i in range(nr):
        a = a0 + i * 2 * math.pi / nr; da = math.pi / nr * 0.5
        pts = np.array([[x, y], [x + r * math.cos(a - da), y + r * math.sin(a - da)], [x + r * math.cos(a + da), y + r * math.sin(a + da)]], np.int32)
        cv2.fillPoly(ov, [pts], 1.0, cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 6) * np.clip(1 - np.hypot(_xx - x, _yy - y) / r, 0, 1)
    f += ov[..., None] * np.array(C(col), np.float32) * amt


def ring(f, x, y, r, col, th=8, op=1.0):
    ov = f.copy(); cv2.circle(ov, (int(x), int(y)), int(r), C(col), th, cv2.LINE_AA); f[:] = f * (1 - op) + ov * op


def munch(t, rate=0.42):
    ph = (t / rate) % 1.0
    return (2 if ph < 0.5 else 0), int(t / rate)


def ichip(text, size=26, inv=False): return chip(text, INKC if not inv else MILK, MILK if not inv else INKC, size)


def mchip(text, size=30): return chip(text, INK_MINT_S, MILK, size)


def achip(text, size=30): return chip(text, ACC_S, MILK, size)


def t3(f, text, y, t, t0, size=260, face=ACC_L, side=ACC_S, x=540):
    """ink 3D title in the accent, snaps in (drawn BEFORE Chubby / the hero)."""
    if t >= t0: title_ink(f, text, y, t, t0, size=size, face=face, side=side, depth=18, x=x)


TABLE = 1330
TTAN = T("i1", "tan?") - 0.15; TBROWN = T("i1", "brown") - 0.1
BLUE = (60, 110, 160); BLUE_L = (214, 236, 250)


def clock_hand(f, x, y, t, speed=1.0, r=58):
    """a live minute hand spinning on the lunch-table wall clock (time-lapse cue)."""
    a = math.radians(-90 + t * 120 * speed)
    cv2.line(f, (int(x), int(y)), (int(x + r * math.cos(a)), int(y + r * math.sin(a))), C(INKC), 6, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), 7, C(INKC), -1, cv2.LINE_AA)


def chub_table(f, x, t, pose, s=1.0, **kw):
    """Chubby behind the lunch table (cloth drawn after him so he sits behind it)."""
    p = dict(pose); p.update(kw)
    chub(f, x, 1500, s, t=t, **p)


# ---- S0: HOOK — the lunch table: Chubby has just cut an apple; the cut half browns in time-lapse (the clock spins); on 'tan' the sun pops
#      and Chubby gets a TAKE + a tan; ink 3D 'A TAN?' behind him ----
def shot_S0(t, n):
    f = set_lunch(t)
    clock_hand(f, 240, 420, t, 1.0 if t < TTAN else 0.0)
    br = clamp(0.1 + 0.9 * ramp(t, 0.1, max(0.6, TBROWN + 0.3)))
    t3(f, "A TAN?", 760, t, TTAN, 280, ACC_L, ACC_S)
    tk = take(t, TTAN, 1.0, 9)
    pose = pose_keys(t, [(0.0, dict(la=(26, 14), ra=(150, 175), lean=3)), (TBROWN - 0.1, dict(la=(60, 30), ra=(150, 175), lean=5)), (TTAN, dict(POSE["shock"]))], 4)
    mh = moving_hold(t, 1, 0.8)
    chub_table(f, 300, t, pose, mouth="o" if TTAN <= t < TTAN + 0.6 else talk(t), expr=tk["expr"] if t >= TTAN else "n", brow=tk["brow"] if t >= TTAN else "up",
               look=(0.8, 0.2) if t < TTAN else (0.3, -0.5), lean=pose.get("lean", 0) + mh["lean"] + tk["lean"], squash=tk["squash"], bob=tk["dy"] + mh["bob"],
               tint=0.35 * ramp(t, TTAN + 0.1, 0.25), hand_r="grip" if t < TTAN else "open", hair=(drag(t, lambda q: take(q, TTAN, 1.0, 9)["dy"], 3, 0.8), 0))
    if t < TTAN: knife_ink_at(f, 462 + 40 * math.sin(math.radians(pose["lean"])), 1100 + 4 * math.sin(t * 2), 62 + 3 * math.sin(t * 1.5), 0.62)
    else:
        ky, kx_, ky_ = drop_land(t, TTAN, 1100, 1300, 0.35)
        knife_ink_at(f, 430 + 40 * clamp((t - TTAN) / 0.35), min(ky, 1322), 62 - 80 * clamp((t - TTAN) / 0.35), 0.62)
    cloth_front(f, TABLE)
    comp(f, scale_el(board_ink_el(620), 0.9), 640, 1372)
    comp(f, scale_el(apple_el(0.0, False, None), 0.62), 470, 1290)
    comp(f, scale_el(apple_el(br, True, None), 0.68), 760, 1272)
    if t >= TTAN:
        comp(f, sun_ink_el("happy"), 860, 620 + 6 * math.sin(t * 2), scale=snap(t, TTAN, 4, 2.0))
        rays(f, 860, 620, 520, (255, 220, 120), 0.4 * ramp(t, TTAN, 0.3), t)
    comp(f, ichip("same apple, a few minutes later", 24), 760, 1456, op=clamp((t - TBROWN - 0.2) / 0.3) if t < TTAN else 0)
    icap(f, "a cut apple goes", "[BROWN]...", t, 0.12, acc=BROWN, size=190, out=TTAN - 0.05)
    icap(f, "for the same reason you get...", "", t, TTAN, acc=ACC, size=150) if t >= TTAN else None
    f = cam(f, 1 + 0.03 * clamp(t / 4), 540, 1100)
    return finish(f, n, look="golden")


# ---- S0b: 'that brown is melanin, the same stuff that colours your skin, your hair, your eyes' — big head close-up with leader labels ----
def shot_S0b(t, n):
    f = ink_set("sepia", (250, 236, 210), 540, 1000, 440); f *= 0.95
    tm = T("i2", "melanin,") - 0.15; ts = T("i2", "skin,") - 0.1; th = T("i2", "hair,") - 0.1; te = T("i2", "eyes.") - 0.1
    if t < ts - 0.05: t3(f, "MELANIN", 620, t, tm, 210, BROWN_L, BROWN_D)
    chub_head_only(f, 420, 1060, 1.9, t, expr="happy" if t < ts else "n", brow="up", look=(0.5, 0.1), tint=0.35)
    comp(f, scale_el(slice_el(0.8), 1.2), 830, 1300 + 4 * math.sin(t * 3), scale=pin(t, st_("S0b"), 0.3))
    comp(f, scale_el(melanin_el(1.0, 2, 40), 0.8), 830, 1180, scale=pin(t, tm, 0.3))
    if t >= tm: draw_arrow(f, 790, 1230, 800, 1290, ramp(t, tm, 0.3), INKC, 6, 20)
    if t >= ts: label_at(f, "SKIN", 760, 940, t, ts, 560, 1120, bg=BROWN_D, fg=MILK, size=30)
    if t >= th: label_at(f, "HAIR", 780, 800, t, th, 520, 880, bg=BROWN_D, fg=MILK, size=30)
    if t >= te: label_at(f, "EYES", 820, 1060, t, te, 500, 1030, bg=BROWN_D, fg=MILK, size=30)
    icap(f, "that brown is...", "", t, st_("S0b") + 0.05, acc=BROWN, size=150, out=ts - 0.05)
    icap(f, "the same stuff in your", "[SKIN, HAIR, EYES]", t, ts, acc=BROWN, size=110) if t >= ts else None
    return finish(f, n, look="warm")


# ---- S1: OPEN LOOP — 'the dip that keeps a lunchbox apple white till lunchtime' — a lunchbox with white slices + a timer ----
def shot_S1(t, n):
    f = set_lunch(t); u = lt(t, "S1")
    td = T("i3", "dip") - 0.1; tl = T("i3", "lunchtime.") - 0.15
    chub_table(f, 280, t, POSE["point"], mouth=talk(t), expr="happy", brow="up", look=(1, -0.2), hand_r="point", lean=4 + moving_hold(t, 2)["lean"])
    cloth_front(f, TABLE)
    lunchbox(f, 700, 1300, t, 0.0, 3, 1.0)
    if t >= td: comp(f, mchip("THE DIP: COMING UP", 30), 700, 760, scale=pin(t, td, 0.25))
    if t >= tl: comp(f, timer_el(0.25 * ramp(t, tl, 1.0), "LUNCH", 80), 880, 980, scale=pin(t, tl, 0.3))
    icap(f, "stick around for the dip that keeps it", "[WHITE]", t, st_("S1") + 0.05, acc=INKC, size=170)
    return finish(f, n, look="golden")


# ---- S2: PART 1 — 'an apple. Inside, millions of tiny cells' — powers-of-ten zoom from the apple into a wall of cells ----
def shot_S2(t, n):
    tm = T("a1", "millions") - 0.15
    def far():
        g = ink_set("applep", (255, 255, 255), 540, 1000, 440)
        comp(g, apple_el(0.0, False, "happy", (0, 0)), 540, 1020, scale=1.5 * pin(t, st_("S2"), 0.3))
        return g
    def near():
        g = ink_set("cream2", (255, 255, 255), 540, 1000, 440)
        for r_ in range(4):
            for c in range(3):
                comp(g, scale_el(cell_el(0.0, True, 3 + r_ * 3 + c, 640, 400), 0.52), 220 + c * 330 + (165 if r_ % 2 else 0), 640 + r_ * 220 + 3 * math.sin(t * 2 + c))
        comp(g, ichip("MILLIONS OF CELLS", 32), 540, 1420, scale=pin(t, tm + 0.3, 0.3))
        return g
    f = zoom_through(t, tm, 0.9, far, near, 540, 1020, 5.0)
    chapter_card(f, t, st_("S2") + 0.05, 1, "INSIDE THE APPLE", y=1440, dur=1.4, col=ACC_L)
    icap(f, "inside: millions of tiny", "[CELLS]", t, st_("S2") + 0.05, acc=ACC, size=180)
    return finish(f, n, look="fresh")


# ---- S2b: 'like little rooms with walls' — ONE cell = a room (big), labels ROOM / WALLS; Chubby stands beside the diagram ----
def shot_S2b(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S2b")
    tw = T("a1", "walls.") - 0.12
    comp(f, cell_el(0.0, True), 600, 980, scale=pin(t, st_("S2b"), 0.3))
    label_at(f, "A ROOM", 600, 700, t, st_("S2b") + 0.15, 600, 790, bg=INKC, fg=MILK, size=30)
    if t >= tw: label_at(f, "WALLS", 900, 1260, t, tw, 905, 1130, bg=ACC_S, fg=MILK, size=30)
    chub(f, 180, 1500, 0.85, t=t, **POSE["point"], mouth=talk(t), expr="n", brow="up", look=(1, -0.3), hand_r="point")
    icap(f, "little", "[ROOMS] with walls", t, st_("S2b") + 0.05, acc=INKC, size=150)
    return finish(f, n, look="fresh")


# ---- S3: 'two things are kept apart' — the divider wall lights up; two empty corners ringed ----
def shot_S3(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S3")
    ta = T("a2", "apart.") - 0.12
    comp(f, cell_el(0.0, True), 600, 980)
    k = ramp(t, ta - 0.1, 0.3)
    if k > 0:
        cv2.line(f, (600, 790), (600, 1170), C(ACC), max(1, int(10 * k)), cv2.LINE_AA)
        for sgn in (-1, 1): ring(f, 600 + sgn * 150, 980, 90 + 6 * math.sin(t * 6), INK_MINT_S if sgn < 0 else ACC_S, 7, k)
        comp(f, achip("KEPT APART", 32), 600, 1260, scale=pin(t, ta, 0.25))
    chub(f, 180, 1500, 0.85, t=t, **POSE["arms_out"], mouth=talk(t), expr="n", brow="up", look=(1, -0.3))
    icap(f, "two things kept", "[APART]", t, st_("S3") + 0.05, acc=ACC, size=190)
    return finish(f, n, look="fresh")


# ---- S3b: 'In one corner, an enzyme called PPO' — the mint machine snaps into the left corner, label ----
def shot_S3b(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S3b")
    tp = T("a2", "PPO:") - 0.12; te = T("a2", "enzyme") - 0.1
    comp(f, cell_el(0.0, True), 600, 980)
    comp(f, ppo_el("happy", (0.5, 0)), 440, 1000 + 3 * math.sin(t * 3), scale=1.1 * snap(t, st_("S3b") + 0.1, 5, 2.0))
    if t >= te: label_at(f, "AN ENZYME", 300, 700, t, te, 420, 900, bg=INK_MINT_S, fg=MILK, size=30)
    if t >= tp: slam(f, mchip("PPO", 56), 440, 1240, -4, t, tp)
    chub(f, 180, 1500, 0.85, t=t, **POSE["present"], mouth=talk(t), expr="happy", brow="up", look=(1, -0.3))
    icap(f, "in one corner, an enzyme called", "[PPO]", t, st_("S3b") + 0.05, acc=INK_MINT_S, size=190)
    return finish(f, n, look="fresh")


# ---- S3c: 'a tiny machine with one job' — PPO close-up: chimney puffs, a 'ONE JOB' tag ----
def shot_S3c(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440); u = lt(t, "S3c")
    tj = T("a2", "job.") - 0.12
    comp(f, ppo_el("happy", (0, 0)), 540, 1020 + 4 * math.sin(t * 2.5), scale=2.4 * pin(t, st_("S3c"), 0.3))
    steam_wisps(f, 420, 880, t, 3, 140, 60, (255, 255, 255), 0.7, 5)
    label_at(f, "TINY MACHINE", 540, 700, t, st_("S3c") + 0.15, 540, 860, bg=INKC, fg=MILK, size=30)
    if t >= tj: slam(f, mchip("ONE JOB", 48), 540, 1340, -3, t, tj)
    icap(f, "a tiny machine with", "[ONE JOB]", t, st_("S3c") + 0.05, acc=INK_MINT_S, size=160)
    return finish(f, n, look="fresh")


# ---- S4: 'In the other corner, polyphenols. The apple's own flavour chemicals' — beads snap into the right corner ----
def shot_S4(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S4")
    tp = T("a3", "polyphenols.") - 0.15; tf = T("a3", "flavour") - 0.1
    comp(f, cell_el(0.0, True), 600, 980)
    comp(f, ppo_el("n", (1, 0)), 440, 1000 + 3 * math.sin(t * 3), scale=1.1)
    for i, (dx, dy) in enumerate(((0, -60), (-40, 30), (50, 40))):
        comp(f, phenol_el("happy", (-0.6, 0), 1 + i), 760 + dx, 990 + dy + 4 * math.sin(t * 4 + i), scale=snap(t, tp - 0.05 + 0.08 * i, 4, 2.0))
    if t >= tp: slam(f, achip("POLYPHENOLS", 40), 760, 1240, 3, t, tp)
    if t >= tf: label_at(f, "FLAVOUR CHEMICALS", 840, 700, t, tf, 780, 900, bg=ACC_S, fg=MILK, size=28)
    chub(f, 180, 1500, 0.85, t=t, **POSE["point"], mouth=talk(t), expr="n", brow="up", look=(1, -0.3), hand_r="point")
    icap(f, "in the other corner:", "[POLYPHENOLS]", t, st_("S4") + 0.05, acc=ACC, size=130)
    return finish(f, n, look="fresh")


# ---- S4b: 'Fine, as long as the two never meet' — both sides wave; a NEVER MEET sign on the divider ----
def shot_S4b(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S4b")
    tn = T("a3", "never") - 0.12
    comp(f, cell_el(0.0, True), 600, 980)
    comp(f, ppo_el("happy", (1, 0)), 440, 1000 + 3 * math.sin(t * 3), scale=1.1)
    for i, (dx, dy) in enumerate(((0, -60), (-40, 30), (50, 40))):
        comp(f, phenol_el("happy", (-0.6, 0), 1 + i), 760 + dx, 990 + dy + 4 * math.sin(t * 4 + i))
    if t >= tn:
        slam(f, chip("NEVER MEET", INKC, MILK, 38), 600, 760, -4, t, tn)
        cv2.line(f, (600, 790), (600, 1170), C(ACC), 10, cv2.LINE_AA)
    chub(f, 180, 1500, 0.85, t=t, **POSE["shrug"], mouth=talk(t), expr="happy", brow="up", look=(1, -0.3))
    icap(f, "fine, as long as they", "[NEVER MEET]", t, st_("S4b") + 0.05, acc=ACC, size=140)
    return finish(f, n, look="fresh")


# ---- S5: 'Then you cut it. The knife smashes through thousands of walls' — the big knife drops through the cell; cracks; Chubby flinches ----
TCUT = T("b1", "cut") - 0.08


def shot_S5(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S5")
    ts = T("b1", "smashes") - 0.12
    k = clamp((t - TCUT) / 0.12)
    br = clamp(0.2 * k + 0.8 * ramp(t, ts - 0.1, 0.5))
    comp(f, cell_el(br, True), 600, 980)
    comp(f, ppo_el("wow" if t >= TCUT else "n", (1, 0)), 440 + 20 * settle(t, TCUT, 1.0, 16, 7), 1000 + 3 * math.sin(t * 3), scale=1.1)
    for i, (dx, dy) in enumerate(((0, -60), (-40, 30), (50, 40))):
        comp(f, phenol_el("wow" if t >= TCUT else "happy", (-0.6, 0), 1 + i), 760 + dx + 10 * settle(t, TCUT, 1.0, 14, 6), 990 + dy + 4 * math.sin(t * 4 + i))
    ky = -300 + (1120 + 300) * (k * k) if t >= TCUT - 0.1 else -300
    if t >= TCUT - 0.1: knife_ink_at(f, 600, ky, -90, 1.1)
    if t >= ts: comp(f, burst_el("SMASH!", ACC_L, INKC, 58), 880, 760, scale=pin(t, ts, 0.2))
    lean_, sq = flinch(t, TCUT, 0.8)
    chub(f, 180, 1500, 0.85, t=t, **(POSE["shock"] if t >= TCUT else POSE["point"]), mouth="o" if t >= TCUT else talk(t), expr="wow" if t >= TCUT else "n", brow="up", look=(1, -0.4), squash=sq,
         hair=(drag(t, lambda q: flinch(q, TCUT, 0.8)[0] * 1.5, 3, 1.0), 0))
    icap(f, "then you", "[CUT] it", t, st_("S5") + 0.05, acc=ACC, size=190)
    return finish(f, n, look="fresh")


# ---- S5b: 'And PPO meets the polyphenols' — the broken room: PPO slides over, hungry face, beads nervous ----
def shot_S5b(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S5b")
    tm = T("b1", "meets") - 0.12
    comp(f, cell_el(1.0, True), 600, 980)
    k = ramp(t, st_("S5b") + 0.05, max(0.4, tm - st_("S5b")))
    comp(f, ppo_el("hungry" if t >= tm - 0.2 else "happy", (1, 0)), 440 + 220 * k, 1000 + 3 * math.sin(t * 3), scale=1.1)
    for i, (dx, dy) in enumerate(((0, -60), (-40, 30), (50, 40))):
        comp(f, phenol_el("wow" if t >= tm - 0.2 else "n", (-0.8, 0), 1 + i), 760 + dx + 6 * math.sin(t * 14 + i) * (t >= tm - 0.2), 990 + dy + 4 * math.sin(t * 4 + i))
    if t >= tm: slam(f, chip("THEY MEET", ACC, INKC, 40), 600, 760, -3, t, tm)
    chub(f, 180, 1500, 0.85, t=t, **POSE["cheek"], mouth=talk(t), expr="sus", brow="sus", look=(1, -0.3))
    icap(f, "and PPO", "[MEETS] the polyphenols", t, st_("S5b") + 0.05, acc=ACC, size=110)
    return finish(f, n, look="fresh")


# ---- S6: 'And then the third guest walks in from the air. That's oxygen.' — O2 molecules float down through the crack; ink title OXYGEN ----
def shot_S6(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S6")
    tg = T("b2", "guest") - 0.1; to = T("b2", "oxygen.") - 0.15
    t3(f, "OXYGEN", 640, t, to, 230, BLUE_L, BLUE)
    comp(f, cell_el(1.0, True), 600, 980)
    comp(f, ppo_el("hungry", (0.5, -0.5)), 660, 1000 + 3 * math.sin(t * 3), scale=1.1)
    for i, (dx, dy) in enumerate(((0, -60), (-40, 30), (50, 40))):
        comp(f, phenol_el("n", (-0.4, -0.6), 1 + i), 760 + dx, 990 + dy + 4 * math.sin(t * 4 + i))
    rng = np.random.default_rng(5)
    for i in range(6):
        q = clamp((t - tg - 0.12 * i) / 1.1)
        if q <= 0: continue
        ox = 300 + rng.uniform(0, 500); oy = 300 + (900 + rng.uniform(-80, 80) - 300) * eio(q)
        comp(f, scale_el(o2_el(1 + i % 3, "happy" if t >= to else None), 0.8), ox + 16 * math.sin(t * 2 + i), oy)
    if t >= tg: label_at(f, "FROM THE AIR", 880, 1330, t, tg, 800, 1200, bg=INKC, fg=MILK, size=30)
    chub(f, 180, 1500, 0.85, t=t, **POSE["hold_up"], mouth=talk(t), expr="n", brow="up", look=(0.6, -0.8))
    icap(f, "and a third guest walks in:", "", t, st_("S6") + 0.05, acc=INKC, size=150, out=to - 0.05)
    return finish(f, n, look="fresh")


# ---- S7: 'PPO grabs the oxygen and the polyphenols and mashes them together' — the machine eats: beads + O2 into the funnel, munch ----
def shot_S7(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440); u = lt(t, "S7")
    tg = T("b3", "grabs") - 0.1; tm = T("b3", "mashes") - 0.12
    mch, _ = munch(t, 0.36)
    comp(f, ppo_el("munch" if (t >= tm and mch) else ("hungry" if t < tm else "happy"), (0.3, 0)), 420, 1020 + 4 * math.sin(t * 2.5) + (6 * math.sin(t * 20) if t >= tm else 0), scale=2.0)
    fx, fy = 420 + 2.0 * 95, 1020        # funnel mouth
    for i, (sx, sy, el) in enumerate(((900, 700, phenol_el("wow", (-1, 0), 1)), (940, 1000, scale_el(o2_el(2), 0.9)), (880, 1300, phenol_el("wow", (-1, 0), 2)), (820, 500, scale_el(o2_el(3), 0.9)), (960, 1200, phenol_el("wow", (-1, 0), 3)))):
        q = clamp((t - tg - 0.18 * i) / 0.7)
        if q >= 1: continue
        comp(f, el, sx + (fx - sx) * eio(q), sy + (fy - sy) * eio(q), scale=1 - 0.5 * q)
    if t >= tm: comp(f, burst_el("MASH!", INK_MINT, INKC, 54), 760, 820, scale=pin(t, tm, 0.2))
    label_at(f, "GRABS BOTH", 300, 720, t, tg, 420, 860, bg=INKC, fg=MILK, size=30)
    icap(f, "PPO grabs them and", "[MASHES] them", t, st_("S7") + 0.05, acc=INK_MINT_S, size=130)
    return finish(f, n, look="fresh")


# ---- S7b: 'At first the result is colourless' — out of the funnel come pale, dotted blobs; a 'COLOURLESS... for now' chip ----
def shot_S7b(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440); u = lt(t, "S7b")
    tc = T("b3", "colourless.") - 0.15
    comp(f, ppo_el("happy", (0.6, 0)), 360, 1020 + 4 * math.sin(t * 2.5), scale=1.8)
    for i in range(4):
        q = clamp((t - st_("S7b") - 0.2 * i) / 1.2)
        if q <= 0: continue
        comp(f, melanin_el(0.15, 1 + i, 46), 560 + 110 * i + 60 * q, 1010 - 40 * math.sin(math.pi * q) + 6 * math.sin(t * 3 + i), scale=(0.5 + 0.5 * eo(min(1, q * 2))) * 1.4)
    if t >= tc: slam(f, chip("COLOURLESS... for now", INKC, MILK, 34), 700, 760, -3, t, tc)
    icap(f, "at first the result is", "[COLOURLESS]", t, st_("S7b") + 0.05, acc=(150, 150, 150), size=130)
    return finish(f, n, look="fresh")


# ---- S8: 'those bits clump into bigger and bigger blobs' — pale blobs drift together and merge into one bigger blob ----
def shot_S8(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S8")
    tc = T("b4", "clump") - 0.12; tb = T("b4", "bigger", 1) - 0.1
    k = ramp(t, tc, max(0.6, tb - tc + 0.4))
    for i in range(8):
        a = i * 2 * math.pi / 8; r0 = 330 * (1 - k) + 20
        comp(f, melanin_el(0.2, 1 + i, 46), 540 + r0 * math.cos(a) + 5 * math.sin(t * 3 + i), 1000 + r0 * math.sin(a) * 0.8, scale=1.4, op=1 - 0.6 * k)
    comp(f, melanin_el(0.3, 9, 60), 540, 1000, scale=0.5 + 2.0 * k)
    if t >= tb: label_at(f, "BIGGER AND BIGGER", 540, 1380, t, tb, 540, 1160, bg=INKC, fg=MILK, size=30)
    icap(f, "those bits", "[CLUMP]", t, st_("S8") + 0.05, acc=INKC, size=190)
    return finish(f, n, look="fresh")


# ---- S8b: 'And the blobs are brown. That's melanin.' — the blob darkens to sepia; lights drop; ink 3D MELANIN; Chubby TAKE ----
def shot_S8b(t, n):
    f = ink_set("sepia", None); f *= 0.92
    tb = T("b4", "brown.") - 0.12; tm = T("b4", "melanin.") - 0.15
    k = ramp(t, tb - 0.1, 0.6)
    mood(f, (120, 70, 30), 0.3 * k)
    t3(f, "MELANIN", 640, t, tm, 230, BROWN_L, BROWN_D)
    comp(f, melanin_el(0.3 + 0.7 * k, 9, 60), 620, 1000, scale=2.5)
    spotlight(f, 620, 1000, 420, 0.3 * k, 240)
    tk = take(t, tb, 0.9, 8)
    pz = dict(POSE["shock"] if t >= tb else POSE["point"]); pz["lean"] = pz.get("lean", 0) + tk["lean"]
    chub(f, 200, 1500, 0.85, t=t, **pz, mouth="o" if tb <= t < tb + 0.5 else talk(t), expr=tk["expr"], brow=tk["brow"], look=(1, -0.4), squash=tk["squash"], bob=tk["dy"],
         hair=(drag(t, lambda q: take(q, tb, 0.9, 8)["dy"], 3, 0.8), 0))
    if t >= tb: slam(f, chip("BROWN", BROWN_D, MILK, 44), 620, 1300, -3, t, tb)
    icap(f, "and the blobs are", "[BROWN]", t, st_("S8b") + 0.05, acc=BROWN_L, size=190, dark=True, out=tm - 0.05)
    return finish(f, n, look="warm")


# ---- S9: 'Same family of pigment your skin makes in the sun' — split: Chubby tanning under the sun | the slice browning ----
def shot_S9(t, n):
    f = ink_set("sunny", (255, 255, 255), 540, 1000, 440); u = lt(t, "S9")
    ts = T("c1", "sun.") - 0.12
    k = ramp(t, st_("S9") + 0.2, max(0.8, ts - st_("S9")))
    def L(g):
        comp(g, sun_ink_el("happy"), 330, 740, scale=0.7)
        chub(g, 330, 1440, 0.78, t=t, **POSE["cheer"], mouth=3, expr="happy", brow="up", tint=0.4 * k)
    def R(g):
        comp(g, scale_el(apple_el(k, True), 1.1), 750, 1060)
    split_contrast(f, t, st_("S9") + 0.05, L, R, "YOUR SKIN", "THE APPLE", (240, 190, 70), ACC, 640, 1480, 0.35, st_("S9") + 0.3)
    icap(f, "same family of pigment your", "[SKIN] makes", t, st_("S9") + 0.05, acc=BROWN, size=140)
    return finish(f, n, look="golden")


# ---- S9b: 'The apple just does it a lot faster' — a clock spins over the browning half ----
def shot_S9b(t, n):
    f = set_lunch(t); u = lt(t, "S9b")
    tf = T("c1", "faster.") - 0.12
    clock_hand(f, 240, 420, t, 2.5)
    chub_table(f, 300, t, POSE["point"], mouth=talk(t), expr="smirk", brow="n", look=(1, 0.1), hand_r="point", tint=0.35)
    cloth_front(f, TABLE)
    comp(f, scale_el(board_ink_el(620), 0.9), 640, 1372)
    comp(f, scale_el(apple_el(clamp(0.3 + 0.7 * ramp(t, st_("S9b"), 1.4)), True), 0.72), 740, 1268)
    if t >= tf: slam(f, achip("A LOT FASTER", 40), 760, 760, -3, t, tf)
    icap(f, "the apple just does it a lot", "[FASTER]", t, st_("S9b") + 0.05, acc=ACC, size=170)
    return finish(f, n, look="golden")


# ---- S10: 'Why would an apple do that?' — Chubby think pose; the browned half with a WHY? chip ----
def shot_S10(t, n):
    f = ink_set("applep", (255, 255, 255), 540, 1000, 440); u = lt(t, "S10")
    comp(f, apple_el(1.0, True, "n", (0, 0)), 640, 1020, scale=1.4 * pin(t, st_("S10"), 0.3))
    comp(f, chip("WHY?", INKC, MILK, 60), 880, 720 + 5 * math.sin(t * 3), scale=pin(t, st_("S10") + 0.3, 0.3))
    chub(f, 200, 1500, 0.9, t=t, **POSE["think"], mouth=talk(t), expr="sus", brow="sus", look=(1, -0.3))
    icap(f, "why would an apple", "[DO THAT]?", t, st_("S10") + 0.05, acc=ACC, size=160)
    return finish(f, n, look="fresh")


# ---- S10b: 'a defence against bugs and germs getting in at the cut' — bugs march at the cut, hit the brown and turn away; ink DEFENCE ----
def shot_S10b(t, n):
    f = ink_set("applep", (255, 255, 255), 540, 1000, 440); u = lt(t, "S10b")
    td = T("c2", "defence") - 0.12; tb = T("c2", "bugs") - 0.1
    t3(f, "DEFENCE", 640, t, td, 230, ACC_L, ACC_S)
    comp(f, apple_el(1.0, True, "angry", (0, 0)), 400, 1040, scale=1.3)
    for i in range(5):
        q = clamp((t - tb - 0.15 * i) / 1.2)
        if q <= 0: continue
        bx = 1000 - 460 * eio(min(1, q * 1.6)) + (40 * clamp((q - 0.65) / 0.35)) * 3; by = 900 + i * 90 + 4 * math.sin(t * 6 + i)
        comp(f, scale_el(bug_el("ouch" if q > 0.62 else "hungry", (-1, 0) if q <= 0.62 else (1, 0), 1 + i % 4, ACC_L), 0.7), bx, by)
    if t >= tb: label_at(f, "BUGS + GERMS", 860, 720, t, tb, 820, 880, bg=ACC_S, fg=MILK, size=28)
    comp(f, ichip(SRC_U, 22), 540, 1462, op=clamp((u - 1.2) / 0.3))
    icap(f, "scientists think it's a", "[DEFENCE]", t, st_("S10b") + 0.05, acc=ACC, size=180, out=td - 0.05)
    return finish(f, n, look="fresh")


# ---- S11: 'Quick guess for you: is that brown bit going bad?' — Chubby to camera, the GUESS card; a held comic pause ----
def shot_S11(t, n):
    f = set_lunch(t) * 0.82; u = lt(t, "S11")
    tg = T("c3", "guess") - 0.1; tb = T("c3", "bad?") - 0.12
    spotlight(f, 400, 1100, 520, 0.4, 240)
    mh = moving_hold(t, 3, 1.0)
    chub_table(f, 340, t, POSE["think"], mouth=talk(t), expr="sus", brow="sus", look=(-0.3, -0.2), lean=-6 + mh["lean"], bob=mh["bob"])
    cloth_front(f, TABLE)
    comp(f, scale_el(slice_el(1.0, "sad", (0.6, -0.4)), 1.0), 760, 1270 + 3 * math.sin(t * 3))
    if t >= tg: slam(f, chip("QUICK GUESS", ACC, INKC, 46), 760, 760, -4, t, tg)
    if t >= tb: comp(f, chip("going bad?  YES / NO", INKC, MILK, 32), 760, 900, scale=pin(t, tb, 0.25))
    icap(f, "quick guess: is that brown bit", "[GOING BAD]?", t, st_("S11") + 0.05, acc=ACC_L, size=130, dark=True)
    return finish(f, n, look="night")


# ---- S11b: 'Nope. It's harmless.' — NOPE + HARMLESS stamps slam, a check mark; Chubby cheer ----
def shot_S11b(t, n):
    f = set_lunch(t); u = lt(t, "S11b")
    th = T("c4", "harmless.") - 0.12
    chub_table(f, 340, t, POSE["cheer"] if t >= th else POSE["present"], mouth=talk(t), expr="happy", brow="up", look=(0.6, -0.2))
    cloth_front(f, TABLE)
    comp(f, scale_el(slice_el(1.0, "happy", (0, 0)), 1.0), 760, 1270 + 3 * math.sin(t * 3))
    slam(f, stamp_el("NOPE", ACC, 70), 760, 760, -8, t, st_("S11b") + 0.02)
    if t >= th: slam(f, stamp_el("HARMLESS", INK_MINT_S, 60), 760, 920, 5, t, th); comp(f, check_el(50, True), 980, 1080, scale=pin(t, th + 0.1, 0.25))
    comp(f, ichip(SRC_I, 22), 540, 1462, op=clamp((t - th - 0.4) / 0.3))
    icap(f, "nope: it's", "[HARMLESS]", t, st_("S11b") + 0.05, acc=INK_MINT_S, size=170)
    return finish(f, n, look="golden")


# ---- S11c: 'It just goes a bit soft and looks sad' — the slice droops (soft) with a sad face; a 'SAME TASTE' chip ----
def shot_S11c(t, n):
    f = set_lunch(t); u = lt(t, "S11c")
    ts = T("c4", "soft") - 0.1; tsd = T("c4", "sad.") - 0.12
    chub_table(f, 340, t, POSE["shrug"], mouth=talk(t), expr="n", brow="up", look=(0.8, 0.2), lean=3)
    cloth_front(f, TABLE)
    k = ramp(t, ts, 0.5)
    comp(f, scale_xy(scale_el(slice_el(1.0, "sad" if t >= tsd else "n", (0, 0)), 1.0), 1 + 0.08 * k, 1 - 0.12 * k), 760, 1270 + 8 * k + 3 * math.sin(t * 3))
    comp(f, mchip("SAME APPLE, SAME TASTE", 28), 760, 760, scale=pin(t, st_("S11c") + 0.1, 0.25))
    if t >= ts: label_at(f, "A BIT SOFT", 900, 1000, t, ts, 820, 1240, bg=INKC, fg=MILK, size=28)
    icap(f, "it just goes a bit", "[SOFT]", t, st_("S11c") + 0.05, acc=INKC, size=180)
    return finish(f, n, look="golden")


# ---- S12: PART 2 THE FIXES — 'every trick does one of three things' — three rule cards with icons: NO OXYGEN / SLOW IT / SWITCH OFF ----
def shot_S12(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440); u = lt(t, "S12")
    items = [(scale_el(o2_el(1, "sad"), 1.3), "KEEP OXYGEN OUT", None), (scale_el(ppo_el("sleepy"), 0.9), "SLOW THE ENZYME", None), (scale_el(ppo_el("off"), 0.9), "SWITCH IT OFF", None)]
    ts = [T("d1", "oxygen") - 0.12, T("d1", "slows") - 0.12, T("d1", "switches") - 0.12]
    cast_card(f, items, t, ts, 1060, 300, "THE THREE RULES", T("d1", "three") - 0.1, MILK, 1.0)
    chapter_card(f, t, st_("S12") + 0.05, 2, "THE FIXES", y=1440, dur=1.4, col=INK_MINT)
    icap(f, "every trick does one of", "[THREE THINGS]", t, st_("S12") + 0.05, acc=INK_MINT_S, size=120)
    return finish(f, n, look="fresh")


# ---- S13: 'Lemon juice, the classic. The acid makes PPO sluggish' — Chubby squeezes a lemon half over the bowl; PPO goes sleepy ----
def shot_S13(t, n):
    f = set_lunch(t); u = lt(t, "S13")
    ta = T("d2", "acid") - 0.1; tsl = T("d2", "sluggish,") - 0.12
    chub_table(f, 300, t, dict(la=(30, 16), ra=(120, 50), lean=6), mouth=talk(t), expr="happy", brow="up", look=(1, 0.3), hand_r="grip",
               hold=scale_el(lemon_ink_el(True), 0.7), hold_off=(40, -60), hold_front=True)
    cloth_front(f, TABLE)
    comp(f, bowl_el(0.5, (250, 240, 170)), 720, 1350, scale=1.0)
    for i in range(3): comp(f, scale_el(slice_el(0.0, None, (0, 0), 2 + i, (252, 244, 190)), 0.6), 640 + i * 80, 1300 + 2 * math.sin(t * 3 + i))
    for i in range(4):
        q = ((t - st_("S13")) * 1.1 + i * 0.25) % 1.0
        if t >= st_("S13") + 0.3: cv2.circle(f, (int(600 + 10 * i), int(1080 + 200 * q * q)), 9, C(LEMON), -1, cv2.LINE_AA); cv2.circle(f, (int(600 + 10 * i), int(1080 + 200 * q * q)), 9, C(INKC), 2, cv2.LINE_AA)
    if t >= ta: comp(f, ppo_el("sleepy", (0, 0)), 900, 1040 + 4 * math.sin(t * 2), scale=snap(t, ta, 4, 2.0))
    if t >= tsl: label_at(f, "SLUGGISH", 900, 820, t, tsl, 900, 950, bg=INK_MINT_S, fg=MILK, size=30)
    icap(f, "lemon juice: the acid makes PPO", "[SLUGGISH]", t, st_("S13") + 0.05, acc=INK_MINT_S, size=130)
    return finish(f, n, look="golden")


# ---- S13b: 'and the vitamin C helps even more. A few minutes in there, done.' — VITAMIN C chip, a timer, the dipped slices stay white ----
def shot_S13b(t, n):
    f = set_lunch(t); u = lt(t, "S13b")
    tv = T("d2", "vitamin") - 0.1; tm = T("d2", "minutes") - 0.12; td = T("d2", "done.") - 0.1
    chub_table(f, 300, t, POSE["present"], mouth=talk(t), expr="happy", brow="up", look=(1, 0.1))
    cloth_front(f, TABLE)
    comp(f, bowl_el(0.5, (250, 240, 170)), 720, 1350, scale=1.0)
    for i in range(3): comp(f, scale_el(slice_el(0.0, None, (0, 0), 2 + i, (252, 244, 190)), 0.6), 640 + i * 80, 1300 + 2 * math.sin(t * 3 + i))
    if t >= tv: slam(f, chip("VITAMIN C: helps even more", INK_MINT_S, MILK, 30), 720, 760, -3, t, tv)
    if t >= tm: comp(f, timer_el(0.1 * ramp(t, tm, 1.0), "A FEW MIN", 80), 900, 980, scale=pin(t, tm, 0.3))
    if t >= td: comp(f, check_el(44, True), 1000, 1200, scale=pin(t, td, 0.25))
    comp(f, ichip(SRC_I, 22), 540, 1462, op=clamp((u - 0.8) / 0.3))
    icap(f, "and the", "[VITAMIN C] helps more", t, st_("S13b") + 0.05, acc=INK_MINT_S, size=120)
    return finish(f, n, look="golden")


# ---- S14: 'No lemon? Honey water. Two spoons of honey in a cup of water, dunk the slices' — honey jar, slices drop in with a splash ----
def shot_S14(t, n):
    f = set_lunch(t); u = lt(t, "S14")
    th = T("d3", "Honey") - 0.1; tw = T("d3", "water,") - 0.1; tdk = T("d3", "dunk") - 0.1
    chub_table(f, 300, t, dict(la=(30, 16), ra=(110, 60), lean=5), mouth=talk(t), expr="happy", brow="up", look=(1, 0.3), hand_r="pinch")
    cloth_front(f, TABLE)
    comp(f, bowl_el(0.55, (250, 214, 130)), 720, 1350, scale=1.0)
    comp(f, honey_jar_el(), 960, 1250, scale=0.8 * pin(t, th, 0.3))
    for i in range(3):
        q = clamp((t - tdk - 0.12 * i) / 0.5)
        y = 1000 + (1300 - 1000) * q * q
        comp(f, scale_el(slice_el(0.0, None, (0, 0), 2 + i, (250, 226, 160) if q >= 1 else None), 0.6), 640 + i * 80, y + 2 * math.sin(t * 3 + i))
        if q >= 1 and t < tdk + 0.12 * i + 0.9: cv2.ellipse(f, (640 + i * 80, 1290), (int(30 + 60 * (t - tdk - 0.12 * i - 0.5)), 8), 0, 0, 360, C(MILK), 4, cv2.LINE_AA)
    if t >= tw: comp(f, mchip("2 SPOONS HONEY : 1 CUP WATER", 26), 720, 760, scale=pin(t, tw, 0.25))
    if t >= tdk: comp(f, burst_el("DUNK!", INK_MINT, INKC, 50), 900, 980, scale=pin(t, tdk, 0.2))
    icap(f, "no lemon?", "[HONEY WATER]", t, st_("S14") + 0.05, acc=(240, 176, 60), size=150)
    return finish(f, n, look="golden")


# ---- S14b: 'The sugar coat keeps oxygen off' — close-up: a slice with a honey glaze; O2 bounce off it ----
def shot_S14b(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S14b")
    tc = T("d3", "coat") - 0.1; to = T("d3", "oxygen") - 0.1
    comp(f, scale_el(slice_el(0.0, "happy", (0, -0.5), 2, (250, 226, 160)), 1.7), 540, 1080 + 4 * math.sin(t * 2))
    k = ramp(t, tc, 0.4)
    if k > 0:
        cv2.ellipse(f, (540, 1080), (int(230 * k), int(250 * k)), 0, 0, 360, C((240, 176, 60)), 12, cv2.LINE_AA)
        label_at(f, "SUGAR COAT", 300, 760, t, tc, 400, 960, bg=(196, 130, 30), fg=MILK, size=30)
    for i in range(4):
        q = ((t - to) * 1.0 + i * 0.25) % 1.0 if t >= to else -1
        if q < 0: continue
        bx = 300 + i * 160; by = 500 + (960 - 500) * min(q, 0.5) * 2 - (120 * clamp((q - 0.5) * 2))
        comp(f, scale_el(o2_el(1 + i, "sad" if q > 0.5 else None), 0.9), bx + (60 * clamp((q - 0.5) * 2)) * (-1 if i % 2 else 1), by)
    if t >= to: comp(f, check_el(40, False), 860, 760, scale=pin(t, to + 0.2, 0.25))
    comp(f, ichip(SRC_N, 22), 540, 1462, op=clamp((u - 0.6) / 0.3))
    icap(f, "the sugar coat keeps", "[OXYGEN] off", t, st_("S14b") + 0.05, acc=(196, 130, 30), size=150)
    return finish(f, n, look="golden")


# ---- S15: 'Cold slows the enzyme, so the fridge buys you time' — the fridge-night place: slices on a shelf, PPO sleepy with zz ----
def shot_S15(t, n):
    f = set_fridge_night(t, 1.0); inkify(f)
    tf = T("d4", "fridge") - 0.1
    for i in range(3): comp(f, scale_el(slice_el(0.1, None, (0, 0), 2 + i), 0.7), 700 + i * 100, 1010 + 2 * math.sin(t * 2 + i))
    comp(f, ppo_el("sleepy", (0, 0)), 830, 1180 + 3 * math.sin(t * 1.5), scale=1.1 * pin(t, st_("S15") + 0.1, 0.3))
    chub(f, 300, 1500, 0.95, t=t, la=(30, 16), ra=(80, 40), mouth=talk(t), expr="n", brow="up", look=(1, -0.3), lean=4, hand_r="point")
    if t >= tf: slam(f, chip("BUYS YOU TIME", INK_MINT_S, MILK, 36), 830, 760, -3, t, tf)
    icap(f, "cold", "[SLOWS] the enzyme", t, st_("S15") + 0.05, acc=(170, 220, 255), size=130, dark=True)
    return finish(f, n, look="cool")


# ---- S15b: 'Heat switches it off for good: cooked apples never go brown' — the stove: a pot of stewing apples, PPO floats up 'OFF' ----
def shot_S15b(t, n):
    f = set_stove(t, on=1.0)
    to = T("d4", "off") - 0.1; tc = T("d4", "cooked") - 0.1
    comp(f, pot_el("steel", 0.6, 0.0, 0.0), 660, 1300 - 225 + 8)
    g = pot_geom(660, 1300 - 225 + 8, 1.0, "steel", 0.6)
    for i in range(4): comp(f, scale_el(slice_el(0.0, None, (0, 0), 2 + i, (250, 236, 200)), 0.5), g["xl"] + 60 + i * 60, g["y_surf"] + 30 + 4 * math.sin(t * 3 + i))
    side_flames(f, 660, 1300 - 2, t, 352, 1.0)
    steam_wisps(f, 660, g["y_rim"] - 40, t, 5, 200, 200, (255, 255, 255), 0.7, 3)
    k = ramp(t, st_("S15b") + 0.1, 1.0)
    comp(f, ppo_el("off", (0, 0)), 660 + 20 * math.sin(t * 2), g["y_rim"] - 60 - 260 * k, scale=1.0, op=1 - 0.5 * k)
    if t >= to: slam(f, chip("OFF FOR GOOD", ACC, INKC, 38), 880, 700, -4, t, to)
    chub(f, 250, 1500, 0.95, t=t, **POSE["present"], mouth=talk(t), expr="happy", brow="up", look=(1, -0.3))
    if t >= tc: comp(f, mchip("COOKED = NEVER BROWN", 28), 660, 880, scale=pin(t, tc, 0.25))
    comp(f, ichip(SRC_S, 22), 540, 1462, op=clamp((t - tc - 0.3) / 0.3))
    icap(f, "heat switches it", "[OFF] for good", t, st_("S15b") + 0.05, acc=ACC_L, size=150, dark=True)
    return finish(f, n, look="warm")


# ---- S16: PART 3 — 'Now the part nobody expects. Some foods go brown on purpose.' — lights drop, Chubby whispers; ink ON PURPOSE ----
def shot_S16(t, n):
    f = set_lunch(t) * 0.6; u = lt(t, "S16")
    tp = T("e1", "purpose.") - 0.15
    mood(f, (120, 80, 40), 0.3)
    t3(f, "ON PURPOSE", 700, t, tp, 200, ACC_L, ACC_S)
    chub_table(f, 420, t, POSE["whisper"], mouth=talk(t), expr="sus", brow="sus", look=(-0.4, -0.3))
    cloth_front(f, TABLE)
    spotlight(f, 440, 1050, 420, 0.5, 220)
    chapter_card(f, t, st_("S16") + 0.05, 3, "ON PURPOSE", y=1440, dur=1.4, col=ACC_L)
    icap(f, "the part nobody expects:", "", t, st_("S16") + 0.05, acc=MILK, size=150, dark=True, out=tp - 0.05)
    return finish(f, n, look="night")


# ---- S16b: 'Black tea gets its colour from this exact reaction, done on purpose' — a cup of black tea; PPO beside it ----
def shot_S16b(t, n):
    f = ink_set("sepia", (250, 236, 210), 540, 1000, 440); f *= 0.95; u = lt(t, "S16b")
    tr = T("e2", "reaction,") - 0.12
    comp(f, food_el("tea"), 540, 1040 + 4 * math.sin(t * 2), scale=2.0 * pin(t, st_("S16b"), 0.3))
    comp(f, scale_el(ppo_el("happy", (0, 0)), 0.9), 250, 860 + 3 * math.sin(t * 3), scale=pin(t, tr, 0.3))
    if t >= tr: label_at(f, "SAME REACTION", 250, 1160, t, tr, 320, 1000, bg=BROWN_D, fg=MILK, size=28)
    comp(f, achip("BLACK TEA", 36), 540, 760, scale=pin(t, st_("S16b") + 0.1, 0.25))
    comp(f, ichip(SRC_S, 22), 540, 1462, op=clamp((u - 1.0) / 0.3))
    icap(f, "black tea: this exact reaction,", "[ON PURPOSE]", t, st_("S16b") + 0.05, acc=BROWN, size=120)
    return finish(f, n, look="warm")


# ---- S16c: 'Coffee and cocoa too' — bean + pod snap in beside the tea ----
def shot_S16c(t, n):
    f = ink_set("sepia", (250, 236, 210), 540, 1000, 440); f *= 0.95; u = lt(t, "S16c")
    tc = T("e2", "cocoa") - 0.1
    comp(f, food_el("tea"), 300, 1040 + 4 * math.sin(t * 2), scale=1.2)
    comp(f, food_el("coffee"), 560, 1040 + 4 * math.sin(t * 2 + 1), scale=1.3 * snap(t, st_("S16c") + 0.05, 4, 2.0))
    if t >= tc: comp(f, food_el("cocoa"), 820, 1040 + 4 * math.sin(t * 2 + 2), scale=1.3 * snap(t, tc, 4, 2.0))
    for i, (x, w) in enumerate(((300, "TEA"), (560, "COFFEE"), (820, "COCOA"))):
        if i == 2 and t < tc: continue
        comp(f, achip(w, 28), x, 1260, op=clamp((t - (st_("S16c") if i < 2 else tc)) / 0.2))
    icap(f, "coffee and", "[COCOA] too", t, st_("S16c") + 0.05, acc=BROWN, size=150)
    return finish(f, n, look="warm")


# ---- S17: 'Avocados, bananas, potatoes: same enzyme, same trick' — three foods snap in and brown one by one ----
def shot_S17(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S17")
    ts = [T("e3", "Avocados,") - 0.12, T("e3", "bananas,") - 0.12, T("e3", "potatoes:") - 0.12]; te = T("e3", "same") - 0.1
    for i, (kind, x) in enumerate((("avocado", 270), ("banana", 540), ("potato", 810))):
        if t < ts[i]: continue
        comp(f, food_el(kind, clamp((t - ts[i] - 0.3) / 1.2)), x, 1000 + 4 * math.sin(t * 2 + i), scale=1.25 * snap(t, ts[i], 4, 2.0))
        comp(f, achip(kind.upper(), 24), x, 1200, op=clamp((t - ts[i]) / 0.2))
    if t >= te: slam(f, mchip("SAME ENZYME, SAME TRICK", 32), 540, 740, -3, t, te)
    chub(f, 540, 1520, 0.6, t=t, **POSE["present"], mouth=talk(t), expr="happy", brow="up", look=(0, -0.6))
    icap(f, "avocados, bananas, potatoes:", "[SAME TRICK]", t, st_("S17") + 0.05, acc=ACC, size=130)
    return finish(f, n, look="fresh")


# ---- S17b: 'That grey top layer on your guacamole? Melanin.' — avocado close-up browning; MELANIN chip; Chubby double take ----
def shot_S17b(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S17b")
    tm = T("e3", "Melanin.") - 0.15; tg = T("e3", "grey") - 0.1
    comp(f, food_el("avocado", clamp(0.4 + 0.6 * ramp(t, tg, 1.0))), 620, 1000 + 4 * math.sin(t * 2), scale=2.2 * pin(t, st_("S17b"), 0.3))
    if t >= tg: label_at(f, "THE GREY TOP LAYER", 620, 700, t, tg, 620, 860, bg=INKC, fg=MILK, size=28)
    look, lean, expr, brow = double_take(t, tm - 0.3)
    chub(f, 200, 1500, 0.85, t=t, la=(30, 16), ra=(96, 50), mouth=talk(t), expr=expr, brow=brow, look=look, lean=lean, hand_r="point", hair=(drag(t, lambda q: double_take(q, tm - 0.3)[1] * 2.0, 3, 1.0), 0))
    if t >= tm: slam(f, chip("MELANIN", BROWN_D, MILK, 48), 620, 1300, -3, t, tm)
    icap(f, "that grey top layer on your", "[GUACAMOLE]?", t, st_("S17b") + 0.05, acc=(90, 130, 60), size=130)
    return finish(f, n, look="fresh")


# ---- S18: 'And one apple can't do it at all: the Arctic apple' — a cut apple that stays white, snow motes, ARCTIC title ----
def shot_S18(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440); u = lt(t, "S18")
    ta = T("f1", "Arctic") - 0.12
    t3(f, "ARCTIC", 640, t, ta, 230, BLUE_L, BLUE)
    comp(f, apple_el(0.0, True, "happy", (0, 0), 1, True), 600, 1040, scale=1.4 * pin(t, st_("S18"), 0.3))
    dust_motes(f, t, 200, 400, 900, 1300, 20, 13, 0.9)
    chub(f, 200, 1500, 0.85, t=t, **POSE["point"], mouth=talk(t), expr="n", brow="up", look=(1, -0.3), hand_r="point")
    if t >= ta: slam(f, chip("THE ARCTIC APPLE", BLUE, MILK, 36), 600, 1340, -3, t, ta)
    icap(f, "one apple", "[CAN'T] do it", t, st_("S18") + 0.05, acc=ACC, size=160, out=ta - 0.05)
    return finish(f, n, look="cool")


# ---- S18b: 'Scientists switched off its PPO gene, so it stays white when you cut it' — a switch flips OFF, PPO greys out, stays white ----
def shot_S18b(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440); u = lt(t, "S18b")
    ts = T("f1", "switched") - 0.1; tw = T("f1", "white") - 0.12
    comp(f, apple_el(0.0, True, "happy" if t >= tw else "n", (0, 0), 1, True), 620, 1060, scale=1.3)
    comp(f, scale_el(switch_el(t < ts + 0.1), 0.7), 260, 900, scale=pin(t, st_("S18b"), 0.3))
    comp(f, ppo_el("off" if t >= ts + 0.1 else "n", (0, 0)), 260, 1180 + 3 * math.sin(t * 2), scale=0.9)
    if t >= ts: label_at(f, "PPO GENE: OFF", 260, 720, t, ts, 260, 800, bg=INKC, fg=MILK, size=28)
    if t >= tw: slam(f, chip("STAYS WHITE", BLUE, MILK, 40), 620, 760, -3, t, tw); comp(f, check_el(44, True), 880, 880, scale=pin(t, tw + 0.1, 0.25))
    icap(f, "PPO gene switched off: it", "[STAYS WHITE]", t, st_("S18b") + 0.05, acc=BLUE, size=120)
    return finish(f, n, look="cool")


# ---- S18c: 'Approved in the US back in twenty fifteen. The apple that never blushes.' — a 2015 stamp; the apple smug; Chubby smirk ----
def shot_S18c(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440); u = lt(t, "S18c")
    ta = T("f2", "fifteen.") - 0.15; tb = T("f2", "blushes.") - 0.15
    comp(f, apple_el(0.0, True, "smirk" if t >= tb else "happy", (0.4, 0), 1, True), 620, 1060, scale=1.3)
    if t >= ta: slam(f, stamp_el("USA 2015", BLUE, 56), 620, 760, -6, t, ta)
    if t >= tb: comp(f, achip("NEVER BLUSHES", 30), 620, 1340, scale=pin(t, tb, 0.25))
    chub(f, 200, 1500, 0.85, t=t, **POSE["cheek"], mouth=talk(t), expr="smirk", brow="n", look=(1, -0.3))
    comp(f, ichip(SRC_A, 22), 540, 1462, op=clamp((u - 0.5) / 0.3))
    icap(f, "the apple that", "[NEVER BLUSHES]", t, st_("S18c") + 0.05, acc=ACC, size=120)
    return finish(f, n, look="cool")


# ---- S19: RECAP — cut -> enzyme + oxygen -> melanin; then the fixes row; 'brown is fine' ----
def shot_S19(t, n):
    f = ink_set("applep", (255, 255, 255), 540, 1000, 440)
    items = [(scale_el(cell_el(1.0, True), 0.36), "THE CUT"), (scale_el(ppo_el("hungry"), 1.0), "ENZYME + O2"), (scale_el(melanin_el(1.0, 9, 60), 0.9), "MELANIN")]
    ts = [T("g1", "cut") - 0.15, T("g1", "enzyme") - 0.15, T("g1", "melanin.") - 0.15]
    recap_steps(f, items, 900, t, ts, 300, 1.0)
    for i, (w, tt) in enumerate((("LEMON", T("g1", "Lemon,") - 0.1), ("HONEY", T("g1", "honey") - 0.1), ("COLD", T("g1", "cold") - 0.1), ("HEAT", T("g1", "heat") - 0.1))):
        if t >= tt: comp(f, mchip(w, 30), 200 + i * 227, 1260, scale=pin(t, tt, 0.25))
    tf = T("g1", "fine") - 0.12
    if t >= tf: slam(f, chip("BROWN IS FINE TO EAT", ACC, INKC, 34), 540, 1400, -3, t, tf)
    icap(f, "", "[REMEMBER]", t, st_("S19") + 0.05, acc=ACC, size=200)
    return finish(f, n, look="fresh")


# ---- S20: send it + FreshNestHub sting ----
def shot_S20(t, n):
    f = set_lunch(t) * 0.95
    vend = LINES["g2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("g2", "Send") + 0.3
        comp(f, scale_el(phone2_el("the apple went brown AGAIN", "it's fine. eat it.", pr), 0.82), 700, 950, scale=pin(t, st_("S20")))
        if pr and t < T("g2", "Send") + 0.75:
            rr = (t - T("g2", "Send") - 0.3) / 0.45
            cv2.circle(f, (700, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub_table(f, 280, t, POSE["point"], mouth=talk(t), expr="happy", brow="up", look=(1, 0), hand_r="point")
        cloth_front(f, TABLE)
        comp(f, scale_el(slice_el(0.8, "happy"), 0.8), 770, 1280)
        ui_word(f, "send to the friend who throws away", "[BROWN APPLE]", 420, t, T("g2", "friend") - 0.1, col=INKC, acc=ACC, size=110, shadow=0.0, lead_col=INKC)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INKC, lead_size=42), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub_table(f, 230, t, POSE["cheer"], mouth=3, expr="happy", brow="up", s=0.85)
        cloth_front(f, TABLE)
        comp(f, scale_el(apple_el(0.0, False), 0.5 * k), 800, 1300)
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TTAN, 0.4, 18), (T("i2", "melanin,") - 0.15, 0.3, 12), (T("i3", "dip") - 0.1, 0.25, 8),
           (T("a1", "millions") - 0.15, 0.3, 10), (T("a2", "apart.") - 0.12, 0.25, 8), (T("a2", "PPO:") - 0.12, 0.3, 12),
           (T("a3", "polyphenols.") - 0.15, 0.3, 12), (T("a3", "never") - 0.12, 0.25, 8), (TCUT, 0.45, 20), (T("b1", "smashes") - 0.12, 0.3, 14),
           (T("b1", "meets") - 0.12, 0.3, 10), (T("b2", "oxygen.") - 0.15, 0.3, 12), (T("b3", "mashes") - 0.12, 0.35, 14),
           (T("b3", "colourless.") - 0.15, 0.25, 8), (T("b4", "brown.") - 0.12, 0.35, 14), (T("b4", "melanin.") - 0.15, 0.4, 16),
           (T("c1", "faster.") - 0.12, 0.3, 10), (T("c2", "defence") - 0.12, 0.35, 14), (T("c3", "guess") - 0.1, 0.25, 8),
           (st_("S11b") + 0.02, 0.35, 14), (T("c4", "harmless.") - 0.12, 0.3, 12), (st_("S12") + 0.1, 0.3, 12),
           (T("d2", "sluggish,") - 0.12, 0.3, 10), (T("d2", "vitamin") - 0.1, 0.25, 8), (T("d3", "dunk") - 0.1, 0.35, 14),
           (T("d3", "coat") - 0.1, 0.25, 8), (T("d4", "fridge") - 0.1, 0.25, 8), (T("d4", "off") - 0.1, 0.35, 14),
           (T("e1", "purpose.") - 0.15, 0.35, 14), (T("e2", "reaction,") - 0.12, 0.25, 8), (T("e3", "same") - 0.1, 0.3, 10),
           (T("e3", "Melanin.") - 0.15, 0.35, 14), (T("f1", "Arctic") - 0.12, 0.3, 12), (T("f1", "white") - 0.12, 0.3, 12),
           (T("f2", "fifteen.") - 0.15, 0.3, 12), (T("g1", "fine") - 0.12, 0.3, 10), (T("g2", "Send") + 0.3, 0.2, 8)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


def _bl(x, s_):
    if s_ < 0.5: return x
    sm = cv2.resize(x, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    return cv2.resize(cv2.GaussianBlur(sm, (0, 0), s_ / 4), (W, H), interpolation=cv2.INTER_LINEAR)


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); k = sh["trans"]; dt = t - sh["start"]
    if i > 0:
        if k == "focus" and dt < 0.34:
            p = dt / 0.34; prv = rs(SHOTS[i - 1]["id"], t, n); m = eio(p)
            f = _bl(prv, 40 * m) * (1 - m) + _bl(f, 40 * (1 - m)) * m
        elif k == "iris" and dt < 0.42:
            cx, cy = IRIS.get(sh["id"], (540, 1000))
            f = iris_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42, cx, cy)
        elif k == "whip" and dt < 0.22:
            p = 1 - dt / 0.22; M = np.float32([[1, 0, -360 * p * p], [0, 1, 0]])
            f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
        elif k == "zoom" and dt < 0.2:
            p = 1 - dt / 0.2; acc = np.zeros_like(f)
            for q in range(5): acc += cam(f, 1 + 0.06 * q * p)
            f = acc / 5
        elif k == "flash" and dt < 0.14: f = f + 0.8 * (1 - dt / 0.14) ** 1.5
        elif k == "punch" and dt < 0.16: f = cam(f, 1 + 0.08 * (1 - dt / 0.16)) + 0.12 * (1 - dt / 0.16)
    nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    if nx is not None and nx["trans"] == "whip" and sh["end"] - t < 0.14:
        p = 1 - (sh["end"] - t) / 0.14; M = np.float32([[1, 0, 360 * p * p], [0, 1, 0]])
        f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
