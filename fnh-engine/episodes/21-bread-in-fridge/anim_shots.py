# ================= shots: FreshNestHub 21 — "Does the fridge make bread go stale faster?" (Chubby INK, ep 5 of the ink look) ===
# COLOUR SCRIPT (5-colour ink palette + ONE accent): CRUST GOLD = bread, starch, titles; COLD BLUE = fridge / freezer. Places: the NEW morning worktop (set_worktop +
# worktop_front with drawers + towel), the NEW inside-a-slice world (set_crumb), paper stages for the race + the recap. CRAFT (ep 21): VISEMES — when Chubby talks
# his mouth makes the real sound shapes (anim_fx.viseme); big face close-ups so you can see it. The hero explaining device is a RACE (positions = staling speed).
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "You") - 0.2, "whip"), ("S1b", T("i2", "but") - 0.12, "punch"),
    ("S2", T("i3", "And") - 0.2, "focus"),
    ("S3", T("a1", "Everybody") - 0.2, "flash"), ("S3b", T("a1", "But") - 0.15, "whip"), ("S3c", T("a1", "and") - 0.1, "punch"),
    ("S4", T("a2", "So") - 0.2, "whip"), ("S4b", T("a2", "It's") - 0.15, "zoom"),
    ("S5", T("a3", "And") - 0.2, "whip"), ("S5b", T("a3", "It's") - 0.1, "punch"),
    ("S6", T("b1", "When") - 0.2, "zoom"), ("S6b", T("b1", "and") - 0.1, "whip"),
    ("S7", T("b2", "But") - 0.2, "whip"), ("S7b", T("b2", "the", 1) - 0.1, "zoom"),
    ("S8", T("b3", "And") - 0.2, "punch"), ("S8b", T("b3", "So") - 0.15, "whip"),
    ("S9", T("b4", "That's") - 0.2, "flash"),
    ("S10", T("c1", "So,") - 0.2, "focus"), ("S10b", T("c2", "Yep,") - 0.15, "flash"),
    ("S11", T("c2", "Those") - 0.15, "whip"),
    ("S12", T("c3", "One") - 0.2, "whip"), ("S12b", T("c3", "That's") - 0.15, "punch"),
    ("S13", T("c4", "It") - 0.2, "whip"), ("S13b", T("c4", "Starch") - 0.15, "punch"),
    ("S14", T("d1", "But") - 0.2, "flash"), ("S14b", T("d1", "In") - 0.15, "whip"),
    ("S15", T("d2", "So") - 0.2, "zoom"),
    ("S16", T("e1", "The") - 0.2, "flash"),
    ("S17", T("e2", "Toast") - 0.2, "whip"), ("S17b", T("e2", "and") - 0.1, "zoom"), ("S17c", T("e2", "so") - 0.1, "punch"),
    ("S18", T("e3", "It's") - 0.2, "whip"), ("S18b", T("e3", "Once") - 0.15, "punch"), ("S18c", T("e3", "so") - 0.1, "zoom"),
    ("S19", T("f1", "One") - 0.2, "flash"), ("S19b", T("f1", "so") - 0.1, "whip"),
    ("S20", T("f2", "But") - 0.2, "whip"), ("S20b", T("f2", "Slice") - 0.15, "punch"),
    ("S21", T("f3", "Then") - 0.2, "whip"), ("S21b", T("f3", "No") - 0.12, "punch"),
    ("S22", T("g1", "So") - 0.2, "flash"), ("S23", T("g2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
SRC_K = "Source: America's Test Kitchen · ScienceABC"
SRC_G = "Source: University of Guelph (Food Science)"
SRC_T = "Source: Colorado State (via TODAY) · Milling MEA"
SRC_F = "Source: Federation of Bakers · Food Republic"
TOP = 1330
RED_I = (176, 52, 44)


def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def icap(f, lead, big, t, t0, acc=ACC_S, size=150, y=440, out=None, tail="", dark=False):
    if dark: ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.6, lead_col=WHITE, out=out, tail=tail)
    else: ui_word(f, lead, big, y, t, t0, col=INKC, acc=acc, size=size, shadow=0.0, lead_col=INKC, out=out, tail=tail)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def ichip(text, size=26, inv=False): return chip(text, INKC if not inv else MILK, MILK if not inv else INKC, size)


def achip(text, size=30): return chip(text, ACC_S, MILK, size)


def bchip(text, size=30): return chip(text, BLUE_S, MILK, size)


def t3(f, text, y, t, t0, size=230, face=None, side=None, x=540):
    if t >= t0: title_ink(f, text, y, t, t0, size=size, face=face or ACC_L, side=side or ACC_S, depth=18, x=x)


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, MILK, 22), 540, y, op=clamp((t - t0) / 0.2))


def pos_keys(t, keys):
    v = keys[0][1]
    for (a, va), (b, vb) in zip(keys, keys[1:]):
        if t >= a: v = va + (vb - va) * eio(clamp((t - a) / max(1e-3, b - a)))
    return v


def fridge_at(f, x, y, s, open_=True, top=False, loaf=False, stale=0.0, mood_=None, cap=False, look=(0, 0), loaf_x=170, frost_=0.0):
    """y = floor line. The loaf sits on the middle shelf (shelf top at local y 600)."""
    comp(f, scale_el(fridge_ink_el(open_, top), s), x, y - 480 * s)
    if open_ and loaf:
        lx = x + (loaf_x - 280) * s; ly = y + (600 - 930) * s - 6 * s - 80 * s
        comp(f, scale_el(loaf_el(stale, mood_, look, cap, frost_), 0.5 * s), lx, ly)
    return (x, y - 480 * s)


def cold_glow(f, x, y, r=420, a=0.28): glow(f, x, y, r, (190, 228, 255), a)


def hammer_k(t, off=0.28, per=0.62):
    m = (t - off) % per
    if m < 0.38: return 1 - eio(m / 0.38)
    if m < 0.53: return 0.0
    return ((m - 0.53) / 0.09) ** 2


def hammer_hits(t, off=0.28, per=0.62): return max(0, int((t - off) // per) + 1)


def toaster_scene(f, t, x=690, up=0.0, hot=0.0, frozen=0.0, stale=0.0, toast=0.0, n=1, y=TOP - 82, s=0.82):
    """draw slices rising out of the slot, then the toaster in front. up 0 = down inside, 1 = popped."""
    for j in range(n):
        el = scale_el(bread_slice_el(stale, None, (0, 0), frozen, toast, seed=3 + j), 0.62 * s)
        comp(f, el, x + (j - (n - 1) / 2) * 96 * s, y - 118 * s - 170 * s * up)
    comp(f, scale_el(toaster_el(hot), s), x, y)
    if hot > 0: glow(f, x, y - 118 * s, 200, (255, 120, 50), 0.22 * hot)


def card(f, x, y, w, h, col=(252, 248, 238), edge=INKC, k=1.0):
    if k <= 0: return
    ww, hh = int(w * k / 2), int(h * k / 2)
    cv2.rectangle(f, (int(x - ww + 8), int(y - hh + 10)), (int(x + ww + 8), int(y + hh + 10)), C((120, 100, 80)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - ww), int(y - hh)), (int(x + ww), int(y + hh)), C(col), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - ww), int(y - hh)), (int(x + ww), int(y + hh)), C(edge), 6, cv2.LINE_AA)


