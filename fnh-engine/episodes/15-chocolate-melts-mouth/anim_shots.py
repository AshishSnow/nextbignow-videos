# ================= shots: FreshNestHub 15 — "Why chocolate melts in your mouth" (cocoa butter crystal shape 5 + bloom) =================
# COLOUR SCRIPT (ep 15): warm walnut + lamp gold = the CHOCOLATIER workroom (story moments, marble slab); deep CRYSTAL indigo with
# cocoa-butter yellow bricks = the invisible world of fat crystals; GOLD backlight = shape 5 the winner; COCOA brown = melted
# chocolate; CHALK grey + cold FRIDGE blue = bloom (the 'scary' white dust); back to warm kitchen gold for the takeaways.
# CRAFT (ep 15): MATERIALS on one light model (anim_cine.mat_shade): tempered chocolate is GLOSS (small sharp highlight + crisp
# window reflection + deep darks), untempered is MATTE (no reflection, low contrast), bloomed is CHALKY (lifted, desaturated, powdery
# speckle) -> the viewer SEES the science (shape 5 = shine). Crystal forms as the SAME 12 bricks built 6 ways (morphing layouts).
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "right") - 0.15, "punch"),
    ("S1", T("i2", "On") - 0.15, "whip"), ("S2", T("i3", "And") - 0.15, "focus"),
    ("S3", T("a1", "Here's") - 0.2, "flash"), ("S4", T("a2", "It") - 0.2, "iris"), ("S4b", T("a2", "And") - 0.15, "whip"),
    ("S5", T("a3", "When") - 0.2, "zoom"), ("S6", T("a4", "Same") - 0.2, "whip"), ("S6b", T("a4", "Like") - 0.15, "focus"),
    ("S7", T("b1", "Shapes") - 0.2, "flash"), ("S7b", T("b1", "They") - 0.15, "whip"),
    ("S8", T("b2", "But") - 0.2, "punch"), ("S9", T("b3", "It's") - 0.2, "whip"), ("S9b", T("b3", "And") - 0.15, "whip"),
    ("S10", T("b4", "Inside") - 0.2, "focus"), ("S11", T("b5", "So") - 0.2, "whip"), ("S11b", T("b5", "and") - 0.15, "punch"),
    ("S12", T("c1", "But") - 0.2, "flash"), ("S13", T("c2", "Melt") - 0.2, "iris"), ("S13b", T("c2", "and", 1) - 0.15, "zoom"),
    ("S14", T("c3", "So") - 0.2, "whip"), ("S15", T("c4", "First,") - 0.2, "focus"),
    ("S16", T("c5", "That") - 0.2, "whip"), ("S16b", T("c5", "But") - 0.15, "punch"),
    ("S17", T("c6", "Those") - 0.2, "iris"), ("S17b", T("c6", "As") - 0.15, "zoom"),
    ("S18", T("d1", "Now,") - 0.2, "flash"), ("S19", T("d2", "It's") - 0.2, "punch"),
    ("S20", T("d3", "When") - 0.2, "whip"), ("S20b", T("d3", "and") - 0.15, "focus"),
    ("S21", T("d4", "Over") - 0.2, "whip"), ("S21b", T("d4", "That") - 0.15, "zoom"),
    ("S22", T("d5", "And") - 0.2, "whip"), ("S22b", T("d5", "It") - 0.15, "iris"),
    ("S23", T("d6", "Either") - 0.2, "flash"), ("S23b", T("d6", "It") - 0.15, "punch"),
    ("S24", T("e1", "So") - 0.2, "whip"), ("S25", T("e2", "And") - 0.2, "whip"), ("S25b", T("e2", "Nobody") - 0.15, "punch"),
    ("S26", T("f1", "Remember:") - 0.2, "focus"), ("S27", T("f2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {"S4": (540, 1000), "S13": (540, 1060), "S17": (540, 1000), "S22b": (540, 1250)}


def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def wui(f, lead, big, t, t0, acc=YEL_, size=170, y=470, out=None, tail=""):   # white caption on dark/colour sets
    ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.6, lead_col=WHITE, out=out, tail=tail)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / d))


def munch(t, rate=0.42):
    ph = (t / rate) % 1.0
    return (2 if ph < 0.5 else 0)


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


GOLD5 = (255, 196, 40); CHOCW = (255, 226, 190)
CTR = 1330


def hand_to_mouth(f, x, y, s, t, held, expr="happy", brow="up", mouth="o", look=(0.5, -0.2), la=(20, 10)):
    return chub(f, x, y, s, la=la, ra=(148, -128), mouth=mouth, expr=expr, brow=brow, look=look, hold=held, hold_off=(-30, -40), hold_front=True)


def crumbs(f, x, y, t, t0, n=9, seed=4):
    q = t - t0
    if q < 0 or q > 0.9: return
    rng = np.random.default_rng(seed)
    for i in range(n):
        vx, vy = rng.uniform(-420, 420), rng.uniform(-520, -160)
        px, py = x + vx * q, y + vy * q + 1400 * q * q
        cv2.rectangle(f, (int(px - 7), int(py - 7)), (int(px + 7), int(py + 7)), C((92, 50, 30)), -1, cv2.LINE_AA)


# ---- S0: HOOK — chocolatier workroom; Chubby SNAPS a shiny bar, pops a piece in his mouth, it melts: bliss, 'MELT' in 3D ----
TSNAP = 0.85; TMELT = T("i1", "melt...") - 0.05


def shot_S0(t, n):
    f = set_chocolatier(t)
    if t >= TMELT:
        glow(f, 420, 900, 380, (255, 200, 120), 0.4 * ramp(t, TMELT, 0.4))
        title3d(f, "MELT", 640, t, TMELT, size=330, face=(250, 196, 140), side=(90, 44, 24), depth=28)
    if t < TSNAP:
        chub(f, 400, 1520, 1.12, la=(20, 10), ra=(118, 120), mouth=talk(t), expr="happy", brow="up", look=(1, -0.3),
             hold=scale_el(choc_bar_el("gloss"), 0.55), hold_off=(70, -40), hold_front=True, bob=2 * math.sin(t * 5))
    elif t < 1.45:
        chub(f, 400, 1520, 1.12, la=(20, 10), ra=(118, 120), mouth="o", expr="wow", brow="up", look=(1, -0.3),
             hold=scale_el(choc_bar_el("gloss", snap=1), 0.55), hold_off=(40, -40), hold_front=True)
        k = clamp((t - TSNAP) / 0.6)
        rot_comp(f, scale_el(choc_bar_el("gloss", cols=1), 0.55), 760 + 60 * k, 930 - 120 * math.sin(math.pi * k), 40 * k, 1.0, 1.0, 0.25)
        crumbs(f, 700, 960, t, TSNAP)
        comp(f, burst_el("SNAP!", YEL_, INK, 56), 820, 760, scale=pin(t, TSNAP, 0.2) * (1 - clamp((t - 1.3) / 0.15)))
    else:
        bliss = t >= TMELT
        hand_to_mouth(f, 400, 1520, 1.12, t, scale_el(choc_piece_el("gloss"), 0.4), expr="happy" if bliss else "n",
                      brow="up", mouth=1 if bliss else "o", look=(0, -0.6) if bliss else (0.5, -0.2))
        if bliss: sparkles(f, 400, 900, t, TMELT, 12, 260, (255, 230, 170))
    marble_front(f, CTR)
    if t >= 1.45: comp(f, scale_el(choc_bar_el("gloss", snap=1), 0.5), 790, CTR - 20)
    f = cam(f, 1 + 0.015 * t, 540, 1100)
    f = np.ascontiguousarray(f, np.float32)
    wui(f, "do you know chocolate is made to", "[MELT]...", t, 0.1, acc=(255, 210, 150), size=200, out=TMELT - 0.05)
    return finish(f, n)


