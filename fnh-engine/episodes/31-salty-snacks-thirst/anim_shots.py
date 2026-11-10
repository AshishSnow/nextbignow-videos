# ================= shots: FreshNestHub 31 — "Why do salty snacks make you thirsty?" (Chubby INK, ep 13 of the ink look) ===
# COLOUR SCRIPT: SALT ORANGE (ACC) = salt only (the crystals' shadow face, the seasoning, SALT words, the checker's alarm). Water = its natural blue,
# cells soft pink, kidneys their own colour. Story = lit places (NEW: the TV ROOM at night with a flickering TV key light; NEW: THE CAPSULE, a mock
# spaceship module with a painted Mars); every explanation = the white BOARD. NO music bed (owner 9 Nov): sound = VO + layered foley (mix.py).
# Craft skill: SOUND DESIGN WITHOUT A MUSIC BED (layered hits, room tone per place, a drop-out before the big moments) + kin_word 'parch'.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "thirsty") - 0.2, "punch"),
    ("S1", T("i2", "And") - 0.1, "whip"), ("S1b", T("i2", "drink") - 0.15, "punch"),
    ("S2", T("i3", "Less") - 0.1, "flash"),
    ("S3", T("a0", "Start") - 0.15, "erase"), ("S3b", T("a0", "The", 1) - 0.1, "punch"),
    ("S4", T("a1", "It") - 0.1, "erase"), ("S4b", T("a1", "so") - 0.1, "punch"),
    ("S5", T("a2", "Salt") - 0.1, "erase"), ("S5b", T("a2", "so") - 0.1, "punch"),
    ("S6", T("a3", "Your") - 0.1, "whip"), ("S6b", T("a3", "Not") - 0.1, "punch"),
    ("S7", T("b1", "Deep") - 0.12, "morph"), ("S7b", T("b1", "It", 1) - 0.1, "punch"),
    ("S8", T("b2", "Its") - 0.1, "erase"),
    ("S9", T("b3", "If") - 0.1, "erase"),
    ("S10", T("b4", "Two") - 0.1, "erase"), ("S10b", T("b4", "keep") - 0.15, "punch"),
    ("S11", T("b5", "And") - 0.1, "whip"),
    ("S12", T("c0", "So") - 0.12, "flash"),
    ("S13", T("c1", "But") - 0.1, "erase"), ("S13b", T("c1", "So") - 0.1, "punch"),
    ("S14", T("c2", "It") - 0.1, "erase"), ("S14b", T("c2", "and", 1) - 0.1, "punch"),
    ("S15", T("c3", "Thats") - 0.1, "whip"), ("S15b", T("c3", "your", 1) - 0.1, "erase"),
    ("S16", T("c4", "And") - 0.1, "erase"), ("S16b", T("c4", "The", 1) - 0.1, "punch"),
    ("S17", T("d0", "Okay") - 0.12, "flash"),
    ("S18", T("d1", "Two") - 0.1, "whip"), ("S18b", T("d1", "for") - 0.1, "punch"),
    ("S19", T("d2", "Same") - 0.1, "punch"),
    ("S20", T("d3", "And") - 0.1, "erase"),
    ("S21", T("d4", "Their") - 0.1, "erase"), ("S21b", T("d4", "helped") - 0.1, "punch"),
    ("S22", T("d5", "Making") - 0.1, "whip"), ("S22b", T("d5", "And") - 0.1, "punch"),
    ("S23", T("e0", "So") - 0.12, "flash"), ("S23b", T("e0", "Over") - 0.1, "punch"),
    ("S24", T("e1", "Salt") - 0.12, "erase"),
    ("S25", T("e2", "Thirsty") - 0.12, "whip"),
    ("S26", T("e3", "Send") - 0.15, "whip"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
_write_on0 = write_on
# MORPH CUT: Chubby's head on the sofa (S6b close-up) -> the board brain
MORPH = {"S7": ((540, 820, 520), (540, 900, 560))}


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
    """phone-size hand lettering (ep 27: the kit default reads too small)."""
    _write_on0(f, text, x, y, t, t0, int(size * 1.3), col, cps, op)


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def t3(f, text, y, t, t0, size=200, face=None, side=None, x=540):
    if t >= t0: title_ink(f, text, y, t, t0, size=size, face=face or ACC_L, side=side or ACC_S, depth=18, x=x)


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, MILK, 22), 540, y, op=clamp((t - t0) / 0.2))


def cc(f, text, x, y, t, t0, bg=None, fg=None, size=34):
    if t >= t0: comp(f, chip(text, bg or INKC, fg or MILK, size), x, y, scale=pin(t, t0))


def kw(f, text, x, y, t, t0, mode="pop", size=130, col=None, **k):
    """kinetic word in hand lettering with an ink stroke (anim_fx.kin_word)."""
    kin_word(f, text, x, y, t, t0, mode, size, col or ACC_S, stroke=2, stroke_col=INKC, **k)


def el_at(f, el, x, y, s=1.0, t=None, t0=None, rot=0.0, op=1.0):
    """place an element; with t/t0 it snaps in (4-frame overshoot)."""
    k = 1.0 if t0 is None else (snap(t, t0, 4) if t >= t0 else 0.0)
    if k > 0.01: rot_comp(f, scale_el(el, s), x, y, rot, k, op, 0.0)


def figure(f, k, cx=540, hy=560, col=BP_INK, w=7):
    """board drawing: a front-view head + torso outline (head first, then the body)."""
    draw_ell_on(f, cx, hy, 150, 160, clamp(k / 0.4), col, w, seed=11)
    kb = clamp((k - 0.4) / 0.6)
    for sg in (-1, 1):
        P = [(cx + sg * 52, hy + 152), (cx + sg * 58, hy + 205), (cx + sg * 210, hy + 250), (cx + sg * 250, hy + 330), (cx + sg * 240, hy + 760), (cx + sg * 150, hy + 830)]
        draw_on(f, P, kb, col, w, seed=12 + sg, tip=sg > 0)


def stamp_x(f, x, y, r, k, col=(176, 40, 44), w=22):
    for sg in (-1, 1): cv2.line(f, (int(x - r * k), int(y - sg * r * k)), (int(x + r * k), int(y + sg * r * k)), C(col), w, cv2.LINE_AA)


def tick(f, x, y, r, k, col=None, w=22):
    col = col or INK_MINT_S
    P = [(x - r, y), (x - r * 0.3, y + r * 0.7), (x + r, y - r * 0.8)]
    draw_on(f, P, k, col, w, seed=5, tip=False)


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look, turn=clamp(look[0]) * 0.5)


def crumbs(f, x, y, t, t0, n=8, spread=180, seed=1, col=None):
    """chip crumbs flying out of a crunch at t0 (ballistic, then gone)."""
    u = t - t0
    if u < 0 or u > 0.9: return
    rng = np.random.default_rng(seed)
    for j in range(n):
        vx = rng.uniform(-1, 1) * spread; vy = -rng.uniform(150, 420)
        px, py = x + vx * u, y + vy * u + 900 * u * u
        r = int(rng.uniform(5, 11)); cv2.circle(f, (int(px), int(py)), r, C(col or CHIP), -1, cv2.LINE_AA); cv2.circle(f, (int(px), int(py)), r, C(INKC), 2, cv2.LINE_AA)


def drops_flow(f, p0, p1, t, n=5, rate=0.7, s=0.32, seed=0, mood="n"):
    """a stream of little water drops travelling p0 -> p1 (on a soft arc)."""
    for j in range(n):
        q = (t * rate + j / n) % 1.0
        x = p0[0] + (p1[0] - p0[0]) * q; y = p0[1] + (p1[1] - p0[1]) * q - 60 * math.sin(math.pi * q)
        el_at(f, wdrop_el(mood if j % 2 == 0 else "happy", seed=319), x, y, s, op=clamp(min(q, 1 - q) * 6))