# ---- S0: HOOK — on the morning worktop Chubby is HAMMERING A NAIL with a slice of fridge bread (already mid-swing at frame 0); fridge door open behind ----
def shot_S0(t, n):
    f = set_worktop(t)
    fridge_at(f, 150, TOP + 20, 0.72, True, False, False)
    cold_glow(f, 150, 950, 320, 0.2)
    tf = T("i1", "faster") - 0.12
    t3(f, "FASTER?", 800, t, tf, 200)
    x = 470; s = 1.1; y = 1500
    stop = T("i1", "than")
    k = hammer_k(t) if t < stop else 0.0
    hx = x + 188 * s + (34 * s) * k; hy = y - 335 * s + 130 * s * k
    sh = (x + 118 * s, y - 261 * s)
    a1, a2 = arm_ik(sh, (hx, hy), 76 * s, 70 * s)
    chub(f, x, y, s, t=t, la=(28, 14), ra=(a1, a2), mouth=talk(t), expr="wow" if t > tf else "sus", brow="up" if t > tf else "sus", look=(1, 0.3), lean=4 + 3 * k, hair=(-6 * k, 0))
    worktop_front(f, TOP)
    nx, ny = 830, 1205
    comp(f, scale_el(nail_el(min(1, hammer_hits(min(t, stop)) / 6)), 0.9), nx, ny)
    rot = -62 + 78 * k
    cx_ = hx + 100 * math.sin(math.radians(rot + 68)); cy_ = hy - 60 + 70 * k
    rot_comp(f, scale_el(bread_slice_el(1.0), 0.62), cx_, cy_, -rot - 30, 1.0, 1.0, 0.0)
    grip_hand(f, hx, hy, s)
    icap(f, "do you know your fridge makes", "[BREAD] go stale", t, 0.1, size=110, y=440)
    if t >= T("i1", "counter") - 0.2: comp(f, achip("FRIDGE VS COUNTER", 32), 540, 1420)
    return finish(f, n, look="warm")


# ---- S1: 'You think you're protecting that loaf in there' — Chubby tucks a loaf in on the fridge shelf, nightcap on ----
def shot_S1(t, n):
    f = set_worktop(t) * 0.92
    fridge_at(f, 720, TOP + 30, 0.86, True, False, True, 0, "happy", True, loaf_x=205)
    cold_glow(f, 700, 900, 420, 0.3)
    chub(f, 290, 1500, 1.0, t=t, **nolean(POSE["present"]), mouth=talk(t), expr="happy", brow="up", look=(1, -0.1), lean=6)
    zzs(f, 700, 680, t, 3, ACC_S, 0.9)
    worktop_front(f, TOP)
    icap(f, "safe in the", "[FRIDGE]?", t, st_("S1") + 0.25, size=150, acc=BLUE_S, y=420)
    return finish(f, n, look="fresh")


# ---- S1b: '...but you're actually aging it' — close on the shelf: the same loaf goes grey + cracked while a clock spins ----
def shot_S1b(t, n):
    f = ink_set("coldb", (255, 255, 255), 540, 960, 430)
    t0 = st_("S1b"); ta = T("i2", "aging") - 0.1
    t3(f, "AGING", 700, t, ta, 250, BLUE_L, BLUE_S)
    k = ramp(t, ta - 0.2, 1.2)
    comp(f, scale_el(loaf_el(k, "sad" if k > 0.4 else "happy", (0, 0), True), 1.3), 540, 1090)
    comp(f, scale_el(clock_ink_el(), 0.7), 860, 1290)
    clock_hands(f, 860, 1290, 8 + 14 * (t - t0) * 2, 110, 0.7)
    f = crash_zoom(f, t, ta, 1.1, 540, 950)
    return finish(f, n, look="cool")


# ---- S2: 'And the strangest part is, stale bread isn't even dry' — a lights-drop aside: big face close-up, Chubby leans in (visemes on show) ----
def shot_S2(t, n):
    f = set_worktop(t) * 0.45
    k = pin(t, st_("S2"), 0.2)
    chub_head_only(f, 540, 1000, 2.5 * k, t, mouth=None, expr="sus", brow="sus", look=(-0.2, 0.1))
    tI = T("i3", "isn't") - 0.1
    if t >= tI: comp(f, scale_el(bread_slice_el(0.9), 0.55), 860, 1320, scale=pin(t, tI))
    icap(f, "stale bread isn't even", "[DRY]", t, tI, size=170, dark=True, y=440, acc=ACC_L)
    return finish(f, n, look="night")


# ---- S3: 'Everybody thinks stale means dried out' — the myth: a slice in the desert, water drops flying off it, MYTH tag ----
def shot_S3(t, n):
    f = ink_set("toastp", (255, 240, 180), 540, 900, 420)
    t0 = st_("S3")
    comp(f, scale_el(sun_ink_el(), 0.8), 840, 660)
    comp(f, scale_el(bread_slice_el(ramp(t, t0, 2.2), "sad", (0, -1)), 1.0), 500, 1060)
    rng = np.random.default_rng(4)
    for i in range(9):
        ph = ((t - t0) * 0.6 + i / 9) % 1; xx = 500 + rng.uniform(-150, 150); yy = 960 - 300 * ph
        cv2.circle(f, (int(xx), int(yy)), 15, C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(xx), int(yy)), 12, C((110, 176, 236)), -1, cv2.LINE_AA)
    chub(f, 860, 1500, 0.8, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="n", brow="up", look=(-1, 0))
    myth_tag(f, 300, 660, t, T("a1", "dried") - 0.1)
    icap(f, "stale means", "[DRIED OUT]?", t, t0 + 0.3, size=130, y=440)
    return finish(f, n, look="golden")


