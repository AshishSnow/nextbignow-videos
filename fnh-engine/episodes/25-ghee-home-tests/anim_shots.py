# ================= shots: FreshNestHub 25 — "Can you test ghee at home?" (Chubby INK, ep 9 of the ink look) ===
# COLOUR SCRIPT: GHEE GOLD glows (translucent, lit from behind) = the real thing, always warm. Fakes are paler + colder. Court wood = neutral. RED = stamps only. Mint fridge cold for the one test that gives a clue.
# THE IDEA: the home tests are put ON TRIAL by Judge Chubby, one by one, on a verdict board you can screenshot. The hero craft: TRANSLUCENCY (_tl_fill). Acting: eyes lead the head (eye_lead), a real gavel with arm IK.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "Youve") - 0.15, "whip"), ("S1b", T("i2", "A") - 0.1, "zoom"), ("S1c", T("i2", "everybody") - 0.1, "punch"), ("S2", T("i3", "So") - 0.2, "flash"), ("S2b", T("i3", "Only") - 0.1, "whip"),
    ("S3", T("a1", "First") - 0.2, "whip"), ("S3b", T("a1", "cooked") - 0.1, "punch"), ("S3c", T("a1", "gone") - 0.25, "flash"), ("S4", T("a2", "The") - 0.15, "whip"), ("S4b", T("a2", "like") - 0.08, "punch"), ("S5", T("a3", "Last") - 0.15, "focus"), ("S5b", T("a3", "in", 1) - 0.08, "zoom"),
    ("S6", T("b1", "Test") - 0.2, "whip"), ("S6b", T("b1", "If") - 0.08, "punch"), ("S7", T("b2", "Sure") - 0.12, "cut"), ("S8", T("c1", "Test") - 0.2, "whip"), ("S8b", T("c1", "Your", 1) - 0.08, "zoom"), ("S9", T("c2", "But") - 0.15, "flash"), ("S9b", T("c2", "melts") - 0.08, "punch"), ("S9c", T("c2", "So") - 0.1, "whip"), ("S10", T("c3", "And") - 0.15, "focus"), ("S10b", T("c3", "Which") - 0.08, "punch"),
    ("S11", T("d1", "Test") - 0.2, "whip"), ("S11b", T("d1", "so") - 0.08, "punch"), ("S12", T("d2", "Nice") - 0.12, "cut"), ("S13", T("e1", "Test") - 0.2, "whip"), ("S14", T("e2", "Buffalo") - 0.12, "flash"), ("S14b", T("e2", "and") - 0.08, "whip"),
    ("S15", T("f1", "Four") - 0.2, "flash"), ("S15b", T("f1", "Bring") - 0.08, "punch"), ("S16", T("f2", "Iodines") - 0.15, "whip"), ("S16b", T("f2", "He") - 0.08, "punch"), ("S17", T("f3", "The") - 0.15, "whip"), ("S17b", T("f3", "It") - 0.08, "zoom"), ("S18", T("f4", "Clever") - 0.15, "focus"), ("S18b", T("f4", "No") - 0.08, "whip"), ("S19", T("f5", "And") - 0.15, "flash"),
    ("S20", T("g1", "Which") - 0.25, "cut"), ("S20b", T("g1", "And") - 0.08, "punch"), ("S21", T("g2", "A") - 0.15, "whip"), ("S21b", T("g2", "Pure") - 0.08, "zoom"), ("S22", T("g3", "Mix") - 0.12, "punch"), ("S23", T("g4", "Its") - 0.15, "flash"), ("S23b", T("g4", "Ghee") - 0.08, "whip"), ("S24", T("g5", "So") - 0.15, "punch"), ("S24b", T("g5", "No") - 0.08, "whip"),
    ("S25", T("h1", "Why") - 0.2, "focus"), ("S25b", T("h1", "even") - 0.08, "punch"), ("S26", T("h2", "But") - 0.12, "whip"), ("S26b", T("h2", "About") - 0.08, "punch"), ("S27", T("h3", "A") - 0.12, "whip"), ("S27b", T("h3", "Your") - 0.08, "cut"),
    ("S28", T("k1", "So") - 0.2, "flash"), ("S29", T("k2", "Look") - 0.12, "whip"), ("S29b", T("k2", "Those") - 0.08, "punch"), ("S30", T("k3", "And") - 0.12, "whip"), ("S30b", T("k3", "That") - 0.08, "punch"), ("S31", T("k4", "Buy") - 0.12, "whip"), ("S31b", T("k4", "and") - 0.08, "punch"),
    ("S32", T("l1", "So") - 0.2, "cut"), ("S33", T("l2", "Send") - 0.15, "whip"),
]


SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}

def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def icap(f, lead, big, t, t0, acc=ACC_S, size=150, y=440, out=None, tail="", dark=False):
    if dark: ui_word(f, lead, big, y, t, t0, col=WHITE, acc=ACC_L, size=size, shadow=0.6, lead_col=WHITE, out=out, tail=tail)
    else: ui_word(f, lead, big, y, t, t0, col=INKC, acc=acc, size=size, shadow=0.0, lead_col=INKC, out=out, tail=tail)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def t3(f, text, y, t, t0, size=230, face=None, side=None, x=540):
    if t >= t0: title_ink(f, text, y, t, t0, size=size, face=face or ACC_L, side=side or ACC_S, depth=18, x=x)


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, MILK, 22), 540, y, op=clamp((t - t0) / 0.2))


def cc(f, text, x, y, t, t0, bg=None, fg=None, size=34):
    if t >= t0: comp(f, chip(text, bg or INKC, fg or MILK, size), x, y, scale=pin(t, t0))


def verdict(f, text, t, t0, x=540, y=760, col=None, size=110, rot=-6):
    slam(f, vstamp_el(text, col or RED_V, size), x, y, rot, t, t0)


def paper_bg(sx=540, sy=980, R=600): return ink_set("paper", (255, 255, 255), sx, sy, R)


def judge(f, x, y, s, t, lean=0.0, **kw):
    kw.setdefault("mouth", talk(t))
    chub(f, x, y, s, t=t, shirt=ROBE, lean=lean, **kw)
    judge_wig(f, x, y, s, lean)


def bang(t, t0, up=1.0):
    """gavel timing: anticipation (it rises slowly before), 3 frames down, a small bounce. -> 0 (up) .. 1 (down on the block)"""
    q = (t - t0) * FPS
    if q < -8: return 0.0
    if q < 0: return -0.12 * (q + 8) / 8
    if q < 3: return q / 3
    if q < 8: return 1 - 0.14 * math.sin((q - 3) / 5 * math.pi)
    return 1.0 - clamp((q - 8) / 10) * 0.98


def judge_gavel(f, x, y, s, t, tslams, top=1250, **kw):
    """Judge Chubby with a real gavel: arm IK to the grip; the block sits on the bench. Draw bench_front AFTER this; call gavel_top after bench to keep the hand in front."""
    k = max([bang(t, ts) for ts in tslams if abs(t - ts) < 2.0] + [0.0])
    bx, by = x + 340 * s, top - 22
    gx = x + 240 * s - 40 * s * k; gy = y - 400 * s + (by - 70 - (y - 400 * s)) * clamp(k)
    ang = 62 - 74 * clamp(k)
    sh = (x + 118 * s, y - 261 * s); a1, a2 = arm_ik(sh, (gx, gy), 76 * s, 70 * s)
    judge(f, x, y, s, t, ra=(a1, a2), hand_r="grip", **kw)
    return dict(gx=gx, gy=gy, ang=ang, bx=bx, by=by, k=k, s=s)


def gavel_top(f, g):
    comp(f, scale_el(block_el(), g["s"]), g["bx"], g["by"])
    gavel_at(f, g["gx"], g["gy"], g["ang"], g["s"] * 0.95); grip_hand(f, g["gx"], g["gy"], g["s"] * 0.9, 0.0, "grip", 0)


def peek(f, t, x, y, s, expr="sus", look=(0, 0)):
    """a reaction: Chubby's head in a corner of a diagram shot, so he stays the actor on every picture."""
    chub_head_only(f, x, y, s, t, mouth=talk(t), expr=expr, brow="sus" if expr == "sus" else "up", look=look, turn=clamp(look[0]) * 0.5)


def hand_at(f, x, y, s=1.0, rot=0.0, shadow=0.25):
    rot_comp(f, scale_el(hand_big_el(), s), x, y, rot, 1.0, 1.0, shadow)