# ---- S0b: ...right at the temperature of YOUR MOUTH (huge face close-up, a thermometer rises to 37) ----
def shot_S0b(t, n):
    f = dof(set_room(t), 8) * 0.8; tt = T("i1", "temperature") - 0.1
    lamp_glow(f, 700, 900, 420, (255, 190, 120), 0.3)
    chub_head_only(f, 700, 1050, 2.0, t, mouth="o" if (t * 2.2) % 1 < 0.6 else 2, expr="happy", brow="up", look=(-0.6, -0.2))
    v = 20 + 17 * ramp(t, tt, 0.9)
    temp_gauge(f, 150, 1420, 640, v, marks=[(37, "37° MOUTH", (220, 60, 60))] if t >= tt + 0.8 else [])
    wui(f, "right at the temperature of your", "[MOUTH]?", t, T("i1", "temperature") - 0.3, acc=(255, 150, 140), size=200)
    return finish(f, n)


# ---- S1: ON THE SHELF it snaps / ON YOUR TONGUE it melts (split panels) ----
def shot_S1(t, n):
    f = dof(set_chocolatier(t), 6) * 0.7; ts = T("i2", "snaps.") - 0.1; tm = T("i2", "melts") - 0.1; tr = T("i2", "On", 1) - 0.1

    def L(g):
        if t < ts:
            comp(g, scale_el(choc_bar_el("gloss"), 0.62), 330, 1060, scale=pin(t, st_("S1"), 0.3))
        else:
            k = clamp((t - ts) / 0.4)
            rot_comp(g, scale_el(choc_bar_el("gloss", cols=2), 0.62), 260 - 20 * k, 1060 + 10 * k, -14 * k, 1.0, 1.0, 0.25)
            rot_comp(g, scale_el(choc_bar_el("gloss", cols=2), 0.62), 400 + 20 * k, 1060 + 10 * k, 14 * k, 1.0, 1.0, 0.25)
            crumbs(g, 330, 1060, t, ts, 7, 2)
            comp(g, burst_el("SNAP!", YEL_, INK, 48), 330, 860, scale=pin(t, ts, 0.2))

    def R(g):
        comp(g, scale_el(tongue_el(), 0.5), 750, 1150)
        melting_piece(g, 750, 1150, 0.7, ramp(t, tm, 1.0), "gloss", t)
        if t >= tm + 0.3: comp(g, chip("MELTS", (150, 80, 40), WHITE, 34), 750, 1380, scale=pin(t, tm + 0.3, 0.2))
    split_contrast(f, t, st_("S1") + 0.02, L, R, "ON THE SHELF", "ON YOUR TONGUE", (90, 120, 170), (220, 110, 120), y0=640, y1=1480, t_r=tr)
    return finish(f, n)


# ---- S2: lights drop — an OLD bar covered in white dust under a spotlight; Chubby recoils; 'MOULD?' (open loop) ----
def shot_S2(t, n):
    tw = T("i3", "white") - 0.1; tq = T("i3", "It's") - 0.1
    f = set_kitchen(t) * 0.36
    mood(f, (150, 200, 140), 0.25 * ramp(t, tq, 0.4))
    if t >= tq: title3d(f, "MOULD?", 720, t, tq, size=270, face=(190, 214, 170), side=(50, 70, 50), depth=24)
    chub(f, 260, 1500, 1.0, la=(150, 150), ra=(150, 160), mouth="o" if t >= tw else 0, expr="sus" if t >= tw else "n", brow="sus", look=(1, 0.3), lean=-8)
    counter_front(f, CTR)
    bel = scale_el(choc_bar_el("chalky", bite=True), 0.7)
    rot_comp(f, bel, 720, CTR - 60, -4, pin(t, tw, 0.3) if t >= tw else 0.0, 1.0, 0.3)
    spotlight(f, 700, 1180, 360, 0.55, 220)
    if t >= tq + 0.6: comp(f, chip("COMING UP", INK, YEL_, 30), 540, 1440, op=clamp((t - tq - 0.6) / 0.3))
    if t < tq: wui(f, "that white dust on", "[OLD] chocolate?", t, st_("S2") + 0.1, acc=(220, 230, 210), size=170)
    return finish(f, n, look="night")


# ---- S3: PART 1 — the secret: zoom INTO the bar: cocoa bits, sugar, and yellow fat = COCOA BUTTER ----
def _s3_far(t):
    f = stage("cocoa", (255, 200, 140), 540, 1000, 420)
    comp(f, scale_el(choc_bar_el("gloss"), 1.1), 540, 1020)
    return f


def _s3_near(t):
    f = stage("cocoa"); rng = np.random.default_rng(31)
    for i in range(70):
        x, y = rng.uniform(80, 1000), rng.uniform(560, 1460); r = rng.uniform(16, 34)
        cv2.circle(f, (int(x + 6 * math.sin(t + i)), int(y)), int(r), C((70, 38, 22)), -1, cv2.LINE_AA)
    for i in range(16):
        sugar_xtal(f, rng.uniform(100, 980), rng.uniform(600, 1420), 1.4, t)
    for i in range(9):
        x, y = rng.uniform(140, 940), rng.uniform(640, 1380); r = rng.uniform(44, 70)
        x += 10 * math.sin(t * 0.8 + i)
        cv2.circle(f, (int(x), int(y)), int(r + 5), C(OUT3), -1, cv2.LINE_AA)
        cv2.circle(f, (int(x), int(y)), int(r), C(BUT), -1, cv2.LINE_AA)
        cv2.circle(f, (int(x - r * 0.35), int(y - r * 0.35)), int(r * 0.3), C(BUT_H), -1, cv2.LINE_AA)
    return f


def shot_S3(t, n):
    tz = T("a1", "The") - 0.2; tc = T("a1", "cocoa") - 0.1
    f = zoom_through(t, tz, 0.9, lambda: _s3_far(t), lambda: _s3_near(t), 540, 1020, 6.0)
    f = np.ascontiguousarray(f, np.float32)
    chapter_card(f, t, st_("S3") + 0.05, 1, "THE FAT", y=1400, dur=1.3, col=(255, 214, 150))
    if t >= tc:
        label_at(f, "COCOA BUTTER", 540, 1440, t, tc, 470, 1300, bg=(200, 150, 40))
        glow(f, 540, 1000, 600, (255, 220, 120), 0.18 * ramp(t, tc, 0.4))
    if t < tz + 0.5: wui(f, "here's the", "[SECRET]", t, st_("S3") + 0.1, acc=(255, 214, 150), size=220, out=tz + 0.4)
    else: wui(f, "the fat in chocolate is", "[COCOA BUTTER]", t, tz + 0.5, acc=BUT, size=140)
    return finish(f, n)


# ---- S4: it comes from the cocoa BEAN (golden-hour cocoa farm; Chubby holds an opened pod) ----
def shot_S4(t, n):
    f = set_dusk(t); tb = T("a2", "bean.") - 0.15
    cast_shadow(f, 330, 1482, 230, 420, 0.05, 0.4)
    chub(f, 330, 1480, 1.0, la=(20, 10), ra=(120, 150), mouth=talk(t), expr="happy", brow="up", look=(1, -0.2),
         hold=scale_el(pod_el(True), 0.55), hold_off=(80, -60), hold_front=True)
    if t >= tb:
        k = clamp((t - tb) / 0.5)
        bx, by = 600 + 160 * k, 860 - 140 * math.sin(math.pi * k * 0.9) + 80 * k
        rot_comp(f, scale_el(bean_el(), 0.9), bx, by, 30 * k, pin(t, tb, 0.3), 1.0, 0.3)
        light_wrap(f, scale_el(bean_el(), 0.9), bx, by, (255, 210, 150), 0.5)
        label_at(f, "COCOA BEAN", 820, 640, t, tb + 0.4, bx, by - 50, bg=(150, 80, 40))
    wui(f, "it comes from the", "[COCOA BEAN]", t, st_("S4") + 0.1, acc=(255, 214, 150), size=160)
    return finish(f, n, look="golden")