# ---- S3b: 'But seal a loaf up so tight that no water can escape' — an airtight box with clamps, the drops bounce inside ----
def shot_S3b(t, n):
    f = ink_set("breadp", (255, 255, 255), 540, 980, 430)
    t0 = st_("S3b"); bx0, by0, bx1, by1 = 170, 790, 910, 1290
    comp(f, scale_el(loaf_el(0, "n"), 1.05 * pin(t, t0 + 0.1, 0.3)), 540, 1090)
    rng = np.random.default_rng(6); d_ = t - t0
    for i in range(8):
        vx, vy = rng.uniform(160, 300) * rng.choice([-1, 1]), rng.uniform(160, 300) * rng.choice([-1, 1]); x0_, y0_ = rng.uniform(bx0 + 40, bx1 - 40), rng.uniform(by0 + 40, by1 - 40)
        wx = (x0_ - bx0 - 24 + vx * d_) % (2 * (bx1 - bx0 - 48)); wx = wx if wx < (bx1 - bx0 - 48) else 2 * (bx1 - bx0 - 48) - wx
        wy = (y0_ - by0 - 24 + vy * d_) % (2 * (by1 - by0 - 48)); wy = wy if wy < (by1 - by0 - 48) else 2 * (by1 - by0 - 48) - wy
        cv2.circle(f, (int(bx0 + 24 + wx), int(by0 + 24 + wy)), 14, C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(bx0 + 24 + wx), int(by0 + 24 + wy)), 11, C((110, 176, 236)), -1, cv2.LINE_AA)
    ov = f.copy(); cv2.rectangle(ov, (bx0, by0), (bx1, by1), C((206, 232, 250)), -1, cv2.LINE_AA); f[:] = f * 0.82 + ov * 0.18
    cv2.rectangle(f, (bx0, by0), (bx1, by1), C(INKC), 10, cv2.LINE_AA)
    cv2.line(f, (bx0 + 40, by0 + 30), (bx0 + 12, by1 - 60), C((255, 255, 255)), 6, cv2.LINE_AA)
    cv2.rectangle(f, (bx0 - 16, by0 - 40), (bx1 + 16, by0 + 6), C((60, 100, 150)), -1, cv2.LINE_AA); cv2.rectangle(f, (bx0 - 16, by0 - 40), (bx1 + 16, by0 + 6), C(INKC), 7, cv2.LINE_AA)
    for xx in (240, 840): cv2.rectangle(f, (xx - 28, by0 - 56), (xx + 28, by0 + 40), C((226, 232, 238)), -1, cv2.LINE_AA); cv2.rectangle(f, (xx - 28, by0 - 56), (xx + 28, by0 + 40), C(INKC), 6, cv2.LINE_AA)
    icap(f, "no water can", "[ESCAPE]", t, T("a1", "water") - 0.1, size=140, y=440, acc=BLUE_S)
    comp(f, chip("SEALED", BLUE_S, MILK, 40), 540, 1340, scale=pin(t, T("a1", "seal") - 0.05))
    return finish(f, n, look="fresh")


# ---- S3c: '...and it still goes hard' — Chubby knocks on the sealed loaf: clonk, MYTH BUSTED ----
def shot_S3c(t, n):
    f = ink_set("breadp", (255, 255, 255), 700, 980, 400)
    th = T("a1", "hard") - 0.15; k = ramp(t, st_("S3c"), 0.6)
    comp(f, scale_el(loaf_el(k, "sad"), 1.0), 710, 1180)
    knock = (abs(math.sin((t - st_("S3c")) * 8.0)) > 0.7)
    chub(f, 260, 1500, 1.0, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="wow" if t > th else "sus", brow="up", look=(1, 0.2), hand_r="grip", lean=5 + (3 if knock else 0))
    myth_tag(f, 760, 720, t, st_("S3c") - 0.1, t_bust=th, word="MYTH")
    icap(f, "it still goes", "[HARD]", t, T("a1", "still") - 0.1, size=170, y=440)
    src(f, SRC_G, t, st_("S3c") + 0.2)
    return finish(f, n, look="warm")


# ---- S4: 'So where did the water go? Nowhere.' — Chubby the detective with the magnifier, looks left, looks right, crash zoom on Nowhere ----
def shot_S4(t, n):
    f = set_worktop(t) * 0.97
    tn = T("a2", "Nowhere.") - 0.1
    lk = keyed(t, [(st_("S4"), -1.0), (st_("S4") + 0.9, 1.0), (tn, 0.0)])
    t3(f, "NOWHERE", 720, t, tn, 190)
    chub(f, 540, 1500, 1.1, t=t, la=(30, 14), ra=(100, 110), mouth=talk(t), expr="sus" if t < tn else "wow", brow="sus" if t < tn else "up", look=(lk, 0), hold=scale_el(magnifier_ink_el(), 0.7), hold_off=(40, -30), hand_r="grip", hold_front=True, lean=4 * lk)
    worktop_front(f, TOP)
    comp(f, scale_el(bread_slice_el(0.9), 0.5), 190, 1240)
    if t < tn: comp(f, chip("WHERE DID THE WATER GO?", INKC, MILK, 34), 540, 620, op=clamp((t - st_("S4") - 0.2) / 0.2))
    f = crash_zoom(f, t, tn, 1.12, 540, 900)
    return finish(f, n, look="warm")


# ---- S4b: 'It's still in there, it's just been locked up' — inside the slice: water drops locked between rows, padlocks pop ----
def shot_S4b(t, n):
    f = set_crumb(t, 0.5)
    tl = T("a2", "locked") - 0.12
    starch_lock(f, 540, 1000, 1.0, t, 680, 420, 6, ramp(t, tl, 0.5))
    icap(f, "still in there,", "[LOCKED UP]", t, st_("S4b") + 0.1, size=130, y=440, acc=BLUE_S)
    comp(f, chip("INSIDE THE SLICE", INKC, MILK, 30), 540, 1360)
    return finish(f, n, look="warm")


# ---- S5: 'And if you saw our leftover rice video, you've already met the culprit' — a pebble-rice bowl callback ----
def shot_S5(t, n):
    f = set_worktop(t)
    chub(f, 300, 1500, 1.0, t=t, **nolean(POSE["whisper"]), mouth=talk(t), expr="smirk", brow="up", look=(1, 0))
    worktop_front(f, TOP)
    comp(f, scale_el(rice_bowl_el("hard", 5, "sad"), 0.82), 760, 1190, scale=pin(t, st_("S5") + 0.2))
    comp(f, achip("REMEMBER THE RICE?", 34), 700, 900, scale=pin(t, st_("S5") + 0.5))
    icap(f, "you've met the", "[CULPRIT]", t, T("a3", "met") - 0.1, size=140, y=440)
    return finish(f, n, look="warm")


# ---- S5b: 'It's starch.' — WANTED poster slams, the starch chain guy looks sideways ----
def shot_S5b(t, n):
    f = ink_set("breadp", (255, 255, 255), 540, 960, 460)
    t0 = st_("S5b"); ts = T("a3", "starch") - 0.1
    slam(f, wanted_el(), 540, 1040, -2, t, t0, 1.0)
    t3(f, "WANTED", 620, t, t0 + 0.03, 120, (140, 60, 40), INKC)
    if t >= t0 + 0.1: comp(f, scale_el(starch_guy_el("angry" if t > ts else "n", (1, 0)), 0.8), 540, 1040, scale=pin(t, t0 + 0.1))
    t3(f, "STARCH", 1270, t, ts, 150)
    f = crash_zoom(f, t, ts, 1.1, 540, 1000)
    return finish(f, n, look="warm")


