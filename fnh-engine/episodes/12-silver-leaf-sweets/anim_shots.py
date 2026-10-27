# ================= shots: FreshNestHub 12 — "Is the silver on Indian sweets real?" (vark / silver leaf) =================
# COLOUR SCRIPT (ep 12): festive warm sets (saffron / festive pink / yellow / orange) = the sweets and the celebration;
# cool STEEL sets = the metal truth (what it is, how thin, how it's made); dark purple / red = the hidden past and the fakes;
# cream / emerald = what you can do with it today. The set flips on the word where the story changes key.
# CRAFT (ep 12): pre-training cast card before the process (cast_card), iris match cuts from a round object into the next
# shot (iris_mix), hammer swung on an ARC with anticipation (hammer_swing) instead of a straight up/down.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "Yep.") - 0.15, "punch"), ("S1b", T("i2", "And") - 0.1, "zoom"),
    ("S2", T("i3", "But") - 0.15, "whip"),
    ("S3", T("a1", "It's") - 0.2, "iris"), ("S3b", T("a1", "That's") - 0.1, "zoom"),
    ("S4", T("a2", "And") - 0.2, "whip"), ("S4b", T("a2", "At") - 0.1, "punch"),
    ("S5", T("a3", "So") - 0.2, "whip"),
    ("S6", T("a4", "First,") - 0.2, "focus"), ("S6b", T("a4", "between") - 0.25, "zoom"),
    ("S7", T("a5", "Then") - 0.2, "whip"), ("S7b", T("a5", "Again") - 0.1, "punch"),
    ("S8", T("a6", "With") - 0.2, "zoom"),
    ("S9", T("b1", "How") - 0.2, "flash"), ("S9b", T("b1", "Take") - 0.1, "whip"),
    ("S10", T("b2", "The") - 0.2, "whip"), ("S11", T("b3", "That") - 0.2, "iris"), ("S12", T("b4", "So") - 0.2, "whip"),
    ("S13", T("c1", "Now,") - 0.2, "focus"), ("S14", T("c2", "For") - 0.2, "whip"), ("S14b", T("c2", "animal") - 0.15, "punch"),
    ("S15", T("c3", "So") - 0.2, "whip"), ("S16", T("c4", "In") - 0.2, "zoom"), ("S17", T("c5", "Now") - 0.2, "whip"),
    ("S18", T("d1", "Now,") - 0.2, "focus"), ("S19", T("d2", "Scientists") - 0.2, "whip"), ("S20", T("d3", "About") - 0.2, "zoom"),
    ("S20b", T("d3", "It") - 0.1, "punch"), ("S21", T("d4", "And") - 0.2, "whip"), ("S22", T("d5", "Many") - 0.2, "iris"),
    ("S23", T("e1", "And") - 0.2, "flash"), ("S23b", T("e1", "Europe") - 0.15, "whip"), ("S24", T("e2", "But") - 0.2, "zoom"),
    ("S25", T("e3", "It's") - 0.2, "whip"),
    ("S26", T("f1", "So") - 0.2, "focus"), ("S26b", T("f1", "It's") - 0.1, "punch"), ("S27", T("f2", "Remember:") - 0.2, "whip"),
    ("S28", T("f3", "Buy") - 0.2, "whip"), ("S29", T("f4", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
# iris match cuts: where the circle opens, in the PREVIOUS shot's picture (a round/central object)
IRIS = {"S3": (540, 1080), "S11": (760, 960), "S22": (540, 1000)}


def lt(t, sid): return t - SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def wui(f, lead, big, t, t0, acc=YEL_, size=170, y=470, out=None, tail=""):   # white caption on dark/colour sets
    ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.5, lead_col=WHITE, out=out, tail=tail)


def rays(f, x, y, r, col, amt, t, nr=14):
    if amt <= 0.01: return
    ov = np.zeros((H, W), np.float32); a0 = t * 0.25
    for i in range(nr):
        a = a0 + i * 2 * math.pi / nr; da = math.pi / nr * 0.5
        pts = np.array([[x, y], [x + r * math.cos(a - da), y + r * math.sin(a - da)], [x + r * math.cos(a + da), y + r * math.sin(a + da)]], np.int32)
        cv2.fillPoly(ov, [pts], 1.0, cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 6) * np.clip(1 - np.hypot(_xx - x, _yy - y) / r, 0, 1)
    f += ov[..., None] * np.array(C(col), np.float32) * amt


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / d))


def munch(t, rate=0.42):
    ph = (t / rate) % 1.0
    return (2 if ph < 0.5 else 0), int(t / rate)


def st_(sid): return SHOT[sid]["start"]


def shiver(t, amt=1.0): return amt * 7 * math.sin(t * 61), amt * 3 * math.sin(t * 47)


def twinkle(f, x, y, w, h, t, n=6, seed=1):
    """little 4-point glints that come and go on a silver surface."""
    rng = np.random.default_rng(seed)
    for i in range(n):
        px, py = x + rng.uniform(-w / 2, w / 2), y + rng.uniform(-h / 2, h / 2); ph = (t * 1.3 + rng.uniform(0, 1)) % 1.0
        s_ = 18 * math.sin(math.pi * ph) ** 2
        if s_ < 2: continue
        for ang in (0, math.pi / 2):
            dx, dy = s_ * math.cos(ang), s_ * math.sin(ang)
            cv2.line(f, (int(px - dx), int(py - dy)), (int(px + dx), int(py + dy)), C(WHITE), 4, cv2.LINE_AA)


def diyas_row(f, t, y=1520, xs=(150, 930)):
    for i, x in enumerate(xs): diya(f, x, y, 0.75, t, i)


def lights(f, t, y=300, n=9):
    """string of festive lights across the top (decoration only)."""
    P = [(int(-20 + i * (W + 40) / 40), int(y + 40 * math.sin(math.pi * i / 40))) for i in range(41)]
    cv2.polylines(f, [np.array(P, np.int32)], False, C(INK), 4, cv2.LINE_AA)
    cols = ((255, 199, 30), (255, 92, 40), (60, 200, 140), (236, 72, 140))
    for i in range(n):
        x, y_ = P[int(2 + i * 36 / (n - 1))]; on = (int(t * 3) + i) % 3 != 0
        glow(f, x, y_ + 18, 26, cols[i % 4], 0.5 if on else 0.15)
        cv2.circle(f, (x, y_ + 18), 13, C(cols[i % 4] if on else (120, 110, 100)), -1, cv2.LINE_AA)


def arm_ik(sh, tg, L1, L2):
    """2-bone IK for Chubby's right arm (chub angle convention: degrees from straight down, + outward)."""
    dx, dy = tg[0] - sh[0], tg[1] - sh[1]; d = min(L1 + L2 - 1e-3, math.hypot(dx, dy))
    th = math.degrees(math.atan2(dx, dy)); al = math.degrees(math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1)))
    a1 = th - al; ex, ey = sh[0] + L1 * math.sin(math.radians(a1)), sh[1] + L1 * math.cos(math.radians(a1))
    return a1, math.degrees(math.atan2(tg[0] - ex, tg[1] - ey))