def sofa_scene(f, t, x=540, s=1.05, **kw_):
    """Chubby on the sofa (sits behind the cushion row) - pass chub kwargs."""
    comp(f, sofa_el(), x, 1340)
    chub(f, x, 1470, s, t=t, sit=True, **kw_)


def bowl_lap(f, x, y, t, level=1.0, s=0.62):
    comp(f, scale_el(chips_bowl_el(level), s), x, y)


def crew(f, x, y, s, t, mood="n", look=(0, 0), talk_=False, kind=0, **k):
    """a crew member in a grey flight jumpsuit (other people = chub(shirt=) + dress)."""
    sh = ((214, 218, 226), (200, 206, 216), (226, 222, 214))[kind % 3]
    m = k.pop("mouth", 0)
    chub(f, x, y, s, t=t, shirt=sh, mouth=talk(t) if talk_ else m, expr=mood, look=look, **k)
    if kind % 3 == 1: dress(f, x, y, s, "cousin", k.get("lean", 0))
    if kind % 3 == 2: dress(f, x, y, s, "boss", k.get("lean", 0))


SUIT = (210, 214, 222)
SRC_MARS = "Source: Rakova et al. + Kitada et al., J Clin Invest (2017)"
SRC_Q = "Source: Quanta Magazine (2025)"


# ---- S0: HOOK, frame 0: movie night, Chubby on the sofa ALREADY crunching a handful of chips (crumbs flying), the question as moving words ----
def shot_S0(t, n):
    f = set_tvroom(t)
    ph = (t * 2.4) % 1.0                                                     # a crunch every 0.42 s
    hand = 150 if ph < 0.45 else 120
    sofa_scene(f, t, 540, 1.08, la=(30, 14), ra=(hand, -128), mouth=(3 if ph < 0.2 else 1) if ph < 0.6 else 0, expr="happy", brow="up", look=(0.2, 0.3), lean=4 * math.sin(t * 3), hand_r="pinch")
    rot_comp(f, scale_el(chip_el(312, bite=min(1.0, t / 1.4)), 0.55), 600, 830 + 6 * math.sin(t * 9), -20, 1.0, 1.0)
    sofa_front(f, 1360)
    bowl_lap(f, 540, 1400, t, 1.0)
    for j in range(5): crumbs(f, 590, 860, t, j * 0.42, 6, 160, seed=3 + j)
    kw(f, "SALTY CHIPS", 540, 330, t, 0.0, "shake", 128, amp=0.6)
    kw(f, "= THIRSTY?", 540, 500, t, 0.55, "parch", 140, t1=1.4, col=WAT_S)
    return finish(f, n, look="night")


# ---- S0b: '...so thirsty?' close-up: the tongue comes out dry, a tumbleweed rolls across ----
def shot_S0b(t, n):
    f = set_tvroom(t); t0 = st_("S0b"); f = dof(f, 4)
    chub_head_only(f, 540, 1000, 2.6, t, mouth="jaw", expr="gross", brow="sad", look=(0, 0.4))
    q = ramp(t, t0, 1.0)
    x = -120 + 1300 * q; a = q * 720
    for k in range(4): cv2.ellipse(f, (int(x), int(1240 - 30 * abs(math.sin(q * 9)))), (60 - k * 12, 54 - k * 10), a + k * 40, 0, 300, C((170, 130, 80)), 5, cv2.LINE_AA)
    kw(f, "THIRSTY?", 540, 380, t, t0 - 0.2, "parch", 160, t1=t0, col=WAT_S)
    return finish(f, n, look="night")


# ---- S1: 'And why, in one long space study, eating more salt...' THE CAPSULE: crew at the console eating trays, Mars in the porthole; a shaker pours ----
def shot_S1(t, n):
    f = set_capsule(t); t0 = st_("S1"); ts = T("i2", "salt") - 0.2
    crew(f, 250, 1500, 0.95, t, "happy", (0.6, 0.3), kind=1, la=(24, 12), ra=(60, 40))
    crew(f, 800, 1500, 0.95, t, "n", (-0.6, 0.3), kind=2, la=(60, 40), ra=(24, 12))
    capsule_front(f, 1330)
    for x in (260, 800): comp(f, scale_el(tray_el(t > ts), 0.75), x, 1310)
    cc(f, "A SPACE STUDY", 540, 330, t, T("i2", "space") - 0.2, INKC, MILK, 50)
    if t > ts:
        a = -130 + 12 * math.sin(t * 20)
        rot_comp(f, scale_el(shaker_el("happy"), 0.75), 540, 1060, a, 1.0, 1.0)
        for j in range(8):
            q = (t * 2 + j / 8) % 1.0; cv2.circle(f, (int(560 + 30 * math.sin(j)), int(1130 + 160 * q)), 5, C(SALTW), -1, cv2.LINE_AA)
        kw(f, "MORE SALT", 540, 480, t, ts, "shake", 120, amp=0.5)
    return finish(f, n, look="cool")


# ---- S1b: '...made people drink less?' a big glass whose water level DROPS, an arrow down, LESS? ----
def shot_S1b(t, n):
    f = set_capsule(t, dim=0.3); t0 = st_("S1b"); f = dof(f, 5)
    lv = 0.85 - 0.55 * ramp(t, T("i2", "less") - 0.2, 0.6)
    comp(f, scale_el(glass2_el(WAT_L, lv), 1.7), 540, 1060)
    draw_arrow_on(f, (860, 820), (860, 1240), ramp(t, T("i2", "less") - 0.2, 0.4), WAT_S, 14)
    kw(f, "LESS?", 540, 420, t, T("i2", "less") - 0.1, "drop", 190, col=WAT_S, t1=en_("S1b") + 5)
    return finish(f, n, look="cool")


# ---- S2: 'Less! I know, it sounds totally backwards.' TV room close: Chubby does a cartoon TAKE; BACKWARDS walks in backwards ----
def shot_S2(t, n):
    f = set_tvroom(t); t0 = st_("S2"); tk = take(t, t0 + 0.05)
    sofa_scene(f, t, 540, 1.25, la=(28, 14), ra=(70, 100), mouth=talk(t), expr=tk["expr"], brow=tk["brow"], look=tk["look"], lean=tk["lean"], squash=tk["squash"])
    sofa_front(f, 1420)
    tb = T("i3", "backwards") - 0.25
    if t > tb:                                                                  # the word arrives right-to-left, letters reversed, then flips round
        q = ramp(t, tb, 0.5); word = "BACKWARDS"
        if q < 0.6: kw(f, word[::-1], 540 + 200 * (1 - q), 400, t, tb, "pop", 120, col=INKC, stagger=0.02)
        else: kw(f, word, 540, 400, t, tb + 0.3, "pop", 120, col=ACC_S, stagger=0.0)
    return finish(f, n, look="night")


# ---- S3: 'Start with the chips.' BOARD: a giant chip, salt crystals sit on it; S3b: '...doesn't just sit on your tongue.' they hop OFF the tongue and down ----
def shot_S3(t, n):
    f = board_bg(); t0 = st_("S3")
    el_at(f, chip_el(316), 540, 1000, 2.6, t, t0 + 0.05)
    for i, (x, y) in enumerate(((420, 930), (620, 900), (540, 1060))):
        el_at(f, salt_el("happy" if i != 1 else "wow", (0, -0.3)), x, y + 6 * math.sin(t * 5 + i), 0.55, t, t0 + 0.4 + 0.12 * i)
    write_on(f, "salt", 860, 760, t, t0 + 0.6, 56, ACC_S)
    draw_arrow_on(f, (830, 790), (650, 880), ramp(t, t0 + 0.8, 0.3), ACC_S, 6)
    peek(f, t, 180, 1360, 0.6, "happy", (0.6, -0.4))
    return finish(f, n, look="fresh")