# ---- S6: 'When bread bakes, the starch in the flour soaks up water and swells' — inside the crumb, chains + drops; they swell ----
def shot_S6(t, n):
    f = set_crumb(t, 0.0)
    tw = T("b1", "water") - 0.1; ts = T("b1", "swells,") - 0.1
    starch_lock(f, 590, 1000, 0.0, t, 620, 400 + 50 * ramp(t, ts, 0.5), 6, 0.0, ramp(t, ts, 0.5))
    if t >= T("b1", "starch") - 0.1: comp(f, achip("STARCH", 40), 260, 770, scale=pin(t, T("b1", "starch") - 0.1))
    if t >= tw: comp(f, bchip("WATER", 40), 850, 770, scale=pin(t, tw))
    chub(f, 150, 1500, 0.72, t=t, **nolean(POSE["present"]), mouth=talk(t), expr="happy", brow="up", look=(1, -0.3))
    icap(f, "in the oven it", "[SWELLS]", t, st_("S6") + 0.2, size=160, y=440)
    src(f, SRC_G, t, st_("S6") + 0.4)
    return finish(f, n, look="golden")


# ---- S6b: 'and that's what makes the inside so soft' — Chubby squishes a pillowy slice, it bounces back ----
def shot_S6b(t, n):
    f = set_worktop(t)
    t0 = st_("S6b"); ts = T("b1", "soft.") - 0.15
    t3(f, "SOFT", 740, t, ts, 260)
    press = 0.5 + 0.5 * math.sin((t - t0) * 7.0)
    el = scale_xy(scale_el(bread_slice_el(0, "love"), 0.95), 1 + 0.10 * press, 1 - 0.14 * press)
    chub(f, 300, 1500, 1.05, t=t, la=(30, 14), ra=(78 + 10 * press, 60), mouth=talk(t), expr="happy", brow="up", look=(1, 0.2), hand_r="open")
    worktop_front(f, TOP)
    comp(f, el, 680, 1205 + 18 * press)
    return finish(f, n, look="golden")


# ---- S7: 'But the second that loaf starts cooling down' — fresh loaf on a rack, steam thinning out ----
def shot_S7(t, n):
    f = set_worktop(t)
    t0 = st_("S7"); tc = T("b2", "cooling") - 0.1
    chub(f, 250, 1500, 0.95, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="sus", brow="up", look=(1, 0))
    worktop_front(f, TOP)
    cv2.rectangle(f, (450, 1312), (980, 1326), C(INKC), -1, cv2.LINE_AA)
    comp(f, scale_el(loaf_el(0, "n"), 0.98), 715, 1158)
    steam_wisps(f, 715, 980, t, 4, 170, 180, (255, 250, 236), 0.75 * (1 - ramp(t, tc, 1.1)), 6)
    icap(f, "the moment it starts", "[COOLING]", t, t0 + 0.2, size=130, y=440, acc=BLUE_S)
    return finish(f, n, look="warm")


# ---- S7b: 'the starch starts squeezing back together, into neat, tight rows, a bit like crystals' — the diagram draws itself ----
def shot_S7b(t, n):
    f = set_crumb(t, 0.25)
    ts = T("b2", "squeezing") - 0.1; tc = T("b2", "crystals.") - 0.1
    k = ramp(t, ts, tc - ts)
    starch_lock(f, 540, 1010, k, t, 680, 430, 6, 0.0)
    if t >= tc:
        for j, (x, y) in enumerate(((170, 830), (910, 860), (210, 1220), (880, 1230))):
            comp(f, scale_el(crystal_el(62), 1.0), x, y, scale=pin(t, tc + 0.05 * j))
    icap(f, "squeezing back into", "[TIGHT ROWS]", t, ts - 0.1, size=120, y=430, out=tc - 0.05)
    t3(f, "CRYSTALS", 640, t, tc, 150)
    return finish(f, n, look="warm")


# ---- S8: 'And those rows trap the water inside them' — padlocks clamp on ----
def shot_S8(t, n):
    f = set_crumb(t, 0.5, 1.05)
    tr = T("b3", "trap") - 0.1
    starch_lock(f, 540, 1000, 1.0, t, 720, 420, 6, ramp(t, tr, 0.6))
    icap(f, "the rows", "[TRAP] the water", t, tr, size=120, y=430, acc=BLUE_S)
    comp(f, bchip("WATER: STILL IN THERE", 34), 540, 1370, scale=pin(t, tr + 0.4))
    src(f, SRC_K, t, tr + 0.5, 1450)
    return finish(f, n, look="warm")


# ---- S8b: 'So it's all still there, but the bread feels dry and hard' — Chubby bites: CLONK, a cartoon take ----
def shot_S8b(t, n):
    f = set_worktop(t)
    tb = T("b3", "feels") - 0.1
    tk = take(t, tb)
    chub(f, 440, 1500 + tk["dy"], 1.15, t=t, la=(30, 14), ra=(148, -130), mouth="jaw" if tb < t < tb + 0.7 else talk(t), expr=tk["expr"] if t > tb else "n", brow=tk["brow"] if t > tb else "n", look=tk["look"], lean=tk["lean"], squash=tk["squash"], hold=scale_el(bread_slice_el(1.0), 0.5), hold_off=(30, -30), hold_front=True)
    worktop_front(f, TOP)
    if tb <= t < tb + 0.55: comp(f, burst_el("CLONK", ACC_L, INKC, 60), 790, 950, scale=pin(t, tb, 0.1))
    icap(f, "it just feels", "[DRY + HARD]", t, tb, size=120, y=440)
    return finish(f, n, look="warm")


# ---- S9: 'That's what stale really is. Your bread isn't drying out, it's setting.' — DRYING crossed out, SETTING slams ----
def shot_S9(t, n):
    f = ink_set("breadp", (255, 255, 255), 540, 980, 440)
    t0 = st_("S9"); td = T("b4", "drying") - 0.1; ts = T("b4", "setting.") - 0.12
    if td <= t < ts + 0.05:
        t3(f, "DRYING", 720, t, td, 200, STALE_C, STALE_S)
        kx = ramp(t, td + 0.45, 0.2)
        cv2.line(f, (120, 730), (int(120 + 840 * kx), 660), C(RED_I), 22, cv2.LINE_AA)
    t3(f, "SETTING", 700, t, ts, 215)
    comp(f, scale_el(loaf_el(0.9, "sad", (-1, 0)), 0.9), 720, 1180)
    chub(f, 250, 1500, 0.98, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="n", brow="up", look=(1, 0), hand_r="point")
    icap(f, "that's what", "[STALE] really is", t, t0 + 0.15, size=110, y=420, out=td)
    f = crash_zoom(f, t, ts, 1.08, 540, 900)
    return finish(f, n, look="warm")


# ---- S10: the GUESS — three loaves on the start line; each lane rings as he names it ----
def shot_S10(t, n):
    f = ink_set("breadp", (255, 255, 255), 540, 980, 480)
    tc = [T("c1", "counter,") - 0.1, T("c1", "freezer,") - 0.1, T("c1", "fridge?") - 0.1]
    race_lanes(f, t, (0, 0, 0))
    for i, tt in enumerate(tc):
        if t >= tt: comp(f, chip("?", ACC_S, MILK, 62), 560, 720 + i * 210 + 48, scale=pin(t, tt))
    icap(f, "quick guess: where is it", "[FASTEST?]", t, st_("S10") + 0.15, size=130, y=440)
    return finish(f, n, look="warm")