def hold_kaju(s=0.45, **kw): return scale_el(kaju_el(True, **kw), s)


# ---- S0: HOOK — Chubby sweeps a metal detector over a plate of Diwali sweets; it goes BEEP BEEP on the silver ----
TB = T("i1", "silver") - 0.1


def shot_S0(t, n):
    beep = t >= TB
    f = stage("festive", (255, 214, 120), 540, 940, 430)
    lights(f, t, 270)
    if beep: rays(f, 540, 1180, 760, (255, 236, 160), 0.35 * ramp(t, TB, 0.2), t)
    plate_of_sweets(f, 640, 1300, 0.9, t, hi=1 if beep else None)
    sw = 14 * math.sin(t * 5.5) * (1 - 0.8 * ramp(t, TB, 0.2))
    hands = chub(f, 240, 1490, 1.0, la=(20, 10), ra=(95 + sw * 0.3, 100), mouth="o" if beep else munch(t, 0.5)[0], expr="wow" if beep else "happy",
                 brow="up", look=(1, 0.4), bob=4 * math.sin(t * 6))
    hx, hy = hands[1]
    detector(f, hx, hy, 300, 118 + sw, t, beep=1.0 if beep else 0.0)
    diyas_row(f, t)
    if beep: comp(f, burst_el("BEEP BEEP!", YEL_, INK, 52), 820, 820, scale=pin(t, TB + 0.05, 0.22) * (1 - clamp((t - T("i1", "real") + 0.1) / 0.2)))
    ui_word(f, "do you know the", "[SILVER] on sweets", 470, t, 0.12, col=WHITE, acc=(220, 228, 245), size=150, shadow=0.6, lead_col=WHITE, out=T("i1", "is") - 0.05)
    ui_word(f, "is real", "[METAL]?", 470, t, T("i1", "is") - 0.05, col=WHITE, acc=YEL_, size=230, shadow=0.6, lead_col=WHITE)
    return finish(f, n)


# ---- S1: yep — REAL SILVER (element tile slams next to the sweet) ----
def shot_S1(t, n):
    f = stage("steel", (230, 236, 248), 540, 1000, 440); u = lt(t, "S1")
    rays(f, 540, 1080, 700, (240, 244, 255), 0.25, t)
    rot_comp(f, scale_el(kaju_el(True, face=True, mood="happy"), 1.55), 540, 1080 + 8 * math.sin(t * 3), 4 * math.sin(t * 2), pin(t, st_("S1"), 0.3), 1.0, 0.35)
    twinkle(f, 540, 1020, 420, 160, t, 7, 3)
    tr = T("i2", "Real") - 0.1
    if t >= tr: slam(f, elem_el("Ag", 47, "SILVER"), 830, 760, -6, t, tr, 0.85)
    if t >= tr: label_at(f, "REAL SILVER LEAF", 300, 760, t, tr + 0.25, 430, 1000)
    wui(f, "yep, real", "[SILVER]", t, st_("S1") + 0.08, acc=(220, 228, 245), size=210)
    return finish(f, n)


# ---- S1b: and you EAT it (Chubby munches the sweet, metal sparkles) ----
def shot_S1b(t, n):
    f = stage("saffron", (255, 236, 170), 540, 960, 430); u = lt(t, "S1b")
    m, c = munch(t, 0.3)
    chub(f, 540, 1470, 1.12, la=(20, 10), ra=(148, -130), mouth=m, brow="up", expr="happy", hold=hold_kaju(0.42), hold_off=(-40, -16), hold_front=True,
         bob=5 * math.sin(t * 16), lean=-2 * math.sin(t * 8))
    hx, hy = head_pos(540, 1470, 1.12)
    sparkles(f, hx + 40, hy + 80, t, T("i2", "eat") - 0.1, 12, 200, (240, 244, 255))
    diyas_row(f, t)
    comp(f, burst_el("CHOMP!", WHITE, INK, 56), 830, 820, scale=pin(t, T("i2", "eat") - 0.05, 0.22))
    ui_word(f, "and you", "[EAT] it!", 470, t, st_("S1b") + 0.05, col=INK, acc=RED_, size=220)
    return finish(f, n)


# ---- S2: open loop — some of it might NOT be silver (a dull fake sweet sneaks in) ----
def shot_S2(t, n):
    f = stage("purple", (200, 190, 255), 540, 980, 420); u = lt(t, "S2")
    tn = T("i3", "not") - 0.1
    plate_of_sweets(f, 540, 1300, 1.0, t, fake_i=2 if t >= tn else None)
    k = ramp(t, st_("S2") + 0.2, 0.5)
    rot_comp(f, scale_el(kaju_el(True, face=True, mood="sly", fake=True), 0.9), 1180 - 400 * k, 980, -8 * math.sin(t * 4), 1.0, 1.0, 0.3)
    if t >= tn:
        comp(f, magnifier_el(), 330 + 20 * math.sin(t * 2), 1000, scale=0.95)
        comp(f, burst_el("FAKE?", RED_, WHITE, 56), 820, 760, scale=pin(t, tn + 0.05, 0.22))
        comp(f, chip("COMING UP: THE FAKES", INK, YEL_, 30), 540, 1460, op=clamp((t - tn - 0.3) / 0.3))
    wui(f, "some might", "[NOT] be silver", t, st_("S2") + 0.15, acc=(255, 120, 120), size=180)
    return finish(f, n)


# ---- S3: PART 1 — it's called VARK (name card; iris opened from the sweet) ----
def shot_S3(t, n):
    f = stage("steel", (236, 240, 250), 540, 1000, 450); u = lt(t, "S3")
    rot_comp(f, leaf_el(460, 460, 2), 540, 1020 + 10 * math.sin(t * 1.8), 6 * math.sin(t * 1.3), pin(t, st_("S3") + 0.1, 0.35), 1.0, 0.35)
    twinkle(f, 540, 1020, 420, 420, t, 8, 5)
    chapter_card(f, t, st_("S3") + 0.05, 1, "WHAT IS IT?", y=1400, dur=1.5, col=(220, 228, 245))
    wui(f, "it's called", "[VARK]", t, T("a1", "vark.") - 0.12, acc=YEL_, size=240)
    return finish(f, n)