def shot_S3b(t, n):
    f = board_bg(); t0 = st_("S3b"); ts = T("a0", "tongue") - 0.3
    comp(f, scale_el(tongue_teeth_el(0.0), 1.15), 540, 900)
    for i in range(3):
        q = ramp(t, ts + 0.12 * i, 0.9); x = 460 + 80 * i; y = 980 - 60 * math.sin(math.pi * q) + 520 * q * q
        el_at(f, salt_el("happy", (0, 0.6)), x, y, 0.42, rot=40 * q * (1 if i % 2 else -1))
    draw_arrow_on(f, (540, 1180), (540, 1430), ramp(t, ts + 0.3, 0.4), BP_INK, 8)
    write_on(f, "not just your tongue", 540, 380, t, t0 + 0.1, 46)
    return finish(f, n, look="fresh")


# ---- S4: 'It soaks through the wall of your gut and into your blood,' BOARD cut-away: gut (top) | the WALL | blood vessel (bottom) - salt slips through ----
GUT_Y, WALL_Y, BLOOD_Y = 760, 980, 1230


def gut_wall(f, t, kd=1.0):
    draw_on(f, [(x, WALL_Y - 60 + 10 * math.sin(x / 70)) for x in range(60, 1030, 30)], kd, BP_INK, 7, seed=31, tip=False)
    draw_on(f, [(x, WALL_Y + 60 + 10 * math.sin(x / 70 + 1)) for x in range(60, 1030, 30)], kd, BP_INK, 7, seed=32, tip=False)
    if kd >= 1:
        for x in range(90, 1020, 60): cv2.ellipse(f, (x, WALL_Y), (26, 40), 0, 0, 360, C((246, 196, 196)), -1, cv2.LINE_AA); cv2.ellipse(f, (x, WALL_Y), (26, 40), 0, 0, 360, C(BP_INK), 3, cv2.LINE_AA)
    for sg in (-1, 1): cv2.line(f, (60, BLOOD_Y + sg * 90), (1020, BLOOD_Y + sg * 90), C((200, 60, 60)), 7, cv2.LINE_AA)
    for j in range(7):                                                            # red blood cells drifting along the vessel
        x = (j * 160 + t * 120) % 1100 - 40; cv2.ellipse(f, (int(x), BLOOD_Y + (j % 3 - 1) * 40), (30, 18), 0, 0, 360, C(BLOOD), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(x), BLOOD_Y + (j % 3 - 1) * 40), (30, 18), 0, 0, 360, C(BLOOD_S), 3, cv2.LINE_AA)


def shot_S4(t, n):
    f = board_bg(); t0 = st_("S4"); tw = T("a1", "wall") - 0.2; tb = T("a1", "blood") - 0.3
    gut_wall(f, t, ramp(t, t0, 0.5))
    write_on(f, "your gut", 230, GUT_Y - 150, t, T("a1", "gut") - 0.25, 50)
    write_on(f, "gut wall", 860, WALL_Y - 120, t, tw, 40)
    write_on(f, "blood", 900, BLOOD_Y + 150, t, tb, 50, (176, 40, 44))
    for i, x in enumerate((300, 540, 780)):
        q = ramp(t, tw + 0.25 * i, 1.4)
        y = GUT_Y + (BLOOD_Y - GUT_Y) * q
        el_at(f, salt_el("happy" if q < 0.4 or q > 0.7 else "ouch", (0, 0.6)), x, y, 0.7)
    return finish(f, n, look="fresh")


# ---- S4b: '...so now your blood is a little saltier than it was.' BOARD: the vessel fills with orange salt dots, a SALTIER meter climbs ----
def shot_S4b(t, n):
    f = board_bg(); t0 = st_("S4b"); k = ramp(t, t0, max(0.4, T("a1", "saltier") - t0))
    for sg in (-1, 1): cv2.line(f, (60, 1000 + sg * 150), (1020, 1000 + sg * 150), C((200, 60, 60)), 9, cv2.LINE_AA)
    rng = np.random.default_rng(5)
    for j in range(46):
        x = (rng.uniform(0, 1100) + t * 140) % 1100 - 40; y = 1000 + rng.uniform(-120, 120)
        if j < 8: cv2.ellipse(f, (int(x), int(y)), (30, 18), 0, 0, 360, C(BLOOD), -1, cv2.LINE_AA)
        elif j < 8 + int(38 * k): cv2.rectangle(f, (int(x - 9), int(y - 9)), (int(x + 9), int(y + 9)), C(ACC), -1); cv2.rectangle(f, (int(x - 9), int(y - 9)), (int(x + 9), int(y + 9)), C(INKC), 2)
    kw(f, "SALTIER", 460, 420, t, T("a1", "saltier") - 0.15, "pop", 150)
    write_on(f, "your blood", 540, 1260, t, t0 + 0.1, 50, (176, 40, 44))
    return finish(f, n, look="fresh")


# ---- S5: 'Salt pulls on water like a magnet,' BOARD: a salt crystal holding a horseshoe magnet; water drops slide towards it ----
def shot_S5(t, n):
    f = board_bg(); t0 = st_("S5"); tm = T("a2", "magnet") - 0.3
    el_at(f, salt_el("smirk" if t > tm else "n", (1, 0)), 280, 1000, 1.6, t, t0)
    if t > tm:
        rot_comp(f, scale_el(magnet_el(), 1.0), 500, 930 + 6 * math.sin(t * 8), -90, 1.0, 1.0)
        for j in range(4):
            q = ramp(t, tm + 0.15 * j, 1.2); x = 940 - 330 * q; y = 760 + 120 * j
            el_at(f, wdrop_el("wow", (-1, 0)), x + 40, y + 10 * math.sin(t * 6 + j), 0.75, rot=-20 * q)
            for k in range(3): cv2.line(f, (int(x + 60 + k * 26), int(y)), (int(x + 90 + k * 26), int(y)), C(WAT), 4, cv2.LINE_AA)
    kw(f, "like a MAGNET", 540, 420, t, tm, "pop", 110, col=INKC)
    return finish(f, n, look="fresh")


# ---- S5b: '...so water slides out of your cells to dilute it, and the cells shrink a little.' three cell buddies lose their water and SHRINK ----
def shot_S5b(t, n):
    f = board_bg(); t0 = st_("S5b"); tsh = T("a2", "shrink") - 0.3
    k = ramp(t, t0 + 0.3, max(0.4, tsh + 0.4 - t0))
    for i, x in enumerate((230, 540, 850)):
        el_at(f, cell_buddy_el("sad" if k > 0.5 else "n", (0, -0.2), k, seed=314 + i), x, 1060 + 6 * math.sin(t * 3 + i), 1.25)
        drops_flow(f, (x, 1000), (x + 40, 700), t + i * 0.3, 2, 0.8, 0.3)
    for i, x in enumerate((380, 700)): el_at(f, salt_el("n"), x, 640 + 8 * math.sin(t * 4 + i), 0.5)
    write_on(f, "your cells", 540, 1340, t, t0 + 0.1, 54)
    kw(f, "shrink", 540, 420, t, tsh, "drop", 130, col=INKC, t1=tsh + 0.6)
    return finish(f, n, look="fresh")