# ---- S10b: 'Yep, it's the fridge' — the fridge lane loaf TAKES OFF ----
def shot_S10b(t, n):
    f = ink_set("coldb", (255, 255, 255), 540, 980, 480)
    t0 = st_("S10b")
    p = (0.10 * ramp(t, t0, 1.2), 0.0, 0.2 * ramp(t, t0, 1.0))
    race_lanes(f, t, p, moods=("n", "n", "wow"))
    icap(f, "it's the", "[FRIDGE]", t, t0 + 0.05, size=170, y=440, acc=BLUE_S)
    return finish(f, n, look="fresh")


# ---- S11: 'Those crystals grow fastest when it's cold but not frozen, which is exactly where your fridge sits' — the thermometer ruler with the fast zone ----
def shot_S11(t, n):
    f = ink_set("coldb", (255, 255, 255), 540, 980, 460)
    tc = T("c2", "cold") - 0.1; tfz = T("c2", "frozen,") - 0.1; te = T("c2", "exactly") - 0.1
    X = temp_strip(f, t, y=1040, zone=ramp(t, tc, 0.3))
    if t >= tfz: comp(f, bchip("FROZEN", 34), X(-14), 880, scale=pin(t, tfz))
    if t >= tc:
        comp(f, chip("FASTEST", ACC_S, MILK, 40), X(5), 880, scale=pin(t, tc))
        for j in range(5):
            kk = clamp((t - tc - 0.2 - j * 0.3) / 0.3)
            if kk > 0: comp(f, scale_el(crystal_el(34), kk), X(5) + (j - 2) * 22, 1040 + 20 * ((j * 2) % 3 - 1))
    if t >= te: comp(f, scale_el(fridge_ink_el(False), 0.40), X(5), 620, scale=pin(t, te))
    if t < te: icap(f, "cold, but not", "[FROZEN]", t, tc, size=150, y=440, acc=BLUE_S)
    src(f, "Source: Milling MEA · ScienceABC (0-10 C)", t, tc + 0.3, 1320)
    return finish(f, n, look="fresh")


# ---- S12: 'One big test kitchen says a rustic loaf goes stale within a day in there' — the race reaches the line ----
def shot_S12(t, n):
    f = ink_set("breadp", (255, 255, 255), 540, 980, 480)
    t0 = st_("S12"); td = T("c3", "day") - 0.15
    k = ramp(t, t0 + 0.1, td - t0 - 0.05)
    race_lanes(f, t, (0.1 + 0.4 * k, 0.0, 0.2 + 0.8 * k), moods=("n", "n", "sad" if k > 0.9 else "wow"), stale=(0.2 * k, 0, k))
    if t >= td: comp(f, chip("STALE IN A DAY", RED_I, MILK, 40), 540, 620, scale=pin(t, td))
    icap(f, "one big test kitchen", "", t, t0 + 0.1, size=110, y=440, out=td + 0.8)
    src(f, SRC_K, t, t0 + 0.3, 1400)
    return finish(f, n, look="warm")


# ---- S12b: 'That's about twice as fast as the counter, and some sources say even more' ----
def shot_S12b(t, n):
    f = ink_set("breadp", (255, 255, 255), 540, 980, 480)
    t0 = st_("S12b"); tt = T("c3", "twice") - 0.12; ts = T("c3", "some") - 0.1
    race_lanes(f, t, (0.5, 0.0, 1.0), moods=("n", "n", "sad"), stale=(0.2, 0, 1))
    t3(f, "x2", 520, t, tt, 260)
    if t >= ts: comp(f, achip("SOME SOURCES SAY EVEN MORE", 34), 540, 1390, scale=pin(t, ts))
    src(f, SRC_K, t, t0 + 0.1, 1450)
    f = crash_zoom(f, t, tt, 1.05, 540, 900)
    return finish(f, n, look="warm")


# ---- S13: 'It feels wrong, because cold slows down almost everything in your kitchen. Germs, mould, milk going off.' ----
def shot_S13(t, n):
    f = set_worktop(t) * 0.94
    fridge_at(f, 800, TOP + 30, 0.78, True, False)
    cold_glow(f, 800, 900, 400, 0.28)
    chub(f, 280, 1500, 1.0, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="sus", brow="sus", look=(1, 0))
    worktop_front(f, TOP)
    tg = [T("c4", "Germs,") - 0.1, T("c4", "mould,") - 0.1, T("c4", "milk") - 0.1]
    for j, tt in enumerate(tg):
        if t < tt: continue
        x = 300 + j * 240; yy = 720
        card(f, x, yy, 210, 180, k=pin(t, tt))
        if j == 0: comp(f, scale_el(germ_el("sad", (0, 0)), 0.58), x, yy - 8)
        if j == 1: comp(f, scale_el(bread_slice_el(0, None, (0, 0), 0, 0, 0.6), 0.42), x, yy - 8)
        if j == 2: comp(f, chip("MILK", INKC, MILK, 36), x, yy - 8)
        comp(f, bchip("SLOW", 24), x, yy + 96, scale=pin(t, tt + 0.12))
    icap(f, "cold slows", "[EVERYTHING]", t, st_("S13") + 0.6, size=120, y=440, acc=BLUE_S)
    return finish(f, n, look="fresh")


# ---- S13b: 'Starch is the weird one.' — snow falling, the starch guy loves the cold, crystals piling up ----
def shot_S13b(t, n):
    f = ink_set("coldb", (255, 255, 255), 540, 980, 430)
    t0 = st_("S13b"); tw = T("c4", "weird") - 0.1
    t3(f, "WEIRD", 730, t, tw, 250, BLUE_L, BLUE_S)
    snow(f, t, 0.7, 34, 5, 500, 1500)
    bob_ = abs(math.sin((t - t0) * 7)) * 34
    comp(f, scale_el(starch_guy_el("happy", (0, -1)), 0.95), 540, 1110 - bob_)
    for j in range(6):
        kk = clamp((t - t0 - 0.15 * j) / 0.2)
        if kk > 0: comp(f, scale_el(crystal_el(40), kk), 240 + j * 120, 1340 - (j % 2) * 40)
    return finish(f, n, look="cool")


# ---- S14: 'But go colder, way colder, and it flips.' — the marker on the ruler slides down to -20 ----
def shot_S14(t, n):
    f = ink_set("freeze", (255, 255, 255), 540, 980, 460)
    t0 = st_("S14"); tf = T("d1", "flips.") - 0.12
    mk = 5 - 25 * ramp(t, t0 + 0.2, tf - t0 - 0.2)
    temp_strip(f, t, y=1060, zone=0.5, marker=mk)
    comp(f, scale_el(fridge_ink_el(False, True), 0.42), 240, 700, scale=pin(t, tf))
    frost(f, ramp(t, t0 + 0.3, tf - t0) * 0.5)
    icap(f, "go colder.", "[WAY] colder", t, t0 + 0.2, size=130, y=440, acc=BLUE_S)
    if t >= tf: comp(f, chip("IT FLIPS", ACC_S, MILK, 56), 640, 760, scale=pin(t, tf))
    return finish(f, n, look="cool")