SRC_K = "Source: Karmactive, 26 Oct 2026 · Deccan Herald"
SRC_D = "Source: DeshGujarat, 26 Oct 2026 (police allegation, lab report awaited)"
SRC_P = "Source: J Food Sci Technol 2014 (palm olein 26.3 °C)"
SRC_G = "Source: The Better India 2024 · Deccan Herald (S. Arya, ICT)"
SRC_F = "Source: FSSAI table via CSE (2012)"
SRC_S = "Source: FSSAI table via CSE · Indian J Anim Sci 2019"
SRC_A = "Source: S. Arya (ICT) in Deccan Herald · FSSAI Media Compendium"
SRC_Q = "Ten shop ghees: 1 to 40 % grain (Int J Dairy Technol 2013)"
SRC_H = "Source: Indian J Dairy Sci 2020"
TI = T("i1", "oil") - 0.08


# ---- S0: HOOK: frame 0, a dollop of ghee is sliding down a big backlit palm. On 'oil' a palm tree SHOOTS out of it. Chubby: take + jaw ----
def shot_S0(t, n):
    f = set_worktop(t); tree = t >= TI; tk = take(t, TI + 0.02)
    chub(f, 170, 1500 + (tk["dy"] if tree else 0), 0.92, t=t, la=(24, 14), ra=(70, 50), mouth=("jaw" if TI + 0.05 < t < TI + 0.9 else talk(t)), expr=tk["expr"] if tree else "happy", brow=tk["brow"] if tree else "up", look=(1, -0.1 if tree else 0.1), lean=tk["lean"] if tree else 3, squash=tk["squash"] if tree else 0, turn=0.5)
    hx, hy = 650, 1190
    glow(f, hx, hy - 60, 480, GHEE_HOT, 0.28)
    hand_at(f, hx, hy, 0.86, 3 * math.sin(t * 1.1))
    sl = 40 + 110 * ramp(t, 0.0, TI + 0.1); k_ = 0.25 + 0.5 * ramp(t, 0.0, TI)
    blob(f, hx, hy + 20 + sl, 92, k_, t, slide=sl)
    if tree:
        palm_tree(f, hx, hy + 40 + sl, 0.9, snap(t, TI, 6, 2.2), t, "happy")
    icap(f, "do you know the palm test", "can't catch [PALM OIL]?", t, 0.04, size=92, y=330)
    return finish(f, n, look="warm")