# ---- S6: 'Your cells don't like that, and something notices.' TV room: Chubby, hand on belly, then his eyes go up; S6b: 'Not your tongue... Your brain.' ----
def shot_S6(t, n):
    f = set_tvroom(t); t0 = st_("S6"); tn = T("a3", "notices") - 0.2
    k = ramp(t, tn, 0.25)                                                       # eyes lead: down at the belly -> up to the head
    sofa_scene(f, t, 540, 1.12, **nolean(POSE["sick"]), mouth=talk(t), expr="sus", brow="sus" if k < 0.5 else "up", look=(0.3 * k, 0.6 - 1.3 * k), lean=-4 + 3 * k, blink=0.3 < k < 0.6)
    sofa_front(f, 1360)
    bowl_lap(f, 540, 1400, t, 0.5)
    if t > tn: kw(f, "?", 760, 560, t, tn, "pop", 170, col=ACC_S)
    return finish(f, n, look="night")


def shot_S6b(t, n):
    f = set_tvroom(t); t0 = st_("S6b"); tb = T("a3", "brain") - 0.25
    f = dof(f, 4)
    brain_t = t > tb
    chub_head_only(f, 540, 1000, 2.5, t, mouth="jaw" if not brain_t else talk(t), expr="n" if not brain_t else "smirk", brow="up", look=(0, 0.3) if not brain_t else (0.3, -0.8))
    if not brain_t:
        stamp_x(f, 540, 1180, 120, ramp(t, t0 + 0.15, 0.2))
        kw(f, "not your tongue", 540, 380, t, t0 + 0.05, "pop", 100, col=INKC)
    else:
        cv2.circle(f, (540, 700), int(170 * snap(t, tb, 4)), C(ACC), 12, cv2.LINE_AA)
        kw(f, "your BRAIN", 540, 380, t, tb, "pop", 130, col=INKC)
    return finish(f, n, look="night")


# ---- S7: 'Deep inside it, there's a tiny spot that checks your blood all day long.' BOARD brain; an inset zooms into the tiny spot: THE SALT CHECKER ----
def shot_S7(t, n):
    f = board_bg(); t0 = st_("S7"); tt = T("b1", "tiny") - 0.2
    comp(f, scale_el(brain_ink_el("happy", (0, 0)), 1.5), 540, 900)
    if t > tt:
        cv2.circle(f, (560, 960), 16, C(ACC), -1, cv2.LINE_AA)
        k = ramp(t, tt + 0.2, 0.4)
        def dr(g): g[:] = np.array(C(BP_PAPER), np.float32); el_at(g, checker_el("happy", (0, 0), 0.2), 760, 1260, 1.05)
        draw_arrow_on(f, (575, 975), (690, 1130), k, ACC_S, 6)
        inset(f, 760, 1260, 170, dr, k, WHITE, 8)
        write_on(f, "a tiny spot", 300, 1330, t, tt + 0.1, 44, ACC_S)
    write_on(f, "checks your blood all day", 540, 380, t, T("b1", "checks") - 0.2, 42)
    return finish(f, n, look="fresh")


# ---- S7b: 'It doesn't measure water, it measures salt.' BOARD split: a water drop (crossed out) vs a salt crystal (ticked), the checker in the middle ----
def shot_S7b(t, n):
    f = board_bg(); t0 = st_("S7b"); tw = T("b1", "water") - 0.2; ts = T("b1", "salt") - 0.2
    el_at(f, checker_el("sus" if t < ts else "happy", (-0.8 if t < ts else 0.8, 0), 0.2 if t < ts else 0.6), 540, 1320, 1.25)
    el_at(f, wdrop_el("sad"), 280, 880, 1.8, t, tw)
    if t > tw + 0.3: stamp_x(f, 280, 880, 150, ramp(t, tw + 0.3, 0.2))
    el_at(f, salt_el("happy"), 790, 880, 1.6, t, ts)
    if t > ts + 0.25: tick(f, 790, 1100, 70, ramp(t, ts + 0.25, 0.3))
    write_on(f, "measures SALT", 540, 400, t, ts, 60, ACC_S)
    return finish(f, n, look="fresh")


# ---- S8: 'It's got a mouthful of a name, the subfornical organ, but think of it as your salt checker.' ----
def shot_S8(t, n):
    f = board_bg(); t0 = st_("S8"); tn = T("b2", "subfornical") - 0.15; tc = T("b2", "checker") - 0.35
    write_on(f, "subfornical organ", 540, 560, t, tn, 58, cps=26)
    if t < tc - 0.6: peek(f, t, 540, 1100, 1.0, "wow", (0, -0.3), mouth="jaw" if T("b2", "mouthful") - 0.2 < t < T("b2", "subfornical") else None)
    if t > tn + 1.0: hatch_on(f, [(150, 610), (930, 610), (930, 630), (150, 630)], ramp(t, tn + 1.0, 0.4), ACC)
    if t > tc - 0.6:
        q = ramp(t, tc - 0.6, 0.4)
        el_at(f, checker_el("happy", (0, -0.2), 0.3), 540, 1080 - 30 * abs(math.sin(t * 5)) * (t > tc), 1.9 * (0.3 + 0.7 * q))
    if t > tc: ui_word(f, "think of it as your", "SALT [CHECKER]", 370, t, tc, col=INKC, acc=ACC_S, size=96)
    return finish(f, n, look="fresh")


# ---- S9: 'If your blood's water shifts by just one to three percent, it sounds the alarm.' a blood tube's water level dips, the dial climbs, RING ----
def shot_S9(t, n):
    f = board_bg(); t0 = st_("S9"); tp = T("b3", "percent") - 0.3; ta = T("b3", "alarm") - 0.25
    lv = 0.9 - 0.08 * ramp(t, T("b3", "one") - 0.2, 0.8)
    gauge(f, 230, 1010, 520, lv, t, 110, None, WAT)
    write_on(f, "water in your blood", 300, 1360, t, t0 + 0.1, 36)
    if t > tp - 0.2: cc(f, "1-3 %", 230, 680, t, tp - 0.2, WAT_S, MILK, 56)
    ring = t > ta
    sh = 8 * math.sin(t * 60) if ring else 0
    el_at(f, checker_el("wow" if ring else "sus", (-0.6, 0), 0.2 + 0.75 * ramp(t, T("b3", "shifts") - 0.1, 1.2), ring), 720 + sh, 1000, 1.6)
    if ring:
        kw(f, "ALARM!", 600, 430, t, ta, "shake", 160, amp=1.2)
    return finish(f, n, look="fresh")


# ---- S10: 'Two things happen at once. A hormone called vasopressin tells your kidneys,' BOARD: the courier flies to the kidneys; S10b '...keep the water' ----
def shot_S10(t, n):
    f = board_bg(); t0 = st_("S10"); tv = T("b4", "vasopressin") - 0.3; tk = T("b4", "kidneys") - 0.3
    kw(f, "2 THINGS AT ONCE", 540, 360, t, t0 + 0.05, "pop", 96, col=INKC)
    el_at(f, checker_el("wow", (0.6, 0.3), 0.9, True), 250, 760, 1.3)
    el_at(f, kidney_el("n", (-0.6, -0.2)), 780, 1150, 1.4, t, tk - 0.4)
    if t > tv:
        q = ramp(t, tv, 1.4); x = 260 + 470 * q; y = 900 + 240 * q - 120 * math.sin(math.pi * q)
        el_at(f, courier_el("happy", (1, 0.4)), x - 60 * q, y - 80 * q, 1.1, rot=-10 * math.sin(t * 10))
        comp(f, scale_el(envelope_el(), 0.6), x - 60 * q + 90, y - 80 * q + 40)
        write_on(f, "vasopressin", 380, 1380, t, tv + 0.1, 46, WAT_S)
    write_on(f, "your kidneys", 760, 1420, t, tk, 44)
    return finish(f, n, look="fresh")