# ---- S3b: a thin sheet of real silver (the leaf peels off the sweet) ----
def shot_S3b(t, n):
    f = stage("saffron", (255, 240, 190), 540, 1000, 420); u = lt(t, "S3b")
    comp(f, scale_el(kaju_el(False), 1.4), 540, 1240)
    k = ramp(t, st_("S3b") + 0.2, 0.7)
    rot_comp(f, scale_el(leaf_el(420, 300, 7), 1.0), 540 + 60 * k, 1200 - 360 * k, -14 * k + 3 * math.sin(t * 2), 1.0, 1.0, 0.25 * k)
    label_at(f, "THIN SHEET", 840, 700, t, st_("S3b") + 0.7, 700, 820)
    label_at(f, "SWEET", 240, 1420, t, st_("S3b") + 0.9, 380, 1300)
    ui_word(f, "a thin sheet of", "[REAL SILVER]", 470, t, st_("S3b") + 0.05, col=INK, acc=(110, 120, 150), size=150)
    return finish(f, n)


# ---- S4: the rules say it must be pure (rule document slams) ----
def shot_S4(t, n):
    f = stage("emerald", (220, 250, 230), 540, 1000, 420); u = lt(t, "S4")
    slam(f, rule_doc_el("FOOD RULE", "INDIA", ("silver leaf", "must be", "PURE")), 540, 1060, -3, t, st_("S4") + 0.15, 1.05)
    tp = T("a2", "pure.") - 0.15
    if t >= tp: rot_comp(f, scale_el(lump_el(), 0.8), 860, 1320, 6 * math.sin(t * 3), pin(t, tp, 0.3), 1.0, 0.3)
    wui(f, "the rules say it must be", "[PURE]", t, st_("S4") + 0.1, acc=YEL_, size=220)
    return finish(f, n)


# ---- S4b: at least 99.9 % (kinetic count-up + purity bar) ----
def shot_S4b(t, n):
    f = stage("steel"); u = lt(t, "S4b")
    v = 99.9 * eo(clamp((t - st_("S4b") - 0.1) / 1.0))
    x0, x1, y = 160, 920, 1080
    cv2.rectangle(f, (x0 - 10, y - 70), (x1 + 10, y + 70), C(INK), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y - 60), (x0 + int((x1 - x0) * v / 100), y + 60), C(SILV), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y - 60), (x0 + int((x1 - x0) * v / 100), y - 30), C(WHITE), -1, cv2.LINE_AA)
    comp(f, chip("SILVER", INK, WHITE, 30), 300, y + 120)
    if v > 99.8: comp(f, chip("0.1% OTHER", INK, YEL_, 24), 860, y + 120, op=clamp((t - st_("S4b") - 1.1) / 0.3))
    twinkle(f, 540, y, 700, 100, t, 5, 9)
    ui_word(f, "at least", f"[{v:.1f}%]", 560, t, st_("S4b") + 0.05, col=WHITE, acc=YEL_, size=200, shadow=0.6, lead_col=WHITE)
    comp(f, chip("Source: FSSAI silver leaf standard, 2016", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.4) / 0.3))
    return finish(f, n)


# ---- S5: how do you turn a LUMP into a sheet you can eat? (question, Chubby scratches his head) ----
def shot_S5(t, n):
    f = stage("yellow", (255, 250, 210), 540, 1000, 420); u = lt(t, "S5")
    tl = T("a3", "lump") - 0.15; ts = T("a3", "sheet") - 0.15
    if t >= tl: rot_comp(f, scale_el(lump_el(), 0.95), 330, 1010, 0, pin(t, tl, 0.3), 1.0, 0.3)
    if t >= ts:
        draw_arrow(f, 470, 1010, 600, 1010, ramp(t, ts, 0.3), INK, 12, 36)
        comp(f, ed_el("", "?", "", big_col=RED_, big_size=120), 535, 900, scale=pin(t, ts + 0.1, 0.25))
        rot_comp(f, scale_el(leaf_el(300, 260, 4), 0.85), 780, 1010, 4 * math.sin(t * 2), pin(t, ts, 0.3), 1.0, 0.3)
    chub(f, 540, 1500, 0.74, la=(-150, -150), ra=(20, 10), mouth=0, expr="sus", brow="sus", look=(0, -0.7))
    ui_word(f, "how do you turn a", "[LUMP] into a [SHEET]?", 470, t, st_("S5") + 0.1, col=INK, acc=RED_, size=130)
    return finish(f, n)


# ---- S6: PRE-TRAINING cast — meet the 3 parts before the process (silver bits, thin sheets, hammer) ----
def shot_S6(t, n):
    f = stage("cream", (255, 236, 200), 540, 1000, 380); u = lt(t, "S6")
    items = [(scale_el(lump_el(), 0.62), "SILVER BITS", "LUMP > LEAF"), (scale_el(paper_el(None, 220, 260), 0.62), "THIN SHEETS", "HOLD IT"),
             (scale_el(hammer_el(), 0.42), "HAMMER", "BEATS IT")]
    ts = [st_("S6") + 0.15, T("a4", "small") - 0.1, T("a4", "silver") - 0.1]
    cast_card(f, items, t, ts, y=1060, gap=285, title="MEET THE CAST")
    ui_word(f, "", "[FIRST]", 470, t, st_("S6") + 0.05, col=INK, acc=RED_, size=200)
    return finish(f, n)


# ---- S6b: bits of silver go between thin sheets (the packet builds up layer by layer) ----
def shot_S6b(t, n):
    f = stage("teal", (120, 200, 190), 540, 1000, 400); u = lt(t, "S6b")
    nl = 1 + int(5 * ramp(t, st_("S6b") + 0.05, max(0.4, SHOT["S6b"]["end"] - st_("S6b") - 0.4)))
    k = 1.0 - ramp(t, SHOT["S6b"]["end"] - 0.5, 0.4)
    packet(f, 540, 1240, 1.5, k_open=k * 2.5, n=nl, t=t)
    label_at(f, "SHEET", 220, 1360, t, st_("S6b") + 0.2, 290, 1255, bg=(120, 80, 50))
    label_at(f, "SILVER BIT", 860, 1050, t, st_("S6b") + 0.4, 600, 1180, bg=(110, 120, 150))
    wui(f, "silver goes", "[BETWEEN] sheets", t, st_("S6b") + 0.05, acc=YEL_, size=150)
    return finish(f, n)


# ---- S7: then they HAMMER it (Chubby swings the hammer on an arc; thud + dust on each hit) ----
PX, PY = 740, 1400
GRIP = (566, 1180)


def hammer_scene(f, t, t0, period=0.5, s=1.0):
    ang, hit = hammer_swing(t, t0, period, up=62, down=5)
    sq = 0.0
    if t >= t0:
        ph = ((t - t0) % period) / period; sq = math.exp(-((ph - 0.98) % 1.0) * 30) if ph > 0.9 or ph < 0.1 else 0.0
    packet(f, PX, PY, 1.0, 0.0, 6, t, squash=0.25 * sq)
    gx, gy = GRIP[0], GRIP[1] + 6 * math.sin(math.radians(ang))
    a1, a2 = arm_ik((466.2, 1245.1), (gx, gy), 76 * 0.9, 70 * 0.9)
    chub(f, 360, 1480, 0.9, la=(20, 10), ra=(a1, a2), mouth=2 if sq > 0.3 else 0, expr="happy", brow="up", look=(1, 0.3))
    rot_comp(f, scale_el(hammer_el(), 0.85), gx, gy, ang, 1.0, 1.0, 0.2)
    cv2.circle(f, (int(gx), int(gy)), 17, C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(gx), int(gy)), 12, C(CH_SKIN), -1, cv2.LINE_AA)
    if sq > 0.2:
        dust_puff(f, PX, PY - 150, t, t - 0.05, 6, 0.4, int(t * 2))
        sparkles(f, PX, PY - 170, t, t - 0.1, 8, 120, (240, 244, 255), int(t * 2))
    return sq