# ---- S4b: ...and it has a STRANGE TALENT (block of cocoa butter sparkles; Chubby squints at it) ----
def shot_S4b(t, n):
    f = stage("butter", (255, 255, 230), 540, 1000, 430); ts_ = T("a2", "strange") - 0.1
    if t >= ts_: title3d(f, "TALENT?", 700, t, ts_, size=250, face=(150, 90, 40), side=(70, 40, 16), depth=22)
    b = scale_el(butter_el(), 1.4)
    rot_comp(f, b, 560, 1080 + 8 * math.sin(t * 3), 3 * math.sin(t * 2), pin(t, st_("S4b"), 0.3), 1.0, 0.3)
    sparkles(f, 560, 1060, t, ts_, 14, 300, (255, 255, 255)); sparkles(f, 560, 1060, t, ts_ + 0.8, 10, 260, (255, 240, 180), 3)
    chub_head_only(f, 220, 1380, 0.9, t, mouth=0, expr="sus", brow="sus", look=(1, -0.4))
    return finish(f, n, look="warm")


# ---- S5: when it cools, it can set into SIX crystal shapes (cooling drop -> six brick stacks pop in, numbered) ----
POS6 = [(250, 780), (540, 780), (830, 780), (250, 1200), (540, 1200), (830, 1200)]


def shot_S5(t, n):
    f = stage("crystal"); t6 = T("a3", "six") - 0.15
    if t < t6:
        k = ramp(t, st_("S5"), t6 - st_("S5"))
        col = tuple(int(a + (b - a) * k) for a, b in zip((255, 200, 90), (220, 236, 255)))
        cv2.circle(f, (540, 1000), 130, C(OUT3), -1, cv2.LINE_AA); cv2.circle(f, (540, 1000), 120, C(col), -1, cv2.LINE_AA)
        cv2.circle(f, (500, 960), 34, C((255, 255, 255)), -1, cv2.LINE_AA)
        comp(f, chip("COOLING", (60, 130, 220), WHITE, 30), 540, 1200, op=clamp((t - st_("S5") - 0.2) / 0.3))
        snow(f, t, 0.5 * k, 26, 5, 500, 1500)
    for i, (x, y) in enumerate(POS6):
        ti = t6 + 0.13 * i
        if t >= ti: form_stack(f, i + 1, x, y, 0.88 * pin(t, ti, 0.25), t, op=clamp((t - ti) / 0.15), wob=0.4 if i < 4 else 0.0)
    if t < t6: wui(f, "when it cools down", "it can [SET]", t, st_("S5") + 0.1, acc=BUT, size=170)
    else: wui(f, "", "[6] crystal shapes", t, t6, acc=BUT, size=130)
    return finish(f, n, look="cool")


# ---- S6: SAME FAT, just STACKED differently (12 bricks keep re-arranging: messy -> neat -> loose -> tight) ----
SEQ6 = [1, 5, 3, 6, 2, 5]


def shot_S6(t, n):
    f = stage("latte", (255, 240, 210), 540, 1040, 420); u = lt(t, "S6")
    ph = u / 0.9; i = int(ph) % len(SEQ6); k = clamp((ph - int(ph)) / 0.55)
    lay = lerp_layout(brick_layout(SEQ6[i]), brick_layout(SEQ6[(i + 1) % len(SEQ6)]), k)
    draw_bricks(f, 540, 1040, lay, 1.55, BUT, 1.0, t, 0.0)
    comp(f, chip("SAME 12 BRICKS", INK, WHITE, 34), 540, 1380, op=clamp((u - 0.3) / 0.3))
    ui_word(f, "same fat, just", "[STACKED] differently", 470, t, st_("S6") + 0.1, col=INK, acc=(200, 120, 20), size=120)
    return finish(f, n)


# ---- S6b: like the same bricks, built six ways (Chubby the builder lays bricks; two walls: messy vs neat) ----
def shot_S6b(t, n):
    f = set_room(t); u = lt(t, "S6b")
    cast_shadow(f, 250, 1482, 230, 420, 0.3, 0.35)
    lay_ph = (u * 3.0) % 1.0
    chub(f, 250, 1480, 0.95, la=(20, 10), ra=(60 + 50 * math.sin(lay_ph * math.pi), 60), mouth=talk(t), expr="happy", brow="up", look=(1, 0.3),
         hold=scale_el(brick_el(BUT), 1.0), hold_off=(30, -10), hold_front=True)
    fa = 1 + int(u / 1.1) % 4
    form_stack(f, fa, 590, 1280, 0.85, t, num=True, wob=0.3)
    form_stack(f, 5, 860, 1280, 0.85, t, num=True, glow_=False)
    ui_word(f, "like the same", "[BRICKS]", 470, t, st_("S6b") + 0.1, col=WHITE, acc=BUT, size=200, shadow=0.6, lead_col=WHITE, tail="built 6 different ways")
    return finish(f, n, look="warm")


# ---- S7: shapes 1-4 = the WEAK ones (four wobbly stacks, a WEAK stamp) ----
def shot_S7(t, n):
    f = stage("crystal"); tw = T("b1", "weak") - 0.1
    for i, x in enumerate((205, 415, 625, 835)):
        form_stack(f, i + 1, x, 1060, 0.7, t, wob=1.6 if t >= tw else 0.5)
    if t >= tw: slam(f, stamp_el("WEAK", RED_, 70), 540, 1380, -6, t, tw)
    wui(f, "shapes", "[1 TO 4]", t, st_("S7") + 0.05, acc=BUT, size=200)
    return finish(f, n, look="cool")


# ---- S7b: they melt too easily -> the chocolate turns SOFT and DULL (stacks melt; a matte bar sags) ----
def shot_S7b(t, n):
    f = stage("chalk"); tm = T("b1", "melt") - 0.1; tsft = T("b1", "soft") - 0.15
    for i, x in enumerate((180, 400, 620, 860)):
        form_stack(f, i + 1, x, 820, 0.5, t, num=False, wob=0.6, melt=ramp(t, tm + i * 0.1, 1.1))
    if t >= tm + 0.3:
        for i, x in enumerate((180, 400, 620, 860)): puddle(f, x, 900, 70, ramp(t, tm + 0.3 + i * 0.1, 0.6))
    k = ramp(t, tsft, 0.8)
    bar = scale_el(choc_bar_el("matte"), 0.95)
    b2 = scale_xy(bar, 1 + 0.06 * k, 1 - 0.18 * k)
    rot_comp(f, b2, 540, 1250 + 20 * k, 0, 1.0, 1.0, 0.3)
    if t >= tsft + 0.3: label_at(f, "SOFT + DULL", 820, 1440, t, tsft + 0.3, 680, 1300, bg=(110, 100, 96))
    if t < tsft: ui_word(f, "they melt", "[TOO EASILY]", 470, t, st_("S7b") + 0.1, col=INK, acc=RED_, size=150, out=tsft - 0.05)
    else: ui_word(f, "so the chocolate turns", "[SOFT] and [DULL]", 470, t, tsft, col=INK, acc=(120, 110, 100), size=150)
    return finish(f, n)