# ---- S14b: 'In a freezer, the starch can barely move, so staling almost stops.' — the starch guy in an ice block; a clock nearly stopped ----
def shot_S14b(t, n):
    f = ink_set("freeze", (255, 255, 255), 540, 980, 480)
    t0 = st_("S14b"); tb = T("d1", "barely") - 0.1; ts = T("d1", "stops.") - 0.12
    ice_block(f, 220, 840, 580, 1300, ramp(t, t0, 0.6), t)
    comp(f, scale_el(starch_guy_el("sad", (0, 0), True, True), 0.92), 400, 1070)
    ov = f.copy(); cv2.rectangle(ov, (222, 842), (578, 1298), C((206, 234, 252)), -1, cv2.LINE_AA); f[:] = f * 0.8 + ov * 0.2
    comp(f, scale_el(clock_ink_el(), 0.9), 800, 880)
    clock_hands(f, 800, 880, 10.2 + 3 * clamp((ts - t) / 0.9), 110, 0.9)
    if t >= ts:
        comp(f, chip("ALMOST STOPPED", BLUE_S, MILK, 34), 790, 1080, scale=pin(t, ts))
        t3(f, "PAUSED", 610, t, ts, 170, FROST, BLUE_S)
    comp(f, ichip("ABOUT -20 C", 28), 400, 1340)
    chub(f, 860, 1500, 0.68, t=t, **nolean(POSE["whisper"]), mouth=talk(t), expr="n", brow="up", look=(-1, 0))
    src(f, SRC_G, t, t0 + 0.2, 1400)
    if t < ts: icap(f, "it can barely", "[MOVE]", t, tb, size=150, y=440, acc=BLUE_S)
    return finish(f, n, look="cool")


# ---- S15: 'So on the counter it's slow, in the fridge it's fast, and in the freezer it's nearly paused.' — the recap race ----
def shot_S15(t, n):
    f = ink_set("breadp", (255, 255, 255), 540, 980, 480)
    ts = [T("d2", "slow,") - 0.1, T("d2", "fast,") - 0.1, T("d2", "paused.") - 0.1]
    t0 = st_("S15")
    p = (pos_keys(t, [(t0, 0.0), (en_("S15"), 0.34)]), 0.01, pos_keys(t, [(t0, 0.0), (t0 + 2.4, 0.78), (en_("S15"), 0.88)]))
    race_lanes(f, t, p, y0=700, moods=("n", "n", "wow"), frost=(0, 0.75, 0))
    for (i, tt, tx, c) in ((0, ts[0], "SLOW", ACC_S), (2, ts[1], "FAST", RED_I), (1, ts[2], "NEARLY PAUSED", BLUE_S)):
        if t >= tt: comp(f, chip(tx, c, MILK, 40), 600, 700 + i * 210 - 30, scale=pin(t, tt))
    return finish(f, n, look="warm")


# ---- S16: 'The good news? Stale bread can come back from the dead.' — dusk graveyard: tombstone, slice zombie pops up ----
def shot_S16(t, n):
    f = inkify(set_dusk(t, 4, 1240), 0.1)
    t0 = st_("S16"); tb = T("e1", "back") - 0.12
    comp(f, scale_el(tomb_el(), 0.95), 720, 1090)
    comp(f, chip("R.I.P. BREAD", INKC, MILK, 30), 720, 990)
    if t >= tb:
        up = eo(clamp((t - tb) / 0.3))
        comp(f, scale_el(bread_slice_el(0.9, "happy", (-1, -0.5)), 0.72), 430, 1370 - 240 * up)
        dust_puff(f, 430, 1290, t, tb, 8)
    cv2.rectangle(f, (0, 1296), (W, H), C((96, 88, 62)), -1, cv2.LINE_AA)
    tk = take(t, tb)
    chub(f, 870, 1500 + tk["dy"], 0.8, t=t, **nolean(POSE["shock"] if t > tb else POSE["idle"]), mouth="jaw" if t > tb else talk(t), expr=tk["expr"] if t > tb else "n", brow="up", look=(-1, 0), lean=tk["lean"])
    icap(f, "the good news?", "", t, t0 + 0.1, size=110, y=440, dark=True, out=tb)
    if t >= tb: icap(f, "back from", "[THE DEAD]", t, tb, size=140, y=440, dark=True, acc=ACC_L)
    return finish(f, n, look="golden")


# ---- S17: 'Toast it, or warm it in the oven' — Chubby drops the stale slice in the toaster ----
def shot_S17(t, n):
    f = set_worktop(t)
    t0 = st_("S17"); tl = T("e2", "Toast") + 0.05
    chub(f, 270, 1500, 1.0, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="happy", brow="up", look=(1, 0.2), hand_r="pinch")
    worktop_front(f, TOP)
    toaster_scene(f, t, 700, up=1 - ramp(t, tl, 0.3), hot=ramp(t, tl + 0.25, 0.6), stale=1.0)
    icap(f, "", "[TOAST] it", t, t0 + 0.1, size=170, y=440)
    return finish(f, n, look="warm")


# ---- S17b: 'and the heat shakes those tight rows loose' — the diagram runs backwards, heat under it ----
def shot_S17b(t, n):
    f = set_crumb(t, 0.25)
    t0 = st_("S17b"); ts = T("e2", "shakes") - 0.1
    k = 1 - ramp(t, ts, 1.0)
    dx = 8 * math.sin(t * 60) * (1 - abs(2 * k - 1))
    starch_lock(f, 540 + dx, 1000, k, t, 680, 430, 6, 0.0)
    glow(f, 540, 1420, 560, (255, 120, 40), 0.55 * ramp(t, t0, 0.3))
    flames(f, 540, 1390, t, 760, 14, 1.0 * ramp(t, t0, 0.3))
    icap(f, "heat shakes the rows", "[LOOSE]", t, ts - 0.1, size=150, y=430)
    src(f, SRC_G, t, t0 + 0.2, 1462)
    return finish(f, n, look="golden")


# ---- S17c: 'so the inside goes soft again' — POP! toast, Chubby holds it up ----
def shot_S17c(t, n):
    f = set_worktop(t)
    ts = T("e2", "soft") - 0.1
    t3(f, "SOFT AGAIN", 720, t, ts, 130)
    chub(f, 300, 1500, 1.08, t=t, **nolean(POSE["hold_up"]), mouth=3 if t > ts else talk(t), expr="happy", brow="up", look=(0.6, -0.4), hold=scale_el(bread_slice_el(0, "love", (0, 0), 0, 0.8), 0.5), hold_off=(10, -60), hold_front=True)
    worktop_front(f, TOP)
    comp(f, scale_el(toaster_el(0.0), 0.82), 760, TOP - 82)
    sparkles(f, 410, 900, t, ts, 10, 200, (255, 214, 120))
    return finish(f, n, look="golden")