def shot_S7(t, n):
    f = stage("orange", (255, 214, 150), 540, 980, 420); u = lt(t, "S7")
    hammer_scene(f, t, T("a5", "hammer") - 0.35, 0.55)
    wui(f, "then they", "[HAMMER] it", t, st_("S7") + 0.1, acc=YEL_, size=210)
    return finish(f, n)


# ---- S7b: again and again, for HOURS (clock spins while the beating goes on) ----
def shot_S7b(t, n):
    f = stage("red", (255, 190, 120), 540, 980, 400); u = lt(t, "S7b")
    hammer_scene(f, t, st_("S7b") - 0.2, 0.42)
    hh = (u * 3) % 12; mm = (u * 180) % 60
    comp(f, scale_el(clock_el(int(hh), int(mm)), 0.75), 840, 760, scale=pin(t, st_("S7b") + 0.1, 0.3))
    th = T("a5", "hours.") - 0.15
    if t >= th: comp(f, chip("FOR HOURS", INK, YEL_, 34), 840, 940, op=clamp((t - th) / 0.2))
    wui(f, "again and", "[AGAIN]", t, st_("S7b") + 0.05, acc=YEL_, size=220)
    return finish(f, n)


# ---- S8: with every hit it spreads wider and thinner (magnified cross-section, step by step) ----
def shot_S8(t, n):
    f = stage("steel", (230, 236, 248), 540, 1000, 420); u = lt(t, "S8")
    hits = int((u - 0.2) / 0.45) + 1 if u > 0.2 else 0
    k = min(1.0, hits / 6)
    wv = 140 + 620 * k; hv = 110 * (1 - k) ** 2 + 6
    cy = 1080
    cv2.rectangle(f, (120, cy - 200), (960, cy + 200), C(INK), -1, cv2.LINE_AA)
    cv2.rectangle(f, (130, cy - 190), (950, cy + 190), C((60, 66, 86)), -1, cv2.LINE_AA)
    for sgn in (-1, 1):   # the two sheets squeezing it
        yy = cy + sgn * (hv / 2 + 34)
        cv2.rectangle(f, (150, int(yy - 30)), (930, int(yy + 30)), C((150, 110, 70)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(540 - wv / 2), int(cy - hv / 2)), (int(540 + wv / 2), int(cy + hv / 2)), C(SILV), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(540 - wv / 2), int(cy - hv / 2)), (int(540 + wv / 2), int(cy - hv / 2 + max(2, hv * 0.25))), C(WHITE), -1, cv2.LINE_AA)
    for sgn in (-1, 1): draw_arrow(f, 540 + sgn * wv / 2, cy - 130, 540 + sgn * (wv / 2 + 70), cy - 130, 1.0 if k > 0 else 0, YEL_, 8, 24)
    comp(f, chip(f"HIT x{hits}" if hits else "CLOSE-UP", INK, YEL_, 30), 540, cy + 250)
    comp(f, chip("SIDE VIEW, MAGNIFIED", INK, WHITE, 24), 540, cy - 240)
    if hits and (u - 0.2) % 0.45 < 0.08: f += 0.06
    ui_word(f, "spreads wider and", "[THINNER]", 470, t, st_("S8") + 0.1, col=WHITE, acc=(220, 228, 245), size=210, shadow=0.6, lead_col=WHITE)
    return finish(f, n)


# ---- S9: PART 2 — how thin? ----
def shot_S9(t, n):
    f = stage("saffron", (255, 240, 190), 540, 1000, 420); u = lt(t, "S9")
    rot_comp(f, scale_el(leaf_el(380, 380, 3), 1.0), 540, 1050, 8 * math.sin(t * 2), pin(t, st_("S9") + 0.05, 0.3), 1.0, 0.3)
    comp(f, magnifier_el(), 700 + 30 * math.sin(t * 2.5), 1160, scale=0.9)
    chapter_card(f, t, st_("S9") + 0.02, 2, "HOW THIN?", y=1400, dur=1.4, col=YEL_)
    ui_word(f, "how", "[THIN]?", 470, t, st_("S9") + 0.05, col=INK, acc=RED_, size=240)
    return finish(f, n)


# ---- S9b: a square metre of normal paper weighs about 80 g (scale count-up) ----
def shot_S9b(t, n):
    f = stage("cream", (240, 250, 255), 540, 1000, 400); u = lt(t, "S9b")
    te = T("b1", "eighty") - 0.15
    g = count_up(t, te - 0.5, 80, 0.6) if t >= te - 0.5 else 0
    comp(f, kscale_el(f"{g} g"), 540, 1300)
    k = ramp(t, st_("S9b") + 0.15, 0.4)
    rot_comp(f, scale_el(paper_el("1 m²", 300, 360), 1.0), 540, 700 + 420 * k, 0, 1.0, 1.0, 0.3)
    label_at(f, "PRINTER PAPER", 240, 900, t, T("b1", "normal") - 0.1, 400, 1000)
    if t >= te: slam(f, stamp_el("80 g", INK, 64), 840, 820, -6, t, te)
    ui_word(f, "a square metre of", "[PAPER]", 470, t, st_("S9b") + 0.05, col=INK, acc=(40, 110, 200), size=200)
    return finish(f, n)


# ---- S10: the same size of silver leaf: LESS THAN 3 g (two scales side by side) ----
def shot_S10(t, n):
    f = stage("steel", (236, 240, 250), 540, 1000, 380); u = lt(t, "S10")
    t3 = T("b2", "three") - 0.15
    comp(f, scale_el(kscale_el("80 g"), 0.72), 290, 1320); comp(f, scale_el(paper_el(None, 300, 360), 0.66), 290, 1110)
    gv = 2.8 * eo(clamp((t - st_("S10") - 0.5) / max(0.3, t3 - st_("S10") - 0.5)))
    comp(f, scale_el(kscale_el(f"{gv:.1f} g", (255, 230, 120)), 0.72), 790, 1320)
    rot_comp(f, scale_el(leaf_el(300, 360, 6), 0.66), 790, 1120 - 3 * math.sin(t * 4), 2 * math.sin(t * 3), pin(t, st_("S10") + 0.2, 0.3), 1.0, 0.25)
    comp(f, chip("PAPER", INK, WHITE, 26), 290, 900); comp(f, chip("SILVER LEAF", INK, WHITE, 26), 790, 900)
    if t >= t3: slam(f, burst_el("< 3 g!", YEL_, INK, 60), 790, 760, -6, t, t3)
    ui_word(f, "same size of silver leaf", "[UNDER 3 g]", 470, t, st_("S10") + 0.05, col=WHITE, acc=YEL_, size=170, shadow=0.6, lead_col=WHITE)
    comp(f, chip("max 2.8 g per square metre (FSSAI 2016)", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.6) / 0.3))
    return finish(f, n)