# ---- S8: but shape 5 is the WINNER (golden backlight, medal, Chubby cheers; 3D 'WINNER' behind) ----
def shot_S8(t, n):
    tw = T("b2", "winner.") - 0.1
    f = set_chocolatier(t) * 0.55
    god_rays(f, 640, 380, t, (255, 214, 120), 0.45, 11, 1500, 1.2, 1.57, 4)
    if t >= tw: title3d(f, "WINNER", 640, t, tw, size=300, face=(255, 208, 70), side=(120, 70, 10), depth=28)
    chub(f, 220, 1500, 1.05, la=(150, 170), ra=(150, 170), mouth=3 if t >= tw else talk(t), expr="wow" if t >= tw else "happy", brow="up", look=(1, -0.4), bob=4 * math.sin(t * 8))
    marble_front(f, CTR)
    form_stack(f, 5, 620, 1060, 1.35 * pin(t, st_("S8") + 0.05, 0.3), t, num=False, glow_=True)
    comp(f, chip("SHAPE 5", (150, 90, 0), WHITE, 40), 620, 1260, op=clamp((t - st_("S8") - 0.2) / 0.2))
    if t >= tw: comp(f, scale_el(medal_el("5"), 0.55), 900, 1090, scale=pin(t, tw + 0.1, 0.3)); confetti(f, t, tw, 40, 3, 2.0)
    return finish(f, n, look="golden")


# ---- S9: it's SHINY, it SNAPS (material close-up: a light sweeps across the gloss, then the bar snaps) ----
def shot_S9(t, n):
    f = stage("cocoa", (255, 200, 140), 540, 1020, 380); tsh = T("b3", "shiny.") - 0.15; tsn = T("b3", "snaps.") - 0.1
    if t < tsn:
        bar = scale_el(choc_bar_el("gloss"), 1.25)
        rot_comp(f, bar, 540, 1040, -6 + 2 * math.sin(t), 1.0, 1.0, 0.35)
        sx = 160 + 760 * ramp(t, tsh - 0.1, 0.6)
        glow(f, sx, 960, 90, (255, 250, 230), 0.55 * clamp((t - tsh + 0.2) / 0.2))
        sparkles(f, 420, 950, t, tsh, 10, 200, (255, 255, 255))
        if t >= tsh: label_at(f, "SHINY", 300, 1360, t, tsh, 400, 1180, bg=(150, 90, 0))
    else:
        k = clamp((t - tsn) / 0.35)
        rot_comp(f, scale_el(choc_bar_el("gloss", cols=2), 1.25), 400 - 50 * k, 1040 + 20 * k, -6 - 10 * k, 1.0, 1.0, 0.35)
        rot_comp(f, scale_el(choc_bar_el("gloss", cols=2), 1.25), 680 + 50 * k, 1040 + 20 * k, -6 + 12 * k, 1.0, 1.0, 0.35)
        crumbs(f, 540, 1040, t, tsn, 12, 6)
        comp(f, burst_el("SNAP!", YEL_, INK, 64), 540, 760, scale=pin(t, tsn, 0.2))
        label_at(f, "SHINY", 300, 1360, t, tsh, 400, 1180, bg=(150, 90, 0)); label_at(f, "SNAPS", 780, 1360, t, tsn + 0.1, 690, 1190, bg=(150, 90, 0))
    wui(f, "shape 5 is", "[SHINY]", t, st_("S9") + 0.05, acc=(255, 210, 120), size=200)
    return finish(f, n, look="warm")


# ---- S9b: and it melts at about 34 C (thermometer climbs; a piece on a plate melts exactly at 34) ----
def shot_S9b(t, n):
    f = stage("cream", (255, 230, 200), 680, 1060, 380); t34 = T("b3", "thirty-four") - 0.2
    v = 20 + 14 * ramp(t, st_("S9b") + 0.2, max(0.3, t34 - st_("S9b") + 0.4))
    temp_gauge(f, 200, 1380, 700, v, marks=[(34, "34° MELTS", (200, 110, 30))] if t >= t34 + 0.3 else [])
    comp(f, scale_el(plate_el(), 0.75), 720, 1300)
    melting_piece(f, 720, 1290, 0.9, ramp(t, t34 + 0.2, 1.2), "gloss", t)
    comp(f, chip("Source: ACS; Beckett, The Science of Chocolate", INK, WHITE, 22), 540, 1462)
    ui_word(f, "melts at about", f"[{int(round(v))}°C]", 470, t, st_("S9b") + 0.1, col=INK, acc=(200, 110, 30), size=200)
    return finish(f, n)


# ---- S10: inside your mouth it's close to 37 -> just a little warmer (+3 degrees) ----
def shot_S10(t, n):
    f = dof(set_room(t), 9) * 0.75; t37 = T("b4", "thirty-seven.") - 0.15; tw = T("b4", "warmer.") - 0.15
    lamp_glow(f, 700, 1000, 450, (255, 180, 120), 0.35)
    chub_head_only(f, 700, 1040, 1.9, t, mouth="o" if t < tw else 1, expr="happy", brow="up", look=(-0.7, 0))
    v = 34 + 3 * ramp(t, t37, 0.7)
    Y = temp_gauge(f, 170, 1420, 720, v, lo=26.0, marks=[(34, "34° MELTS", (200, 110, 30))] + ([(37, "37° MOUTH", (220, 60, 60))] if t >= t37 + 0.2 else []))
    if t < tw: wui(f, "inside your mouth, close to", "[37°C]", t, st_("S10") + 0.1, acc=(255, 150, 140), size=200, out=tw - 0.05)
    else: wui(f, "just a little warmer", "[+3°C]", t, tw, acc=(255, 150, 140), size=200)
    return finish(f, n)


# ---- S11: so it stays SOLID in the wrapper (kitchen, cool light, Chubby shows the wrapped bar; 3D 'SOLID') ----
def shot_S11(t, n):
    f = set_kitchen(t)
    title3d(f, "SOLID", 640, t, st_("S11") + 0.15, size=320, face=(220, 236, 255), side=(60, 90, 130), depth=26)
    chub(f, 300, 1500, 1.05, la=(20, 10), ra=(118, 120), mouth=talk(t), expr="smirk", brow="up", look=(1, -0.2),
         hold=scale_el(wrapped_bar_el(0.45), 0.6), hold_off=(90, -40), hold_front=True)
    counter_front(f, CTR)
    return finish(f, n, look="cool")


# ---- S11b: ...and melts the moment it hits your tongue (Chubby eats; close-up inset of the tongue: piece -> puddle) ----
def shot_S11b(t, n):
    f = set_kitchen(t); tt = T("b5", "melts") - 0.1
    hand_to_mouth(f, 260, 1500, 1.0, t, scale_el(choc_piece_el("gloss"), 0.35), expr="happy", mouth="o", look=(0.4, -0.3))
    counter_front(f, CTR)
    k = pin(t, st_("S11b") + 0.1, 0.3)

    def close(g):
        g[:] = stage("pink")
        comp(g, scale_el(tongue_el(), 0.75), 720, 1060)
        melting_piece(g, 720, 1040, 1.0, ramp(t, tt, 1.3), "gloss", t)
    inset(f, 720, 1000, 300, close, k)
    if k > 0.5: comp(f, chip("YOUR TONGUE", INK, WHITE, 30), 720, 1350)
    wui(f, "melts the moment it hits your", "[TONGUE]", t, T("b5", "tongue.") - 0.4, acc=(255, 160, 180), size=200)
    return finish(f, n)