# ---- S18: 'It's a one-time rescue, though.' — a '1x' stamp on the toast ----
def shot_S18(t, n):
    f = ink_set("toastp", (255, 255, 255), 540, 980, 430)
    to = T("e3", "one-time") - 0.1
    comp(f, scale_el(bread_slice_el(0, "n", (0, 0), 0, 0.8), 1.15), 540, 1060)
    t3(f, "ONE TIME", 640, t, to, 150)
    if t >= to + 0.2: slam(f, stamp_el("1x ONLY", RED_I, 62), 780, 1320, -9, t, to + 0.2, 1.0)
    return finish(f, n, look="warm")


# ---- S18b: 'Once it cools, it goes hard even faster than before' — clock spin, the toast goes stale ----
def shot_S18b(t, n):
    f = set_worktop(t)
    t0 = st_("S18b"); tf = T("e3", "faster") - 0.1
    k = ramp(t, t0, 1.1)
    t3(f, "FASTER", 720, t, tf, 200)
    chub(f, 260, 1500, 0.96, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="sad", brow="sad", look=(1, 0.2))
    worktop_front(f, TOP)
    comp(f, scale_el(bread_slice_el(k, "sad" if k > 0.5 else "n", (0, 0), 0, 0.7 * (1 - k)), 0.9), 700, 1200)
    comp(f, scale_el(clock_ink_el(), 0.55), 900, 900); clock_hands(f, 900, 900, 8 + (t - t0) * 12, 110, 0.55)
    icap(f, "once it", "[COOLS]", t, t0 + 0.1, size=150, y=440, acc=BLUE_S)
    src(f, "Source: ScienceABC · Milling MEA", t, t0 + 0.2)
    return finish(f, n, look="fresh")


# ---- S18c: 'so warm it right before you eat it' — straight out of the toaster into his mouth, munch ----
def shot_S18c(t, n):
    f = set_worktop(t)
    m_ = 2 if ((t * 2.6) % 1) < 0.5 else 0
    chub(f, 380, 1500, 1.15, t=t, la=(30, 14), ra=(148, -130), mouth=m_, expr="happy", brow="up", look=(0.4, 0), hold=scale_el(bread_slice_el(0, None, (0, 0), 0, 0.8), 0.46), hold_off=(0, -20), hold_front=True)
    worktop_front(f, TOP)
    comp(f, scale_el(toaster_el(0.5), 0.72), 800, TOP - 72)
    steam_wisps(f, 800, 1110, t, 3, 120, 110, (255, 250, 236), 0.6, 4)
    icap(f, "warm it right before", "[YOU EAT IT]", t, st_("S18c") + 0.05, size=120, y=440)
    return finish(f, n, look="golden")


# ---- S19: 'One honest catch. The fridge really does slow down mould' — two slices side by side ----
def shot_S19(t, n):
    f = ink_set("moss", (255, 255, 255), 540, 980, 480)
    t0 = st_("S19"); tm = T("f1", "mould,") - 0.15
    comp(f, chip("ONE HONEST CATCH", INKC, MILK, 42), 540, 440, scale=pin(t, t0 + 0.1))
    k = ramp(t, t0 + 0.4, 2.4)
    card(f, 300, 1050, 400, 560); card(f, 780, 1050, 400, 560, (226, 240, 250))
    comp(f, scale_el(bread_slice_el(0, "sad", (0, 0), 0, 0, k), 0.95), 300, 1050)
    comp(f, scale_el(bread_slice_el(0.5 * k, "n", (0, 0), 0, 0, 0.3 * k), 0.95), 780, 1050)
    comp(f, achip("COUNTER", 34), 300, 800); comp(f, bchip("FRIDGE", 34), 780, 800)
    if t >= tm: comp(f, bchip("MOULD SLOWS DOWN", 40), 540, 620, scale=pin(t, tm))
    src(f, SRC_T, t, t0 + 0.6, 1400)
    return finish(f, n, look="fresh")


# ---- S19b: 'so if it's brutally hot where you live, it isn't the crime I'm making it sound like' ----
def shot_S19b(t, n):
    f = set_worktop(t); mood(f, (255, 150, 60), 0.28)
    th = T("f1", "hot") - 0.12; tc = T("f1", "crime") - 0.12
    comp(f, scale_el(sun_ink_el("angry"), 0.8), 200, 620, scale=pin(t, th))
    fridge_at(f, 780, TOP + 30, 0.72, False, False)
    chub(f, 340, 1500, 1.0, t=t, **nolean(POSE["cheek"]), mouth=talk(t), expr="sad", brow="sad", look=(1, 0))
    sweat(f, 340, 1090, t, 3, 1.0)
    worktop_front(f, TOP)
    if t >= tc: slam(f, stamp_el("NOT A CRIME", (40, 130, 90), 54), 770, 880, -8, t, tc, 1.0)
    icap(f, "brutally", "[HOT]?", t, th, size=170, y=440)
    src(f, "Source: Federation of Bakers", t, th + 0.2)
    return finish(f, n, look="golden")


# ---- S20: 'But your freezer does that job better.' — top door swings, cold light ----
def shot_S20(t, n):
    f = set_worktop(t) * 0.9
    fridge_at(f, 720, TOP + 30, 0.86, False, True)
    cold_glow(f, 720, 700, 320, 0.4)
    chub(f, 290, 1500, 1.0, t=t, **nolean(POSE["present"]), mouth=talk(t), expr="happy", brow="up", look=(1, -0.4))
    worktop_front(f, TOP)
    icap(f, "the", "[FREEZER] does it better", t, T("f2", "freezer") - 0.1, size=100, y=440, acc=BLUE_S)
    return finish(f, n, look="fresh")


# ---- S20b: 'Slice the loaf first, wrap it tight, and freeze it.' — three steps as big cards, in time ----
def shot_S20b(t, n):
    f = ink_set("breadp", (255, 255, 255), 540, 980, 480)
    ts = [T("f2", "Slice") - 0.1, T("f2", "wrap") - 0.1, T("f2", "freeze") - 0.1]
    for j, (tt, y_) in enumerate(zip(ts, (620, 900, 1180))):
        if t < tt: continue
        k = pin(t, tt)
        card(f, 540, y_, 760, 250, k=k)
        comp(f, chip(str(j + 1), ACC_S, MILK, 56), 220, y_, scale=k)
        if j == 0:
            comp(f, scale_el(loaf_el(0), 0.42), 700, y_)
            knife_ink_at(f, 620, y_ - 80, 90 + 6 * math.sin(t * 16), 0.5)
            comp(f, ichip("SLICE", 40), 410, y_)
        if j == 1:
            comp(f, scale_el(freezer_bag_el(4), 0.5), 720, y_)
            comp(f, ichip("WRAP TIGHT", 36), 430, y_)
        if j == 2:
            comp(f, scale_el(freezer_bag_el(4, 1.0), 0.42), 720, y_)
            snow(f, t, 0.3, 16, 5, y_ - 110, y_ + 110)
            comp(f, ichip("FREEZE", 40), 420, y_)
    src(f, "Source: Federation of Bakers · Food Republic", t, ts[0] + 0.2, 1400)
    return finish(f, n, look="fresh")