# ---- S11: hundreds of times thinner than a HAIR (iris into a magnified view: hair end-on vs leaf edge-on) ----
def shot_S11(t, n):
    f = stage("purple", (200, 210, 255), 540, 1000, 440); u = lt(t, "S11")
    cv2.circle(f, (540, 1000), 380, C(INK), -1, cv2.LINE_AA); cv2.circle(f, (540, 1000), 368, C((250, 248, 240)), -1, cv2.LINE_AA)
    hair_cross(f, 660, 900, 150 * pin(t, st_("S11") + 0.2, 0.35), t, leaf_w=560)
    label_at(f, "A HAIR (END ON)", 300, 720, t, st_("S11") + 0.4, 450, 820, bg=(110, 70, 40))
    label_at(f, "SILVER LEAF (EDGE ON)", 470, 1300, t, T("b3", "thinner") - 0.2, 560, 1123, bg=(80, 90, 120))
    comp(f, chip("MAGNIFIED", YEL_, INK, 26), 820, 1300, op=clamp((u - 0.2) / 0.3))
    wui(f, "hundreds of times thinner than a", "[HAIR]", t, st_("S11") + 0.1, acc=YEL_, size=200)
    return finish(f, n)


# ---- S12: so one sweet carries just a few milligrams (tiny scale, Chubby happy) ----
def shot_S12(t, n):
    f = stage("festive", (255, 214, 140), 540, 980, 420); u = lt(t, "S12")
    lights(f, t, 270)
    rot_comp(f, scale_el(kaju_el(True, face=True, mood="happy"), 0.95), 760, 1080 + 6 * math.sin(t * 3), 0, 1.0, 1.0, 0.3)
    comp(f, scale_el(kscale_el("few mg", (255, 230, 120)), 0.7), 760, 1290)
    twinkle(f, 760, 1050, 300, 120, t, 4, 2)
    chub(f, 280, 1480, 0.8, la=(20, 10), ra=(70, 40), mouth=talk(t), expr="happy", brow="up", look=(1, 0))
    wui(f, "silver on one sweet: just a", "[FEW MILLIGRAMS]", t, st_("S12") + 0.1, acc=YEL_, size=130)
    return finish(f, n)


# ---- S13: PART 3 — the hammering had a SECRET (dark set, padlocked packet) ----
def shot_S13(t, n):
    f = stage("purple", (120, 90, 200), 540, 1000, 420); u = lt(t, "S13")
    packet(f, 540, 1250, 1.4, 0.0, 6, t)
    tsec = T("c1", "secret.") - 0.15
    spotlight(f, 540, 1150, 330, 0.55 * ramp(t, st_("S13") + 0.2, 0.4))
    if t >= tsec:
        comp(f, padlock_el(False), 540, 1000, scale=pin(t, tsec, 0.3) * 0.9)
        comp(f, burst_el("SECRET!", RED_, WHITE, 56), 820, 780, scale=pin(t, tsec + 0.05, 0.22))
    chapter_card(f, t, st_("S13") + 0.02, 3, "THE SECRET", y=1420, dur=1.4, col=(255, 140, 160))
    wui(f, "now, the", "[WEIRD] part", t, st_("S13") + 0.1, acc=(255, 140, 160), size=200)
    return finish(f, n)


# ---- S14: silver was beaten between layers of ... ----
def shot_S14(t, n):
    f = stage("teal", (220, 250, 240), 540, 1000, 400); u = lt(t, "S14")
    packet(f, 540, 1250, 1.4, 1.2, 6, t)
    comp(f, ed_el("", "?", "", big_col=RED_, big_size=160), 540, 1060 + 6 * math.sin(t * 5))
    label_at(f, "WHAT WERE THESE?", 790, 1430, t, st_("S14") + 0.3, 700, 1270, bg=RED_)
    wui(f, "silver was beaten between", "[LAYERS] of...", t, st_("S14") + 0.1, acc=YEL_, size=170)
    return finish(f, n)


# ---- S14b: ... ANIMAL GUTS (layers turn into pink gut tubes; Chubby gasps) ----
def shot_S14b(t, n):
    f = stage("red", (120, 20, 40), 600, 1100, 400); u = lt(t, "S14b")
    packet(f, 650, 1290, 1.15, 1.0, 6, t, gut=True)
    rot_comp(f, scale_el(cow_el(), 0.7), 800, 840, 6 * math.sin(t * 2), pin(t, st_("S14b") + 0.1, 0.3), 1.0, 0.3)
    label_at(f, "ANIMAL GUT", 820, 1460, t, st_("S14b") + 0.3, 720, 1290, bg=INK)
    chub(f, 260, 1480, 0.85, la=(150, 175), ra=(150, 175), mouth="o", expr="wow", brow="up", look=(1, 0), squash=0.2 * math.exp(-max(0, u) * 5))
    wui(f, "", "[ANIMAL GUTS]", t, st_("S14b") + 0.05, acc=(255, 220, 220), size=200)
    return finish(f, n)


# ---- S15: your vegetarian sweet... wasn't always vegetarian (VEG mark gets crossed) ----
def veg_mark(f, x, y, s, broken=0.0):
    cv2.rectangle(f, (int(x - 60 * s), int(y - 60 * s)), (int(x + 60 * s), int(y + 60 * s)), C(WHITE), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - 60 * s), int(y - 60 * s)), (int(x + 60 * s), int(y + 60 * s)), C((20, 150, 60)), int(10 * s), cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), int(32 * s), C((20, 150, 60)), -1, cv2.LINE_AA)
    if broken > 0:
        k = clamp(broken)
        for sg in (-1, 1):
            p0 = (x - 80 * s, y - sg * 80 * s); p1 = (x - 80 * s + 160 * s * k, y - sg * 80 * s + sg * 160 * s * k)
            cv2.line(f, (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1])), C(INK), int(26 * s), cv2.LINE_AA)
            cv2.line(f, (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1])), C(RED_), int(14 * s), cv2.LINE_AA)