# ---- S12: PART 2 — but here's the CATCH (dim workroom, a steaming pot, Chubby suspicious) ----
def shot_S12(t, n):
    f = set_chocolatier(t) * 0.6
    mood(f, (90, 60, 140), 0.25)
    chub(f, 300, 1500, 1.05, la=(150, -150), ra=(20, 10), mouth=talk(t), expr="sus", brow="sus", look=(1, 0.3))
    marble_front(f, CTR)
    comp(f, scale_el(pot_el(), 1.0), 760, CTR - 120)
    steam(f, 760, CTR - 260, t, 1.0)
    chapter_card(f, t, st_("S12") + 0.05, 2, "THE CATCH", y=1430, dur=1.4, col=(220, 180, 255))
    wui(f, "here's the", "[CATCH]", t, st_("S12") + 0.1, acc=(220, 180, 255), size=220)
    return finish(f, n, look="night")


# ---- S13: melt chocolate and JUST LET IT COOL (top-down pool turning cold) ----
def shot_S13(t, n):
    f = stage("cocoa"); tc = T("c2", "cool,") - 0.15
    pool(f, 540, 1060, 360, t)
    if t >= tc:
        mood(f, (120, 180, 255), 0.35 * ramp(t, tc, 0.6))
        snow(f, t, ramp(t, tc, 0.6), 30, 7, 600, 1500)
        comp(f, chip("JUST LET IT COOL", (60, 130, 220), WHITE, 34), 540, 1460, scale=pin(t, tc, 0.25))
    wui(f, "melt chocolate and just let it", "[COOL]", t, st_("S13") + 0.1, acc=(170, 210, 255), size=200)
    return finish(f, n)