def shot_S10b(t, n):
    f = board_bg(); t0 = st_("S10b")
    el_at(f, kidney_el("happy", (0, 0.3), hat=True), 540, 1000, 1.35)
    for j in range(5):
        a = t * 1.4 + j * 2 * math.pi / 5; el_at(f, wdrop_el("happy"), 540 + 260 * math.cos(a), 1000 + 200 * math.sin(a), 0.45)
    ui_word(f, "", "KEEP THE [WATER]", 380, t, t0 + 0.05, col=INKC, acc=WAT_S, size=110)
    write_on(f, "don't send it out", 540, 1380, t, T("b4", "dont") - 0.2, 46)
    return finish(f, n, look="fresh")


# ---- S11: 'And you get that dry, I need a glass right now feeling. That's thirst.' TV room: parched Chubby reaches for a glass ----
def shot_S11(t, n):
    f = set_tvroom(t); t0 = st_("S11"); tt = T("b5", "thirst") - 0.3
    reach = ramp(t, T("b5", "glass") - 0.3, 0.4)
    sofa_scene(f, t, 470, 1.15, la=(30, 14), ra=(60 + 40 * reach, 40 - 30 * reach), mouth="jaw" if t < tt else talk(t), expr="gross", brow="sad", look=(0.8, 0), lean=-6 - 8 * reach, hand_r="open")
    sofa_front(f, 1360)
    comp(f, scale_el(glass2_el(WAT_L, 0.85), 0.9), 900, 1240)
    kw(f, "THIRST", 540, 400, t, tt, "parch", 170, t1=tt + 0.2, col=WAT_S)
    return finish(f, n, look="night")


# ---- S12: 'So you grab a glass, you drink, and you feel better almost straight away.' WORKTOP: he gulps it down, relief ----
def shot_S12(t, n):
    f = set_worktop(t); t0 = st_("S12"); td = T("c0", "drink") - 0.2; tb = T("c0", "better") - 0.2
    tilt = ramp(t, td, 0.4)
    chub(f, 540, 1520, 1.15, t=t, la=(24, 12), ra=(120 + 30 * tilt, -100 - 40 * tilt), mouth=0 if t < tb else 3, expr="n" if t < tb else "happy", brow="up", look=(0, -0.4 * tilt), lean=-6 * tilt, hand_r="grip")
    worktop_front(f, 1330)
    hx, hy = 540 + 120, 1520 - 520 * 1.15 + 120
    rot_comp(f, scale_el(glass2_el(WAT_L, 0.9 - 0.7 * ramp(t, td, max(0.5, tb - td))), 0.75), hx, hy - 40 * tilt, 40 * tilt, 1.0, 1.0)
    if t > tb:
        for j in range(6):
            a = j * math.pi / 3 + t; r = 260 + 20 * math.sin(t * 6); cv2.line(f, (int(540 + r * math.cos(a)), int(820 + r * math.sin(a))), (int(540 + (r + 40) * math.cos(a)), int(820 + (r + 40) * math.sin(a))), C(WAT), 6, cv2.LINE_AA)
        kw(f, "ahh", 540, 380, t, tb, "breathe", 150, col=WAT_S)
    return finish(f, n, look="golden")


# ---- S13: 'But water takes thirty to sixty minutes to actually reach your blood.' BOARD: a 0-60 min ruler, a water drop strolls along it ----
def ruler60(f, t, t0, y=1000):
    draw_on(f, [(120, y), (960, y)], ramp(t, t0, 0.4), BP_INK, 8, seed=41, tip=False)
    for m in range(0, 61, 10):
        x = 120 + 840 * m / 60; cv2.line(f, (int(x), y - 22), (int(x), y + 22), C(BP_INK), 6, cv2.LINE_AA)
        if t > t0 + 0.3: write_on(f, str(m), x, y + 80, t, t0 + 0.3, 30)
    write_on(f, "minutes", 540, y + 170, t, t0 + 0.5, 40)


def shot_S13(t, n):
    f = board_bg(); t0 = st_("S13"); tm = T("c1", "thirty") - 0.2
    ruler60(f, t, t0)
    if t > tm: hatch_on(f, [(540, 960), (960, 960), (960, 1040), (540, 1040)], ramp(t, tm, 0.6), WAT)
    q = ramp(t, t0 + 0.3, 3.5)
    el_at(f, wdrop_el("happy", (1, 0)), 120 + 600 * q, 900 - 20 * abs(math.sin(t * 7)), 0.55)
    comp(f, clock_ink_el(80), 860, 640); clock_hands(f, 860, 640, 3 + 4 * (t - t0), 80)
    kw(f, "30-60 min", 420, 600, t, tm, "pop", 120, col=WAT_S)
    write_on(f, "to reach your blood", 540, 380, t, T("c1", "reach") - 0.2, 44)
    return finish(f, n, look="fresh")


# ---- S13b: 'So how does your brain know when to stop?' the checker scratches its head next to a big question mark ----
def shot_S13b(t, n):
    f = board_bg(); t0 = st_("S13b")
    el_at(f, checker_el("sus", (0.6, -0.4), 0.85, False), 420, 1000 + 8 * math.sin(t * 4), 1.6)
    kw(f, "?", 820, 900, t, t0 + 0.2, "pop", 360, col=ACC_S)
    kw(f, "when to STOP?", 540, 420, t, T("c1", "stop") - 0.3, "pop", 120, col=INKC)
    return finish(f, n, look="fresh")


# ---- S14: 'It takes a shortcut. Your mouth and throat feel the gulps, your gut checks the salt,' BOARD body: dotted SHORTCUT arrows to the brain ----
def shot_S14(t, n):
    f = board_bg(); t0 = st_("S14"); tm = T("c2", "mouth") - 0.2; tg = T("c2", "gut") - 0.2
    figure(f, 1.0, 540, 520)
    for j in range(3):                                                           # gulps travelling down the throat
        q = ((t - tm) * 1.2 + j / 3) % 1.0
        if t > tm: el_at(f, wdrop_el("happy"), 540, 700 + 420 * q, 0.3)
    if t > tm:
        cc(f, "GULP", 760, 700, t, tm, WAT_S, MILK, 40)
        draw_arrow_on(f, (600, 690), (600, 520), ramp(t, tm + 0.3, 0.3), ACC_S, 7)
    if t > tg:
        comp(f, scale_el(stomach_ink_el("happy", (0, -0.4)), 0.6), 540, 1180, scale=snap(t, tg, 4))
        draw_arrow_on(f, (640, 1120), (640, 560), ramp(t, tg + 0.2, 0.5), ACC_S, 7, bend=0.25)
        write_on(f, "checks the salt", 820, 1380, t, tg, 40)
    kw(f, "SHORTCUT", 540, 340, t, T("c2", "shortcut") - 0.2, "sneak", 120, stagger=0.05)
    return finish(f, n, look="fresh")