def shot_S15(t, n):
    f = stage("yellow", (255, 250, 210), 540, 1000, 420); u = lt(t, "S15")
    tw = T("c3", "wasn't") - 0.15
    chub(f, 360, 1480, 1.0, la=(20, 10), ra=(148, -130), mouth=0 if t < tw else "o", expr="happy" if t < tw else "wow", brow="up", look=(1, -0.2),
         hold=hold_kaju(0.42), hold_off=(-40, -16), hold_front=True)
    veg_mark(f, 780, 960, 1.4, ramp(t, tw, 0.2))
    comp(f, chip("VEG", (20, 150, 60), WHITE, 34), 780, 1130)
    if t >= tw: comp(f, burst_el("WAIT, WHAT?", WHITE, INK, 46), 780, 740, scale=pin(t, tw + 0.1, 0.22))
    ui_word(f, "your vegetarian sweet", "[WASN'T ALWAYS]", 470, t, st_("S15") + 0.05, col=INK, acc=RED_, size=150, tail="vegetarian")
    return finish(f, n)


# ---- S16: 2016 — India's food regulator BANNED animal parts ----
def shot_S16(t, n):
    f = stage("emerald", (220, 250, 230), 540, 1000, 420); u = lt(t, "S16")
    comp(f, scale_el(rule_doc_el("FOOD RULE", "2016", ("silver leaf:", "99.9% pure", "no animal parts")), 1.0), 540, 1050, scale=pin(t, st_("S16") + 0.1, 0.3))
    tb = T("c4", "banned") - 0.1
    if t >= tb: slam(f, stamp_el("BANNED", RED_, 80), 540, 1260, -8, t, tb)
    if t >= tb: rot_comp(f, scale_el(cow_el(), 0.45), 860, 760, -10, 1.0, 0.9, 0.3)
    wui(f, "in", "[2016]", t, st_("S16") + 0.05, acc=YEL_, size=230, out=tb - 0.05)
    if t >= tb: wui(f, "animal parts", "[BANNED]", t, tb, acc=(255, 140, 140), size=200)
    comp(f, chip("Source: FSSAI notification, July 2016", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.5) / 0.3))
    return finish(f, n)


# ---- S17: now: special paper or plastic sheets (clean packet, check) ----
def shot_S17(t, n):
    f = stage("sky", (240, 250, 255), 540, 1000, 420); u = lt(t, "S17")
    packet(f, 540, 1260, 1.4, 0.8, 6, t)
    tp = T("c5", "paper") - 0.15; tq = T("c5", "plastic") - 0.15
    if t >= tp: comp(f, scale_el(paper_el("PAPER", 220, 260), 0.75), 280, 900, scale=pin(t, tp, 0.3))
    if t >= tq:
        rot_comp(f, scale_el(paper_el("PLASTIC", 220, 260), 0.75), 800, 900, 6, pin(t, tq, 0.3), 0.9, 0.3)
        comp(f, check_el(46, True), 540, 860, scale=pin(t, tq + 0.3, 0.25))
    wui(f, "now: special", "[PAPER] or [PLASTIC]", t, st_("S17") + 0.1, acc=YEL_, size=140)
    return finish(f, n)


# ---- S18: PART 4 — the fakes I promised (detective Chubby with a magnifier) ----
def shot_S18(t, n):
    f = stage("purple", (190, 170, 255), 540, 1000, 420); u = lt(t, "S18")
    rot_comp(f, scale_el(kaju_el(True, face=True, mood="sly", fake=True), 1.1), 760, 1080 + 8 * math.sin(t * 4), -6 * math.sin(t * 3), 1.0, 1.0, 0.3)
    chub(f, 300, 1480, 0.9, la=(20, 10), ra=(70, 40), mouth=0, expr="sus", brow="sus", look=(1, 0),
         hold=magnifier_el(), hold_off=(40, -40), hold_front=True)
    chapter_card(f, t, st_("S18") + 0.02, 4, "THE FAKES", y=760, dur=1.4, col=(255, 140, 140))
    wui(f, "now, the", "[FAKE] silver", t, st_("S18") + 0.1, acc=(255, 140, 140), size=200)
    return finish(f, n)


# ---- S19: scientists in Lucknow tested 178 sheets (grid fills, count-up) ----
def shot_S19(t, n):
    f = stage("steel", (236, 240, 250), 540, 1000, 380); u = lt(t, "S19")
    scientist(f, 190, 1480, 0.62, la=(70, 40), ra=(20, 10), mouth=talk(t), expr="happy", brow="up", look=(1, 0))
    tn = T("d2", "hundred") - 0.15
    nn = count_up(t, tn, 178, 1.0) if t >= tn else 0
    cols = 12
    for i in range(nn):
        r, c = divmod(i, cols); x = 400 + c * 44; y = 760 + r * 42
        cv2.rectangle(f, (x - 17, y - 15), (x + 17, y + 15), C(INK), -1, cv2.LINE_AA)
        cv2.rectangle(f, (x - 13, y - 11), (x + 13, y + 11), C(SILV), -1, cv2.LINE_AA)
    comp(f, chip("LUCKNOW, INDIA", INK, WHITE, 28), 640, 700, op=clamp((t - T("d2", "Lucknow") + 0.1) / 0.3))
    ui_word(f, "they tested", f"[{nn}] sheets" if t >= tn else "[SHOP] silver", 470, t, st_("S19") + 0.05, col=INK, acc=RED_, size=180)
    comp(f, chip("Source: Das, Dixit & Khanna, Food Addit Contam 2005", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.5) / 0.3))
    return finish(f, n)


# ---- S20: about one in ten wasn't silver at all (10 leaves; one goes dull) ----
def shot_S20(t, n):
    f = stage("red", (255, 200, 170), 540, 1000, 380); u = lt(t, "S20")
    tt = T("d3", "ten") - 0.1
    for i in range(10):
        r, c = divmod(i, 5); x = 220 + c * 160; y = 900 + r * 260
        fake = i == 7 and t >= tt + 0.2
        el = scale_el(leaf_el(170, 200, 20 + i, fake=fake), 0.9)
        rot_comp(f, el, x, y + (14 * math.sin(t * 7) if fake else 0), 0, pin(t, st_("S20") + 0.04 * i, 0.25), 1.0, 0.2)
        if fake: cv2.circle(f, (x, y), 130, C(YEL_), 8, cv2.LINE_AA)
    wui(f, "about", "[1 IN 10]", t, st_("S20") + 0.05, acc=YEL_, size=230)
    return finish(f, n)


# ---- S20b: it was ALUMINIUM (element tiles: Ag crossed, Al slams) ----
def shot_S20b(t, n):
    f = stage("steel", (220, 226, 236), 540, 1000, 400); u = lt(t, "S20b")
    comp(f, elem_el("Ag", 47, "SILVER"), 300, 1050, scale=0.95)
    k = clamp((u - 0.1) / 0.2)
    for sg in (-1, 1):
        cv2.line(f, (300 - 110, int(1050 - sg * 120)), (int(300 - 110 + 220 * k), int(1050 - sg * 120 + sg * 240 * k)), C(INK), 28, cv2.LINE_AA)
        cv2.line(f, (300 - 110, int(1050 - sg * 120)), (int(300 - 110 + 220 * k), int(1050 - sg * 120 + sg * 240 * k)), C(RED_), 16, cv2.LINE_AA)
    ta = T("d3", "aluminum!") - 0.2
    if t >= ta: slam(f, elem_el("Al", 13, "ALUMINIUM", ALU, bad=True), 780, 1050, 4, t, ta, 1.05)
    if t >= ta: comp(f, scale_el(leaf_el(220, 180, 31, fake=True), 0.9), 780, 1360)
    wui(f, "it was", "[ALUMINIUM]", t, st_("S20b") + 0.05, acc=(255, 140, 140), size=170)
    return finish(f, n)