# ---- S13b: ...you get a MESSY MIX of all the shapes (every kind of crystal pops up in the setting chocolate) ----
MIX = [(int(np.random.default_rng(i).integers(1, 7)), 190 + (i % 4) * 230 + (60 if (i // 4) % 2 else 0), 760 + (i // 4) * 230) for i in range(12)]


def shot_S13b(t, n):
    f = stage("cocoa"); tm = T("c2", "messy") - 0.15
    pool(f, 540, 1060, 400, t * 0.2)
    for j, (fm, x, y) in enumerate(MIX):
        tj = st_("S13b") + 0.08 * j
        if t >= tj and x < 960: form_stack(f, fm, x, y, 0.48 * pin(t, tj, 0.2), t, num=False, wob=0.5)
    if t >= tm + 0.5:
        comp(f, scale_el(choc_bar_el("matte"), 0.55), 540, 1430, scale=pin(t, tm + 0.5, 0.3))
    wui(f, "you get a", "[MESSY MIX]", t, st_("S13b") + 0.05, acc=(255, 140, 120), size=200)
    return finish(f, n)


# ---- S14: chocolate makers use a trick: TEMPERING (Chubby in a white coat works chocolate on the marble slab) ----
def shot_S14(t, n):
    f = set_chocolatier(t); tt = T("c3", "tempering.") - 0.15
    if t >= tt: title3d(f, "TEMPERING", 640, t, tt, size=230, face=(255, 226, 190), side=(110, 60, 30), depth=24)
    sw = math.sin(t * 5)
    chub(f, 320, 1520, 1.08, la=(20, 10), ra=(70 + 18 * sw, 40), mouth=talk(t), expr="happy", brow="up", look=(1, 0.5), shirt=(240, 240, 236),
         hold=scale_el(spatula_el(), 0.6), hold_off=(40, 30), hold_front=True)
    marble_front(f, CTR)
    cv2.ellipse(f, (int(640 + 30 * sw), CTR + 120), (240, 60), 0, 0, 360, C(OUT3), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(640 + 30 * sw), CTR + 120), (232, 54), 0, 0, 360, C((110, 60, 36)), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(560 + 30 * sw), CTR + 100), (70, 12), 0, 0, 360, C((240, 210, 180)), -1, cv2.LINE_AA)
    if t < tt: wui(f, "chocolate makers use a", "[TRICK]", t, st_("S14") + 0.1, acc=(255, 214, 150), size=200, out=tt - 0.05)
    return finish(f, n, look="warm")


# ---- S15: 1 MELT -> 2 COOL -> 3 WARM A LITTLE (a temperature line drawn with the voice; Chubby rides the line) ----
def shot_S15(t, n):
    f = stage("cream", (255, 236, 214), 540, 1000, 300)
    head = temper_chart(f, t, (T("c4", "melt") - 0.15, T("c4", "cool") - 0.15, T("c4", "warm") - 0.15))
    if head is not None: chub_head_only(f, head[0], head[1] - 90, 0.42, t, mouth=talk(t), expr="happy", brow="up")
    ui_word(f, "tempering in", "[3 STEPS]", 470, t, st_("S15") + 0.1, col=INK, acc=(200, 110, 30), size=190)
    return finish(f, n)


# ---- S16: the gentle warm-up melts the WEAK crystals (orange warmth; shapes 1-4 melt, 5 stays) ----
def shot_S16(t, n):
    f = stage("crystal"); tm = T("c5", "melts") - 0.15
    mood(f, (255, 150, 60), 0.3 * ramp(t, st_("S16"), 0.6))
    glow(f, 540, 1500, 600, (255, 140, 50), 0.35)
    for i, (x, y) in enumerate(((200, 860), (430, 860), (660, 860), (890, 860), (540, 1210))):
        fm = i + 1
        form_stack(f, fm, x, y, 0.6 if fm < 5 else 0.8, t, num=fm == 5, melt=ramp(t, tm + 0.1 * i, 1.0) if fm < 5 else 0.0,
                   glow_=fm == 5 and t >= tm + 0.6)
        if fm < 5 and t >= tm + 0.4: puddle(f, x, y + 60, 60, ramp(t, tm + 0.4 + 0.1 * i, 0.5))
    wui(f, "the warm-up melts the", "[WEAK] ones", t, st_("S16") + 0.1, acc=(255, 180, 120), size=170)
    return finish(f, n)


# ---- S16b: but shape 5 SURVIVES (alone, golden) ----
def shot_S16b(t, n):
    f = stage("crystal", (255, 214, 120), 540, 1060, 380)
    title3d(f, "SURVIVES", 700, t, st_("S16b") + 0.1, size=230, face=(255, 214, 90), side=(120, 70, 10), depth=24)
    form_stack(f, 5, 540, 1100, 1.4 * pin(t, st_("S16b"), 0.3), t, num=False, glow_=True)
    sparkles(f, 540, 1100, t, st_("S16b") + 0.2, 14, 330, (255, 240, 180))
    comp(f, chip("SHAPE 5", (150, 90, 0), WHITE, 40), 540, 1380)
    return finish(f, n, look="golden")


# ---- S17: those crystals work like SEEDS (top-down: a few golden seed bricks glow in the liquid chocolate) ----
SEEDS = [(390, 900), (700, 960), (520, 1220), (780, 1240)]


def shot_S17(t, n):
    f = stage("cocoa"); ts_ = T("c6", "seeds.") - 0.2
    pool(f, 540, 1060, 400, t)
    for i, (x, y) in enumerate(SEEDS):
        ti = st_("S17") + 0.15 * i
        if t >= ti:
            glow(f, x, y, 70, (255, 210, 90), 0.6 + 0.3 * math.sin(t * 6 + i))
            rot_comp(f, scale_el(brick_el(GOLD5), 1.0), x, y, 0, pin(t, ti, 0.25), 1.0, 0.25)
    if t >= ts_: label_at(f, "SEEDS", 540, 1450, t, ts_, 520, 1260, bg=(150, 90, 0))
    wui(f, "they work like", "[SEEDS]", t, st_("S17") + 0.05, acc=(255, 214, 90), size=220)
    return finish(f, n)


# ---- S17b: as it sets, the rest LINES UP THE SAME WAY (neat brick lattice grows out from the seeds -> glossy bar) ----
_LAT = None


def lattice():
    global _LAT
    if _LAT is None:
        pts = []
        for r_ in range(-12, 13):
            for c_ in range(-8, 9):
                x = 540 + c_ * 78 + (39 if r_ % 2 else 0); y = 1060 + r_ * 38
                if (x - 540) ** 2 + (y - 1060) ** 2 < 370 ** 2:
                    dmin = min(math.hypot(x - sx, y - sy) for sx, sy in SEEDS); pts.append((dmin, x, y))
        _LAT = sorted(pts)
    return _LAT


def shot_S17b(t, n):
    f = stage("cocoa"); tw = T("c6", "way.") - 0.1
    pool(f, 540, 1060, 400, t)
    R = 70 + 360 * ramp(t, st_("S17b") + 0.1, tw - st_("S17b") - 0.1)
    el = scale_el(brick_el(GOLD5), 0.98)
    for d_, x, y in lattice():
        if d_ > R: break
        rot_comp(f, el, x, y, 0, min(1.0, 0.5 + (R - d_) / 60), 1.0, 0.0)
    if t >= tw:
        k = ramp(t, tw, 0.5)
        bar = scale_el(choc_bar_el("gloss"), 1.15)
        g = f.copy(); rot_comp(g, bar, 540, 1060, -4, 1.0, 1.0, 0.35); f[:] = f * (1 - k) + g * k
        if k > 0.5: comp(f, chip("SHINY + SNAPPY", (150, 90, 0), WHITE, 34), 540, 1440, scale=pin(t, tw + 0.25, 0.25))
    wui(f, "the rest lines up the", "[SAME WAY]", t, st_("S17b") + 0.05, acc=(255, 214, 90), size=180)
    return finish(f, n)


# ---- S18: PART 3 — that white dust... in your HALLOWEEN candy bag (night room, pumpkin pail, flashlight on a bloomed bar) ----
def shot_S18(t, n):
    f = set_room(t) * 0.42; th = T("d1", "Halloween") - 0.15
    mood(f, (120, 60, 160), 0.35)
    comp(f, scale_el(bucket_el(True), 0.85), 770, 1300)
    chub(f, 360, 1480, 1.0, la=(20, 10), ra=(118, 130), mouth=talk(t), expr="sus", brow="sus", look=(1, -0.3),
         hold=scale_el(choc_bar_el("chalky"), 0.45), hold_off=(70, -40), hold_front=True)
    spotlight(f, 560, 930, 260, 0.55, 160)
    chapter_card(f, t, st_("S18") + 0.05, 3, "THE WHITE DUST", y=1440, dur=1.5, col=(220, 220, 210))
    if t < th: wui(f, "now, that", "[WHITE DUST]", t, st_("S18") + 0.1, acc=(230, 230, 220), size=180, out=th - 0.05)
    else: wui(f, "in your", "[HALLOWEEN] candy bag", t, th, acc=(255, 150, 60), size=140)
    return finish(f, n, look="night")


# ---- S19: it's NOT mould (MOULD? -> busted) — it's called BLOOM (3D) ----
def shot_S19(t, n):
    f = stage("chalk", (240, 236, 228), 540, 1100, 400); tb = T("d2", "mould.") + 0.05; tbl = T("d2", "bloom.") - 0.15
    if t >= tbl: title3d(f, "BLOOM", 820, t, tbl, size=330, face=(246, 242, 234), side=(120, 110, 100), depth=28)
    bar = scale_el(choc_bar_el("chalky"), 0.95)
    rot_comp(f, bar, 540, 1200, -3, pin(t, st_("S19"), 0.25), 1.0, 0.35)
    if t < tbl + 0.2:
        comp(f, scale_el(mould_el(), 0.7), 300, 600, op=1 - clamp((t - tbl) / 0.2))
        myth_tag(f, 620, 620, t, st_("S19") + 0.05, tb, 52, "MOULD?")
    if t >= tbl: comp(f, check_el(46, True), 860, 1400, scale=pin(t, tbl + 0.2, 0.25))
    return finish(f, n, look="fresh")


# ---- S20: warmth -> fat MELTS -> RISES to the surface (cut-away bar with yellow fat drops travelling up) ----
def shot_S20(t, n):
    f = stage("orange", (255, 210, 140), 860, 680, 200); tw = T("d3", "warm,") - 0.15; tm = T("d3", "melts,") - 0.15; tr = T("d3", "rises") - 0.15
    sun_icon(f, 860, 680, 80, t)
    god_rays(f, 860, 680, t, (255, 220, 160), 0.25, 9, 900, 1.0, 2.2, 3)
    x0, x1, y0, y1 = 140, 940, 900, 1330
    cv2.rectangle(f, (x0 - 6, y0 - 6), (x1 + 6, y1 + 6), C(OUT3), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C((106, 58, 34)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y0 + 18), C((150, 90, 56)), -1, cv2.LINE_AA)
    rng = np.random.default_rng(9)
    for i in range(18):
        bx, by = rng.uniform(x0 + 40, x1 - 40), rng.uniform(y0 + 80, y1 - 40)
        if t >= tm:
            k = ramp(t, tr + 0.03 * i, 1.4)
            by = by + (y0 + 16 - by) * k
        r = 18 if t >= tm else 12
        cv2.circle(f, (int(bx), int(by)), r + 3, C(OUT3), -1, cv2.LINE_AA)
        cv2.circle(f, (int(bx), int(by)), r, C(BUT if t >= tm else (180, 140, 70)), -1, cv2.LINE_AA)
    comp(f, chip("INSIDE THE BAR", INK, WHITE, 28), 540, 1380)
    if t >= tw: comp(f, chip("1  WARM", INK, WHITE, 32), 330, 800, scale=pin(t, tw, 0.25))
    if t >= tm: comp(f, chip("2  FAT MELTS", INK, BUT, 32), 600, 800, scale=pin(t, tm, 0.25))
    if t >= tr:
        draw_arrow(f, 930, y1 - 40, 930, y0 + 20, eo(clamp((t - tr) / 0.4)), INK, 10, 30)
        comp(f, chip("3  RISES", (90, 80, 70), WHITE, 32), 540, 1450, scale=pin(t, tr, 0.25))
    wui(f, "when chocolate gets", "[WARM]", t, st_("S20") + 0.1, acc=(255, 220, 120), size=200)
    return finish(f, n, look="warm")


# ---- S20b: ...and sets again as a WHITE FILM (the same bar turns from gloss to chalky in front of you) ----
def shot_S20b(t, n):
    f = stage("chalk", (250, 246, 238), 540, 1060, 400); tf = T("d3", "white") - 0.3
    k = ramp(t, st_("S20b") + 0.3, tf - st_("S20b"))
    a = scale_el(choc_bar_el("gloss"), 1.15); b = scale_el(choc_bar_el("chalky"), 1.15)
    g1 = f.copy(); rot_comp(g1, a, 540, 1060, -4, 1.0, 1.0, 0.35)
    g2 = f.copy(); rot_comp(g2, b, 540, 1060, -4, 1.0, 1.0, 0.35)
    f = g1 * (1 - k) + g2 * k
    if t >= tf: label_at(f, "FAT BLOOM", 760, 1420, t, tf, 640, 1220, bg=(120, 110, 100))
    ui_word(f, "it sets again as a", "[WHITE FILM]", 470, t, st_("S20b") + 0.05, col=INK, acc=(150, 140, 130), size=170)
    return finish(f, n, look="fresh")


# ---- S21: over MONTHS, shape 5 slowly turns into shape 6 (calendar flips; the bricks squeeze tighter) ----
def shot_S21(t, n):
    f = stage("cream"); u = lt(t, "S21"); t6 = T("d4", "six.") - 0.3; tsl = T("d4", "slowly") - 0.1
    mth = 1 + min(5, int(u / 0.6))
    rot_comp(f, scale_el(calendar_el("MONTH", str(mth)), 0.55), 230, 820, -5, 1.0, 1.0, 0.25)
    k = ramp(t, tsl, t6 - tsl + 0.2)
    col = tuple(int(a + (b - a) * k) for a, b in zip(FORM_COL[5], FORM_COL[6]))
    draw_bricks(f, 640, 1150, lerp_layout(brick_layout(5), brick_layout(6), k), 1.25, col, 1.0, t)
    comp(f, chip("SHAPE 6" if k > 0.6 else "SHAPE 5", INK, WHITE, 36), 640, 1400)
    ui_word(f, "over", "[MONTHS]", 470, t, st_("S21") + 0.05, col=INK, acc=(150, 90, 0), size=200, tail="shape 5 can turn into shape 6")
    return finish(f, n)


# ---- S21b: that can bloom too (a bar dusts over slowly, calendar in the corner) ----
def shot_S21b(t, n):
    f = stage("chalk"); k = ramp(t, st_("S21b") + 0.2, 1.2)
    a = scale_el(choc_bar_el("gloss"), 1.0); b = scale_el(choc_bar_el("chalky"), 1.0)
    g1 = f.copy(); rot_comp(g1, a, 540, 1100, 3, 1.0, 1.0, 0.35); g2 = f.copy(); rot_comp(g2, b, 540, 1100, 3, 1.0, 1.0, 0.35)
    f = g1 * (1 - k) + g2 * k
    rot_comp(f, scale_el(calendar_el("MONTH", "6"), 0.4), 860, 800, 6, 1.0, 1.0, 0.25)
    ui_word(f, "that can", "[BLOOM] too", 470, t, st_("S21b") + 0.05, col=INK, acc=(150, 140, 130), size=200)
    return finish(f, n, look="fresh")


# ---- S22: in a damp FRIDGE (night kitchen lit only by the open fridge; drops of water bead on the bar) ----
def shot_S22(t, n):
    f = set_fridge_night(t); tw = T("d5", "water") - 0.1; ts_ = T("d5", "sugar") - 0.1
    chub(f, 250, 1500, 1.0, la=(20, 10), ra=(70, 40), mouth=talk(t), expr="sus", brow="sus", look=(1, 0.2))
    mood(f, (120, 170, 255), 0.25)
    comp(f, scale_el(plate_el(), 0.7), 640, 1420)
    bar = scale_el(choc_bar_el("gloss"), 0.6)
    comp(f, bar, 640, 1350)
    light_wrap(f, bar, 640, 1350, (170, 220, 255), 0.7)
    if t >= tw:
        rng = np.random.default_rng(3)
        for i in range(16):
            ti = tw + 0.08 * i; x, y = rng.uniform(500, 780), rng.uniform(1290, 1410)
            if t >= ti:
                r = int(8 + 6 * pin(t, ti, 0.3))
                cv2.circle(f, (int(x), int(y)), r + 2, C((40, 80, 130)), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), r, C((190, 230, 255)), -1, cv2.LINE_AA)
                cv2.circle(f, (int(x - r * 0.3), int(y - r * 0.3)), max(1, r // 3), C(WHITE), -1, cv2.LINE_AA)
        comp(f, chip("WATER", (60, 130, 220), WHITE, 30), 860, 1230, scale=pin(t, tw, 0.25))
    if t >= ts_: comp(f, chip("PULLS SUGAR UP", (90, 110, 150), WHITE, 30), 640, 1170, scale=pin(t, ts_, 0.25))
    wui(f, "in a damp", "[FRIDGE]", t, st_("S22") + 0.1, acc=(170, 220, 255), size=200)
    return finish(f, n, look="cool")


# ---- S22b: it dries into tiny white SUGAR crystals (magnifier close-up of the bar's surface) ----
def shot_S22b(t, n):
    f = stage("frost")
    comp(f, scale_el(choc_bar_el("chalky"), 0.9), 540, 1250)

    def close(g):
        g[:] = stage("cocoa")
        rng = np.random.default_rng(8)
        for i in range(24):
            ti = st_("S22b") + 0.05 * i; x, y = rng.uniform(320, 760), rng.uniform(760, 1180)
            if t >= ti: sugar_xtal(g, x, y, 1.6 * pin(t, ti, 0.2), t)
    inset(f, 540, 970, 270, close, pin(t, st_("S22b") + 0.05, 0.3))
    label_at(f, "SUGAR CRYSTALS", 540, 1450, t, st_("S22b") + 0.5, 540, 1250, bg=(90, 110, 150))
    wui(f, "tiny white", "[SUGAR] crystals", t, st_("S22b") + 0.1, acc=(200, 230, 255), size=150)
    return finish(f, n, look="cool")


# ---- S23: either way, it's still SAFE to eat (bright kitchen, Chubby eats a bloomed piece; big check; 3D 'SAFE') ----
def shot_S23(t, n):
    f = set_kitchen(t); tsf = T("d6", "safe") - 0.15
    if t >= tsf: title3d(f, "SAFE", 640, t, tsf, size=340, face=(120, 230, 150), side=(20, 100, 50), depth=28)
    hand_to_mouth(f, 300, 1500, 1.05, t, scale_el(choc_piece_el("chalky"), 0.4), expr="happy", mouth=munch(t), look=(0.3, -0.3))
    counter_front(f, CTR)
    if t >= tsf: comp(f, check_el(60, True), 800, 1150, scale=pin(t, tsf + 0.1, 0.3))
    if t < tsf: wui(f, "either way, it's still", "[SAFE] to eat", t, st_("S23") + 0.1, acc=(140, 240, 160), size=170, out=tsf - 0.05)
    return finish(f, n, look="fresh")


# ---- S23b: it just feels a bit CHALKY (close-up chewing, a puff of white dust, 'meh' face) ----
def shot_S23b(t, n):
    f = dof(set_kitchen(t), 8); tc = T("d6", "chalky.") - 0.15
    chub_head_only(f, 540, 1050, 2.0, t, mouth=munch(t) if t < tc else 0, expr="sus" if t >= tc else "n", brow="sus" if t >= tc else "n", look=(0, 0))
    dust_puff(f, 540, 1250, t, tc, 10, 0.7)
    wui(f, "it just feels a bit", "[CHALKY]", t, st_("S23b") + 0.1, acc=(230, 230, 220), size=200)
    return finish(f, n)


# ---- S24: keep it somewhere COOL + DRY, NOT in the fridge (split: jar in a cupboard vs fridge with a red X) ----
def fridge_icon(g, x, y, s=1.0):
    cv2.rectangle(g, (int(x - 110 * s), int(y - 230 * s)), (int(x + 110 * s), int(y + 230 * s)), C(OUT3), -1, cv2.LINE_AA)
    cv2.rectangle(g, (int(x - 100 * s), int(y - 220 * s)), (int(x + 100 * s), int(y + 220 * s)), C((236, 244, 252)), -1, cv2.LINE_AA)
    cv2.line(g, (int(x - 100 * s), int(y - 60 * s)), (int(x + 100 * s), int(y - 60 * s)), C(OUT3), 6, cv2.LINE_AA)
    for yy in (-150, 20): cv2.rectangle(g, (int(x + 60 * s), int(y + yy * s)), (int(x + 76 * s), int(y + (yy + 80) * s)), C((150, 160, 176)), -1, cv2.LINE_AA)


def shot_S24(t, n):
    f = set_room(t) * 0.8; tn = T("e1", "Not") - 0.15

    def L(g):
        cv2.rectangle(g, (150, 860), (510, 1300), C((150, 100, 64)), -1, cv2.LINE_AA)
        cv2.rectangle(g, (170, 880), (490, 1280), C((96, 62, 40)), -1, cv2.LINE_AA)
        comp(g, scale_el(jar_el(), 0.8), 330, 1120)
        comp(g, chip("CUPBOARD", INK, WHITE, 28), 330, 1380)

    def R(g):
        fridge_icon(g, 750, 1080, 0.95)
        if t >= tn + 0.2:
            k = clamp((t - tn - 0.2) / 0.2)
            for sg in (-1, 1):
                cv2.line(g, (600, 1080 - sg * 180), (int(600 + 300 * k), int(1080 - sg * 180 + sg * 360 * k)), C(INK), 34, cv2.LINE_AA)
                cv2.line(g, (600, 1080 - sg * 180), (int(600 + 300 * k), int(1080 - sg * 180 + sg * 360 * k)), C(RED_), 22, cv2.LINE_AA)
        comp(g, chip("TOO DAMP", RED_, WHITE, 28), 750, 1380)
    split_contrast(f, t, st_("S24") + 0.02, L, R, "COOL + DRY", "NOT THE FRIDGE", (40, 170, 110), (220, 60, 60), y0=640, y1=1480, t_r=tn)
    wui(f, "keep your chocolate", "[COOL + DRY]", t, st_("S24") + 0.1, acc=(140, 240, 160), size=170)
    return finish(f, n)


# ---- S25: already bloomed? melt it into a CAKE (golden kitchen; the bloomed bar drops into a pot; a cake pops up) ----
def shot_S25(t, n):
    f = set_kitchen(t); tc = T("e2", "cake.") - 0.15; tm = T("e2", "Melt") - 0.1
    god_rays(f, 120, 560, t, (255, 210, 140), 0.18, 7, 1500, 0.55, 0.55, 2)
    if t >= tc: title3d(f, "CAKE!", 640, t, tc, size=320, face=(255, 196, 140), side=(110, 50, 24), depth=26)
    chub(f, 280, 1500, 1.02, la=(20, 10), ra=(100, 90) if t < tc else (150, 170), mouth=talk(t), expr="happy" if t < tc else "wow", brow="up", look=(1, 0.2))
    counter_front(f, CTR)
    if t < tc:
        comp(f, scale_el(pot_el(), 0.75), 740, CTR - 80)
        k = ramp(t, tm, 0.5)
        rot_comp(f, scale_el(choc_bar_el("chalky"), 0.4), 740, 860 + 260 * k, 30 * k, 1.0, 1.0 - 0.9 * clamp((k - 0.8) / 0.2), 0.2)
        steam(f, 740, CTR - 200, t, 0.9)
    else:
        comp(f, scale_el(cake_el(), 0.85), 740, CTR - 120, scale=pin(t, tc, 0.3))
        sparkles(f, 740, CTR - 200, t, tc, 12, 260)
    if t < tc: wui(f, "already bloomed?", "[MELT IT]", t, st_("S25") + 0.1, acc=(255, 214, 150), size=200, out=tc - 0.05)
    return finish(f, n, look="golden")


# ---- S25b: nobody will KNOW (Chubby with a slice of cake, smirk + raised brow) ----
def shot_S25b(t, n):
    f = set_kitchen(t)
    chub(f, 420, 1500, 1.12, la=(20, 10), ra=(118, 120), mouth=0, expr="smirk", brow="sus", look=(0, 0), hold=scale_el(cake_el(), 0.3), hold_off=(80, -40), hold_front=True,
         bob=2 * math.sin(t * 4))
    counter_front(f, CTR)
    sparkles(f, 560, 980, t, st_("S25b") + 0.3, 8, 160)
    wui(f, "nobody will", "[KNOW]", t, st_("S25b") + 0.05, acc=(255, 214, 150), size=220)
    return finish(f, n, look="golden")


# ---- S26: RECAP — shape 5 -> melts at 34 in your mouth -> white bloom = fat or sugar (safe) ----
def shot_S26(t, n):
    f = stage("cocoa", (255, 210, 150), 540, 1000, 420)
    items = [(scale_el(choc_piece_el("gloss"), 0.9), "SHAPE 5"), (scale_el(tongue_el(), 0.28), "MELTS AT 34°"), (scale_el(choc_piece_el("chalky"), 0.9), "BLOOM IS SAFE")]
    ts = [T("f1", "built") - 0.15, T("f1", "mouth.") - 0.15, T("f1", "bloom") - 0.15]
    recap_steps(f, items, 1000, t, ts, 290, 1.1)
    if t >= T("f1", "fat") - 0.1: comp(f, chip("FAT OR SUGAR", (120, 110, 100), WHITE, 30), 540, 1340, scale=pin(t, T("f1", "fat") - 0.1, 0.25))
    wui(f, "", "[REMEMBER]", t, st_("S26") + 0.05, acc=(255, 214, 150), size=200)
    return finish(f, n, look="warm")


# ---- S27: send it + FreshNestHub sting ----
def shot_S27(t, n):
    f = set_chocolatier(t) * 0.8
    vend = LINES["f2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("f2", "Send") + 0.3
        comp(f, scale_el(phone2_el("why is my chocolate white??", "it's bloom. still safe!", pr), 0.82), 680, 950, scale=pin(t, st_("S27")))
        if pr and t < T("f2", "Send") + 0.75:
            rr = (t - T("f2", "Send") - 0.3) / 0.45
            cv2.circle(f, (680, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 250, 1500, 0.85, la=(20, 10), ra=(70, 40), mouth=talk(t), expr="happy", brow="up", look=(1, 0), hold=scale_el(choc_bar_el("chalky"), 0.3), hold_off=(40, -20), hold_front=True)
        marble_front(f, 1400)
        ui_word(f, "send to the friend who throws away", "[WHITE CHOCOLATE]", 420, t, T("f2", "friend") - 0.1, col=WHITE, acc=(255, 214, 150), size=110, shadow=0.6, lead_col=WHITE)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=WHITE, lead_size=42, shadow=0.6), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        hand_to_mouth(f, 400, 1520, 0.75, t, scale_el(choc_piece_el("gloss"), 0.3), expr="happy", mouth=munch(t))
        marble_front(f, 1400)
    return finish(f, n, look="warm")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TSNAP, 0.35, 18), (TMELT, 0.3, 10), (T("i2", "snaps.") - 0.1, 0.35, 16), (T("i3", "It's") - 0.1, 0.35, 14),
           (T("a1", "cocoa") - 0.1, 0.25, 8), (T("a3", "six") - 0.15, 0.3, 12), (T("b1", "weak") - 0.1, 0.35, 16),
           (T("b2", "winner.") - 0.1, 0.45, 20), (T("b3", "snaps.") - 0.1, 0.4, 18), (T("b3", "thirty-four") - 0.2, 0.3, 12),
           (T("b4", "warmer.") - 0.15, 0.25, 10), (T("c2", "messy") - 0.15, 0.3, 12), (T("c3", "tempering.") - 0.15, 0.35, 14),
           (T("c5", "survives.") - 0.2, 0.3, 12), (T("c6", "way.") - 0.1, 0.3, 12), (T("d2", "mould.") + 0.05, 0.4, 18),
           (T("d2", "bloom.") - 0.15, 0.35, 14), (T("d5", "fridge,") - 0.1, 0.25, 10), (T("d6", "safe") - 0.15, 0.35, 14),
           (T("e1", "Not") - 0.15, 0.35, 14), (T("e2", "cake.") - 0.15, 0.4, 16), (T("f2", "Send") + 0.3, 0.2, 8)]


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