# ---- S14b: '...and within a minute, the thirst switches off.' the checker's dial drops, the bell stops; a stopwatch '1 min' ----
def shot_S14b(t, n):
    f = board_bg(); t0 = st_("S14b"); to = T("c2", "off") - 0.3
    off = t > to
    el_at(f, checker_el("happy" if off else "wow", (0, 0), 0.9 - 0.75 * ramp(t, t0 + 0.3, max(0.4, to - t0)), not off), 540, 1050, 1.7)
    comp(f, scale_el(stopwatch_el("1 min", INK), 0.7), 800, 640, scale=pin(t, T("c2", "minute") - 0.3))
    if off: kw(f, "OFF", 380, 420, t, to, "pop", 170, col=INK_MINT_S)
    return finish(f, n, look="fresh")


# ---- S15: 'That's why sea water never works. Your mouth says ahh,' DUSK BEACH: Chubby sips from a glass of sea water, waves behind ----
def shot_S15(t, n):
    t0 = st_("S15"); f = inkify(set_dusk(t)); ta = T("c3", "ahh") - 0.3
    for k in range(3):                                                           # waves on the horizon
        y = 1150 + k * 30; P = np.array([(x, y + 10 * math.sin(x / 50 + t * 2 + k)) for x in range(0, W + 20, 20)], np.int32)
        cv2.polylines(f, [P], False, C((90, 150, 200)), 8, cv2.LINE_AA)
    tilt = ramp(t, t0 + 0.4, 0.4)
    chub(f, 540, 1500, 1.15, t=t, la=(24, 12), ra=(120 + 30 * tilt, -100 - 40 * tilt), mouth=3 if t > ta else 0, expr="happy" if t > ta else "n", brow="up", look=(0, -0.3), lean=-5 * tilt, hand_r="grip")
    rot_comp(f, scale_el(glass2_el((150, 200, 190), 0.8), 0.75), 660, 1520 - 520 * 1.15 + 120 - 40 * tilt, 40 * tilt, 1.0, 1.0)
    cc(f, "SEA WATER", 540, 330, t, t0 + 0.1, (60, 120, 150), MILK, 52)
    if t > ta: kw(f, "ahh...", 540, 480, t, ta, "breathe", 120, col=WAT_S)
    return finish(f, n, look="golden")


# ---- S15b: '...your gut tastes the salt, and the thirst comes right back.' BOARD: the gut frowns at salt, the checker's bell rings AGAIN ----
def shot_S15b(t, n):
    f = board_bg(); t0 = st_("S15b"); tb = T("c3", "back") - 0.4
    el_at(f, stomach_ink_el("ouch" if t > t0 + 0.6 else "n", (0.5, 0)), 320, 1080, 1.6)
    for j in range(4): el_at(f, salt_el("smirk"), 220 + 70 * j, 1260 + 20 * math.sin(t * 5 + j), 0.42)
    ring = t > tb
    el_at(f, checker_el("wow" if ring else "sus", (-0.6, 0.3), 0.9 if ring else 0.5, ring), 800 + (6 * math.sin(t * 60) if ring else 0), 900, 1.2)
    draw_arrow_on(f, (420, 980), (680, 900), ramp(t, t0 + 0.6, 0.4), ACC_S, 7)
    write_on(f, "salty water", 320, 1400, t, t0 + 0.1, 44, ACC_S)
    if ring: kw(f, "BACK ON", 540, 420, t, tb, "shake", 140, amp=1.0)
    return finish(f, n, look="fresh")


# ---- S16: 'And in mice, these thirst cells fire while they're still eating, before the blood even changes.' BOARD: a mouse munches, the bell rings, the blood meter hasn't moved ----
def shot_S16(t, n):
    f = board_bg(); t0 = st_("S16"); te = T("c4", "eating") - 0.3
    comp(f, scale_el(mouse_el(chew=(t * 6) % 1 < 0.5), 1.25), 330, 1050)
    for j in range(3): cv2.ellipse(f, (int(470 + 30 * j), 1150), (14, 9), 20 * j, 0, 360, C((220, 190, 120)), -1, cv2.LINE_AA)
    ring = t > te
    el_at(f, checker_el("wow" if ring else "n", (-0.6, 0.3), 0.7 if ring else 0.2, ring), 800, 820, 0.95)
    gauge(f, 840, 1220, 300, 0.5, t, 80, None, (200, 60, 60))
    write_on(f, "blood: no change yet", 560, 1400, t, T("c4", "blood") - 0.2, 36)
    write_on(f, "in mice", 540, 380, t, T("c4", "mice") - 0.2, 56, ACC_S)
    src(f, "Source: Knight lab, UCSF, Nature (2016), via STAT", t, t0 + 0.3, 1480)
    return finish(f, n, look="fresh")


# ---- S16b: 'The brain sees the salt coming.' the checker with binoculars spots a salt crystal far off ----
def shot_S16b(t, n):
    f = board_bg(); t0 = st_("S16b")
    el_at(f, checker_el("smirk", (1, -0.2), 0.4), 280, 1050, 1.3)
    for sg in (-1, 1): cv2.circle(f, (330 + sg * 26, 950), 26, C(INKC), 8, cv2.LINE_AA)
    q = ramp(t, t0, 1.6)
    el_at(f, salt_el("happy", (-1, 0)), 960 - 180 * q, 820 + 10 * math.sin(t * 6), 0.4 + 0.3 * q)
    draw_arrow_on(f, (420, 950), (760, 840), ramp(t, t0 + 0.3, 0.4), BP_INK, 6, bend=-0.1)
    kw(f, "sees it coming", 540, 420, t, T("c4", "sees") - 0.2, "sneak", 100, col=INKC)
    return finish(f, n, look="fresh")


# ---- S17: 'Okay, so let's go back to that space study.' THE CAPSULE: a big ink title SPACE STUDY, Chubby in a jumpsuit points at the porthole ----
def shot_S17(t, n):
    f = set_capsule(t); t0 = st_("S17")
    t3(f, "PART 2", 300, t, t0 + 0.05, 120)
    t3(f, "MARS?", 470, t, T("d0", "space") - 0.2, 190)
    chub(f, 380, 1500, 1.1, t=t, shirt=SUIT, **nolean(POSE["point"]), lean=4, mouth=talk(t), expr="happy", brow="up", look=(1, -0.3), turn=0.5, hand_r="point")
    capsule_front(f, 1330)
    return finish(f, n, look="cool")


# ---- S18: 'Two crews of ten men lived sealed inside a pretend spaceship, on a fake trip to Mars,' a row of crew; the hatch seals; '2 CREWS x 10' ----
def shot_S18(t, n):
    f = set_capsule(t); t0 = st_("S18"); tm = T("d1", "Mars") - 0.3
    for i, x in enumerate((150, 340, 540, 740, 930)):
        crew(f, x, 1500 + (i % 2) * 30, 0.7, t, "happy" if i % 2 else "n", (0, 0.2), kind=i, la=(24, 12), ra=(24, 12), lean=3 * math.sin(t * 2 + i))
    capsule_front(f, 1380)
    cc(f, "2 CREWS x 10 MEN", 540, 330, t, T("d1", "ten") - 0.2, INKC, MILK, 50)
    if t > tm: cc(f, "A PRETEND TRIP TO MARS", 540, 440, t, tm, MARS_S, MILK, 40)
    return finish(f, n, look="cool")


# ---- S18b: '...for up to two hundred and five days.' the locker calendar counts up: 205 DAYS ----
def shot_S18b(t, n):
    f = set_capsule(t); t0 = st_("S18b"); f = dof(f, 3)
    v = count_up(t, t0 + 0.2, 205, 1.6)
    comp(f, scale_el(calendar_el("DAYS", str(v)), 1.5), 540, 980, scale=pin(t, t0))
    cc(f, "105 days + 205 days", 540, 1380, t, t0 + 0.6, INKC, MILK, 40)
    src(f, SRC_MARS, t, t0 + 0.4, 1462)
    return finish(f, n, look="cool")


