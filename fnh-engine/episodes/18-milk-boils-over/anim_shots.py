# ================= shots: FreshNestHub 18 — "Why does milk boil over but water never does?" (Chubby INK, ep 2 of the ink look) =================
# COLOUR SCRIPT (5-colour ink palette + ONE accent): paper white = milk / foam; AMBER accent = heat, the proteins, the 'jacket', the skin,
# the lid (everything that CAUSES the boil-over); MINT = the fixes (wide pot, stir, moderate heat, the soap drop that proves it); water = a
# pale wash. Places: the new STOVE (gas hob, live flames) for every kitchen moment, paper stages for the cut-away pot diagrams.
# CRAFT (ep 18): FOLLOW-THROUGH + DRAG - Chubby's hair lags his head (anim_fx.drag), the foam overshoots and settles (follow), the
# spoon swings with lag; ACTING: new hand poses (grip on the spoon, pinch for the soap drop, point); the jump-back from the hot pot.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "Same") - 0.2, "whip"), ("S1b", T("i2", "Milk") - 0.15, "punch"),
    ("S2", T("i3", "And") - 0.2, "whip"), ("S2b", T("i3", "The", 1) - 0.15, "zoom"),
    ("S3", T("a1", "Okay,") - 0.2, "flash"), ("S4", T("a2", "Nothing") - 0.2, "whip"),
    ("S5", T("b1", "Milk") - 0.2, "whip"), ("S5b", T("b1", "But") - 0.15, "punch"),
    ("S6", T("b2", "There's") - 0.2, "whip"), ("S6b", T("b2", "And") - 0.15, "zoom"),
    ("S7", T("b3", "So") - 0.2, "whip"), ("S7b", T("b3", "It", 1) - 0.15, "punch"),
    ("S8", T("b4", "That") - 0.2, "flash"), ("S8b", T("b4", "Soap") - 0.15, "zoom"),
    ("S9", T("c1", "So") - 0.2, "whip"),
    ("S10", T("c2", "Then") - 0.2, "focus"), ("S10b", T("c2", "so") - 0.15, "zoom"),
    ("S11", T("c3", "They") - 0.2, "whip"), ("S12", T("c4", "And") - 0.2, "whip"), ("S12b", T("c4", "so") - 0.15, "punch"),
    ("S13", T("c5", "Water") - 0.2, "flash"),
    ("S14", T("d1", "Want") - 0.2, "whip"), ("S14b", T("d1", "a", 1) - 0.15, "zoom"), ("S15", T("d2", "Plain") - 0.2, "flash"),
    ("S16", T("e1", "Okay,") - 0.2, "whip"), ("S17", T("e2", "A") - 0.2, "whip"), ("S17b", T("e2", "Butter") - 0.15, "punch"), ("S17c", T("e2", "The", 1) - 0.15, "zoom"),
    ("S18", T("e3", "The") - 0.2, "flash"), ("S18b", T("e3", "About") - 0.15, "zoom"),
    ("S19", T("e4", "In") - 0.2, "whip"), ("S20", T("e5", "Two") - 0.2, "whip"), ("S20b", T("e5", "and") - 0.15, "punch"),
    ("S21", T("e6", "And") - 0.2, "whip"), ("S22", T("f1", "Bonus:") - 0.2, "flash"),
    ("S23", T("g1", "Quick") - 0.2, "whip"), ("S24", T("g2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
SRC_V = "Source: University of Valencia (Mètode) · The Conversation"
SRC_A = "Source: America's Test Kitchen / Cook's Illustrated"
SRC_K = "Source: The Kitchn · The Conversation"


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


def ichip(text, size=26, inv=False): return chip(text, INKC if not inv else MILK, MILK if not inv else INKC, size)


def mchip(text, size=30): return chip(text, INK_MINT_S, MILK, size)


def achip(text, size=30): return chip(text, ACC_S, MILK, size)


def t3(f, text, y, t, t0, size=260, face=ACC_L, side=ACC_S, x=540):
    """3D title in the accent (drawn BEFORE Chubby / the hero)."""
    if t >= t0: title3d(f, text, y, t, t0, size=size, face=face, side=side, depth=22, x=x)


HOB = 1300; POT_Y = HOB - 225 + 8          # pot_el("steel") centre so its bottom sits on the burner grate
TOVER = T("i1", "over,") - 0.1; TWATER = T("i1", "water") - 0.1


def head_x_hook(t):
    """Chubby's head x in the hook (reaches toward the pot, then jumps back on 'over') — for the hair drag."""
    return 300 - jump_back(t, TOVER, 100, 0.28)


def foam_hook(t):
    """foam height in the hook: climbs from frame 0, overshoots over the rim on 'over', settles (follow-through on a liquid)."""
    k = 0.3 + 0.75 * ramp(t, 0.0, TOVER + 0.1)
    return clamp(k + 0.12 * follow(t, TOVER, 1.0, 3, 12, 5))


# ---- S0: HOOK — the stove: the milk pot is already foaming at frame 0; on 'over' it spills; Chubby jumps back (hair lags) ----
def shot_S0(t, n):
    f = set_stove(t, on=1.0)
    fo = foam_hook(t)
    t3(f, "OVER?", 760, t, TOVER, 300, ACC_L, ACC_S)
    comp(f, pot_el("steel", 0.6, fo, clamp((fo - 0.5) * 2) * 0.75), 660, POT_Y)
    side_flames(f, 660, HOB - 2, t, 352, 1.0)
    steam_wisps(f, 660, POT_Y - 240, t, 4, 150, 160, (255, 255, 255), 0.6, 2)
    hx = head_x_hook(t); hair = drag(t, head_x_hook, 3, 0.9)
    lean_, sq = flinch(t, TOVER, 0.8)
    if t < TOVER:
        hands = chub(f, hx, 1500, 1.0, t=t, la=(30, 16), ra=(96, 72), mouth=talk(t), expr="happy", brow="up", look=(0.8, -0.3), lean=6,
                     hold=scale_el(spoon_el(), 0.75), hold_off=(150, -10), hold_front=True, hand_r="grip", hair=(hair, 0))
    else:
        chub(f, hx, 1500, 1.0, t=t, **POSE["shock"], mouth="o", expr="wow", brow="up", look=(0.9, -0.2), squash=sq, hair=(hair, 0))
        sy, sx_, sy_ = drop_land(t, TOVER, 1120, 1300, 0.4)          # the dropped spoon falls to the hob and bounces (follow-through)
        rot_comp(f, scale_xy(scale_el(spoon_el(), 0.75), sx_, sy_), 470 + 40 * clamp((t - TOVER) / 0.4), sy, -20 + 30 * clamp((t - TOVER) / 0.4) + 6 * settle(t, TOVER + 0.4, 1.0, 16, 6), 1.0, 1.0, 0.3)
    if t >= TWATER:
        k = pin(t, TWATER, 0.3)
        comp(f, pot_el("water", 0.55, 0.0, 0.0), 940, POT_Y + 60, scale=0.6 * k)
        g = pot_geom(940, POT_Y + 60, 0.6, "water", 0.55)
        rising_bubbles(f, 940, g["y_bot"] - 10, g["y_surf"] - 30, t, 120, 4, 9, 140, 4, g["y_surf"])
        comp(f, ichip("WATER", 24), 920, g["top"] - 30, scale=k)
    icap(f, "why milk boils", "[OVER]...", t, 0.12, acc=ACC, size=190, dark=True, out=TWATER - 0.05)
    icap(f, "but water", "[NEVER] does?", t, TWATER, acc=MILK, size=150, dark=True) if t >= TWATER else None
    f = cam(f, 1 + 0.03 * clamp(t / 4), 540, 1100)
    return finish(f, n, look="warm")


# ---- S1: 'Same stove. Same pot.' — two identical pots on two burners: WATER (left) just bubbles, MILK (right) is climbing ----
def shot_S1(t, n):
    f = set_stove(t, on=0.0, flame_w=0)
    u = lt(t, "S1"); tw = T("i2", "Water") - 0.1
    for i, (x, kind) in enumerate(((300, "water"), (780, "steel"))):
        flames(f, x, HOB - 2, t, 300, 11, 1.0)
        fo = 0.0 if kind == "water" else clamp(0.15 + 0.5 * ramp(t, st_("S1") + 0.2, en_("S1") - st_("S1")))
        comp(f, pot_el(kind, 0.55, fo, 0.0), x, POT_Y + 10, scale=0.9)
        side_flames(f, x, HOB - 2, t, 320, 1.0)
        g = pot_geom(x, POT_Y + 10, 0.9, kind, 0.55)
        if kind == "water": rising_bubbles(f, x, g["y_bot"] - 12, g["y_surf"] - 30, t, 180, 6, 11, 150, 6, g["y_surf"])
        comp(f, ichip("WATER" if kind == "water" else "MILK", 30), x, g["top"] - 40, scale=pin(t, st_("S1") + 0.15 * i, 0.3))
    if t >= tw: label_at(f, "just bubbles", 300, 700, t, tw, 300, 820, bg=INKC, fg=MILK, size=28)
    icap(f, "same stove,", "[SAME POT]", t, st_("S1") + 0.05, acc=MILK, size=150, dark=True)
    return finish(f, n, look="warm")


# ---- S1b: 'Milk climbs out like it's got somewhere to be' — the milk pot foams over the rim, drips; Chubby double-takes ----
def shot_S1b(t, n):
    f = set_stove(t, on=0.0, flame_w=0); u = lt(t, "S1b")
    tc = T("i2", "climbs") - 0.1
    flames(f, 780, HOB - 2, t, 300, 11, 1.0)
    fo = clamp(0.6 + 0.45 * ramp(t, tc, 1.0) + 0.1 * follow(t, tc + 1.0, 1.0, 3, 12, 5))
    comp(f, pot_el("steel", 0.55, fo, clamp((fo - 0.6) * 2) * 0.5), 780, POT_Y + 10, scale=0.9)
    side_flames(f, 780, HOB - 2, t, 320, 1.0)
    look, lean, expr, brow = double_take(t, tc + 0.3)
    hair = drag(t, lambda q: double_take(q, tc + 0.3)[1] * 2.0, 3, 1.0)
    chub(f, 300, 1500, 1.0, t=t, la=(30, 16), ra=(70, 40), mouth=talk(t), expr=expr, brow=brow, look=look, lean=lean, hair=(hair, 0), hand_r="point")
    if t >= tc + 0.9: comp(f, chip("SOMEWHERE TO BE", ACC, INKC, 30), 780, 640, scale=pin(t, tc + 0.9, 0.25))
    icap(f, "milk", "[CLIMBS] out", t, st_("S1b") + 0.05, acc=ACC, size=180, dark=True)
    return finish(f, n, look="warm")


# ---- S2: 'the trick most of us use' — Chubby lays a wooden spoon across the pot; a little timer: 'a few seconds' ----
def shot_S2(t, n):
    f = set_stove(t, on=1.0); u = lt(t, "S2")
    ts = T("i3", "seconds.") - 0.15
    fo = clamp(0.3 + 0.4 * ramp(t, st_("S2") + 0.5, 2.5))
    comp(f, pot_el("steel", 0.55, fo, 0.25), 540, POT_Y)
    side_flames(f, 540, HOB - 2, t, 352, 1.0)
    k = ramp(t, st_("S2"), 0.6)
    rot_comp(f, scale_el(spoon_el(), 0.8), 540, POT_Y - 232 - 60 * (1 - k), -4 + 2 * settle(t, st_("S2") + 0.6, 1.0, 14, 6), 1.0, 1.0, 0.3)
    chub(f, 230, 1500, 1.0, t=t, la=(30, 16), ra=(96, 40), mouth=talk(t), expr="n", brow="up", look=(1, -0.4), lean=4, hand_r="open")
    if t >= ts:
        comp(f, timer_el(0.08 * ramp(t, ts, 1.0), "A FEW SEC", 90), 860, 700, scale=pin(t, ts, 0.3))
        comp(f, chip("THEN IT GOES OVER ANYWAY", ACC, INKC, 24), 860, 860, scale=pin(t, ts + 0.5, 0.25))
    icap(f, "the trick most of us use?", "[THE SPOON]", t, st_("S2") + 0.05, acc=ACC, size=150, dark=True)
    return finish(f, n, look="warm")


# ---- S2b: OPEN LOOP — 'the one that actually works is coming up': a big covered shape on a podium under a spotlight ----
def shot_S2b(t, n):
    f = ink_set("steelb", None); f *= 0.75
    podium(f, 620, 1250, 640, 110, t)
    cloth(f, 620, 1250, 560, 230, t, 0.0)
    spotlight(f, 620, 1120, 360, 0.55, 200)
    god_rays(f, 620, 250, t, (255, 230, 190), 0.2, 7, 1000, 0.5, 1.57, 3)
    tw = T("i3", "works") - 0.1
    chub(f, 230, 1500, 0.95, t=t, **POSE["think"], mouth=talk(t), expr="sus", brow="sus", look=(1, -0.2))
    comp(f, ichip("COMING UP", 32), 620, 900, scale=pin(t, st_("S2b") + 0.2, 0.25))
    if t >= tw: comp(f, mchip("THE ONE THAT WORKS", 30), 620, 1060, scale=pin(t, tw, 0.25))
    icap(f, "the one that", "[ACTUALLY WORKS]", t, st_("S2b") + 0.05, acc=INK_MINT, size=120, dark=True)
    return finish(f, n, look="night")


# ---- S3: PART 1 WATER — cut-away water pot: steam bubbles rise, reach the top... and POP ----
def shot_S3(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S3")
    tp = T("a1", "pop.") - 0.1; tg = T("a1", "Gone.") - 0.1; tr = T("a1", "rise,") - 0.1
    t3(f, "POP", 640, t, tp, 300, MILK, STEEL_S)
    comp(f, pot_el("water", 0.55, 0.0, 0.0), 540, 1040, scale=1.7)
    g = pot_geom(540, 1040, 1.7, "water", 0.55)
    flames(f, 540, g["bottom"] + 16, t, 520, 15, 1.0)
    rising_bubbles(f, 540, g["y_bot"] - 20, g["y_surf"] - 40, t, 380, 9, 20, 150, 7, g["y_surf"] if t >= tp - 0.2 else None)
    if t >= tr: label_at(f, "STEAM BUBBLES", 200, 1420, t, tr, 380, 1200, bg=INKC, fg=MILK, size=28)
    if t >= tg: comp(f, ichip("GONE", 36), 540, g["y_surf"] - 90, scale=pin(t, tg, 0.25))
    chapter_card(f, t, st_("S3") + 0.05, 1, "WATER FIRST", y=1440, dur=1.6, col=ACC_L)
    icap(f, "steam bubbles reach the top...", "", t, st_("S3") + 0.05, acc=ACC, size=150, out=tp - 0.05)
    return finish(f, n, look="fresh")


# ---- S4: 'Nothing holds them. So the water level never climbs.' — the level line stays; Chubby shrugs ----
def shot_S4(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S4")
    tn = T("a2", "never") - 0.1
    comp(f, pot_el("water", 0.55, 0.0, 0.0), 680, 1040, scale=1.3)
    g = pot_geom(680, 1040, 1.3, "water", 0.55)
    rising_bubbles(f, 680, g["y_bot"] - 20, g["y_surf"] - 40, t, 280, 7, 16, 150, 8, g["y_surf"])
    cv2.line(f, (int(g["xl"] - 60), int(g["y_surf"])), (int(g["xr"] + 60), int(g["y_surf"])), C(INK_MINT_S), 6, cv2.LINE_AA)
    label_at(f, "LEVEL STAYS", 880, 640, t, st_("S4") + 0.3, g["xr"] + 40, g["y_surf"], bg=INK_MINT_S, fg=MILK, size=28)
    chub(f, 230, 1500, 1.0, t=t, **POSE["shrug"], mouth=talk(t), expr="n", brow="up", look=(1, -0.3))
    if t >= tn: comp(f, mchip("NEVER CLIMBS", 32), 680, 1420, scale=pin(t, tn, 0.25))
    icap(f, "nothing holds them, so the level", "[NEVER CLIMBS]", t, st_("S4") + 0.05, acc=INK_MINT_S, size=120)
    return finish(f, n, look="fresh")


# ---- S5: PART 2 MILK — 'milk looks like water... about ninety percent water' — a tall glass fills; 90 % counts up ----
def shot_S5(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S5")
    tn = T("b1", "ninety") - 0.15
    x0, x1, y0, y1 = 400, 680, 640, 1320
    k = ramp(t, tn - 0.2, 1.2)
    cv2.rectangle(f, (x0, int(y1 - (y1 - y0) * 0.9 * k)), (x1, y1), C(MILK), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C(INKC), 7, cv2.LINE_AA)
    cv2.line(f, (x0, int(y1 - (y1 - y0) * 0.9)), (x1, int(y1 - (y1 - y0) * 0.9)), C(INKC), 4, cv2.LINE_AA)
    if t >= tn:
        comp(f, chip(f"{count_up(t, tn, 90, 1.0)}%  WATER", INKC, MILK, 34), 540, 1000, scale=pin(t, tn, 0.25))
    comp(f, ichip("MILK", 30), 540, 600)
    chub(f, 200, 1500, 0.95, t=t, la=(30, 16), ra=(96, 40), mouth=talk(t), expr="n", brow="n", look=(1, -0.4), lean=4, hand_r="point")
    chapter_card(f, t, st_("S5") + 0.05, 2, "NOW MILK", y=1440, dur=1.6, col=ACC_L)
    icap(f, "milk is about", "[90%] water", t, st_("S5") + 0.05, acc=INKC, size=170)
    return finish(f, n, look="fresh")


# ---- S5b: 'that last ten percent changes everything' — the amber 10 % slice at the top lights up; 3D 10% ----
def shot_S5b(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S5b")
    te = T("b1", "everything.") - 0.15
    x0, x1, y0, y1 = 400, 680, 640, 1320
    t3(f, "10%", 1100, t, te, 280, ACC_L, ACC_S, x=860)
    cv2.rectangle(f, (x0, int(y1 - (y1 - y0) * 0.9)), (x1, y1), C(MILK), -1, cv2.LINE_AA)
    k = ramp(t, st_("S5b") + 0.1, 0.5)
    cv2.rectangle(f, (x0, y0), (x1, int(y1 - (y1 - y0) * 0.9)), C(ACC_L), -1, cv2.LINE_AA)
    if k > 0: rays(f, 540, y0 + 30, 420, (255, 210, 120), 0.5 * k, t)
    cv2.rectangle(f, (x0, y0), (x1, y1), C(INKC), 7, cv2.LINE_AA)
    cv2.line(f, (x0, int(y1 - (y1 - y0) * 0.9)), (x1, int(y1 - (y1 - y0) * 0.9)), C(INKC), 4, cv2.LINE_AA)
    comp(f, chip("90% WATER", INKC, MILK, 28), 540, 1000)
    label_at(f, "THE OTHER 10%", 230, 760, t, st_("S5b") + 0.1, 400, 670, bg=ACC_S, fg=MILK, size=28)
    for i, (el, dx) in enumerate(((protein_el("happy"), -60), (fat_el(), 40), (scale_el(sugar_cube_el(), 0.8), 120))):
        comp(f, scale_el(el, 0.55), 540 + dx, 672 + 4 * math.sin(t * 5 + i), scale=pin(t, st_("S5b") + 0.3 + 0.1 * i, 0.3))
    icap(f, "that last ten percent", "[CHANGES EVERYTHING]", t, st_("S5b") + 0.05, acc=ACC, size=110)
    return finish(f, n, look="golden")


# ---- S6: 'protein, a bit of fat, a bit of sugar' — MEET THE CAST card (pre-training) ----
def shot_S6(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440)
    items = [(scale_el(protein_el("happy"), 1.2), "PROTEIN", "LOVES BUBBLES"), (scale_el(fat_el(), 1.3), "FAT", "A BIT"), (scale_el(sugar_cube_el(), 1.2), "SUGAR", "A BIT")]
    ts = [T("b2", "protein") - 0.1, T("b2", "fat,") - 0.1, T("b2", "sugar.") - 0.1]
    cast_card(f, items, t, ts, 1000, 300, "MEET THE CAST", None, MILK, 1.0)
    icap(f, "what's in that 10%", "", t, st_("S6") + 0.05, acc=ACC, size=150)
    return finish(f, n, look="fresh")


# ---- S6b: 'the proteins love sitting on the edge of a bubble' — beads hop onto a big bubble's rim, heart eyes ----
def shot_S6b(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S6b")
    te = T("b2", "edge") - 0.1
    k = ramp(t, te - 0.1, 0.9)
    comp(f, bubble_el(150, k, "happy" if k > 0.8 else "n", (0, 0), 3), 540, 1000)
    for i in range(5):
        q = clamp((t - st_("S6b") - 0.1 * i) / max(0.2, te - st_("S6b")))
        a = -2.2 + i * 1.1; sx, sy = 540 + 420 * math.cos(a), 1000 + 320 * math.sin(a) * 0.8
        ex, ey = 540 + 158 * math.cos(a), 1000 + 158 * math.sin(a)
        if q < 1: comp(f, scale_el(protein_el("love", (-math.cos(a), -math.sin(a))), 0.7), sx + (ex - sx) * eio(q), sy + (ey - sy) * eio(q) - 60 * math.sin(math.pi * q))
    label_at(f, "THE EDGE OF A BUBBLE", 540, 1420, t, te, 540, 1150, bg=ACC_S, fg=MILK, size=28)
    icap(f, "proteins love sitting on", "[THE EDGE]", t, st_("S6b") + 0.05, acc=ACC, size=170)
    return finish(f, n, look="fresh")


# ---- S7: 'a steam bubble rises through milk, and proteins wrap around it like a JACKET' — cut-away milk pot, one hero bubble ----
def shot_S7(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S7")
    tj = T("b3", "jacket.") - 0.15
    t3(f, "JACKET", 640, t, tj, 280, ACC_L, ACC_S)
    comp(f, pot_el("steel", 0.6, 0.0, 0.0), 540, 1040, scale=1.7)
    g = pot_geom(540, 1040, 1.7, "steel", 0.6)
    flames(f, 540, g["bottom"] + 16, t, 520, 15, 1.0)
    k = ramp(t, st_("S7") + 0.1, max(0.6, tj - st_("S7") - 0.1))
    by = g["y_bot"] - 60 - (g["y_bot"] - 60 - (g["y_surf"] + 70)) * k
    jk = ramp(t, tj - 0.3, 0.5)
    comp(f, bubble_el(60, jk, "n", (0, -0.5), 2), 540 + 10 * math.sin(t * 3), by)
    for i in range(4):
        a = i * 1.6; q = clamp((t - st_("S7") - 0.4 - 0.1 * i) / 0.8)
        if q < 1: comp(f, scale_el(protein_el("love"), 0.45), 540 + (120 + 60 * (1 - q)) * math.cos(a) * (1 - q), by + 90 * math.sin(a) * (1 - q), op=1 - q)
    if t >= tj: label_at(f, "PROTEIN JACKET", 230, 760, t, tj, 470, by - 10, bg=ACC_S, fg=MILK, size=28)
    icap(f, "proteins wrap around it like a", "[JACKET]", t, st_("S7") + 0.05, acc=ACC, size=170, out=tj - 0.05)
    return finish(f, n, look="fresh")


# ---- S7b: 'It reaches the top... and it doesn't pop' — the jacketed bubble sits on the surface, smug; a 'no pop' sign ----
def shot_S7b(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S7b")
    td = T("b3", "doesn't") - 0.1
    comp(f, pot_el("steel", 0.6, 0.0, 0.0), 540, 1040, scale=1.7)
    g = pot_geom(540, 1040, 1.7, "steel", 0.6)
    k = ramp(t, st_("S7b"), 0.6)
    by = g["y_surf"] + 70 - 110 * k
    comp(f, bubble_el(60, 1.0, "smirk" if t >= td else "n", (0, 0), 2), 540, by + 2 * math.sin(t * 4))
    for i in range(3):
        comp(f, scale_el(bubble_el(60, 1.0, None, (0, 0), 3 + i), 0.7), 400 + i * 140, g["y_surf"] - 30 + 4 * math.sin(t * 3 + i), op=clamp((t - st_("S7b") - 0.4 - 0.2 * i) / 0.3))
    if t >= td:
        comp(f, check_el(44, False), 700, by - 80, scale=pin(t, td, 0.25))
    icap(f, "it reaches the top...", "", t, st_("S7b") + 0.05, acc=ACC, size=150, out=td - 0.05)
    icap(f, "and it", "[DOESN'T] pop", t, td, acc=ACC, size=160) if t >= td else None
    return finish(f, n, look="fresh")


# ---- S8: 'That trick has a name: SURFACTANT' — define on sight; a label on the jacket; Chubby presents ----
def shot_S8(t, n):
    f = ink_set("amber", (255, 230, 180), 540, 1000, 440); f *= 0.95
    tn = T("b4", "name:") - 0.1; ts = T("b4", "surfactant.") - 0.15
    t3(f, "SURFACTANT", 640, t, ts, 170, MILK, ACC_S)
    comp(f, bubble_el(120, 1.0, "happy", (0, 0), 3), 640, 1040)
    if t >= ts: label_at(f, "= holds a bubble together", 640, 1360, t, ts, 640, 1180, bg=INKC, fg=MILK, size=28)
    chub(f, 230, 1500, 1.0, t=t, **POSE["present"], mouth=talk(t), expr="happy", brow="up", look=(1, -0.3))
    icap(f, "that trick has a name:", "", t, st_("S8") + 0.05, acc=MILK, size=150, dark=True, out=ts - 0.05)
    return finish(f, n, look="golden")


# ---- S8b: 'Soap does it too, and that's why soap makes foam' — soap bottle pumps, a foam cloud of jacketed bubbles ----
def shot_S8b(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440); u = lt(t, "S8b")
    tf = T("b4", "foam.") - 0.15
    comp(f, soap_el(), 300, 1080, scale=1.4 * pin(t, st_("S8b"), 0.3))
    k = ramp(t, st_("S8b") + 0.3, max(0.6, tf - st_("S8b")))
    rng = np.random.default_rng(9)
    for i in range(14):
        q = clamp((k * 14 - i) / 3)
        if q <= 0: continue
        bx = 540 + rng.uniform(-40, 300); by = 1120 - rng.uniform(0, 420) * q
        comp(f, scale_el(bubble_el(40, 0.5, None, (0, 0), 1 + i % 3, MILK), rng.uniform(0.6, 1.3) * (0.6 + 0.4 * q)), bx, by + 4 * math.sin(t * 5 + i))
    if t >= tf: comp(f, chip("SOAP = A SURFACTANT TOO", INK_MINT_S, MILK, 30), 540, 740, scale=pin(t, tf, 0.25))
    icap(f, "soap does it too,", "[THAT'S WHY] it foams", t, st_("S8b") + 0.05, acc=INK_MINT_S, size=110)
    return finish(f, n, look="fresh")


# ---- S9: PART 3 — 'the bubbles pile up... FOAM' — jacketed bubbles stack from the surface up; 3D FOAM ----
def shot_S9(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S9")
    tf = T("c1", "foam.") - 0.15; tp = T("c1", "pile") - 0.1
    t3(f, "FOAM", 640, t, tf, 320, MILK, ACC_S)
    comp(f, pot_el("steel", 0.5, 0.0, 0.0), 540, 1040, scale=1.7)
    g = pot_geom(540, 1040, 1.7, "steel", 0.5)
    rows = 5
    for r_ in range(rows):
        for c in range(6):
            i = r_ * 6 + c; q = clamp((t - tp - 0.07 * i) / 0.3)
            if q <= 0: continue
            bx = g["xl"] + 40 + c * (g["xr"] - g["xl"] - 80) / 5 + (20 if r_ % 2 else 0); by = g["y_surf"] - 10 - r_ * 58
            comp(f, scale_el(bubble_el(40, 0.75, None, (0, 0), 1 + i % 3), 0.85 * (0.7 + 0.3 * pin(t, tp + 0.07 * i, 0.3))), bx, by + 3 * math.sin(t * 4 + i))
    chapter_card(f, t, st_("S9") + 0.05, 3, "FOAM + SKIN", y=1440, dur=1.6, col=ACC_L)
    icap(f, "the bubbles", "[PILE UP]", t, st_("S9") + 0.05, acc=ACC, size=170, out=tf - 0.05)
    return finish(f, n, look="fresh")


# ---- S10: 'Then it gets worse' — lights drop, amber mood; steam leaves the top (evaporation arrows) ----
def shot_S10(t, n):
    f = ink_set("amber", None); f *= 0.78
    mood(f, (255, 150, 60), 0.3)
    te = T("c2", "evaporates") - 0.1
    comp(f, pot_el("steel", 0.5, 0.35, 0.0), 540, 1060, scale=1.6)
    g = pot_geom(540, 1060, 1.6, "steel", 0.5)
    flames(f, 540, g["bottom"] + 16, t, 520, 15, 1.0)
    if t >= te - 0.3:
        steam_wisps(f, 540, g["y_surf"] - 150, t, 7, 260, 300, (255, 255, 255), 0.85, 4)
        for i in range(3): draw_arrow(f, 420 + i * 120, g["y_surf"] - 120, 420 + i * 120, g["y_surf"] - 230, ramp(t, te + 0.1 * i, 0.4), MILK, 7, 24)
        label_at(f, "WATER EVAPORATES", 820, 700, t, te, 700, g["y_surf"] - 200, bg=INKC, fg=MILK, size=26)
    spotlight(f, 540, 1000, 460, 0.35, 220)
    icap(f, "then it gets", "[WORSE]", t, st_("S10") + 0.05, acc=ACC_L, size=200, dark=True)
    return finish(f, n, look="golden")


# ---- S10b: '...so the proteins and fat up there get thicker' — beads and drops crowd at the surface ----
def shot_S10b(t, n):
    f = ink_set("amber", None); f *= 0.82
    tt = T("c2", "thicker.") - 0.15
    comp(f, pot_el("steel", 0.5, 0.35, 0.5 * ramp(t, tt - 0.4, 0.8)), 540, 1060, scale=1.6)
    g = pot_geom(540, 1060, 1.6, "steel", 0.5)
    k = ramp(t, st_("S10b"), max(0.8, tt - st_("S10b")))
    rng = np.random.default_rng(15)
    for i in range(16):
        x0_, y0_ = rng.uniform(g["xl"] + 30, g["xr"] - 30), rng.uniform(g["y_surf"] + 40, g["y_bot"] - 30)
        y1_ = g["y_surf"] - 180 + rng.uniform(-14, 14); x1_ = g["xl"] + 40 + (g["xr"] - g["xl"] - 80) * (i / 15)
        q = eio(clamp((k * 1.3 - i * 0.02)))
        el = scale_el(protein_el("n"), 0.45) if i % 3 else scale_el(fat_el(), 0.5)
        comp(f, el, x0_ + (x1_ - x0_) * q, y0_ + (y1_ - y0_) * q)
    icap(f, "proteins and fat up top get", "[THICKER]", t, st_("S10b") + 0.05, acc=ACC_L, size=150, dark=True)
    return finish(f, n, look="golden")


# ---- S11: 'They set into a SKIN. You've seen it.' — confiding close-up: Chubby points at the wrinkly skin on the pot ----
def shot_S11(t, n):
    f = set_stove(t, on=0.6) * 0.7
    mood(f, (255, 160, 70), 0.25)
    ts = T("c3", "skin.") - 0.12; tw = T("c3", "wrinkly") - 0.1
    k = ramp(t, ts - 0.2, 0.6)
    comp(f, pot_el("steel", 0.6, 0.0, k), 640, POT_Y, scale=1.0)
    side_flames(f, 640, HOB - 2, t, 352, 0.6)
    g = pot_geom(640, POT_Y, 1.0, "steel", 0.6)
    chub(f, 250, 1500, 1.0, t=t, **POSE["whisper"], mouth=talk(t), expr="sus", brow="sus", look=(1, -0.4), hand_r="point")
    spotlight(f, 520, 1050, 420, 0.55, 220)
    if t >= ts: label_at(f, "THE SKIN", 860, 760, t, ts, 760, g["y_surf"] - 10, bg=ACC_S, fg=MILK, size=30)
    if t >= tw: comp(f, chip("you've seen it", ACC_L, INKC, 26), 860, 900, scale=pin(t, tw, 0.25))
    icap(f, "they set into a", "[SKIN]", t, st_("S11") + 0.05, acc=ACC_L, size=200, dark=True)
    return finish(f, n, look="night")


# ---- S12: 'And the skin is a LID. The steam can't get out' — cut-away: skin on top, trapped bubbles bump under it ----
def shot_S12(t, n):
    f = ink_set("amber", None); f *= 0.9
    tl = T("c4", "lid.") - 0.12; tc = T("c4", "can't") - 0.1
    t3(f, "A LID", 640, t, tl, 280, ACC_L, ACC_S)
    comp(f, pot_el("steel", 0.5, 0.45, 1.0), 540, 1060, scale=1.6)
    g = pot_geom(540, 1060, 1.6, "steel", 0.5)
    flames(f, 540, g["bottom"] + 16, t, 520, 15, 1.0)
    ytop = g["y_surf"] - 0.45 * (g["y_surf"] - g["top"] - 16)
    for i in range(5):
        q = ((t * 0.7) + i * 0.2) % 1.0; bx = g["xl"] + 50 + i * (g["xr"] - g["xl"] - 100) / 4
        by = g["y_surf"] - 20 - (g["y_surf"] - 20 - ytop - 30) * q
        comp(f, scale_el(bubble_el(40, 0.75, "sad" if q > 0.85 else None, (0, -1), 1 + i % 3), 0.8), bx, by)
    if t >= tc:
        for i in range(3): comp(f, check_el(34, False), 420 + i * 120, ytop - 60 + 4 * math.sin(t * 6 + i), scale=pin(t, tc + 0.1 * i, 0.25))
        label_at(f, "STEAM CAN'T GET OUT", 540, 1420, t, tc, 540, ytop + 60, bg=INKC, fg=MILK, size=28)
    icap(f, "and the skin is", "[A LID]", t, st_("S12") + 0.05, acc=ACC_L, size=190, dark=True, out=tl - 0.05)
    return finish(f, n, look="golden")


# ---- S12b: '...it lifts the whole foam up... and up... and over the edge' — the foam + skin rise and spill; shake ----
def shot_S12b(t, n):
    f = set_stove(t, on=1.0)
    tu1 = T("c4", "up...") - 0.1; tu2 = T("c4", "up", 1) - 0.1; to = T("c4", "over") - 0.1
    k = 0.45 + 0.2 * ramp(t, tu1, 0.5) + 0.2 * ramp(t, tu2, 0.5) + 0.2 * ramp(t, to, 0.4) + 0.1 * follow(t, to + 0.4, 1.0, 3, 12, 5)
    t3(f, "OVER", 780, t, to, 300, ACC_L, ACC_S)
    comp(f, pot_el("steel", 0.5, clamp(k), 1.0), 540, POT_Y, scale=1.15)
    side_flames(f, 540, HOB - 2, t, 400, 1.0)
    lean_, sq = flinch(t, to, 0.9)
    hair = drag(t, lambda q: flinch(q, to, 0.9)[0] * 1.5, 3, 1.0)
    chub(f, 200, 1500, 0.9, t=t, **(POSE["shock"] if t >= to else POSE["point"]), mouth="o" if t >= to else talk(t), expr="wow" if t >= to else "n", brow="up", look=(1, -0.5), squash=sq, hair=(hair, 0))
    if t >= to: comp(f, burst_el("OVER!", ACC_L, INKC, 58), 880, 760, scale=pin(t, to, 0.2))
    icap(f, "it lifts the whole foam", "[UP]", t, st_("S12b") + 0.05, acc=ACC_L, size=170, dark=True, out=to - 0.05)
    icap(f, "and over", "[THE EDGE]", t, to, acc=ACC_L, size=160, dark=True) if t >= to else None
    return finish(f, n, look="warm")


# ---- S13: 'Water can't do that. No proteins, no jacket, no skin, no lid.' — split: WATER vs MILK checklist ----
def shot_S13(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440)
    tp = T("c5", "proteins,") - 0.1; tj = T("c5", "jacket,") - 0.1; ts = T("c5", "skin,") - 0.1; tl = T("c5", "lid.") - 0.12
    def L(g):
        comp(g, pot_el("water", 0.55, 0.0, 0.0), 330, 980, scale=0.75)
        for i, (w, tt) in enumerate((("PROTEINS", tp), ("JACKET", tj), ("SKIN", ts), ("LID", tl))):
            if t >= tt: comp(g, check_el(30, False), 240, 1230 + i * 52, scale=pin(t, tt, 0.25)); comp(g, chip(f"NO {w}", INKC, MILK, 22), 360, 1230 + i * 52, op=clamp((t - tt) / 0.2))
    def R(g):
        comp(g, pot_el("steel", 0.55, 0.9, 1.0), 750, 980, scale=0.75)
        for i, (w, tt) in enumerate((("PROTEINS", tp), ("JACKET", tj), ("SKIN", ts), ("LID", tl))):
            if t >= tt: comp(g, check_el(30, True), 660, 1230 + i * 52, scale=pin(t, tt, 0.25)); comp(g, chip(w, ACC_S, MILK, 22), 780, 1230 + i * 52, op=clamp((t - tt) / 0.2))
    split_contrast(f, t, st_("S13") + 0.05, L, R, "WATER", "MILK", INK_MINT, ACC, 640, 1470, 0.35, st_("S13") + 0.3)
    icap(f, "water", "[CAN'T] do that", t, st_("S13") + 0.05, acc=INK_MINT_S, size=150)
    return finish(f, n, look="fresh")


# ---- S14: PART 4 PROOF — 'Want proof? A scientist at the University of Valencia suggests this' — Chubby with the soap bottle ----
def shot_S14(t, n):
    f = set_stove(t, on=1.0); u = lt(t, "S14")
    comp(f, pot_el("water", 0.55, 0.0, 0.0), 620, POT_Y)
    side_flames(f, 620, HOB - 2, t, 352, 1.0)
    g = pot_geom(620, POT_Y, 1.0, "water", 0.55)
    rising_bubbles(f, 620, g["y_bot"] - 14, g["y_surf"] - 30, t, 200, 6, 11, 150, 5, g["y_surf"])
    chub(f, 240, 1500, 1.0, t=t, **POSE["hold_up"], mouth=talk(t), expr="smirk", brow="n", look=(1, -0.3), hold=scale_el(soap_el(), 0.75), hold_off=(40, -120), hold_front=True, hand_r="grip")
    comp(f, ichip("WATER", 26), 620, g["top"] - 36)
    chapter_card(f, t, st_("S14") + 0.05, 4, "PROOF", y=1440, dur=1.6, col=ACC_L)
    comp(f, ichip(SRC_V, 22), 540, 1462, op=clamp((u - 1.8) / 0.3))
    icap(f, "want", "[PROOF]?", t, st_("S14") + 0.05, acc=INK_MINT, size=200, dark=True)
    return finish(f, n, look="warm")


# ---- S14b: 'a drop of dish soap in a pot of water. Then boil it.' — pinch hand, ONE drop falls into the water ----
def shot_S14b(t, n):
    f = set_stove(t, on=1.0); u = lt(t, "S14b")
    td = T("d1", "drop") - 0.1; tb = T("d1", "boil") - 0.1
    comp(f, pot_el("water", 0.55, 0.0, 0.0), 620, POT_Y)
    side_flames(f, 620, HOB - 2, t, 352, 1.0 if t >= tb else 0.4)
    g = pot_geom(620, POT_Y, 1.0, "water", 0.55)
    rising_bubbles(f, 620, g["y_bot"] - 14, g["y_surf"] - 30, t, 200, 7 if t >= tb else 3, 11, 150, 5, g["y_surf"])
    chub(f, 260, 1500, 1.0, t=t, la=(30, 16), ra=(120, 40), mouth=talk(t), expr="n", brow="up", look=(1, -0.5), lean=6, hand_r="pinch")
    q = clamp((t - td) / 0.45)
    if 0 < q < 1: comp(f, soap_drop_el(), 560, 700 + (g["y_surf"] - 700) * q * q)
    if q >= 1: cv2.circle(f, (560, int(g["y_surf"])), int(10 + 40 * clamp((t - td - 0.45) / 0.4)), C(INK_MINT), max(1, int(5 * (1 - clamp((t - td - 0.45) / 0.4)))), cv2.LINE_AA)
    if t >= td: slam(f, mchip("1 DROP OF SOAP", 34), 620, 700, -4, t, td)
    if t >= tb: comp(f, achip("BOIL IT", 30), 880, 860, scale=pin(t, tb, 0.25))
    icap(f, "a drop of dish soap", "[IN WATER]", t, st_("S14b") + 0.05, acc=INK_MINT, size=150, dark=True)
    return finish(f, n, look="warm")


# ---- S15: 'Plain water... now boils over. Same trick, different jacket.' — the soapy water foams over; Chubby double take ----
def shot_S15(t, n):
    f = set_stove(t, on=1.0)
    to = T("d2", "over.") - 0.15; tj = T("d2", "different") - 0.1
    t3(f, "BOILS OVER", 760, t, to, 220, MILK, INK_MINT_S)
    k = clamp(0.3 + 0.75 * ramp(t, st_("S15"), max(0.6, to - st_("S15") + 0.2)) + 0.1 * follow(t, to + 0.2, 1.0, 3, 12, 5))
    comp(f, pot_el("water", 0.55, k, 0.0), 620, POT_Y)
    side_flames(f, 620, HOB - 2, t, 352, 1.0)
    look, lean, expr, brow = double_take(t, to - 0.2)
    hair = drag(t, lambda q: double_take(q, to - 0.2)[1] * 2.0, 3, 1.0)
    chub(f, 250, 1500, 1.0, t=t, la=(30, 16), ra=(96, 60), mouth=talk(t), expr=expr, brow=brow, look=look, lean=lean, hair=(hair, 0), hand_r="point")
    if t >= tj: comp(f, chip("SAME TRICK, DIFFERENT JACKET", INK_MINT_S, MILK, 26), 540, 1420, scale=pin(t, tj, 0.25))
    comp(f, ichip("SOAPY WATER", 26), 620, 760, scale=pin(t, st_("S15"), 0.3))
    icap(f, "plain water...", "", t, st_("S15") + 0.05, acc=MILK, size=150, dark=True, out=to - 0.05)
    return finish(f, n, look="warm")


# ---- S16: PART 5 THE FIXES — 'America's Test Kitchen tried the classics' — a TESTED clipboard; Chubby presents ----
def shot_S16(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440); u = lt(t, "S16")
    tc = T("e1", "America's") - 0.1
    t3(f, "THE FIXES", 640, t, st_("S16") + 0.1, 220, MILK, INK_MINT_S)
    cv2.rectangle(f, (380, 820), (900, 1340), C(INKC), -1, cv2.LINE_AA); cv2.rectangle(f, (392, 832), (888, 1328), C(MILK), -1, cv2.LINE_AA)
    cv2.rectangle(f, (560, 800), (720, 850), C(STEEL_S), -1, cv2.LINE_AA)
    comp(f, chip("TESTED", INKC, MILK, 30), 640, 900)
    for i, (el, lab, tt) in enumerate(((scale_el(spoon_el(), 0.45), "spoon in the pot", tc), (scale_el(butter_el(), 0.7), "butter on the rim", tc + 0.2), (scale_el(pot_el("wide", 0.5, 0.0, 0.0), 0.3), "a big wide pot", tc + 0.4))):
        if t < tt: continue
        comp(f, el, 520, 990 + i * 120, scale=pin(t, tt, 0.3)); comp(f, chip(lab, INKC, MILK, 22), 760, 990 + i * 120, op=clamp((t - tt) / 0.2))
    chub(f, 200, 1500, 0.95, t=t, **POSE["present"], mouth=talk(t), expr="happy", brow="up", look=(1, -0.3))
    chapter_card(f, t, st_("S16") + 0.05, 5, "THE FIXES", y=1440, dur=1.6, col=INK_MINT)
    comp(f, ichip(SRC_A, 22), 540, 1462, op=clamp((u - 1.8) / 0.3))
    icap(f, "okay, the fixes:", "", t, st_("S16") + 0.05, acc=INK_MINT_S, size=170)
    return finish(f, n, look="fresh")


# ---- S17: 'A spoon left in the pot?' — the spoon trick with a timer: DELAYED ----
def shot_S17(t, n):
    f = set_stove(t, on=1.0); u = lt(t, "S17")
    comp(f, pot_el("steel", 0.55, 0.35 + 0.1 * math.sin(t * 2), 0.5), 540, POT_Y)
    side_flames(f, 540, HOB - 2, t, 352, 1.0)
    rot_comp(f, scale_el(spoon_el(), 0.8), 540, POT_Y - 232, -4, 1.0, 1.0, 0.3)
    comp(f, timer_el(0.15 * ramp(t, st_("S17"), 1.5), "DELAYED", 90), 880, 700, scale=pin(t, st_("S17") + 0.2, 0.3))
    chub(f, 200, 1500, 0.9, t=t, la=(30, 16), ra=(96, 40), mouth=talk(t), expr="sus", brow="sus", look=(1, -0.4), lean=4, hand_r="point")
    icap(f, "a spoon left in the pot?", "[ONLY DELAYS IT]", t, st_("S17") + 0.05, acc=ACC, size=120, dark=True)
    return finish(f, n, look="warm")


# ---- S17b: 'Butter on the rim?' — butter smeared on the rim: DELAYED too ----
def shot_S17b(t, n):
    f = set_stove(t, on=1.0); u = lt(t, "S17b")
    comp(f, pot_el("steel", 0.55, 0.45 + 0.1 * math.sin(t * 2), 0.5), 540, POT_Y)
    side_flames(f, 540, HOB - 2, t, 352, 1.0)
    cv2.rectangle(f, (364, POT_Y - 236), (716, POT_Y - 222), C(ACC_L), -1, cv2.LINE_AA)
    comp(f, butter_el(), 880, 1000 + 4 * math.sin(t * 3), scale=pin(t, st_("S17b"), 0.3))
    comp(f, timer_el(0.15 * ramp(t, st_("S17b"), 1.5), "DELAYED", 90), 880, 700, scale=pin(t, st_("S17b") + 0.2, 0.3))
    chub(f, 200, 1500, 0.9, t=t, la=(30, 16), ra=(96, 40), mouth=talk(t), expr="sus", brow="sus", look=(1, -0.4), lean=4, hand_r="point")
    icap(f, "butter on the rim?", "[ONLY DELAYS IT]", t, st_("S17b") + 0.05, acc=ACC, size=120, dark=True)
    return finish(f, n, look="warm")


# ---- S17c: 'The milk still came over.' — both tricks in place, the pot goes over anyway; buzzer ----
def shot_S17c(t, n):
    f = set_stove(t, on=1.0)
    ts = T("e2", "still") - 0.1
    k = clamp(0.5 + 0.55 * ramp(t, ts - 0.2, 0.7) + 0.1 * follow(t, ts + 0.5, 1.0, 3, 12, 5))
    comp(f, pot_el("steel", 0.55, k, 0.75), 540, POT_Y)
    side_flames(f, 540, HOB - 2, t, 352, 1.0)
    rot_comp(f, scale_el(spoon_el(), 0.8), 540, POT_Y - 232 - 30 * ramp(t, ts, 0.5), -4 - 12 * ramp(t, ts, 0.5), 1.0, 1.0, 0.3)
    lean_, sq = flinch(t, ts, 0.6)
    chub(f, 200, 1500, 0.9, t=t, **POSE["cheek"], mouth="o" if t >= ts else talk(t), expr="sad", brow="sad", look=(1, -0.4), squash=sq)
    if t >= ts: comp(f, burst_el("STILL!", ACC_L, INKC, 54), 880, 760, scale=pin(t, ts, 0.2))
    icap(f, "the milk", "[STILL] came over", t, st_("S17c") + 0.05, acc=ACC, size=140, dark=True)
    return finish(f, n, look="warm")


# ---- S18: 'The one that worked every time: a big, WIDE pot' — the cloth lifts: a wide pot; mint rays; Chubby tada ----
def shot_S18(t, n):
    f = ink_set("mintd", None); f *= 0.9
    tw = T("e3", "wide") - 0.12
    t3(f, "WIDE POT", 640, t, tw, 240, MILK, INK_MINT_S)
    podium(f, 620, 1250, 640, 110, t)
    k = ramp(t, tw - 0.1, 0.5)
    comp(f, pot_el("wide", 0.5, 0.0, 0.0), 620, 1130, scale=0.85 * (0.9 + 0.1 * k))
    cloth(f, 620, 1250, 560, 230, t, k)
    if t >= tw: rays(f, 620, 1100, 700, (170, 240, 210), 0.5 * ramp(t, tw, 0.3), t); comp(f, check_el(60, True), 900, 900, scale=pin(t, tw, 0.25))
    chub(f, 220, 1500, 0.95, t=t, **(POSE["tada"] if t >= tw else POSE["present"]), mouth=talk(t), expr="happy", brow="up", look=(1, -0.3))
    icap(f, "the one that worked every time:", "", t, st_("S18") + 0.05, acc=MILK, size=150, dark=True, out=tw - 0.05)
    return finish(f, n, look="fresh")


# ---- S18b: 'About four litres of pot for half a litre of milk' — scale: the wide pot nearly empty; chips 4 L / 0.5 L ----
def shot_S18b(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 1000, 440); u = lt(t, "S18b")
    tf = T("e3", "four") - 0.1; th = T("e3", "half") - 0.1
    comp(f, pot_el("wide", 0.15, 0.0, 0.0), 540, 1050, scale=1.1)
    g = pot_geom(540, 1050, 1.1, "wide", 0.15)
    if t >= tf: slam(f, mchip("4 LITRE POT", 40), 540, 700, -3, t, tf)
    if t >= th: label_at(f, "0.5 L OF MILK", 540, 1360, t, th, 540, g["y_surf"], bg=ACC_S, fg=MILK, size=30)
    comp(f, ichip("way bigger than feels right", 24), 540, 820, op=clamp((u - 0.2) / 0.3))
    comp(f, ichip(SRC_A, 22), 540, 1462, op=clamp((u - 1.0) / 0.3))
    icap(f, "about", "[4 L] pot : [0.5 L] milk", t, st_("S18b") + 0.05, acc=INK_MINT_S, size=110)
    return finish(f, n, look="fresh")


# ---- S19: 'In a wide pot the bubbles have room to grow big. And big bubbles pop, jacket or no jacket.' ----
def shot_S19(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S19")
    tb = T("e4", "big.") - 0.1; tp = T("e4", "pop,") - 0.1
    comp(f, pot_el("wide", 0.5, 0.0, 0.0), 540, 1060, scale=1.3)
    g = pot_geom(540, 1060, 1.3, "wide", 0.5)
    flames(f, 540, g["bottom"] + 16, t, 800, 21, 1.0)
    for i in range(5):
        ph = ((t - st_("S19")) * 0.55 + i * 0.2) % 1.0
        bx = g["xl"] + 70 + i * (g["xr"] - g["xl"] - 140) / 4; by = g["y_bot"] - 30 - (g["y_bot"] - 30 - g["y_surf"]) * clamp(ph / 0.7)
        r_ = 18 + 50 * clamp(ph / 0.7)
        if ph < 0.7: comp(f, scale_el(bubble_el(60, 1.0 if t >= tb - 0.5 else 0.0, None, (0, 0), 1 + i % 3), r_ / 60), bx, by)
        elif t >= tp - 0.1: pop_star(f, bx, g["y_surf"] - 10, t, t - (ph - 0.7) / 0.3 * 0.3, r_ * 1.2, INKC, 0.3)
        else: comp(f, scale_el(bubble_el(60, 1.0, None, (0, 0), 1 + i % 3), r_ / 60), bx, g["y_surf"] - 10)
    if t >= tb: label_at(f, "ROOM TO GROW BIG", 540, 740, t, tb, 540, g["y_surf"] - 60, bg=INK_MINT_S, fg=MILK, size=28)
    if t >= tp: comp(f, mchip("BIG BUBBLES POP", 34), 540, 1400, scale=pin(t, tp, 0.25))
    icap(f, "in a wide pot, bubbles grow", "[BIG]... and pop", t, st_("S19") + 0.05, acc=INK_MINT_S, size=120)
    return finish(f, n, look="fresh")


# ---- S20: 'Two easy extras: moderate heat' — Chubby turns the knob; the flames drop ----
def shot_S20(t, n):
    tm = T("e5", "moderate") - 0.1
    on = 1.0 - 0.55 * ramp(t, tm, 0.6)
    f = set_stove(t, on=on)
    comp(f, pot_el("steel", 0.55, 0.3, 0.25), 540, POT_Y)
    side_flames(f, 540, HOB - 2, t, 352, on)
    sh = (230 + 118 * 0.95, 1500 - 261 * 0.95)
    a1, a2 = arm_ik(sh, (300, HOB + 200), 76 * 0.95, 70 * 0.95)
    chub(f, 230, 1500, 0.95, t=t, la=(30, 16), ra=(a1, a2), mouth=talk(t), expr="n", brow="up", look=(0.3, 0.6), lean=4, hand_r="grip")
    if t >= tm: slam(f, mchip("FLAME DOWN", 36), 540, 700, -4, t, tm)
    icap(f, "two easy extras:", "[MODERATE] heat", t, st_("S20") + 0.05, acc=INK_MINT, size=130, dark=True)
    return finish(f, n, look="warm")


# ---- S20b: 'and a stir every few minutes to break the skin and let the steam out' — Chubby stirs (arm IK on the spoon), skin breaks ----
def shot_S20b(t, n):
    f = set_stove(t, on=0.45); u = lt(t, "S20b")
    ts = T("e5", "stir") - 0.1; tk = T("e5", "skin") - 0.1
    k = ramp(t, tk - 0.2, 0.8)
    comp(f, pot_el("steel", 0.55, 0.2, 1.0 - k), 560, POT_Y)
    side_flames(f, 560, HOB - 2, t, 352, 0.45)
    g = pot_geom(560, POT_Y, 1.0, "steel", 0.55)
    if t >= tk: steam_wisps(f, 560, g["y_surf"] - 80, t, 6, 260, 220, (255, 255, 255), 0.85, 7)
    sw = 40 * math.sin(u * 5) if t >= ts else 0
    gx, gy = 560 + sw, g["y_rim"] - 120 + 10 * math.cos(u * 5)
    x, y, s = 240, 1500, 0.95
    sh = (x + 118 * s, y - 261 * s)
    a1, a2 = arm_ik(sh, (gx, gy), 76 * s, 70 * s)
    chub(f, x, y, s, t=t, la=(30, 16), ra=(a1, a2), mouth=talk(t), expr="happy", brow="up", look=(1, -0.3), lean=5, hand_r="grip")
    spoon_at(f, gx, gy, -62 - sw * 0.4, 0.8)
    grip_hand(f, gx, gy, s * 0.9, 0.0, "grip", 0)
    if t >= ts: slam(f, mchip("STIR EVERY FEW MINUTES", 32), 540, 700, -4, t, ts)
    if t >= tk: label_at(f, "SKIN BROKEN, STEAM OUT", 880, 900, t, tk, 700, g["y_surf"] - 60, bg=INK_MINT_S, fg=MILK, size=26)
    comp(f, ichip(SRC_K, 22), 540, 1462, op=clamp((u - 1.4) / 0.3))
    icap(f, "and a", "[STIR]", t, st_("S20b") + 0.05, acc=INK_MINT, size=190, dark=True)
    return finish(f, n, look="warm")


# ---- S21: JOKE — 'don't walk away. Milk waits for the exact moment you check your phone.' ----
def shot_S21(t, n):
    f = set_stove(t, on=1.0); u = lt(t, "S21")
    tp = T("e6", "phone.") - 0.3; tm = T("e6", "exact") - 0.1
    k = clamp(0.3 + 0.7 * ramp(t, tm, 1.0) + 0.1 * follow(t, tm + 1.0, 1.0, 3, 12, 5))
    comp(f, pot_el("steel", 0.55, k, 0.75), 700, POT_Y)
    side_flames(f, 700, HOB - 2, t, 352, 1.0)
    look, lean, expr, brow = double_take(t, tp + 0.15)
    if t < tp + 0.15: look, lean, expr, brow = (0.2, 0.7), 2.0, "happy", "n"
    hair = drag(t, lambda q: double_take(q, tp + 0.15)[1] * 2.0 if q >= tp + 0.15 else 2.0, 3, 1.0)
    chub(f, 260, 1500, 1.0, t=t, la=(60, 40), ra=(110, -100), mouth=talk(t), expr=expr, brow=brow, look=look, lean=lean, hair=(hair, 0),
         hold=scale_el(phone_el(), 0.55), hold_off=(-10, -30), hold_front=True, hand_r="grip")
    if t >= tm: comp(f, chip("THE EXACT MOMENT", ACC, INKC, 28), 700, 700, scale=pin(t, tm, 0.25))
    icap(f, "and don't", "[WALK AWAY]", t, st_("S21") + 0.05, acc=ACC, size=160, dark=True)
    return finish(f, n, look="warm")


# ---- S22: BONUS — 'pasta water boils over too. Different jacket... starch.' ----
def shot_S22(t, n):
    f = ink_set("cream2", (255, 255, 255), 540, 1000, 440); u = lt(t, "S22")
    ts = T("f1", "starch.") - 0.15; tj = T("f1", "Different") - 0.1
    t3(f, "STARCH", 800, t, ts, 260, ACC_L, ACC_S)
    k = clamp(0.4 + 0.6 * ramp(t, st_("S22") + 0.2, 1.4) + 0.1 * follow(t, st_("S22") + 1.6, 1.0, 3, 12, 5))
    comp(f, pot_el("pasta", 0.55, k, 0.0), 540, 1060, scale=1.4)
    g = pot_geom(540, 1060, 1.4, "pasta", 0.55)
    flames(f, 540, g["bottom"] + 16, t, 560, 15, 1.0)
    comp(f, ichip("PASTA WATER", 30), 540, g["top"] - 50, scale=pin(t, st_("S22"), 0.3))
    if t >= tj: comp(f, achip("DIFFERENT JACKET, SAME STORY", 26), 540, 1400, scale=pin(t, tj, 0.25))
    icap(f, "bonus: pasta water", "[BOILS OVER] too", t, st_("S22") + 0.05, acc=ACC, size=120)
    return finish(f, n, look="fresh")


# ---- S23: RECAP — proteins hold the bubbles -> skin traps the steam -> foam climbs; then the 3 fixes ----
def shot_S23(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 1000, 440)
    items = [(scale_el(bubble_el(60, 1.0, "happy"), 1.0), "JACKETS"), (scale_el(pot_el("steel", 0.5, 0.3, 1.0), 0.42), "SKIN = LID"),
             (scale_el(pot_el("steel", 0.5, 1.0, 0.75), 0.42), "FOAM CLIMBS")]
    ts = [T("g1", "proteins") - 0.15, T("g1", "skin") - 0.15, T("g1", "foam") - 0.15]
    recap_steps(f, items, 940, t, ts, 300, 1.0)
    for i, (w, tt) in enumerate((("WIDE POT", T("g1", "Wide") - 0.1), ("LOWER HEAT", T("g1", "lower") - 0.1), ("STIR", T("g1", "stir.") - 0.1))):
        if t >= tt: comp(f, mchip(w, 32), 240 + i * 300, 1300, scale=pin(t, tt, 0.25))
    icap(f, "", "[REMEMBER]", t, st_("S23") + 0.05, acc=ACC, size=200)
    return finish(f, n, look="fresh")


# ---- S24: send it + FreshNestHub sting ----
def shot_S24(t, n):
    f = set_stove(t, on=0.5) * 0.9
    vend = LINES["g2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("g2", "Send") + 0.3
        comp(f, scale_el(phone2_el("my chai boiled over AGAIN", "wide pot. trust me.", pr), 0.82), 680, 950, scale=pin(t, st_("S24")))
        if pr and t < T("g2", "Send") + 0.75:
            rr = (t - T("g2", "Send") - 0.3) / 0.45
            cv2.circle(f, (680, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 250, 1500, 0.9, t=t, **POSE["point"], mouth=talk(t), expr="happy", brow="up", look=(1, 0), hand_r="point")
        ui_word(f, "send to the friend who lost", "[A POT OF CHAI]", 420, t, T("g2", "friend") - 0.1, col=WHITE, acc=ACC_L, size=110, shadow=0.6, lead_col=WHITE)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=WHITE, lead_size=42, shadow=0.6), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 420, 1520, 0.75, t=t, **POSE["cheer"], mouth=3, expr="happy", brow="up")
        comp(f, pot_el("wide", 0.5, 0.0, 0.0), 760, 1380, scale=0.45 * k)
    return finish(f, n, look="warm")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TOVER, 0.4, 18), (T("i2", "climbs") - 0.1, 0.3, 12), (T("i3", "seconds.") - 0.15, 0.25, 8),
           (T("a1", "pop.") - 0.1, 0.3, 12), (T("b1", "everything.") - 0.15, 0.3, 12), (T("b2", "edge") - 0.1, 0.25, 8),
           (T("b3", "jacket.") - 0.15, 0.35, 14), (T("b3", "doesn't") - 0.1, 0.3, 10), (T("b4", "surfactant.") - 0.15, 0.3, 12),
           (T("c1", "foam.") - 0.15, 0.35, 14), (T("c2", "worse.") - 0.1, 0.3, 12), (T("c2", "thicker.") - 0.15, 0.3, 12),
           (T("c3", "skin.") - 0.12, 0.3, 10), (T("c4", "lid.") - 0.12, 0.35, 14), (T("c4", "over") - 0.1, 0.45, 20),
           (T("c5", "lid.") - 0.12, 0.3, 10), (T("d1", "drop") - 0.1, 0.25, 8), (T("d2", "over.") - 0.15, 0.4, 18),
           (st_("S16") + 0.1, 0.3, 12), (T("e2", "still") - 0.1, 0.4, 16), (T("e3", "wide") - 0.12, 0.4, 16), (T("e3", "four") - 0.1, 0.3, 12),
           (T("e4", "pop,") - 0.1, 0.3, 12), (T("e5", "moderate") - 0.1, 0.25, 8), (T("e5", "stir") - 0.1, 0.3, 10),
           (T("e6", "exact") - 0.1, 0.3, 12), (T("f1", "starch.") - 0.15, 0.35, 14), (T("g2", "Send") + 0.3, 0.2, 8)]


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