# ---- S21: 'Then just drop the frozen slices straight in the toaster.' — frosty slices drop in ----
def shot_S21(t, n):
    f = set_worktop(t)
    t0 = st_("S21"); td = T("f3", "straight") - 0.1
    chub(f, 260, 1500, 1.0, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="n", brow="up", look=(1, 0.2), hand_r="pinch")
    worktop_front(f, TOP)
    toaster_scene(f, t, 700, up=1 - ramp(t, td, 0.25), hot=ramp(t, td + 0.3, 0.4), frozen=1.0, n=2)
    dust_puff(f, 700, 1120, t, td + 0.2, 8)
    icap(f, "straight from the", "[FREEZER]", t, t0 + 0.2, size=150, y=440, acc=BLUE_S)
    src(f, SRC_F, t, t0 + 0.3)
    return finish(f, n, look="fresh")


# ---- S21b: 'No thawing needed.' — POP, two golden slices; deadpan ----
def shot_S21b(t, n):
    f = set_worktop(t)
    t0 = st_("S21b")
    chub(f, 260, 1500, 1.0, t=t, **nolean(POSE["tada"]), mouth=talk(t), expr="smirk", brow="up", look=(1, -0.2))
    worktop_front(f, TOP)
    toaster_scene(f, t, 700, up=eo(clamp((t - t0 - 0.05) / 0.14)), hot=0.0, toast=0.85, n=2)
    icap(f, "no thawing", "[NEEDED]", t, t0 + 0.05, size=150, y=440)
    return finish(f, n, look="golden")


# ---- S22: 'So remember it like this: counter for now, freezer for later, and the fridge for literally everything else.' — the mnemonic as three cards ----
def shot_S22(t, n):
    f = ink_set("breadp", (255, 255, 255), 540, 980, 480)
    ts = [T("g1", "now,") - 0.25, T("g1", "later,") - 0.25, T("g1", "else.") - 0.6]
    icap(f, "remember it like", "[THIS]", t, st_("S22") + 0.05, size=130, y=430, out=ts[0])
    if t < ts[0] + 0.1:
        chub(f, 540, 1500 + 320 * ramp(t, ts[0] - 0.25, 0.3), 1.2, t=t, **nolean(POSE["hold_up"]), mouth=talk(t), expr="smirk", brow="up", look=(0.2, -0.3), hand_r="point", lean=4)
    for j, (tt, y_) in enumerate(zip(ts, (620, 900, 1180))):
        if t < tt: continue
        k = pin(t, tt); card(f, 540, y_, 840, 250, k=k)
        if j == 0:
            comp(f, scale_el(bread_bin_el(1.0), 0.5), 260, y_)
            comp(f, scale_el(loaf_el(0, "happy"), 0.28), 262, y_ - 40)
            comp(f, ichip("COUNTER", 34), 620, y_ - 60); comp(f, chip("FOR NOW", ACC_S, MILK, 52), 620, y_ + 30)
        if j == 1:
            comp(f, scale_el(freezer_bag_el(4, 1.0), 0.48), 260, y_)
            comp(f, ichip("FREEZER", 34), 620, y_ - 60); comp(f, chip("FOR LATER", BLUE_S, MILK, 52), 620, y_ + 30)
        if j == 2:
            comp(f, scale_el(fridge_ink_el(True), 0.24), 260, y_)
            comp(f, ichip("FRIDGE", 34), 620, y_ - 60); comp(f, chip("EVERYTHING ELSE", RED_I, MILK, 44), 620, y_ + 30)
    f = push_in(f, t, st_("S22") + 0.3, en_("S22"), 1.04, 540, 950)
    return finish(f, n, look="warm")


# ---- S23: send it (bread next to the eggs) + FreshNestHub sting ----
def shot_S23(t, n):
    f = set_worktop(t) * 0.97
    vend = LINES["g2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("g2", "Send") + 0.3
        comp(f, scale_el(phone2_el("my bread lives by the eggs", "counter or freezer!", pr), 0.82), 720, 930, scale=pin(t, st_("S23")))
        if pr and t < T("g2", "Send") + 0.75:
            rr = (t - T("g2", "Send") - 0.3) / 0.45
            cv2.circle(f, (720, 1200), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 280, 1500, 0.95, t=t, **POSE["point"], mouth=talk(t), expr="happy", brow="up", look=(1, 0), hand_r="point")
        worktop_front(f, TOP)
        ui_word(f, "the friend who keeps bread", "[BY THE EGGS]", 420, t, T("g2", "friend") - 0.1, col=INKC, acc=ACC_S, size=100, shadow=0.0, lead_col=INKC)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INKC, lead_size=42), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 180, 1500, 0.8, t=t, **POSE["cheer"], mouth=3, expr="happy", brow="up")
        worktop_front(f, TOP)
        comp(f, scale_el(loaf_el(0, "happy"), 0.5 * k), 800, 1230)
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "faster") - 0.12, 0.4, 16), (T("i2", "aging") - 0.1, 0.35, 14), (T("i3", "isn't") - 0.1, 0.25, 8),
           (T("a1", "dried") - 0.1, 0.25, 8), (T("a1", "hard") - 0.15, 0.4, 16), (T("a2", "Nowhere") - 0.1, 0.35, 14), (T("a2", "locked") - 0.12, 0.3, 10),
           (T("a3", "starch") - 0.1, 0.4, 16), (st_("S5b") + 0.03, 0.3, 10), (T("b1", "swells,") - 0.1, 0.25, 8), (T("b1", "soft.") - 0.15, 0.25, 8),
           (T("b2", "crystals.") - 0.1, 0.3, 12), (T("b3", "trap") - 0.1, 0.3, 10), (T("b3", "feels") - 0.1, 0.4, 18), (T("b4", "setting.") - 0.12, 0.4, 16),
           (st_("S10b") + 0.05, 0.35, 14), (T("c2", "exactly") - 0.1, 0.25, 8), (T("c3", "day") - 0.15, 0.3, 12), (T("c3", "twice") - 0.12, 0.35, 14),
           (T("c4", "weird") - 0.1, 0.35, 14), (T("d1", "flips.") - 0.12, 0.35, 14), (T("d1", "stops.") - 0.12, 0.3, 10), (T("d2", "fast,") - 0.1, 0.2, 8),
           (T("e1", "back") - 0.12, 0.4, 16), (st_("S17c") + 0.03, 0.35, 14), (T("e3", "one-time") + 0.1, 0.3, 12), (T("e3", "faster") - 0.1, 0.35, 14),
           (T("f1", "hot") - 0.12, 0.25, 8), (T("f1", "crime") - 0.12, 0.3, 12), (st_("S21b") + 0.05, 0.3, 12), (T("g1", "else.") - 0.6, 0.3, 10), (T("g2", "Send") + 0.3, 0.2, 8)]


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