# ---- S19: 'Same food every day, only the salt went up and down, a few weeks at a time.' trays + a 3-step salt chart that steps up and down ----
def shot_S19(t, n):
    f = set_capsule(t, dim=0.2); t0 = st_("S19")
    comp(f, scale_el(tray_el(False), 1.0), 540, 640)
    g = f.copy(); cv2.rectangle(g, (110, 860), (970, 1400), C(BP_PAPER), -1); f[:] = f * 0.1 + g * 0.9
    cv2.rectangle(f, (110, 860), (970, 1400), C(INKC), 5, cv2.LINE_AA)
    levels = [0.8, 0.55, 0.3, 0.55, 0.8]
    kk = ramp(t, t0 + 0.4, max(0.5, en_("S19") - t0 - 0.8))
    P = []
    for i, lv in enumerate(levels):
        x0 = 160 + 160 * i; y = 1340 - 380 * lv; P += [(x0, y), (x0 + 160, y)]
    draw_on(f, P, kk, ACC_S, 12, seed=51, tip=True)
    write_on(f, "salt", 220, 920, t, t0 + 0.3, 40, ACC_S); write_on(f, "weeks", 860, 1370, t, T("d2", "weeks") - 0.2, 36)
    write_on(f, "same food every day", 540, 380, t, t0 + 0.05, 46, INKC)
    return finish(f, n, look="cool")


# ---- S20: 'And when the salt went up, they didn't drink more. They drank less.' BOARD bar chart: SALT up, WATER DRUNK down; LESS ----
def shot_S20(t, n):
    f = board_bg(); t0 = st_("S20"); tu = T("d3", "up") - 0.2; tl = T("d3", "less") - 0.3
    base = 1300
    hs = 160 + 360 * ramp(t, tu, 0.5)
    cv2.rectangle(f, (220, int(base - hs)), (440, base), C(ACC), -1); cv2.rectangle(f, (220, int(base - hs)), (440, base), C(INKC), 5)
    el_at(f, salt_el("happy"), 330, base - hs - 80, 0.5)
    hw = 420 - 200 * ramp(t, tl, 0.5)
    cv2.rectangle(f, (640, int(base - hw)), (860, base), C(WAT), -1); cv2.rectangle(f, (640, int(base - hw)), (860, base), C(INKC), 5)
    el_at(f, wdrop_el("sad" if t > tl else "n"), 750, base - hw - 80, 0.5)
    cv2.line(f, (160, base), (920, base), C(BP_INK), 7, cv2.LINE_AA)
    write_on(f, "salt eaten", 330, base + 80, t, t0 + 0.1, 36); write_on(f, "water drunk", 750, base + 80, t, t0 + 0.3, 36)
    if t > tu: draw_arrow_on(f, (490, base - 100), (490, base - hs + 40), ramp(t, tu, 0.3), ACC_S, 10)
    if t > tl: draw_arrow_on(f, (910, base - 420), (910, base - hw + 60), ramp(t, tl, 0.3), WAT_S, 10)
    kw(f, "LESS", 540, 440, t, tl, "drop", 200, col=WAT_S, t1=en_("S20") + 5)
    if t < tl: kw(f, "not more...", 540, 440, t, T("d3", "more") - 0.3, "pop", 110, col=INKC)
    return finish(f, n, look="fresh")


# ---- S21: 'Their kidneys held on to water instead,' BOARD: the kidney hugs the drops; S21b: '...with help from a waste product called urea' UREA pulls water back on a rope ----
def shot_S21(t, n):
    f = board_bg(); t0 = st_("S21")
    el_at(f, kidney_el("happy", (0, 0.3), hat=True), 540, 1000, 1.8, t, t0 + 0.05)
    for j, (x, y) in enumerate(((250, 880), (830, 880), (290, 1170), (790, 1170))):
        el_at(f, wdrop_el("happy"), x + 10 * math.sin(t * 3 + j), y + 8 * math.cos(t * 4 + j), 0.7, t, t0 + 0.4 + 0.12 * j)
    write_on(f, "held on to water", 540, 400, t, T("d4", "held") - 0.2, 48, WAT_S)
    return finish(f, n, look="fresh")


def shot_S21b(t, n):
    f = board_bg(); t0 = st_("S21b"); tu = T("d4", "urea") - 0.3; tp = T("d4", "pulls") - 0.3
    el_at(f, kidney_el("n", (0.6, 0)), 220, 1000, 1.3)
    if t > tu:
        el_at(f, urea_el("happy", (1, 0)), 500, 1010, 1.4, t, tu)
        q = ramp(t, tp, 1.2)
        for j in range(3):
            x = 900 - 250 * q - 70 * j; cv2.line(f, (590, 940), (int(x), int(900 + 60 * j)), C((150, 104, 60)), 7, cv2.LINE_AA)
            el_at(f, wdrop_el("wow" if q < 0.5 else "happy", (-1, 0)), x, 900 + 60 * j, 0.6)
        write_on(f, "urea", 520, 1220, t, tu + 0.1, 60, UREA_S)
        write_on(f, "a waste product", 520, 1340, t, T("d4", "waste") - 0.3, 38)
    kw(f, "pulls water back", 540, 420, t, tp, "pop", 96, col=INKC)
    return finish(f, n, look="fresh")


# ---- S22: 'Making all that urea takes energy.' CAPSULE: a battery drains; S22b: '...the crew on the salty food kept saying they were hungry.' tummies rumble ----
def shot_S22(t, n):
    f = set_capsule(t, dim=0.15); t0 = st_("S22")
    lv = 1.0 - 0.7 * ramp(t, t0 + 0.2, 1.4)
    comp(f, scale_el(battery_el(lv, "ENERGY"), 1.4), 540, 960, scale=pin(t, t0))
    el_at(f, urea_el("happy"), 820, 1220 + 10 * math.sin(t * 6), 1.0)
    kw(f, "takes ENERGY", 540, 420, t, T("d5", "energy") - 0.2, "pop", 110, col=INKC)
    return finish(f, n, look="cool")


def shot_S22b(t, n):
    f = set_capsule(t); t0 = st_("S22b"); th = T("d5", "hungry") - 0.3
    for i, x in enumerate((250, 540, 830)):
        crew(f, x, 1500, 0.9, t, "sad" if t > th else "sus", (0, 0.4), kind=i, la=(26, -112), ra=(26, -112), lean=-4 + 2 * math.sin(t * 9 + i) * (t > th))
    capsule_front(f, 1330)
    for x in (250, 540, 830): comp(f, scale_el(tray_el(True), 0.6), x, 1310)
    if t > th: kw(f, "HUNGRY", 540, 400, t, th, "shake", 160, amp=0.8)
    else: cc(f, "SALTY FOOD WEEKS", 540, 400, t, t0 + 0.1, ACC_S, MILK, 44)
    return finish(f, n, look="cool")


# ---- S23: 'So the thirst after chips is real, but it's short.' TV room: Chubby with chips + water, SHORT ; S23b: 'Over weeks, your body plays a longer game...' ----
def shot_S23(t, n):
    f = set_tvroom(t); t0 = st_("S23"); ts = T("e0", "short") - 0.25
    sofa_scene(f, t, 540, 1.1, **nolean(POSE["shrug"]), mouth=talk(t), expr="smirk", brow="up", look=(0.2, -0.1))
    sofa_front(f, 1360)
    bowl_lap(f, 380, 1400, t, 0.25, 0.5)
    comp(f, scale_el(glass2_el(WAT_L, 0.6), 0.6), 760, 1340)
    kw(f, "REAL", 540, 340, t, T("e0", "real") - 0.2, "pop", 130, col=INKC)
    if t > ts: kw(f, "but SHORT", 540, 500, t, ts, "pop", 120)
    return finish(f, n, look="night")