# ---- S1: 'You've seen it.' a phone: the reel everyone forwards ----
def shot_S1(t, n):
    f = set_droom(t, dim=0.15); t0 = st_("S1")
    x0, y0, x1, y1 = phone_frame(f, 650, 900, 560, 980)
    hand_at(f, (x0 + x1) // 2, y1 - 300, 0.62, 0, 0)
    blob(f, (x0 + x1) // 2, y1 - 280 + 20 * ramp(t, t0, 1.0), 62, 0.5, t)
    cc(f, "PURE OR FAKE?", (x0 + x1) // 2, y0 + 90, t, t0 + 0.05, RED_V, MILK, 40)
    for j in range(6):
        p = ((t - t0) * 0.5 + j * 0.17) % 1
        comp(f, scale_el(heart_el(), 0.7), x1 - 50 + 18 * math.sin(p * 8 + j), y1 - 90 - p * 460, op=clamp(3 * (1 - p)))
    chub(f, 200, 1500, 1.02, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="smirk", brow="up", look=(1, -0.1), hand_r="point", turn=0.5)
    table_front(f, 1410)
    icap(f, "you've", "[SEEN IT]", t, t0 + 0.04, size=120, y=320)
    return finish(f, n, look="warm")


# ---- S1b: 'A little on your hand, it melts, it slides': close-up: the translucent dollop, lit from behind ----
def shot_S1b(t, n):
    f = paper_bg(); t0 = st_("S1b"); tm = T("i2", "melts") - 0.1; ts = T("i2", "slides") - 0.1
    glow(f, 540, 980, 620, GHEE_HOT, 0.3)
    hand_at(f, 540, 1210, 1.12)
    k_ = 0.05 + 0.75 * ramp(t, tm, 0.7); sl = 170 * ramp(t, ts, 0.9)
    blob(f, 540, 1050 + sl, 150, k_, t, slide=sl)
    if t < tm: icap(f, "a little on", "your [HAND]", t, t0 + 0.03, size=120, y=360)
    elif t < ts: icap(f, "it", "[MELTS]", t, tm, size=150, y=380)
    else: icap(f, "it", "[SLIDES]", t, ts, size=150, y=380)
    return finish(f, n, look="golden")


# ---- S1c: 'everybody nods. Pure.' three people nod in time; PURE stamps ----
def shot_S1c(t, n):
    f = set_droom(t); tp = T("i2", "Pure") - 0.1
    for i, (x, kind, shirt, s_) in enumerate(((210, "aunty", (230, 70, 130), 0.92), (540, None, None, 1.1), (870, "boss", (70, 130, 190), 0.92))):
        kw = dict(shirt=shirt) if shirt else {}
        nod = 6 * math.sin(t * 7.5 + i * 0.5); ly = 0.5 * math.sin(t * 7.5 + i * 0.5)
        chub(f, x, 1500, s_, t=t, **{k: v for k, v in POSE["idle"].items()}, mouth=2, expr="happy", brow="up", look=(0.0, ly), bob=nod, **kw)
        if kind: dress(f, x, 1500, s_, kind, 0)
    verdict(f, "PURE", t, tp, 540, 640, ACC_S, 140)
    return finish(f, n, look="warm")


# ---- S2: 'let's put these home tests on trial': the COURTROOM: gavel comes down on 'trial' ----
def shot_S2(t, n):
    f = set_court(t); t0 = st_("S2"); tr = T("i3", "trial") - 0.1
    t3(f, "ON TRIAL", 560, t, tr, 170)
    g = judge_gavel(f, 500, 1560, 1.3, t, [tr], expr="sus" if t < tr else "n", brow="sus" if t < tr else "up", look=(0.6, 0.2) if t < tr else (0, 0))
    bench_front(f, 1250); gavel_top(f, g)
    return finish(f, n, look="warm")


# ---- S2b: 'Only one's worth your time.' the defendants in a row; one gets the ring ----
def shot_S2b(t, n):
    f = set_court(t, dim=0.45); t0 = st_("S2b"); to = T("i3", "ones") - 0.1
    items = ("water", "palm", "smell", "colour", "iodine", "acid", "fridge")
    for i, kind in enumerate(items):
        x = 200 + (i % 4) * 226 + (113 if i >= 4 else 0); y = 700 if i < 4 else 930
        cv2.circle(f, (x, y), 92, C((250, 244, 228)), -1, cv2.LINE_AA); cv2.circle(f, (x, y), 92, C(INKC), 6, cv2.LINE_AA)
        comp(f, test_icon_el(kind), x, y, scale=pin(t, t0 + i * 0.05, 0.2) * 1.05)
    if t >= to:
        k = t - to
        cv2.circle(f, (200 + 2 * 226 + 113, 930), int(106 + 6 * math.sin(k * 8)), C(ACC), 11, cv2.LINE_AA)
    chub_head_only(f, 540, 1200, 0.72, t, mouth=talk(t), expr="smirk", brow="up", look=(0, -0.8)); judge_wig(f, 540, 1200 + 420 * 0.72, 0.72)
    bench_front(f, 1290, plate=False)
    icap(f, "only", "[ONE]'s worth your time", t, to, size=80, y=430, dark=True)
    return finish(f, n, look="warm")


# ---- S3: 'First, the real thing. Ghee is butter': a block of butter in a kadai on the stove ----
def shot_S3(t, n):
    f = inkify(set_stove(t, on=0.8, flame_w=300), 0.1); t0 = st_("S3"); tb = T("a1", "butter") - 0.1
    comp(f, kadai_el(), 610, 1160)
    side_flames(f, 610, 1298, t, 300, 0.7)
    if t >= tb - 0.25: comp(f, scale_el(butter_el(), 2.6), 610, 1040 + 14 * math.sin(t * 2), scale=pin(t, tb - 0.25))
    chub(f, 170, 1500, 0.98, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="happy", brow="up", look=(1, 0.2), hand_r="point", turn=0.5)
    icap(f, "first, the", "[REAL] thing", t, t0 + 0.04, size=120, y=360)
    return finish(f, n, look="warm")


def shot_S3b(t, n):
    f = inkify(set_stove(t, on=0.8, flame_w=300), 0.1); t0 = st_("S3b")
    comp(f, kadai_el(), 610, 1160); side_flames(f, 610, 1298, t, 300, 0.8)
    blob(f, 610, 1056, 140, 0.7 + 0.2 * ramp(t, t0, 0.6), t)
    fly_drops(f, (610, 1020), (760, 560), t, n=11, rate=1.1, seed=5, s=0.3, arc=-100)
    steam_wisps(f, 610, 980, t, 4, 240, 170)
    cc(f, "THE WATER LEAVES", 700, 490, t, t0 + 0.1, (60, 120, 170), MILK, 38)
    chub(f, 170, 1500, 0.98, t=t, **nolean(POSE["present"]), mouth=talk(t), expr="wow", brow="up", look=(1, -0.4), turn=0.5, lean=3)
    return finish(f, n, look="warm")


# ---- S3c: 'gone': the hero jar lit from behind: TRANSLUCENT gold (the new craft) ----
def shot_S3c(t, n):
    f = set_worktop(t); t0 = st_("S3c")
    glow(f, 620, 980, 620, GHEE_HOT, 0.42)
    t3(f, "GHEE", 540, t, t0 + 0.06, 220)
    worktop_front(f, 1330)
    comp(f, scale_el(ghee_jar_el("liquid", 0.86, "happy", (0, 0)), 1.5), 640, 1040, scale=snap(t, t0, 5))
    chub(f, 190, 1500, 0.95, t=t, **nolean(POSE["cheek"]), mouth=talk(t), expr="happy", brow="up", look=(1, -0.2), turn=0.5, lean=-3)
    cc(f, "ALMOST PURE MILK FAT", 620, 1395, t, t0 + 0.25, ACC_S, MILK, 34)
    return finish(f, n, look="golden")


# ---- S4: 'The fake's built from cheaper fats': a jar with a price tag dropping ----
def shot_S4(t, n):
    f = set_worktop(t, blur=7); t0 = st_("S4"); tc = T("a2", "cheaper") - 0.1
    worktop_front(f, 1330)
    comp(f, scale_el(ghee_jar_el("smooth", 0.8, "smirk", (-0.6, 0)), 1.3), 660, 1060)
    chub(f, 210, 1500, 0.98, t=t, **POSE["think"], mouth=talk(t), expr="sus", brow="sus", look=(1, 0), turn=0.5)
    icap(f, "the", "[FAKE]", t, t0 + 0.03, size=150, y=380)
    if t >= tc: slam(f, burst_el("CHEAPER", (255, 220, 90), RED_V, 56), 810, 760, 8, t, tc)
    return finish(f, n, look="cool")


def shot_S4b(t, n):
    f = paper_bg(); t0 = st_("S4b"); tp = T("a2", "palm") - 0.1; tv = T("a2", "vanuspatee") - 0.1
    palm_tree(f, 300, 1250, 0.95, snap(t, tp, 6, 2.0) if t >= tp else 0, t, "smirk")
    if t >= tp: cc(f, "PALM OIL", 300, 1310, t, tp + 0.1, INKC, MILK, 40)
    if t >= tv: comp(f, scale_el(vanaspati_el("smirk"), 1.15), 760, 1060, scale=snap(t, tv, 5))
    if t >= tv: cc(f, "VANASPATI", 760, 1310, t, tv + 0.1, INKC, MILK, 40)
    icap(f, "", "CHEAPER [FATS]", t, t0, size=118, y=380)
    return finish(f, n, look="cool")


# ---- S5: 'Last month in Junagadh, police say they found...': a dark store, a torch finds the shelf ----
def shot_S5(t, n):
    f = set_store(t); t0 = st_("S5"); dur = en_("S5") - t0; p = (t - t0) / max(0.1, dur)
    for (x, el_, s_) in ((300, oil_bottle_el(), 1.0), (480, oil_bottle_el(), 1.0)): comp(f, scale_el(el_, s_), x, 1085)
    for x in (660, 750, 840, 930): comp(f, scale_el(essence_el(None, seed=121 + x), 0.72), x, 1100)
    bx = 320 + 540 * ramp(p, 0.1, 0.85)
    torch_beam(f, 210, 1240, bx, 1060, 250, 0.75)
    f *= 0.72
    chub(f, 150, 1500, 0.86, t=t, la=(24, 14), ra=(70, 60), mouth=talk(t), expr="sus", brow="sus", look=(1, -0.1), turn=0.5, cap=True, hand_r="grip")
    cv2.line(f, (int(150 + 150), 1272), (int(150 + 210), 1240), C((60, 60, 70)), 26, cv2.LINE_AA)
    if T("a3", "police") - 0.1 <= t: cc(f, "JUNAGADH, GUJARAT", 540, 440, t, T("a3", "police") - 0.1, ACC_L, INKC, 44)
    if t >= T("a3", "soybean") - 0.1: cc(f, "SOYBEAN OIL", 320, 860, t, T("a3", "soybean") - 0.1, INKC, MILK, 34)
    if t >= T("a3", "essence") - 0.3: cc(f, "ARTIFICIAL ESSENCE", 760, 860, t, T("a3", "essence") - 0.3, RED_V, MILK, 34)
    src(f, SRC_D, t, t0 + 0.4, 1475)
    return finish(f, n, look="night")


def shot_S5b(t, n):
    f = set_store(t); t0 = st_("S5b")
    for i, x in enumerate((230, 540, 850)): comp(f, scale_el(tin_el(True, None if i != 1 else "smirk", (0, 0), 91 + i, "COW GHEE"), 1.2 if i == 1 else 0.95), x, 1060 + (20 if i != 1 else 0))
    torch_beam(f, 540, 1600, 540, 1040, 330, 0.42)
    f *= 0.78
    t3(f, "PURE?", 560, t, T("a3", "pure") - 0.1, 200)
    src(f, SRC_D, t, t0, 1475)
    return finish(f, n, look="night")


# ---- S6: 'Test one, water.' the glass takes the stand ----
def shot_S6(t, n):
    f = set_court(t); t0 = st_("S6")
    judge(f, 300, 1560, 1.2, t, **nolean(POSE["point"]), expr="sus", brow="sus", look=(1, 0.2), hand_r="point", turn=0.5)
    bench_front(f, 1250)
    glass_float(f, 780, 1090, 1.15, t, GOLD_C, None, 1.0)
    test_pill(f, 1, t, t0); icap(f, "", "[WATER]", t, T("b1", "water") - 0.1, size=150, y=420)
    return finish(f, n, look="warm")


def shot_S6b(t, n):
    f = paper_bg(); t0 = st_("S6b"); tf = T("b1", "floats") - 0.1
    glass_float(f, 540, 1040, 2.0, t, GOLD_C)
    test_pill(f, 1, t, t0); icap(f, "floats, so", "it's [PURE]?", t, tf, size=120, y=430)
    return finish(f, n, look="fresh")


# ---- S7: 'Sure, and so does every oil in your kitchen.' four glasses, four fats, all floating. USELESS ----
def shot_S7(t, n):
    f = set_worktop(t, blur=7); t0 = st_("S7"); te = T("b2", "every") - 0.1; tk_ = T("b2", "kitchen") - 0.15
    worktop_front(f, 1330)
    cols = (PALM_C, PALE_C, ((246, 214, 90), (214, 176, 50), (255, 234, 140), (255, 250, 200)), ((230, 196, 60), (190, 150, 30), (250, 220, 110), (255, 246, 190)))
    for i, (c_, nm) in enumerate(zip(cols, ("PALM", "SOYBEAN", "MUSTARD", "COCONUT"))):
        if t >= te + i * 0.12: glass_float(f, 170 + i * 248, 1120, 0.92, t, c_, nm, 1.0)
    chub_head_only(f, 540, 790, 0.92, t, mouth=talk(t), expr="n", brow="n", look=(0, 0.6))
    verdict(f, "USELESS", t, tk_, 540, 480, RED_V, 130)
    return finish(f, n, look="fresh")


# ---- S8: 'Test two, your palm.' ; S8b 'Your hand's warm, so ghee melts.' ----
def shot_S8(t, n):
    f = set_court(t); t0 = st_("S8")
    judge(f, 300, 1560, 1.2, t, **nolean(POSE["point"]), expr="sus", brow="sus", look=(1, 0.2), hand_r="point", turn=0.5)
    bench_front(f, 1250)
    hand_at(f, 760, 1000, 0.62, 0, 0.2)
    test_pill(f, 2, t, t0); icap(f, "", "your [PALM]", t, T("c1", "palm") - 0.1, size=140, y=420)
    return finish(f, n, look="warm")


def shot_S8b(t, n):
    f = paper_bg(); t0 = st_("S8b"); tw = T("c1", "warm") - 0.1; tm = T("c1", "melts") - 0.1
    if t >= tw: glow(f, 540, 1100, 620, (255, 170, 110), 0.34 * ramp(t, tw, 0.4))
    glow(f, 540, 1000, 420, GHEE_HOT, 0.2)
    hand_at(f, 540, 1210, 1.05)
    blob(f, 540, 1090, 130, 0.1 + 0.8 * ramp(t, tm - 0.1, 0.7), t)
    test_pill(f, 2, t, t0); icap(f, "your hand's", "[WARM]", t, tw, size=140, y=430)
    return finish(f, n, look="golden")


# ---- S9: 'But palm olein, the runny part of palm oil': the bottle, the palm tree ; S9b '...about twenty six degrees': a thermometer ; S9c 'So it slides too' ----
def shot_S9(t, n):
    f = set_worktop(t, blur=7); t0 = st_("S9"); tr = T("c2", "runny") - 0.1
    worktop_front(f, 1330)
    palm_tree(f, 780, 1320, 0.95, 1.0, t, "smirk")
    glow(f, 400, 1040, 300, (255, 186, 90), 0.25)
    comp(f, scale_el(oil_bottle_el(), 1.25), 400, 1060, scale=snap(t, t0, 5))
    chub_head_only(f, 170, 1100, 0.6, t, mouth=talk(t), expr="sus", brow="sus", look=(1, 0))
    icap(f, "palm", "[OLEIN]", t, t0 + 0.05, size=150, y=380)
    if t >= tr: cc(f, "THE RUNNY PART OF PALM OIL", 540, 560, t, tr, ACC_S, MILK, 38)
    return finish(f, n, look="warm")


def shot_S9b(t, n):
    f = paper_bg(sx=700); t0 = st_("S9b"); ty = T("c2", "twenty") - 0.05
    k = 0.12 + 0.34 * ramp(t, ty - 0.2, 0.5)
    comp(f, scale_el(thermo_ink_el(k, False), 1.5), 310, 1040, scale=pin(t, t0, 0.2))
    if t >= ty - 0.2:
        v = 12 + (count_up(t, ty - 0.2, 26, 0.5) / 26) * 14
        comp(f, ed_el("", f"{int(v + 0.5)} °C", big_col=ACC_S, big_size=190), 690, 900)
    comp(f, ed_el("melts at about", "", lead_col=INKC, lead_size=52), 690, 760, op=clamp((t - t0) / 0.2))
    blob(f, 690, 1190, 120, 0.25 + 0.65 * ramp(t, ty, 0.8), t, col=PALM_C)
    src(f, SRC_P, t, t0 + 0.3, 1450)
    peek(f, t, 880, 1290, 0.62, "wow", (-1, -0.3))
    return finish(f, n, look="warm")


def crash_finish(f, t, t0, z, cx, cy, n, look):
    if t >= t0: f = crash_zoom(f, t, t0, z, cx, cy)
    return finish(f, n, look=look)


def shot_S9c(t, n):
    f = paper_bg(); t0 = st_("S9c"); tz = T("c2", "too") - 0.12
    glow(f, 540, 1000, 480, (255, 200, 120), 0.25)
    hand_at(f, 540, 1210, 1.05)
    sl = 200 * ramp(t, t0, 0.8)
    blob(f, 540, 1020 + sl, 125, 0.75, t, slide=sl, col=PALM_C)
    palm_tree(f, 860, 1420, 0.5, 1.0, t, "happy")
    if t >= tz: icap(f, "it slides", "[TOO]", t, tz, size=170, y=420)
    peek(f, t, 180, 1270, 0.72, "wow" if t >= tz else "sus", (1, -0.3))
    return crash_finish(f, t, tz, 1.16, 540, 1000, n, "warm")


# ---- S10: 'one guide says pure ghee slides, another says it stays grainy.' Chubby between two phones, eyes lead the head ; S10b 'Which is it?' ----
def _guide(f, cx, cy, head, big, col):
    x0, y0, x1, y1 = phone_frame(f, cx, cy, 380, 560)
    comp(f, ed_el(head, "", lead_col=INKC, lead_size=30), (x0 + x1) // 2, y0 + 70)
    comp(f, ed_el("", big, big_col=col, big_size=66), (x0 + x1) // 2, (y0 + y1) // 2 + 20)


def shot_S10(t, n):
    f = set_droom(t, dim=0.2); t0 = st_("S10"); ta = T("c3", "another") - 0.1
    _guide(f, 260, 760, "PURE GHEE", "SLIDES", ACC_S)
    if t >= ta: _guide(f, 820, 760, "PURE GHEE", "GRAINY", RED_V)
    e = eye_lead(t, ta - 0.05, -1.0, 1.0)
    chub(f, 540, 1500, 1.02, t=t, la=(30, 16), ra=(30, 16), mouth=talk(t), expr="sus", brow="sus", look=e["look"], turn=e["turn"], lean=e["lean"], blink=e["blink"])
    src(f, SRC_G, t, t0 + 0.3, 1466)
    return finish(f, n, look="warm")


def shot_S10b(t, n):
    f = set_droom(t, dim=0.2); t0 = st_("S10b")
    _guide(f, 260, 760, "PURE GHEE", "SLIDES", ACC_S); _guide(f, 820, 760, "PURE GHEE", "GRAINY", RED_V)
    e = eye_lead(t, t0, 1.0, -1.0); e2 = eye_lead(t, t0 + 0.45, -1.0, 0.0)
    q = e if t < t0 + 0.45 else e2
    chub(f, 540, 1500, 1.08, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="sus", brow="up", look=q["look"], turn=q["turn"], lean=q["lean"], blink=q["blink"])
    verdict(f, "USELESS", t, T("c3", "it") - 0.02, 540, 1380, RED_V, 110)
    icap(f, "", "[WHICH] IS IT?", t, t0 + 0.02, size=118, y=330)
    return finish(f, n, look="warm")


# ---- S11: 'Test three, smell. It's nutty': he sniffs a jar, gold wisps ; S11b 'so it's real?' ----
def shot_S11(t, n):
    f = set_court(t, blur=6); t0 = st_("S11"); tn_ = T("d1", "nutty") - 0.1
    comp(f, scale_el(ghee_jar_el("liquid", 0.8), 1.0), 760, 1120)
    steam_wisps(f, 760, 900, t, 4, 220, 90, GHEE_RIM, 0.7)
    chub_head_only(f, 370, 1000, 1.45, t, mouth="o" if int(t * 3) % 2 else 0, expr="happy" if t > tn_ else "n", brow="up", look=(1, -0.2), turn=0.6)
    test_pill(f, 3, t, t0)
    icap(f, "", "[SMELL]", t, T("d1", "smell") - 0.1, size=150, y=420)
    return finish(f, n, look="golden")


def shot_S11b(t, n):
    f = set_court(t, blur=6); t0 = st_("S11b")
    comp(f, scale_el(ghee_jar_el("liquid", 0.8, "happy"), 1.2), 760, 1120)
    chub_head_only(f, 340, 1000, 1.5, t, mouth=talk(t), expr="happy", brow="up", look=(0.8, -0.1), turn=0.5)
    test_pill(f, 3, t, t0)
    icap(f, "so it's", "[REAL]?", t, t0 + 0.02, size=150, y=430)
    return finish(f, n, look="golden")


# ---- S12: 'Nice. Remember those bottles of essence?' the essence bottle sprays the same smell onto a fake tin. FOOLED ----
def shot_S12(t, n):
    f = set_store(t); t0 = st_("S12"); te = T("d2", "essence") - 0.15; tr = T("d2", "Remember") - 0.05
    glow(f, 540, 1050, 620, (255, 214, 170), 0.35)
    comp(f, scale_el(tin_el(True, "smirk", (-0.6, 0), 93, "COW GHEE"), 1.15), 740, 1120)
    if t >= tr:
        comp(f, scale_el(essence_el("smirk", (0.6, 0)), 1.05), 330, 1130, scale=snap(t, tr, 5))
        fly_drops(f, (380, 1000), (680, 980), t, n=7, rate=1.2, seed=7, s=0.16, arc=-60)
    steam_wisps(f, 740, 900, t, 4, 200, 100, GHEE_RIM, 0.65)
    e = eye_lead(t, tr, 1.0, -0.7)
    chub_head_only(f, 540, 760, 1.05, t, mouth=talk(t), expr="wow" if t >= te else "happy", brow="up", look=e["look"], turn=e["turn"], blink=e["blink"])
    verdict(f, "FOOLED", t, te + 0.2, 540, 500, RED_V, 120)
    return finish(f, n, look="warm")


# ---- S13: 'Test four, colour. Yellow's good, white's bad?' two jars face to face ----
def shot_S13(t, n):
    f = set_court(t, blur=6); t0 = st_("S13"); ty = T("e1", "Yellows") - 0.1; tw = T("e1", "whites") - 0.1
    if t >= ty - 0.15: comp(f, scale_el(ghee_jar_el("grain", 0.82, "happy", (0.7, 0)), 1.25), 300, 1060, scale=pin(t, ty - 0.15, 0.2))
    if t >= tw: comp(f, scale_el(ghee_jar_el("white", 0.82, "sad", (-0.7, 0)), 1.25), 780, 1060, scale=snap(t, tw, 5))
    bench_front(f, 1290, plate=False)
    if t >= ty: cc(f, "GOOD?", 300, 780, t, ty, GOOD, MILK, 48)
    if t >= tw: cc(f, "BAD?", 780, 780, t, tw, RED_V, MILK, 48)
    test_pill(f, 4, t, t0); icap(f, "", "[COLOUR]", t, T("e1", "colour") - 0.1, size=140, y=430)
    return finish(f, n, look="warm")


# ---- S14: 'Buffalo ghee is naturally white' ; S14b 'and yellow can come out of a bottle': pale fat turns gold from a dropper. FOOLED ----
def shot_S14(t, n):
    f = set_dusk(t); f = inkify(f, 0.1); t0 = st_("S14"); tw = T("e2", "white") - 0.1
    comp(f, scale_el(buffalo_el("happy"), 1.35), 330, 1130, scale=snap(t, t0, 5))
    comp(f, scale_el(ghee_jar_el("white", 0.85, "happy", (-0.6, 0)), 1.15), 780, 1160)
    if t >= tw: t3(f, "WHITE", 620, t, tw, 200, face=(250, 244, 226), side=(150, 130, 90))
    src(f, "Source: Deccan Herald (buffalo ghee is usually white)", t, t0 + 0.3, 1466)
    return finish(f, n, look="golden")


def shot_S14b(t, n):
    f = paper_bg(); t0 = st_("S14b"); tb = T("e2", "yellow") - 0.05; k = ramp(t, tb, 1.0)
    comp(f, scale_el(ghee_jar_el("smooth", 0.8), 1.5), 620, 1110, op=1.0)
    comp(f, scale_el(ghee_jar_el("white", 0.8, "smirk", (-0.3, 0)), 1.5), 620, 1110, op=1 - k)
    comp(f, scale_el(essence_el(None, label="DYE"), 0.85), 280, 830)
    if t > tb:
        fly_drops(f, (340, 900), (620, 900), t, n=5, rate=1.3, seed=4, s=0.14, arc=-50)
    chub_head_only(f, 190, 1280, 0.62, t, mouth=talk(t), expr="sus", brow="sus", look=(1, -0.2), turn=0.5)
    verdict(f, "FOOLED", t, T("e2", "bottle") - 0.1, 620, 620, RED_V, 120)
    src(f, SRC_F + ": a test just for dye in ghee", t, t0 + 0.3, 1466)


    return finish(f, n, look="fresh")


# ---- S15: 'Four tests, no winners.' the board so far ; S15b 'Bring in the chemistry.' ----
def shot_S15(t, n):
    f = paper_bg(sy=900, R=700); t0 = st_("S15")
    verdict_board(f, t, [t0 + 0.02 + i * 0.1 for i in range(4)], y0=560, gap=140)
    icap(f, "four tests", "NO [WINNERS]", t, T("f1", "no") - 0.1, size=110, y=350)
    chub_head_only(f, 540, 1300, 0.74, t, mouth=talk(t), expr="sad", brow="sad", look=(0, -0.7))
    return finish(f, n, look="fresh")


def shot_S15b(t, n):
    f = set_court(t); t0 = st_("S15b"); tc = T("f1", "chemistry") - 0.1
    if t >= tc: t3(f, "CHEMISTRY", 560, t, tc, 150)
    g = judge_gavel(f, 500, 1560, 1.3, t, [tc], expr="smirk", brow="up")
    bench_front(f, 1250); gavel_top(f, g)
    comp(f, scale_el(tube_el(0.0, 0.5), 0.5), 200, 1150, scale=pin(t, t0, 0.2)); comp(f, scale_el(bottle_el(), 0.42), 340, 1150, scale=pin(t, t0 + 0.08, 0.2))
    return finish(f, n, look="warm")


# ---- S16: 'Iodine's the guard from my paneer video, with one photo.' ; S16b 'He only knows starch.' the potato is stopped, the oil strolls in ----
def shot_S16(t, n):
    f = paper_bg(sy=1000); t0 = st_("S16")
    guard_post(f, t, "smirk", look=(0, 0), gx=600, gy=1180)
    cc(f, "THE GUARD FROM THE PANEER VIDEO", 540, 440, t, t0 + 0.1, INKC, MILK, 34)
    return finish(f, n, look="fresh")


def shot_S16b(t, n):
    f = paper_bg(sy=1000); t0 = st_("S16b"); ts = T("f2", "starch") - 0.15
    guard_post(f, t, "angry" if t >= ts else "n", look=(-0.8, 0), gx=600, gy=1180, door_open=0.5)
    comp(f, scale_el(potato_el("sad" if t >= ts else "sus", (0.5, 0)), 0.95), 300 - (40 * snap(t, ts, 4) if t >= ts else 0), 1340)
    p = clamp((t - t0) / max(0.1, en_("S16b") - t0))
    comp(f, scale_el(oil_drop_el("happy"), 0.9), 180 + 700 * p, 1370 - 26 * abs(math.sin(t * 8)), op=1.0 if p < 0.92 else 0.0)
    verdict(f, "ONLY STARCH", t, ts, 540, 480, ACC_S, 96)
    peek(f, t, 880, 680, 0.55, "smirk", (-0.7, 0.6))
    return finish(f, n, look="fresh")


# ---- S17: 'The acid test's on the official list.' ; S17b 'It turns crimson if there's vanaspati.' ----
def shot_S17(t, n):
    f = paper_bg(sy=1040); t0 = st_("S17"); to = T("f3", "official") - 0.1
    comp(f, scale_el(tube_el(0.0, 0.6), 1.4), 300, 1040, scale=snap(t, t0, 5))
    if t >= to: comp(f, scale_el(article_el(), 1.2), 720, 1000, scale=pin(t, to, 0.25))
    if t >= to: cc(f, "OFFICIAL LIST", 720, 720, t, to + 0.05, ACC_S, MILK, 40)
    icap(f, "the", "[ACID] test", t, T("f3", "acid") - 0.1, size=130, y=420)
    src(f, SRC_F, t, t0 + 0.3, 1466)
    peek(f, t, 520, 1320, 0.5, "sus", (-1, -0.4))
    return finish(f, n, look="fresh")


def shot_S17b(t, n):
    f = paper_bg(sy=1040); t0 = st_("S17b"); tc = T("f3", "crimson") - 0.15
    comp(f, scale_el(tube_el(ramp(t, tc, 0.5), 0.6), 1.6), 300, 1040)
    comp(f, scale_el(vanaspati_el("wow" if t >= tc else "n", (-0.7, 0)), 1.1), 730, 1130)
    if t >= tc: glow(f, 300, 1250, 240, (220, 40, 80), 0.25 * ramp(t, tc, 0.5))
    if t >= T("f3", "vanuspatee") - 0.1: cc(f, "VANASPATI", 730, 910, t, T("f3", "vanuspatee") - 0.1, INKC, MILK, 38)
    icap(f, "turns", "[CRIMSON]", t, tc, acc=(182, 22, 62), size=130, y=420)
    peek(f, t, 540, 1330, 0.55, "wow" if t >= tc else "happy", (-1, -0.2))
    return finish(f, n, look="fresh")


# ---- S18: 'Clever, but it's really spotting sesame oil ... as a tag' ; S18b 'No tag, and it can slip through.' ----
def shot_S18(t, n):
    f = paper_bg(sy=1040); t0 = st_("S18"); ts = T("f4", "sesame") - 0.1; tg = T("f4", "tag") - 0.12
    comp(f, scale_el(vanaspati_el("n", tag=t >= tg), 1.55), 540, 1090)
    if ts <= t: comp(f, scale_el(sesame_el(), 1.4), 300, 780, scale=snap(t, ts, 5))
    if ts <= t: cc(f, "SESAME OIL", 300, 660, t, ts + 0.1, ACC_S, MILK, 40)
    if t >= tg: label_at(f, "THE TAG", 880, 800, t, tg, 800, 1120, bg=RED_V, fg=MILK, size=38)
    icap(f, "it's really spotting", "[SESAME]", t, ts, size=130, y=440)
    src(f, SRC_S, t, t0 + 0.3, 1466)
    peek(f, t, 170, 1270, 0.6, "smirk", (1, -0.3))
    return finish(f, n, look="fresh")


def shot_S18b(t, n):
    f = paper_bg(sy=1040); t0 = st_("S18b"); ts = T("f4", "through") - 0.15; p = ramp(t, t0, en_("S18b") - t0)
    comp(f, scale_el(tube_el(0.0, 0.6), 1.4), 760, 1040)
    cc(f, "NO COLOUR", 760, 660, t, t0 + 0.3, INKC, MILK, 38)
    comp(f, scale_el(vanaspati_el("smirk", (-0.3, 0)), 0.95), 170 + 420 * p, 1320 - 18 * abs(math.sin(t * 7)))
    icap(f, "no tag", "[NO ALARM]", t, t0 + 0.03, size=110, y=420)
    verdict(f, "ONLY SESAME", t, ts, 460, 760, ACC_S, 84)
    peek(f, t, 880, 1370, 0.5, "sus", (-1, 0))
    return finish(f, n, look="fresh")


# ---- S19: 'And that's strong acid, so please, not in your kitchen.' lights down, red mood, STOP ----
def shot_S19(t, n):
    f = set_worktop(t, blur=6); t0 = st_("S19"); tk_ = T("f5", "kitchen") - 0.15; f *= 0.72
    mood(f, (230, 50, 50), 0.32)
    worktop_front(f, 1330)
    comp(f, scale_el(tube_el(0.75, 0.6), 1.05), 760, 1040)
    chub(f, 280, 1500, 1.05, t=t, **nolean(POSE["stop"]), mouth=talk(t), expr="sus", brow="sad", look=(0, 0))
    verdict(f, "NOT AT HOME", t, tk_, 540, 620, RED_V, 110)
    icap(f, "that's", "[STRONG] ACID", t, T("f5", "strong") - 0.1, acc=(255, 120, 100), size=110, y=350, dark=True)
    return finish(f, n, look="night")


# ---- S20: 'Which leaves the fridge.' the dark kitchen, the door opens, cold light ; S20b 'And this is the one.' gold jar in the cold light ----
def shot_S20(t, n):
    f = set_fridge_night(t); t0 = st_("S20"); tf = T("g1", "fridge") - 0.2; e = eye_lead(t, tf, -0.4, 1.0)
    chub(f, 300, 1500, 1.05, t=t, la=(24, 14), ra=(70, 40), mouth=talk(t), expr="sus", brow="up", look=e["look"], turn=e["turn"], lean=e["lean"], blink=e["blink"], hand_r="point")
    if t >= tf: t3(f, "THE FRIDGE", 460, t, tf, 150, face=(200, 232, 245), side=(50, 100, 150))
    if t >= tf: comp(f, scale_el(ghee_jar_el("liquid", 0.5), 0.72), 860, 1000, scale=snap(t, tf + 0.1, 5))
    return finish(f, n, look="cool")


def shot_S20b(t, n):
    f = set_fridge_night(t); t0 = st_("S20b"); to = T("g1", "one") - 0.15
    glow(f, 540, 1000, 420, GHEE_RIM, 0.32)
    comp(f, scale_el(ghee_jar_el("grain", 0.82, "happy"), 1.7), 540, 1040, scale=snap(t, t0, 5))
    if t >= to:
        cv2.circle(f, (540, 1040), int(390 + 10 * math.sin((t - to) * 8)), C(ACC_L), 14, cv2.LINE_AA)
        t3(f, "THIS ONE", 470, t, to, 150)
    return crash_finish(f, t, to, 1.12, 540, 900, n, "golden")


# ---- S21: 'A teaspoon, a couple of hours.' a teaspoon, a clock racing ; S21b 'Pure ghee sets evenly, into little grains all through.' + the magnifier ----
def shot_S21(t, n):
    f = set_worktop(t, blur=5); t0 = st_("S21"); tc = T("g2", "couple") - 0.1; top_ = 1330
    worktop_front(f, top_)
    comp(f, scale_el(fridge_ink_el(True, False), 0.72), 180, 1000)
    comp(f, scale_el(ghee_jar_el("liquid", 0.42), 0.46), 145, 1000)
    if t >= tc - 0.1:
        comp(f, scale_el(clock_ink_el(), 1.25), 740, 660, scale=pin(t, tc - 0.1, 0.25)); clock_hands(f, 740, 660, 2.0 * ramp(t, tc, en_("S21") - tc), s=1.25)
    comp(f, scale_el(spoon_el(), 1.1), 660, 1180 + 10 * math.sin(t * 2.5))
    blob(f, 736, 1120, 42, 0.3, t)
    icap(f, "a", "[TEASPOON]", t, T("g2", "teaspoon") - 0.1, size=110, y=340)
    peek(f, t, 430, 1200, 0.62, "happy", (1, -0.1))
    return finish(f, n, look="fresh")


def shot_S21b(t, n):
    f = paper_bg(sy=1040); t0 = st_("S21b"); te = T("g2", "evenly") - 0.1
    glow(f, 400, 1040, 460, GHEE_RIM, 0.28)
    comp(f, scale_el(ghee_jar_el("grain", 0.86, "happy"), 1.75), 400, 1060)
    def dr(g, cx=800, cy=880, r=200):
        rng = np.random.default_rng(3); g[int(cy - r):int(cy + r), int(cx - r):int(cx + r)] = C(GHEE)
        for i in range(70):
            a, b = rng.uniform(-r, r), rng.uniform(-r, r); cv2.circle(g, (int(cx + a), int(cy + b)), int(rng.uniform(7, 13)), C((255, 226, 130) if i % 2 else (196, 122, 22)), -1, cv2.LINE_AA)
    if t >= te: inset(f, 800, 880, 190, dr, k=snap(t, te, 5), ring=WHITE)
    if t >= T("g2", "little") - 0.1: cc(f, "SAME GRAINS ALL THROUGH", 760, 1160, t, T("g2", "little") - 0.1, ACC_S, MILK, 32)
    icap(f, "sets", "[EVENLY]", t, te, size=140, y=430)
    src(f, SRC_A, t, t0 + 0.3, 1466)
    return finish(f, n, look="golden")


# ---- S22: 'Mix in palm oil, and the solid and the liquid split apart.' ----
def shot_S22(t, n):
    f = paper_bg(sy=1040); t0 = st_("S22"); ts = T("g3", "split") - 0.15; tm = T("g3", "palm") - 0.1
    comp(f, scale_el(ghee_jar_el("grain", 0.86), 1.05), 220, 1120, op=0.75)
    k = ramp(t, ts - 0.1, 0.45)
    comp(f, scale_el(ghee_jar_el("smooth", 0.86), 1.75), 660, 1060, op=1 - k)
    comp(f, scale_el(ghee_jar_el("split", 0.86, "sad" if k > 0.5 else None), 1.75), 660, 1060, op=k)
    if t >= tm: palm_tree(f, 960, 800, 0.36, snap(t, tm, 5), t, None)
    if t >= ts:
        label_at(f, "LIQUID", 920, 900, t, ts + 0.1, 800, 950, bg=INKC, fg=MILK, size=34); label_at(f, "SOLID", 920, 1240, t, ts + 0.2, 800, 1190, bg=INKC, fg=MILK, size=34)
        verdict(f, "LAYERS", t, ts + 0.05, 560, 620, RED_V, 110)
    icap(f, "mix in", "[PALM OIL]", t, t0 + 0.03, size=110, y=380, out=ts)
    return finish(f, n, look="fresh")


# ---- S23: 'It's a clue, not a verdict.' the gavel stops in mid air ; S23b 'Ghee that's cooled fast can come out smooth.' ----
def shot_S23(t, n):
    f = set_court(t); t0 = st_("S23"); tv = T("g4", "verdict") - 0.1; tc = T("g4", "clue") - 0.1
    g = judge_gavel(f, 500, 1560, 1.3, t, [], expr="sus" if t >= tv else "smirk", brow="up", look=(0.7, -0.5))
    bench_front(f, 1250); gavel_top(f, g)
    verdict(f, "A CLUE", t, tc, 540, 500, GOOD, 130, 4)
    if t >= tv: cc(f, "NOT A VERDICT", 540, 660, t, tv, RED_V, MILK, 62)
    return finish(f, n, look="warm")


def shot_S23b(t, n):
    f = paper_bg(sy=1040); t0 = st_("S23b"); ts = T("g4", "smooth") - 0.2
    comp(f, scale_el(ghee_jar_el("smooth", 0.86, "happy" if t >= ts else "n"), 1.75), 540, 1000)
    for i in range(16):
        p = ((t - t0) * 0.9 + i * 0.11) % 1; y = 720 + i * 34; x = 40 + 1000 * p
        cv2.line(f, (int(x), y), (int(x + 80), y), C((150, 200, 230)), 4, cv2.LINE_AA)
    cc(f, "COOLED FAST", 540, 620, t, t0 + 0.1, (60, 120, 170), MILK, 44)
    if t >= ts: verdict(f, "STILL REAL", t, ts, 540, 1290, GOOD, 90, 3)
    src(f, SRC_Q, t, t0 + 0.2, 1456)
    return finish(f, n, look="fresh")


# ---- S24: 'So layers, be suspicious.' ; S24b 'No layers? Still not proof.' ----
def shot_S24(t, n):
    f = set_worktop(t, blur=6); t0 = st_("S24")
    worktop_front(f, 1330)
    comp(f, scale_el(ghee_jar_el("split", 0.86, "sad"), 1.3), 690, 1090)
    if t >= t0 + 0.2: label_at(f, "A CLEAR LINE", 760, 800, t, t0 + 0.2, 690, 1040, bg=RED_V, fg=MILK, size=34)
    chub(f, 230, 1500, 1.02, t=t, **POSE["think"], mouth=talk(t), expr="sus", brow="sus", look=(1, 0.2), turn=0.5)
    icap(f, "layers?", "[SUSPICIOUS]", t, T("g5", "suspicious") - 0.25, size=112, y=430)
    return finish(f, n, look="cool")


def shot_S24b(t, n):
    f = set_worktop(t, blur=6); t0 = st_("S24b"); tp = T("g5", "proof") - 0.15
    worktop_front(f, 1330)
    comp(f, scale_el(ghee_jar_el("grain", 0.86, "smirk"), 1.3), 690, 1090)
    chub(f, 230, 1500, 1.02, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="n", brow="up", look=(1, 0), turn=0.5)
    icap(f, "no layers?", "", t, t0 + 0.03, size=100, y=430)
    verdict(f, "NOT PROOF", t, tp, 620, 700, RED_V, 110)
    return finish(f, n, look="fresh")


# ---- S25: 'Why so hard? Some sellers blend it': streams pour into one jar ; S25b 'even simple lab numbers miss it': a clipboard of ticks on a fake ----
def shot_S25(t, n):
    f = ink_set("steel", (255, 255, 255), 540, 1000, 560); t0 = st_("S25"); ts = T("h1", "blend") - 0.2
    comp(f, scale_el(ghee_jar_el("smooth", 0.3 + 0.5 * ramp(t, t0, en_("S25") - t0)), 1.45), 540, 1160)
    cv2.line(f, (360, 760), (500, 1000), C(GHEE), 16, cv2.LINE_AA); cv2.line(f, (720, 760), (580, 1000), C(FAKE), 16, cv2.LINE_AA)
    comp(f, scale_el(milkfat_el(), 2.2), 300, 690); comp(f, scale_el(oil_bottle_el(), 0.82), 770, 690); cc(f, "MILK FAT", 300, 820, t, t0 + 0.1, ACC_S, MILK, 34); cc(f, "CHEAP OIL", 770, 925, t, t0 + 0.1, INKC, MILK, 34)
    icap(f, "why so", "[HARD]?", t, t0 + 0.03, size=130, y=390, out=ts)
    if t >= ts: icap(f, "some sellers", "[BLEND]", t, ts, size=130, y=390)
    return finish(f, n, look="cool")


def shot_S25b(t, n):
    f = ink_set("steel", (255, 255, 255), 540, 1000, 560); t0 = st_("S25b"); tl = T("h1", "lab") - 0.1; tm = T("h1", "miss") - 0.15
    label_card(f, 540, 980, t, [tl + i * 0.1 for i in range(3)], names=("RM VALUE", "POLENSKE", "BR READING"), s=0.92)
    verdict(f, "IT PASSES", t, tm, 560, 1320, GOOD, 96)
    icap(f, "simple", "[LAB] numbers", t, tl, size=110, y=440)
    src(f, SRC_H, t, t0 + 0.3, 1466)
    return finish(f, n, look="cool")


# ---- S26: 'milk fat has a tiny fat palm oil doesn't, called butyric acid' long chains + the tiny guy ; S26b 'About two and a half per cent in ghee, zero in palm oil.' ----
def shot_S26(t, n):
    f = paper_bg(sy=1040); t0 = st_("S26"); tt = T("h2", "tiny") - 0.1; tb = T("h2", "butyric") - 0.1
    for i, y in enumerate((760, 860, 960)):
        comp(f, chain_el(16, (232, 214, 150), 26, 171 + i), 540 + 30 * math.sin(t + i), y)
    if t >= tt: comp(f, chain_el(4, ACC, 34, 181, "happy"), 540, 1170, scale=snap(t, tt, 5))
    if t >= tb: label_at(f, "BUTYRIC ACID", 830, 1330, t, tb, 620, 1200, bg=ACC_S, fg=MILK, size=38)
    icap(f, "milk fat has a", "[TINY] fat", t, tt, size=130, y=430)
    peek(f, t, 190, 1270, 0.6, "wow", (1, -0.2))
    return finish(f, n, look="golden")


def shot_S26b(t, n):
    f = paper_bg(sy=1040); t0 = st_("S26b"); tz = T("h2", "zero") - 0.1
    comp(f, scale_el(ghee_jar_el("liquid", 0.86), 1.35), 290, 1040)
    comp(f, ed_el("", "2.4%", big_col=ACC_S, big_size=120), 290, 690)
    for i in range(6):
        p = (t * 0.28 + i / 6) % 1
        comp(f, scale_el(chain_el(4, ACC, 20, 190 + i), 0.82), 220 + (i % 3) * 66, 1190 - 220 * p, op=clamp(4 * p) * clamp(4 * (1 - p)))
    if t >= tz:
        comp(f, scale_el(oil_bottle_el(), 1.2), 790, 1060, scale=snap(t, tz, 5))
        comp(f, ed_el("", "0", big_col=RED_V, big_size=170), 790, 690, scale=snap(t, tz, 4))
    src(f, SRC_H + " (2.43 % in pure ghee, 0.00 in palm oil)", t, t0 + 0.3, 1466)
    peek(f, t, 540, 1340, 0.5, "wow" if t >= tz else "happy", (0.6, -0.5))
    return finish(f, n, look="golden")


# ---- S27: 'A lab can count it, and catch palm oil down to about five per cent.' the readout draws itself ; S27b 'Your hand can't count.' ----
def shot_S27(t, n):
    f = ink_set("steel", (255, 255, 255), 540, 1000, 560); t0 = st_("S27"); k = ramp(t, t0 + 0.1, 1.5); tf = T("h3", "five") - 0.1
    sx, sy = peaks(f, 150, 620, 780, 470, k, 1.0)
    if k > 0.22: label_at(f, "BUTYRIC", 300, 560, t, t0 + 0.5, sx, sy, bg=ACC_S, fg=MILK, size=34)
    chub(f, 250, 1500, 0.72, t=t, **nolean(POSE["point"]), shirt=(250, 250, 246), mouth=talk(t), expr="happy", brow="up", look=(1, -0.6), hand_r="point", turn=0.5)
    if t >= tf: comp(f, ed_el("catches palm oil down to", "ABOUT 5%", big_col=ACC_S, lead_col=INKC, big_size=100, lead_size=40), 660, 1270, scale=snap(t, tf, 4))
    icap(f, "a lab can", "[COUNT] it", t, t0 + 0.03, size=120, y=400)
    src(f, SRC_H, t, t0 + 0.3, 1466)
    return finish(f, n, look="cool")


def shot_S27b(t, n):
    f = set_worktop(t, blur=8); t0 = st_("S27b"); tc = T("h3", "cant") - 0.1
    hand_at(f, 680, 1230, 0.9, 6)
    chub_head_only(f, 270, 900, 1.08, t, mouth=talk(t), expr="sus", brow="up", look=(1, 0.4), turn=0.5)
    for j, x in enumerate((560, 680, 800)):
        if t >= tc + j * 0.12: t3(f, "?", 690 - 30 * (j % 2), t, tc + j * 0.12, 120, x=x)
    icap(f, "your hand", "[CAN'T] COUNT", t, tc, acc=RED_V, size=110, y=400)
    return crash_finish(f, t, tc, 1.1, 540, 900, n, "warm")


# ---- S28: 'So before Diwali, check the tin, not your hand.' Diwali room: the hand goes down, the tin comes up ----
def shot_S28(t, n):
    f = set_droom(t); t0 = st_("S28"); tt = T("k1", "tin") - 0.12; thd = T("k1", "hand") - 0.1
    k = snap(t, tt, 5) if t >= tt else 0
    chub(f, 300, 1500, 1.08, t=t, **nolean(POSE["hold_up"]), mouth=talk(t), expr="happy", brow="up", look=(0.9, -0.3), turn=0.5, lean=3)
    table_front(f, 1400)
    if k > 0: comp(f, scale_el(tin_el(False, "happy"), 1.3), 720, 1000 + 40 * (1 - k), scale=max(0.01, k))
    t3(f, "THE TIN", 500, t, tt, 190)
    if t >= thd: cc(f, "NOT YOUR HAND", 720, 1310, t, thd, RED_V, MILK, 40)
    return finish(f, n, look="golden")


# ---- S29: 'licence number, the maker, a batch number and an expiry date' ; S29b 'Those tins had no batch number and no expiry.' ----
def shot_S29(t, n):
    f = set_droom(t, dim=0.25); t0 = st_("S29")
    ts = [T("k2", "licence") - 0.1, T("k2", "maker") - 0.1, T("k2", "batch") - 0.1, T("k2", "expiry") - 0.1]
    label_card(f, 540, 930, t, ts)
    icap(f, "", "[CHECK] THE LABEL", t, t0 + 0.03, size=96, y=470, dark=True)
    src(f, "Source: Karmactive, 26 Oct 2026 · FSSAI advice via FoodTechNetwork", t, t0 + 0.3, 1400)
    return finish(f, n, look="warm")


def shot_S29b(t, n):
    f = set_store(t); t0 = st_("S29b"); glow(f, 540, 940, 760, (255, 220, 170), 0.3)
    ts = [t0 - 1, t0 - 1, T("k2", "batch", 1) - 0.1, T("k2", "expiry", 1) - 0.1]
    label_card(f, 540, 930, t, ts, fake=True)
    icap(f, "those tins", "[NO] BATCH, [NO] EXPIRY", t, t0 + 0.03, acc=(255, 120, 100), size=70, y=470, dark=True)
    src(f, SRC_D, t, t0 + 0.2, 1400)
    return finish(f, n, look="night")


# ---- S30: 'And a seal isn't proof.' ; S30b 'That raid found sealing machines.' the press comes down on a tin, twice ----
def shot_S30(t, n):
    f = paper_bg(sy=1040); t0 = st_("S30"); ts = T("k3", "proof") - 0.15
    comp(f, scale_el(tin_el(False), 1.5), 540, 1070)
    cv2.ellipse(f, (540, 845), (170, 34), 0, 0, 360, C((230, 220, 180)), -1, cv2.LINE_AA); cv2.ellipse(f, (540, 845), (170, 34), 0, 0, 360, C(INKC), 5, cv2.LINE_AA)
    comp(f, ed_el("SEALED", "", lead_col=INKC, lead_size=38), 540, 845)
    icap(f, "a", "[SEAL]", t, t0 + 0.03, size=130, y=450)
    verdict(f, "NOT PROOF", t, ts, 540, 1090, RED_V, 110)
    return finish(f, n, look="fresh")


def shot_S30b(t, n):
    f = set_store(t); t0 = st_("S30b"); glow(f, 540, 1040, 640, (255, 214, 170), 0.3)
    phase = ((t - t0) * 1.6) % 1; dn = (1 - abs(2 * phase - 1)) ** 2
    comp(f, scale_el(tin_el(True, None, seed=94, tag_text="COW GHEE"), 0.72), 380, 1180)
    comp(f, scale_el(sealer_el(dn), 1.2), 500, 1030)
    icap(f, "that raid found", "[SEALING] MACHINES", t, t0 + 0.03, acc=ACC_L, size=88, y=450, dark=True)
    src(f, SRC_D, t, t0 + 0.2, 1466)
    return finish(f, n, look="night")


# ---- S31: 'Buy from a shop you trust' ; S31b 'if the price looks too good, ask why.' ----
def shot_S31(t, n):
    f = set_shop(t); t0 = st_("S31")
    chub(f, 760, 1500, 1.0, t=t, **POSE["idle"], shirt=(230, 150, 60), mouth=0, expr="happy", brow="up", look=(-1, 0), turn=-0.5); dress(f, 760, 1500, 1.0, "boss")
    chub(f, 260, 1500, 1.05, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="happy", brow="up", look=(1, 0), hand_r="point", turn=0.5)
    shop_front(f, 1300)
    comp(f, scale_el(tin_el(False, "happy"), 0.62), 540, 1190)
    icap(f, "a shop you", "[TRUST]", t, T("k4", "trust") - 0.15, size=130, y=420)
    return finish(f, n, look="warm")


def shot_S31b(t, n):
    f = set_shop(t, dim=0.1); t0 = st_("S31b"); tp = T("k4", "price") - 0.1; tw = T("k4", "why") - 0.15; e = eye_lead(t, tp, 0.0, 1.0)
    chub(f, 260, 1500, 1.05, t=t, **nolean(POSE["think"]), mouth=talk(t), expr="sus", brow="sus", look=e["look"], turn=e["turn"], blink=e["blink"])
    shop_front(f, 1300)
    comp(f, scale_el(tin_el(True, "smirk", (-0.4, 0), 95), 1.05), 720, 1100)
    if t >= tp: rot_comp(f, burst_el("TOO GOOD?", (255, 220, 90), RED_V, 50), 780, 760, -8 + 3 * math.sin(t * 3), snap(t, tp, 5))
    if t >= tw: icap(f, "", "ASK [WHY]", t, tw, size=130, y=450)
    return finish(f, n, look="warm")


# ---- S32: 'So remember. Fridge for a clue, lab for the truth, label before you pay.' the whole board: a screenshot card ----
def shot_S32(t, n):
    f = paper_bg(sy=860, R=760); t0 = st_("S32")
    verdict_board(f, t, [t0 + 0.02 + i * 0.05 for i in range(7)], y0=420, gap=106, cur=6, x_v=590)
    for (x, top_, bot_, w_) in ((230, "FRIDGE", "A CLUE", "clue"), (540, "LAB", "THE TRUTH", "truth"), (850, "LABEL", "BEFORE YOU PAY", "pay")):
        tw = T("l1", w_) - 0.3
        if t >= tw:
            comp(f, ed_el(top_, "", lead_col=INKC, lead_size=36), x, 1200, scale=snap(t, tw, 4))
            comp(f, chip(bot_, ACC_S, MILK, 28), x, 1262, scale=snap(t, tw, 4))
    chub_head_only(f, 540, 1400, 0.42, t, mouth=talk(t), expr="happy", brow="up", look=(0, -0.7))
    comp(f, chip("SAVE THIS", INKC, ACC_L, 34), 540, 300, op=clamp((t - t0) / 0.2))
    return finish(f, n, look="fresh")


# ---- S33: 'Send this to whoever's rubbing ghee on their hand right now.' ; then logo ----
def shot_S33(t, n):
    t0 = st_("S33"); f = set_droom(t); vend = LINES["l2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("l2", "Send") + 0.25
        comp(f, scale_el(phone2_el("stop rubbing ghee on your hand", "the palm test can't catch palm oil", pr), 0.82), 760, 960, scale=pin(t, t0))
        if pr and t < T("l2", "Send") + 0.7:
            rr = (t - T("l2", "Send") - 0.25) / 0.45; cv2.circle(f, (760, 1230), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 300, 1500, 1.05, t=t, la=(20, 12), ra=(70, 40), mouth=talk(t), expr="smirk", brow="up", hand_r="point", look=(1, -0.1), turn=0.5)
        ui_word(f, "send this to whoever's rubbing", "GHEE ON THEIR [HAND]", 440, t, T("l2", "Send") - 0.05, col=INKC, acc=ACC_S, size=78)
    else:
        k = pin(t, vend + 0.2, 0.4); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INKC, lead_size=42), 540, 1030, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1500, 0.7, t=t, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up")
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TI, 0.45, 18), (T("i2", "Pure") - 0.1, 0.35, 12), (T("i3", "trial") - 0.08, 0.45, 18), (T("a1", "gone") - 0.2, 0.25, 8), (T("a2", "cheaper") - 0.1, 0.25, 10), (T("b2", "kitchen") - 0.15, 0.35, 14), (T("c2", "too") - 0.12, 0.35, 14), (T("c3", "it") - 0.02, 0.3, 12),
           (T("d2", "essence") + 0.05, 0.35, 14), (T("e2", "bottle") - 0.1, 0.3, 12), (T("f1", "chemistry") - 0.08, 0.45, 18), (T("f2", "starch") - 0.15, 0.3, 12), (T("f3", "crimson") - 0.15, 0.3, 10), (T("f4", "through") - 0.15, 0.3, 12), (T("f5", "kitchen") - 0.15, 0.35, 14),
           (T("g1", "one") - 0.15, 0.35, 12), (T("g3", "split") - 0.1, 0.35, 12), (T("g4", "clue") - 0.1, 0.3, 10), (T("g5", "proof") - 0.15, 0.35, 12), (T("h1", "miss") - 0.15, 0.3, 10), (T("h2", "zero") - 0.1, 0.3, 12), (T("h3", "cant") - 0.1, 0.3, 12), (T("k1", "tin") - 0.12, 0.3, 10), (T("k3", "proof") - 0.15, 0.35, 14), (T("k4", "why") - 0.15, 0.25, 8), (T("l2", "Send") + 0.25, 0.2, 8)]


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