# ---- S21: less than half were as pure as the rule says (46 % vs 54 % bars) ----
def shot_S21(t, n):
    f = stage("cream", (255, 236, 210), 540, 1000, 380); u = lt(t, "S21")
    k = ramp(t, st_("S21") + 0.3, 0.8)
    for x, v, lab, col in ((330, 46, "99.9% PURE", (90, 170, 120)), (750, 54, "LESS PURE", (220, 90, 70))):
        h_ = 6.5 * v * k
        cv2.rectangle(f, (x - 110, int(1360 - h_)), (x + 110, 1360), C(INK), -1, cv2.LINE_AA)
        cv2.rectangle(f, (x - 100, int(1360 - h_ + 10)), (x + 100, 1350), C(col), -1, cv2.LINE_AA)
        comp(f, chip(f"{int(round(v * k))}%", INK, WHITE, 36), x, 1360 - h_ - 50)
        comp(f, chip(lab, INK, WHITE, 26), x, 1410)
    th = T("d4", "half") - 0.15
    if t >= th: slam(f, stamp_el("UNDER HALF", RED_, 50), 330, 820, -6, t, th)
    ui_word(f, "pure enough? less than", "[HALF]", 470, t, st_("S21") + 0.05, col=INK, acc=RED_, size=220)
    comp(f, chip("of the real-silver sheets", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.6) / 0.3))
    return finish(f, n)


# ---- S22: tiny traces of lead and nickel (iris into a magnified leaf with specks; element tiles) ----
def shot_S22(t, n):
    f = stage("purple", (190, 180, 255), 540, 1000, 440); u = lt(t, "S22")
    def close(g):
        g[:] = np.array(C(SILV), np.float32); twinkle(g, 540, 1000, 600, 600, t, 8, 4)
        rng = np.random.default_rng(3)
        for i in range(26):
            x, y = rng.uniform(260, 820), rng.uniform(720, 1280); col = ((90, 90, 110), (60, 140, 120), (180, 120, 60))[i % 3]
            cv2.circle(g, (int(x), int(y)), int(rng.uniform(6, 14)), C(col), -1, cv2.LINE_AA)
    inset(f, 540, 1000, 300, close, pin(t, st_("S22") + 0.05, 0.3))
    tl = T("d5", "lead") - 0.15; tn_ = T("d5", "nickel.") - 0.15
    if t >= tl: slam(f, elem_el("Pb", 82, "LEAD", (190, 190, 210), bad=True), 230, 760, -8, t, tl, 0.7)
    if t >= tn_: slam(f, elem_el("Ni", 28, "NICKEL", (200, 214, 200), bad=True), 850, 760, 8, t, tn_, 0.7)
    comp(f, chip("tiny specks of other metals", INK, WHITE, 26), 540, 1360, op=clamp((u - 0.3) / 0.3))
    wui(f, "tiny traces of", "[OTHER METALS]", t, st_("S22") + 0.1, acc=YEL_, size=150)
    return finish(f, n)


# ---- S23: PART 5 — here's the twist ----
def shot_S23(t, n):
    f = stage("saffron", (255, 236, 170), 540, 980, 430); u = lt(t, "S23")
    rays(f, 540, 1000, 760, (255, 240, 190), 0.3, t)
    chub(f, 540, 1480, 1.0, la=(150, 175), ra=(150, 175), mouth=2, expr="wow", brow="up", look=(0, -0.5), bob=8 * abs(math.sin(t * 6)))
    chapter_card(f, t, st_("S23") + 0.02, 5, "THE TWIST", y=760, dur=1.3, col=YEL_)
    ui_word(f, "here's the", "[TWIST]", 470, t, st_("S23") + 0.05, col=INK, acc=RED_, size=230)
    return finish(f, n)


# ---- S23b: Europe allows silver as a food colour too (bottle labelled with its additive code) ----
def shot_S23b(t, n):
    f = stage("sky", (236, 246, 255), 540, 1000, 420); u = lt(t, "S23b")
    rot_comp(f, scale_el(colour_bottle_el("E174"), 1.25), 540, 1080 + 6 * math.sin(t * 2), 4 * math.sin(t * 1.5), pin(t, st_("S23b") + 0.05, 0.3), 1.0, 0.35)
    twinkle(f, 540, 1180, 200, 160, t, 4, 6)
    label_at(f, "FOOD COLOUR E174", 820, 800, t, T("e1", "food") - 0.15, 620, 960)
    comp(f, scale_el(kaju_el(True), 0.5), 250, 1380); comp(f, scale_el(barfi_el((150, 220, 130)), 0.5), 830, 1380)
    wui(f, "in Europe, silver is a", "[FOOD COLOUR]", t, st_("S23b") + 0.05, acc=YEL_, size=160)
    return finish(f, n)


# ---- S24: but its food safety experts can't confirm it's safe yet (panel + stamp) ----
def shot_S24(t, n):
    f = stage("steel", (236, 240, 250), 540, 1000, 380); u = lt(t, "S24")
    for i, x in enumerate((230, 540, 850)):
        scientist(f, x, 1480, 0.6, la=(20, 10), ra=(-150, -150) if i == 1 else (20, 10), mouth=0, expr="sus", brow="sus", look=(0, -0.4), bob=3 * math.sin(t * 3 + i))
    comp(f, scale_el(colour_bottle_el("E174"), 0.9), 540, 790)
    tc = T("e2", "can't") - 0.1
    if t >= tc: slam(f, stamp_el("CAN'T CONFIRM SAFE", RED_, 46), 540, 960, -5, t, tc)
    wui(f, "europe's experts", "[CAN'T CONFIRM]", t, st_("S24") + 0.05, acc=(255, 140, 140), size=150)
    comp(f, chip("Source: EFSA opinions on silver (E174), 2016 and 2025", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.5) / 0.3))
    return finish(f, n)