def shot_S23b(t, n):
    f = board_bg(); t0 = st_("S23b"); tsc = T("e0", "scientists") - 0.3
    comp(f, scale_el(stopwatch_el("now", INK), 0.8), 260, 900)
    comp(f, scale_el(calendar_el("WEEKS", "?"), 0.9), 800, 900, scale=pin(t, t0 + 0.2))
    draw_arrow_on(f, (380, 900), (640, 900), ramp(t, t0 + 0.2, 0.4), BP_INK, 8)
    write_on(f, "a longer game", 540, 1260, t, T("e0", "longer") - 0.2, 52, ACC_S)
    if t > tsc:
        for j in range(3): kw(f, "?", 300 + 240 * j, 1430, t, tsc + 0.15 * j, "pop", 110, col=BP_INK)
        write_on(f, "still being worked out", 540, 400, t, tsc, 42)
    return finish(f, n, look="fresh")


# ---- S24: RECAP chain map 'Salt into your blood, water out of your cells, your salt checker sounds the alarm, you drink, and your mouth and gut switch it off.' ----
def recap_items():
    return [(scale_el(salt_el("happy"), 0.42), "SALT IN"), (scale_el(cell_buddy_el("sad", k=0.8), 0.38), "CELLS SHRINK"), (scale_el(checker_el("wow", ring=True, needle=0.9), 0.36), "ALARM"),
            (scale_el(glass2_el(WAT_L, 0.8), 0.35), "DRINK"), (scale_el(checker_el("happy", needle=0.2), 0.36), "OFF")]


def shot_S24(t, n):
    f = board_bg(); t0 = st_("S24")
    keys = [T("e1", "Salt") - 0.1, T("e1", "water") - 0.1, T("e1", "checker") - 0.3, T("e1", "drink") - 0.2, T("e1", "switch") - 0.2]
    cur = -1; tc = t0
    for i, k_ in enumerate(keys):
        if t >= k_: cur, tc = i, k_
    big = [lambda: salt_el("happy"), lambda: cell_buddy_el("sad", k=0.8), lambda: checker_el("wow", needle=0.9, ring=True), lambda: glass2_el(WAT_L, 0.8), lambda: checker_el("happy", needle=0.2)]
    if cur >= 0: el_at(f, big[cur](), 540, 860, 1.5, t, tc)
    chain_map(f, recap_items(), cur, t, tc, y=1300, gap=170, r=56)
    comp(f, chip("THE WHOLE STORY", INKC, ACC_L, 34), 540, 330)
    return finish(f, n, look="fresh")


# ---- S25: 'Thirsty after a salty snack? Plain water is the fix. Another handful of chips is not.' WORKTOP: water gets a tick, the chip hand gets a STOP ----
def shot_S25(t, n):
    f = set_worktop(t); t0 = st_("S25"); tw = T("e2", "water") - 0.2; tn = T("e2", "Another") - 0.2
    nope = t > tn
    chub(f, 540, 1500, 1.1, t=t, **(nolean(POSE["stop"]) if nope else nolean(POSE["hold_up"])), mouth=talk(t), expr="smirk" if nope else "happy", brow="up", look=(0.6, 0) if nope else (-0.3, -0.3), hand_r="open" if nope else "grip")
    worktop_front(f, 1330)
    if not nope:
        comp(f, scale_el(glass2_el(WAT_L, 0.9), 0.8), 680, 840)
        if t > tw: tick(f, 840, 640, 60, ramp(t, tw, 0.3))
        kw(f, "PLAIN WATER", 540, 380, t, tw, "pop", 120, col=WAT_S)
    else:
        comp(f, scale_el(chips_bowl_el(1.0), 0.6), 740, 1300)
        stamp_x(f, 740, 1250, 110, ramp(t, tn + 0.3, 0.2))
        kw(f, "not more chips", 540, 380, t, tn, "pop", 100, col=INKC)
    return finish(f, n, look="golden")


# ---- S26: 'Send this to the friend who finishes the whole packet of chips, and then the whole bottle of water.' TV room: the friend with an empty packet + a giant bottle; logo ----
FRIEND = (236, 150, 110)


def shot_S26(t, n):
    t0 = st_("S26"); f = set_tvroom(t); vend = LINES["e3"]["end"] + 0.15; tb = T("e3", "bottle") - 0.3
    if t < vend + 0.2:
        chub(f, 330, 1500, 1.0, t=t, **nolean(POSE["shrug"]), mouth=3, expr="happy", brow="up", look=(1, 0), turn=0.5)
        glug = t > tb
        chub(f, 760, 1500, 1.05, t=t, shirt=FRIEND, la=(30, 14), ra=(150, -128) if glug else (60, 40), mouth="o" if glug else 1, expr="happy", brow="up", look=(0, -0.5) if glug else (-0.5, 0), lean=-8 if glug else 0, hand_r="grip")
        dress(f, 760, 1500, 1.05, "cousin")
        sofa_front(f, 1420)
        comp(f, scale_el(packet_el(), 0.45), 880, 1300)
        if glug: rot_comp(f, scale_el(glass2_el(WAT_L, 0.3 + 0.5 * (1 - ramp(t, tb, 1.0))), 0.8), 800, 860, 150, 1.0, 1.0)
        comp(f, scale_el(phone2_el("finished the chips", "and the water?!", t > T("e3", "Send") + 0.3), 0.55), 540, 760, scale=pin(t, t0))
        ui_word(f, "send this to the friend who", "FINISHES [EVERYTHING]", 380, t, T("e3", "Send") - 0.05, col=WHITE, acc=ACC_L, size=88, shadow=0.6, lead_col=WHITE)
    else:
        f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32); k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 760, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1500, 0.62, t=t, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up")
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(0.42, 0.25, 6), (T("i1", "thirsty") - 0.2, 0.3, 10), (T("i2", "less") - 0.1, 0.35, 12), (T("i3", "Less") - 0.05, 0.3, 10),
           (T("a1", "blood") - 0.2, 0.25, 8), (T("a1", "saltier") - 0.15, 0.3, 10), (T("a2", "magnet") - 0.3, 0.3, 10), (T("a2", "shrink") - 0.3, 0.3, 10),
           (T("a3", "brain") - 0.25, 0.35, 12), (T("b1", "salt") - 0.2, 0.3, 10), (T("b2", "checker") - 0.35, 0.3, 10), (T("b3", "alarm") - 0.25, 0.5, 18),
           (T("b4", "keep") - 0.15, 0.3, 10), (T("b5", "thirst") - 0.3, 0.35, 12), (T("c0", "better") - 0.2, 0.25, 8), (T("c1", "stop") - 0.3, 0.3, 10),
           (T("c2", "off") - 0.3, 0.3, 10), (T("c3", "back") - 0.4, 0.4, 14), (T("c4", "eating") - 0.3, 0.3, 10), (T("d0", "space") - 0.2, 0.3, 10),
           (T("d1", "Mars") - 0.3, 0.25, 8), (T("d3", "less") - 0.3, 0.45, 16), (T("d4", "urea") - 0.3, 0.25, 8), (T("d5", "hungry") - 0.3, 0.35, 12),
           (T("e0", "short") - 0.25, 0.3, 10), (T("e2", "not") - 0.2, 0.3, 10), (T("e3", "bottle") - 0.3, 0.3, 10)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


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