# ---- S25: not proven harmful — there just isn't enough data (data gauge half empty, two honest chips) ----
def shot_S25(t, n):
    f = stage("cream", (240, 246, 255), 540, 1000, 380); u = lt(t, "S25")
    gauge_tube(f, 260, 760, 1360, 0.35 * ramp(t, st_("S25") + 0.2, 0.6), 1.0, 90, (90, 170, 255), "")
    comp(f, chip("DATA", INK, WHITE, 30), 260, 700)
    th = T("e3", "harmful.") - 0.2; td = T("e3", "data.") - 0.2
    if t >= th: comp(f, chip("HARMFUL? NOT PROVEN", INK, WHITE, 34), 680, 960, op=clamp((t - th) / 0.2), scale=pin(t, th, 0.3))
    if t >= td: comp(f, chip("SAFE? NOT CONFIRMED", INK, YEL_, 34), 680, 1110, op=clamp((t - td) / 0.2), scale=pin(t, td, 0.3))
    ui_word(f, "just not enough", "[DATA]", 470, t, st_("S25") + 0.05, col=INK, acc=(40, 110, 200), size=220)
    return finish(f, n)


# ---- S26: so the silver is real ----
def shot_S26(t, n):
    f = stage("festive", (255, 214, 140), 540, 980, 420); u = lt(t, "S26")
    lights(f, t, 270)
    plate_of_sweets(f, 540, 1150, 1.4, t, hi=1)
    twinkle(f, 540, 1100, 640, 200, t, 9, 8)
    diyas_row(f, t)
    wui(f, "so the silver is", "[REAL]", t, st_("S26") + 0.05, acc=(220, 228, 245), size=230)
    return finish(f, n)


# ---- S26b: there for SHINE, not for health (check vs cross) ----
def shot_S26b(t, n):
    f = stage("yellow", (255, 250, 210), 540, 1000, 400); u = lt(t, "S26b")
    ts = T("f1", "shine,") - 0.15; th = T("f1", "health.") - 0.15
    rot_comp(f, scale_el(kaju_el(True), 1.0), 300, 1080, 0, 1.0, 1.0, 0.3); twinkle(f, 300, 1050, 260, 100, t, 5, 3)
    if t >= ts: comp(f, check_el(56, True), 300, 820, scale=pin(t, ts, 0.25)); comp(f, chip("SHINE", INK, WHITE, 34), 300, 1290)
    if t >= th:
        comp(f, check_el(56, False), 780, 820, scale=pin(t, th, 0.25)); comp(f, chip("HEALTH", INK, WHITE, 34), 780, 1290)
        chub_head_only(f, 780, 1060, 0.9, t, mouth=0, expr="sus", brow="sus")
    ui_word(f, "for shine,", "[NOT] for health", 470, t, st_("S26b") + 0.05, col=INK, acc=RED_, size=170)
    return finish(f, n)


# ---- S27: recap 1-2-3 ----
def shot_S27(t, n):
    f = stage("steel", (236, 240, 250), 540, 1000, 380); u = lt(t, "S27")
    items = [(scale_el(elem_el("Ag", 47, "SILVER"), 0.62), "REAL SILVER"), (scale_el(hammer_el(), 0.4), "HAMMERED THIN"),
             (scale_el(kaju_el(True, face=True, mood="sly", fake=True), 0.5), "SOMETIMES FAKE")]
    ts = [T("f2", "real") - 0.15, T("f2", "hammered") - 0.15, T("f2", "sometimes") - 0.15]
    recap_steps(f, items, 1000, t, ts, 300, 1.0)
    wui(f, "", "[REMEMBER]", t, st_("S27") + 0.05, acc=YEL_, size=200)
    return finish(f, n)


# ---- S28: buy from a shop you trust, enjoy as a treat (sweet-shop counter, Diwali lights) ----
def shot_S28(t, n):
    f = stage("saffron", (255, 236, 170), 540, 980, 420); u = lt(t, "S28")
    lights(f, t, 270)
    comp(f, scale_el(counter_el("SWEET SHOP", (255, 120, 80), 640, 300), 1.0), 620, 1300)
    plate_of_sweets(f, 620, 1130, 0.7, t)
    chub(f, 210, 1480, 0.82, la=(20, 10), ra=(150, 175), mouth=talk(t), expr="happy", brow="up", look=(1, -0.2))
    tt = T("f3", "treat.") - 0.15
    if t >= tt: comp(f, burst_el("TREAT!", YEL_, INK, 52), 860, 780, scale=pin(t, tt, 0.22))
    ui_word(f, "a shop you trust,", "[A TREAT]", 470, t, st_("S28") + 0.05, col=INK, acc=RED_, size=200)
    return finish(f, n)


# ---- S29: send it + FreshNestHub sting ----
def shot_S29(t, n):
    f = stage("festive", (255, 236, 200), 540, 880, 420); u = lt(t, "S29")
    vend = LINES["f4"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("f4", "Send") + 0.3
        comp(f, scale_el(phone2_el("is the silver real??", "REAL. and sometimes FAKE", pr), 0.82), 650, 950, scale=pin(t, st_("S29")))
        if pr and t < T("f4", "Send") + 0.75:
            rr = (t - T("f4", "Send") - 0.3) / 0.45
            cv2.circle(f, (650, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        m, c = munch(t, 0.3)
        chub(f, 250, 1480, 0.8, la=(20, 10), ra=(148, -130), mouth=m, expr="happy", brow="up", look=(1, 0), hold=hold_kaju(0.36), hold_off=(-30, -16), hold_front=True)
        ui_word(f, "send to the friend who grabs the", "[SILVER SWEET]", 420, t, T("f4", "friend") - 0.1, col=WHITE, acc=YEL_, size=150, shadow=0.6, lead_col=WHITE)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INK, lead_size=42), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1480, 0.7, la=(20, 10), ra=(148, -130), mouth=munch(t, 0.3)[0], expr="happy", brow="up", hold=hold_kaju(0.3), hold_off=(-20, -10), hold_front=True)
        diyas_row(f, t)
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TB, 0.45, 20), (T("i2", "Real") - 0.1, 0.3, 14), (T("i2", "eat") - 0.05, 0.3, 12), (T("i3", "not") - 0.1, 0.3, 12),
           (T("a1", "vark.") - 0.12, 0.3, 12), (st_("S4") + 0.15, 0.3, 14), (T("a2", "ninety-nine") - 0.1, 0.25, 10),
           (T("a5", "hammer") - 0.05, 0.3, 14), (T("b1", "eighty") - 0.15, 0.3, 12), (T("b2", "three") - 0.15, 0.4, 18),
           (T("b3", "hair.") - 0.2, 0.3, 12), (T("c1", "secret.") - 0.15, 0.35, 16), (st_("S14b") + 0.05, 0.5, 24),
           (T("c3", "wasn't") - 0.15, 0.35, 16), (T("c4", "banned") - 0.1, 0.4, 20), (T("d3", "ten") - 0.1, 0.3, 12),
           (T("d3", "aluminum!") - 0.2, 0.45, 22), (T("d4", "half") - 0.15, 0.3, 14), (T("d5", "lead") - 0.15, 0.25, 10),
           (T("e1", "twist.") - 0.15, 0.35, 16), (T("e2", "can't") - 0.1, 0.4, 18), (T("f1", "health.") - 0.15, 0.25, 10)]


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
